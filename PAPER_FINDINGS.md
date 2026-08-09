# E-HGATv2 — Paper Findings (durable summary)

> Single source of truth for the paper's claims, numbers, caveats, data provenance, and open
> items. Written so context survives `/compact`. Paper: `paper/main.tex` (2057 lines),
> "Faithful Tropical Explanations for Guiding Bi-Objective QC + SA-AGV Scheduling",
> prepared for Prof. Mahdi Homayouni.

## Thesis in one line
A single object — the gradient of an **exact max-plus (tropical) longest-path** layer embedded
in a physics-fused heterogeneous GATv2 surrogate (**TAPE** = Tropical Attribution for Physical
Explanations) — is a **faithful** critical-path attribution, and it (R1/R2) explains schedules,
(R3) steers NSGA-II, and (R4) describes Pareto-front behaviour. Learned **attention is not
faithful**; TAPE is faithful **by construction**.

## STRATEGY (owner directive, 2026-07-03) — THIS IS AN OR PAPER FIRST
The advisor is an **OR advisor**; this paper must deliver **demonstrably valuable OR results**,
not an interpretability thesis. The verbatim requirements are in `ADVISOR_BRIEF.md`. The paper
must show:
1. **R3 scalability** — guided optimization (attn/TAPE-steered NSGA-II) keeps its advantage as N
   grows, where standard non-GNN methods (**random NSGA-II, mp-BRKGA**) **stall**.
2. **Amortization** — the surrogate **learns Pareto-front behaviour** and reuses search-time
   knowledge (search→knowledge loop); R4 corr 0.945 on the composition-diverse set.
3. **Peak-power–coupled regime** — the SAME scalability + amortization advantages must hold under
   the coupled power constraint, not just uncoupled.
4. **R1** — native encoding of the problem features (physics-fused heterogeneous encoding).

**The interpretability / attention-faithfulness / Viterbi / H1-second-architecture track is a
SEPARATE LATER FORK (TMLR/ICLR), NOT this paper.** Do not reframe this paper around
attention-faithfulness; do not spend this paper's compute on Viterbi or a 2nd architecture.
When the OR paper is done and submitted, fork the repo for the ML submission and add Viterbi there.

## The interpretability contribution (DEFERRED to the ML fork — kept for that future paper)
For the later ML fork only: the interpretability core is the attention≠critical-path
dissociation. The OR problem is the rare testbed with an *exact, computable* ground-truth
attribution (the critical path), which the attention-faithfulness literature (Jain & Wallace
2019) never had. The exact attribution comes from the **head being a tropical DP** (shared by
Viterbi/CTC/DTW/shortest-path), so the domain is *replaceable* — the point a second domain
(Viterbi/CRF) would prove in the fork. **The dissociation is independent of whether the surrogate
is a good scheduler.** None of this drives the current OR paper.

## Load-bearing vs decidable ground truth (the core strategic tension — READ THIS)
The single most important framing issue for venue/significance. Do not conflate two different
"ground truths":
1. **Ground truth for faithfulness** = the critical path (what actually sets C_max). In the
   *uncoupled* regime this is **closed-form** (`d/v` + the max-plus DP) — the GNN is **not
   needed to compute it**.
2. **The signal under test** = the GNN's *attention*, which comes only from the GNN.

