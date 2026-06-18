"""Fine-tune the fused tropical head against the exact scheduling physics.

The frozen heterogeneous core is preserved; only the new projection heads
(:class:`~ehgat.explain.fused_ehgat.FusedEHGATv2.head_parameters`) are trained. The loss
**anchors the local physical attributes** (leg times/energies and node delay ``tau``) to
their exact simulator values *and* matches the composed objectives, which together make the
otherwise non-injective max-plus map identifiable and the gradients dense:

    L = ||leg_pred - leg_true||^2 + ||tau_pred - tau_true||^2
        + alpha ||C_max_pred - C_max_true||^2 + beta ||E_pred - E_true||^2

(each term standardised by its training std so the scales are balanced). A
``CosineAnnealingLR`` decays the LR from 1e-3 to 1e-5 over the schedule, and validation
``R^2`` for ``(C_max, E)`` is logged each epoch -- it should restore to ``>= 0.99`` once the
heads snap onto the physics layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch
from torch import Tensor

from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.evaluator import build_precedence, evaluate
from ehgat.environment.instance import Instance
from ehgat.environment.physics import leg_energy, travel_time
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.surrogate.ehgatv2 import EHGATv2, EHGATv2Config
from ehgat.surrogate.graph import build_hetero_graph
from ehgat.surrogate.train import TrainConfig, regression_metrics, train_surrogate
from ehgat.utils.seeding import make_rng, seed_everything

__all__ = ["FusedSample", "FusedTrainConfig", "FusedTrainResult", "build_samples", "train_fused"]


@dataclass(slots=True)
class FusedSample:
    """One labelled schedule for fused fine-tuning."""

    data: object          # HeteroData (raw graph)
    legs: Tensor          # [N, 4] exact (empty_t, loaded_t, empty_e, loaded_e)
    tau: Tensor           # [N] exact handling delay
    objectives: Tensor    # [2] exact (C_max, E)


@dataclass(frozen=True)
class FusedTrainConfig:
    """Hyper-parameters for the anchored fused fine-tune."""

    num_samples: int = 800
    epochs: int = 30
    batch_size: int = 32
    lr: float = 1e-3
    eta_min: float = 1e-5
    weight_decay: float = 0.0
    val_frac: float = 0.2
    alpha_makespan: float = 1.0
    beta_energy: float = 1.0
    use_physics_prior: bool = False  # False = GNN predicts legs; True = exact-prior baseline
    seed: int = 0


@dataclass
class FusedTrainResult:
    """Trained fused model, per-epoch history and held-out metrics."""

    model: FusedEHGATv2
    history: list[dict[str, float]] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)


def _exact_legs(schedule, instance: Instance) -> tuple[Tensor, Tensor]:
    """Exact ``[N, 4]`` leg attributes and ``[N]`` handling delays for ``schedule``."""
    n = instance.num_tasks
    agv_prev, _qc_prev, _ = build_precedence(schedule.agv_sequences, schedule.qc_sequences, n)
    legs: list[list[float]] = []
    for j, task in enumerate(instance.tasks):
        origin = instance.agv_start if agv_prev[j] < 0 else instance.tasks[agv_prev[j]].dropoff
        empty_d = instance.distance.distance(origin, task.pickup)
        loaded_d = instance.loaded_distance(task)
        legs.append(
            [
                travel_time(empty_d, schedule.empty_speed[j], loaded=False),
                travel_time(loaded_d, schedule.loaded_speed[j], loaded=True),
                leg_energy(empty_d, schedule.empty_speed[j], loaded=False),
                leg_energy(loaded_d, schedule.loaded_speed[j], loaded=True),
            ]
        )
    tau = torch.tensor([float(t.handling_time) for t in instance.tasks], dtype=torch.float32)
    return torch.tensor(legs, dtype=torch.float32), tau


def build_samples(instance: Instance, num_samples: int, *, seed: int = 0) -> list[FusedSample]:
    """Decode/evaluate random chromosomes into anchored fused-training samples."""
    if num_samples < 1:
        raise ValueError(f"num_samples must be >= 1, got {num_samples}")
    rng = make_rng(seed)
    n = instance.num_tasks
    samples: list[FusedSample] = []
    for _ in range(num_samples):
        keys = rng.random(NUM_BLOCKS * n)
        schedule = decode(keys, instance)
        evaluation = evaluate(schedule, instance)
        legs, tau = _exact_legs(schedule, instance)
        samples.append(
            FusedSample(
                data=build_hetero_graph(schedule, instance),
                legs=legs,
                tau=tau,
                objectives=torch.tensor(list(evaluation.objectives), dtype=torch.float32),
            )
        )
    return samples


def _scales(samples: list[FusedSample]) -> dict[str, Tensor]:
    """Per-quantity training std used to balance the anchoring/objective loss terms."""
    eps = 1e-6
    legs = torch.cat([s.legs[:, :2] for s in samples], dim=0)     # [sum N, 2] times only
    tau = torch.cat([s.tau for s in samples], dim=0)              # [sum N]
    objs = torch.stack([s.objectives for s in samples], dim=0)    # [S, 2]
    return {
        "leg": legs.std(dim=0).clamp_min(eps),
        "tau": tau.std().clamp_min(eps),
        "makespan": objs[:, 0].std().clamp_min(eps),
        "energy": objs[:, 1].std().clamp_min(eps),
    }


@torch.no_grad()
def _evaluate(model: FusedEHGATv2, samples: list[FusedSample]) -> dict[str, float]:
    model.eval()
    preds, trues = [], []
    for s in samples:
        out = model(s.data)
        preds.append(out.objectives.detach())
        trues.append(s.objectives)
    pred = torch.stack(preds, dim=0)
    true = torch.stack(trues, dim=0)
    return regression_metrics(pred, true)


def build_core(instance: Instance, *, seed: int = 0, num_samples: int = 1500, epochs: int = 60) -> EHGATv2:
    """Train a base E-HGATv2 surrogate to supply the frozen embedding core."""
    result = train_surrogate(
        instance, TrainConfig(num_samples=num_samples, epochs=epochs, seed=seed)
    )
    return result.model


def train_fused(
    instance: Instance,
    core: EHGATv2 | None = None,
    config: FusedTrainConfig | None = None,
) -> FusedTrainResult:
    """Fit the anchored fused head on a frozen core; return model + R^2 history.

    If ``core`` is ``None`` a base surrogate is trained first (:func:`build_core`).
    """
    config = config or FusedTrainConfig()
    seed_everything(config.seed)
    if core is None:
        core = build_core(instance, seed=config.seed)

    model = FusedEHGATv2(core, use_physics_prior=config.use_physics_prior)
    model.freeze_core()

    samples = build_samples(instance, config.num_samples, seed=config.seed)
    rng = make_rng(config.seed)
    order = rng.permutation(len(samples)).tolist()
    samples = [samples[i] for i in order]
    n_val = round(config.val_frac * len(samples))
    val_samples = samples[:n_val]
    train_samples = samples[n_val:]
    scales = _scales(train_samples)

    # De-normalisation buffers so the heads predict O(1) residuals (stable, fast to fit).
    train_times = torch.cat([s.legs[:, :2] for s in train_samples], dim=0)
    train_tau = torch.cat([s.tau for s in train_samples], dim=0)
    model.set_leg_normalization(
        leg_mean=train_times.mean(dim=0),
        leg_std=train_times.std(dim=0),
        tau_mean=train_tau.mean(),
        tau_std=train_tau.std(),
    )

    optimizer = torch.optim.Adam(
        model.head_parameters(), lr=config.lr, weight_decay=config.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config.epochs, eta_min=config.eta_min
    )

    result = FusedTrainResult(model=model)
    gen = torch.Generator().manual_seed(config.seed)
    for epoch in range(config.epochs):
        model.train()
        model.core.eval()  # keep frozen core's normalisation/dropout in eval mode
        perm = torch.randperm(len(train_samples), generator=gen).tolist()
        epoch_loss = 0.0
        for start in range(0, len(perm), config.batch_size):
            chunk = perm[start : start + config.batch_size]
            optimizer.zero_grad()
            batch_loss = torch.zeros((), dtype=torch.float32)
            for idx in chunk:
                s = train_samples[idx]
                out = model(s.data)
                leg_term = (((out.leg_times - s.legs[:, :2]) / scales["leg"]) ** 2).mean()
                tau_term = (((out.node_delay - s.tau) / scales["tau"]) ** 2).mean()
                cmax_term = ((out.makespan - s.objectives[0]) / scales["makespan"]) ** 2
                e_term = ((out.energy - s.objectives[1]) / scales["energy"]) ** 2
                batch_loss = batch_loss + (
                    leg_term + tau_term + config.alpha_makespan * cmax_term + config.beta_energy * e_term
                )
            batch_loss = batch_loss / max(len(chunk), 1)
            batch_loss.backward()
            optimizer.step()
            epoch_loss += float(batch_loss) * len(chunk)
        scheduler.step()

        record = {
            "epoch": float(epoch),
            "train_loss": epoch_loss / max(len(train_samples), 1),
            "lr": float(scheduler.get_last_lr()[0]),
        }
        if val_samples:
            val_metrics = _evaluate(model, val_samples)
            record["r2_makespan"] = val_metrics["r2_makespan"]
            record["r2_energy"] = val_metrics["r2_energy"]
            record["mae_overall"] = val_metrics["mae_overall"]
        result.history.append(record)

    result.metrics = _evaluate(model, val_samples or train_samples)
    return result
