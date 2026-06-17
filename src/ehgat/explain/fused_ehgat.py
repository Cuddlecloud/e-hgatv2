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
import torch.nn.functional as F
from torch import Tensor, nn
from torch_geometric.data import HeteroData

from ehgat.explain.event_dag import EventDag, assemble_event_dag, extract_precedence
from ehgat.explain.tropical_dp import tropical_longest_path
from ehgat.surrogate.ehgatv2 import EHGATv2
from ehgat.surrogate.graph import AGV_EDGE, NODE_TYPE, QC_EDGE

__all__ = ["FusedEHGATv2", "FusedPrediction"]


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

    @property
    def objectives(self) -> Tensor:
        """``[2]`` physical ``(C_max, E)`` vector for loss/metrics."""
        return torch.stack([self.makespan, self.energy])

    @property
    def legs(self) -> Tensor:
        """``[N, 4]`` predicted ``(empty_t, loaded_t, empty_e, loaded_e)`` for anchoring."""
        return torch.stack([self.empty_t, self.loaded_t, self.empty_e, self.loaded_e], dim=-1)


class FusedEHGATv2(nn.Module):
    """Wrap a trained :class:`EHGATv2` core with tropical-DP makespan + additive energy."""

    def __init__(self, core: EHGATv2) -> None:
        super().__init__()
        self.core = core
        hidden = core.config.hidden
        # Local physical attribute projections off the frozen structural embeddings.
        self.leg_head = nn.Linear(2 * hidden, 4)   # empty_t, loaded_t, empty_e, loaded_e
        self.delay_head = nn.Linear(hidden, 1)     # node delay d_v (anchored to tau)

    def freeze_core(self) -> None:
        """Lock the heterogeneous message-passing layers; train only the new heads."""
        for p in self.core.parameters():
            p.requires_grad_(False)
        self.core.eval()

    def head_parameters(self) -> list[nn.Parameter]:
        """Trainable projection-head parameters (the only ones the fine-tuner optimises)."""
        return list(self.leg_head.parameters()) + list(self.delay_head.parameters())

    def _local_attributes(self, data: HeteroData) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
        """Project node embeddings to non-negative ``(empty_t, loaded_t, empty_e, loaded_e, d)``."""
        h = self.core.encode(data)  # [N, hidden]
        agv_index = data[AGV_EDGE].edge_index
        # One AGV arc per task with dst = j; order by dst so row k <-> task k.
        order = torch.argsort(agv_index[1])
        src = agv_index[0][order]
        dst = agv_index[1][order]
        leg_in = torch.cat([h[src], h[dst]], dim=-1)            # [N, 2H]
        legs = F.softplus(self.leg_head(leg_in))                 # [N, 4] non-negative times/energies
        node_delay = F.softplus(self.delay_head(h)).squeeze(-1)  # [N]
        return legs[:, 0], legs[:, 1], legs[:, 2], legs[:, 3], node_delay

    def forward(self, data: HeteroData) -> FusedPrediction:
        """Predict one graph's ``(C_max, E)`` via tropical DP + additive energy.

        ``data`` must be a single :class:`HeteroData` (the tropical DP is assembled per
        graph). Batching is handled by iterating graphs in the trainer/explainer.
        """
        n = int(data[NODE_TYPE].x.shape[0])
        is_load = data[NODE_TYPE].x[:, 1] > 0.5
        agv_prev, qc_prev = extract_precedence(
            data[AGV_EDGE].edge_index, data[QC_EDGE].edge_index, n
        )
        empty_t, loaded_t, empty_e, loaded_e, node_delay = self._local_attributes(data)

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
        )
