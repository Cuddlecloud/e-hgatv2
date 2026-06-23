"""scripts/run_tape_guided_bench.py -- the "faithful explanations steer the search" study.

This is the experiment that unifies the advisor's Req 2 (explanation) and Req 3
(optimization) into ONE evidenced claim. Per instance it:

1. trains the core E-HGATv2 + the physics-fused TAPE head (`train_fused`);
2. runs NSGA-II under three guidance signals at a **matched exact-evaluation budget**:
   - ``E-HGATv2-TAPE``  -- Signal #3: fused-GNN TAPE (faithful by construction) drives
     both the bottleneck task selection AND the offspring screening;
   - ``E-HGATv2-attn``  -- Signal #1: the bare HAN attention readout (the unfaithful foil);
   - ``NSGA-II (random)`` -- no guidance (the null);
   plus the published baselines ``mp-BRKGA`` (multi-population) and ``single-pop BRKGA``;
3. measures the **faithfulness** of each guidance signal on a fixed schedule sample:
   attention precision@1 / Spearman (expected ~random) vs TAPE leg-critical Jaccard vs the
   exact max-plus oracle (expected ~1.0).

The headline: TAPE is the only signal that is BOTH faithful (Req 2) AND wins the search
(Req 3); attention may help the search a little but is unfaithful, so it cannot carry the
"explanation steers the search" claim.

Budget matching: mp-BRKGA evaluates ``(Omega+Pi)*P = 4P`` chromosomes/generation, so the
GAT/BRKGA arms use ``pop = 4P`` to equalise exact evaluations/generation; all use the same
``--gens``. The surrogate screening (``screening_factor``) is the GNN's *free* advantage --
it screens ``k*pop`` candidates cheaply but still spends only ``pop`` exact evals/gen.

Run on the VM::

    python scripts/run_tape_guided_bench.py --instance toy:10 --seeds 5 --gens 60
    python scripts/run_tape_guided_bench.py --instance toy:10 --peak-power 30 --seeds 5 --gens 60
    python scripts/run_tape_guided_bench.py --instance L15 --seeds 5 --gens 60

Writes ``experiments/fused_tape_guided/tape_bench_<tag>.{json,md}``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from scipy import stats as sps

OUT_DIR = Path(__file__).resolve().parents[1] / "experiments" / "fused_tape_guided"
Front = tuple[tuple[float, float], ...]


def _load_instance(spec: str, peak_power: float | None):
    """Return (instance, label). ``spec`` is 'toy:N' or an L-id like 'L15'."""
    from ehgat.environment.dsdl import load_tables_4_5
    from ehgat.environment.instance import build_toy_instance

    if spec.startswith("toy:"):
        n = int(spec.split(":", 1)[1])
        return build_toy_instance(num_tasks=n, peak_power=peak_power), spec
    data = Path(__file__).resolve().parents[1] / "data" / "tables_4_5.json"
    return load_tables_4_5(data, peak_power=peak_power, only=[spec])[0].instance, spec


def _pareto(points: list[tuple[float, float]]) -> Front:
    seen: set[tuple[float, float]] = set()
    uniq: list[tuple[float, float]] = []
    for m, e in points:
        k = (round(float(m), 6), round(float(e), 6))
        if k not in seen:
            seen.add(k)
            uniq.append((float(m), float(e)))
    front: list[tuple[float, float]] = []
    best_e: float | None = None
    for m, e in sorted(uniq):
        if best_e is None or e < best_e:
            front.append((m, e))
            best_e = e
    return tuple(front)


def _ci(vals: list[float]) -> tuple[float, float]:
    a = np.asarray(vals, float)
    if a.size < 2:
        return float(a.mean()) if a.size else float("nan"), 0.0
    half = float(sps.t.ppf(0.975, a.size - 1) * a.std(ddof=1) / np.sqrt(a.size))
    return float(a.mean()), half


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--instance", default="toy:10", help="'toy:N' or an L-id like 'L15'")
    p.add_argument("--peak-power", type=float, default=None, help="kW budget => coupled regime")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--gens", type=int, default=60)
    p.add_argument("--ref-gens", type=int, default=200, help="generations for the PF* proxy runs")
    p.add_argument("--screening", type=int, default=4, help="surrogate screening factor for GAT arms")
    p.add_argument("--p-mult", type=int, default=20, help="mp-BRKGA per-population size P = p_mult*N "
                   "(paper: 20; lower for compute tractability -- all methods stay budget-matched)")
    p.add_argument("--unroll", type=int, default=2, help="coupled fused unroll steps")
    p.add_argument("--core-samples", type=int, default=2000)
    p.add_argument("--core-epochs", type=int, default=80)
    p.add_argument("--fused-samples", type=int, default=1500)
    p.add_argument("--fused-epochs", type=int, default=80)
    p.add_argument("--faith-samples", type=int, default=40)
    p.add_argument("--mutation-temperature", type=float, default=0.25)
    p.add_argument("--device", default="cpu", help="training device (cuda|cpu); search runs on cpu")
    args = p.parse_args()

    import torch

    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "1")))

    from ehgat.baselines.brkga import BRKGAConfig, run_brkga
    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.benchmark.faithfulness import evaluate_faithfulness
    from ehgat.environment.decoder import NUM_BLOCKS, decode
    from ehgat.environment.instance import EXACT_TOY_TASKS
    from ehgat.environment.oracle import exact_pareto_front
    from ehgat.explain.fused_explainer import faithfulness_report
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
    from ehgat.metrics import gd_plus, hypervolume, igd_plus, nadir_reference, spread
    from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2
    from ehgat.utils.seeding import make_rng

    instance, label = _load_instance(args.instance, args.peak_power)
    n = instance.num_tasks
    coupled = instance.peak_power is not None
    base_pop = args.p_mult * n   # mp per-population size P (paper: 20*N)
    matched_pop = 4 * base_pop   # GAT/BRKGA pop so exact-evals/gen match mp (Omega+Pi=4)
    G = args.gens
    tag = label.replace(":", "") + ("_pp%g" % args.peak_power if coupled else "_unc")

    print(f"instance={label} N={n} coupled={coupled} | mp P={base_pop}x4, GAT/BRKGA pop={matched_pop} "
          f"| gens={G} | matched evals/gen={matched_pop}", flush=True)

    # ---- train core + fused TAPE head (the engine behind Signal #3) ----
    print("training core + fused TAPE head ...", flush=True)
    core = build_core(instance, seed=0, num_samples=args.core_samples,
                      epochs=args.core_epochs, device=args.device)
    fused_res = train_fused(instance, core, FusedTrainConfig(
        num_samples=args.fused_samples, epochs=args.fused_epochs,
        unroll_steps=(args.unroll if coupled else 0), seed=0))
    fused = fused_res.model.cpu()
    core = core.cpu()
    print(f"  fused R2_makespan={fused_res.metrics.get('r2_makespan'):.4f} "
          f"R2_energy={fused_res.metrics.get('r2_energy'):.4f}", flush=True)

    # ---- arms (all at matched exact-eval budget) ----
    def run_tape(seed: int):
        r = run_attention_nsga2(instance, None, AttentionNSGA2Config(
            matched_pop, G, seed=seed, guidance="tape", screening_factor=args.screening,
            mutation_temperature=args.mutation_temperature), fused_model=fused)
        return r.front, r.evaluations

    def run_attn(seed: int):
        r = run_attention_nsga2(instance, core, AttentionNSGA2Config(
            matched_pop, G, seed=seed, guidance="attention", screening_factor=args.screening,
            mutation_temperature=args.mutation_temperature))
        return r.front, r.evaluations

    def run_rand(seed: int):
        r = run_attention_nsga2(instance, core, AttentionNSGA2Config(
            matched_pop, G, seed=seed, random_mutation=True, screening_factor=1))
        return r.front, r.evaluations

    def run_mp(seed: int):
        r = run_mp_brkga(instance, MpBRKGAConfig(pop_size=base_pop, generations=G, seed=seed))
        return r.front, r.evaluations

    def run_sp(seed: int):
        r = run_brkga(instance, BRKGAConfig(pop_size=matched_pop, generations=G, seed=seed))
        return r.front, r.evaluations

    methods = {
        "E-HGATv2-TAPE": run_tape,
        "E-HGATv2-attn": run_attn,
        "NSGA-II (random)": run_rand,
        "mp-BRKGA": run_mp,
        "single-pop BRKGA": run_sp,
    }

    # ---- reference PF* proxy ----
    if label.startswith("toy:") and n <= EXACT_TOY_TASKS and not coupled:
        reference = tuple((float(m), float(e)) for m, e in exact_pareto_front(instance).front)
        ref_kind = "exact Oracle"
    else:
        pool: list[tuple[float, float]] = []
        rg = args.ref_gens
        pool += list(run_mp_brkga(instance, MpBRKGAConfig(base_pop, rg, seed=1000)).front)
        pool += list(run_brkga(instance, BRKGAConfig(matched_pop, rg, seed=1000)).front)
        pool += list(run_attention_nsga2(instance, None, AttentionNSGA2Config(
            matched_pop, rg, seed=1000, guidance="tape", screening_factor=args.screening),
            fused_model=fused).front)
        reference = _pareto(pool)
        ref_kind = f"non-dominated union of mp-BRKGA + BRKGA + TAPE @ {rg} gens"
    ref_point = nadir_reference(reference, margin=0.1)
    ref_hv = hypervolume(reference, ref_point)
    print(f"reference: {ref_kind} | {len(reference)} pts | HV*={ref_hv:.1f}", flush=True)

    # ---- optimisation runs ----
    raw: dict[str, dict[str, list[float]]] = {
        m: {"gd_plus": [], "igd_plus": [], "spread": [], "hv": [], "hv_ratio": [], "evals": []}
        for m in methods}
    t0 = time.perf_counter()
    for name, fn in methods.items():
        for seed in range(args.seeds):
            front, evals = fn(seed)
            raw[name]["gd_plus"].append(gd_plus(front, reference))
            raw[name]["igd_plus"].append(igd_plus(front, reference))
            raw[name]["spread"].append(spread(front, reference))
            hv = hypervolume(front, ref_point)
            raw[name]["hv"].append(hv)
            raw[name]["hv_ratio"].append(hv / ref_hv if ref_hv > 0 else float("nan"))
            raw[name]["evals"].append(float(evals))
        print(f"  {name}: done {args.seeds} seeds", flush=True)

    # ---- faithfulness head-to-head on a fixed schedule sample ----
    rng = make_rng(123)
    faith_scheds = [decode(rng.random(NUM_BLOCKS * n), instance) for _ in range(args.faith_samples)]
    attn_faith = evaluate_faithfulness(faith_scheds, instance, core)
    tape_reports = [faithfulness_report(fused, s, instance) for s in faith_scheds]
    tape_jaccard = float(np.mean([r.leg_critical_jaccard for r in tape_reports]))
    tape_cmax_err = float(np.mean([r.makespan_abs_error for r in tape_reports]))
    faithfulness = {
        "attention_precision_at_1": attn_faith.precision_at_1,
        "attention_spearman_rho": attn_faith.spearman_rho,
        "tape_leg_critical_jaccard": tape_jaccard,
        "tape_makespan_abs_error": tape_cmax_err,
        "random_precision_at_1_baseline": 1.0 / n,
    }

    metrics = [("hv_ratio", "HV / HV*", 4), ("gd_plus", "GD+", 4),
               ("igd_plus", "IGD+", 4), ("spread", "Spread", 4), ("evals", "true evals", 0)]
    agg = {m: {k: _ci(raw[m][k]) for k, *_ in metrics} for m in methods}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"tape_bench_{tag}.json").write_text(json.dumps(
        {"instance": label, "n": n, "coupled": coupled, "peak_power": args.peak_power,
         "gens": G, "seeds": args.seeds, "p_mult": args.p_mult, "base_pop": base_pop,
         "matched_pop": matched_pop, "screening": args.screening,
         "ref_kind": ref_kind, "ref_hv": ref_hv, "faithfulness": faithfulness, "raw": raw,
         "aggregate": {m: {k: list(v) for k, v in agg[m].items()} for m in methods}}, indent=2))

    md = [f"# Faithful-guidance study -- {label} (N={n}, {'coupled' if coupled else 'uncoupled'})",
          f"\n_{args.seeds} seeds, {G} gens, matched exact-eval budget (mp {base_pop}x4 = "
          f"GAT/BRKGA {matched_pop}/gen). Reference: {ref_kind}. Cells = mean (95% CI)._\n",
          "## Optimisation (Req 3)\n",
          "| Method | " + " | ".join(lbl for _, lbl, _ in metrics) + " |",
          "|---|" + "|".join(["---"] * len(metrics)) + "|"]
    for m in methods:
        cells = []
        for k, _lbl, dec in metrics:
            mean, half = agg[m][k]
            cells.append(f"{mean:.{dec}f} ± {half:.{dec}f}" if dec else f"{mean:.0f}")
        md.append(f"| {m} | " + " | ".join(cells) + " |")
    md += ["\n## Guidance-signal faithfulness (Req 2)\n",
           "| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |",
           "|---|---|---|---|",
           f"| attention (Signal #1) | {attn_faith.precision_at_1:.3f} | "
           f"{attn_faith.spearman_rho:.3f} | n/a |",
           f"| **TAPE (Signal #3)** | n/a | n/a | **{tape_jaccard:.3f}** |",
           f"| random baseline | {1.0 / n:.3f} | 0.000 | n/a |",
           f"\n_TAPE makespan abs-error vs oracle: {tape_cmax_err:.3f}. "
           f"A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._\n"]
    md_text = "\n".join(md) + "\n"
    (OUT_DIR / f"tape_bench_{tag}.md").write_text(md_text)
    print("\n" + md_text, flush=True)
    print(f"wrote experiments/fused_tape_guided/tape_bench_{tag}.* "
          f"(total {time.perf_counter() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
