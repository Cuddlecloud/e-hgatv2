"""scripts/run_critical_path_demo.py -- Req 2 worked-example explainability demo.

The aggregate faithfulness study (``scripts/run_fused_tape.py``) reports *mean* leg/arc
Jaccard over random schedules. This driver instead produces the **human-readable worked
example** the advisor asked for: for a small "stub" instance it takes a Pareto-optimal
schedule, **traverses the exact makespan critical path**, and prints a precise additive
quantification

    C_max = sum over on-path legs of (leg duration) + sum over on-path tasks of (QC handling),

then shows the **fused-GNN TAPE recovers the identical path** (leg-critical Jaccard) and
predicts each on-path duration (per-activity abs error). The decomposition is exact because
the makespan is the max-plus longest path: every on-path activity carries a binary
subgradient ``dC_max/d(duration) = 1`` (:mod:`ehgat.explain.tropical_dp`), so the on-path
durations sum to the makespan by construction.

For each instance we report the traversal at BOTH front extremes -- the makespan-optimal end
and the energy-optimal end -- so the migration of the binding bottleneck (the R2/R4 "why is
this solution Pareto-optimal" knowledge) is visible in the same artifact.

Writes ``experiments/critical_path_demo/critpath_<tag>.{json,md,tex}``.

Run on the VM::

    python scripts/run_critical_path_demo.py --instances toy:5 toy:8 toy:10 L07
    python scripts/run_critical_path_demo.py --instances toy:8 --peak-power 30
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

OUT = Path(__file__).resolve().parents[1] / "experiments" / "critical_path_demo"
_TOL = 1e-4  # decomposition self-consistency tolerance (C_max vs summed on-path durations)


def _load_instance(spec: str, peak_power: float | None):
    from ehgat.environment.dsdl import load_tables_4_5
    from ehgat.environment.instance import build_toy_instance

    if spec.startswith("toy:"):
        n = int(spec.split(":", 1)[1])
        return build_toy_instance(num_tasks=n, peak_power=peak_power)
    data = Path(__file__).resolve().parents[1] / "data" / "tables_4_5.json"
    return load_tables_4_5(data, peak_power=peak_power, only=[spec])[0].instance


def _jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    u = a | b
    return len(a & b) / len(u) if u else 1.0


def _durations(ev, instance, coupled: bool) -> tuple[list[float], list[float], list[float]]:
    """Effective per-task (empty_leg, loaded_leg, QC handling) durations.

    Under peak-power coupling the per-leg power waits are folded into the leg duration so the
    quantification matches the coupled critical path (the same convention the coupled TAPE
    oracle uses, ``explain_schedule_coupled``)."""
    n = instance.num_tasks
    empty = [float(ev.empty_time[j]) for j in range(n)]
    loaded = [float(ev.loaded_time[j]) for j in range(n)]
    handling = [float(instance.tasks[j].handling_time) for j in range(n)]
    if coupled:
        wait_e = getattr(ev, "wait_empty", [0.0] * n)
        wait_l = getattr(ev, "wait_loaded", [0.0] * n)
        empty = [empty[j] + float(wait_e[j]) for j in range(n)]
        loaded = [loaded[j] + float(wait_l[j]) for j in range(n)]
    return empty, loaded, handling


def _on_path(grads: tuple[float, ...], threshold: float = 0.5) -> set[int]:
    return {j for j, g in enumerate(grads) if g > threshold}


def _critical_rows(ex, ev, instance, coupled: bool) -> tuple[list[dict], float]:
    """Ordered on-path activities (task, kind, duration, dC_max) and their summed duration.

    ``ex`` is a TapeExplanation; an activity is on the critical path iff its binary
    subgradient exceeds 0.5. Rows are ordered by the task's completion time so the table
    reads as a forward traversal from the start of the schedule to the makespan-defining
    task."""
    empty_dur, loaded_dur, handling = _durations(ev, instance, coupled)
    rows: list[dict] = []
    total = 0.0
    for j in range(instance.num_tasks):
        completion = float(ev.completion[j])
        if ex.empty_time_grad[j] > 0.5:
            rows.append({"task": j, "activity": "empty_leg", "duration": empty_dur[j],
                         "dCmax": float(ex.empty_time_grad[j]), "completion": completion})
            total += empty_dur[j]
        if ex.loaded_time_grad[j] > 0.5:
            rows.append({"task": j, "activity": "loaded_leg", "duration": loaded_dur[j],
                         "dCmax": float(ex.loaded_time_grad[j]), "completion": completion})
            total += loaded_dur[j]
        if ex.node_grad[j] > 0.5:
            rows.append({"task": j, "activity": "qc_handling", "duration": handling[j],
                         "dCmax": float(ex.node_grad[j]), "completion": completion})
            total += handling[j]
    rows.sort(key=lambda r: (r["completion"], r["task"], r["activity"]))
    return rows, total


def _fused_durations(model, schedule, instance) -> tuple[list[float], list[float], list[float]]:
    """The fused model's own predicted (empty_leg, loaded_leg, QC handling) durations."""
    import torch

    from ehgat.surrogate.graph import build_hetero_graph

    model.eval()
    with torch.no_grad():
        out = model(build_hetero_graph(schedule, instance))
    empty = [float(v) for v in out.empty_t.detach().cpu()]
    loaded = [float(v) for v in out.loaded_t.detach().cpu()]
    handling = [float(v) for v in out.node_delay.detach().cpu()]
    return empty, loaded, handling


