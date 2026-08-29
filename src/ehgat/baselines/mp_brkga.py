"""Multi-population biased random-key genetic algorithm (mp-BRKGA).

Faithful reproduction of the advisor's baseline -- Fontes & Homayouni (2022),
*A bi-objective multi-population biased random key genetic algorithm for joint scheduling
of quay cranes and speed adjustable vehicles*, FSMJ 35:241-268, Section 4. This is the
**actual published state-of-the-art** the attention-guided E-HGATv2 search must beat, NOT
the single-population variant in :mod:`ehgat.baselines.brkga` (which is exactly the paper's
own ablation in its Fig. 6, where mp-BRKGA is shown to dominate it near the boundaries).

Algorithm (paper Sec. 4, verbatim mapping)
------------------------------------------
The method evolves ``Omega + Pi`` independent populations in parallel:

* **Omega single-objective populations** -- one per objective. Population ``o`` ranks by
  objective ``o`` alone, so it drives the *extreme/boundary* solution of that objective.
* **Pi multi-objective populations** -- each ranks all objectives with NSGA-II
  non-dominated sorting + crowding distance (Deb et al. 2002).

Each generation, for every population, the next generation is::

    Ne elites  +  No offspring  +  Nm mutants            (Ne+No+Nm = P)

with ``Ne = elite_frac * P``, ``Nm = mutant_frac * P``, ``P = pop_size`` (paper: 20N).
Offspring use **biased parameterized uniform crossover**: one parent is drawn from the
elite set, the other from the whole population, and each gene is inherited from the elite
parent with probability ``inherit_prob`` (``p_e``). Mutants are fresh random-key vectors.

**Migration via a shared elite pool** (the crux that distinguishes mp- from single-pop):
the ``Ne`` elites of a multi-objective population ``pi`` at generation ``g+1`` are *selected
from a pool*, not just its own best. The pool = ``pi``'s own best ``Ne`` (by rank/crowding)
PLUS the best ``Ne`` of **each** single-objective population (by that objective), deduped.
So boundary specialists migrate into the multi-objective populations. Additionally, every
``n_exchange`` generations *all* multi-objective populations also contribute their best
``Ne`` to the pool (pool size then up to ``(Omega+Pi)*Ne``; otherwise ``(Omega+1)*Ne``).
``Ne`` elites are then chosen from the pool by non-dominated rank + crowding.

Paper's chosen configuration: ``P=20N, elite_frac=0.2, mutant_frac=0.1, p_e=0.7,
Gmax=300, Pi=2, Omega=2, n_exchange=30``.

Final front = global non-dominated archive over every population and generation (>= the
paper's "merge best of each Omega pop + non-dominated of each Pi pop", since the archive
accumulates all of them and re-filters by dominance).

Fairness note for benchmarking
------------------------------
Per generation this evaluates ``(Omega+Pi)*P`` chromosomes -- e.g. 4x a single-population
run at the same ``P``/generations. Any head-to-head against the E-HGATv2 search must
therefore equalise the **total evaluation budget** (see ``evaluations`` on the result), not
just ``pop_size`` and ``generations``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import numpy as np

from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.evaluator import evaluate
from ehgat.environment.instance import Instance
from ehgat.search.nsga2 import fast_non_dominated_sort, order_by_rank_crowding
from ehgat.utils.seeding import make_rng

__all__ = ["MpBRKGAConfig", "MpBRKGAResult", "default_mp_config", "run_mp_brkga"]

Objectives = tuple[float, float]
# Maps an (n, chrom_len) array of candidate chromosomes to predicted (makespan, energy) per row.
ScreenFn = "Callable[[np.ndarray], list[Objectives]]"
_ARCHIVE_ROUND = 6


@dataclass(frozen=True, slots=True)
class MpBRKGAConfig:
    """mp-BRKGA hyper-parameters (defaults follow Fontes & Homayouni 2022, Sec. 5.2)."""

    pop_size: int  # P per population (paper: 20N)
    generations: int = 300  # Gmax
    elite_frac: float = 0.2
    mutant_frac: float = 0.1
    inherit_prob: float = 0.7  # p_e
    num_objectives: int = 2  # Omega single-objective populations (one per objective)
    num_multi: int = 2  # Pi multi-objective populations
    n_exchange: int = 30  # migrate all Pi pops' elites into the pool every n_exchange gens
    seed: int = 0
    screening_factor: int = 1  # k>1 => over-produce k*No offspring, surrogate-screen to No (needs screen_fn)
    snapshot_every: int = 0  # >0 => also retain archive chromosomes every N generations

    def __post_init__(self) -> None:
        if self.screening_factor < 1:
            raise ValueError("screening_factor must be >= 1")
        if self.num_objectives not in (0, 2):
            raise ValueError("num_objectives (Omega) must be 0 or 2 for this bi-objective problem")
        if self.num_multi < 1:
            raise ValueError("num_multi (Pi) must be >= 1")


@dataclass(frozen=True, slots=True)
class MpBRKGAResult:
    """Outcome of an mp-BRKGA run (mirrors :class:`~ehgat.baselines.brkga.BRKGAResult`)."""

    front: tuple[Objectives, ...]
    chromosomes: tuple[np.ndarray, ...]
    front_history: tuple[tuple[Objectives, ...], ...]
    evaluations: int
    # (generation, objectives, chromosomes) triples, populated only when
    # ``MpBRKGAConfig.snapshot_every`` is positive. ``front_history`` keeps objectives at every
    # generation but discards the chromosomes, so an explanation cannot be recomputed from it
    # after the fact; this retains what the attribution needs, at the cost of memory, and is
    # therefore opt-in rather than always on.
    chrom_snapshots: tuple[tuple[int, tuple[Objectives, ...], tuple[np.ndarray, ...]], ...] = ()


def default_mp_config(
    instance: Instance, *, generations: int = 300, seed: int = 0
) -> MpBRKGAConfig:
    """Paper-default mp-BRKGA config for ``instance`` (P = 20N, Omega=2, Pi=2, n_ex=30)."""
    return MpBRKGAConfig(pop_size=20 * instance.num_tasks, generations=generations, seed=seed)


def _evaluate_population(pop: np.ndarray, instance: Instance) -> list[Objectives]:
    return [evaluate(decode(chrom, instance), instance).objectives for chrom in pop]


def _biased_crossover(
    rng: np.random.Generator,
    elite_parent: np.ndarray,
    other_parent: np.ndarray,
    inherit_prob: float,
) -> np.ndarray:
    """Parameterized uniform crossover: inherit each elite gene w.p. ``inherit_prob``."""
    take_elite = rng.random(elite_parent.shape[0]) < inherit_prob
    return np.where(take_elite, elite_parent, other_parent)


def _breed(
    rng: np.random.Generator,
    pop: np.ndarray,
    elite_chrom: np.ndarray,
    n_elite: int,
    n_offspring: int,
    n_mutant: int,
    inherit_prob: float,
    rank_order: np.ndarray,
    screen_fn: "ScreenFn | None" = None,
    screening_factor: int = 1,
) -> np.ndarray:
    """Build the next population: ``Ne`` elites + ``No`` offspring + ``Nm`` mutants.

    ``elite_chrom`` is the carried elite block (>= ``n_elite`` rows). For single-objective
    populations it is that population's own best ``Ne``; for multi-objective populations it
    is the ``Ne`` selected from the migration *pool* (so immigrants can be carried). Each
    offspring crosses one elite parent with one parent drawn from the **non-elite** portion of
    the population, inheriting elite genes with probability ``inherit_prob``.

    The non-elite restriction follows the author's own code, where the two parents are drawn
    from disjoint ranges -- ``P1 = random.randint(0, elite)`` and
    ``P2 = random.randint(elite, Pmax)`` (mp-BRKGA_DL01.py:263-264) -- so an offspring can
    never be the child of two elites. He samples from ``popSORT``, freshly ranked this
    generation, so ``rank_order`` must be the *current* ranking; ``pop``'s own row order is one
    generation stale and is not a substitute for it.

    **Surrogate screening (ablation).** When ``screen_fn`` is given and ``screening_factor``
    ``k>1``, the offspring block is *over-produced* to ``k*No`` crossover children, ranked by
    the surrogate's predicted objectives (non-dominated rank + crowding), and the best ``No``
    are kept. Elites and mutants are untouched. Only the kept ``P`` chromosomes are exact-
    evaluated next generation, so screening adds ZERO exact evaluations -- the same free
    advantage the GNN-guided NSGA-II arm uses, ported to the mp-BRKGA backbone.
    """
    chrom_len = pop.shape[1]
    nxt = np.empty_like(pop)
    nxt[:n_elite] = elite_chrom[:n_elite]

    k = screening_factor if (screen_fn is not None and screening_factor > 1) else 1
    n_cand = n_offspring * k
    cand = np.empty((n_cand, chrom_len))
    # Second parent from this generation's non-elites, matching his disjoint P1/P2 ranges.
    # Guard the degenerate case of an all-elite population by falling back to the whole of it
    # rather than sampling an empty range.
    non_elite = rank_order[n_elite:] if n_elite < rank_order.size else rank_order
    for c in range(n_cand):
        ep = elite_chrom[rng.integers(elite_chrom.shape[0])]
        op = pop[non_elite[rng.integers(non_elite.size)]]
        cand[c] = _biased_crossover(rng, ep, op, inherit_prob)
    if k > 1:
        pred = screen_fn(cand)  # surrogate-predicted (makespan, energy) per candidate
        keep = order_by_rank_crowding(pred, fast_non_dominated_sort(pred))[:n_offspring]
        nxt[n_elite : n_elite + n_offspring] = cand[keep]
    else:
        nxt[n_elite : n_elite + n_offspring] = cand[:n_offspring]

    nxt[n_elite + n_offspring :] = rng.random((n_mutant, chrom_len))
    return nxt


def _dedup_pool(
    chroms: list[np.ndarray], objs: list[Objectives]
) -> tuple[list[np.ndarray], list[Objectives]]:
    """Deduplicate (chrom, obj) pairs by rounded-objective key, preserving order."""
    seen: set[tuple[float, float]] = set()
    out_c: list[np.ndarray] = []
    out_o: list[Objectives] = []
    for c, o in zip(chroms, objs, strict=True):
        key = (round(o[0], _ARCHIVE_ROUND), round(o[1], _ARCHIVE_ROUND))
        if key in seen:
            continue
        seen.add(key)
        out_c.append(c)
        out_o.append(o)
    return out_c, out_o


def _update_archive(
    archive_obj: list[Objectives],
    archive_chrom: list[np.ndarray],
    new_obj: list[Objectives],
    new_chrom: list[np.ndarray],
) -> tuple[list[Objectives], list[np.ndarray]]:
    """Merge ``new`` into the archive, keeping a deduplicated non-dominated set."""
    merged_chrom, merged_obj = _dedup_pool(
        archive_chrom + new_chrom, archive_obj + new_obj
    )
    keep = fast_non_dominated_sort(merged_obj)[0]
    return [merged_obj[i] for i in keep], [merged_chrom[i] for i in keep]


def run_mp_brkga(
    instance: Instance, config: MpBRKGAConfig, screen_fn: "ScreenFn | None" = None
) -> MpBRKGAResult:
    """Evolve the multi-population BRKGA and return its global non-dominated front.

    ``screen_fn`` (with ``config.screening_factor > 1``) enables budget-neutral surrogate
    screening of each population's offspring block -- the GNN-enhancement ablation.
    """
    p = config.pop_size
    # ``ceil``, not ``round``, to match the author's own ``math.ceil(eliten*Pmax)`` and
    # ``math.ceil(Mutrate*Pmax)`` (mp-BRKGA_DL01.py:137-138). At his published ``Pmax = 20N``
    # the two agree exactly (0.2*20N = 4N and 0.1*20N = 2N are integral), so this changes
    # nothing at the published configuration; it removes the divergence for any other pop_size.
    n_elite = max(1, ceil(config.elite_frac * p))
    n_mutant = max(1, ceil(config.mutant_frac * p))
    n_offspring = p - n_elite - n_mutant
    if n_offspring < 0:
        raise ValueError(
            f"pop_size {p} too small for elite+mutant ({n_elite}+{n_mutant}); "
            f"increase pop_size or reduce fractions."
        )

    rng = make_rng(config.seed)
    chrom_len = NUM_BLOCKS * instance.num_tasks
    omega = config.num_objectives
    pi = config.num_multi

    # Omega single-objective populations (index == the objective they specialise on) and
    # Pi multi-objective populations.
    omega_pops = [rng.random((p, chrom_len)) for _ in range(omega)]
    pi_pops = [rng.random((p, chrom_len)) for _ in range(pi)]

    archive_obj: list[Objectives] = []
    archive_chrom: list[np.ndarray] = []
    history: list[tuple[Objectives, ...]] = []
    snapshots: list[tuple[int, tuple[Objectives, ...], tuple[np.ndarray, ...]]] = []
    evaluations = 0

    for gen in range(config.generations + 1):
        omega_objs = [_evaluate_population(pop, instance) for pop in omega_pops]
        pi_objs = [_evaluate_population(pop, instance) for pop in pi_pops]
        evaluations += (omega + pi) * p

        # Global archive over every population this generation.
        for pop, objs in [*zip(omega_pops, omega_objs), *zip(pi_pops, pi_objs)]:
            f0 = fast_non_dominated_sort(objs)[0]
            archive_obj, archive_chrom = _update_archive(
                archive_obj, archive_chrom, [objs[i] for i in f0], [pop[i] for i in f0]
            )
        history.append(tuple(sorted(archive_obj)))
        if config.snapshot_every and (
            gen % config.snapshot_every == 0 or gen == config.generations
        ):
            order_s = sorted(range(len(archive_obj)), key=lambda i: archive_obj[i])
            snapshots.append((
                gen,
                tuple(archive_obj[i] for i in order_s),
                tuple(archive_chrom[i].copy() for i in order_s),
            ))

        if gen == config.generations:
            break

        # --- single-objective populations: elite = best Ne by their own objective ---
        omega_elite_idx: list[np.ndarray] = []
        omega_order: list[np.ndarray] = []  # full ranking, needed for the non-elite parent pool
        for o in range(omega):
            scores = np.asarray([obj[o] for obj in omega_objs[o]], dtype=float)
            order = np.argsort(scores, kind="stable")
            omega_order.append(order)
            omega_elite_idx.append(order[:n_elite])

        # Best-Ne (chrom, obj) blocks each Omega pop contributes to the migration pool.
        omega_pool_chrom = [omega_pops[o][omega_elite_idx[o]] for o in range(omega)]
        omega_pool_obj = [[omega_objs[o][i] for i in omega_elite_idx[o]] for o in range(omega)]

        # Own best-Ne of each Pi pop (needed for migration on exchange generations).
        pi_orders = [
            order_by_rank_crowding(pi_objs[pp], fast_non_dominated_sort(pi_objs[pp]))
            for pp in range(pi)
        ]
        pi_own_elite_chrom = [pi_pops[pp][pi_orders[pp][:n_elite]] for pp in range(pi)]
        pi_own_elite_obj = [[pi_objs[pp][i] for i in pi_orders[pp][:n_elite]] for pp in range(pi)]

        is_exchange = config.n_exchange > 0 and gen > 0 and gen % config.n_exchange == 0

        # --- evolve multi-objective populations with the migration pool ---
        new_pi_pops: list[np.ndarray] = []
        for pp in range(pi):
            pool_chrom: list[np.ndarray] = list(pi_own_elite_chrom[pp])
            pool_obj: list[Objectives] = list(pi_own_elite_obj[pp])
            for o in range(omega):  # boundary specialists always migrate in
                pool_chrom.extend(omega_pool_chrom[o])
                pool_obj.extend(omega_pool_obj[o])
            if is_exchange:  # every n_exchange gens, other multi-objective pops too
                for other in range(pi):
                    if other == pp:
                        continue
                    pool_chrom.extend(pi_own_elite_chrom[other])
                    pool_obj.extend(pi_own_elite_obj[other])

            pool_chrom, pool_obj = _dedup_pool(pool_chrom, pool_obj)
            pool_order = order_by_rank_crowding(pool_obj, fast_non_dominated_sort(pool_obj))
            chosen = pool_order[:n_elite]
            elite_block = np.stack([pool_chrom[i] for i in chosen])
            if elite_block.shape[0] < n_elite:  # pad from own elite if pool too small
                pad = pi_own_elite_chrom[pp][: n_elite - elite_block.shape[0]]
                elite_block = np.concatenate([elite_block, pad], axis=0)

            new_pi_pops.append(
                _breed(
                    rng, pi_pops[pp], elite_block,
                    n_elite, n_offspring, n_mutant, config.inherit_prob,
                    rank_order=np.asarray(pi_orders[pp]),
                    screen_fn=screen_fn, screening_factor=config.screening_factor,
                )
            )

        # --- evolve single-objective populations ---
        new_omega_pops = [
            _breed(
                rng, omega_pops[o], omega_pops[o][omega_elite_idx[o]],
                n_elite, n_offspring, n_mutant, config.inherit_prob,
                rank_order=omega_order[o],
                screen_fn=screen_fn, screening_factor=config.screening_factor,
            )
            for o in range(omega)
        ]

        omega_pops = new_omega_pops
        pi_pops = new_pi_pops

    order = sorted(range(len(archive_obj)), key=lambda i: archive_obj[i])
    return MpBRKGAResult(
        front=tuple(archive_obj[i] for i in order),
        chromosomes=tuple(archive_chrom[i].copy() for i in order),
        front_history=tuple(history),
        chrom_snapshots=tuple(snapshots),
        evaluations=evaluations,
    )
