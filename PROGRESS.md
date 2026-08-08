# Project Progress & Forward Plan — E-HGATv2 Paper

**Last updated:** 2026-06-30
**Purpose:** Authoritative tracker of what is *established by benchmarks*, what is *ambiguous / needs more runs*, what is *open*, and the prioritized plan to advance rigorously.

> **Strategic note (2026-06-30):** Sections 1–7 track the *OR-paper* state. **Section 8 is the reframe-and-elevate plan** that turns this into a TMLR/ICLR-grade **ML interpretability** paper — what to *add*, how to *position* it, the venue/timeline strategy for Fall MS admissions, and the precise honesty constraints. The two are the same body of work. **If the goal is publication, §8 is the live plan.**

---

## 1. SOLID — established by benchmarks, in the paper

| Result | Evidence | Status |
|---|---|---|
| **R2 uncoupled** — variable→objective attribution (AGV speed, crane workload, dispatch order) | `critpath_*_v2.json`: 4 instances (SD-5/8/10, L07), all 8 traversals Jaccard = **1.000**; real speeds/distances/QC IDs in paper | ✅ Solid |
| **TAPE faithfulness (uncoupled)** | `tape_bench_*_unc.json`: leg-Jaccard 0.95–0.98, makespan abs err 11s (toy10) | ✅ Solid |
| **Fidelity study (uncoupled)** | `fused_eval_unc_*`: R²=0.997–0.998, Jaccard=0.98–0.99, 20 seeds, N=6–50 | ✅ Solid |
| **Attention ≠ explanation** | Spearman ρ ≈ 0 (−0.09 to +0.09) across coupled/uncoupled; TAPE ρ high | ✅ Solid, well-supported |
| **R3 optimization vs weak baselines** | `paper_stats.json`: TAPE beats mp-BRKGA, single-pop BRKGA, NSGA-II(random) on HV; Friedman p=8e-6, Holm-corrected | ✅ Solid *vs those baselines* |

---

## 2. AMBIGUOUS / WEAK — claims NOT yet established, need more runs or reframing

### 2.1 ⚠️ R3 headline is statistically weak vs the attention variant
- **Finding:** On HV ratio, `E-HGATv2-TAPE` avg rank = **1.91**, but `E-HGATv2-attn` = **1.45** (attention ranks *better*). TAPE-vs-attn Wilcoxon **p = 0.067 (NOT significant)**, Cliff's δ = −0.21 (small).
- **Implication:** We cannot currently claim "TAPE guidance optimizes better than attention guidance." The defensible claim is narrower: *both GNN-guided variants beat classical baselines; TAPE adds faithful explanation at no optimization cost.*
- **Options:** (a) reframe the claim honestly (recommended, cheap); (b) raise seeds 5→20+ to test if separation emerges; (c) add IGD+/GD+/spread as the primary lens if TAPE wins there. **Decision needed.**

### 2.2 ⚠️ Coupled makespan-extreme critical-path recovery is broken
- **Finding:** `critpath_coupled_toy10_v2.json` makespan-optimal Jaccard = **0.111** (energy-optimal = 1.000). The v2 rerun (unroll=4, 2000 samples) produced **identical** R² (0.898) and Jaccard — **the "fix" did nothing.**
- **Context:** Front-*averaged* coupled fidelity is fine (leg-Jaccard 0.95 toy10 / 0.87 toy20). The failure is specifically at the **makespan extreme**, where all AGVs run at max speed → maximum power contention → hardest DP point.
- **Options:** (a) honestly scope as a stated limitation + report front-averaged Jaccard, not the extreme (recommended baseline); (b) investigate root cause — is it sampling (few training schedules near the makespan extreme), unroll depth, or a genuine surrogate-accuracy ceiling? (c) try targeted sampling weighted toward high-speed schedules. **Decision needed: explain-and-scope vs invest in a fix.**