def _traverse(label: str, schedule, instance, fused, coupled: bool) -> dict:
    from ehgat.environment.evaluator import evaluate
    from ehgat.explain.fused_explainer import explain_fused
    from ehgat.explain.tape_explainer import explain_schedule, explain_schedule_coupled

    ev = evaluate(schedule, instance)
    oracle = explain_schedule_coupled(schedule, instance) if coupled else explain_schedule(schedule, instance)
    fused_ex = explain_fused(fused, schedule, instance)

    rows, oracle_total = _critical_rows(oracle, ev, instance, coupled)
    consistent = abs(oracle_total - oracle.makespan) <= _TOL * max(1.0, abs(oracle.makespan))

    # Which on-path activities does the fused-GNN TAPE also flag?
    f_empty, f_loaded, f_handling = _fused_durations(fused, schedule, instance)
    fused_legs = (_on_path(fused_ex.empty_time_grad)
                  | {j + instance.num_tasks for j in _on_path(fused_ex.loaded_time_grad)})
    oracle_legs = (_on_path(oracle.empty_time_grad)
                   | {j + instance.num_tasks for j in _on_path(oracle.loaded_time_grad)})
    for r in rows:
        j, act = r["task"], r["activity"]
        if act == "empty_leg":
            r["gnn_on_path"] = fused_ex.empty_time_grad[j] > 0.5
            r["gnn_duration"] = f_empty[j]
        elif act == "loaded_leg":
            r["gnn_on_path"] = fused_ex.loaded_time_grad[j] > 0.5
            r["gnn_duration"] = f_loaded[j]
        else:
            r["gnn_on_path"] = fused_ex.node_grad[j] > 0.5
            r["gnn_duration"] = f_handling[j]
        r["abs_err"] = abs(r["gnn_duration"] - r["duration"])

    return {
        "label": label,
        "makespan": oracle.makespan,
        "energy": oracle.energy,
        "fused_makespan": fused_ex.makespan,
        "fused_energy": fused_ex.energy,
        "path_len": len(rows),
        "decomposition_total": oracle_total,
        "decomposition_consistent": consistent,
        "leg_critical_jaccard": _jaccard(fused_legs, oracle_legs),
        "rows": rows,
    }


def analyse(spec: str, peak_power: float | None, args) -> dict:
    from ehgat.environment.evaluator import evaluate
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
    from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2

    instance = _load_instance(spec, peak_power)
    coupled = instance.peak_power is not None

    core = build_core(instance, seed=0, num_samples=args.core_samples,
                      epochs=args.core_epochs, device=args.device)
    fused_res = train_fused(instance, core, FusedTrainConfig(
        num_samples=args.fused_samples, epochs=args.fused_epochs,
        unroll_steps=(args.unroll if coupled else 0), seed=0))
    fused = fused_res.model.cpu()

    res = run_attention_nsga2(
        instance, None,
        AttentionNSGA2Config(args.pop, args.gens, seed=0, guidance="tape",
                             screening_factor=args.screening),
        fused_model=fused)
    scheds = list(res.schedules)
    if not scheds:
        raise RuntimeError(f"{spec}: guided search returned an empty Pareto set")

    evals = [evaluate(s, instance) for s in scheds]
    mk_idx = min(range(len(scheds)), key=lambda i: evals[i].makespan)
    en_idx = min(range(len(scheds)), key=lambda i: evals[i].energy)

    traversals = [_traverse("makespan_optimal", scheds[mk_idx], instance, fused, coupled)]
    if en_idx != mk_idx:
        traversals.append(_traverse("energy_optimal", scheds[en_idx], instance, fused, coupled))

    result = {
        "instance": spec,
        "n": instance.num_tasks,
        "num_agvs": instance.num_agvs,
        "num_qcs": len(instance.qcs),
        "coupled": coupled,
        "peak_power": peak_power,
        "n_front": len(scheds),
        "fused_r2_makespan": float(fused_res.metrics.get("r2_makespan", float("nan"))),
        "traversals": traversals,
    }
    for t in traversals:
        flag = "ok" if t["decomposition_consistent"] else "MISMATCH"
        print(f"  {spec} [{t['label']}]: C_max={t['makespan']:.3f} "
              f"path_len={t['path_len']} sum_on_path={t['decomposition_total']:.3f} "
              f"({flag}) leg-Jaccard(GNN vs oracle)={t['leg_critical_jaccard']:.3f}",
              flush=True)
    return result


