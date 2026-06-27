"""R4 (per-task target): does the predictor recover WHICH tasks are critical?

The aggregate transport/QC fraction is saturated on the real benchmark (model can't
beat a constant). The per-task criticality target is balanced (~0.53 critical) and
strongly front-position-dependent (every task is sometimes critical), so it is a fair
test of whether R4 amortizes anything non-trivial.

We build one row per (instance, front-position lambda, task):
    features = [lambda, instance-level structural feats, PER-TASK structural feats]
    label    = is this task on the critical path at this front position?
Labels come from the cached per_task_critical vectors (TAPE). Per-task features are
extracted deterministically from the instance (no NSGA-II/TAPE rerun needed).

Two models are compared under leave-one-real-out (LORO):
  - lambda-only baseline: instance+lambda features, NO per-task feats. Same prediction
    for every task at a given (instance, lambda) -> measures how much front position
    alone explains. Its job is to expose whether per-task structure adds anything.
  - full model: + per-task features.
If full AUC >> baseline AUC on held-out instances, per-task structure genuinely
predicts which tasks become critical -> R4 amortization works for this target.

Usage:
    python scripts/loro_pertask.py --instances L01 ... L35 \
        --cache-dir experiments/front_learning/cache --out .../loro_pertask.json
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from run_front_learning import _load_instance  # noqa: E402


def _pertask_features(spec: str) -> tuple[np.ndarray, np.ndarray]:
    """Return (instance_level[F_i], per_task[n_tasks, F_t]) feature blocks."""
    inst = _load_instance(spec, None)
    n = inst.num_tasks
    handling = np.array([t.handling_time for t in inst.tasks], dtype=float)
    mean_h = float(handling.mean())
    std_h = float(handling.std()) or 1.0
    # QC load: how many tasks share each task's crane.
    qc_count: dict = {}
    for t in inst.tasks:
        qc_count[t.qc] = qc_count.get(t.qc, 0) + 1
    qc_load = np.array([qc_count[t.qc] for t in inst.tasks], dtype=float)

    inst_level = np.array([float(n), float(inst.num_agvs), float(len(inst.qcs)), mean_h])
    per_task = np.stack([
        handling,                          # absolute handling time
        (handling - mean_h) / std_h,       # standardized handling time
        qc_load,                           # tasks sharing this crane
        qc_load / n,                       # crane load as fraction of all tasks
        np.arange(n) / max(n - 1, 1),      # normalized task index
    ], axis=1)
    return inst_level, per_task


def _build_rows(spec: str, cache_dir: Path):
    """Rows for one instance: (X_full, X_lambda_only, y), grouped per front point."""
    dps = json.loads((cache_dir / f"front_{spec.replace(':', '_').replace('/', '_')}.json").read_text())
    inst_level, per_task = _pertask_features(spec)
    n = per_task.shape[0]
    X_full, X_lam, y, groups = [], [], [], []
    for gi, dp in enumerate(dps):
        lam = dp["lam"]
        crit = dp["per_task_critical"]
        if len(crit) != n:
            continue
        for j in range(n):
            ctx = np.concatenate([[lam], inst_level])          # lambda + instance feats
            X_lam.append(ctx)
            X_full.append(np.concatenate([ctx, per_task[j]]))  # + per-task feats
            y.append(float(crit[j]))
            groups.append(gi)
    return (np.array(X_full), np.array(X_lam), np.array(y), np.array(groups))


def _train_eval(Xtr, ytr, Xte, yte):
    """Train a small MLP classifier; return held-out AUC + accuracy."""
    import torch
    import torch.nn as nn

    Xtr_t = torch.tensor(Xtr, dtype=torch.float32)
    ytr_t = torch.tensor(ytr, dtype=torch.float32).unsqueeze(1)
    mu = Xtr_t.mean(0)
    sd = Xtr_t.std(0).clamp(min=1e-6)
    Xtr_n = (Xtr_t - mu) / sd

    model = nn.Sequential(
        nn.Linear(Xtr.shape[1], 64), nn.ReLU(),
        nn.Linear(64, 64), nn.ReLU(),
        nn.Linear(64, 1),
    )
    # class balance
    pos = float(ytr.mean()) or 0.5
    pw = torch.tensor([(1 - pos) / pos])
    lossf = nn.BCEWithLogitsLoss(pos_weight=pw)
    opt = torch.optim.Adam(model.parameters(), lr=2e-3, weight_decay=1e-4)
    for _ in range(400):
        opt.zero_grad()
        loss = lossf(model(Xtr_n), ytr_t)
        loss.backward()
        opt.step()

    Xte_n = (torch.tensor(Xte, dtype=torch.float32) - mu) / sd
    with torch.no_grad():
        p = torch.sigmoid(model(Xte_n)).numpy().ravel()
    return _auc(yte, p), float(((p > 0.5) == (yte > 0.5)).mean())


def _auc(y, score):
    y = np.asarray(y)
    if y.min() == y.max():
        return float("nan")
    order = np.argsort(score)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(score) + 1)
    npos = float((y == 1).sum())
    nneg = float((y == 0).sum())
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", nargs="+", required=True)
    ap.add_argument("--cache-dir", default="experiments/front_learning/cache")
    ap.add_argument("--out", default="experiments/front_learning/loro_pertask.json")
    args = ap.parse_args()

    cdir = Path(args.cache_dir)
    data = {}
    for s in args.instances:
        cf = cdir / f"front_{s.replace(':', '_').replace('/', '_')}.json"
        if cf.exists():
            data[s] = _build_rows(s, cdir)
    print(f"Built per-task rows for {len(data)} instances "
          f"({sum(len(d[2]) for d in data.values())} total task-rows)")

    per = {}
    for held in sorted(data):
        Xf_te, Xl_te, y_te, _ = data[held]
        tr = [data[s] for s in data if s != held]
        Xf_tr = np.concatenate([t[0] for t in tr]); Xl_tr = np.concatenate([t[1] for t in tr])
        y_tr = np.concatenate([t[2] for t in tr])
        auc_full, acc_full = _train_eval(Xf_tr, y_tr, Xf_te, y_te)
        auc_base, acc_base = _train_eval(Xl_tr, y_tr, Xl_te, y_te)
        baserate = max(float(y_te.mean()), 1 - float(y_te.mean()))
        per[held] = {"auc_full": auc_full, "auc_lambda_only": auc_base,
                     "acc_full": acc_full, "acc_lambda_only": acc_base,
                     "base_rate_acc": baserate, "n_rows": int(len(y_te)),
                     "crit_frac": float(y_te.mean())}
        print(f"  [{held}] AUC full={auc_full:.3f} vs lam-only={auc_base:.3f} | "
              f"acc full={acc_full:.3f} vs base-rate={baserate:.3f}", flush=True)

    af = np.array([v["auc_full"] for v in per.values()])
    al = np.array([v["auc_lambda_only"] for v in per.values()])
    accf = np.array([v["acc_full"] for v in per.values()])
    accb = np.array([v["base_rate_acc"] for v in per.values()])
    agg = {
        "n": len(per),
        "auc_full_mean": float(np.nanmean(af)), "auc_full_median": float(np.nanmedian(af)),
        "auc_lambda_only_mean": float(np.nanmean(al)),
        "auc_full_minus_lambda_mean": float(np.nanmean(af - al)),
        "acc_full_mean": float(accf.mean()), "base_rate_acc_mean": float(accb.mean()),
        "frac_full_auc_above_0.7": float(np.mean(af >= 0.7)),
        "frac_full_beats_lambda": float(np.mean(af > al + 0.02)),
    }
    Path(args.out).write_text(json.dumps({"aggregate": agg, "per_instance": per}, indent=2))
    print("\n=== LORO per-task aggregate ===")
    print(f"  AUC full:        mean={agg['auc_full_mean']:.3f} median={agg['auc_full_median']:.3f}")
    print(f"  AUC lambda-only: mean={agg['auc_lambda_only_mean']:.3f}")
    print(f"  full - lambda:   mean={agg['auc_full_minus_lambda_mean']:+.3f} "
          f"(per-task structure adds this much AUC)")
    print(f"  acc full={agg['acc_full_mean']:.3f} vs base-rate={agg['base_rate_acc_mean']:.3f}")
    print(f"  frac AUC>=0.7: {agg['frac_full_auc_above_0.7']:.2f}  "
          f"frac beats lambda-only: {agg['frac_full_beats_lambda']:.2f}")
    print(f"\nSaved {args.out}")


if __name__ == "__main__":
    main()