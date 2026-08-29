"""Thesis data collection: solve, validate, then explain the resulting Pareto fronts.

One run covers every quantity the thesis reports, in the order the argument is made.

The front is produced by the author's own metaheuristic family -- ``run_mp_brkga`` at his
published configuration, with single-population ``run_brkga`` alongside -- and **no surrogate
takes any part in generating it**. The surrogate is fitted afterwards and applied post hoc to the
finished front, which is the role the supervisor's scope assigns it.

Four groups of measurements are recorded per (instance, seed):

*Front quality.* Cardinality, hypervolume against a reference shared by both arms, IGD+ against
their non-dominated union, spacing and spread, and the two boundary solutions. Where published
optima exist the boundaries are checked for **weak dominance** rather than equality: three speed
levels are available here against the single level of the published scenario, and the additional
levels are respectively faster and more energy-efficient than nominal, so a correct solver must
reach at least the published boundary on each objective and may pass it.

*Surrogate calibration.* Held-out coefficient of determination and absolute error for both
objectives. The energy figure is reported for completeness only: the readout sums the arc energy
features and the objective is exactly that sum, so unity is a property of the architecture rather
than evidence of learning.

*Attribution faithfulness.* Leg and arc critical-path agreement between the fused model's own
tropical gradients and the exact oracle, over the front itself rather than over random schedules,
since the front is what the thesis explains.

*Front behaviour.* The duration-weighted transport share at each end of the front and its
movement between them, computed identically from the exact oracle and from the model, together
with the local trade-off weight swept by the front.

Usage::

    python scripts/run_thesis_experiments.py --set L --seeds 10
    python scripts/run_thesis_experiments.py --set DL --seeds 5 --workers 8
    python scripts/run_thesis_experiments.py --set fleet --instances L15 --agv-sweep 1 2 3 4 6 8
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import numpy as np
from scipy import stats as sps

OUT_DIR = REPO / "experiments" / "thesis"
L_DATA = REPO / "data" / "tables_4_5.json"


def _load(instance_id: str, num_agvs: int | None):
    """Load one published instance, optionally overriding the fleet size."""
    from dataclasses import replace

    from ehgat.environment.dsdl import load_dl_instances, load_tables_4_5

    if instance_id.startswith("DL"):
        inst = load_dl_instances(only=[instance_id])[0].instance
    else:
        inst = load_tables_4_5(L_DATA, only=[instance_id])[0].instance
    if num_agvs is not None and num_agvs != inst.num_agvs:
        inst = replace(inst, num_agvs=num_agvs)
    return inst


def _front_quality(arms: dict[str, list[tuple[float, float]]]) -> dict:
    """Cardinality, hypervolume, IGD+, spacing and spread per arm on a shared reference."""
    from ehgat.metrics import hypervolume, igd_plus, nadir_reference, spacing, spread
    from ehgat.search.nsga2 import non_dominated_indices

    populated = [f for f in arms.values() if f]
    if not populated:
        return {}
    reference = nadir_reference(*populated, margin=0.1)
    union = [p for f in populated for p in f]
    keep = non_dominated_indices([tuple(map(float, p)) for p in union])
    union_nd = [union[i] for i in keep]

    out: dict[str, dict] = {}
    for name, front in arms.items():
        if not front:
            out[name] = {"n": 0}
            continue
        objs = np.asarray(front, dtype=float)
        order = np.argsort(objs[:, 0])
        out[name] = {
            "n": len(front),
            "hypervolume": float(hypervolume(front, reference)),
            "igd_plus": float(igd_plus(front, union_nd)),
            "spacing": float(spacing(front)),
            "spread": float(spread(front)),
            "makespan_min": float(objs[order[0], 0]),
            "energy_at_makespan_min": float(objs[order[0], 1]),
            "energy_min": float(objs[:, 1].min()),
            "makespan_at_energy_min": float(objs[order[-1], 0]),
        }
    out["_reference"] = {"nadir": list(map(float, reference)), "union_n": len(union_nd)}
    return out


def _front_behaviour(instance, schedules: list, model=None) -> dict:
    """Transport share at both ends of the front, its migration, and the lambda sweep."""
    from ehgat.explain.critical_share import (
        critical_path_shares,
        exact_critical_shares,
        migration,
    )
    from ehgat.explain.fused_explainer import explain_fused
    from ehgat.explain.tape_explainer import explain_schedule
    from ehgat.explain.tcs_calculator import ParetoPoint, local_lambda
    from ehgat.environment.evaluator import evaluate

    if len(schedules) < 2:
        return {"n_front": len(schedules)}

    evaluated = [(s, evaluate(s, instance)) for s in schedules]
    evaluated.sort(key=lambda pair: (pair[1].makespan, pair[1].energy))
    mk_end, en_end = evaluated[0][0], evaluated[-1][0]

    exact_mk = exact_critical_shares(mk_end, instance)
    exact_en = exact_critical_shares(en_end, instance)
    out = {
        "n_front": len(schedules),
        "exact": {
            "rho_makespan_end": exact_mk.transport,
            "rho_energy_end": exact_en.transport,
            "migration": migration(exact_mk, exact_en),
            "decomposition_closes": bool(exact_mk.closes and exact_en.closes),
        },
    }

    # The lambda sweep needs the exact explanations of every front point, which are cheap.
    points = [
        ParetoPoint(str(i), ev.makespan, ev.energy, explain_schedule(s, instance))
        for i, (s, ev) in enumerate(evaluated)
    ]
    lambdas = [local_lambda(points, i) for i in range(len(points))]
    out["lambda_min"] = float(min(lambdas))
    out["lambda_max"] = float(max(lambdas))
    out["lambda_span"] = float(max(lambdas) - min(lambdas))

    if model is not None:
        import torch

        from ehgat.surrogate.graph import build_hetero_graph

        handling = tuple(t.handling_time for t in instance.tasks)
        model_shares = []
        for schedule in (mk_end, en_end):
            # The share must weight the model's gradients by the model's OWN predicted leg
            # durations; pairing them with exact durations would silently mix the two
            # explanations and the ``closes`` check would no longer mean anything.
            with torch.no_grad():
                prediction = model(build_hetero_graph(schedule, instance))
                empty_t = tuple(float(v) for v in prediction.empty_t.detach().cpu())
                loaded_t = tuple(float(v) for v in prediction.loaded_t.detach().cpu())
                node_delay = tuple(float(v) for v in prediction.node_delay.detach().cpu())
            fused = explain_fused(model, schedule, instance)
            model_shares.append(
                critical_path_shares(fused, empty_t, loaded_t, node_delay)
            )
        out["model"] = {
            "rho_makespan_end": model_shares[0].transport,
            "rho_energy_end": model_shares[1].transport,
            "migration": migration(*model_shares),
            "decomposition_closes": bool(all(m.closes for m in model_shares)),
        }
        out["rho_abs_error_makespan_end"] = abs(
            model_shares[0].transport - exact_mk.transport
        )
        out["rho_abs_error_energy_end"] = abs(model_shares[1].transport - exact_en.transport)
    return out


def _run_one(instance_id: str, seed: int, cfg: dict) -> dict:
    """One (instance, seed) replicate: solve, then fit and explain."""
    threads = int(os.environ.get("THREADS_PER_WORKER", "1"))
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)
    import torch

    torch.set_num_threads(threads)

    from ehgat.baselines.brkga import BRKGAConfig, run_brkga
    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.explain.fused_explainer import faithfulness_report

    t0 = time.perf_counter()
    instance = _load(instance_id, cfg.get("num_agvs"))
    n = instance.num_tasks
    pop = cfg["pop_multiplier"] * n
    gens = cfg["generations"]

    mp_result = run_mp_brkga(
        instance, MpBRKGAConfig(pop_size=pop, generations=gens, seed=seed)
    )
    sp_result = run_brkga(instance, BRKGAConfig(pop_size=pop, generations=gens, seed=seed))
    t_solve = time.perf_counter() - t0

    quality = _front_quality(
        {"mp_brkga": list(mp_result.front), "brkga": list(sp_result.front)}
    )
    front_schedules = [decode(c, instance) for c in mp_result.chromosomes]

    row: dict = {
        "instance": instance_id,
        "seed": seed,
        "num_tasks": n,
        "num_qcs": len(instance.qcs),
        "num_agvs": instance.num_agvs,
        "agv_per_qc": instance.num_agvs / len(instance.qcs),
        "pop_size": pop,
        "generations": gens,
        "evaluations_mp": mp_result.evaluations,
        "evaluations_sp": sp_result.evaluations,
        "solve_s": t_solve,
        "quality": quality,
    }

    if cfg["fit_surrogate"]:
        from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused

        t1 = time.perf_counter()
        core = build_core(
            instance,
            seed=seed,
            num_samples=cfg["core_samples"],
            epochs=cfg["core_epochs"],
            device="cpu",
        )
        # scale the fused budget with instance size when asked
        _fs = cfg["fused_samples"]
        if cfg.get("samples_per_leg"):
            _fs = max(_fs, int(cfg["samples_per_leg"] * 2 * instance.num_tasks))
        fused_cfg = FusedTrainConfig(
            num_samples=_fs, epochs=cfg["fused_epochs"], seed=seed
        )
        try:
            from ehgat.explain.train_fused_batched import train_fused_batched

            fitted = train_fused_batched(instance, core, fused_cfg, device="cpu")
        except Exception:
            fitted = train_fused(instance, core, fused_cfg)
        model = fitted.model.cpu()
        row["fit_s"] = time.perf_counter() - t1
        row["calibration"] = {k: float(v) for k, v in fitted.metrics.items()}

        sample = front_schedules[: cfg["explain_limit"]]
        reports = [faithfulness_report(model, s, instance) for s in sample]
        if reports:
            row["faithfulness"] = {
                "n_explained": len(reports),
                "leg_jaccard": float(np.mean([r.leg_critical_jaccard for r in reports])),
                "arc_jaccard": float(np.mean([r.arc_critical_jaccard for r in reports])),
                "makespan_abs_error": float(np.mean([r.makespan_abs_error for r in reports])),
                "energy_abs_error": float(np.mean([r.energy_abs_error for r in reports])),
            }
        row["behaviour"] = _front_behaviour(instance, front_schedules, model)
    else:
        row["behaviour"] = _front_behaviour(instance, front_schedules, None)

    row["wall_s"] = time.perf_counter() - t0
    return row


def _ci95(values: list[float]) -> dict:
    """Mean with a Student-t 95% interval over seeds, ignoring absent values."""
    arr = np.asarray([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    mean = float(arr.mean())
    if arr.size == 1:
        return {"mean": mean, "ci_lo": mean, "ci_hi": mean, "n": 1}
    half = float(sps.t.ppf(0.975, arr.size - 1) * arr.std(ddof=1) / np.sqrt(arr.size))
    return {"mean": mean, "ci_lo": mean - half, "ci_hi": mean + half, "n": int(arr.size)}


def _dig(row: dict, path: str):
    node = row
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node if isinstance(node, (int, float)) else None


_AGGREGATE = (
    "quality.mp_brkga.n",
    "quality.mp_brkga.hypervolume",
    "quality.mp_brkga.igd_plus",
    "quality.mp_brkga.makespan_min",
    "quality.mp_brkga.energy_min",
    "quality.brkga.hypervolume",
    "calibration.r2_makespan",
    "calibration.r2_energy",
    "calibration.mae_makespan",
    "faithfulness.leg_jaccard",
    "faithfulness.arc_jaccard",
    "behaviour.exact.rho_makespan_end",
    "behaviour.exact.rho_energy_end",
    "behaviour.exact.migration",
    "behaviour.model.migration",
    "behaviour.rho_abs_error_makespan_end",
    "behaviour.lambda_span",
    "solve_s",
    "wall_s",
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--set", choices=("L", "DL", "fleet"), default="L")
    ap.add_argument("--instances", nargs="+", default=None)
    ap.add_argument("--agv-sweep", nargs="+", type=int, default=None,
                    help="fleet sizes to sweep (only with --set fleet)")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--generations", type=int, default=300, help="his published Gmax")
    ap.add_argument("--pop-multiplier", type=int, default=20, help="P = m*N; his published m=20")
    ap.add_argument("--no-surrogate", action="store_true",
                    help="fronts and exact behaviour only; skips every fit")
    ap.add_argument("--core-samples", type=int, default=2000)
    ap.add_argument("--core-epochs", type=int, default=80)
    ap.add_argument("--fused-samples", type=int, default=1200)
    ap.add_argument("--samples-per-leg", type=float, default=0.0,
                    help="if >0, set fused samples to this many per leg (2N legs), which keeps "
                         "the training budget proportional to what the head must learn")
    ap.add_argument("--fused-epochs", type=int, default=40)
    ap.add_argument("--explain-limit", type=int, default=64)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()

    if args.instances:
        instance_ids = args.instances
    elif args.set == "DL":
        instance_ids = [f"DL{i:02d}" for i in range(1, 11)]
    else:
        instance_ids = list(json.loads(L_DATA.read_text())["table5_loading_instances"]["instances"])

    cfg = {
        "generations": args.generations,
        "pop_multiplier": args.pop_multiplier,
        "fit_surrogate": not args.no_surrogate,
        "core_samples": args.core_samples,
        "core_epochs": args.core_epochs,
        "fused_samples": args.fused_samples,
        "samples_per_leg": args.samples_per_leg,
        "fused_epochs": args.fused_epochs,
        "explain_limit": args.explain_limit,
        "num_agvs": None,
    }

    jobs: list[tuple[str, int, dict]] = []
    if args.set == "fleet":
        if not args.agv_sweep:
            raise SystemExit("--set fleet requires --agv-sweep")
        for instance_id in instance_ids:
            for fleet in args.agv_sweep:
                for seed in range(args.seeds):
                    jobs.append((instance_id, seed, {**cfg, "num_agvs": fleet}))
    else:
        for instance_id in instance_ids:
            for seed in range(args.seeds):
                jobs.append((instance_id, seed, dict(cfg)))

    tag = args.tag or args.set
    print(
        f"thesis runs | set={args.set} | {len(instance_ids)} instances x {args.seeds} seeds"
        f"{f' x {len(args.agv_sweep)} fleets' if args.set == 'fleet' else ''}"
        f" = {len(jobs)} replicates | P={args.pop_multiplier}N Gmax={args.generations}"
        f" | surrogate={'no' if args.no_surrogate else 'yes'} | {args.workers} workers",
        flush=True,
    )

    rows: list[dict] = []
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(_run_one, i, s, c): (i, s, c.get("num_agvs")) for i, s, c in jobs}
        for done, future in enumerate(as_completed(futures), start=1):
            try:
                row = future.result()
            except Exception as exc:  # keep the sweep alive; record the failure
                key = futures[future]
                print(f"FAILED {key}: {type(exc).__name__}: {exc}", flush=True)
                rows.append({"instance": key[0], "seed": key[1], "num_agvs": key[2],
                             "error": f"{type(exc).__name__}: {exc}"})
                continue
            rows.append(row)
            mig = _dig(row, "behaviour.exact.migration")
            r2 = _dig(row, "calibration.r2_makespan")
            print(
                f"done {row['instance']} seed={row['seed']} N={row['num_tasks']} "
                f"A/Q={row['agv_per_qc']:.2f} |PF|={_dig(row, 'quality.mp_brkga.n')} "
                f"migr={mig if mig is None else round(mig, 3)} "
                f"R2mk={r2 if r2 is None else round(r2, 3)} "
                f"({row['wall_s']:.0f}s) [{done}/{len(jobs)}]",
                flush=True,
            )

    groups: dict[str, list[dict]] = {}
    for row in rows:
        if "error" in row:
            continue
        key = row["instance"] if args.set != "fleet" else f"{row['instance']}@{row['num_agvs']}"
        groups.setdefault(key, []).append(row)

    aggregate = {}
    for key, group in groups.items():
        head = group[0]
        entry = {
            "num_tasks": head["num_tasks"],
            "num_qcs": head["num_qcs"],
            "num_agvs": head["num_agvs"],
            "agv_per_qc": head["agv_per_qc"],
            "seeds": len(group),
        }
        for path in _AGGREGATE:
            entry[path] = _ci95([_dig(r, path) for r in group])
        aggregate[key] = entry

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"thesis_{tag}.json"
    out.write_text(
        json.dumps(
            {"config": {**cfg, "seeds": args.seeds, "set": args.set,
                        "agv_sweep": args.agv_sweep},
             "per_seed": rows, "aggregate": aggregate},
            indent=2,
        )
        + "\n"
    )
    failures = sum(1 for r in rows if "error" in r)
    print(
        f"\nwrote {out.relative_to(REPO)} | {len(rows) - failures} ok, {failures} failed "
        f"| total {time.perf_counter() - t0:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