### 2.3 ✅ R4 (front-behaviour learning) — amortization PROVEN on a composition-diverse set (2026-06-27)
**Bottom line:** R4 amortizes critical-path composition across instances with **between-instance corr 0.945** — but *only demonstrably so on a set that actually spans the composition spectrum.* The real benchmark looked like a failure purely because it is transport-saturated (no variance to predict).

- **Original failure:** train corr 0.93 / test corr **−0.49** on a single held-out L07. Two bugs fixed in `scripts/run_front_learning.py`: hardcoded features (num_qcs frozen at 3, num_agvs faked as N/2) and zero structural diversity (all training qc=3). Pipeline re-architected for per-instance caching + core-parallel fan-out (`compute_front_cache.sh`).
- **Real benchmark (LORO, 35 instances, `loro_real_results.json` / `loro_baseline_comparison.json`):** held-out MAE 0.048 — but a constant-mean predictor (≈0.88) *also* gets 0.048; model beats it on only 14/35. **Not because it can't learn — because there is nothing to learn:** critical paths are transport-dominated everywhere (transport_frac **0.88 ± 0.04**, 87% of front points > 0.80). Saturated target ⇒ constant is unbeatable. (Caught only after adding the baseline check; the first "MAE generalizes" reading omitted it.)
- **Proof on a composition-diverse set (`loro_composition_proof.py` / `loro_composition_proof.json`):** 20 synthetic instances, fleet/crane ratios tuned to span QC-bound→transport-bound (`num_agvs` high + few cranes ⇒ QC-bound; few AGVs + many cranes ⇒ transport-bound). Achieved composition spread **std 0.29, range 0.19–0.99**. Leave-one-instance-out:
  - **MODEL MAE 0.107 vs naive-constant MAE 0.289** (improvement +0.182, 2.7×); model beats constant on **17/20**.
  - **Between-instance composition recovery corr(pred_mean, true_mean) = +0.945** — the predictor reads structure and tells QC-bound (0.19) from transport-bound (0.99) on held-out instances.
- **Honest limitations (kept):** (i) *within-front* λ-ordering recovery is weak/mixed-sign — fronts are relatively flat *within* an instance, so the fine ordering is noisy. (ii) **Per-task criticality** (which *specific* task is critical) is NOT predictable from static task features: LORO AUC 0.529 ≈ chance, *worse* than a λ-only baseline (`loro_pertask_results.json`) — criticality is set by the realized schedule, not static attributes. (iii) Synthetic→real transfer is weak (L07 corr −0.34); the proof is synthetic→synthetic with held-out *structure*.
- **Paper framing:** R4 amortizes instance-level critical-path composition from structure (corr 0.945) — the "search→knowledge" loop works when composition varies. Report the transport-saturation of the real Table-5 instances as *why* a single real held-out looks flat, not as a method failure. **P1 resolved.**

### 2.4 ⚠️ Uneven seed counts undercut rigor
- Optimization benchmarks (`tape_bench_*`, `paper_stats`): **5 seeds**.
- Fidelity study: **20 seeds**.
- Coupled optimization coverage: only **toy:10, toy:20** (2 instances, 5 seeds each).
- Mismatch invites reviewer pushback. Optimization claims rest on the thinnest sampling.

---

## 3. OPEN PROBLEMS — ranked by value × tractability

| # | Problem | Value | Effort | Recommendation |
|---|---|---|---|---|
| **P1** | R4 generalization (§2.3) | **Highest** — core contribution | ~~Medium~~ | ✅ **RESOLVED** — amortization proven on composition-diverse set (between-instance corr 0.945, beats constant 17/20). Real benchmark flat only because transport-saturated. |
| **P2** | R3 claim weak vs attn (§2.1) | High — headline integrity | Low | **Reframe + more seeds** |
| **P3** | Coupled makespan extreme (§2.2) | Medium — honesty/robustness | Low–Med | **Scope as limitation; optional root-cause probe** |
| **P4** | Seed sweep (§2.4) | Medium — reviewer-proofing | Low (compute) | **20+ seeds where it matters** |
| **P5** | Commit fleet-scaling work | Plumbing for P1 | Trivial | **Verify tests, commit** |