Faithfulness asks "does the model's explanation (attention) match what drives the answer,"
NOT "does the GNN compute the answer." So the GNN **is** load-bearing **for the claim** (the
attention being falsified is the GNN's), and is **not** load-bearing **for computing the
ground truth**. Having a ground truth is the asset because it lets you *check* the attention
against a known answer — the thing the whole attention-faithfulness literature (Jain &
Wallace) cannot do. The faithfulness *logic* is sound and IS a claim about the GNN.

**The real weakness is IMPORTANCE, not logic.** On uncoupled scheduling the task is
closed-form solvable, so the GNN is a model **nobody would deploy** — falsifying the attention
of an unnecessary model is low-stakes. Where the GNN *is* necessary (coupled, no closed form)
the result is synthetic and weakest (Jaccard 0.11 at the makespan extreme). So the paper is
caught between *clean-but-unnecessary-model* and *necessary-but-synthetic-and-weak*. Scale,
seeds, and even a 2nd architecture do NOT fix this (GAT/Transformer on the same solvable task
are still unnecessary models).

**Where the E-HGATv2 GNN is load-bearing (full ledger):**
| Setting | Model necessary for task? | Faithfulness ground truth | Verdict |
|---|---|---|---|
| Uncoupled scheduling | No (leg times = d/v) | exact, physical/closed-form | GNN redundant -> strawman |
| Coupled scheduling | Yes (no closed-form C_max) | exact (simulator) | GNN load-bearing but synthetic + weakest |
| Viterbi/CRF (NLP) | Yes (scores learned) | exact (model's own Viterbi path) | load-bearing -> but NOT this GNN |

**Does Viterbi have a ground truth? YES — and a cleaner one.** In Viterbi/CRF the faithfulness
ground truth is the **model's own decoded path** (argmax of the tropical DP over *learned*
scores) + its gradient — exactly computable, so faithfulness stays decidable. It has no
*external* closed-form critical path, but that's the **correct** faithfulness ground truth
("does the explanation reflect the model's computation"), AND the model is necessary. Key
insight: scheduling's *extra* asset — a physical closed-form critical path independent of the
model — **is exactly what makes its model a strawman** (closed-form => model unnecessary =>
nobody cares about its attention). Viterbi keeps the decidable ground truth and removes the
unnecessary-model poison pill. **You don't need physical ground truth; you need *decidable*
ground truth on a *necessary* model.** Scheduling gives the first, not the second; Viterbi gives
both. This is the real (non-scale) reason Viterbi is the centerpiece for an ICLR-significant
claim, and why the demote-GNN-to-apparatus reframe is not optional.

**Strategic fork:** (A) reframe around TAPE-the-method + invest in Viterbi (GNN -> one instance,
demoted); or (B) make the coupled regime a strong *GNN-necessary* result and defend its realism.
What you cannot do: keep the GNN central on the uncoupled regime and call it ICLR-significant.

## CONFOUND: is the unfaithfulness real, or an artifact of THIS design? (threat to validity)
The fusion does NOT corrupt the attention (two-stage training: the core + its attention are
trained alone on scalar C_max by MSE, then **frozen**; the TAPE head is added downstream and
never backprops into the attention). So "fusing TAPE makes attention gibberish" is literally
false. **But** the attention may be gibberish for two design-specific reasons, either of which
would make the finding about *this model*, not *attention*:
1. **Architecturally degenerate attention.** In a resolved schedule each task has ≤1 AGV and ≤1
   QC predecessor, so the within-relation GATv2 softmax is **degenerate (α ≡ 1)**; the only
   non-degenerate attention is a **2-way** semantic gate (AGV- vs QC-bound). That is not the
   rich multi-neighbour attention the faithfulness debate is about — a reviewer can say the
   max-plus-aligned design *crushed* the attention, it wasn't "unfaithful."
2. **Scalar-only supervision.** The core is trained only to fit the scalar C_max; nothing ties
   attention to the critical path. The paper admits β *could* encode the binding resource in
   the β→{0,1} limit but scalar training doesn't make it. So the result may reduce to
   "unsupervised attention doesn't spontaneously become a critical-path detector" — weak.
   (Latent tension in the paper: it claims the architecture is max-plus-*aligned* AND that
   attention is unfaithful; if alignment worked, attention would be faithful.)

**Two controls are now NECESSARY, not optional:**
- (a) A **non-max-plus-aligned architecture (plain Transformer, rich attention)** on the same
  task. If its attention is *also* unfaithful → confound ruled out. If faithful → the
  unfaithfulness was the design. **Decisive test.**
- (b) **Try to train attention to be faithful** (critical-path alignment loss). If it *still*
  can't match the critical path → strong/surprising. If a little supervision fixes it → finding
  collapses to "you didn't ask it to." 

Until (a) runs, we cannot distinguish "attention is unfaithful" from "this design's attention is
degenerate." Real threat to the core claim.

## NOVELTY VERDICT (literature search, 2026-07)
**Verdict: the *specific combination* — using the exact gradient/decoded-path of a tropical/
Viterbi DP as a FREE ground-truth faithfulness oracle to falsify learned ATTENTION, in a
structured-prediction model class — is OPEN (not found). BUT both component ideas are
established, so the novelty is the *synthesis + model class*, not either piece.**

What already exists (a reviewer will cite these against novelty):
- **Attention is unfaithful** is old: Jain & Wallace 2019; Wiegreffe & Pinter 2019 (1908.04626);
  Serrano & Smith 2019. Classification/QA/sentiment, PROXY ground truth (erasure/gradient/
  adversarial). Wiegreffe & Pinter explicitly list sequence labeling as *future work*.
- **⚠️ BIGGEST DENT — exact/synthetic ground-truth faithfulness eval ALREADY EXISTS.** Arras
  et al. 2022 (pure synthetic task, known true explanation); Bastings et al. "Will You Find
  These Shortcuts?" (2111.07367, injected lexical shortcuts as ground truth); RULER
  needle-in-haystack attribution; "Faithfulness Metrics Don't Measure Faithfulness: A
  Meta-Evaluation with Ground Truth" (2605.25052, 2026). ⇒ **The paper's claim that the debate
  is "unfalsifiable" / "only a physically grounded objective makes faithfulness decidable" is
  FALSE and MUST be dropped/rescoped.** Deciding faithfulness against exact ground truth is an
  established methodology.
- Mensch & Blondel 2018 (1802.03676): DP gradient used to COMPUTE structured attention + notes
  sparsity→interpretability — NOT as an oracle to audit other attention.
- "On the explainability of max-plus neural networks" (2605.00889, 2026): max-plus critical-path
  attribution (most-activated-neuron) but its OWN method, on image classification, vs SHAP/IG —
  not an attention audit, not structured prediction.
- "Tropical Attention" (2505.17190, 2025): tropical attention to SOLVE combinatorial tasks —
  builds a model, does not audit faithfulness.

**The genuinely open gap:** no paper (i) uses the DP's *own* gradient (decoded/critical path) as
the ground-truth attribution oracle, (ii) to falsify *attention*, (iii) in a load-bearing
structured-prediction model. No head-to-head of attention-faithfulness vs the Viterbi/CRF path
in sequence labeling exists (searches confirmed absence).

**Defensible novelty (narrow, honest):** prior exact-ground-truth work *injects* the ground truth
(synthetic shortcuts/needles) into otherwise-normal tasks; here the exact attribution is
*intrinsic and free* (the DP gradient), on a model class (structured prediction) that is actually
deployed. That INTRINSIC-vs-INJECTED distinction + the structured-prediction/tropical-DP class is
the real delta — modest, framing-level, not a new empirical phenomenon. **Do NOT claim
"decidability is new"; DO claim "an intrinsic free exact oracle for a deployed structured model
class, where injected-shortcut methods don't apply."**

## Central results (with exact numbers)

### Faithfulness — TAPE yes, attention no (R2)
- TAPE leg-critical Jaccard vs exact oracle: **0.95–1.00 uncoupled, 0.87–0.95 coupled**.
- Attention Spearman ρ vs true makespan levers: **−0.09 to +0.17** (≈ zero).
- **Granularity ladder** (attention / TAPE / random baseline), pooled 9 instances:
  - precision@1: 0.69 / **0.98** / 0.70   (critical-fraction baseline ≈0.70, NOT 1/N)
  - ROC-AUC: 0.51 / **0.94** / 0.50
  - Spearman vs graded sensitivity: +0.07 / **+0.70** / 0.00
  - separation (crit−off, σ): +0.06 / **+1.92** / 0.00
  - ⇒ attention carries **no** critical-path info at any granularity; TAPE near-exact.

### The optimization win is SCREENING, not attention/TAPE targeting (the key nuance)
Search-guidance ablation, mean HV/HV\* over N=5,8,10:
- random mutation **+ screening**: **0.991 (BEST)**
- attention-targeted + screening: 0.977
- TAPE-targeted + screening: 0.956
- random mutation, **no** screening: 0.950 (null)

⇒ **Screening is the engine** (+0.041 over null). **Diffuse beats precise** targeting (HV rewards
spread; exact bottleneck-targeting is over-exploitative). So "the GNN helps optimize" = TRUE
(via the surrogate screening + amortization); "attention *specifically* helps" = FALSE.

### ✅ THE THESIS CLAIM IS SUPPORTED — GNN-infused NSGA-II beats the baselines, gap GROWS with N (NEW, 2026-07-04, READ THIS BEFORE DESPAIRING OVER mp-BRKGA)
**Framing correction (owner, 2026-07-04):** the thesis claim is the standard OR one — *"infusing
NSGA-II with the GNN surrogate beats the standard baselines (random NSGA-II, single-pop BRKGA,
mp-BRKGA)."* It compares against baselines **as configured**. A "screened mp-BRKGA" is an ICLR-strict
fairness bar, NOT the thesis bar; "would a cheaper surrogate also screen" is a secondary robustness
question (the GNN-vs-classical ablation), not a threat to the headline. DO NOT gate the OR claim on it.

> ⚠️ **SUPERSEDED 2026-08-09 — DO NOT QUOTE THE TABLE BELOW.** It is the `scaling_natfull_*`
> ladder (8 seeds, k=2, N≤80, 15-gen PF*). The canonical ladder is `scaling_opt_{unc,pp30}`
> (N=10–160, **20 seeds, k=4**, 50-gen PF*), which is stronger everywhere: TAPE wins **all 30
> cells**, 29/30 beyond the combined 95% CI, margins up to **+0.674**. In particular the
> "N=40 goes negative vs mp-BRKGA (−0.040/−0.050)" line below is **WRONG at canonical
> settings** — it is +0.022 (unc) / +0.123 (pp30): the dip narrows but never inverts.
> Canonical numbers and the four-ladder provenance table: `docs/PROGRESS.md` §"WHICH R3
> LADDER IS CANONICAL". In the paper as Table `tab:optladder` + `fig:scale`.

Native budget, k=2, 8-seed cells, **best-guided minus baseline** (hv_ratio):
| regime | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| unc: guided − random-NSGA-II | +0.104 | +0.130 | +0.192 | **+0.284** |
| unc: guided − single-pop BRKGA | +0.081 | +0.156 | +0.281 | **+0.404** |
| unc: guided − mp-BRKGA | +0.161 | +0.091 | −0.040 | +0.086 |
| pp30: guided − random-NSGA-II | +0.161 | +0.293 | +0.315 | (pending) |
| pp30: guided − single-pop BRKGA | +0.073 | +0.148 | +0.366 | (pending) |
| pp30: guided − mp-BRKGA | +0.151 | +0.170 | −0.050 | (pending) |

- **Guided BEATS random NSGA-II and single-pop BRKGA at EVERY N, and the margin GROWS with N**
  (unc random: +0.10→+0.28; unc sp-BRKGA: +0.08→+0.40). This IS the R3 advisor requirement met:
  "standard non-GNN methods STALL where GNN-guided holds." Random NSGA-II stalls (0.825→0.575),
  sp-BRKGA stalls harder (0.848→0.455), guided holds (0.912→0.832). Supported decisively at scale.
- **mp-BRKGA is the ONE strong baseline** (tuned multi-pop metaheuristic, does not stall): guided
  wins small-N, ties large-N (unc N=80 = +0.086), one coupled N=40 loss. **Competitive with the
  strongest baseline while dominating the rest = a legitimate OR thesis result. You do NOT need to
  beat mp-BRKGA; you need to beat the baselines (✓) and stay competitive with the best (✓).**
- Mechanism honesty (does not threaten the headline): the GNN's help is SCREENING (surrogate
  prediction), attention/TAPE targeting is ~neutral. Frame as "surrogate-assisted NSGA-II"; the
  guided-vs-random margin is the clean ablation proving the GNN adds value.
