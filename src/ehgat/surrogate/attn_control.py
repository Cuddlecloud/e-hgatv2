"""Rich self-attention surrogate — the **control** for the attention-faithfulness probe.

Why this model exists
---------------------
:class:`~ehgat.surrogate.ehgatv2.EHGATv2` cannot answer "is *rich* attention faithful to
the critical path?" for a structural reason: in a **resolved** schedule each task has at
most one AGV and one QC predecessor (see :func:`ehgat.surrogate.graph.build_hetero_graph`
— exactly one AGV arc per task), so any *neighbour* attention is a softmax over a single
edge and is therefore **degenerate (α ≡ 1)** regardless of the aggregation. The degeneracy
is a property of the resolved-schedule graph, not of ``aggr='max'``.

To get genuinely non-degenerate attention we must let a token attend over **all** tasks,
not just its resource-predecessor. This model is a **global self-attention (Transformer)
encoder over the task set** with a learned **readout query** whose attention distribution
over tasks is the *audited explanation*. That is:

* the closest possible analogue to the transformer/CRF **fork** (self-attention encoder),
  so a faithfulness result here de-risks that fork's central bet; and
* a **drop-in** for :mod:`ehgat.benchmark.faithfulness`: it implements ``.attention()`` and
  ``.predict()`` against the same :class:`HeteroData`, so ``evaluate_faithfulness`` runs on
  it unchanged. The per-task readout attention is mapped onto the one-AGV-arc-per-task
  convention the oracle uses.

Nothing in the OR / search pipeline imports this module; it is purely additive.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch_geometric.data import HeteroData

from ehgat.surrogate.graph import AGV_EDGE, NODE_TYPE, QC_EDGE, assert_graph_semantics
from ehgat.utils.assertions import EDGE_FEATURES, NODE_FEATURES

__all__ = ["AttentionMap", "SelfAttnConfig", "SelfAttnSurrogate", "graph_to_tokens"]

AttentionMap = dict[str, tuple[Tensor, Tensor]]

NODE_DIM = len(NODE_FEATURES)  # 4  (Handling_Time, Is_Load, Is_Unload, QC_ID)
EDGE_DIM = len(EDGE_FEATURES)  # 3  (Travel_Time, Empty_Energy, Loaded_Energy)
STRUCT_DIM = 3  # (AGV chain id, AGV chain depth, QC chain depth) — precedence position
TOKEN_DIM = NODE_DIM + EDGE_DIM + STRUCT_DIM  # 10 — features + arc + precedence structure


@dataclass(frozen=True)
class SelfAttnConfig:
    """Architecture hyper-parameters for the rich-attention control."""

    hidden: int = 64
    layers: int = 3
    heads: int = 4
    out_dim: int = 2  # (makespan, energy)
    dropout: float = 0.0
    ff_mult: int = 2

    def __post_init__(self) -> None:
        if self.hidden % self.heads != 0:
            raise ValueError(f"hidden ({self.hidden}) must be divisible by heads ({self.heads})")


def _chain_depths_roots(pred: list[int], n: int) -> tuple[list[int], list[int]]:
    """For a predecessor map (``pred[j] = -1`` if ``j`` is first on its resource), return
    per-task ``(depth, root)`` along the resource chain via memoised walk."""
    depth: list[int | None] = [None] * n
    root: list[int | None] = [None] * n

    def walk(j: int) -> tuple[int, int]:
        if depth[j] is not None:
            return depth[j], root[j]  # type: ignore[return-value]
        p = pred[j]
        if p < 0:
            depth[j], root[j] = 0, j
        else:
            dp, rp = walk(p)
            depth[j], root[j] = dp + 1, rp
        return depth[j], root[j]  # type: ignore[return-value]

    for j in range(n):
        walk(j)
    return [int(d) for d in depth], [int(r) for r in root]  # type: ignore[arg-type]


def _structural_features(data: HeteroData) -> Tensor:
    """``[N, 3]`` precedence-position features derived from the graph edges.

    ``(AGV chain id, AGV chain depth, QC chain depth)``, each normalised to ``[0, 1]``. This
    is the schedule's *ordering* — the analogue of positional encodings in the NLP fork — and
    is exactly what the longest-path (makespan) computation needs; without it a bag-of-tasks
    transformer cannot identify chain-mates or accumulate path times. Global attention stays
    fully rich; these features only tell each token *where* it sits in the precedence DAG.
    """
    x = data[NODE_TYPE].x
    n = x.shape[0]
    agv_index = data[AGV_EDGE].edge_index
    qc_index = data[QC_EDGE].edge_index

    agv_pred = [-1] * n  # self-arc (src==dst) marks the first task on an AGV → stays -1
    for s, d in zip(agv_index[0].tolist(), agv_index[1].tolist(), strict=True):
        if s != d:
            agv_pred[d] = s
    qc_pred = [-1] * n  # first task on a QC has no incoming QC arc → stays -1
    for s, d in zip(qc_index[0].tolist(), qc_index[1].tolist(), strict=True):
        qc_pred[d] = s

    agv_depth, agv_root = _chain_depths_roots(agv_pred, n)
    qc_depth, _ = _chain_depths_roots(qc_pred, n)
    denom = max(n - 1, 1)
    rows = [
        [agv_root[j] / denom, agv_depth[j] / denom, qc_depth[j] / denom] for j in range(n)
    ]
    return x.new_tensor(rows)


def graph_to_tokens(data: HeteroData) -> tuple[Tensor, Tensor]:
    """``HeteroData`` → ``(tokens [N, 10], total_energy [1])``.

    Each task becomes one token carrying its node features, the features of its single
    incoming AGV arc (which holds its travel/energy), and its **precedence-position**
    features (chain id + depths). ``total_energy`` is the schedule's additive AGV energy,
    fed to the readout so the additive objective is not lost by attention-weighted pooling.
    """
    x = data[NODE_TYPE].x  # [N, 4]
    agv_index = data[AGV_EDGE].edge_index  # [2, N] (one arc per task, dst = task id)
    agv_attr = data[AGV_EDGE].edge_attr  # [N, 3]
    n = x.shape[0]
    arc = x.new_zeros((n, EDGE_DIM))
    arc[agv_index[1]] = agv_attr  # scatter each arc onto its destination task
    struct = _structural_features(data)  # [N, 3]
    tokens = torch.cat([x, arc, struct], dim=-1)  # [N, 10]
    total_energy = (arc[:, 1] + arc[:, 2]).sum().reshape(1)  # empty + loaded energy
    return tokens, total_energy


class SelfAttnSurrogate(nn.Module):
    """Transformer encoder over tasks + readout-query attention; predicts ``(C_max, E)``.

    The audited attention is the **readout query's** softmax distribution over the tasks —
    a standard "attention as explanation" readout (cf. CLS→token attention), here genuinely
    non-degenerate because it ranges over all ``N`` tasks.
    """

    input_mean: Tensor
    input_std: Tensor
    energy_mean: Tensor
    energy_std: Tensor
    target_mean: Tensor
    target_std: Tensor

    def __init__(self, config: SelfAttnConfig | None = None) -> None:
        super().__init__()
        self.config = config or SelfAttnConfig()
        h = self.config.hidden
        self.token_encoder = nn.Linear(TOKEN_DIM, h)
        self.act = nn.ReLU()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=h,
            nhead=self.config.heads,
            dim_feedforward=self.config.ff_mult * h,
            dropout=self.config.dropout,
            batch_first=True,
            activation="relu",
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=self.config.layers)
        # Learned readout query; its attention over tokens is the audited explanation.
        self.readout_query = nn.Parameter(torch.empty(h))
        nn.init.normal_(self.readout_query, std=0.1)
        self.readout_attn = nn.MultiheadAttention(
            h, self.config.heads, dropout=self.config.dropout, batch_first=True
        )
        self.head = nn.Sequential(
            nn.Linear(h + 1, h),  # +1: standardised total energy (additive branch)
            nn.ReLU(),
            nn.Linear(h, self.config.out_dim),
        )

        self.register_buffer("input_mean", torch.zeros(TOKEN_DIM))
        self.register_buffer("input_std", torch.ones(TOKEN_DIM))
        self.register_buffer("energy_mean", torch.zeros(1))
        self.register_buffer("energy_std", torch.ones(1))
        self.register_buffer("target_mean", torch.zeros(self.config.out_dim))
        self.register_buffer("target_std", torch.ones(self.config.out_dim))

    def set_normalization(
        self,
        *,
        input_mean: Tensor,
        input_std: Tensor,
        energy_mean: Tensor,
        energy_std: Tensor,
        target_mean: Tensor,
        target_std: Tensor,
    ) -> None:
        """Populate standardisation buffers from training-set statistics."""
        eps = 1e-8
        self.input_mean.copy_(input_mean)
        self.input_std.copy_(input_std.clamp_min(eps))
        self.energy_mean.copy_(energy_mean)
        self.energy_std.copy_(energy_std.clamp_min(eps))
        self.target_mean.copy_(target_mean)
        self.target_std.copy_(target_std.clamp_min(eps))

    def forward_tokens(
        self, tokens: Tensor, total_energy: Tensor, *, return_attention: bool = False
    ) -> tuple[Tensor, Tensor | None]:
        """Core path. ``tokens [B, N, 7]``, ``total_energy [B, 1]`` → ``out [B, out_dim]``.

        Returns readout attention ``[B, N]`` (head-averaged) when ``return_attention``.
        """
        dev = self.input_mean.device  # allow CPU-built graphs to flow into a GPU model
        tokens = tokens.to(dev)
        total_energy = total_energy.to(dev)
        t = (tokens - self.input_mean) / self.input_std
        h = self.act(self.token_encoder(t))  # [B, N, H]
        h = self.encoder(h)  # [B, N, H] — rich token-token self-attention builds reps
        b = h.shape[0]
        q = self.readout_query.view(1, 1, -1).expand(b, 1, -1)  # [B, 1, H]
        pooled, attn_w = self.readout_attn(
            q, h, h, need_weights=return_attention, average_attn_weights=True
        )  # pooled [B, 1, H]; attn_w [B, 1, N] or None
        e = (total_energy - self.energy_mean) / self.energy_std  # [B, 1]
        out = self.head(torch.cat([pooled.squeeze(1), e], dim=-1))  # [B, out_dim]
        attn = attn_w.squeeze(1) if (return_attention and attn_w is not None) else None
        return out, attn

    def _attn_map(self, data: HeteroData, attn_vec: Tensor) -> AttentionMap:
        """Map per-task readout attention ``[N]`` onto the AGV/QC arc convention."""
        agv_index = data[AGV_EDGE].edge_index
        qc_index = data[QC_EDGE].edge_index
        attn_vec = attn_vec.to(agv_index.device)  # edge indices are CPU (harness-built)
        result: AttentionMap = {
            AGV_EDGE[1]: (agv_index.detach(), attn_vec[agv_index[1]].detach())
        }
        if qc_index.numel() > 0:
            result[QC_EDGE[1]] = (qc_index.detach(), attn_vec[qc_index[1]].detach())
        else:
            result[QC_EDGE[1]] = (
                torch.empty((2, 0), dtype=torch.long, device=attn_vec.device),
                torch.empty(0, device=attn_vec.device),
            )
        return result

    def forward(
        self, data: HeteroData, *, return_attention: bool = False
    ) -> tuple[Tensor, AttentionMap | None]:
        """Single-graph forward (the faithfulness harness path).

        Training uses :meth:`forward_tokens` directly with pre-stacked tensors; this adapter
        handles one :class:`HeteroData` at a time, which is all ``evaluate_faithfulness`` and
        ``predict`` ever pass.
        """
        assert_graph_semantics(data)
        batch = getattr(data[NODE_TYPE], "batch", None)
        if batch is not None and int(batch.max().item()) > 0:
            raise ValueError(
                "SelfAttnSurrogate.forward handles one graph at a time; "
                "use forward_tokens for batched training."
            )
        tokens, total_energy = graph_to_tokens(data)
        out, attn = self.forward_tokens(
            tokens.unsqueeze(0), total_energy.unsqueeze(0), return_attention=return_attention
        )
        attn_map = self._attn_map(data, attn.squeeze(0)) if attn is not None else None
        return out, attn_map

    @torch.no_grad()
    def predict(self, data: HeteroData) -> Tensor:
        """Physical ``[1, out_dim]`` ``(C_max, E)`` prediction (de-normalised)."""
        self.eval()
        out, _ = self.forward(data)
        return out * self.target_std + self.target_mean

    @torch.no_grad()
    def attention(self, data: HeteroData) -> AttentionMap:
        """Detached readout attention map for a single graph (drop-in for the harness)."""
        self.eval()
        _, attn = self.forward(data, return_attention=True)
        assert attn is not None  # return_attention=True always populates it
        return attn