---

## 4. FORWARD PLAN

### Phase A — Land the in-flight infrastructure (prereq for P1)
The uncommitted changes (`scripts/run_benchmark.py`, `benchmark/runner.py`, `environment/instance.py`, `tests/unit/test_instance.py`) add `scaled_fleet(N)`, `build_scaling_instance(...)`, and configurable `--agvs/--qcs`. This is exactly the lever P1 needs (vary QC/AGV counts).
- [ ] Run `pytest tests/unit/test_instance.py` and full unit suite — confirm green.
- [ ] Sanity-check `scaled_fleet` policy (AGVs/QCs per N) and `AVAILABLE_QCS` bound (≤ cranes in distance matrix).
- [ ] Commit on a branch.

### Phase B — Fix R4 generalization (P1) — the main scientific work
**Hypothesis:** R4 failed because of zero structural diversity in training (all qc=3). A training set spanning QC counts {2,3,…}, AGV counts, and N should let the predictor learn the *structural* mapping, not memorize 3-crane fronts.
- [ ] Build a diverse instance set with `build_scaling_instance` — vary N, num_qcs ∈ {2,3,4,…}, num_agvs.
- [ ] Regenerate `front_data.json`: NSGA-II front + per-solution TAPE composition per instance.
- [ ] **Leave-one-structure-out evaluation** — hold out a QC count entirely, test generalization to unseen structure (the honest test).
- [ ] Possibly enrich instance features (currently num_tasks/agvs/qcs/handling stats) — but first see if diversity alone fixes corr.
- [ ] **Success criterion:** held-out corr ≳ 0.7 and MAE ≲ 0.08. If it still fails, that is itself a publishable finding (front structure is instance-specific; amortization has limits) — report honestly.
- [ ] Write R4 results section with the leave-one-out table.

### Phase C — Repair the R3 narrative (P2)
- [ ] Rewrite the optimization claim to what the data supports: GNN-guided (both TAPE & attn) > classical baselines; TAPE matches attn on HV **and** adds faithful, exact explanation (the differentiator).
- [ ] Raise optimization seeds 5→20 on at least the core instances; re-run `compute_paper_stats.py`; check whether TAPE/attn separation emerges on any metric.

### Phase D — Coupled honesty pass (P3)
- [ ] In the paper, report coupled **front-averaged** Jaccard (0.95/0.87) as the headline; explicitly state the makespan-extreme degradation (0.11) as a scoped limitation with the power-contention mechanism.
- [ ] *Optional probe:* diagnose whether targeted high-speed-schedule sampling lifts the extreme. Time-box it; do not block the paper.

### Phase E — Seed sweep & finishing (P4)
- [ ] 20+ seeds on scaling + tape_guided; refresh CIs.
- [ ] **Implementation & reproducibility appendix (REQUIRED for TMLR/workshop checklist):**
  - [ ] Body: add ~2 sentences naming the tropical layer as a custom `torch.autograd.Function` with a hand-derived backward (forward caches per-node argmax arc; backward routes the cotangent along the cached critical path → Eq. `tapechain` exactly, not via generic autodiff). Reference App. B. Mention the batched variant.
  - [ ] Create Appendix B: hyperparameter table (GATv2 layers/hidden dim/heads, projection & readout heads, optimizer/lr/wd/epochs=50/batch — from `src/ehgat/surrogate/train.py`), trainable-param count, PyTorch/PyG versions.
  - [ ] Add hardware + wall-clock-per-instance row (needs one timed VM run to fill; placeholder until then).
  - [ ] Do NOT paste the `backward()` source in the main body — appendix/repo only.
