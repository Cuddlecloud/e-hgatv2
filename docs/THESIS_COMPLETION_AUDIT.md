# Thesis completion audit

Claim-by-claim map of what the thesis asserts against the evidence on disk, and a decision on
whether further VM campaigns are required. Generated 2026-08-28 against `thesis/main.tex`
and `experiments/`.

## 1. Evidence inventory

| dataset | records | coverage | used by the thesis |
|---|---|---|---|
| `pareto_explanation/exact_explanation_L.json` | 35 | L set, 1 seed | yes (Table 3) |
| `pareto_explanation/dl_parts/*/…DL.json` | 10 | DL set, 1 seed | yes (Table 4) |
| `thesis/migration_stats.json` | 54 cells | 6 instances x 9 ratios | yes (Table 5, Fig 7) |
| `thesis/thesis_DL_full.json` | 100 | DL set, 10 seeds, A/Q=0.50 | yes (Fig 6) |
| `thesis/thesis_L_full.json` | 350 | **all 35 L instances**, 10 seeds, A/Q 0.33–1.0 | **no** |
| `thesis/published_validation.json` | 35 x 4 | published optima comparison | numbers hand-carried into prose |
| `thesis/thesis_fleet_sweep.json` | 140 | 4 instances, superseded by the 540 sweep | no |
| `thesis/thesis_probe.json`, `*_smoke_*.json` | 11 | smoke tests | no |

## 2. Claim-to-evidence map

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | The evaluator agrees with the source objective | 2400 schedules, 8 instances, zero difference | complete |
| C2 | Computed makespans lie at or below published fixed-speed optima | 35 instances, 4 scenario columns | complete; not wired into the generated tables |
| C3 | The decomposition identity closes | asserted per traversal; 9 of 990 fail, all disclosed | complete |
| C4 | Migration is negligible on the published large set | Table 4 (1 seed) and Figure 6 (10 seeds) | complete; the two sources use different seed counts |
| C5 | Migration depends on A/Q with a threshold near unity | 540 replicates, Wilcoxon with Holm correction | complete for the small-instance geometry |
| C6 | That threshold applies to the DL geometry | none; inferred from C5 | **gap** |
| C7 | The surrogate reproduces the exact explanation | 540 paired comparisons, mean abs error 0.034 | complete |

## 3. Does the work require further VM runs?

**No, for the claims the thesis currently makes.** C1–C5 and C7 rest on collected and
statistically tested data. C6 is the only unsupported claim, and it is an extrapolation across
terminal geometries rather than a measurement.

Three improvements require no compute at all:

1. **Report `thesis_L_full.json`.** It carries 344 usable replicates across all 35 published
   small instances at their native fleet ratios, and shows the proportion of replicates with
   migration exceeding 0.1 rising from 0% at A/Q = 0.33 to 61% at A/Q = 1.0. This corroborates
   the ratio dependence of C5 on 35 instances rather than 6, from runs the 540-replicate sweep
   did not use.
2. **Repoint Table 4 at the ten-seed DL campaign.** Table 5 reports ten-seed means; Table 4
   reports single runs. The headline moves from +0.043 to +0.064, and the qualitative claim is
   unchanged.
3. **Wire `published_validation.json` into the table pipeline**, so the verification figures in
   Section 4.2 are generated rather than transcribed.

## 4. If C6 is to be closed by measurement

Median cost is 1726 s per DL replicate against 65 s per small-instance replicate.

| option | replicates | core-hours | wall clock at 12 workers | closes |
|---|---|---|---|---|
| full DL sweep, 10 instances x 9 ratios x 10 seeds | 900 | 432 | 36 h | C6 completely |
| targeted probe, 3 instances x 3 ratios x 10 seeds | 90 | 43 | 3.5 h | C6 for three instances |
| declare as a limitation | 0 | 0 | 0 | nothing, but removes the overreach |

The targeted probe is the only option with a favourable ratio of evidential value to cost. The
full sweep multiplies the compute tenfold to add instances that are expected to behave alike.

## 5. Recommended order of work

1. Items 1–3 of Section 3. No compute.
2. State the C6 limitation explicitly in Section 5.
3. Run the targeted probe only if the examiner requires the threshold to be demonstrated on the
   dual-cycling geometry.
