"""Cross-instance transfer of Pareto-front behaviour for the E-HGATv2 surrogate.

A single surrogate is fitted on schedules harvested from guided search over a set
of training instances, frozen, and applied without refitting to held-out
instances. Three quantities are measured per held-out instance.

Front recovery. The surrogate predicts (C_max, E) over a candidate pool; the
non-dominated subset of those predictions is scored against the exact
non-dominated subset of the same pool, by hypervolume ratio and IGD+.

Front structure. The transport share rho of the critical path and the bottleneck
migration between the makespan- and energy-optimal extremes are read from the
surrogate's tropical gradients and compared against the exact max-plus backtrack.

Guidance transfer. The frozen surrogate steers NSGA-II on the held-out instance;
hypervolume is reported against an unguided arm at matched evaluation budget.

Three reference arms bound the comparison: a surrogate refitted on the held-out
instance (upper bound), a surrogate fitted on i.i.d. random schedules at matched
sample budget (isolating the contribution of search-derived training data), and a
structure-blind random selection of pool members (floor).

Usage
-----
    python scripts/run_front_transfer.py --train L01 L02 L03 --test L07

    python scripts/run_front_transfer.py --train ... --test L07 --seed 3 \
        --out experiments/front_transfer/shard_L07_s3.json
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

OUT = Path(__file__).resolve().parents[1] / "experiments" / "front_transfer"


# --------------------------------------------------------------------------
# Instance resolution
# --------------------------------------------------------------------------
def load_instance(spec: str, peak_power: float | None):
    """Resolve an instance specification to an :class:`Instance`.

    Accepts ``toy:N[:Q[:A]]`` for the synthetic generator, or a published
    identifier (``L07``) drawn from Tables 4-5 of Homayouni and Fontes (2022).
    """
    from ehgat.environment.dsdl import load_tables_4_5
    from ehgat.environment.instance import AVAILABLE_QCS, build_toy_instance

    if spec.startswith("toy:"):
        parts = spec.split(":")
        n = int(parts[1])
        num_qcs = int(parts[2]) if len(parts) > 2 else 3
        num_agvs = int(parts[3]) if len(parts) > 3 else 2
        if num_qcs > len(AVAILABLE_QCS):
            raise ValueError(f"{spec}: num_qcs={num_qcs} exceeds {len(AVAILABLE_QCS)}")
        return build_toy_instance(
            num_tasks=n, qcs=AVAILABLE_QCS[:num_qcs], num_agvs=num_agvs,
            peak_power=peak_power)
    data = Path(__file__).resolve().parents[1] / "data" / "tables_4_5.json"
    return load_tables_4_5(data, peak_power=peak_power, only=[spec])[0].instance


# --------------------------------------------------------------------------
# Candidate pools
# --------------------------------------------------------------------------
def _breed(parents: list, n: int, chrom_len: int, rng) -> list:
    """Breed ``n`` chromosomes from ``parents`` by uniform crossover and jitter.

    Each gene is inherited from one of two uniformly drawn parents; a further
    2/L of genes are resampled uniformly, giving a pool concentrated in the
    neighbourhood of the parent set rather than over the whole key space.
    """
    pool = []
    for _ in range(n):
        a, b = rng.integers(0, len(parents), size=2)
        mask = rng.random(chrom_len) < 0.5
        child = np.where(mask, parents[a], parents[b]).astype(float)
        jitter = rng.random(chrom_len) < (2.0 / chrom_len)
        child[jitter] = rng.random(int(jitter.sum()))
        pool.append(np.clip(child, 0.0, 1.0))
    return pool


def search_derived_pool(instance, fused, *, gens: int, pool_size: int, seed: int):
    """Construct a near-front candidate pool from a short guided search.

    A TAPE-guided run of ``gens`` generations supplies an archive, around which
    offspring are bred. The resulting pool is concentrated near the front, where
    objective differences between candidates are small and ranking is therefore
    discriminating. Uniformly sampled random keys spread candidates over the
    whole objective range and understate the difficulty of the ranking task.
    """
    from ehgat.environment.decoder import NUM_BLOCKS, decode, encode_canonical
    from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2
    from ehgat.utils.seeding import make_rng

    n = instance.num_tasks
    chrom_len = NUM_BLOCKS * n
    pop = max(8, 5 * n)

    warm = run_attention_nsga2(
        instance, None,
        AttentionNSGA2Config(pop_size=pop, generations=gens, guidance="tape",
                             screening_factor=1, seed=seed),
        fused_model=fused)

    rng = make_rng(seed + 7)
    parents = [encode_canonical(s, instance) for s in warm.schedules]
    if len(parents) < 2:
        parents = [rng.random(chrom_len) for _ in range(pop)]

    keys = _breed(parents, pool_size, chrom_len, rng)
    scheds, seen = [], set()
    for k in keys:
        try:
            s = decode(k, instance)
        except Exception:
            continue
        sig = (tuple(s.assignment), tuple(s.global_order),
               tuple(s.loaded_speed), tuple(s.empty_speed))
        if sig in seen:
            continue
        seen.add(sig)
        scheds.append(s)
    return scheds, warm


def random_pool(instance, *, pool_size: int, seed: int):
    from ehgat.environment.decoder import NUM_BLOCKS, decode
    from ehgat.utils.seeding import make_rng

    rng = make_rng(seed)
    out = []
    for _ in range(pool_size):
        try:
            out.append(decode(rng.random(NUM_BLOCKS * instance.num_tasks), instance))
        except Exception:
            continue
    return out


# --------------------------------------------------------------------------
# Training samples anchored on supplied schedules
# --------------------------------------------------------------------------
def samples_from_schedules(instance, schedules: list):
    """Anchored fused-training samples for a given set of schedules.

    Mirrors :func:`ehgat.explain.train_fused.build_samples`, except that the
    schedules are supplied by the caller rather than decoded from uniform random
    keys, so the training distribution is that of the search trajectory.
    """
    import torch

    from ehgat.environment.evaluator import evaluate
    from ehgat.explain.train_fused import FusedSample, _exact_legs
    from ehgat.surrogate.graph import build_hetero_graph

    n = instance.num_tasks
    out = []
    for s in schedules:
        ev = evaluate(s, instance)
        legs, tau = _exact_legs(s, instance)
        if ev.wait_empty:
            waits = torch.tensor(
                list(zip(ev.wait_empty, ev.wait_loaded, strict=True)),
                dtype=torch.float32)
        else:
            waits = torch.zeros((n, 2), dtype=torch.float32)
        out.append(FusedSample(
            data=build_hetero_graph(s, instance),
            legs=legs, tau=tau,
            objectives=torch.tensor(list(ev.objectives), dtype=torch.float32),
            waits=waits, power_arcs=tuple(ev.power_arcs)))
    return out


# --------------------------------------------------------------------------
# Front-recovery and front-structure measures
# --------------------------------------------------------------------------
@dataclass
class FrontScore:
    n_pred: int
    n_true: int
    hv_ratio: float
    igd_plus: float
    transport_share_pred: float
    transport_share_true: float
    migration_pred: float
    migration_true: float


def _transport_share(model, instance, schedules: list) -> float:
    """Surrogate estimate of the transport share rho over a set of schedules.

    Legs and handlings are counted as binding where the corresponding tropical
    gradient exceeds one half; rho is the AGV-leg count as a fraction of all
    binding activities.
    """
    from ehgat.explain.fused_explainer import explain_fused

    shares = []
    for s in schedules:
        ex = explain_fused(model, s, instance)
        n_t = float((np.asarray(ex.empty_time_grad) > 0.5).sum()
                    + (np.asarray(ex.loaded_time_grad) > 0.5).sum())
        n_q = float((np.asarray(ex.node_grad) > 0.5).sum())
        if n_t + n_q > 0:
            shares.append(n_t / (n_t + n_q))
    return float(np.mean(shares)) if shares else float("nan")


def _transport_share_exact(instance, schedules: list) -> float:
    """Exact transport share rho of the critical path, averaged over schedules.

    Obtained from the max-plus backtrack of
    :func:`ehgat.benchmark.faithfulness.critical_path_binding`, which partitions
    the critical path into AGV- and QC-bound tasks. No surrogate is involved.
    """
    from ehgat.benchmark.faithfulness import critical_path_binding

    shares = []
    for s in schedules:
        agv, qc = critical_path_binding(s, instance)
        tot = len(agv) + len(qc)
        if tot:
            shares.append(len(agv) / tot)
    return float(np.mean(shares)) if shares else float("nan")


def _crit_tasks_exact(instance, schedule) -> set[int]:
    from ehgat.benchmark.faithfulness import critical_path_binding

    agv, qc = critical_path_binding(schedule, instance)
    return set(agv) | set(qc)


def _migration_exact(instance, front_scheds: list, objs: list) -> float:
    """Exact bottleneck migration between the two extremes of a front.

    Defined as one minus the Jaccard index of the exact critical-task sets at the
    makespan-optimal and energy-optimal ends, so that zero denotes an unchanged
    bottleneck and one a wholly disjoint one.
    """
    if len(front_scheds) < 2:
        return float("nan")
    order = np.argsort([o[0] for o in objs])
    a = _crit_tasks_exact(instance, front_scheds[order[0]])
    b = _crit_tasks_exact(instance, front_scheds[order[-1]])
    union = a | b
    return 1.0 - (len(a & b) / len(union)) if union else float("nan")


def _top_tasks(model, instance, schedule, k: int = 3) -> set[int]:
    from ehgat.explain.fused_explainer import explain_fused

    ex = explain_fused(model, schedule, instance)
    per_task = (np.asarray(ex.empty_time_grad) + np.asarray(ex.loaded_time_grad)
                + np.asarray(ex.node_grad))
    return set(np.argsort(-per_task)[:k].tolist())


def _migration(model, instance, front_scheds: list, objs: list) -> float:
    """Surrogate estimate of the bottleneck migration across a front.

    Defined as one minus the Jaccard index of the three most strongly binding
    tasks at the makespan-optimal and energy-optimal ends, ranked by the summed
    tropical gradients of the surrogate.
    """
    if len(front_scheds) < 2:
        return float("nan")
    order = np.argsort([o[0] for o in objs])
    mk, en = front_scheds[order[0]], front_scheds[order[-1]]
    a, b = _top_tasks(model, instance, mk), _top_tasks(model, instance, en)
    union = a | b
    return 1.0 - (len(a & b) / len(union)) if union else float("nan")


def pool_reference(instance, pool: list):
    """Nadir reference point and exact objective vectors for a candidate pool.

    The reference is derived from the exact objectives of the entire pool and is
    therefore independent of any surrogate's selection, which is required for
    hypervolumes computed under different arms to be comparable.
    """
    from ehgat.environment.evaluator import evaluate
    from ehgat.metrics import nadir_reference

    true = [tuple(map(float, evaluate(s, instance).objectives)) for s in pool]
    return nadir_reference(true), true


def score_front(model, instance, pool: list, ref, true: list) -> FrontScore:
    """Score the surrogate-selected front against the exact front of a pool.

    The surrogate ranks the pool by predicted (C_max, E); its non-dominated
    subset is then re-scored with exact objectives, so the reported hypervolume
    measures the quality of the selection rather than the accuracy of the
    prediction. ``ref`` and ``true`` are supplied by :func:`pool_reference`.
    """
    from ehgat.metrics import hypervolume, igd_plus
    from ehgat.search.nsga2 import non_dominated_indices
    from ehgat.search.tape_guidance import tape_predict_objectives

    pred = [(float(p[0]), float(p[1]))
            for p in tape_predict_objectives(model, pool, instance)]

    ip = non_dominated_indices(pred)
    it = non_dominated_indices(true)
    # Exact objectives are used for both selections, so the comparison isolates
    # ranking quality from prediction error.
    sel = [true[i] for i in ip]
    tru = [true[i] for i in it]

    hv_sel, hv_tru = hypervolume(sel, ref), hypervolume(tru, ref)

    sel_s = [pool[i] for i in ip]
    tru_s = [pool[i] for i in it]
    return FrontScore(
        n_pred=len(sel), n_true=len(tru),
        hv_ratio=float(hv_sel / hv_tru) if hv_tru > 0 else float("nan"),
        igd_plus=float(igd_plus(sel, tru)),
        # Surrogate estimates are read from tropical gradients on the selected
        # front; the reference values derive from the exact max-plus backtrack.
        transport_share_pred=_transport_share(model, instance, sel_s[:24]),
        transport_share_true=_transport_share_exact(instance, tru_s[:24]),
        migration_pred=_migration(model, instance, sel_s, sel),
        migration_true=_migration_exact(instance, tru_s, tru),
    )


def naive_floor(instance, pool: list, ref, true: list, seed: int) -> dict:
    """Floor obtained by selecting pool members uniformly at random.

    The selection is size-matched to the exact front, so any surrogate that
    fails to exceed this baseline has extracted no usable information about
    front membership.
    """
    from ehgat.metrics import hypervolume, igd_plus
    from ehgat.search.nsga2 import non_dominated_indices
    from ehgat.utils.seeding import make_rng

    it = non_dominated_indices(true)
    tru = [true[i] for i in it]
    rng = make_rng(seed + 11)
    pick = rng.choice(len(pool), size=min(len(it), len(pool)), replace=False)
    sel = [true[i] for i in pick]
    hv_tru = hypervolume(tru, ref)
    return {"hv_ratio": float(hypervolume(sel, ref) / hv_tru) if hv_tru > 0 else float("nan"),
            "igd_plus": float(igd_plus(sel, tru))}


# --------------------------------------------------------------------------
# Training arms
# --------------------------------------------------------------------------
def train_pooled(train_specs: list[str], peak_power, args):
    """Fit one surrogate on search-derived schedules pooled across instances.

    The frozen embedding core is fitted on the largest training instance; the
    fused head, which supplies the objective predictions, is then fitted on the
    pooled cross-instance sample set through the sample-injection path of
    :func:`ehgat.explain.train_fused.train_fused`. A bootstrap head of reduced
    width drives the harvesting search, since a trajectory cannot be gathered
    before some surrogate exists.
    """
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused

    insts = [(s, load_instance(s, peak_power)) for s in train_specs]
    insts.sort(key=lambda kv: kv[1].num_tasks)
    anchor_spec, anchor = insts[-1]

    print(f"  core on anchor {anchor_spec} (N={anchor.num_tasks})", flush=True)
    core = build_core(anchor, seed=args.seed, num_samples=args.core_samples,
                      epochs=args.core_epochs, device=args.device)

    per = max(16, args.traj_samples // max(1, len(insts)))
    pooled = []
    for spec, inst in insts:
        # A reduced-width head suffices to drive the harvesting search.
        boot = train_fused(inst, core, FusedTrainConfig(
            num_samples=min(300, args.fused_samples), epochs=20,
            unroll_steps=(2 if peak_power else 0), seed=args.seed)).model
        scheds, _ = search_derived_pool(inst, boot, gens=args.warm_gens,
                                        pool_size=per, seed=args.seed)
        pooled += samples_from_schedules(inst, scheds[:per])
        print(f"  trajectory {spec}: +{min(len(scheds), per)} samples", flush=True)

    res = train_fused(anchor, core, FusedTrainConfig(
        epochs=args.fused_epochs, unroll_steps=(2 if peak_power else 0),
        seed=args.seed), samples=pooled)
    return res.model, res.metrics, len(pooled)


def train_random_matched(train_specs: list[str], peak_power, args, n_samples: int):
    """Reference arm fitted on i.i.d. random schedules at matched sample budget.

    Differs from :func:`train_pooled` only in the training distribution, and
    therefore isolates the contribution of search-derived data.
    """
    from ehgat.explain.train_fused import (FusedTrainConfig, build_core,
                                           build_samples, train_fused)

    insts = [(s, load_instance(s, peak_power)) for s in train_specs]
    insts.sort(key=lambda kv: kv[1].num_tasks)
    _, anchor = insts[-1]
    core = build_core(anchor, seed=args.seed, num_samples=args.core_samples,
                      epochs=args.core_epochs, device=args.device)
    per = max(16, n_samples // max(1, len(insts)))
    pooled = []
    for _, inst in insts:
        pooled += build_samples(inst, per, seed=args.seed)
    res = train_fused(anchor, core, FusedTrainConfig(
        epochs=args.fused_epochs, unroll_steps=(2 if peak_power else 0),
        seed=args.seed), samples=pooled)
    return res.model, res.metrics


def train_refit(instance, peak_power, args):
    """Reference arm fitted on the held-out instance itself.

    Provides an upper bound, since no transfer is required.
    """
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused

    core = build_core(instance, seed=args.seed, num_samples=args.core_samples,
                      epochs=args.core_epochs, device=args.device)
    res = train_fused(instance, core, FusedTrainConfig(
        num_samples=args.fused_samples, epochs=args.fused_epochs,
        unroll_steps=(2 if peak_power else 0), seed=args.seed))
    return res.model, res.metrics


# --------------------------------------------------------------------------
# Guidance transfer under the frozen surrogate
# --------------------------------------------------------------------------
def guided_hv(instance, fused, *, gens: int, seed: int) -> dict:
    from ehgat.metrics import hypervolume, nadir_reference
    from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2

    pop = max(8, 5 * instance.num_tasks)
    arms = {}
    # The unguided arm disables both guidance channels: mutation targets are drawn
    # uniformly and no offspring over-production occurs, matching the ablation floor
    # of the accompanying study at an identical evaluation budget.
    for name, rand_mut, screen in (("guided", False, 3), ("baseline", True, 1)):
        r = run_attention_nsga2(
            instance, None,
            AttentionNSGA2Config(pop_size=pop, generations=gens, guidance="tape",
                                 random_mutation=rand_mut, screening_factor=screen,
                                 seed=seed),
            fused_model=fused)
        arms[name] = ([tuple(map(float, o)) for o in r.front], r.evaluations)

    ref = nadir_reference(*[v[0] for v in arms.values()])
    out = {k: {"hv": float(hypervolume(v[0], ref)), "evaluations": int(v[1]),
               "front_size": len(v[0])} for k, v in arms.items()}
    # The reference point is derived from the two fronts of this call, so absolute
    # hypervolumes are comparable only within it. The guided-to-unguided ratio is
    # invariant to that choice and is therefore the quantity compared across arms.
    b = out["baseline"]["hv"]
    out["hv_ratio_guided_over_baseline"] = float(out["guided"]["hv"] / b) if b > 0 else float("nan")
    return out


# --------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--train", nargs="+", required=True, help="training instance specs")
    p.add_argument("--test", nargs="+", required=True, help="held-out instance specs")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--peak-power", type=float, default=None,
                   help="set to run the coupled regime (e.g. 30)")
    p.add_argument("--pool-size", type=int, default=600)
    p.add_argument("--warm-gens", type=int, default=15)
    p.add_argument("--payoff-gens", type=int, default=40)
    p.add_argument("--core-samples", type=int, default=1500)
    p.add_argument("--core-epochs", type=int, default=60)
    p.add_argument("--fused-samples", type=int, default=800)
    p.add_argument("--fused-epochs", type=int, default=80)
    p.add_argument("--traj-samples", type=int, default=800)
    p.add_argument("--device", default="cpu")
    p.add_argument("--arms", nargs="+",
                   default=["transfer", "random", "refit"],
                   help="which training arms to run")
    p.add_argument("--skip-payoff", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    pp = args.peak_power
    overlap = set(args.train) & set(args.test)
    if overlap:
        raise SystemExit(f"train/test overlap -- that invalidates the claim: {overlap}")

    result: dict = {"config": vars(args), "arms": {}}

    models: dict = {}
    if "transfer" in args.arms:
        print("[transfer] one surrogate, search-gathered, pooled across instances",
              flush=True)
        m, metrics, n_pool = train_pooled(args.train, pp, args)
        models["transfer"] = m
        result["arms"]["transfer"] = {"train_metrics": metrics, "n_samples": n_pool,
                                      "per_instance": {}}
    if "random" in args.arms:
        n = result["arms"].get("transfer", {}).get("n_samples", args.traj_samples)
        print(f"[random] control at matched budget ({n} samples)", flush=True)
        m, metrics = train_random_matched(args.train, pp, args, n)
        models["random"] = m
        result["arms"]["random"] = {"train_metrics": metrics, "per_instance": {}}

    for spec in args.test:
        inst = load_instance(spec, pp)
        print(f"\n=== held-out {spec} (N={inst.num_tasks}, "
              f"agvs={inst.num_agvs}, qcs={len(inst.qcs)}) ===", flush=True)

        # The pool is constructed with a surrogate that has not been fitted on this
        # instance, so pool composition does not depend on the held-out data.
        pool_model = models.get("transfer") or models.get("random")
        if pool_model is None:
            pool_model, _ = train_refit(inst, pp, args)
        pool, _ = search_derived_pool(inst, pool_model, gens=args.warm_gens,
                                      pool_size=args.pool_size, seed=args.seed)
        rand = random_pool(inst, pool_size=args.pool_size, seed=args.seed + 3)
        print(f"  near-front pool={len(pool)}  random pool={len(rand)}", flush=True)

        # One reference point per pool, shared by all arms.
        ref_nf, true_nf = pool_reference(inst, pool)
        ref_rp, true_rp = pool_reference(inst, rand)

        if "refit" in args.arms:
            m, metrics = train_refit(inst, pp, args)
            models["refit"] = m
            result["arms"].setdefault("refit", {"per_instance": {}})
            result["arms"]["refit"].setdefault("train_metrics", {})[spec] = metrics

        for arm in args.arms:
            if arm not in models:
                continue
            m = models[arm]
            entry = {
                "near_front": asdict(score_front(m, inst, pool, ref_nf, true_nf)),
                "random_pool": asdict(score_front(m, inst, rand, ref_rp, true_rp)),
            }
            if not args.skip_payoff:
                entry["payoff"] = guided_hv(inst, m, gens=args.payoff_gens,
                                            seed=args.seed)
            result["arms"][arm]["per_instance"][spec] = entry
            nf = entry["near_front"]
            print(f"  [{arm:8s}] near-front HV={nf['hv_ratio']:.4f} "
                  f"IGD+={nf['igd_plus']:.4f} "
                  f"|pred|={nf['n_pred']}/{nf['n_true']}", flush=True)

        result.setdefault("naive", {})[spec] = {
            "near_front": naive_floor(inst, pool, ref_nf, true_nf, args.seed),
            "random_pool": naive_floor(inst, rand, ref_rp, true_rp, args.seed),
        }

    out = Path(args.out) if args.out else OUT / f"front_transfer_s{args.seed}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