- **Better-surrogate lever @ N=160:** under the thesis framing this is DEFENSIBLE (compare to
  baselines as configured) — it widens the already-decisive random/sp-BRKGA win and may flip the
  mp-BRKGA tie. Needs baseline N=160 to land first. NOTE: this SUPERSEDES the earlier
  "screened-mp-BRKGA is the decisive arm" claim below — that bar was mis-imported from ICLR.

### ⚠️ SCREENING IS UNDER-CRANKED AT k=2 IN EVERY RUN — free headroom (NEW, 2026-07-04)
**The mechanism (`screening_factor=k`):** generate `k×P` candidate offspring, surrogate-rank them,
exact-evaluate only the best `P` (`attention_nsga2.py:912-927`). `evaluations += len(offspring)`
is capped at `P`, so **cranking `k` costs ZERO extra exact evals** — only cheap surrogate forward
passes. mp-BRKGA has no equivalent. This is the same knob in the guidance ablation above, not a
new mechanism.
- **Every result to date used k=2** (`run_opt_scaling.sh` COMMON hard-codes `--screening 2`,
  overriding the argparse default of 4). The main table, the scaling sweep, AND the
  currently-running native N=160 overnight sweep are all at k=2 = **under-cranked**.
- **The guided arm bundles guidance + screening** (`run_tape`: `guidance="tape",
  screening_factor=k`). There is NO guidance-only or screening-only arm. So the runs that
  *lost to mp-BRKGA* had screening ON (at k=2), not off — the loss was under-cranked screening,
  not missing screening. (random NSGA-II arm = the only screening-off control, `screening_factor=1`.)

**De-risking probe (`scripts/probe_screening_fidelity.py`, N=40, both regimes, one seed each):**
warm a TAPE-guided population, build a shared `k_max×P` near-Pareto offspring pool, then measure
whether surrogate screening recovers the *true-best-P* hypervolume. Metric **HV-recovery** =
`(HV_surrogate − HV_random)/(HV_oracle − HV_random)`: 1.0 = picks as well as an oracle, 0 = no
better than random.

| | uncoupled | coupled (pp=30) |
|---|---|---|
| global held-out R²_makespan | 0.990 | **0.658** (weak) |
| **in-pool Spearman(pred,true) makespan** | 0.996 | **0.891** |
| HV-recovery @ k=2 / 4 / 8 / 16 | 1.00/1.00/1.00/1.00 | 1.00/1.00/0.89/1.00 |
| HV_oracle rises with k? | yes 14.4M→16.1M | yes 10.2M→11.4M |

**Key insight:** what screening needs is *ranking* fidelity, not *regression* fidelity. In the
coupled regime global R² was only 0.66, yet **in-pool ranking Spearman was 0.89** and HV-recovery
stayed ~0.89–1.00. Ranking survives inside the narrow near-Pareto pool even where absolute R²
sags. And HV_oracle *climbs* with k — a bigger pool genuinely contains better offspring, which the
surrogate harvests, for free. ⇒ **cranking k=2→8/16 is a real, free improvement to the guided arm
in BOTH regimes.**

**What it does NOT prove (honest):** (a) the probe measures ONE generation's selection quality,
not 40-gen convergence — high k over-concentrates offspring and can collapse diversity over many
gens; (b) it does NOT guarantee flipping the mp-BRKGA loss into a win. It proves un-exploited
headroom that costs nothing to test. **Next step: re-run the benchmark with `--screening 8` (and
16), multi-seed, both regimes, comparing final HV — this confirms the per-gen gain survives 40
gens of convergence.**

### ⚠️ WHAT IS ACTUALLY LOAD-BEARING FOR OPTIMIZATION — GNN vs attention vs generic surrogate (NEW, 2026-07-04, READ BEFORE ANY OPTIMIZATION CLAIM)
This resolves a recurring conflation that keeps causing panic. Three DISTINCT questions — do not merge them:

1. **"Is screening a novel mechanism?" → NO.** Surrogate-assisted MOEA (train cheap model,
   over-produce offspring, screen with it) is a 20-year-old paradigm (ParEGO, MOEA-D-EGO, K-RVEA,
   CSEA). *Using a surrogate to screen* is not, by itself, a contribution.
2. **"What is the surrogate?" → It IS the GNN.** `model.predict()` in the screening path
   (`attention_nsga2._predict_objectives`, `attention_nsga2.py:386-399`) is the E-HGATv2 GNN's own
   forward pass (message passing → embeddings → fused regression head). There is NO separate random
   forest / independent model. The paper attributes screening to the GNN correctly (main.tex:795,
   "the fused head's near-exact (Cmax,E) prediction screens").
3. **"Is the GNN BETTER than a generic surrogate at screening?" → UNTESTED = the real risk.**
   If a random forest / GP screens just as well, the optimization win is the 20-yr paradigm with a
   GNN plugged in, and it is NOT distinctively about the GNN. **This is the load-bearing unclosed
   hole.** No GNN-vs-classical-surrogate comparison has been run.