def _latex_table(results: list[dict]) -> str:
    lines = [
        r"% Auto-generated by scripts/run_critical_path_demo.py -- do not edit by hand.",
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Worked-example critical-path traversal (R2). For the makespan-optimal "
        r"Pareto schedule of each stub instance, the exact max-plus critical path is listed "
        r"as an ordered sequence of binding activities whose durations sum to $C_{\max}$ "
        r"(decomposition exact by construction). The fused-GNN TAPE recovers the identical "
        r"path (leg-critical Jaccard) and predicts each on-path duration.}",
        r"\label{tab:critpath}",
        r"\small",
        r"\begin{tabular}{llrrr}",
        r"\toprule",
        r"Instance & On-path activities ($\to$) & $C_{\max}$ & Path len & Leg-Jaccard \\",
        r"\midrule",
    ]
    for r in results:
        t = r["traversals"][0]  # makespan-optimal
        seq = " $\\to$ ".join(
            f"$t_{{{row['task']}}}$:{row['activity'].split('_')[0]}" for row in t["rows"]
        )
        lines.append(
            f"{r['instance']} & {seq} & {t['makespan']:.2f} & {t['path_len']} & "
            f"{t['leg_critical_jaccard']:.2f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(lines)


def _markdown(results: list[dict]) -> str:
    md = ["# Critical-path worked examples (R2)\n"]
    for r in results:
        md.append(f"## {r['instance']} (N={r['n']}, AGV={r['num_agvs']}, QC={r['num_qcs']}, "
                  f"coupled={r['coupled']}, fused R2(Cmax)={r['fused_r2_makespan']:.3f})\n")
        for t in r["traversals"]:
            md.append(f"### {t['label']}: C_max={t['makespan']:.3f}, E={t['energy']:.3f} "
                      f"(GNN C_max={t['fused_makespan']:.3f}); leg-Jaccard(GNN vs oracle)="
                      f"{t['leg_critical_jaccard']:.3f}; decomposition "
                      f"{'consistent' if t['decomposition_consistent'] else 'MISMATCH'} "
                      f"(sum on-path = {t['decomposition_total']:.3f})\n")
            md.append("| order | task | activity | duration (exact) | dC_max | GNN on-path | "
                      "GNN duration | abs err |")
            md.append("|---|---|---|---|---|---|---|---|")
            for k, row in enumerate(t["rows"]):
                md.append(f"| {k} | t{row['task']} | {row['activity']} | {row['duration']:.3f} "
                          f"| {row['dCmax']:.2f} | {row['gnn_on_path']} | "
                          f"{row['gnn_duration']:.3f} | {row['abs_err']:.3f} |")
            md.append("")
    return "\n".join(md) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description="Req 2 worked-example critical-path traversal.")
    p.add_argument("--instances", nargs="+", default=["toy:5", "toy:8", "toy:10", "L07"])
    p.add_argument("--peak-power", type=float, default=None)
    p.add_argument("--pop", type=int, default=120)
    p.add_argument("--gens", type=int, default=40)
    p.add_argument("--screening", type=int, default=3)
    p.add_argument("--unroll", type=int, default=2)
    p.add_argument("--core-samples", type=int, default=1200)
    p.add_argument("--core-epochs", type=int, default=60)
    p.add_argument("--fused-samples", type=int, default=1000)
    p.add_argument("--fused-epochs", type=int, default=60)
    p.add_argument("--device", default="cpu")
    p.add_argument("--tag", default=None)
    args = p.parse_args()

    import torch

    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "1")))

    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in args.instances:
        print(f"instance {spec} ...", flush=True)
        results.append(analyse(spec, args.peak_power, args))

    tag = args.tag or ("coupled" if args.peak_power is not None else "uncoupled")
    (OUT / f"critpath_{tag}.json").write_text(json.dumps(results, indent=2))
    (OUT / f"critpath_{tag}.md").write_text(_markdown(results))
    (OUT / f"critpath_{tag}.tex").write_text(_latex_table(results))
    print(f"\nwrote {OUT}/critpath_{tag}.{{json,md,tex}}", flush=True)

    mismatches = [(r["instance"], t["label"]) for r in results for t in r["traversals"]
                  if not t["decomposition_consistent"]]
    if mismatches:
        raise SystemExit(f"DECOMPOSITION MISMATCH (on-path durations != C_max): {mismatches}")


if __name__ == "__main__":
    main()
