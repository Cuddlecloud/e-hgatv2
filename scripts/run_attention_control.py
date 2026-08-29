"""Attention-faithfulness CONTROL harness — the stepping-stone probe for the TMLR fork.

Question this answers
---------------------
The scheduling paper's attention-unfaithfulness result is **confounded**: E-HGATv2's
attention is degenerate/thin by design (max-plus aggregation + a 2-way semantic gate), so
"attention is unfaithful" might just mean "this design sidelined attention." Before staking
September on the transformer/CRF fork — whose central bet is *"rich attention diverges from
an exact structured oracle"*. The cousin bet is tested cheaply **here**:

    Does a genuinely RICH attention model (global self-attention over all tasks) align with
    the exact critical path, or is it *also* unfaithful?

* Rich attention **also** unfaithful (≈ random baseline)  → the phenomenon is architecture
  -general, not a max-plus artifact → the fork's headline is likely to hold → **build it**.
* Rich attention **faithful** (well above baseline)        → attention *can* track the
  critical path when it is the main computation → the fork's bet is weaker / needs nuance →
  learned cheaply, before the sprint.

Method
------
For each instance the driver samples resolved schedules, labels them with the exact evaluator, trains
:class:`~ehgat.surrogate.attn_control.SelfAttnSurrogate` (Transformer over tasks) to predict
``(C_max, E)``, then score its readout attention against the exact critical-path oracle with
the **existing** :func:`~ehgat.benchmark.faithfulness.evaluate_faithfulness`. We also report
predictive accuracy (so an "unfaithful" verdict cannot be dismissed as an under-trained
model) and the random / critical-fraction baseline (the honest chance level).

Nothing here touches the OR/search pipeline or any banked result; it is purely additive.

Usage (smoke)::

    python scripts/run_attention_control.py --instances toy:10 --samples 400 --epochs 150

Usage (decision-grade, VM)::

    python scripts/run_attention_control.py --instances toy:10 toy:15 toy:20 \
        --samples 4000 --epochs 600 --seeds 5 --out experiments/attn_control/result.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from ehgat.benchmark.faithfulness import critical_agv_arcs, evaluate_faithfulness
from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.evaluator import ScheduleCycleError, evaluate
from ehgat.environment.instance import build_toy_instance
from ehgat.surrogate.attn_control import SelfAttnConfig, SelfAttnSurrogate, graph_to_tokens
from ehgat.surrogate.graph import build_hetero_graph


def _build_instance(spec: str):
    """`toy:N` → an N-task toy instance (uncoupled; peak_power left None)."""
    if spec.startswith("toy:"):
        return build_toy_instance(num_tasks=int(spec.split(":", 1)[1]))
    if spec == "toy":
        return build_toy_instance()
    raise ValueError(f"unsupported instance spec {spec!r} (use 'toy:N')")


def _sample(instance, n_samples: int, rng: np.random.Generator):
    """Sample valid resolved schedules + exact (C_max, E) labels."""
    n = instance.num_tasks
    scheds, targets = [], []
    attempts = 0
    while len(scheds) < n_samples and attempts < n_samples * 20:
        attempts += 1
        keys = rng.random(NUM_BLOCKS * n)
        try:
            sched = decode(keys, instance)
            ev = evaluate(sched, instance)
            build_hetero_graph(sched, instance)  # ensure no AGV/QC deadlock
        except ScheduleCycleError:
            continue
        scheds.append(sched)
        targets.append(ev.objectives)
    return scheds, np.asarray(targets, dtype=float)


def _to_tensors(scheds, instance):
    """Stack per-schedule token tensors (same N ⇒ stackable) + total-energy scalars."""
    toks, energies = [], []
    for s in scheds:
        data = build_hetero_graph(s, instance)
        tk, e = graph_to_tokens(data)
        toks.append(tk)
        energies.append(e)
    return torch.stack(toks), torch.stack(energies)  # [B, N, 7], [B, 1]


def _r2(pred: np.ndarray, true: np.ndarray) -> float:
    ss_res = float(((true - pred) ** 2).sum())
    ss_tot = float(((true - true.mean()) ** 2).sum())
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def _random_baseline_p1(scheds, instance, rng: np.random.Generator, draws: int = 200) -> float:
    """Empirical precision@1 of a uniformly-random attention (mean over draws & schedules)."""
    n = instance.num_tasks
    hits, total = 0, 0
    crit_sets = [critical_agv_arcs(s, instance) for s in scheds]
    for crit in crit_sets:
        if not crit:
            continue
        top = rng.integers(0, n, size=draws)
        hits += int(np.isin(top, list(crit)).sum())
        total += draws
    return hits / total if total else float("nan")


def _val_metrics(model, va_tok, va_e, va_y, va_s, instance):
    """``(r2_cmax, r2_energy, attn_p1, attn_spearman)`` for the current model state."""
    was_training = model.training
    model.eval()
    with torch.no_grad():
        out, _ = model.forward_tokens(va_tok, va_e)
        pred = (out * model.target_std + model.target_mean).cpu().numpy()
    r2_cmax = _r2(pred[:, 0], va_y[:, 0])
    r2_energy = _r2(pred[:, 1], va_y[:, 1])
    faith = evaluate_faithfulness(va_s, instance, model)
    if was_training:
        model.train()
    return r2_cmax, r2_energy, faith.precision_at_1, faith.spearman_rho


def _train_and_eval(spec: str, args, seed: int) -> dict:
    device = torch.device(
        args.device
        if args.device != "auto"
        else ("cuda" if torch.cuda.is_available() else "cpu")
    )
    instance = _build_instance(spec)
    n = instance.num_tasks
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)

    scheds, targets = _sample(instance, args.samples, rng)
    if len(scheds) < 20:
        raise RuntimeError(f"{spec}: only {len(scheds)} valid schedules sampled")
    n_val = max(10, int(len(scheds) * args.holdout))
    tr_s, va_s = scheds[:-n_val], scheds[-n_val:]
    tr_y, va_y = targets[:-n_val], targets[-n_val:]

    tr_tok, tr_e = _to_tensors(tr_s, instance)
    va_tok, va_e = _to_tensors(va_s, instance)
    tr_yt = torch.tensor(tr_y, dtype=torch.float32)

    model = SelfAttnSurrogate(
        SelfAttnConfig(hidden=args.hidden, layers=args.layers, heads=args.heads)
    ).to(device)
    tr_tok, tr_e, tr_yt = tr_tok.to(device), tr_e.to(device), tr_yt.to(device)
    va_tok, va_e = va_tok.to(device), va_e.to(device)

    flat = tr_tok.reshape(-1, tr_tok.shape[-1])
    model.set_normalization(
        input_mean=flat.mean(0),
        input_std=flat.std(0),
        energy_mean=tr_e.mean(0),
        energy_std=tr_e.std(0),
        target_mean=tr_yt.mean(0),
        target_std=tr_yt.std(0),
    )

    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    tgt_mean, tgt_std = model.target_mean, model.target_std
    n_tr = tr_tok.shape[0]

    # Baselines are model-independent — compute once.
    crit_frac = float(np.mean([len(critical_agv_arcs(s, instance)) / n for s in va_s]))
    rand_p1 = _random_baseline_p1(va_s, instance, rng)

    trajectory = []  # (epoch, loss, r2, faithfulness) — does attention track the oracle as R² rises?
    for epoch in range(1, args.epochs + 1):
        model.train()
        perm = torch.randperm(n_tr, device=device)
        epoch_loss = 0.0
        for i in range(0, n_tr, args.batch):
            idx = perm[i : i + args.batch]
            out, _ = model.forward_tokens(tr_tok[idx], tr_e[idx])
            y_std = (tr_yt[idx] - tgt_mean) / tgt_std
            loss = ((out - y_std) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss.detach()) * len(idx)
        if args.eval_every and epoch % args.eval_every == 0:
            r2c, r2e, p1, sp = _val_metrics(model, va_tok, va_e, va_y, va_s, instance)
            trajectory.append(
                {"epoch": epoch, "train_loss": epoch_loss / n_tr, "r2_cmax": r2c,
                 "r2_energy": r2e, "attn_p1": p1, "attn_spearman": sp}
            )
            print(
                f"    [{spec} s{seed}] ep{epoch} loss={epoch_loss / n_tr:.4f} "
                f"R²c={r2c:.3f} p@1={p1:.3f}(rand {rand_p1:.3f}) sp={sp:+.3f}",
                flush=True,
            )

    r2c, r2e, p1, sp = _val_metrics(model, va_tok, va_e, va_y, va_s, instance)
    return {
        "instance": spec,
        "N": n,
        "seed": seed,
        "device": str(device),
        "n_train": n_tr,
        "n_val": len(va_s),
        "pred_r2_cmax": r2c,
        "pred_r2_energy": r2e,
        "attn_precision_at_1": p1,
        "attn_spearman": sp,
        "baseline_random_p1": rand_p1,
        "baseline_critical_fraction": crit_frac,
        "trajectory": trajectory,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--instances", nargs="+", default=["toy:10"], help="e.g. toy:10 toy:15")
    p.add_argument("--samples", type=int, default=400)
    p.add_argument("--epochs", type=int, default=150)
    p.add_argument("--seeds", type=int, default=1, help="number of seeds per instance (0..S-1)")
    p.add_argument("--holdout", type=float, default=0.2)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--hidden", type=int, default=64)
    p.add_argument("--layers", type=int, default=3)
    p.add_argument("--heads", type=int, default=4)
    p.add_argument("--device", type=str, default="auto", help="auto|cpu|cuda")
    p.add_argument("--eval-every", type=int, default=0, help="record faithfulness-vs-R² every K epochs")
    p.add_argument("--out", type=str, default="")
    args = p.parse_args()

    def _save():
        if args.out:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps({"config": vars(args), "rows": rows}, indent=2))

    rows = []
    for spec in args.instances:
        for seed in range(args.seeds):
            row = _train_and_eval(spec, args, seed)
            rows.append(row)
            _save()  # incremental — ephemeral VM may die mid-run
            print(
                f"[{spec} seed={seed}] "
                f"pred R²(Cmax/E)={row['pred_r2_cmax']:.3f}/{row['pred_r2_energy']:.3f} | "
                f"attn p@1={row['attn_precision_at_1']:.3f} "
                f"spearman={row['attn_spearman']:+.3f} | "
                f"baseline p@1(rand/crit-frac)={row['baseline_random_p1']:.3f}/"
                f"{row['baseline_critical_fraction']:.3f}",
                flush=True,
            )

    print("\n=== VERDICT HINT ===")
    for spec in args.instances:
        srows = [r for r in rows if r["instance"] == spec]
        p1 = float(np.mean([r["attn_precision_at_1"] for r in srows]))
        sp = float(np.mean([r["attn_spearman"] for r in srows]))
        base = float(np.mean([r["baseline_random_p1"] for r in srows]))
        r2 = float(np.mean([r["pred_r2_cmax"] for r in srows]))
        delta = p1 - base
        tag = (
            "RICH ATTENTION ~ RANDOM → unfaithful (fork bet holds)"
            if delta < 0.08
            else "RICH ATTENTION > RANDOM → attention carries signal (fork bet weaker)"
        )
        note = "" if r2 > 0.5 else "  ⚠ LOW pred R² — undertrained; verdict unreliable"
        print(f"{spec}: attn p@1={p1:.3f} vs random {base:.3f} (Δ={delta:+.3f}); "
              f"spearman={sp:+.3f}; predR²={r2:.3f} → {tag}{note}")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({"config": vars(args), "rows": rows}, indent=2))
        print(f"\nsaved → {out_path}")


if __name__ == "__main__":
    main()