**Screening uses the GNN's REGRESSION output, NOT its attention weights (code-verified).**
`_predict_objectives` docstring: uses "the surrogate's near-exact regression (**not its
attention**)". Screening ranks on the two predicted scalars (makespan, energy); the attention
*pattern* is never read out for screening. ⇒ Swap the GATv2 attention for any black-box aggregator
that predicts equally well and screening is byte-for-byte identical. **Attention *faithfulness*
(the paper's whole thesis) is ORTHOGONAL to the optimization win.** You cannot use the optimization
result as evidence for the faithfulness claim, or vice versa. Two papers wearing one architecture.

**What IS structurally GNN-specific (a generic RF/GP CANNOT do it):**
- **Size-transfer / generalisation** (train-small/eval-large, R²≥0.98, amortization r=0.945). Graph
  nets are size-agnostic; a flat RF/GP trained on N=10 features cannot even be *evaluated* at N=160
  (wrong input dimension). **This is the genuine GNN-specific, defensible optimization-adjacent
  contribution — the honest spine. Frame the OR paper's GNN claim as size-transfer/amortization,
  NOT "attention guides search".**
- **TAPE** (differentiable critical-path gradient) requires the differentiable max-plus structure;
  an RF has no gradient / no TAPE. GNN/DP-specific — but its *optimization* value is weak (guidance
  neutral-to-harmful, see ablation above). Its real value is faithfulness → the TMLR fork.

**Paper R3 framing vulnerability (NOT fraud, but fixable):** §R3 headline is "Faithful guidance:
the explanation steers the search" (main.tex:780). It bundles TWO channels — (1) TAPE-guided
*mutation* (the distinctive, faithfulness-specific claim), and (2) regression-head *screening* (the
generic workhorse). The narrative invites crediting the win to channel (1), but the ablation says
channel (1) is neutral-to-harmful (random+screen 0.991 ≥ TAPE+screen 0.956) and channel (2) carries
the win. A sharp reviewer will demand the channels be separated. **Fix:** run the 2×2 (guidance ∈
{random, attn, tape} × screening ∈ {on, off}) at a couple of cells; rewrite R3 to say what's true —
"regression head amortizes + screens (workhorse); faithful guidance is a modest/neutral add-on."

### NATIVE-budget k=2 scaling — COMPLETE N=10–80 both regimes, 8 seeds (DONE 2026-07-04) — ⚠️ SUPERSEDED by `scaling_opt_*` (20 seeds, k=4, N→160); see the banner above and `docs/PROGRESS.md`
Native budget (P=20N), 8 seeds, k=2. Aggregated `scaling_natfull_{unc,pp30}/opt_scaling_summary.md`,
rsync'd to local `experiments/fused_tape_guided/`. **TAPE − mp-BRKGA (HV/HV\*):**

| regime | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| uncoupled | +0.144 | +0.091 | **−0.041** | **+0.059** |
| coupled pp30 | +0.151 | +0.170 | **−0.084** | **+0.057** |

- **Trajectory: win → win → dip(N=40) → win(N=80), both regimes.** Guided **decisively beats the
  weak baselines at every N and the gap GROWS** (guided − random-NSGA-II up to +0.39; guided −
  sp-BRKGA up to +0.48 at N=80 — 4–5× the ±0.1 CI = bulletproof). vs the one strong baseline
  (mp-BRKGA): wins N=10/20/80, loses only N=40. **N=80 is a WIN → the N=40 dip is NOT a scaling
  collapse; it recovers.** Guided-vs-mp is soft (±0.06–0.10 CI; unc N=80 was 4/8 per-seed) → state
  as "edges mp-BRKGA," decisive win only over random/sp-BRKGA.

#### ★ WHY the N=40 dip (diagnosed, 2026-07-04) — discrete fleet provisioning, NOT a metric artifact or scaling weakness
Diagnosed from the raw shard jsons (no new compute):
1. **The dip is in ABSOLUTE HV, not the PF\* reference.** Raw TAPE-hv ÷ mp-hv = 1.149/1.063/**0.939**/1.045
   (unc) and 1.182/1.161/**0.884**/1.021 (pp30) — same win/win/lose/win. ref_hv grows smoothly
   (1.05M→6.0M→15.4M→28.4M unc). ⇒ mp-BRKGA genuinely finds a better front at N=40; the
   circular-PF\* hypothesis is KILLED.
2. **Not monotonic degradation** (N=80 recovers) ⇒ "surrogate fidelity decays with N" is WRONG.
3. **Root cause = `scaled_fleet(N)` discontinuity** (`instance.py:199`, AGVs=round(N/12), QCs=clamp(round(N/40),3,6)):
   | N | AGVs | QCs | tasks/AGV | AGV/QC |
   |---|---|---|---|---|
   | 10 | 2 | 3 | 5.0 | 0.67 |
   | 20 | 2 | 3 | 10.0 | 0.67 |
   | **40** | **3** | **3** | **13.3 ← ladder MAX** | **1.00 ← bottleneck crossover** |
   | 80 | 7 | 3 | 11.4 | 2.33 |
   | 160 | 13 | 3–4 | 12.3 | 3.25 |
   N=40 is (a) the **most AGV-contended** point (round(40/12)=3 under-provisions → 13.3 tasks/AGV, the
   ladder max) AND (b) the **bottleneck-balance crossover** (AGV/QC=1.0, where the instance flips from
   QC-bound/AGV-scarce at small N to transport-bound/AGV-rich at large N).
4. **Mechanism:** the guided arm's edge comes from EXPLOITING bottleneck structure (surrogate screens
   toward, TAPE steers toward, the critical resource). At N=40 the instance is maximally contended AND
   bottleneck-ambiguous → least exploitable structure → surrogate/critical-path edge shrinks, while
   mp-BRKGA's structure-AGNOSTIC brute multi-pop search is relatively strongest. Clear structure (and
   the guided lead) returns at N=80/160 (transport-bound). ⇒ **guided's advantage tracks bottleneck
   clarity.** Honest framing for the paper: disclose the N=40 dip as "an artifact of discrete fleet
   provisioning at the bottleneck-balance crossover," pair with the N=80 recovery. NOT a scaling weakness.
5. **To confirm (optional, cheap):** rerun N=40 with 4 AGVs (tasks/AGV→10, matching N=20/80); if the
   dip vanishes the fleet-discontinuity explanation is proven. Or check in-pool Spearman dips at N=40.

- **attn ≈ TAPE (regime-dependent flip at N=80: coupled TAPE +0.059, unc attn +0.027)** — honest claim
  stays TIED. TAPE targeting neutral-to-slightly-harmful for the OR objective (screening is the engine).

### TMLR viability of the interpretability reframe (NEW, 2026-07-04)
TMLR judges *"are claims supported by accurate evidence?"* — NOT novelty/impact. So "modest but
rigorous" fits TMLR, and **reframing on interpretability makes the weak optimization results
IRRELEVANT** (beating mp-BRKGA stops being a claim the paper makes). Conditional on THREE things:
(1) the DP-gradient-as-faithfulness-oracle novelty must actually hold — RE-CHECK the deep-research
verdict (OPEN/PARTIALLY-COVERED/TAKEN) before banking on it; (2) a SECOND tropical-DP domain
(Viterbi/CRF) to generalise beyond one scheduling GNN — this is what makes it a *methods* paper;
(3) a clean quantitative attention-vs-DP-gradient divergence result. Not a consolation prize — a
legitimately separate, defensible paper.

