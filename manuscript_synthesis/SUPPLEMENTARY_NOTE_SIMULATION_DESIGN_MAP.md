# Supplementary Note: In silico measurement-design map

This in silico analysis evaluates measurement-design identifiability under known latent truth; it does not
estimate biological parameter values or patient mechanisms in the public datasets. Synthetic data are used
only as a supplementary illustration of method/design behaviour, not a result. No claim of disease
mechanism, clinical utility, biomarker validity, clinical prediction, or biological function is made.

## Purpose
To make the measurement-breaker logic operational: given known latent truth, which additional measurements
reduce which ambiguities that a burden-only NET-burden readout collapses, and where does each measurement
fail? The aim is an honest map of what information each measurement adds — not a demonstration that any one
design is best.

## Data-generating model
A minimal stock model with deliberately richer-than-recoverer structure. NET-burden stock `B` accumulates
from formation `F` and is removed at a saturable effective rate `k_eff(B) = k0/(1 + alpha·B)` (with
`alpha = 0.15`); the observed readout is `Y = K_R·B` with lognormal (multiplicative) observation noise, and
an optional sparse/irregular time-course. Additional latents: viability `V` (NET-forming capacity) and a
functional-execution readout `G`. All values are arbitrary units; simulated parameters are not biological
parameters.

## Recovery / identifiability assessment
For each ambiguity, two latent hypotheses are fixed so that they are **burden-equivalent** (identical
expected cross-sectional `Y`), so burden alone cannot separate them. For each candidate breaker, a noisy
observation is classified to the nearer hypothesis by its generator-expected observable (log-space distance)
using only the measurements that breaker provides. This is an information/distinguishability test between two
fixed known truths — not a parametric fit of the generator to itself — so it is not circular in that sense;
rigour comes from burden-equivalent hypotheses, partial observables and noise. Score = 2·(accuracy − 0.5),
in [0,1] (0 = indistinguishable from burden alone, 1 = resolved).

## Candidate measurement breakers
M0 burden-only; M1 + formation assay; M2 + serum degradation/clearance assay; M3 + time-course/decay;
M4 + viability; M5 + functional-execution readout; M6 + detectability calibration; M7 combined minimal panel
(formation + clearance + detectability + function). M7 is reported as an informationally-complementary
combination, not as a winner.

## Ambiguities tested
A1 formation vs clearance; A2 true burden vs detectability; A3 ongoing production vs persistence (the
formation/removal axis in its persistence framing); A4 viable NET-forming capacity vs accumulated released
material; A5 burden vs functional execution.

## Metrics
Ambiguity-reduction score (above) per (ambiguity × breaker). Robustness reported as the change in score under
higher observation noise and fewer time points. No composite metric is used and no term is tuned to favour a
specific breaker.

## Robustness check
Base: cv = 0.15, four time points. Stress: cv = 0.45 (high noise); two time points. The time-course breaker
(M3) scores 1.00 for A1/A2/A3 at base and **degrades under high noise** (to ~0.78–0.94), a genuine failure
regime; the burden-only null (M0 ≈ 0) and the A4/A5 blind spots are stable across regimes.

## Results
- **Burden-only (M0) resolves nothing** (≈0 across all ambiguities) — a quantitative restatement of the
  central point.
- **Different breakers resolve different ambiguities.** Formation, clearance and time-course each resolve
  the formation/removal axis (A1, A3); a serum degradation/clearance assay, a time-course, or a detectability
  calibration resolve burden-vs-detectability (A2), but a **formation assay does not** (A2, M1 = 0).
- The **combined minimal panel (M7)** resolves the burden-side ambiguities because it covers complementary
  measurements — not because it "wins"; and it still misses A4 (it lacks a viability readout).

## Blind spots
- **Viability (A4)** and **functional execution (A5)** are unresolved by any burden-based measurement; only a
  direct viability readout (M4) resolves A4 and only a direct functional readout (M5) resolves A5. Burden
  recovery never establishes viable forming capacity or executed output.
- No single measurement — including the combined panel — resolves the full latent space.

## Claim ceilings
This analysis evaluates measurement-design identifiability, not biological parameter values or patient
mechanisms. It supports the manuscript's central point that different breakers resolve different ambiguities
while leaving distinct blind spots. It is not a disease simulator, not an agent-based model, not a
self-preferential benchmark, and makes no clinical, causal, biomarker or biological-parameter claim.
Reproducible code and outputs: `modeling/measurement_design_map/` (to be archived with the Zenodo release).
See `Supplementary_Figure_simulation_design_map`.
