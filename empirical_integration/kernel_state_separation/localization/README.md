# Localization — Li ST002477 metabolomic state separation

Descriptive, post-hoc localization of the kernel-confirmed distributional separation
(`KERNEL_STATE_SEPARATION_SUPPORTED`). Identifies **candidate** state-associated metabolites and
module-level associations. NOT biomarkers, flux, causality, prediction or executed function.

Allowed claim: *Severity is associated with robust distributional separation of the metabolomic
state; selected metabolites and modules may contribute descriptively to this separation.*

## Files
- `LI_ST002477_FEATURE_CONTRIBUTION_POLICY.md` — descriptive-only policy
- `LI_ST002477_LOCALIZATION_STATUS.tsv` — per-step status
- `LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv` — per-metabolite Kruskal/FDR/Cliff's/pattern
- `LI_ST002477_MODULE_LEVEL_SUMMARY.tsv` — module-level descriptive support
- `LI_ST002477_LOCALIZATION_REPORT.md` — interpretive summary with inferential limits
- `scripts/` — 01 contribution, 02 bootstrap stability, 03 module summary, 04 validation
- `outputs/` — results tables + validation report

## Run
```
python scripts/01_feature_contribution_by_permutation.py
python scripts/02_bootstrap_feature_stability.py
python scripts/03_module_level_metabolic_summary.py
python scripts/04_validate_localization_claims.py
```
Rank-based stats on the real intensities (75 biological samples). statsmodels BH-FDR. Fixed seed.
