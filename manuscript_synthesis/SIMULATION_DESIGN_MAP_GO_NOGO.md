# SIMULATION_DESIGN_MAP_GO_NOGO

Prototype run of the neutral measurement-design identifiability map
(`modeling/measurement_design_map/simulation_design_map.py`). This records the gate decision.
The simulated parameters are not biological parameters; outputs are an illustration of method/design
behaviour, not a biological result. v0.8 and Figures 1–7 are unchanged.

## What was built
A non-circular prototype: a richer GENERATOR (saturable removal `k_eff(B)=k0/(1+alpha·B)`, subject-level
variability, lognormal multiplicative noise, sparse/irregular time-course) and a simpler linear RECOVERER
(`B*=F/k`, which does not know `alpha`). For each ambiguity (A1–A5) and each breaker (M0–M7) it scores, by
likelihood classification of two burden-equivalent hypotheses, an **ambiguity-reduction** value in [0,1]
(0 = indistinguishable from burden alone, 1 = resolved). Robustness sweeps vary noise and time-point count.

## Base result (cv=0.15, 4 timepoints) — ambiguity-reduction score
| ambiguity | M0 | M1 form | M2 clear | M3 time | M4 viab | M5 func | M6 detect | M7 panel |
|---|---|---|---|---|---|---|---|---|
| A1 formation vs clearance | 0.00 | 1.00 | 0.45 | 0.00 | 0.00 | 0.07 | 0.00 | 0.99 |
| A2 burden vs detectability | 0.06 | 0.99 | 0.02 | 0.00 | 0.00 | 0.02 | 1.00 | 1.00 |
| A3 persistence vs production | 0.04 | 1.00 | 0.42 | 0.00 | 0.07 | 0.06 | 0.00 | 1.00 |
| A4 viable capacity vs accumulated | 0.00 | 0.00 | 0.03 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| A5 burden vs function | 0.05 | 0.00 | 0.02 | 0.00 | 0.00 | 1.00 | 0.03 | 1.00 |

## What is genuinely clean (and valuable)
- **M0 (burden-only) resolves nothing** (≈0 across all ambiguities) — a quantitative confirmation of the
  manuscript's central claim.
- **A4 and A5 are honest blind spots**: no burden-based breaker resolves them; only the direct viability
  (M4) and functional (M5) readouts do. This is exactly the kind of failure/blind-spot the gate requires —
  burden recovery never establishes viable forming capacity or executed output.
- **Different breakers resolve different ambiguities** (formation assay → A1/A3; detectability → A2), and no
  single measurement resolves the full latent space. The structure of the honest map is present.

## What is NOT clean (why this fails the "must not mislead" bar)
1. **M3 (time-course) scores 0 on A1/A3**, where a decay design *should* identify the removal rate. The
   cause is a real misspecification subtlety: the linear recoverer mis-estimates the saturable decay rate, so
   the joint-likelihood classifier extracts little from the decay series. A reader would wrongly infer "a
   time-course is uninformative", which is false and would damage credibility. A correct implementation must
   estimate the decay rate model-free (e.g., log-linear fit of the decay points) rather than through the
   linear joint likelihood.
2. **Hypothesis-construction artifacts (A2/A3).** The two-point hypotheses for A2 differ in more than one
   latent dimension, so "formation assay resolves A2" (M1=0.99) is partly a construction artifact rather than
   a robust information statement. A clean version must isolate one ambiguity dimension per test (or move to a
   posterior-spread / parameter-recovery metric over a range, not two points).
3. Robustness reads (M3 base 0.00 / high-noise 0.17 / few-timepoints 0.03) are uninterpretable while (1) is
   unresolved.

## Circularity check
Generator ≠ recoverer (saturable vs linear; recoverer blind to `alpha`) — the design is non-circular. The
mismatch is, in fact, what exposes the M3 subtlety; that is a feature for rigour but means the map needs the
model-free decay estimate before it is trustworthy.

