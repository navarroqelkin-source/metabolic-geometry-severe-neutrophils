# SIMULATION_DESIGN_MAP_FREEZE_NOTE

**Status: FROZEN for Frontiers submission.**

The simulation-design map has been accepted only as supplementary material. It evaluates measurement-design
identifiability under known latent truth and does not estimate biological parameter values or patient
mechanisms in public datasets. No further simulation expansion is planned before Frontiers submission.

## Scope, locked
- Decision: `GO_SUPPLEMENT_ONLY` (see `SIMULATION_DESIGN_MAP_GO_NOGO.md`).
- Frozen artifacts:
  - `SUPPLEMENTARY_NOTE_SIMULATION_DESIGN_MAP.md`
  - `figures/Supplementary_Figure_simulation_design_map.svg` (+ PDF/PNG in `figures/final_exports/`)
  - `modeling/measurement_design_map/` (code + outputs)
  - one short paragraph in v0.8 Discussion (abstract unchanged; Figures 1–7 untouched).

## Frozen — do NOT do before submission
- Do not expand the simulation or add new generator/recoverer variants.
- Do not move the Supplementary Figure into the main text or make it a main figure.
- Do not add ABM, a disease simulator, or any biological-parameter / clinical / causal / biomarker /
  predictive claim.
- Do not modify Figures 1–7 or the abstract (abstract only on explicit PI instruction).

## Future-programme note (not for this submission)
Further development of the measurement-design / recovery analysis (richer generators, parameter-recovery
intervals, broader robustness) belongs to the future programme / M0, not to the v0.8 Frontiers submission.
