"""R4 leave-one-real-out (LORO) generalization analysis.

Reuses the per-instance front-data caches written by run_front_learning.py stage 1.
For each held-out real instance, fits the front-behaviour predictor on ALL other
instances in the pool and reports held-out corr/MAE. Aggregates the distribution so
the R4 claim rests on real-to-real generalization, not a single held-out instance.

Usage:
    python scripts/loro_front_learning.py --instances L01 L02 ... L35 \
        --cache-dir experiments/front_learning/cache --out experiments/front_learning/loro.json
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

# Reuse the exact predictor + feature encoding from the main R4 script.
from run_front_learning import (  # noqa: E402
    _evaluate_predictor,
    _load_cached,
    _train_predictor,
)


def main() -> None:
    p = argparse.ArgumentParser(description="R4 leave-one-real-out generalization.")
    p.add_argument("--instances", nargs="+", required=True)
    p.add_argument("--cache-dir", default="experiments/front_learning/cache")
    p.add_argument("--out", default="experiments/front_learning/loro_results.json")
    p.add_argument("--min-points", type=int, default=5,
                   help="Skip held-out instances with fewer than this many front points.")
    args = p.parse_args()

    cache_dir = Path(args.cache_dir)
    pool = {spec: _load_cached(cache_dir, spec) for spec in args.instances}
    pool = {k: v for k, v in pool.items() if v}
    print(f"Loaded {len(pool)} instances, "
          f"{sum(len(v) for v in pool.values())} total front points")

    per_instance: dict[str, dict] = {}
    for held in sorted(pool):
        test_data = pool[held]
        if len(test_data) < args.min_points:
            print(f"  [{held}] skipped (n={len(test_data)} < {args.min_points})")
            continue
        train_data = [dp for spec, dps in pool.items() if spec != held for dp in dps]
        model, x_mean, x_std = _train_predictor(train_data)
        m = _evaluate_predictor(model, x_mean, x_std, test_data)
        per_instance[held] = m
        print(f"  [{held}] corr_t={m['corr_transport']:+.3f} corr_qc={m['corr_qc']:+.3f} "
              f"mae_t={m['mae_transport_frac']:.3f} mae_qc={m['mae_qc_frac']:.3f} "
              f"(n={m['n_test_points']})", flush=True)

    corr_t = np.array([m["corr_transport"] for m in per_instance.values()])
    corr_q = np.array([m["corr_qc"] for m in per_instance.values()])
    mae_t = np.array([m["mae_transport_frac"] for m in per_instance.values()])
    mae_q = np.array([m["mae_qc_frac"] for m in per_instance.values()])

    def _stats(a: np.ndarray) -> dict:
        return {"mean": float(a.mean()), "median": float(np.median(a)),
                "std": float(a.std()), "min": float(a.min()), "max": float(a.max())}

    agg = {
        "n_held_out": len(per_instance),
        "corr_transport": _stats(corr_t),
        "corr_qc": _stats(corr_q),
        "mae_transport_frac": _stats(mae_t),
        "mae_qc_frac": _stats(mae_q),
        "frac_corr_t_above_0.7": float(np.mean(corr_t >= 0.7)),
        "frac_corr_t_above_0.5": float(np.mean(corr_t >= 0.5)),
        "frac_corr_t_positive": float(np.mean(corr_t > 0)),
        "frac_mae_t_below_0.08": float(np.mean(mae_t <= 0.08)),
    }
    summary = {"aggregate": agg, "per_instance": per_instance}
    Path(args.out).write_text(json.dumps(summary, indent=2))

    print("\n=== LORO aggregate ===")
    print(f"  corr(transport): mean={agg['corr_transport']['mean']:+.3f} "
          f"median={agg['corr_transport']['median']:+.3f} "
          f"min={agg['corr_transport']['min']:+.3f} max={agg['corr_transport']['max']:+.3f}")
    print(f"  mae(transport):  mean={agg['mae_transport_frac']['mean']:.3f} "
          f"median={agg['mae_transport_frac']['median']:.3f}")
    print(f"  fraction corr>=0.7: {agg['frac_corr_t_above_0.7']:.2f}  "
          f"corr>=0.5: {agg['frac_corr_t_above_0.5']:.2f}  "
          f"corr>0: {agg['frac_corr_t_positive']:.2f}")
    print(f"  fraction mae<=0.08: {agg['frac_mae_t_below_0.08']:.2f}")
    print(f"\nSaved {args.out}")


if __name__ == "__main__":
    main()