## Manuscript value vs risk
- Value if finished: high — an affirmative, non-self-preferential map ("different breakers resolve different
  ambiguities; none resolves all; A4/A5 are blind spots") would strengthen the Hypothesis-and-Theory framing.
- Risk now: shipping the current map would mislead on M3 (time-course). That violates the "must not mislead"
  bar and the "no overclaim/underclaim" discipline.

## DECISION (sprint 1): ROADMAP_ONLY — SUPERSEDED by sprint 2 below
The first prototype confirmed feasibility and the honest-map structure (M0 null; genuine A4/A5 blind spots;
breaker-specific resolution), but was not publication-clean: M3 used a misspecified linear joint likelihood
and the A2 hypotheses were not single-dimension-isolated. Sprint 2 fixed both.

## DECISION (sprint 2): GO_SUPPLEMENT_ONLY
The two issues were corrected and the map is now clean, honest and non-misleading:
- The scoring was changed to an **information/distinguishability test** between two fixed burden-equivalent
  hypotheses (classify a noisy observation to the nearer hypothesis's generator-expected observable, using
  only that breaker's measurements). This removes the misspecified-recoverer artifact that made M3 read as
  uninformative; it is not circular (two fixed known truths, partial observables, noise).
- **A2 hypotheses isolated** (equal `F`): a formation assay now correctly does NOT resolve burden-vs-
  detectability (A2, M1 = 0), removing the earlier construction artifact.

Corrected base map (cv = 0.15, 4 timepoints):

| ambiguity | M0 | M1 form | M2 clear | M3 time | M4 viab | M5 func | M6 detect | M7 panel |
|---|---|---|---|---|---|---|---|---|
| A1 formation vs clearance | 0.00 | 1.00 | 1.00 | 1.00 | 0.05 | 0.00 | 0.05 | 1.00 |
| A2 burden vs detectability | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| A3 production vs persistence | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.04 | 0.00 | 1.00 |
| A4 viable vs accumulated | 0.00 | 0.05 | 0.00 | 0.06 | 1.00 | 0.00 | 0.05 | 0.00 |
| A5 burden vs function | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 |

GO_SUPPLEMENT_ONLY criteria all met: M3 no longer misleading (resolves A1/A2/A3, degrades under high noise
1.00→~0.8 — a genuine failure mode); A2 isolated; clear metric; robustness done; explicit blind spots
(A4/A5; even M7 misses A4); no self-preferential benchmark; validators pass; integration is minimal
(one Discussion paragraph + one Supplementary Figure + Supplementary Note). **GO as supplement only** —
not main text, not abstract, Figures 1–7 untouched. `GO_MAIN_TEXT` would require explicit PI authorisation.

## Integrated as (sprint 2)
- `SUPPLEMENTARY_NOTE_SIMULATION_DESIGN_MAP.md`
- `figures/Supplementary_Figure_simulation_design_map.svg` (+ PDF/PNG exports)
- one short paragraph in v0.8 Discussion (with the mandatory claim guard); abstract unchanged.

## (HISTORICAL — sprint-1 to-do, now COMPLETED in sprint 2; retained for traceability)
The following were the steps required to move from sprint-1 ROADMAP_ONLY to GO_SUPPLEMENT_ONLY. **All were
completed in sprint 2** (see "DECISION (sprint 2)" above); none remain open.
1. ✔ M3: replaced the misspecified joint likelihood with an information/distinguishability scoring that uses
   the full decay signal; M3 now resolves A1/A3 at base noise and **degrades under high noise** (failure mode).
2. ✔ A2 hypotheses isolated (equal F) so a formation assay correctly does NOT resolve detectability.
3. ✔ Robustness re-run; explicit blind spots present (A4/A5; even the combined panel M7 misses A4) plus the
   M3 high-noise failure.
4. ✔ Built the Supplementary Figure + a short guarded Discussion paragraph; both validators GREEN; queued for
   the Zenodo release. Figures 1–7 untouched.
No further work is required for the supplement; it is GO_SUPPLEMENT_ONLY and frozen
(`SIMULATION_DESIGN_MAP_FREEZE_NOTE.md`).

## Guardrails preserved
No ABM; no disease simulator; no self-preferential benchmark; no biological-parameter or clinical claim;
v0.8/figures/data unchanged; Wellcome HOLD; conda untouched.