### R3 optimization dominance vs classical metaheuristics
- **TAPE > mp-BRKGA on HV in 11/11 instances**, Holm p=0.0029. Friedman χ²₄=37.2, p=1.6e-7.
- Avg HV ranks: attn **1.27**, TAPE **1.73**, random 3.45, sp-BRKGA, **mp-BRKGA last**.
- **TAPE vs attention: statistically TIED** (Holm p=0.175 @20 seeds; attn numerically ahead
  8/11; Cliff's δ=−0.12). Honest claim: *faithful TAPE guidance **preserves** the optimization
  performance of unfaithful attention* — do **NOT** claim TAPE converges faster than attention.
- **Convergence** (N=50, 30 seeds, matched eval budget, **vs single-pop BRKGA**): guided reaches
  BRKGA's *final* HV by gen ≈42 (**2.4× fewer iters**), ends **2.5×** higher; IGD⁺ 296 vs 1435.
- **Scaling amplifies the gap**: guided-over-BRKGA +1.3 pts HV\* at N=5 → **+38.8 at N=50**.
- ⚠️ The convergence/scaling sweep used **single-pop BRKGA, not mp-BRKGA**. mp-BRKGA convergence
  comparison is a **deferred run** (paper flags it as "a straightforward additional run").

### Size generalisation — TRAIN-ONCE @N=16, EVAL to N=5000 (NEW, 2026-07-03, VM/GPU) — `tab:generalize`
Train the core+fused ONCE at N=16, inference-only up to N=5000 (312× extrapolation), 3 seeds,
uncoupled. Result (per-N means):
- **Fused makespan R² FLAT ≥0.98 across the whole ladder**: 0.997 (N=16) → 0.989 (N=5000).
- **Black-box global-readout core R² COLLAPSES monotonically**: −0.3 → −7263 (worse than mean).
  The physics-fused head predicts per-leg (size-invariant) times + tropical DP aggregates → size-
  invariant; a pooled global readout cannot extrapolate a makespan magnitude that grows with N.
- TAPE leg-Jaccard preserved 0.90–1.00; attention ρ ≈ 0 (|ρ|≤0.07) at every N (dissociation holds).
- ⇒ surrogate + explanation transfer intact FAR beyond the N≤160 DL benchmark. **This is the OR
  scalability headline** the advisor wants.
- **Coupled does NOT size-generalise**: same train-at-16 head, R² turns negative within a small
  multiple of N=16 (seed0: N=25 R²=0.81, N=50 R²=−2.1, N=100 R²=−70, N=250 R²=−986) because
  power-wait arcs have no closed-form contribution to extrapolate. Coupled needs retraining at the
  target size (where it's accurate, R²≈0.78). Honest negative, reported as such.
- Script: `scripts/run_scaling_generalization.py`; data `experiments/scaling/generalization_uncoupled.json`.

### MATRIX RE-RUN (proxy fix, 20 seeds, 11 instances) — DONE 2026-07-03 — REFRESHES tab:main/tab:stats
Re-ran `run_tape_matrix_sharded.sh 20 4` with the folded-PF* proxy fix. **0 cells >1.0** (max
HV/HV*=0.9766) — the reference-proxy caveat is now FALSE and REMOVED from the paper. Had to
delete a stale `tape_bench_toy8_unc.json` (early smoke) that duplicated toy8 → 12 instances;
clean count is 11. **SD-20-C now ran at 20 seeds** (not 5) — that caveat is also obsolete.
Refreshed headline (hv_ratio):
- TAPE > mp-BRKGA **11/11**, Holm **p=0.0029**, Cliff's δ=**0.64 (large)** [unchanged from paper].
- HV avg ranks: **TAPE 1.45, attn 1.55**, random 3.64, sp-BRKGA 3.82, **mp-BRKGA 4.55 (worst)**.
  (Was attn 1.27 / TAPE 1.73 — now TAPE is *slightly ahead*, strengthening the tie claim.)
- **TAPE vs attn: TIED, Holm p=0.831** (was 0.175), δ=+0.008 negligible, tape_wins 6/11, Wilcoxon p=0.831.
- Friedman: hv_ratio χ²=35.05 p=4.5e-7; gd_plus χ²=37.45 p=1.45e-7 (abstract's "37.2/1.6e-7" ≈ gd_plus).
- Refreshed tab:main per-instance (TAPE/attn/rand/mp/sp, * = best):
  SD-5 *.977/.975/.969/.928/.964; SD-8 .931/*.954/.914/.881/.907; SD-10 .872/*.899/.837/.774/.796;
  SD-15 .866/*.869/.784/.759/.806; SD-20 *.800/.749/.643/.674/.673; L07 .951/*.959/.928/.911/.921;
  L15 *.941/.929/.850/.849/.826; L21 *.940/.916/.847/.742/.870; L35 *.945/.940/.876/.827/.878;
  SD-10-C .872/*.887/.811/.778/.804; SD-20-C *.750/.732/.497/.603/.595.
  ⇒ **TODO: refresh tab:main + tab:stats + abstract Friedman/rank/p numbers to these in the final pass.**

### R3 optimisation scaling — guided vs mp-BRKGA across N (NEW, GPU sweep IN PROGRESS)
Train+optimise per N (retrain each instance), matched budget P=5N (=20N evals/gen), 6 seeds, both
regimes. GPU-enabled search (`--search-device cuda`) needed for N≥80 (TAPE guidance is per-schedule,
~90–120 min/seed on CPU at N=160). Ladder: uncoupled N=10/20/40/80/160, coupled N=10/20/40/80.
- Early points (uncoupled, HV/HV*): N=10 guided ~0.905 (TAPE)/0.909 (attn) vs mp-BRKGA 0.794,
  random 0.826, sp-BRKGA 0.841. Guided leads mp-BRKGA by ~0.11 at N=10.
- The gap-vs-N (does mp-BRKGA "stall" as N grows) is the deliverable — ✅ **COMPLETE 2026-07-06**,
  landed in `scaling_opt_{unc,pp30}` at 20 seeds/k=4, N=10–160, BOTH regimes. **Answer: yes,
  mp-BRKGA stalls hard** — at N=160 it reaches 0.040 (unc) / 0.264 (pp30) of HV* against TAPE's
  0.597 / 0.879. TAPE−mp margin +0.557 unc, +0.615 pp30. Canonical table in `docs/PROGRESS.md`
  §"WHICH R3 LADDER IS CANONICAL"; in the paper as Table `tab:optladder` + `fig:scale`.
- Key compute fact (see `COMPUTE_SCALING.md`): exact evaluator is FAST (1259 evals/s @N=160);
  mp-BRKGA @N=160 40-gen ≈ 228s/seed. The cost is the per-schedule TAPE guidance/screening; GPU
  helps modestly (per-schedule launches, not batched). Batching `explain_fused` would give ~10×.

### Surrogate fidelity scaling (retrain per N, 20 seeds) — Table `tab:fidelity`
- Uncoupled makespan R²: **0.998 (N=6) → 0.997 (N=50)** (flat over 8.3× growth). Energy R²=**1.000** (exact by construction).
- Uncoupled leg-Jaccard: 0.991 → 0.980 (≥0.98 to N=50).
- Coupled: R² 0.805→0.777, Jaccard 0.928→0.913 (N=10→50). Coupled is the genuinely harder regime.

### Amortization of front composition (R4)
- Public **L01–L35 transport-saturated** (ρ=0.88±0.04) ⇒ amortization **untestable** (model MAE
  0.048 = constant baseline 0.048). Itself a finding: "transport binds" is near-invariant here.
- **Composition-diverse synthetic** (20 inst, ρ∈[0.19,0.99]): LOIO MAE **0.107** vs constant
  0.289 (2.7× better, wins 17/20), predicted-vs-true **r=0.945**.
- Does NOT amortize: within-front ρ ordering (~0.12), per-task criticality from static features
  (AUC 0.53 = chance). Amortization is at **instance-composition** level, not per-task.

#### ⚠️ R4 predictor is a feature-MLP, NOT the GNN (open item — 2026-07-03)
The R4 amortization predictor is a **tiny 2-layer MLP (32-32)** on **5 hand-crafted scalar
features** `[λ, num_tasks, num_agvs, num_qcs, mean_handling]` → `(transport_frac, qc_frac)`
(`scripts/run_front_learning.py:_train_predictor`, `_feature_row`). It is **not** the E-HGATv2
GNN. Chosen for **simplicity/differentiability** (coarse aggregate target), NOT for accuracy over
a GNN — the docstring says "simple predictor… tiny… since we're predicting aggregate statistics";
**GNN-vs-MLP was never compared**. For 5 features × ~20 instances a tiny model is methodologically
correct (a GNN would likely overfit), so it's not a bug — but it sits **off the GNN-centric
narrative**.
- **The GNN IS central to R4's pipeline anyway**: it guides the NSGA-II search that produces each
  front (stage 1), and **TAPE** computes the critical-path composition targets (stage 2). Only the
  final amortization step (stage 3, instance→composition) uses the MLP.
- **Proposed upgrade (deferred, contained — does NOT redo R4)**: make the amortizer the GNN's
  **pooled instance embedding → composition**, reusing the cached fronts + the same LOIO protocol.
  If it holds ≳0.9 → fully GNN-centric R4; if it only matches the MLP (likely, since composition is
  count-driven) → honest finding "structure-counts suffice", keep MLP as efficient baseline.
  Wait for the box to free (curriculum + opt sweeps) before running.

### Coupled regime (weakest result)
- R²≈0.80, front-avg Jaccard 0.87 @N=20. Both graph methods still beat all non-learned baselines.
- **SD-10-C: energy extreme Jaccard 1.00, makespan extreme collapses to 0.11** (max power
  contention, power-wait arcs have no closed form). Genuine surrogate-accuracy ceiling
  (reproduced with 4-step unroll + 2000 samples). Coupled is **our own synthetic construction**,
  NOT part of the FSMJ benchmark — label exploratory.

## Config / budget facts
- mp-BRKGA fully implemented (`src/ehgat/baselines/mp_brkga.py`, 294 lines): multi-pop Ω single-obj
  + Π multi-obj, shared-elite migration; paper config P=20N, elite=0.2P, mutant=0.1P, pe=0.7,
  Gmax=300, Π=2, Ω=2, nex=30. Baselines: mp-BRKGA, single-pop BRKGA, NSGA-II(random), attn, TAPE.
- **Main-table runs: 20 seeds, 40 generations** (starved vs his 300). ⚠️ **Discrepancy to
  reconcile**: paper limitations says pop reduced "20N → 5N", but `runner.py` default = 20N and
  `screening_ablation.py` = 5N. Verify which the main `tape_bench_*` actually used.
- Physics constants (3 speeds): empty 4.8/6.0/7.2 m/s @ 7.8/10/13.2 kW; loaded 2.4/3.0/3.6 m/s @
  11.7/15/19.8 kW. Coupled peak-power budget = 30 kW.

## Data provenance (the confusion that keeps biting)
- **Repo Tables 4&5** = **2022 book chapter** [homayouni2022book]: distance matrix (6 QC × 6 LU)
  + **loading-only** instances **L01–L35** (in `data/tables_4_5.json`). These have **NO published
  optima** anywhere accessible.
- **DS01–DS26** (the Table-2 MILP/mp-BRKGA optima we'd reproduce) = **2021a paper**, **dual-cycle**
  (load+unload), **NOT in the repo** — only a *placeholder* `data/dsdl_instances.template.json`.
- **DL01–DL10** (Table-3, large, N up to 160) = 2023 paper, not in repo.
- Paper data link `fastmanufacturingproject.wordpress.com` = **job-shop only** (JSPT/FJSPT/EEJSP),
  **no AGV/container data** (verified). ⇒ external Table-2 reproduction **needs the professor's
  DS/DL data**; user is requesting it.

## Recurrence validation status
- vs his **equations** (Fontes & Homayouni 2023, Eqs 10–18): **symbolically verified this
  session** — LOAD/UNLOAD match; first-unload-zero-τ matches Eqs 14/15/17 (Eq 10 vacuous for a
  crane's first task). Encoded in `test_evaluator.py:81`.
- vs **brute force**: `test_oracle.py` cross-checks exact Pareto DP vs 3^(2N) brute force @N=5;
  evaluator = oracle = brute force.
- vs his **dataset numbers**: **NOT done** — needs DS Table-2 data. One residual ambiguity
  (implicit `c_0` flooring first unload at τ) is decidable ONLY by that reproduction.

## Open items
**OR / advisor track (orthogonal to the ML paper):**
1. **[BLOCKER]** Table-2 external reproduction — needs DS/DL data from professor.
2. Full-budget run (P=20N, G=300) vs the 40-gen main table (#2) — also unblocks the mp-BRKGA
   convergence sweep.
3. Reference-front >1.0 fix: **DONE in code** (`run_tape_guided_bench.py` now folds all evaluated
   fronts into PF\*, ratio ≤1 by construction) — needs a **VM re-run** to regenerate cells.
4. Coupled regime weakest (makespan-extreme Jaccard 0.11) — label exploratory / future work.
5. Amortization on a real structurally-diverse set (DL instances) — needs the data.
6. "TAPE exact" precision paragraph: **DONE** (after `prop:exact` in `main.tex`).
7. **[TODO — ABLATION] Does GNN screening enhance the mp-BRKGA backbone, or wreck its diversity?**
   (method question, 2026-07-04). mp-BRKGA is greedy on the PARENT side (elite retention, biased
   crossover pe=0.7, migration) but BLIND on offspring — it evaluates whatever crossover produces,
   no look-ahead. GNN screening adds the offspring-side selection it structurally lacks
   (complementary, not redundant). **Code DONE + smoke-tested**: `mp_brkga.py` has
   `screening_factor` + optional `screen_fn` (over-produce k·No offspring → surrogate-rank →
   keep No, elites/mutants untouched, ZERO extra exact evals); `run_tape_guided_bench.py --mp-screen`
   adds a `mp-BRKGA+GNN-screen` arm w/ the same core surrogate. Smoke @N=8: mp 0.78 → mp+screen 0.95
   (+0.17, budget-neutral) — plumbing works, NOT evidence.
   - **Hypotheses to test:** HELPS (offspring look-ahead filters duds free) vs HURTS (diversity
     collapse — screening over-concentrates offspring, HV rewards spread; perturbs the tuned
     0.2/0.1/0.7 elite/mutant/offspring balance → premature convergence; surrogate bias steers
     toward duds where ranking fidelity is low = coupled / large-N).
   - **Must measure (pure HV HIDES the failure mode):** HV/HV\* + **spread/decision-space diversity
     (CO-PRIMARY)** + **evals-to-target-HV (convergence/efficiency)**, across **k∈{2,8,16}** (expect
     an INVERTED-U, not monotone), both regimes, N∈{40,80,160}.
   - Also add **single-pop BRKGA+GNN-screen** (same hook, ~5-line edit) → a 3×2 backbone×screening
     ablation table (NSGA-II / mp-BRKGA / sp-BRKGA × screen off/on) = "GNN surrogate is a
     backbone-agnostic enhancer." NOTE: NSGA "screen-on" cell = random-mutation + screening_factor=k
     (current main-table random arm is screen-OFF, =1).
   - **Framing honesty:** surrogate-assisted BRKGA/MOEA is an established class (K-RVEA etc.);
     novelty is the *physics-fused GNN surrogate* + this problem, NOT "screening a BRKGA."
   - **★ KEY HYPOTHESIS TO TEST (owner-recommended): GNN-infused mp-BRKGA shows MONOTONIC
     performance growth at higher N.** i.e. the enhancement (mp+GNN-screen − vanilla mp) should
     GROW with N — mirroring how guided−random-NSGA-II already grows with N (+0.10→+0.28 unc,
     +0.16→+0.32 pp30). Rationale: at large N the offspring space explodes and blind crossover
     wastes more exact evals on duds, so surrogate look-ahead should pay off MORE as N grows. If
     confirmed, the story is "the GNN's value as a backbone enhancer scales with problem size" —
     the strongest possible version of the R3 claim. Measure Δ=(mp+screen − mp) vs N∈{40,80,160}
     both regimes; want Δ increasing in N (and not diversity-collapsing — track spread).
   - Run when the box frees (after native N=160 baseline lands + pushed).
8. **[TODO — LEVER] Better surrogate (more training samples/epochs) → demonstrate a DEFENSIBLE win
   at N=160** (owner-recommended, 2026-07-04). The ONE genuinely GNN-specific optimization lever:
   a better-ranking surrogate improves screening for the guided arm (and mp+GNN-screen) WITHOUT
   helping vanilla mp-BRKGA (it has no surrogate). Most useful in **coupled**, where fidelity is
   only Spearman 0.89 / global R² 0.66 — headroom to raise ranking quality.
   - **Plan:** at N=160 both regimes, retrain surrogate with larger budget (e.g. core 2000/80 +
     fused 1500/80 vs the sweep's 800/40 + 600/40), rerun the guided arms (+ mp+GNN-screen), compare
     final HV vs the k=2 baseline and vs mp-BRKGA.
   - **Cheap GATE FIRST (do before the full opt run):** ranking-fidelity probe at N=160
     (`probe_screening_fidelity.py`), default-surrogate vs bigger-surrogate — does more training
     actually raise in-pool Spearman / HV-recovery at N=160? If it doesn't move (selection may be
     near-oracle already — HV-recovery was ~1.0 at N=40), more training won't help → STOP.
   - **Honest caveats:** (a) costs training exact-evals — the cost-ledger MUST charge them;
     (b) coupled R²=0.66 suggests a fidelity ceiling; (c) it's still a *screening* win (defensible
     under the OR thesis framing = beat baselines as configured; NOT defensible vs a screened
     baseline — but per owner, the thesis bar is baselines-as-configured, so this is fine).
   - **Needs baseline N=160 to land first** (can't measure a "win" without it).

**ML / publishability track (see `memory/paper-to-iclr-tmlr-punchlist.md`):**
7. 2nd attention architecture (transformer-style) — biggest hole for "attention" not "this model".
8. Readout robustness (last-layer/mean/max/rollout/grad×attn invariance).
9. 2nd DP domain: **Viterbi/CRF** on NLP tagging — proves the mechanism is tropical-DP, not OR.

**Scaling study (in progress):** `scripts/run_scaling_generalization.py` — **train-small /
eval-large** (train once @N=16, inference to N=10000): core R² collapse vs fused R² hold, TAPE
Jaccard, attention ρ/prec@1 vs N. VM-only. See `memory/scaling-is-train-small-eval-large.md`.

## Compute optimisation (2026-07-05) — batched tropical DP; Numba is dead
**Profiled the guided-tape search on an A40 (N=80, both regimes).** Full measured correction in
`GPU_PARALLELIZATION.md` §0. Findings:
- **Exact evaluator (the "Numba refactor" target) = 0.2–0.3% of wall-clock**, both regimes →
  Numba is useless; it was mis-ranked as a top lever. Dropped.
- **Real bottleneck = the fused head's `tropical_longest_path` in a per-node Python loop**
  (`tropical_dp.py:52`, 2× `.item()` GPU-syncs/node) — **68% (unc)/83% (coupled)** of wall,
  called per-graph in BOTH screening (`tape_predict_objectives`) and per-gen guidance
  (`tape_signals_batch`). Naive `SEARCH_DEV=cuda` *hurt* (millions of GPU syncs). NSGA sorts 0.0%.
- **FIX (implemented, parity-tested):** route both paths through the pre-existing layer-vectorised
  `batched_longest_path` (`build_batch`+`_forward_batch`, `train_fused_batched.py`) — one
  block-diagonal max-plus DP per chunk, zero per-node syncs. **6.6× (unc)/9.8× (coupled)** on the
  profiled search. `tests/unit/test_screening_batched_parity.py` proves screening makespan/energy
  bit-parity + guidance batch-invariance + coupled guidance bit-parity; full 239-test suite green.
- **Comparability:** screening ranks unchanged (bit-identical). A whole-ladder re-baseline through
  N=160 with the batched path is still required for internal consistency (as any impl/device move
  would be), but search *behaviour* is preserved. **This is the efficient path to N=160.**

## VM
Ephemeral vast.ai box; address changes per session. Current (2026-07-02): `ssh -i
~/.ssh/e_hgatv2_instance_ed25519 -p 23856 root@154.42.3.13` (2× A40 46GB, 255 cores, bare — needs
repo + env). All heavy runs on VM (see `memory/compute-runs-on-vm.md`).

## 2026-08-09 — Remnant-data audit of main.tex (COMPLETE)

Swept all 557 experiment JSONs against the paper. Everything now reported, except the
explicitly-listed gaps at the bottom. What got added this pass:

- **`fig:conv` CI bands.** `scaling_bench/N50/benchmark_results.json` stored
  `hv_curve_lo`/`hv_curve_hi` (101 pts × 3 methods, 30 seeds) that the figure never drew.
  Added as shaded polygons + the `HV*` = 3.454e6 ceiling line. Guided band separates from
  BOTH baselines **from generation 18**. Finals as fractions of HV*: 0.645 / 0.257 / 0.230.
- **`fig:conv` CANNOT be extended to mp-BRKGA** — that run has only BRKGA,
  E-HGATv2-NSGA-II, NSGA-II(random). Would need a new run. Caption now says so explicitly.
- **Attention architectural control** (`experiments/attn_control/`) — I wrote this up, then
  REMOVED it (commit f254fc1) at the user's direction: it is September interp-fork material,
  not OR-thesis scope. Numbers kept here only so the artifact is not re-discovered and
  re-litigated: global self-attention encoder, learned readout query over all N tasks,
  p@1 0.66/0.50/0.55 vs random 0.57/0.55/0.55 (gap +0.013), rho ~ 0 — but its own
  R2_Cmax is only 0.51/0.33/0.22, so it is a negative control on a weaker predictor and the
  paragraph argued a point then hedged it to near-nothing. Bad paper content either way.
  If the fork ever uses it, it needs a like-for-like control that actually fits Cmax.
- **Aggregated TAPE landscape** (`experiments/gnn_landscape/`). 256 schedules over 4
  decision families → assignment .35 > sequence .26 > loaded .21 > empty .18, stable ±0.01
  over N=10/20/50. Validated against the SAME aggregator run on the exact oracle: agrees to
  **≤0.0013** per family at N=10,20. AGV-side share 0.72–0.74. Negative reported too:
  pareto-vs-dominated family contrast ≤0.026, so this aggregate describes the INSTANCE, not
  solution quality.
- **Full 35-instance real L-set fidelity** (`fused_eval_real_Lset_full.json`, 5 seeds).
  R² mean 0.9994 / worst 0.9989; leg-Jaccard mean 0.995 / worst 0.989; arc 0.994; MAE 1.8s.
  Fidelity section previously only had synthetic instances (fixed 2 AGV/3 QC).
- **Coupled size curriculum** (`generalization_pp30_curriculum.json`). Pooling training over
  N∈{16,28,40} lifts coupled R² from −1.5 @ N=50 → +0.69 @ N=48, +0.52 @ N=32; still
  collapses after (−0.19 @ 64, −4.4 @ 96). Extends usable coupled extrapolation ~25 → ~50.
- **`tab:generalize` N=25 row** existed in the artifact, was missing from the table.
- **Tree-surrogate fit + TreeSHAP/Sobol divergence** (`landscape/landscape_n10.json`,
  `tabular_boundary`). Tree held-out R² = **0.12** (makespan) / 0.27 (energy). Sobol puts
  0.94 of makespan mass on the structural families; TreeSHAP puts **0.51** → absolute
  under-weighting **0.43** (same 0.43 for energy). Claims (1) and (3) of §XGBoost were
  argument-only before; now measured.

### ★ CORRECTED: the screening-throughput claim was WRONG (was main.tex item 1)
Old text: "~3ms for 200 schedules at N=50 vs ~45ms per schedule exact → ~15× throughput."
Internally inconsistent (3ms/200 vs 45ms/1 is 3000×, not 15×) and **not reproducible**.
Measured on this machine, 1 CPU thread, N=50, 200 schedules:

| regime | exact eval | surrogate fwd | + HeteroData build | fwd-only | incl. graph |
|---|---|---|---|---|---|
| uncoupled | 15.9 ms | 8.0 ms | 34.3 ms | 2.0× | **0.38× (LOSS)** |
| coupled pp30 | 74.3 ms | 9.9 ms | 28.7 ms | **7.5×** | 1.9× |

Uncoupled evaluator is just an O(N) longest path over closed-form leg times — it is cheap.
Paper now says plainly: **uncoupled screening is budget-neutral, not faster**; the
comparison is matched on *exact evaluations*, which is what makes the HV advantage
attributable to the ranking. The speed win is real only in the coupled regime. Also
removed the "throughput reported in Section~\ref{sec:ladder}" back-reference in the
tropical-layer appendix (no such throughput number is reported).
(Pairs with `memory/verify-mechanism-before-asserting.md` — measured, not recalled.)

### Still open after this audit
- `fig:conv` has no mp-BRKGA arm (needs a new run).
- No Related Work section.
- R4 (amortisation) has no coupled result.
- `fig:dag`, `tab:hyper` defined but never `\ref`'d.
- N=40 fleet-provisioning attribution still INFERRED, not isolated (controlled rerun at
  fixed AGV/QC ratio, ~1h, unrun).
- Nothing is compile-verified: no pdflatex/tectonic/latexmk on this machine.

## 2026-08-09 (later) — Second sweep: critical_path_demo + front_learning

The first audit swept `fused_tape_guided/`, `scaling_*`, `landscape/`, `fused_eval/`.
This pass finished the two directories left over. Both had real problems.

### ★ CORRECTED: the R2 worked-example section quoted SUPERSEDED v1 artifacts
`experiments/critical_path_demo/` holds two generations: `critpath_*.json` (v1) and
`critpath_*_v2.json` (v2, adds `distance_m` / `speed_ms` / `speed_level` / `qc` /
`agv_sequences` / `per_qc_on_path` — v1 has all of those as `null`). Commit `1f3ba8c`
regenerated the paper's per-step tables from v2 but left other numbers on v1. Fixed:

| item | was (v1) | now (v2) |
|---|---|---|
| SD-10 σ*_C energy | 12,896 kJ | **14,317 kJ** |
| SD-10 σ*_E energy | 10,938 kJ | **10,744 kJ** |
| energy saving at E-extreme | 15% | **25%** |
| `tab:critpath_summary` SD-8 | 100%/0% → 67%/33% | **86%/14% → 82%/18%** |
| `tab:critpath_summary` L07 | 63%/37% → 50%/50% | **89%/11% → 94%/6%** |

SD-5 and SD-10 rows were already correct. Added the coupled **SD-10-C** row
(83%/17% → 65%/35%) — that instance was in the directory and never in the table.

**Claim that had to be weakened.** The old caption + following paragraph said the
bottleneck migrates from transport to cranes at the energy extreme "consistently across
all instances." On v2 that is false: it holds on SD-5 (17→33%), SD-10 (0→35%) and
SD-10-C (17→35%), and NOT on SD-8 (14→18%) or L07 (11→6%), where the energy extreme just
stretches the same transport chain. Rewritten to state migration as an instance-level
property the attribution has to be read to establish. The transport-dominance of the
*makespan* extreme does hold everywhere (83–100%).
Note this is a per-instance/extreme statement and is NOT in tension with §sec:pts, which
reports migration ≥0.5 on 9/11 instances under a different metric (1 − Jaccard of the
top-3 *tasks*, not the transport/QC activity share).

### ★ NEW: two front-learning structural holdouts were never reported
`front_learning/results_holdout_qc5_smallN.json` and `results_holdout_qc235out.json` test
**grouped fleet-structure holdout**, which LOIO does not.
- Hold out a whole crane count (train 2–6 QC, test the unseen 5-QC instances + L07):
  test MAE(ρ) **0.113**, r **0.44** (train 0.049 / 0.87).
- Also remove the small-fleet end (train 3–6 QC, test contains 2-QC instances *below* the
  trained range): MAE **0.158**, r **−0.01**. Damage is concentrated on the out-of-range
  instances — toy:24:2:2 0.242, toy:40:2:3 0.237, vs 0.113–0.161 in-range.
Conclusion added to the paper as amortisation limitation (iii): **R4 transfer is
interpolative in fleet structure**, not extrapolative.

### Verified clean (no action needed)
- All 11 `fused_tape_guided/tcs_frontier_*.json` — every migration/concentration pair
  matches `tab:pts` and both `fig:r4` panels exactly.
- `front_learning/`: `loro_real_results` (0.048 saturated), `loro_composition_proof`
  (0.107 vs 0.289, 17/20, r=0.945), `loro_baseline_comparison` (14/35),
  `loro_pertask_results` (AUC 0.529), `front_stability` (0.048 mean within-front std,
  80% below 0.06) — all already in §sec:amortise.
- `experiments/benchmark_results.json` (top level) — N=5, 10 seeds, superseded sweep,
  correctly not incorporated.
- `critpath_coupled_toy10_v2.json` makespan-extreme Jaccard 0.111 — already reported as a
  limitation at the end of the coupled section.

Commits: `a592ef2` (worked-example v1→v2 fix), `a52e092` (structural holdouts).
Structure re-verified after both: 10/10 figure, 17/17 table, 11/11 tikzpicture, 9/9 axis,
20/20 tabular, 5/5 itemize, 2/2 enumerate, 20/20 equation, zero dangling refs.

### Sweep status: COMPLETE
Every directory under `experiments/` has now been checked against `paper/main.tex`.
The "Still open" list above is unchanged by this pass.