- [ ] Recompile paper, verify all pgfplots/TikZ render, table-overflow check.
- [ ] Final proofread.

---

## 5. DECISIONS NEEDED FROM USER (before/while executing)
1. **R3 reframe (§2.1):** accept the honest narrower claim, or invest seeds to chase TAPE>attn significance?
2. **Coupled extreme (§2.2):** scope as a limitation (fast), or invest in a root-cause fix attempt?
3. **R4 scope (§2.3/Phase B):** is "leave-one-QC-count-out generalization" the right bar, or a different held-out axis (N? handling-time regime?)?
4. **Compute budget / VM:** VM is ephemeral — Phase B regeneration + Phase C/E seed sweeps are the compute-heavy steps; sequence them before VM teardown and rsync+commit all artifacts.

---

## 6. DATA LOCATIONS
| Artifact | Path |
|---|---|
| R2 worked examples (v2) | `experiments/critical_path_demo/critpath_*_v2.json` |
| R2 coupled (v1+v2, extreme=0.111) | `experiments/critical_path_demo/critpath_coupled_toy10*.json` |
| R4 front-learning (FAILS generalization) | `experiments/front_learning/front_learning_results.json`, `front_data.json` |
| Optimization benchmark + stats | `experiments/fused_tape_guided/tape_bench_*.json`, `paper_stats.json` |
| Coupled optimization (toy10/20, 5 seeds) | `experiments/fused_tape_guided/tape_bench_toy{10,20}_pp30.json` |
| Fidelity (coupled 20 seeds) | `experiments/fused_eval/fused_eval_coupled_pp30_gnn_predicts_legs.json` |
| Fidelity (uncoupled 20 seeds) | `experiments/fused_eval/fused_eval_unc_c3_gnn_predicts_legs.json` |
| TCS frontier | `experiments/fused_tape_guided/tcs_frontier_*.json` |
| Paper source | `paper/main.tex` |
| R4 script | `scripts/run_front_learning.py` |
| Fleet-scaling infra (uncommitted) | `src/ehgat/benchmark/runner.py` (`build_scaling_instance`, `scaled_fleet`) |

---

## 7. VM
```
ssh -p 24520 root@154.42.3.37 -L 8080:localhost:8080   # alias: ehvm
Repo: /workspace/e-hgatv2   Env: uv-managed .venv (torch 2.12.1+cu130)
Hardware: 255 cores, 2× A40 (49 GB). Python 3.12.
```
⚠️ Ephemeral — rsync results to local and commit before teardown.
**Parallelism:** fan independent per-instance jobs across cores with `xargs -P`
(`scripts/run_front_parallel.sh`). GPU does NOT help the front-learning pipeline —
it is CPU-bound on simulator sample generation, not GNN gradient steps.

---

# 8. PUBLICATION PLAN — making this TMLR/ICLR-grade (the live plan)

**Last reviewed:** 2026-06-30. Owner-facing decisions flagged ⟶.

## 8.0 The reframe (do this first — it costs nothing and changes everything)
The publishable contribution is **NOT the scheduling/OR machinery**. It is the **ML interpretability finding about attention**. The OR problem is demoted to *the apparatus that happens to supply an exact ground truth*. Concretely:

