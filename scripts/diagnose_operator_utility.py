"""scripts/diagnose_operator_utility.py -- is bottleneck-TYPE a usable operator signal?

The decisive test for whether the AOS Channel-B null (random ~ attention ~ oracle) is a
*real* null or a *broken* harness. It bypasses the NSGA-II ablation entirely and measures,
on the **exact Max-Plus evaluator** (ground truth, no surrogate), the realized utility of
each mutation operator -- and whether that utility is conditional on the task's exact
bottleneck type (the oracle's core premise).

For a set of realistic parents (random feasible schedules + the non-dominated front of a
large random pool), and for every task, each operator is applied and the following recorded:
Pareto-dominance credit (`operator_reward`) of the child vs the parent on exact objectives.
We then ask three questions:

1. **Marginal:** do the four operators differ in utility at all? (If not, *no* policy can
   beat random -> the null is real and operator selection is simply not a lever.)
2. **Conditional (the oracle premise):** for AGV-bound tasks, do the AGV operators
   (`reassign`/`swap_agv`) beat `swap_qc`? For QC-bound tasks, does `swap_qc` win? If the
   conditional structure is absent, a *perfect* bottleneck-type oracle carries no usable
   information -> oracle-ties-random is mathematically forced, not a bug.
3. **Policy gain:** how much expected reward a type-matched policy gains over uniform, vs
   the upper bound of an operator-utility oracle (best op per type). type_gain ~ 0 with
   utility_gain >> 0 is the smoking gun that the lever is *utility*, not *type*.

Usage (on the pod):
    .venv/bin/python scripts/diagnose_operator_utility.py --tasks 10 20 50
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from ehgat.benchmark.faithfulness import critical_path_binding
from ehgat.environment.decoder import NUM_BLOCKS, Schedule, decode
from ehgat.environment.evaluator import evaluate
from ehgat.environment.instance import Instance, build_toy_instance
from ehgat.search.attention_nsga2 import (
    _MUTATION_OPS,
    mutate_reassign_agv,
    mutate_speed,
    mutate_swap_on_agv,
    mutate_swap_on_qc,
    operator_reward,
)
from ehgat.search.nsga2 import fast_non_dominated_sort
from ehgat.utils.seeding import make_rng

_AGV_OPS = ("reassign", "swap_agv")
_QC_OPS = ("swap_qc",)


def _apply(op: str, s: Schedule, j: int, instance: Instance, rng: np.random.Generator):
    if op == "speed":
        return mutate_speed(s, j, rng)
    if op == "reassign":
        return mutate_reassign_agv(s, instance, j, rng)
    if op == "swap_agv":
        return mutate_swap_on_agv(s, instance, j)
    if op == "swap_qc":
        return mutate_swap_on_qc(s, instance, j)
    raise ValueError(op)


def _task_type(j: int, agv_bound: set[int], qc_bound: set[int]) -> str:
    if j in agv_bound:
        return "AGV"
    if j in qc_bound:
        return "QC"
    return "off"  # not on the critical path of this parent


def _parent_sets(
    instance: Instance, rng: np.random.Generator, pool: int, n_random: int, n_front: int
) -> dict[str, list[Schedule]]:
    chrom = NUM_BLOCKS * instance.num_tasks
    schedules = [decode(rng.random(chrom), instance) for _ in range(pool)]
    objectives = [evaluate(s, instance).objectives for s in schedules]
    front = fast_non_dominated_sort(objectives)[0]
    front_set = [schedules[i] for i in front][:n_front]
    dominated = [schedules[i] for i in range(pool) if i not in set(front)]
    rng.shuffle(dominated)
    return {"random": dominated[:n_random], "front": front_set}


def _collect(
    instance: Instance, parents: list[Schedule], trials: int, rng: np.random.Generator
) -> dict:
    """Return reward samples keyed by operator and by (type, operator)."""
    by_op: dict[str, list[float]] = defaultdict(list)
    by_op_dom: dict[str, list[float]] = defaultdict(list)
    by_op_feasible: dict[str, list[float]] = defaultdict(list)
    by_type_op: dict[tuple[str, str], list[float]] = defaultdict(list)
    type_counts: dict[str, int] = defaultdict(int)

    n = instance.num_tasks
    for s in parents:
        p_obj = evaluate(s, instance).objectives
        agv_bound, qc_bound = critical_path_binding(s, instance)
        for j in range(n):
            ttype = _task_type(j, agv_bound, qc_bound)
            type_counts[ttype] += 1
            for op in _MUTATION_OPS:
                rewards = []
                feas = 0
                for _ in range(trials):
                    child = _apply(op, s, j, instance, rng)
                    if child is None or child == s:
                        rewards.append(0.0)  # infeasible / no-op -> no progress
                        continue
                    feas += 1
                    c_obj = evaluate(child, instance).objectives
                    rewards.append(operator_reward(p_obj, c_obj))
                r = float(np.mean(rewards))
                by_op[op].append(r)
                by_op_dom[op].append(float(np.mean([1.0 if x >= 1.0 else 0.0 for x in rewards])))
                by_op_feasible[op].append(feas / trials)
                by_type_op[(ttype, op)].append(r)
    return {
        "by_op": by_op,
        "by_op_dom": by_op_dom,
        "by_op_feasible": by_op_feasible,
        "by_type_op": by_type_op,
        "type_counts": dict(type_counts),
    }


def _cell_mean(d: dict, key) -> float:
    v = d.get(key, [])
    return float(np.mean(v)) if v else float("nan")


def _policy_gains(data: dict) -> dict:
    """Expected reward of uniform vs type-matched vs utility-oracle policies."""
    by_op = data["by_op"]
    by_type_op = data["by_type_op"]
    uniform = float(np.mean([np.mean(by_op[op]) for op in _MUTATION_OPS]))

    # Type-matched policy: AGV-bound -> AGV ops, QC-bound -> swap_qc, off -> uniform.
    type_counts = data["type_counts"]
    total = sum(type_counts.values()) or 1
    type_reward = 0.0
    for ttype, cnt in type_counts.items():
        if ttype == "AGV":
            r = np.mean([_cell_mean(by_type_op, ("AGV", op)) for op in _AGV_OPS])
        elif ttype == "QC":
            r = np.mean([_cell_mean(by_type_op, ("QC", op)) for op in _QC_OPS])
        else:
            r = uniform
        type_reward += (cnt / total) * float(r)

    # Utility-oracle upper bound: best operator per type (what an operator-utility oracle gets).
    util_reward = 0.0
    for ttype, cnt in type_counts.items():
        cells = [_cell_mean(by_type_op, (ttype, op)) for op in _MUTATION_OPS]
        cells = [c for c in cells if not np.isnan(c)]
        util_reward += (cnt / total) * (max(cells) if cells else uniform)

    return {
        "uniform": uniform,
        "type_matched": type_reward,
        "utility_oracle": util_reward,
        "type_gain": type_reward - uniform,
        "utility_gain": util_reward - uniform,
    }


def _print_report(n: int, parent_label: str, data: dict, gains: dict) -> None:
    print(f"\n===== N={n}  parents={parent_label} =====")
    print(f"  task-type mix (critical-path binding): {data['type_counts']}")
    print("  -- MARGINAL operator utility (mean reward / P(dominate) / feasible%) --")
    for op in _MUTATION_OPS:
        print(
            f"    {op:9s} reward={np.mean(data['by_op'][op]):.3f}  "
            f"P(dom)={np.mean(data['by_op_dom'][op]):.3f}  "
            f"feas={np.mean(data['by_op_feasible'][op]):.2f}"
        )
    print("  -- CONDITIONAL reward  E[reward | task-type, operator] (the oracle premise) --")
    print(f"    {'type':5s} " + "".join(f"{op:>10s}" for op in _MUTATION_OPS))
    for ttype in ("AGV", "QC", "off"):
        row = "".join(f"{_cell_mean(data['by_type_op'], (ttype, op)):>10.3f}" for op in _MUTATION_OPS)
        print(f"    {ttype:5s} {row}")
    print("  -- POLICY expected reward --")
    print(
        f"    uniform={gains['uniform']:.3f}  type-matched={gains['type_matched']:.3f}  "
        f"utility-oracle={gains['utility_oracle']:.3f}"
    )
    print(
        f"    >> type_gain={gains['type_gain']:+.3f}   utility_gain={gains['utility_gain']:+.3f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose whether bottleneck-type drives operator utility")
    parser.add_argument("--tasks", type=int, nargs="+", default=[10, 20, 50])
    parser.add_argument("--pool", type=int, default=2000, help="random schedules to draw parents from")
    parser.add_argument("--random-parents", type=int, default=150)
    parser.add_argument("--front-parents", type=int, default=80)
    parser.add_argument("--trials", type=int, default=3, help="trials per (task, operator)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=str, default=str(Path(__file__).resolve().parents[1] / "experiments" / "operator_utility"))
    ns = parser.parse_args()

    out = Path(ns.out)
    out.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}

    for n in ns.tasks:
        instance = build_toy_instance(num_tasks=n)
        rng = make_rng(ns.seed)
        parent_sets = _parent_sets(instance, rng, ns.pool, ns.random_parents, ns.front_parents)
        summary[str(n)] = {}
        for label, parents in parent_sets.items():
            if not parents:
                continue
            data = _collect(instance, parents, ns.trials, rng)
            gains = _policy_gains(data)
            _print_report(n, label, data, gains)
            summary[str(n)][label] = {
                "type_counts": data["type_counts"],
                "marginal": {op: float(np.mean(data["by_op"][op])) for op in _MUTATION_OPS},
                "conditional": {
                    f"{t}|{op}": _cell_mean(data["by_type_op"], (t, op))
                    for t in ("AGV", "QC", "off")
                    for op in _MUTATION_OPS
                },
                "gains": gains,
                "num_parents": len(parents),
            }

    path = out / "operator_utility.json"
    path.write_text(json.dumps(summary, indent=2))
    print(f"\nSaved: {path}")
    print(
        "\nVERDICT KEY:\n"
        "  type_gain ~ 0            -> bottleneck-TYPE is not a usable signal (oracle MUST tie random): REAL null.\n"
        "  type_gain ~ utility_gain -> type fully explains operator choice: oracle SHOULD win (if not, harness bug).\n"
        "  utility_gain >> type_gain ~ 0 -> operators differ but TYPE doesn't predict which: lever is UTILITY, not type."
    )


if __name__ == "__main__":
    main()
