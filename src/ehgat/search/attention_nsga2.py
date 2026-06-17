"""Attention-guided NSGA-II metaheuristic (Module 4).

This is the project's core contribution: an NSGA-II that replaces blind random mutation
with a **bottleneck-targeted** operator informed by the E-HGATv2 surrogate's edge
attention. Each candidate schedule is encoded as a typed graph (``surrogate/graph.py``);
the trained model's per-arc attention (``EHGATv2.attention``) exposes the **criticality
of every disjunctive AGV arc**. The arc with maximal attention is the learned bottleneck,
and mutation is focused on the task it delivers -- precisely the decision most likely to
shorten the max-plus critical path or trade makespan for energy.

Genetic structure (standard ``(mu + lambda)`` NSGA-II, Deb et al. 2002):

- **Representation**: a population of decoded :class:`~ehgat.environment.decoder.Schedule`
  objects (so the surrogate can score them directly).
- **Crossover** happens in the canonical *random-key* space: parents are re-encoded with
  ``encode_canonical``, recombined by biased uniform crossover, and ``decode``\\ d back --
  which is always acyclic by the SPV construction.
- **Attention-guided mutation** targets the bottleneck task with one of three operators:
    1. ``speed`` -- nudge the empty/loaded speed level (trades ``C_max`` against ``E``;
       no precedence change, always acyclic);
    2. ``reassign`` -- move the task to a different AGV and re-project the global order
       (acyclic by construction);
    3. ``swap`` -- a *direct* swap of the task with its AGV-sequence predecessor. This
       reorders one resource chain independently of the QC chains and **can introduce an
       AGV/QC deadlock**, so it is re-validated with Kahn's algorithm
       (``build_precedence`` -> :class:`ScheduleCycleError`) and rejected on a cycle.

Operator 3 is the reason the evaluator re-validates acyclicity at all; the no-deadlock
invariant (every schedule admitted to the population is acyclic) is property-tested.

The search keeps an external, deduplicated non-dominated **archive** and a per-generation
``front_history`` for the convergence (H1) study, and is fully deterministic from a
single seeded NumPy generator. The exact Oracle (``oracle.py``) upper-bounds quality.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from torch_geometric.data import Batch

from ehgat.benchmark.faithfulness import critical_path_binding
from ehgat.environment.decoder import NUM_BLOCKS, Schedule, decode, encode_canonical
from ehgat.environment.evaluator import ScheduleCycleError, build_precedence, evaluate
from ehgat.environment.instance import Instance
from ehgat.environment.physics import SpeedLevel
from ehgat.search.nsga2 import (
    crowding_distance,
    fast_non_dominated_sort,
    order_by_rank_crowding,
)
from ehgat.surrogate.ehgatv2 import EHGATv2
from ehgat.surrogate.graph import AGV_EDGE, QC_EDGE, build_hetero_graph
from ehgat.utils.seeding import make_rng

__all__ = [
    "AttentionNSGA2Config",
    "AttentionNSGA2Result",
    "attention_bottleneck_task",
    "attention_bottleneck_type",
    "attention_task_probabilities",
    "default_config",
    "mutate_reassign_agv",
    "mutate_speed",
    "mutate_swap_on_agv",
    "mutate_swap_on_qc",
    "operator_probabilities",
    "run_attention_nsga2",
]

Objectives = tuple[float, float]
_SPEED_LEVELS: tuple[SpeedLevel, ...] = tuple(SpeedLevel)
_ARCHIVE_ROUND = 6  # dedup objective-key precision (mirrors the BRKGA archive)
_MUTATION_OPS = ("speed", "reassign", "swap_agv", "swap_qc")
_SPEED_BASELINE = 0.5  # neutral operator score for `speed` (drives the C_max/E trade-off)
_OPERATOR_SOURCES = ("random", "attention", "oracle")
_AGGREGATION_WINDOWS = ("full", "front", "best")


@dataclass(frozen=True, slots=True)
class AttentionNSGA2Config:
    """Hyper-parameters for the attention-guided NSGA-II."""

    pop_size: int
    generations: int = 100
    crossover_prob: float = 0.9  # else a parent is cloned before mutation
    mutation_prob: float = 0.9  # prob. a child undergoes attention-guided mutation
    inherit_prob: float = 0.7  # biased uniform crossover bias toward parent A
    tournament_size: int = 2
    random_mutation: bool = False  # H2 ablation: select a random task instead of max-alpha
    mutation_temperature: float = 0.25  # softmax temperature for soft bottleneck sampling
    screening_factor: int = 1  # generate k*lambda offspring, surrogate-screen to lambda (1=off)
    operator_selection: str = "random"  # Channel-B AOS source: random | attention | oracle
    operator_temperature: float = 1.0  # softmax tau for operator probs (exploitation knob)
    aggregation_window: str = "front"  # bottleneck-type readout source: full | front | best
    seed: int = 0


@dataclass(frozen=True, slots=True)
class AttentionNSGA2Result:
    """Outcome of an attention-guided NSGA-II run."""

    front: tuple[Objectives, ...]  # non-dominated (makespan, energy), ascending
    schedules: tuple[Schedule, ...]  # schedule for each front point (aligned)
    front_history: tuple[tuple[Objectives, ...], ...]  # archive front per generation
    evaluations: int
    deadlocks_rejected: int  # swap mutations rejected by Kahn re-validation


def default_config(
    instance: Instance, *, generations: int = 100, seed: int = 0
) -> AttentionNSGA2Config:
    """Population ``P = 20N`` (matching the BRKGA baseline) for fair comparison."""
    return AttentionNSGA2Config(
        pop_size=20 * instance.num_tasks, generations=generations, seed=seed
    )


# --------------------------------------------------------------------------------------
# Attention bottleneck identification
# --------------------------------------------------------------------------------------
def attention_bottleneck_task(schedule: Schedule, instance: Instance, model: EHGATv2) -> int:
    """Return the task delivered by the **maximum-attention AGV arc** of ``schedule``.

    This is the surrogate's learned bottleneck: the disjunctive resource arc whose
    criticality (semantic attention weight) is highest. Ties are broken by the lowest
    arc index for determinism.
    """
    data = build_hetero_graph(schedule, instance)
    edge_index, alpha = model.attention(data)[AGV_EDGE[1]]
    if alpha.numel() == 0:
        return 0
    best = int(alpha.argmax().item())
    return int(edge_index[1, best].item())


def attention_task_probabilities(
    schedule: Schedule, instance: Instance, model: EHGATv2, *, temperature: float = 0.25
) -> np.ndarray:
    """Per-task mutation probabilities from the surrogate's AGV-arc attention.

    A temperature-scaled softmax over each task's incoming-arc attention. This is the
    **soft** alternative to :func:`attention_bottleneck_task`: high-attention tasks are
    favoured, but every task keeps a non-zero probability, preserving search diversity
    (a hard argmax concentrates ~all mutations on 1-2 tasks and collapses exploration).
    """
    n = instance.num_tasks
    data = build_hetero_graph(schedule, instance)
    edge_index, alpha = model.attention(data)[AGV_EDGE[1]]
    if alpha.numel() == 0:
        return np.full(n, 1.0 / n)
    scores = np.zeros(n)
    tasks = edge_index[1].numpy()
    scores[tasks] = alpha.numpy()
    logits = (scores - scores.max()) / max(temperature, 1e-6)
    probs = np.exp(logits)
    return np.asarray(probs / probs.sum())


def attention_bottleneck_type(
    schedule: Schedule, instance: Instance, model: EHGATv2
) -> tuple[np.ndarray, np.ndarray]:
    """Per-task semantic attention on the AGV vs QC relation: ``(w_agv, w_qc)``.

    The surrogate's HAN semantic weights classify, for each task, **which resource chain
    gates it** -- ``w_agv`` (AGV routing/sequencing) vs ``w_qc`` (QC serialisation). Because
    the weights are a per-task softmax over the two relations, ``w_agv[j] + w_qc[j] == 1``
    (a task with no incoming QC arc is pure AGV-bound, ``w_qc[j] == 0``). This is the
    **bottleneck-type** signal the Channel-B operator-selection controller consumes,
    distinct from the *which-task* signal of :func:`attention_task_probabilities`.
    """
    n = instance.num_tasks
    attn = model.attention(build_hetero_graph(schedule, instance))
    w_agv = np.zeros(n)
    agv_index, agv_alpha = attn[AGV_EDGE[1]]
    if agv_alpha.numel() > 0:
        w_agv[agv_index[1].cpu().numpy()] = agv_alpha.cpu().numpy()
    w_qc = np.zeros(n)
    qc_index, qc_alpha = attn[QC_EDGE[1]]
    if qc_alpha.numel() > 0:
        w_qc[qc_index[1].cpu().numpy()] = qc_alpha.cpu().numpy()
    return w_agv, w_qc


# --------------------------------------------------------------------------------------
# Mutation operators (each returns a new Schedule, or None if it deadlocks)
# --------------------------------------------------------------------------------------
def mutate_speed(schedule: Schedule, task: int, rng: np.random.Generator) -> Schedule:
    """Nudge the empty- or loaded-leg speed level of ``task`` to a different value.

    Pure cost/timing change with no precedence effect, so the result is always acyclic.
    Trades makespan against energy -- the second axis of the bottleneck decision.
    """
    leg = "empty" if rng.random() < 0.5 else "loaded"
    current = schedule.empty_speed[task] if leg == "empty" else schedule.loaded_speed[task]
    choices = [lvl for lvl in _SPEED_LEVELS if lvl != current]
    new_level = _SPEED_LEVELS[0] if not choices else choices[int(rng.integers(len(choices)))]
    if leg == "empty":
        speeds = list(schedule.empty_speed)
        speeds[task] = new_level
        return replace(schedule, empty_speed=tuple(speeds))
    speeds = list(schedule.loaded_speed)
    speeds[task] = new_level
    return replace(schedule, loaded_speed=tuple(speeds))


def mutate_reassign_agv(
    schedule: Schedule, instance: Instance, task: int, rng: np.random.Generator
) -> Schedule:
    """Reassign ``task`` to a different AGV, re-projecting the existing global order.

    Because both AGV and QC sequences remain projections of one shared total order
    (``global_order``), the schedule stays acyclic by construction.
    """
    if instance.num_agvs < 2:
        return schedule
    current = schedule.assignment[task]
    others = [a for a in range(instance.num_agvs) if a != current]
    new_agv = others[int(rng.integers(len(others)))]
    assignment = list(schedule.assignment)
    assignment[task] = new_agv
    agv_sequences = tuple(
        tuple(t for t in schedule.global_order if assignment[t] == a)
        for a in range(instance.num_agvs)
    )
    return replace(schedule, assignment=tuple(assignment), agv_sequences=agv_sequences)


def mutate_swap_on_agv(schedule: Schedule, instance: Instance, task: int) -> Schedule | None:
    """Swap ``task`` with its immediate predecessor on its AGV chain.

    This reorders a single AGV chain independently of the QC chains, so it **may create
    an AGV/QC deadlock**. The result is re-validated with Kahn's algorithm; on a cycle
    this returns ``None`` (the caller keeps the parent). On success the (now consistent)
    global order is refreshed from the Kahn topological order so the schedule round-trips
    through ``encode_canonical``/``decode``.
    """
    agv = schedule.assignment[task]
    seq = list(schedule.agv_sequences[agv])
    pos = seq.index(task)
    if pos == 0:
        return None  # no predecessor on this AGV to swap with
    seq[pos - 1], seq[pos] = seq[pos], seq[pos - 1]
    agv_sequences = list(schedule.agv_sequences)
    agv_sequences[agv] = tuple(seq)

    n = instance.num_tasks
    try:
        _, _, topo = build_precedence(tuple(agv_sequences), schedule.qc_sequences, n)
    except ScheduleCycleError:
        return None  # deadlock -> reject the mutation
    return replace(schedule, agv_sequences=tuple(agv_sequences), global_order=topo)


def mutate_swap_on_qc(schedule: Schedule, instance: Instance, task: int) -> Schedule | None:
    """Swap ``task`` with its immediate predecessor on its **QC** serialisation chain.

    The QC analogue of :func:`mutate_swap_on_agv`: it reorders a single QC chain
    independently of the AGV chains, so it **may create an AGV/QC deadlock** and is
    re-validated with Kahn's algorithm (returns ``None`` on a cycle, the parent is kept).
    This is the operator a **QC-bound** bottleneck needs -- AGV operators (`reassign`,
    `swap`) cannot relieve a serialisation gated by the crane chain. On success the global
    order is refreshed from the Kahn topological order so the schedule round-trips through
    ``encode_canonical``/``decode``.
    """
    qc_idx = instance.qcs.index(instance.tasks[task].qc)
    seq = list(schedule.qc_sequences[qc_idx])
    pos = seq.index(task)
    if pos == 0:
        return None  # no predecessor on this QC chain to swap with
    seq[pos - 1], seq[pos] = seq[pos], seq[pos - 1]
    qc_sequences = list(schedule.qc_sequences)
    qc_sequences[qc_idx] = tuple(seq)

    n = instance.num_tasks
    try:
        _, _, topo = build_precedence(schedule.agv_sequences, tuple(qc_sequences), n)
    except ScheduleCycleError:
        return None  # deadlock -> reject the mutation
    return replace(schedule, qc_sequences=tuple(qc_sequences), global_order=topo)


def _predict_objectives(
    schedules: list[Schedule], instance: Instance, model: EHGATv2
) -> list[Objectives]:
    """Batched surrogate prediction of (makespan, energy) for candidate schedules.

    Used by offspring **screening**: the surrogate's near-exact regression
    (not its attention) pre-filters a k-times larger candidate pool, so the
    expensive exact evaluations are spent only on predicted-dominant offspring.
    """
    graphs = [build_hetero_graph(s, instance) for s in schedules]
    batch = Batch.from_data_list(graphs)
    preds = model.predict(batch)
    return [(float(m), float(e)) for m, e in preds.tolist()]


# --------------------------------------------------------------------------------------
# Channel-B: XAI-driven adaptive operator selection (AOS)
# --------------------------------------------------------------------------------------
def operator_probabilities(agv_bias: float, temperature: float) -> np.ndarray:
    """Operator distribution over ``_MUTATION_OPS`` from an AGV-vs-QC bottleneck bias.

    ``agv_bias`` in ``[0, 1]`` is the share of the bottleneck attributable to the AGV
    resource (vs the QC chain). It biases the **operator** choice (Channel B): high ->
    favour the AGV-structural operators (``reassign``, ``swap_agv``); low -> favour
    ``swap_qc``. ``speed`` keeps a neutral baseline because it drives the makespan/energy
    trade-off regardless of which resource binds. ``temperature`` is the exploitation knob
    (low -> sharpen toward the bottleneck type; high -> toward a uniform, diversity-
    preserving distribution -- the limit recovers random AOS).
    """
    b = float(np.clip(agv_bias, 0.0, 1.0))
    scores = np.array([_SPEED_BASELINE, b, b, 1.0 - b])  # speed, reassign, swap_agv, swap_qc
    logits = (scores - scores.max()) / max(temperature, 1e-6)
    probs = np.exp(logits)
    return np.asarray(probs / probs.sum())


def _aggregation_window(
    population: list[Schedule], front0: list[int], objectives: list[Objectives], mode: str
) -> list[Schedule]:
    """Schedules whose bottleneck signal feeds the operator controller (Signal-to-Noise)."""
    if mode == "full":
        return population
    if mode == "front":
        return [population[i] for i in front0]
    if mode == "best":  # the front member with the smallest makespan (the C_max-critical one)
        best = min(front0, key=lambda i: objectives[i][0])
        return [population[best]]
    raise ValueError(f"unknown aggregation_window {mode!r}; use one of {_AGGREGATION_WINDOWS}")


def _agv_bias(
    schedules: list[Schedule],
    instance: Instance,
    model: EHGATv2,
    *,
    source: str,
    temperature: float,
) -> float:
    """Aggregate AGV-vs-QC bottleneck bias over ``schedules`` for the operator controller.

    ``attention`` uses the surrogate's semantic ``w_agv`` weighted by its which-task
    attention (the learned readout); ``oracle`` uses the exact Max-Plus critical-path
    binding fraction (the upper-bound signal). Returns a bias in ``[0, 1]``.
    """
    if not schedules:
        return 0.5
    if source == "attention":
        biases = []
        for s in schedules:
            w_agv, _ = attention_bottleneck_type(s, instance, model)
            p = attention_task_probabilities(s, instance, model, temperature=temperature)
            biases.append(float(np.dot(p, w_agv)))
        return float(np.mean(biases))
    if source == "oracle":
        biases = []
        for s in schedules:
            agv_bound, qc_bound = critical_path_binding(s, instance)
            total = len(agv_bound) + len(qc_bound)
            biases.append(len(agv_bound) / total if total else 0.5)
        return float(np.mean(biases))
    raise ValueError(f"unknown operator_selection {source!r}; use one of {_OPERATOR_SOURCES}")


def _operator_distribution(
    population: list[Schedule],
    front0: list[int],
    objectives: list[Objectives],
    instance: Instance,
    model: EHGATv2,
    config: AttentionNSGA2Config,
) -> np.ndarray | None:
    """Per-generation Channel-B operator distribution (``None`` => uniform/random AOS)."""
    if config.operator_selection == "random":
        return None
    window = _aggregation_window(population, front0, objectives, config.aggregation_window)
    bias = _agv_bias(
        window,
        instance,
        model,
        source=config.operator_selection,
        temperature=config.mutation_temperature,
    )
    return operator_probabilities(bias, config.operator_temperature)


def _mutate(
    schedule: Schedule,
    instance: Instance,
    model: EHGATv2,
    rng: np.random.Generator,
    *,
    guided: bool = True,
    temperature: float = 0.25,
    op_probs: np.ndarray | None = None,
) -> tuple[Schedule, bool]:
    """Apply one mutation operator. Returns ``(schedule, deadlock_rejected)``.

    ``guided`` controls **Channel A** (which task): the target is sampled from the
    surrogate's attention distribution, else uniformly at random (the H2 ablation).
    ``op_probs`` controls **Channel B** (which operator): ``None`` => uniform operator
    choice (random AOS); otherwise the operator is sampled from the bottleneck-type-biased
    distribution of :func:`operator_probabilities`.
    """
    if guided:
        probs = attention_task_probabilities(schedule, instance, model, temperature=temperature)
        task = int(rng.choice(instance.num_tasks, p=probs))
    else:
        task = int(rng.integers(instance.num_tasks))
    if op_probs is None:
        op = _MUTATION_OPS[int(rng.integers(len(_MUTATION_OPS)))]
    else:
        op = _MUTATION_OPS[int(rng.choice(len(_MUTATION_OPS), p=op_probs))]
    if op == "speed":
        return mutate_speed(schedule, task, rng), False
    if op == "reassign":
        return mutate_reassign_agv(schedule, instance, task, rng), False
    if op == "swap_agv":
        mutated = mutate_swap_on_agv(schedule, instance, task)
    else:  # swap_qc
        mutated = mutate_swap_on_qc(schedule, instance, task)
    if mutated is None:
        return schedule, True
    return mutated, False


# --------------------------------------------------------------------------------------
# Crossover (random-key space) and selection
# --------------------------------------------------------------------------------------
def _crossover(
    parent_a: Schedule,
    parent_b: Schedule,
    instance: Instance,
    rng: np.random.Generator,
    inherit_prob: float,
) -> Schedule:
    """Biased uniform crossover in random-key space; the decoded child is acyclic."""
    keys_a = encode_canonical(parent_a, instance)
    keys_b = encode_canonical(parent_b, instance)
    take_a = rng.random(NUM_BLOCKS * instance.num_tasks) < inherit_prob
    child_keys = np.where(take_a, keys_a, keys_b)
    return decode(child_keys, instance)


def _tournament(rank: list[int], crowding: list[float], rng: np.random.Generator, k: int) -> int:
    """Return the index winning a ``k``-way tournament (lower rank, then higher crowd)."""
    contenders = rng.integers(len(rank), size=k)
    best = int(contenders[0])
    for c in contenders[1:]:
        ci = int(c)
        if rank[ci] < rank[best] or (rank[ci] == rank[best] and crowding[ci] > crowding[best]):
            best = ci
    return best


def _rank_and_crowding(
    objectives: list[Objectives],
) -> tuple[list[list[int]], list[int], list[float]]:
    """Compute Pareto fronts plus per-individual rank and crowding distance."""
    fronts = fast_non_dominated_sort(objectives)
    n = len(objectives)
    rank = [0] * n
    crowd = [0.0] * n
    for r, front in enumerate(fronts):
        cd = crowding_distance(objectives, front)
        for i in front:
            rank[i] = r
            crowd[i] = cd[i]
    return fronts, rank, crowd


# --------------------------------------------------------------------------------------
# Archive
# --------------------------------------------------------------------------------------
def _update_archive(
    archive_obj: list[Objectives],
    archive_sched: list[Schedule],
    new_obj: list[Objectives],
    new_sched: list[Schedule],
) -> tuple[list[Objectives], list[Schedule]]:
    """Merge ``new`` into the archive, keeping a deduplicated non-dominated set."""
    seen: set[tuple[float, float]] = set()
    merged_obj: list[Objectives] = []
    merged_sched: list[Schedule] = []
    for obj, sched in zip(archive_obj + new_obj, archive_sched + new_sched, strict=True):
        key = (round(obj[0], _ARCHIVE_ROUND), round(obj[1], _ARCHIVE_ROUND))
        if key in seen:
            continue
        seen.add(key)
        merged_obj.append(obj)
        merged_sched.append(sched)
    keep = fast_non_dominated_sort(merged_obj)[0]
    return [merged_obj[i] for i in keep], [merged_sched[i] for i in keep]


# --------------------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------------------
def run_attention_nsga2(
    instance: Instance, model: EHGATv2, config: AttentionNSGA2Config
) -> AttentionNSGA2Result:
    """Run the attention-guided NSGA-II and return its non-dominated front."""
    if config.pop_size < 2:
        raise ValueError(f"pop_size must be >= 2, got {config.pop_size}")
    if config.operator_selection not in _OPERATOR_SOURCES:
        raise ValueError(
            f"operator_selection must be one of {_OPERATOR_SOURCES}, "
            f"got {config.operator_selection!r}"
        )
    if config.aggregation_window not in _AGGREGATION_WINDOWS:
        raise ValueError(
            f"aggregation_window must be one of {_AGGREGATION_WINDOWS}, "
            f"got {config.aggregation_window!r}"
        )
    model.eval()
    rng = make_rng(config.seed)
    chrom_len = NUM_BLOCKS * instance.num_tasks

    population = [decode(rng.random(chrom_len), instance) for _ in range(config.pop_size)]
    objectives = [evaluate(s, instance).objectives for s in population]
    evaluations = len(population)

    archive_obj: list[Objectives] = []
    archive_sched: list[Schedule] = []
    history: list[tuple[Objectives, ...]] = []
    deadlocks_rejected = 0

    for gen in range(config.generations + 1):
        fronts, rank, crowd = _rank_and_crowding(objectives)
        front0 = fronts[0]
        archive_obj, archive_sched = _update_archive(
            archive_obj,
            archive_sched,
            [objectives[i] for i in front0],
            [population[i] for i in front0],
        )
        history.append(tuple(sorted(archive_obj)))

        if gen == config.generations:
            break

        op_probs = _operator_distribution(population, front0, objectives, instance, model, config)

        # ---- create lambda offspring (optionally surrogate-screened from k*lambda) ----
        num_candidates = config.pop_size * max(1, config.screening_factor)
        candidates: list[Schedule] = []
        while len(candidates) < num_candidates:
            pa = population[_tournament(rank, crowd, rng, config.tournament_size)]
            if rng.random() < config.crossover_prob:
                pb = population[_tournament(rank, crowd, rng, config.tournament_size)]
                child = _crossover(pa, pb, instance, rng, config.inherit_prob)
            else:
                child = pa
            if rng.random() < config.mutation_prob:
                child, rejected = _mutate(
                    child,
                    instance,
                    model,
                    rng,
                    guided=not config.random_mutation,
                    temperature=config.mutation_temperature,
                    op_probs=op_probs,
                )
                deadlocks_rejected += int(rejected)
            candidates.append(child)
        if config.screening_factor > 1:
            predicted = _predict_objectives(candidates, instance, model)
            pred_fronts = fast_non_dominated_sort(predicted)
            keep = order_by_rank_crowding(predicted, pred_fronts)[: config.pop_size]
            offspring = [candidates[i] for i in keep]
        else:
            offspring = candidates
        off_obj = [evaluate(child, instance).objectives for child in offspring]
        evaluations += len(offspring)

        # ---- (mu + lambda) environmental selection ----
        combined = population + offspring
        combined_obj = objectives + off_obj
        sel_fronts = fast_non_dominated_sort(combined_obj)
        order = order_by_rank_crowding(combined_obj, sel_fronts)[: config.pop_size]
        population = [combined[i] for i in order]
        objectives = [combined_obj[i] for i in order]

    order = sorted(range(len(archive_obj)), key=lambda i: archive_obj[i])
    return AttentionNSGA2Result(
        front=tuple(archive_obj[i] for i in order),
        schedules=tuple(archive_sched[i] for i in order),
        front_history=tuple(history),
        evaluations=evaluations,
        deadlocks_rejected=deadlocks_rejected,
    )