- **Thesis (what the paper is about):** *In models whose decision is governed by a structured (tropical / max-plus) inference layer, an **exact** attribution to the decision-determining structure exists for free — the gradient of that layer (TAPE). Using it as ground truth, learned **attention is not faithful** to the decision structure, even though it is **useful** for the downstream task. Usefulness and faithfulness are **dissociable**, and here we dissociate them.*
- **Headline = the DISSOCIATION, not the bare falsification.** "Attention is unfaithful" is a 2019 debate (Jain–Wallace ↔ Wiegreffe–Pinter) and reviewers have seen it; *table stakes*. What is fresh: (a) a setting with **exact ground truth** (NLP never had one), and (b) the **dissociation** — attention guides search as well as the exact signal yet encodes none of the critical-path structure; the search benefit comes from **screening, not targeting** (the ablation in `screening_ablation.py`).
- **Drop from the thesis/abstract/intro:** quay cranes, AGVs, makespan/energy, NSGA-II, MILP. Keep them **only** inside the experimental-apparatus section. The title/abstract should read as an interpretability paper (e.g. *"Faithful Attributions for Learning-Augmented Combinatorial Optimization via Tropical Objective Layers"* or a cleaner attention-faithfulness framing).
- **Never sell TAPE's exactness as the discovery** — it is *definitional* (gradient of a closed-form DP = its optimal path). The contribution is the **falsification + dissociation that the exact oracle enables**. Leading with "our attribution is exact" invites the fatal *"physics solving physics / circular"* critique.

## 8.1 The three holes that block TMLR acceptance (must-do)
A careful reviewer sinks the current single-architecture, single-domain result on exactly these. All three reuse the existing ladder (`scripts/attention_ladder.py`) + 20-seed stats harness — they are **additive experiments, not a rewrite**.

