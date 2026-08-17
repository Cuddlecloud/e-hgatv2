"""Aggregation of front-transfer shards into per-arm and per-instance summaries.

Each shard reports one (held-out instance, seed) replicate. Means are taken over
seeds within an instance and then over instances, so every instance carries equal
weight irrespective of how many front points its pool admits. Confidence
intervals are percentile bootstrap intervals over the seed replicates.
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np

__all__ = ["aggregate"]

ARMS = ("transfer", "random", "refit")
POOLS = ("near_front", "random_pool")


def _boot_ci(xs: list[float], reps: int = 10000, alpha: float = 0.05,
             seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap interval for the mean of ``xs``."""
    a = np.asarray([x for x in xs if np.isfinite(x)], dtype=float)
    if a.size < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = a[rng.integers(0, a.size, size=(reps, a.size))].mean(axis=1)
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))


def _paired_delta(a: list[float], b: list[float], reps: int = 10000,
                  seed: int = 0) -> dict:
    """Paired bootstrap on the seed-matched difference ``a - b``."""
    pa, pb = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(pa) & np.isfinite(pb)
    d = pa[m] - pb[m]
    if d.size < 2:
        return {"delta": float("nan"), "ci": [float("nan")] * 2, "n": int(d.size)}
    rng = np.random.default_rng(seed)
    means = d[rng.integers(0, d.size, size=(reps, d.size))].mean(axis=1)
    lo, hi = float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))
    return {"delta": float(d.mean()), "ci": [lo, hi], "n": int(d.size),
            "significant": bool(lo > 0 or hi < 0)}


