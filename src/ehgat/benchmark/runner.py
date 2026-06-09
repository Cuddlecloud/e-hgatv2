"""Multi-seed effectiveness benchmark (Module 5) -- BRKGA vs E-HGATv2-NSGA-II.

Runs three methods on the exact toy under a **shared evaluation budget** (identical
``pop_size`` and ``generations`` => identical evaluations) and against the **same** golden
``PF*`` and hypervolume reference point, so the comparison is apples-to-apples:

- ``BRKGA`` -- the stochastic baseline (Module 2);
- ``E-HGATv2-NSGA-II`` -- attention-guided mutation (Module 4);
- ``NSGA-II (random)`` -- the H2 ablation: the identical skeleton with attention replaced
  by uniform task selection, isolating the causal contribution of attention.

For each method it records the per-generation hypervolume curve (mean + normal CI band
across seeds, the H1 convergence story) and final-front HV / IGD+ / GD+ / spread with
bootstrap CIs. It also reports H3 attention faithfulness for the trained surrogate against
a random-selection baseline. The surrogate is trained **once** and reused across seeds.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np

from ehgat.baselines.brkga import BRKGAConfig, run_brkga
from ehgat.benchmark.faithfulness import (
    FaithfulnessResult,
    critical_agv_arcs,
    evaluate_faithfulness,
)
from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.instance import EXACT_TOY_TASKS, Instance, build_toy_instance
from ehgat.environment.oracle import exact_pareto_front
from ehgat.metrics import gd_plus, hypervolume, igd_plus, nadir_reference, spread
from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2
from ehgat.surrogate.ehgatv2 import EHGATv2
from ehgat.surrogate.train import TrainConfig, train_surrogate
from ehgat.utils.seeding import make_rng

__all__ = [
    "BenchmarkConfig",
    "BenchmarkResult",
    "MethodResult",
    "Stat",
    "run_benchmark",
]

Front = Sequence[tuple[float, float]]
_BRKGA = "BRKGA"
_GUIDED = "E-HGATv2-NSGA-II"
_RANDOM = "NSGA-II (random)"
_Z_95 = 1.959963984540054  # normal two-sided 95% multiplier


@dataclass(frozen=True, slots=True)
class Stat:
    """A point estimate with a (bootstrap) confidence interval."""

    mean: float
    lo: float
    hi: float


@dataclass(frozen=True, slots=True)
class BenchmarkConfig:
    """Configuration for the effectiveness benchmark."""

    num_tasks: int = EXACT_TOY_TASKS
    generations: int = 60
    pop_size: int | None = None  # default 20N (matches BRKGA + attention search)
    num_seeds: int = 10
    base_seed: int = 0
    surrogate_samples: int = 1000
    surrogate_epochs: int = 50
    hv_margin: float = 0.1
    faithfulness_samples: int = 60
    bootstrap_resamples: int = 2000
    ci: float = 0.95

    @property
    def seeds(self) -> tuple[int, ...]:
        return tuple(range(self.base_seed, self.base_seed + self.num_seeds))


@dataclass(frozen=True, slots=True)
class MethodResult:
    """Per-method aggregate across seeds."""

    name: str
    hv_curve_mean: np.ndarray  # [generations + 1]
    hv_curve_lo: np.ndarray
    hv_curve_hi: np.ndarray
    hv_curves: np.ndarray  # [num_seeds, generations + 1] raw
    final_hv: Stat
    final_igd_plus: Stat
    final_gd_plus: Stat
    final_spread: Stat
    final_fronts: tuple[tuple[tuple[float, float], ...], ...]  # per seed


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Full benchmark outcome (charts + tables are derived from this)."""

    config: BenchmarkConfig
    num_tasks: int
    num_agvs: int
    num_qcs: int
    pop_size: int
    generations: int
    golden_front: tuple[tuple[float, float], ...]
    golden_hv: float
    reference_point: tuple[float, float]
    methods: dict[str, MethodResult] = field(default_factory=dict)
    faithfulness: dict[str, FaithfulnessResult] = field(default_factory=dict)
    random_precision_at_1: float = 0.0


def _bootstrap_ci(
    values: np.ndarray, *, resamples: int, ci: float, rng: np.random.Generator
) -> Stat:
    arr = np.asarray(values, dtype=float)
    mean = float(arr.mean())
    if arr.size < 2:
        return Stat(mean, mean, mean)
    idx = rng.integers(0, arr.size, size=(resamples, arr.size))
    boots = arr[idx].mean(axis=1)
    alpha = 1.0 - ci
    return Stat(
        mean,
        float(np.quantile(boots, alpha / 2)),
        float(np.quantile(boots, 1 - alpha / 2)),
    )


