"""Physics-fused E-HGATv2: a tropical Max-Plus DP makespan head + exact additive energy.

The standard :class:`~ehgat.surrogate.ehgatv2.EHGATv2` pools node embeddings into a smooth
MLP that regresses ``(C_max, E)``. That MLP **smears** gradients across all features, so
input-attribution of ``C_max`` is not faithful to the schedule's true critical path.

:class:`FusedEHGATv2` keeps the frozen heterogeneous message-passing **core** but replaces
the makespan MLP with a *physics-anchored, natively differentiable* head:

1. **Tropical projection heads** map node embeddings to **local physical attributes**:
   - an **edge/leg head** ``FC(h_u || h_v) -> (empty_t, loaded_t, empty_e, loaded_e)`` per
     task (indexed by its single incoming AGV arc), and
   - a **node delay head** ``FC(h_v) -> d_v`` per task (the quay-crane handling ``tau``).
2. These local attributes are composed into ``C_max`` by the **exact** max-plus DP
   (:func:`~ehgat.explain.event_dag.assemble_event_dag` + tropical longest path), so
   ``dC_max/d(local attribute)`` is the *exact binary critical path* -- faithful by
   construction, with no Jacobian smearing.
3. **Energy is exact-additive**: ``E = sum_j (empty_e_j + loaded_e_j)`` over the predicted
   leg energies -- a strictly linear head, so ``dE/d(leg energy) = 1``.

**Identifiability.** Because the raw max-plus output only constrains the *active* critical
path, the local attributes are made identifiable by direct **physics anchoring**: training
(:mod:`ehgat.explain.train_fused`) supervises ``empty_t``/``loaded_t``/``empty_e``/
``loaded_e``/``d_v`` against their exact physical values, guaranteeing dense gradients on
every leg even when it is off the current critical path.

This is built **non-destructively** -- it wraps a trained core and the original scalar head
remains fully functional via ``core.forward`` / ``core.predict``.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch_geometric.data import HeteroData

from ehgat.environment.physics import SPEED_TABLE, SpeedLevel
from ehgat.explain.event_dag import (
    EventDag,
    assemble_coupled_event_dag,
    assemble_event_dag,
    extract_precedence,
)
from ehgat.explain.tropical_dp import tropical_longest_path
from ehgat.surrogate.ehgatv2 import EDGE_DIM, EHGATv2
from ehgat.surrogate.graph import AGV_EDGE, NODE_TYPE, QC_EDGE

__all__ = ["FusedEHGATv2", "FusedPrediction"]

_N_LEG_TIMES = 2  # (empty_t, loaded_t) -- the GNN-predicted transport overheads
_T_TRAVEL_COL = 0  # EDGE_FEATURES index of Travel_Time (= empty_t + loaded_t)
_E_EMPTY_COL = 1  # EDGE_FEATURES index of Empty_Energy
_E_LOADED_COL = 2  # EDGE_FEATURES index of Loaded_Energy

# Empty/loaded legs use *independent* speed levels, so the time split is not a smooth
# function of the arc features -- but it is exactly recoverable. Each leg's energy pins its
# level (``empty_t = empty_e / empty_power(level)``); the true (empty_level, loaded_level)
# pair is the one whose leg times sum to the arc's Travel_Time. We invert this exactly over
# the 3x3 discrete level grid; the selected branch stays differentiable w.r.t. the energies.
_EMPTY_POWERS = tuple(SPEED_TABLE[lvl].empty_power for lvl in SpeedLevel)   # (7.8, 10, 13.2)
_LOADED_POWERS = tuple(SPEED_TABLE[lvl].loaded_power for lvl in SpeedLevel)  # (11.7, 15, 19.8)


def _leg_time_prior(travel_time: Tensor, empty_e: Tensor, loaded_e: Tensor) -> tuple[Tensor, Tensor]:
    """Exact ``(empty_t, loaded_t)`` split via discrete inversion of the per-leg powers."""
    pe = travel_time.new_tensor(_EMPTY_POWERS)   # [3]
    pl = travel_time.new_tensor(_LOADED_POWERS)  # [3]
    empty_cand = empty_e[:, None] / pe[None, :]   # [N, 3] candidate empty times
    loaded_cand = loaded_e[:, None] / pl[None, :]  # [N, 3] candidate loaded times
    total = empty_cand[:, :, None] + loaded_cand[:, None, :]            # [N, 3, 3]
    n = travel_time.shape[0]
    flat = (total - travel_time[:, None, None]).abs().reshape(n, 9).argmin(dim=1)  # [N]
    ei, li = flat // 3, flat % 3
    empty_t = empty_cand.gather(1, ei[:, None]).squeeze(1)
    loaded_t = loaded_cand.gather(1, li[:, None]).squeeze(1)
    return empty_t, loaded_t


@dataclass(slots=True)
class FusedPrediction:
    """One graph's fused outputs and the differentiable local attributes behind them.

    The leg/delay tensors are retained as graph nodes so the explainer can read exact
    ``dC_max/d(leg)`` and ``dE/d(leg)`` after ``backward``.
    """

    makespan: Tensor          # scalar
    energy: Tensor            # scalar
    node_delay: Tensor        # [N]  predicted tau
    empty_t: Tensor           # [N]
    loaded_t: Tensor          # [N]
    empty_e: Tensor           # [N]
    loaded_e: Tensor          # [N]
    dag: EventDag             # assembled event DAG (edge_weights carry leg-time grads)
    wait_empty: Tensor        # [N]  predicted empty-leg power wait (0 when uncoupled)
    wait_loaded: Tensor       # [N]  predicted loaded-leg power wait (0 when uncoupled)

    @property
    def objectives(self) -> Tensor:
        """``[2]`` physical ``(C_max, E)`` vector for loss/metrics."""
        return torch.stack([self.makespan, self.energy])

    @property
    def leg_times(self) -> Tensor:
        """``[N, 2]`` GNN-predicted ``(empty_t, loaded_t)`` for time anchoring."""
        return torch.stack([self.empty_t, self.loaded_t], dim=-1)

    @property
    def leg_waits(self) -> Tensor:
        """``[N, 2]`` GNN-predicted ``(empty_wait, loaded_wait)`` for power-wait anchoring."""
        return torch.stack([self.wait_empty, self.wait_loaded], dim=-1)


class FusedEHGATv2(nn.Module):
    """Wrap a trained :class:`EHGATv2` core with tropical-DP makespan + additive energy.

    **Physics-anchored / residual heads.** The projection heads are fed not only the frozen
    structural embeddings but the **raw physical priors** that closed-form-determine the
    targets -- the AGV arc's ``(travel_time, empty_e, loaded_e)`` and the node's handling
    time -- standardised with the core's own buffers. They predict in *standardised* leg
    space and are de-normalised by registered ``leg_*`` / ``tau_*`` buffers (set from
    training stats by :func:`~ehgat.explain.train_fused.train_fused`), so the head only has
    to learn an ``O(1)`` residual rather than reach physical scale from a cold ``softplus``.
    This makes the otherwise non-injective max-plus map identifiable and dense-gradient.
    """

    leg_mean: Tensor
    leg_std: Tensor
    tau_mean: Tensor
    tau_std: Tensor
    wait_mean: Tensor
    wait_std: Tensor

    def __init__(
        self, core: EHGATv2, *, use_physics_prior: bool = False, coupled: bool = False
    ) -> None:
        super().__init__()
        self.core = core
        # When True the leg head learns a residual around the exact closed-form leg split
        # (faithful-by-construction *baseline*, but the GNN barely contributes). When False
        # (default) the GNN must predict the leg times itself from its embeddings + the
        # standardised arc priors -- the GNN does the real lifting; the max-plus layer still
        # guarantees faithful critical-path gradients regardless.
        self.use_physics_prior = use_physics_prior
        # Under peak-power coupling the GNN additionally predicts a per-leg *power wait*; the
        # leg's effective max-plus weight is ``leg_time + wait`` and the makespan is composed
        # over the precedence-only coupled activity DAG (no explicit resolution arcs needed --
        # the continuous waits reproduce the coupled critical path exactly when correct).
        self.coupled = coupled
        hidden = core.config.hidden
        # Heads see [h_src || h_dst || standardised arc priors] and [h || handling prior].
        # Only the *leg times* are learned; leg energies are read exactly from the inputs.
        self.leg_head = nn.Sequential(
            nn.Linear(2 * hidden + EDGE_DIM, hidden), nn.ReLU(), nn.Linear(hidden, _N_LEG_TIMES)
        )
        self.delay_head = nn.Sequential(
            nn.Linear(hidden + 1, hidden), nn.ReLU(), nn.Linear(hidden, 1)
        )
        # Power-wait head: a per-leg (empty, loaded) resource-contention delay. Same context
        # as the leg head; the wait is a global concurrency quantity the message passing must
        # infer from the schedule structure.
        self.wait_head = nn.Sequential(
            nn.Linear(2 * hidden + EDGE_DIM, hidden), nn.ReLU(), nn.Linear(hidden, _N_LEG_TIMES)
        )
        # De-normalisation of standardised head outputs into physical units.
        self.register_buffer("leg_mean", torch.zeros(_N_LEG_TIMES))
        self.register_buffer("leg_std", torch.ones(_N_LEG_TIMES))
        self.register_buffer("tau_mean", torch.zeros(1))
        self.register_buffer("tau_std", torch.ones(1))
        self.register_buffer("wait_mean", torch.zeros(_N_LEG_TIMES))
        self.register_buffer("wait_std", torch.ones(_N_LEG_TIMES))

    def set_leg_normalization(
        self,
        *,
        leg_mean: Tensor,
        leg_std: Tensor,
        tau_mean: Tensor,
        tau_std: Tensor,
        wait_mean: Tensor | None = None,
        wait_std: Tensor | None = None,
    ) -> None:
        """Populate leg/delay (and optional wait) de-normalisation buffers from train stats."""
        eps = 1e-6
        self.leg_mean.copy_(leg_mean)
        self.leg_std.copy_(leg_std.clamp_min(eps))
        self.tau_mean.copy_(tau_mean.reshape(1))
        self.tau_std.copy_(tau_std.reshape(1).clamp_min(eps))
        if wait_mean is not None and wait_std is not None:
            self.wait_mean.copy_(wait_mean)
            self.wait_std.copy_(wait_std.clamp_min(eps))

    def freeze_core(self) -> None:
        """Lock the heterogeneous message-passing layers; train only the new heads."""
        for p in self.core.parameters():
            p.requires_grad_(False)
        self.core.eval()

    def head_parameters(self) -> list[nn.Parameter]:
        """Trainable projection-head parameters (the only ones the fine-tuner optimises)."""
        params = list(self.leg_head.parameters()) + list(self.delay_head.parameters())
        if self.coupled:
            params += list(self.wait_head.parameters())
        return params

    def static_features(
        self, data: HeteroData, h: Tensor
    ) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
        """Embedding+prior features that DON'T depend on the heads (so they can be cached).

        Returns ``(leg_in, delay_in, empty_e, loaded_e, arc)`` with rows in task order
        (AGV arc per task, sorted by dst). ``leg_in`` feeds the leg/wait heads, ``delay_in``
        the tau head; ``empty_e``/``loaded_e`` are the exact arc leg energies.
        """
        x = data[NODE_TYPE].x
        agv_index = data[AGV_EDGE].edge_index
        agv_attr = data[AGV_EDGE].edge_attr
        agv_prior = (agv_attr - self.core.agv_mean) / self.core.agv_std
        hand_prior = (x[:, 0:1] - self.core.node_mean[0]) / self.core.node_std[0]

        order = torch.argsort(agv_index[1])  # row k <-> task k
        src = agv_index[0][order]
        dst = agv_index[1][order]
        arc = agv_attr[order]
        empty_e = arc[:, _E_EMPTY_COL]
        loaded_e = arc[:, _E_LOADED_COL]
        leg_in = torch.cat([h[src], h[dst], agv_prior[order]], dim=-1)  # [N, 2H + EDGE_DIM]
        delay_in = torch.cat([h, hand_prior], dim=-1)                   # [N, H + 1]
        return leg_in, delay_in, empty_e, loaded_e, arc

    @torch.no_grad()
    def encode_cached(self, data: HeteroData) -> Tensor:
        """Frozen-core node embeddings ``h`` ``[N, hidden]``, detached for reuse.

        The core is frozen, so ``h`` is identical across every fine-tuning epoch -- caching
        it once and passing it to ``forward(data, h=...)`` skips the GNN message passing (the
        single most expensive part of the per-graph step) on every subsequent epoch.
        """
        self.core.eval()
        return self.core.encode(data).detach()

    def _local_attributes(
        self, data: HeteroData, h: Tensor | None = None
    ) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
        """Project embeddings + physics priors to local physical attributes.

        Returns ``(empty_t, loaded_t, empty_e, loaded_e, d, wait_empty, wait_loaded)``.

        Leg *times* are GNN-predicted (anchored, de-normalised); leg *energies* are read
        **exactly** from the input AGV arc features (Empty_Energy / Loaded_Energy), so the
        energy objective is strictly exact and additive (``dE/d(leg energy) = 1``). The
        per-leg power *waits* are predicted only when ``self.coupled`` (else zero).

        ``h`` may be a precomputed (cached) frozen-core embedding; if ``None`` it is computed
        on the fly. Heads still backprop into their own parameters either way.
        """
        if h is None:
            h = self.core.encode(data)  # [N, hidden]
        leg_in, delay_in, empty_e, loaded_e, arc = self.static_features(data, h)
        if self.use_physics_prior:
            # Baseline: residual around the exact closed-form split (GNN barely contributes).
            handling = data[NODE_TYPE].x[:, 0]
            empty_prior, loaded_prior = _leg_time_prior(arc[:, _T_TRAVEL_COL], empty_e, loaded_e)
            resid = self.leg_head(leg_in) * self.leg_std
            empty_t = (empty_prior + resid[:, 0]).clamp_min(0.0)
            loaded_t = (loaded_prior + resid[:, 1]).clamp_min(0.0)
            node_delay = (handling + self.delay_head(delay_in).squeeze(-1) * self.tau_std).clamp_min(0.0)
        else:
            # GNN-does-the-work: predict the leg times / delay from embeddings (+ priors as
            # input features), de-normalised by the leg/tau buffers. The split is a learnable
            # function of (Travel_Time, energies); the GNN must infer it.
            times = (self.leg_head(leg_in) * self.leg_std + self.leg_mean).clamp_min(0.0)
            empty_t, loaded_t = times[:, 0], times[:, 1]
            node_delay = (
                self.delay_head(delay_in).squeeze(-1) * self.tau_std + self.tau_mean
            ).clamp_min(0.0)

        if self.coupled:
            waits = (self.wait_head(leg_in) * self.wait_std + self.wait_mean).clamp_min(0.0)
            wait_empty, wait_loaded = waits[:, 0], waits[:, 1]
        else:
            zeros = empty_t.new_zeros(empty_t.shape[0])
            wait_empty, wait_loaded = zeros, zeros
        return empty_t, loaded_t, empty_e, loaded_e, node_delay, wait_empty, wait_loaded

    def forward(self, data: HeteroData, h: Tensor | None = None) -> FusedPrediction:
        """Predict one graph's ``(C_max, E)`` via tropical DP + additive energy.

        ``data`` must be a single :class:`HeteroData` (the tropical DP is assembled per
        graph). Batching is handled by iterating graphs in the trainer/explainer. ``h`` is an
        optional cached frozen-core embedding (see :meth:`encode_cached`).
        """
        n = int(data[NODE_TYPE].x.shape[0])
        is_load = data[NODE_TYPE].x[:, 1] > 0.5
        agv_prev, qc_prev = extract_precedence(
            data[AGV_EDGE].edge_index, data[QC_EDGE].edge_index, n
        )
        (empty_t, loaded_t, empty_e, loaded_e, node_delay, wait_empty, wait_loaded) = (
            self._local_attributes(data, h=h)
        )

        if self.coupled:
            # Effective leg durations fold the predicted power wait into the travel time, so
            # the precedence-only coupled activity DAG reproduces the coupled makespan exactly
            # (no resolution arcs). Handling tau stays exact -- only AGV legs wait for power.
            empty_eff = empty_t + wait_empty
            loaded_eff = loaded_t + wait_loaded
            dag = assemble_coupled_event_dag(
                is_load, agv_prev, qc_prev, empty_eff, loaded_eff, node_delay, []
            )
        else:
            dag = assemble_event_dag(is_load, agv_prev, qc_prev, empty_t, loaded_t, node_delay)
        completion = tropical_longest_path(dag.node_weights, dag.edge_index, dag.edge_weights)
        makespan = completion[dag.completion_nodes].max()
        energy = (empty_e + loaded_e).sum()  # strictly additive -> exact, dE/d(leg_e) = 1
        return FusedPrediction(
            makespan=makespan,
            energy=energy,
            node_delay=node_delay,
            empty_t=empty_t,
            loaded_t=loaded_t,
            empty_e=empty_e,
            loaded_e=loaded_e,
            dag=dag,
            wait_empty=wait_empty,
            wait_loaded=wait_loaded,
        )
