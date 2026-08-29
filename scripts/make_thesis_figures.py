"""Generate the thesis data figures from the collected artifacts.

Two figures are produced, both directly from the experiment JSON so that a rerun cannot leave a
stale plot in the document:

``fig_migration.pdf``
    Migration against the fleet-to-crane ratio, one series per instance, with the significance of
    each cell marked. This is the central empirical result and the threshold structure is far
    easier to read as a curve than as the 54 rows of the corresponding table.

``fig_front.pdf``
    The two explained extremes of one front. The left panel places them on the objective plane;
    the right panel shows what the explanation actually says about each -- the critical path
    resolved into travel and handling, the two bars summing to the makespan by the decomposition
    identity. Only the boundary points of a front are retained in the artifact, so no curve
    between them is drawn: the figure claims exactly what was stored.

Sign convention throughout: migration is rho(makespan-optimal) - rho(energy-optimal), matching
``ehgat.explain.critical_share.migration``.

Writes into ``thesis/figs/``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path("thesis/figs")
STATS = Path("experiments/thesis/migration_stats.json")
SWEEP = Path("experiments/thesis/thesis_sweep540.json")
DL_FULL = Path("experiments/thesis/thesis_dl_scaled.json")

# Okabe-Ito, which is colour-blind safe, paired with distinct markers and dash patterns so the
# series remain separable when the document is printed in greyscale.
STYLES = [
    ("o", "-",                  "#0072B2"),
    ("s", (0, (5, 2)),          "#D55E00"),
    ("^", (0, (1, 1.6)),        "#009E73"),
    ("D", (0, (6, 2, 1, 2)),    "#CC79A7"),
    ("v", (0, (3, 1, 1, 1)),    "#56B4E9"),
    ("P", (0, (2, 2)),          "#E69F00"),
]

# Travel is the quantity under discussion, so it carries the saturated fill; handling is the
# remainder and is kept visually quiet.
C_TRAVEL, C_HANDLING = "#4C72B0", "#C7C7C7"

# House style follows the figures of the source work (Figs. 5, 8 and 9 of Fontes and
# Homayouni): a full box rule on all four sides, fine dotted gridlines on both axes, series
# separated by marker shape rather than by colour alone, and a framed legend inside the axes.
# Mathtext is set in Computer Modern so symbols in the figures match those in the body text.
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["CMU Serif", "Latin Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 9.5,
    "axes.titlesize": 9.5,
    "legend.fontsize": 7.6,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "axes.grid": True,
    "grid.color": "0.75",
    "grid.linestyle": ":",
    "grid.alpha": 0.9,
    "grid.linewidth": 0.5,
    "axes.axisbelow": True,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "black",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "legend.frameon": True,
    "legend.framealpha": 1.0,
    "legend.edgecolor": "0.4",
    "legend.fancybox": False,
    "legend.borderpad": 0.45,
})


def fig_migration() -> None:
    """All six instances on one axes, after the convention of the source work.

    The earlier form used six small multiples with the other five instances repeated in grey
    behind each. That separated the series but spent most of the panel area on repeated
    context, and it did not read as one figure. A single axes carries the six directly,
    distinguished by marker shape and dash pattern rather than by colour alone, so the shared
    threshold is read off one set of axes. The compression below $A/Q = 1$ is the result
    itself, migration being near zero there, and is therefore not a defect of the display.
    Dispersion moves to Table 4.4, which reports it numerically for every cell.
    """
    d = json.loads(STATS.read_text())
    items = list(d["instances"].items())

    fig, ax = plt.subplots(figsize=(6.3, 3.8))

    for i, (inst, cells) in enumerate(items):
        marker, dash, colour = STYLES[i % len(STYLES)]
        aq = [c["aq"] for c in cells]
        mean = [c["mean"] for c in cells]
        ax.plot(aq, mean, marker=marker, linestyle=dash, color=colour, label=inst,
                markersize=4.0, linewidth=1.1, markerfacecolor="white",
                markeredgewidth=1.0, zorder=4)

    # cells that fail Holm correction, marked once for the whole figure rather than per panel
    ns = [(c["aq"], c["mean"]) for _, cells in items for c in cells if not c["significant"]]
    if ns:
        ax.scatter(*zip(*ns), s=46, facecolors="none", edgecolors="black",
                   linewidths=0.9, zorder=6, label="not significant (Holm)")

    ax.axhline(0.0, color="black", linewidth=0.7, zorder=3)
    ax.axvline(1.0, color="black", linewidth=0.7, linestyle=(0, (4, 3)), zorder=3)
    ax.annotate(r"$A/Q = 1$", xy=(1.0, 0.16), xytext=(1.10, 0.155),
                fontsize=8, color="0.25")

    ax.set_xlabel(r"fleet-to-crane ratio $A/Q$")
    ax.set_ylabel(r"migration  $\rho_{\mathrm{mk}} - \rho_{\mathrm{en}}$")
    ax.set_xlim(0.0, 4.75)
    # The legend sits upper right, which is the only region no series enters: the saturated
    # tails of L07 and L21 occupy the lower right, and a legend placed there hid eight points
    # of the very effect the figure exists to show. Headroom is added rather than overlapping.
    ax.set_ylim(-0.78, 0.40)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
    ax.set_yticks([0.2, 0.0, -0.2, -0.4, -0.6])
    ax.legend(loc="upper right", ncol=3, handlelength=2.4, columnspacing=1.0,
              borderaxespad=0.5, handletextpad=0.5)

    fig.savefig(OUT / "fig_migration.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_migration.pdf'}")


def fig_front() -> None:
    """One front in the objective plane, every point carrying its own explanation.

    Panel (a) is drawn on the axes the source work uses for a Pareto front, makespan against
    energy, so that it is read the same way. The addition is that each point is shaded by its
    duration-weighted transport share, which turns a front into a statement about what binds
    where along it. An earlier version plotted the two extremes alone, the sweep artifact
    retaining only those; the front campaign records the share at every point, so the whole
    front is now shown.
    """
    from matplotlib import cm, colors as mcolors
    from matplotlib.lines import Line2D

    camp = _campaign("loading")
    cand = [r for r in camp if r["instance"] == "L_L21"
            and abs(r["agv_per_qc"] - 5 / 3) < 1e-2 and len(r["front"]) > 20]
    r = min(cand, key=lambda x: (abs(x["migration"] + 0.669), x["seed"]))
    pts = sorted(r["front"], key=lambda x: x["cmax"])

    xs = [q["cmax"] for q in pts]
    ys = [q["energy"] for q in pts]
    rhos = [q["rho"] for q in pts]
    mk_x, mk_y, rho_mk = xs[0], ys[0], rhos[0]
    en_x, en_y, rho_en = xs[-1], ys[-1], rhos[-1]

    # The colourbar is drawn from panel (a)'s space, so the inter-panel gap has to clear both
    # it and panel (b)'s y-axis label; at the previous 0.36 the two overprinted.
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(6.6, 2.9), gridspec_kw={"width_ratios": [1.25, 1.0], "wspace": 0.62})

    # ---- left: the whole front, each point shaded by what binds it -------------------------
    axL.plot(xs, ys, color="0.65", linewidth=0.8, linestyle=(0, (4, 2)), zorder=2)
    sc = axL.scatter(xs, ys, c=rhos, cmap="coolwarm", vmin=0.0, vmax=1.0, s=26,
                     edgecolors="black", linewidths=0.4, zorder=3)
    for x, y, rho, dy_off, va in ((mk_x, mk_y, rho_mk, 12, "bottom"),
                                  (en_x, en_y, rho_en, -18, "top")):
        axL.annotate(rf"$\rho = {rho:.3f}$", xy=(x, y), xytext=(0, dy_off),
                     textcoords="offset points", fontsize=7.8, ha="center", va=va)

    dx, dy = (en_x - mk_x), (mk_y - en_y)
    axL.set_xlim(mk_x - 0.20 * dx, en_x + 0.16 * dx)
    axL.set_ylim(en_y - 0.26 * dy, mk_y + 0.22 * dy)
    axL.set_xlabel(r"makespan $C_{\max}$ (s)")
    axL.set_ylabel(r"energy $E$ (kJ)")
    axL.set_title(f"(a) the front, {len(pts)} points", fontsize=8.5, pad=6)

    cb = fig.colorbar(sc, ax=axL, fraction=0.046, pad=0.03)
    cb.set_label(r"$\rho_{\mathrm{transport}}$", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    cb.outline.set_linewidth(0.6)

    # ---- right: the decomposition the explanation reports ------------------------------------
    labels = ["makespan-\noptimal", "energy-\noptimal"]
    cmax = [mk_x, en_x]
    travel = [rho_mk * mk_x, rho_en * en_x]
    handling = [c - t for c, t in zip(cmax, travel)]

    bars_t = axR.bar(labels, travel, width=0.52, color=C_TRAVEL, label="vehicle travel",
                     edgecolor="black", linewidth=0.5, zorder=3)
    axR.bar(labels, handling, width=0.52, bottom=travel, color=C_HANDLING,
            label="crane handling", edgecolor="black", linewidth=0.5, zorder=3)

    for bar, t, c in zip(bars_t, travel, cmax):
        axR.text(bar.get_x() + bar.get_width() / 2, t / 2, f"{t / c:.0%}",
                 ha="center", va="center", fontsize=8, color="white", fontweight="bold")
        axR.text(bar.get_x() + bar.get_width() / 2, c + 0.02 * max(cmax),
                 rf"$C_{{\max}}={c:.0f}$", ha="center", va="bottom", fontsize=7.5)

    axR.set_ylim(0, max(cmax) * 1.16)
    axR.set_ylabel("critical-path duration (s)")
    axR.set_title(r"(b) critical-path composition", fontsize=8.5, pad=6)
    axR.legend(frameon=False, loc="upper left", fontsize=7.5, borderaxespad=0.1,
               handletextpad=0.5, handlelength=1.4)
    axR.grid(axis="x", visible=False)

    fig.savefig(OUT / "fig_front.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_front.pdf'}  "
          f"[L21 seed {r['seed']}, A/Q={r['agv_per_qc']:.2f}, {len(pts)} front points, "
          f"migration {r['migration']:+.3f}]")


def fig_dl() -> None:
    """The published large set, which the document otherwise carries only as a table.

    Two questions are asked of it. Panel (a): is the transport share high at *both* ends, as
    the degenerate-regime argument claims? Panel (b): is the DL set anomalous, or does it simply
    sit at a fleet ratio below the threshold? The second panel puts it beside the small
    instances at the same ratio and at ratios above it, which is the comparison the text makes
    in words.
    """
    rows = json.loads(DL_FULL.read_text())
    rows = rows["per_seed"] if isinstance(rows, dict) and "per_seed" in rows else rows

    per = {}
    excluded = 0
    for r in rows:
        e = r["behaviour"]["exact"]
        if not e.get("decomposition_closes") or math.isnan(e["migration"]):
            excluded += 1
            continue
        per.setdefault(r["instance"], []).append(
            (e["rho_makespan_end"], e["rho_energy_end"], e["migration"], r["num_tasks"]))

    names = sorted(per, key=lambda k: per[k][0][3])          # order by instance size
    mk = [sum(x[0] for x in per[k]) / len(per[k]) for k in names]
    en = [sum(x[1] for x in per[k]) / len(per[k]) for k in names]
    dl_mig = [sum(x[2] for x in per[k]) / len(per[k]) for k in names]
    labels = [f"{k}  ($N{{=}}{per[k][0][3]}$)" for k in names]

    stats = json.loads(STATS.read_text())["instances"]
    l_lo = [c["mean"] for cs in stats.values() for c in cs if abs(c["aq"] - 0.5) < 1e-6]
    l_hi = [c["mean"] for cs in stats.values() for c in cs if c["aq"] >= 1.5]

    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(6.3, 3.2), gridspec_kw={"width_ratios": [1.25, 1.0], "wspace": 0.42})

    # ---- (a) both ends of every DL front, as a dumbbell ------------------------------------
    y = list(range(len(names)))
    for yi, a, b in zip(y, en, mk):
        axL.plot([a, b], [yi, yi], color="0.6", linewidth=1.4, zorder=1)
    axL.scatter(en, y, marker="s", s=34, facecolors="white", edgecolors="black",
                linewidths=1.1, zorder=3, label=r"energy-optimal end")
    axL.scatter(mk, y, marker="o", s=34, color=C_TRAVEL, zorder=3,
                label=r"makespan-optimal end")
    axL.set_yticks(y)
    axL.set_yticklabels(labels, fontsize=7.5)
    axL.invert_yaxis()
    axL.set_xlim(0.78, 1.02)
    axL.set_xlabel(r"transport share $\rho_{\mathrm{transport}}$")
    axL.set_title("(a) transport share at both extremes", fontsize=8.5, pad=6)
    axL.legend(frameon=False, fontsize=7.2, loc="lower left", handletextpad=0.4,
               borderaxespad=0.2)
    axL.grid(axis="y", visible=False)

    # ---- (b) is DL anomalous, or just below the threshold? ---------------------------------
    groups = [("DL set\n$A/Q=0.50$", dl_mig, C_TRAVEL),
              ("L set\n$A/Q=0.50$", l_lo, "0.45"),
              ("L set\n$A/Q\\geq1.5$", l_hi, "#D55E00")]
    rng = np.random.default_rng(0)
    for i, (lab, vals, colour) in enumerate(groups):
        jitter = rng.uniform(-0.13, 0.13, len(vals))
        axR.scatter(np.full(len(vals), i) + jitter, vals, s=17, color=colour,
                    alpha=0.75, linewidths=0, zorder=3)
        m = float(np.mean(vals))
        axR.hlines(m, i - 0.28, i + 0.28, color="black", linewidth=1.4, zorder=4)
        # above the group's own maximum, so the annotation never lands on a point
        axR.text(i, max(vals) + 0.055, f"{m:+.3f}", ha="center", fontsize=7.5)

    axR.axhline(0.0, color="black", linewidth=0.7, zorder=2)
    axR.set_xticks(range(len(groups)))
    axR.set_xticklabels([g[0] for g in groups], fontsize=7.5)
    axR.set_xlim(-0.55, len(groups) - 0.45)
    axR.set_ylim(-0.85, 0.30)
    axR.set_ylabel(r"migration  $\rho_{\mathrm{mk}} - \rho_{\mathrm{en}}$")
    axR.set_title("(b) migration by set and fleet ratio", fontsize=8.5, pad=6)
    axR.grid(axis="x", visible=False)

    fig.savefig(OUT / "fig_dl.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_dl.pdf'}  [{len(names)} instances, {excluded} replicate(s) excluded]")


CAMPAIGN = Path("experiments/front_campaign")


def _campaign(fam: str) -> list[dict]:
    return json.loads((CAMPAIGN / fam / "front_campaign.json").read_text())["per_seed"]


def fig_families() -> None:
    """The threshold, measured independently on all three instance families.

    Every earlier result rested on the loading family alone, in which every container is loaded
    and the unloading recurrence is never exercised. This figure repeats the measurement on the
    unloading family and on the mixed dual-cycling family built from it.
    """
    import statistics as st
    fams = [("loading", "#0072B2", "o", "-"),
            ("unloading", "#D55E00", "s", (0, (5, 2))),
            ("mixed", "#009E73", "^", (0, (1, 1.6)))]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for fam, colour, marker, dash in fams:
        by = {}
        for r in _campaign(fam):
            if "migration" in r:
                by.setdefault(round(r["agv_per_qc"], 2), []).append(r["migration"])
        xs = sorted(k for k, v in by.items() if len(v) >= 10)
        mu = [st.mean(by[x]) for x in xs]
        sd = [st.pstdev(by[x]) for x in xs]
        lo = [m - s for m, s in zip(mu, sd)]
        hi = [m + s for m, s in zip(mu, sd)]
        # Three families overlap across most of the range, so the bands are kept faint:
        # they indicate the spread across instances without competing with the means,
        # which are the quantity the figure is making a claim about.
        ax.fill_between(xs, lo, hi, color=colour, alpha=0.07, linewidth=0, zorder=2)
        ax.plot(xs, mu, marker=marker, linestyle=dash, color=colour, markersize=3.6,
                linewidth=1.3, label=f"{fam} ({sum(len(v) for v in by.values())} rep.)", zorder=4)
    ax.axhline(0.0, color="black", linewidth=0.7, zorder=3)
    ax.axvline(1.0, color="grey", linewidth=0.7, linestyle=":", zorder=3)
    ax.annotate(r"$A/Q = 1$", xy=(1.03, 0.12), fontsize=8, color="0.35")
    ax.set_xlim(0.1, 4.7)
    ax.set_xlabel(r"fleet-to-crane ratio $A/Q$")
    ax.set_ylabel(r"migration  $\rho_{\mathrm{mk}} - \rho_{\mathrm{en}}$")
    ax.legend(frameon=False, loc="lower left", fontsize=8)
    fig.savefig(OUT / "fig_families.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_families.pdf'}")


def fig_profile() -> None:
    """The explanation resolved along a whole front, rather than at its two extremes.

    One panel per family, each the front of a representative instance at a ratio above the
    threshold, with the transport share plotted at every point the decomposition closes on.
    """
    picks = [("loading", "#0072B2"), ("unloading", "#D55E00"), ("mixed", "#009E73")]
    fig, axes = plt.subplots(1, 3, figsize=(6.3, 2.5), sharey=True)
    fig.subplots_adjust(wspace=0.12)
    for ax, (fam, colour) in zip(axes, picks):
        # A front of moderate size with a wide share range reads best: the largest fronts
        # crowd hundreds of near-identical points into the high-makespan tail.
        cand = [r for r in _campaign(fam)
                if r["agv_per_qc"] >= 1.5 and 30 <= r["n_closed"] <= 70]
        rng_of = lambda r: max(p["rho"] for p in r["front"]) - min(p["rho"] for p in r["front"])
        r = max(cand, key=rng_of)
        cm = [p["cmax"] for p in r["front"]]
        rho = [p["rho"] for p in r["front"]]
        # Three encodings rather than one, because the raw sequence alone reads as noise and
        # the claim being made is about a trend and its departures, not about either separately.
        # (i) the crane-bound half of the panel is shaded, so the regime a point sits in is read
        # from position rather than from the reader tracking a dotted rule; (ii) the points are
        # joined faintly in front order, which is what makes the local non-monotonicity visible;
        # (iii) a centred rolling median over five neighbours carries the underlying rise, so
        # trend and departure are separable instead of superimposed.
        ax.axhspan(0.0, 0.5, color="0.90", zorder=0)
        ax.plot(cm, rho, color="0.72", linewidth=0.6, zorder=2)
        ax.scatter(cm, rho, s=9, color=colour, alpha=0.85, zorder=3,
                   edgecolors="none")
        k = 5
        med = [float(np.median(rho[max(0, i - k // 2):i + k // 2 + 1]))
               for i in range(len(rho))]
        ax.plot(cm, med, color=colour, linewidth=1.6, zorder=4)
        # the two extremes are the quantity Table 4.4 reports; mark them explicitly
        for idx, mk in ((0, "o"), (-1, "s")):
            ax.scatter([cm[idx]], [rho[idx]], s=42, marker=mk, facecolors="none",
                       edgecolors="black", linewidths=1.0, zorder=5)
        ax.axhline(0.5, color="black", linewidth=0.6, linestyle=":", zorder=1)
        ax.set_ylim(0, 1)
        ax.set_xlabel(r"$C_{\max}$ (s)")
        ax.set_title(f"{fam}\n{r['instance']}, $A/Q={r['agv_per_qc']:.2f}$, "
                     f"{r['n_closed']} pts", fontsize=7.5, pad=4)
        ax.tick_params(labelsize=7.5)
    axes[0].set_ylabel(r"$\rho_{\mathrm{transport}}$")
    # placed at the bottom of the first panel only, clear of the data in every panel
    # the dotted rule at 0.5 already separates the regimes; label it once, in the margin
    # right of centre: the makespan-optimal marker sits at the lower left of every panel
    axes[0].annotate("crane-bound", xy=(0.52, 0.06), xycoords="axes fraction",
                     fontsize=7, color="0.35")
    from matplotlib.lines import Line2D
    axes[2].legend(handles=[
        Line2D([], [], color="0.5", lw=1.6, label="rolling median (5)"),
        Line2D([], [], marker="o", color="none", markeredgecolor="black", label="makespan end"),
        Line2D([], [], marker="s", color="none", markeredgecolor="black", label="energy end")],
        loc="lower right", fontsize=6.2, borderaxespad=0.3, handlelength=1.6,
        labelspacing=0.3)
    fig.savefig(OUT / "fig_profile.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_profile.pdf'}")



EVOL = Path("experiments/thesis/search_evolution_surrogate.json")


def fig_evolution() -> None:
    """How the explanation moves while the search runs.

    The surrogate campaign records the two front ends and the model's agreement at each archive
    snapshot rather than every front point, so this reports what it measures: migration against
    generation, grouped by side of the fleet-to-crane threshold. An earlier version also drew the
    front at four generation budgets, after Figure 5 of the source work, but that panel needs the
    full front at each snapshot and is left out rather than drawn empty.
    """
    if not EVOL.exists():
        print("SKIPPED fig_evolution: no search_evolution_surrogate.json")
        return
    doc = json.loads(EVOL.read_text())
    rows = [{"agv_per_qc": c["agv_per_qc"], "snapshots": s["snapshots"]}
            for c in doc["per_cell"] for s in c["seeds"]]

    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    groups = {r"$A/Q < 1$ (below threshold)": [], r"$A/Q \geq 1$ (above threshold)": []}
    for r in rows:
        key = list(groups)[0] if r["agv_per_qc"] < 1.0 else list(groups)[1]
        for sn in r["snapshots"]:
            if sn.get("exact_migration") is not None:
                groups[key].append((sn["gen"], sn["exact_migration"]))
    for i, (label, pairs) in enumerate(groups.items()):
        by = {}
        for g, m in pairs:
            by.setdefault(g, []).append(m)
        xs = sorted(by)
        mean = [float(np.mean(by[g])) for g in xs]
        sd = [float(np.std(by[g])) for g in xs]
        marker, dash, colour = STYLES[i]
        ax.fill_between(xs, [m - t for m, t in zip(mean, sd)],
                        [m + t for m, t in zip(mean, sd)],
                        color=colour, alpha=0.12, linewidth=0)
        ax.plot(xs, mean, marker=marker, linestyle=dash, color=colour, markersize=4.2,
                linewidth=1.3, markerfacecolor="white", markeredgewidth=0.9, label=label)
    ax.axhline(0.0, color="black", linewidth=0.7)
    ax.set_xlabel("generation")
    ax.set_ylabel(r"migration  $\rho_{\mathrm{mk}} - \rho_{\mathrm{en}}$")
    ax.set_xlim(-3, 103)
    ax.legend(loc="lower right", fontsize=7.5, borderaxespad=0.5)
    fig.savefig(OUT / "fig_evolution.pdf")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_evolution.pdf'}  [{len(rows)} replicates, single panel]")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (fig_migration, fig_front, fig_dl, fig_families, fig_profile, fig_evolution):
        try:
            fn()
        except Exception as exc:
            print(f"SKIPPED {fn.__name__}: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
