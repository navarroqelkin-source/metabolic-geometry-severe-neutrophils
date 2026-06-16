# SIMULATION_DESIGN_MAP_SPEC

## Purpose
Specify a neutral, in silico **measurement-design identifiability map**: under known latent truth, determine
which measurement breakers reduce which ambiguities that burden-only NET-burden readouts cannot resolve, and
where each measurement fails. This is NOT a competitive benchmark and does not aim to show that any one
design "wins"; it maps what information each measurement adds and what remains unresolved. No ABM, no disease
simulator, no biological-parameter inference in the public datasets.

Central question: *Given known latent truth, which measurement breakers reduce which ambiguities that
burden-only NET-burden measurements cannot resolve?*

## What this analysis can claim
- That, under a known data-generating process, burden-only readouts collapse distinct latent mechanisms.
- That specific added measurements reduce specific ambiguities, quantified by an ambiguity-reduction metric.
- That no single measurement resolves the full latent space, and that some regimes remain unresolved
  (failure/blind-spot zones) — a result is suspect if it shows no failure mode.

## What this analysis cannot claim
This in silico analysis evaluates measurement-design identifiability under known latent truth. It validates
neither biological parameter values nor patient mechanisms in the public datasets.
Synthetic data are used only as a supplementary illustration of method/design behavior, not as a biological result.
No claim of disease mechanism, clinical utility, biomarker validity, clinical prediction, or executed
biological function is made; simulated parameters are not biological parameters.

## Latent processes
- `F` = NET formation / production flow.
- `k` = effective removal = degradation + clearance (so `k` aggregates both; persistence ≈ 1/k).
- `B` = accumulated NET-associated burden (stock).
- `K_R` = detectability / observation gain (composition-dependent).
- `V` = viability / cell availability (NET-forming capacity).
- `G` = downstream effector / functional-execution readout (latent).
- Latent truth is set by the generator; it is never inferred from the public datasets.

## Observable burden
- `Y = K_R · B + noise` (cross-sectional), and optionally a sparse time-course `Y(t_i)`.

## Candidate measurement breakers (evaluated neutrally)
- `M0` burden-only; `M1` + formation assay; `M2` + serum degradation/clearance assay; `M3` + time-course/
  decay; `M4` + viability; `M5` + functional execution readout; `M6` + detectability calibration;
  `M7` combined minimal panel. `M7` is reported as an informationally-necessary combination only if the map
  shows it, not as a preferred "winner".

## Ambiguities to test
- `A1` high formation vs low clearance (the core F-vs-k ambiguity).
- `A2` true burden vs high detectability (`K_R`).
- `A3` persistence vs ongoing production.
- `A4` viable NET-forming capacity vs accumulated released material.
- `A5` burden vs functional execution (downstream effector output).

## Data-generating model (deliberate mismatch to the recoverer)
`dB/dt = F(t) − k_eff(B, subject)·B + P`, `Y = K_R(subject)·B + noise`, with richer-than-recoverer elements:
- saturable removal, e.g. `k_eff(B) = k0 / (1 + alpha·B)`;
- heterogeneous persistence / subject-level variability in `F`, `k0`, `K_R`;
- multiplicative / non-Gaussian (lognormal) noise;
- irregular / sparse sampling.
The recoverer must NOT use the same saturation function.

## Recovery / identifiability assessment
- Recoverer = a simpler minimal stock-flow model (`dB/dt = F − k·B`, linear removal).
- `M0`: characterise the burden-only identifiability ridge (which latent combinations fit equally well; only
  `F/k` is constrained at steady state).
- `M1…M6`: add one breaker as a constraint and recover `F` and/or `k` (or classify formation-dominant vs
  clearance-limited); `M7`: minimal combination.
- Generator ≠ recoverer guarantees the assessment is not tautological.

## Metrics
- Parameter-recovery error: bias and RMSE for `F`, `k` (and `K_R` where applicable).
- Classification accuracy for formation-dominant vs clearance-limited profiles.
- **Ambiguity-reduction score** = reduction in the volume of the compatible latent-parameter set after adding
  a breaker (relative to `M0`), per ambiguity. Metric must not be constructed to favour any single breaker.
- Failure characterisation: minimum number of time points and noise tolerance at which recovery degrades.

## Robustness checks
- Sweep noise level, number/irregularity of time points, and subject-level `K_R` variation.
- Report at least one regime where a breaker fails (blind spot). Absence of any failure mode is treated as a
  red flag (possible circularity / overfit to the generator).

## Figure candidate
- Only if results are clean: `Figure8_measurement_design_identifiability_map.svg` (Panel A burden-only
  collapse; B latent truth + compatible ridge; C breaker-specific ambiguity reduction; D honest map of which
  measurement resolves which ambiguity and what remains unresolved). Otherwise a supplementary figure. Do not
  touch Figures 1–7.

## Decision gate
After the prototype, record GO_MAIN_TEXT / GO_SUPPLEMENT_ONLY / ROADMAP_ONLY / NO_GO in
`SIMULATION_DESIGN_MAP_GO_NOGO.md`. Hard time gate: 72 h prototype, 5 days max to an integrable version; if no
clean result, it does not enter the Frontiers submission. The piece must show at least one failure/blind spot
to be acceptable. No self-preferential benchmark; claim guards must pass both validators.