| # | Hole | Why it sinks the paper | Fix | Effort |
|---|---|---|---|---|
| **H1** | **Single architecture.** All evidence is the one GATv2 surrogate. | Reviewer: *"you've shown **this attention** is bad, not **attention**."* Subject of the claim is unproven. **Biggest hole.** | Add a **2nd attention architecture** (transformer-style attention encoder over the *same* node features → same per-task attention vector, plugged into `attention_per_task`'s slot). Show the unfaithfulness reproduces. | ~2–4 days; reuses entire ladder/evaluator/stats |
| **H2** | **Attention read-out confound** (the whole Wiegreffe–Pinter rebuttal). | Reviewer: *"which layer/head? raw vs rollout vs gradient-weighted? did you try the others?"* One readout = one cherry-pick. | Report **≥4 readouts** — last-layer, mean-over-heads, max-over-heads, attention-rollout, gradient×attention — and show the ρ≈0 / AUC≈0.5 result is **invariant** across all. Implement as a `mode=` arg through the same ladder. | ~1–2 days |
| **H3** | **Single domain / small N.** toy:5–20 + L-instances is thin and OR-only. | *"Case study, not a phenomenon. Niche OR toy."* | Add a **second, unrelated DP domain: Viterbi/CRF** sequence labeling (see §8.3). Two structurally unrelated DPs from two fields ⇒ "phenomenon" bar cleared. | ~2–3 weeks (see breakdown) |

**Until H1 exists, claims MUST stay scoped** to "our tropical-DP surrogate," not "attention" universally. TMLR rejects *unsupported* claims, not *narrow* ones — but the narrower the claim the more a reviewer questions significance, so H1+H2 are what license broadening to "attention."

## 8.2 Non-issues (de-catastrophized — do NOT spend effort here)
- **"Large N breaks MILP" is irrelevant to the headline.** The faithfulness oracle is the **O(N) exact critical path of a *given* schedule** (`critical_path_binding`), cheap at any N. MILP solves for the *optimal schedule*; the faithfulness experiment evaluates attention against the critical path of *whatever schedule the decoder emits*. Run the ladder at N=50/200/1000 freely. MILP only ever mattered for (a) **evaluator validation** — already done vs brute force at N=5, exact-by-construction above that; (b) **true-Pareto-front benchmarking** — at large N use the **high-budget reference-front proxy** already in `screening_ablation.py` (`reference = _pareto(pool)`), the accepted MOO standard (`log()` that it's a proxy).
- **Viterbi does NOT make this a "significantly more complex project."** It doubles the *surface area* (a parallel `seqlabel/` subpackage + NLP deps) but **not the conceptual difficulty** — the exact oracle, the ladder, and the stats are already built and reused. New code is a model + a dataset loader + a ground-truth-attribution wiring.

## 8.3 Viterbi/CRF second domain — detailed work breakdown
Viterbi **IS** a tropical (max-plus) DP, so it is conceptually native: TAPE = gradient of the Viterbi score; the **Viterbi-decoded path = the "critical path."** This ports the experiment onto the **home turf of the attention-explanation debate**, with a ground truth that turf never had.

| Piece | Effort | Notes |
|---|---|---|
| Dataset — CoNLL-2003 NER **or** UD POS via HF `datasets` | ~0.5 day | Standard loader + tokenization |
| Model — transformer encoder + CRF head (`torch-struct` or `pytorch-crf`) | ~3–4 days | **Must train a *decent* tagger** or the faithfulness test is uninteresting (explaining a bad model proves nothing) |
| Ground truth — Viterbi path + gradient-of-score = TAPE | ~3–4 days | **The one genuinely tricky bit:** define per-token criticality fairly (on-path indicator + graded marginal sensitivity). `torch-struct` gives the differentiable DP, so the gradient is free; the care is in the *definition* and a fair attention-vs-TAPE comparison |
| Attention readout (reuse H2 variants) | ~1 day | Transformer self-attention already exists; same pooling modes |
| Wire into ladder + 20-seed stats | ~1 day | `attention_ladder.py` reused: swap `attention_per_task`→token attention, `critical_path_binding`→Viterbi path, `marginal_makespan_speedup`→potential gradients |

**Realistic total: ~2–3 weeks** focused (~1.5 if the tagger trains cleanly first try). Complexity = a **new parallel subpackage** (`ehgat/seqlabel/` or a sibling), new deps (HF + a CRF lib), **zero disturbance to existing scheduling code** — shares only the ladder + stats utilities. Main risks: (i) tagger quality, (ii) defensible CRF ground-truth definition, (iii) fair attention comparison — all *thinking-hours*, not line-count.

⟶ **Decision:** confirm dataset choice (CoNLL-2003 NER recommended — cleanest, most-cited in the attention debate) and CRF lib (`torch-struct` recommended — gives differentiable Viterbi + backward for free).

**Optional 3rd DP domain** (diminishing returns; only if a spare ~1–1.5 wk before deadline): sequence alignment / edit distance (Needleman–Wunsch) or DTW — also tropical, ground truth = exact alignment path, runs on synthetic data (no dataset curation), but still needs a learned attention-aligner (the model cost recurs). Reviewers credit "≥2 independent domains" heavily; the 2→3 jump is much smaller than 1→2. **Recommendation: skip unless time permits; 2 domains clears the bar.**

## 8.4 ICLR-only extras (skip for TMLR — TMLR doesn't gate on novelty)
ICLR rejects on **novelty/significance**; the topic fights you regardless of execution. To move ICLR from ~40% → ~50%:
1. **Positive reframe** — from negative *"attention unfaithful"* to a *lens*: *"models with structured-inference layers already contain an exact, free attribution; the field reaches for attention out of habit — here is the general construction and two demonstrations."* A lens is rewarded; a negative finding is discounted.
2. **One constructive payoff** (~+1 wk) — show TAPE *does something attention can't*: repair rationale extraction on the CRF task, or **catch a spurious correlation / bug** attention misses, or a faithfulness-certified explanation. Negative-**plus**-constructive >> negative-only. **Single highest-leverage ICLR move.**

## 8.5 Venue + timeline strategy (Fall MS admissions: deadlines mid-Dec 2026 → mid-Jan 2027)
**Decisive timing fact:** *ICLR 2027 decisions land ~late January 2027 — AFTER most deadlines.* So a Sept ICLR submission is only ever **"under review"** in-window. **TMLR is the only venue that can become an actual acceptance in-window** (rolling, ~2-month first decision; **no page limit** so 12+ pages is fine — speed is governed by **revision rounds, not length**).

**Plan:**
- **Primary: TMLR.** Submit **early September** (not late — every week earlier buys a revision round inside the window). Keep **main body ~9–10 pp + appendix-load the breadth** (Viterbi details, readout tables, per-instance numbers, reproducibility) so it *reviews like a short paper*. Scope claims conservatively to force **minor-not-major** revisions.
- **Parallel: a NeurIPS 2026 workshop** (interpretability / XAI / structured prediction). Workshop deadlines ~Sept → notification ~Oct → present Dec. This is the **guaranteed in-window credential**; TMLR is the publication upside.
- **By mid-December you can truthfully state:** *"Accepted, NeurIPS 2026 workshop [name]; under review at TMLR (public reviews)."* Stronger for MS admissions than "under review at ICLR" (yours includes an actual acceptance).
- **ICLR:** optionally submit as a *free upside option* (public OpenReview reviews are themselves a credential), but it cannot finalize in-window — do not rely on it. Can also re-target a later ICML/ICLR after admissions, or post to arXiv.

**Odds with the full package:** **TMLR ~70–80%** (clears rigor/scope, the only axis TMLR judges); **ICLR ~35–45%** (~45–55% only with §8.4 reframe + constructive payoff). Strategy: **TMLR is the floor, the workshop is the certainty, ICLR is the lottery ticket.**

## 8.6 Calendar (~10 weeks: late-June → early-Sept submission)
| Window | Work |
|---|---|
| **now → mid-July** | Lock scope/title (§8.0); stand up Viterbi/CRF stack (HF + `torch-struct`); run scheduling **H1 (2nd architecture) + H2 (readout robustness)** sweeps on VM |
| **mid-July → mid-Aug** | Viterbi/CRF: train tagger, build ground-truth attribution, run ladder + 20-seed stats (§8.3) |
| **mid-Aug → early-Sept** | Integrate; final 20-seed stats across both domains; **rewrite framing to interpretability thesis**; main-body tighten + appendix-load; proofread |
| **early Sept** | Submit **TMLR + NeurIPS workshop** (same core paper) |
| **Oct** | Workshop notification → **in-window acceptance locked** |
| **Nov–Dec** | TMLR first decision / one revision round |

## 8.7 Carry-over OR-paper items still required (from §§2–5) — fold into the above
These pre-existing TODOs are *prerequisites* for the elevated paper, not separate work:
- **R3 reframe (§2.1):** the honest claim is *both GNN-guided variants beat classical baselines; TAPE adds faithful explanation at no optimization cost* — this **is** the dissociation headline. Bump optimization seeds 5→20 (matches §2.4).
- **Coupled makespan-extreme (§2.2):** scope as a stated limitation (front-averaged Jaccard headline; report the 0.111 extreme + power-contention mechanism). Do not block on a fix.
- **Seed parity (§2.4):** 20+ seeds everywhere the paper makes a quantitative claim.
- **mp-BRKGA baseline (pre-advisor punch list):** validate-or-caveat the reproduction against published Cmax/E (VM available).
- **a^agv_j equation gap + MILP→ours notation bridge + bibliography placeholder** (pre-advisor punch list) — needed before sending to advisor / submission either way.

## 8.8 Honesty constraints (binding — established with the user)
- Claims stay **scoped** ("our surrogate" / "this tropical-DP setting") until **H1** proves architecture-independence; only then broaden to "attention."
- **Never** frame TAPE's exactness as a discovery — it is definitional; the contribution is the **falsification/dissociation** it enables.
- The **"physics-solving-physics / circular"** critique is fatal to the framing *"our attribution is exact"* and harmless to *"we built a setting with ground truth and used it to falsify a deployed explanation method."* Always lead with the latter + the R2/R3 dissociation, pre-empting the critique before a reviewer raises it.
- Viterbi's honest justification is **positioning** (the debate's home turf), **not** a new epistemic mechanism — do not oversell it as "generalization proof."
- All heavy runs on the **VM**; rsync + commit artifacts before teardown.
