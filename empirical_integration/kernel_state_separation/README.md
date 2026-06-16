# Kernel state separation

Distributional state-separation tests (MMD + energy distance + permutation + bandwidth
sensitivity) applied **only** to real Tier 1/Tier 2 matrices. Current eligible input:
`Li_ST002477` metabolomics (287 metabolites × 75 biological samples; Control/Mild/Severe).

Question: *do Control, Mild and Severe occupy distinguishable metabolomic state distributions?*
Not: "which metabolite is a biomarker". See `KERNEL_STATE_SEPARATION_POLICY.md` for the claim ceiling.

## Files
- `KERNEL_STATE_SEPARATION_POLICY.md` — eligibility + claim ceiling
- `KERNEL_INPUT_REGISTRY.tsv` — eligible matrices (with provenance/QC)
- `KERNEL_ANALYSIS_STATUS.tsv` — per-step gate status
- `KERNEL_TEST_RESULTS.tsv` — consolidated test results
- `KERNEL_VALIDATION_REPORT.md` — final separation verdict
- `scripts/` — 01 prepare, 02 MMD, 03 energy distance, 04 sensitivity/validation
- `outputs/` — prepared matrix, per-method results, sensitivity summary

## Run
```
python scripts/01_prepare_li_metabolomics_kernel_input.py
python scripts/02_mmd_two_sample_tests.py
python scripts/03_energy_distance_tests.py
python scripts/04_kernel_sensitivity_report.py
```
stdlib + numpy + scipy. Permutations use a fixed seed for reproducibility. If the real matrix is
absent, scripts record `MISSING_REAL_MATRIX` / `KERNEL_ANALYSIS_BLOCKED` and fabricate nothing.
