"""Exact explanation of why finalized Pareto solutions are Pareto-optimal (required core).

This driver serves the advisor's prescribed core -- "explain why selected solutions are
Pareto-optimal" -- and nothing else. Two properties make it the *required* tier rather than a
bonus:

1. **No surrogate participates in front generation.** Fronts come from ``run_mp_brkga`` under
   exact evaluation. The attribution-guided search is demoted to future work, so it must not
   appear here; ``scripts/run_critical_path_demo.py`` cannot be reused for this purpose because
   it builds its Pareto set with ``run_attention_nsga2(..., guidance="tape")``.
2. **No network participates in the explanation.** The traversal uses the exact max-plus oracle
   only. The surrogate's post-hoc reproduction of the same path is a separate and strictly
   weaker claim, enabled with ``--with-surrogate`` and reported in its own block so that a poor
   faithfulness number cannot weaken a result that does not depend on the model.

For each instance the front's two extremes are explained -- the makespan-optimal end and the
energy-optimal end -- because the *contrast* between them is the explanation. The binding
bottleneck migrates between vehicle travel and crane handling as the front is traversed, and the
duration-weighted share ``rho`` quantifies that migration in a way that closes against the
makespan by construction.

The coupled power regime is out of scope (advisor's scope cut), so no peak-power option exists
here by design.

Run on the VM::

    python scripts/run_pareto_explanation.py --set L --out experiments/pareto_explanation
    python scripts/run_pareto_explanation.py --set DL --generations 100
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga  # noqa: E402
from ehgat.environment.decoder import decode  # noqa: E402
from ehgat.environment.evaluator import evaluate  # noqa: E402
from ehgat.environment.dsdl import load_dl_instances, load_tables_4_5  # noqa: E402
from ehgat.explain.critical_share import critical_path_shares  # noqa: E402
from ehgat.explain.tape_explainer import explain_schedule  # noqa: E402
from ehgat.explain.traversal import exact_traversal  # noqa: E402

# The L instances chosen for the sweep: the four published anchors plus L01 as the hand-checkable
# smallest case. L21/L15/L35 are also the instances where bottleneck migration is largest.
DEFAULT_L = ("L01", "L07", "L15", "L21", "L35")


def _load(spec: str, which: str):
    if which == "DL":
        return load_dl_instances(only=[spec])[0].instance
    return load_tables_4_5("data/tables_4_5.json", only=[spec])[0].instance


def _shares(schedule, instance):
    """Duration-weighted transport/handling split of the critical path."""
    ev = evaluate(schedule, instance)
    ex = explain_schedule(schedule, instance)
    return critical_path_shares(
        ex,
        empty_time=tuple(float(v) for v in ev.empty_time),
        loaded_time=tuple(float(v) for v in ev.loaded_time),
        handling_time=tuple(float(t.handling_time) for t in instance.tasks),
    )


def analyse(spec: str, which: str, args) -> dict:
    instance = _load(spec, which)

    cfg = MpBRKGAConfig(
        pop_size=args.pop or 20 * instance.num_tasks,
        generations=args.generations,
        seed=args.seed,
    )
    res = run_mp_brkga(instance, cfg)  # no screen_fn: exact evaluation only
    if not res.front:
        raise RuntimeError(f"{spec}: mp-BRKGA returned an empty front")

    schedules = [decode(c, instance) for c in res.chromosomes]
    objs = [evaluate(s, instance).objectives for s in schedules]
    mk_idx = min(range(len(objs)), key=lambda i: objs[i][0])
    en_idx = min(range(len(objs)), key=lambda i: objs[i][1])

    ends = [("makespan_optimal", mk_idx)]
    if en_idx != mk_idx:
        ends.append(("energy_optimal", en_idx))

    traversals, shares = [], {}
    for label, idx in ends:
        t = exact_traversal(label, schedules[idx], instance)
        traversals.append(t)
        shares[label] = _shares(schedules[idx], instance)

    mk_rho = shares["makespan_optimal"].transport
    en_rho = shares.get("energy_optimal", shares["makespan_optimal"]).transport

    out = {
        "instance": spec,
        "n": instance.num_tasks,
        "num_agvs": instance.num_agvs,
        "num_qcs": len(instance.qcs),
        "aq_ratio": instance.num_agvs / len(instance.qcs),
        "front_size": len(res.front),
        "evaluations": res.evaluations,
        "generations": cfg.generations,
        "pop_size": cfg.pop_size,
        "seed": cfg.seed,
        "rho_transport_makespan_end": mk_rho,
        "rho_transport_energy_end": en_rho,
        # Signed shift of the transport share across the front, using the package convention in
        # ehgat.explain.critical_share.migration: POSITIVE means the makespan-optimal end leans
        # more on travel than the energy-optimal end does. Must match run_thesis_experiments.py,
        # or the two result tables would carry opposite signs.
        "migration": mk_rho - en_rho,
        "traversals": [
            {
                **{k: v for k, v in asdict(t).items() if k != "activities"},
                "path_len": t.path_len,
                "closes": t.closes,
                "travel_total": t.travel_total,
                "handling_total": t.handling_total,
                "rho_transport": shares[t.label].transport,
                "rho_handling": shares[t.label].handling,
                "shares_close": shares[t.label].closes,
                "activities": [asdict(a) for a in t.activities],
            }
            for t in traversals
        ],
    }

    for t in traversals:
        s = shares[t.label]
        flag = "ok" if t.closes else "DECOMPOSITION MISMATCH"
        sflag = "ok" if s.closes else "SHARES MISMATCH"
        print(
            f"  {spec:6} [{t.label:16}] Cmax={t.makespan:9.3f} sum={t.decomposition_total:9.3f}"
            f" ({flag}) path={t.path_len:3d} rho_t={s.transport:.3f} ({sflag})",
            flush=True,
        )
    print(f"  {spec:6} migration (rho_t energy_end - makespan_end) = {out['migration']:+.3f}", flush=True)
    return out


def main() -> None:
    p = argparse.ArgumentParser(
        description="Exact explanation of Pareto-optimality (required core; no surrogate)."
    )
    p.add_argument("--set", dest="which", choices=["L", "DL"], default="L")
    p.add_argument("--instances", nargs="+", default=None,
                   help="override the instance list (default: the five L anchors, or DL01..DL10)")
    p.add_argument("--generations", type=int, default=100)
    p.add_argument("--pop", type=int, default=None, help="default 20N, his convention")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", type=Path, default=Path("experiments/pareto_explanation"))
    args = p.parse_args()

    if args.instances:
        specs = list(args.instances)
    elif args.which == "DL":
        specs = [f"DL{i:02d}" for i in range(1, 11)]
    else:
        specs = list(DEFAULT_L)

    print(f"[exact] set={args.which} instances={len(specs)} gens={args.generations} "
          f"seed={args.seed} -- no surrogate in front generation or explanation", flush=True)

    results, failures = [], []
    for spec in specs:
        try:
            results.append(analyse(spec, args.which, args))
        except Exception as exc:  # isolate per instance so one failure cannot cost the rest
            print(f"  {spec:6} FAILED: {type(exc).__name__}: {exc}", flush=True)
            failures.append({"instance": spec, "error": f"{type(exc).__name__}: {exc}"})

    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"exact_explanation_{args.which}.json"
    path.write_text(json.dumps({
        "tier": "required (advisor prescribed core item 3)",
        "front_source": "mp-BRKGA, exact evaluation, no surrogate",
        "explanation_source": "tape_explainer.explain_schedule (exact oracle, no network)",
        "coupled": False,
        "results": results,
        "failures": failures,
    }, indent=2))

    n_bad = sum(1 for r in results for t in r["traversals"] if not t["closes"])
    print(f"\n[exact] wrote {path}")
    print(f"[exact] {len(results)} ok, {len(failures)} failed, "
          f"{n_bad} decomposition mismatches (must be 0)")


if __name__ == "__main__":
    main()