def aggregate(shard_dir: Path) -> dict:
    """Pool shard JSONs into per-instance and overall summaries."""
    rows: list[dict] = []
    for f in sorted(glob.glob(str(shard_dir / "shard_*.json"))):
        d = json.loads(Path(f).read_text())
        seed = int(d["config"]["seed"])
        for arm in ARMS:
            if arm not in d.get("arms", {}):
                continue
            for spec, entry in d["arms"][arm]["per_instance"].items():
                for pool in POOLS:
                    s = entry.get(pool)
                    if not s:
                        continue
                    rows.append({
                        "arm": arm, "pool": pool, "instance": spec, "seed": seed,
                        "hv_ratio": s["hv_ratio"], "igd_plus": s["igd_plus"],
                        "n_pred": s["n_pred"], "n_true": s["n_true"],
                        "rho_pred": s["transport_share_pred"],
                        "rho_true": s["transport_share_true"],
                        "migr_pred": s["migration_pred"],
                        "migr_true": s["migration_true"],
                        "payoff": (entry.get("payoff") or {}).get(
                            "hv_ratio_guided_over_baseline", float("nan")),
                    })
        for spec, nv in (d.get("naive") or {}).items():
            for pool in POOLS:
                if pool in nv:
                    rows.append({"arm": "naive", "pool": pool, "instance": spec,
                                 "seed": seed, **nv[pool],
                                 "n_pred": 0, "n_true": 0,
                                 "rho_pred": float("nan"), "rho_true": float("nan"),
                                 "migr_pred": float("nan"), "migr_true": float("nan"),
                                 "payoff": float("nan")})

    out: dict = {"n_rows": len(rows), "by_arm": {}, "by_instance": {},
                 "contrasts": {}}
    insts = sorted({r["instance"] for r in rows})
    arms = ("naive",) + ARMS

    def pick(arm: str, pool: str, key: str, inst: str | None = None) -> list[float]:
        return [r[key] for r in rows
                if r["arm"] == arm and r["pool"] == pool
                and (inst is None or r["instance"] == inst)]

    for pool in POOLS:
        out["by_arm"][pool] = {}
        for arm in arms:
            # Instance-level means first, so no instance dominates by replicate count.
            per_inst = {i: float(np.nanmean(pick(arm, pool, "hv_ratio", i)))
                        for i in insts if pick(arm, pool, "hv_ratio", i)}
            if not per_inst:
                continue
            hv = list(per_inst.values())
            igd = [float(np.nanmean(pick(arm, pool, "igd_plus", i))) for i in insts
                   if pick(arm, pool, "igd_plus", i)]
            entry = {
                "hv_ratio_mean": float(np.nanmean(hv)),
                "hv_ratio_ci": list(_boot_ci(hv)),
                "igd_plus_mean": float(np.nanmean(igd)),
                "igd_plus_ci": list(_boot_ci(igd)),
                "n_instances": len(per_inst),
            }
            if arm != "naive":
                rp = pick(arm, pool, "rho_pred")
                rt = pick(arm, pool, "rho_true")
                mp = pick(arm, pool, "migr_pred")
                mt = pick(arm, pool, "migr_true")
                pay = pick(arm, pool, "payoff")
                entry |= {
                    "rho_pred_mean": float(np.nanmean(rp)),
                    "rho_true_mean": float(np.nanmean(rt)),
                    "rho_abs_err": float(np.nanmean(np.abs(np.asarray(rp) - np.asarray(rt)))),
                    "migr_pred_mean": float(np.nanmean(mp)),
                    "migr_true_mean": float(np.nanmean(mt)),
                    "migr_abs_err": float(np.nanmean(np.abs(np.asarray(mp) - np.asarray(mt)))),
                    "payoff_ratio_mean": float(np.nanmean(pay)),
                    "payoff_ratio_ci": list(_boot_ci(pay)),
                }
            out["by_arm"][pool][arm] = entry

    # Seed-matched contrasts on the discriminating pool.
    for pool in POOLS:
        cs = {}
        for a, b in (("transfer", "random"), ("transfer", "naive"),
                     ("refit", "transfer")):
            keyed = {}
            for arm in (a, b):
                keyed[arm] = {(r["instance"], r["seed"]): r["hv_ratio"]
                              for r in rows if r["arm"] == arm and r["pool"] == pool}
            common = sorted(set(keyed[a]) & set(keyed[b]))
            cs[f"{a}_minus_{b}_hv"] = _paired_delta(
                [keyed[a][k] for k in common], [keyed[b][k] for k in common])
        out["contrasts"][pool] = cs

    for i in insts:
        out["by_instance"][i] = {}
        for pool in POOLS:
            out["by_instance"][i][pool] = {
                arm: {
                    "hv_ratio": float(np.nanmean(pick(arm, pool, "hv_ratio", i))),
                    "igd_plus": float(np.nanmean(pick(arm, pool, "igd_plus", i))),
                    "n_seeds": len(pick(arm, pool, "hv_ratio", i)),
                }
                for arm in arms if pick(arm, pool, "hv_ratio", i)
            }
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dir", default="experiments/front_transfer")
    p.add_argument("--out", default="experiments/front_transfer/summary.json")
    args = p.parse_args()

    res = aggregate(Path(args.dir))
    Path(args.out).write_text(json.dumps(res, indent=2))

    for pool in POOLS:
        print(f"\n=== {pool} ===")
        print(f"{'arm':10s} {'HV ratio':>22s} {'IGD+':>20s} "
              f"{'rho err':>9s} {'migr err':>9s} {'payoff':>8s}")
        for arm, e in res["by_arm"].get(pool, {}).items():
            hv = f"{e['hv_ratio_mean']:.4f} [{e['hv_ratio_ci'][0]:.4f},{e['hv_ratio_ci'][1]:.4f}]"
            ig = f"{e['igd_plus_mean']:.3f} [{e['igd_plus_ci'][0]:.3f},{e['igd_plus_ci'][1]:.3f}]"
            rho = f"{e.get('rho_abs_err', float('nan')):.3f}"
            mig = f"{e.get('migr_abs_err', float('nan')):.3f}"
            pay = f"{e.get('payoff_ratio_mean', float('nan')):.4f}"
            print(f"{arm:10s} {hv:>22s} {ig:>20s} {rho:>9s} {mig:>9s} {pay:>8s}")
        print("  contrasts (paired, seed-matched):")
        for k, v in res["contrasts"].get(pool, {}).items():
            print(f"    {k:28s} {v['delta']:+.4f} "
                  f"[{v['ci'][0]:+.4f},{v['ci'][1]:+.4f}] n={v['n']} "
                  f"{'SIG' if v.get('significant') else 'ns'}")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
