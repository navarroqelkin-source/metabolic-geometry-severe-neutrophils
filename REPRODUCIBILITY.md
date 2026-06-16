# Reproducibility

## Environment
Python 3.10; `pip install -r requirements.txt` (numpy, scipy, pandas, matplotlib).
Figure rasterisation used a headless browser + PyMuPDF; this is not required to reproduce the numeric analysis.

## Reproduce
- Claim validators: `python manuscript_synthesis/scripts/validate_*.py` (expect 0 unguarded).
- Metabolic state-separation (Figures 3-4): see `empirical_integration/kernel_state_separation/` (scripts +
  `outputs/` + `localization/`): MMD, energy distance, per-feature FDR / monotonicity / Cliff's delta /
  bootstrap stability, and module-level summary.
- Released-material proteome + PTM (Figure 5): `empirical_integration/chapman_*`.
- Observation model / design map: `modeling/minimal_net_burden_model/`, `modeling/measurement_design_map/`.

## Data
Public source accessions only (ST002477, PXD011796, PXD029046, NeuMap; see README). Raw third-party data are
not redistributed; only derived outputs are included.