def _normal_band(curves: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-generation mean and 95% normal CI band across seeds."""
    mean = curves.mean(axis=0)
    n = curves.shape[0]
    if n < 2:
        return mean, mean.copy(), mean.copy()
    sem = curves.std(axis=0, ddof=1) / math.sqrt(n)
    return mean, mean - _Z_95 * sem, mean + _Z_95 * sem


def _hv_curve(history: Sequence[Front], reference: tuple[float, float]) -> list[float]:
    return [hypervolume(front, reference) for front in history]


def _evaluate_method(
    name: str,
    run: Callable[[int], tuple[Sequence[Front], Front]],
    *,
    config: BenchmarkConfig,
    golden: Front,
    reference: tuple[float, float],
    stat_rng: np.random.Generator,
) -> MethodResult:
    curves: list[list[float]] = []
    final_fronts: list[tuple[tuple[float, float], ...]] = []
    final_hv: list[float] = []
    final_igd: list[float] = []
    final_gd: list[float] = []
    final_spread: list[float] = []
    for seed in config.seeds:
        history, final = run(seed)
        curves.append(_hv_curve(history, reference))
        final_fronts.append(tuple((float(m), float(e)) for m, e in final))
        final_hv.append(hypervolume(final, reference))
        final_igd.append(igd_plus(final, golden))
        final_gd.append(gd_plus(final, golden))
        final_spread.append(spread(final, golden))

    curve_arr = np.asarray(curves, dtype=float)
    mean, lo, hi = _normal_band(curve_arr)
    _rsp = config.bootstrap_resamples
    _ci = config.ci
    return MethodResult(
        name=name,
        hv_curve_mean=mean,
        hv_curve_lo=lo,
        hv_curve_hi=hi,
        hv_curves=curve_arr,
        final_hv=_bootstrap_ci(np.asarray(final_hv), resamples=_rsp, ci=_ci, rng=stat_rng),
        final_igd_plus=_bootstrap_ci(np.asarray(final_igd), resamples=_rsp, ci=_ci, rng=stat_rng),
        final_gd_plus=_bootstrap_ci(np.asarray(final_gd), resamples=_rsp, ci=_ci, rng=stat_rng),
        final_spread=_bootstrap_ci(np.asarray(final_spread), resamples=_rsp, ci=_ci, rng=stat_rng),
        final_fronts=tuple(final_fronts),
    )


def _random_precision_at_1(
    instance: Instance, model: EHGATv2, n_samples: int, seed: int
) -> float:
    """Expected precision@1 of selecting a uniformly random AGV arc (the H3 foil)."""
    rng = make_rng(seed)
    n = instance.num_tasks
    chrom_len = NUM_BLOCKS * n
    total = 0.0
    for _ in range(n_samples):
        sched = decode(rng.random(chrom_len), instance)
        total += len(critical_agv_arcs(sched, instance)) / n  # P(random arc is critical)
    return total / n_samples


def run_benchmark(config: BenchmarkConfig | None = None) -> BenchmarkResult:
    """Run the full multi-seed effectiveness benchmark and return its aggregate result."""
    config = config or BenchmarkConfig()
    instance = build_toy_instance(num_tasks=config.num_tasks)
    pop_size = config.pop_size or 20 * instance.num_tasks
    generations = config.generations

    oracle = exact_pareto_front(instance)
    golden = tuple((float(m), float(e)) for m, e in oracle.front)
    reference = nadir_reference(golden, margin=config.hv_margin)
    golden_hv = hypervolume(golden, reference)

    model = train_surrogate(
        instance,
        TrainConfig(num_samples=config.surrogate_samples, epochs=config.surrogate_epochs, seed=0),
    ).model

    stat_rng = make_rng(12345)  # dedicated stream for bootstrap, independent of search seeds

    def brkga_run(seed: int) -> tuple[Sequence[Front], Front]:
        res = run_brkga(
            instance, BRKGAConfig(pop_size=pop_size, generations=generations, seed=seed)
        )
        return res.front_history, res.front

    def guided_run(seed: int) -> tuple[Sequence[Front], Front]:
        res = run_attention_nsga2(
            instance, model, AttentionNSGA2Config(pop_size, generations, seed=seed)
        )
        return res.front_history, res.front

    def random_run(seed: int) -> tuple[Sequence[Front], Front]:
        res = run_attention_nsga2(
            instance,
            model,
            AttentionNSGA2Config(pop_size, generations, seed=seed, random_mutation=True),
        )
        return res.front_history, res.front

    methods = {
        name: _evaluate_method(
            name, run, config=config, golden=golden, reference=reference, stat_rng=stat_rng
        )
        for name, run in ((_BRKGA, brkga_run), (_GUIDED, guided_run), (_RANDOM, random_run))
    }

    faith_rng = make_rng(999)
    chrom_len = NUM_BLOCKS * instance.num_tasks
    faith_schedules = [
        decode(faith_rng.random(chrom_len), instance) for _ in range(config.faithfulness_samples)
    ]
    faithfulness = {_GUIDED: evaluate_faithfulness(faith_schedules, instance, model)}
    random_p1 = _random_precision_at_1(instance, model, config.faithfulness_samples, seed=999)

    return BenchmarkResult(
        config=config,
        num_tasks=instance.num_tasks,
        num_agvs=instance.num_agvs,
        num_qcs=len(instance.qcs),
        pop_size=pop_size,
        generations=generations,
        golden_front=golden,
        golden_hv=golden_hv,
        reference_point=reference,
        methods=methods,
        faithfulness=faithfulness,
        random_precision_at_1=random_p1,
    )
