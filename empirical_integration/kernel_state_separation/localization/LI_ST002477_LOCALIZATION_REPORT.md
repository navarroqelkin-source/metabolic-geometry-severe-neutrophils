> **SUPERSEDED FOR CROSS-PAIR ORDERING.** Do not use this document to compare the relative
> magnitudes of the three clinical contrasts, or to support Control-Severe dominance or
> two-metric agreement. Within-pair statements are unaffected, subject to the limitations in the
> root notice. See [NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md](../../../NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md).

# Li ST002477 — Localization Report

This localization analysis identifies candidate contributors to distributional separation. It does
not identify validated biomarkers, fluxes or causal mechanisms.

## 1. Kernel result (context)
`KERNEL_STATE_SEPARATION_SUPPORTED`: Control/Mild/Severe occupy distinguishable metabolomic state
distributions (MMD + energy distance, permutation p~0.001 across all bandwidths, outlier-stable,
severity-ordered Control–Severe > Control–Mild > Mild–Severe).

## 2. Objective
Descriptively localize which metabolites and modules are associated with that separation —
strictly post hoc, no mechanism.

## 3. Metabolites with strongest descriptive evidence
Rank-based (Kruskal-Wallis + BH-FDR; Cliff's delta Control-vs-Severe), confirmed by bootstrap
stability (top-20 frequency over 500 resamples):
- **Thioproline** (q≈2e-6, δ_CS=+0.92, monotonic_down; top20=0.91)
- **Fucose 1-phosphate** (q≈2e-6, δ_CS=+0.89; top20=0.97)
- **Hypoxanthine** (q≈2e-6, δ_CS=+0.89, monotonic_down; top20=0.89)
- **Erythrose 4-phosphate** (q≈2e-6, δ_CS=+0.87; top20=0.89) — a pentose-phosphate-pathway intermediate
- **Anserine** (q≈2e-6, δ_CS=+0.78, monotonic_down; top20=0.79)
- **Glucuronolactone**, **short-chain (acyl)carnitines** [β-hydroxycarnitine 6:0, carnitine 4:0], **β-alanine**, **histamine** (all q<1e-5, large |δ|).

These are **candidate state-associated metabolites**, not biomarkers.

## 4. Severity patterns
116/287 metabolites show a monotonic median trend across Control→Mild→Severe (60 up, 56 down among
those; remainder non-monotonic). 183/287 are FDR-significant (q<0.05); 98 reach "strong" descriptive
support (q<0.01 and large Cliff's delta). 39 metabolites are bootstrap-stable in the top 20/50.

## 5. Modules supported
- **M05 (GAPDH_glycolysis_PPP): SUPPORTED** — 22/31 mapped metabolites FDR-significant; median
  Control-vs-Severe Cliff's δ ≈ +0.12; includes the PPP intermediate erythrose 4-phosphate and
  several sugar-phosphates. Module-level metabolic **state** association only.
- **M08 (lipid_mediator_resolution): NOT REPRESENTED** — 0 lipid-mediator metabolites are present
  in this HILIC central-carbon panel, so M08 receives no real support here (honest negative).
- General metabolic-state pool: 161/256 significant — broad state shift beyond the curated modules.

## 6. Inferential limits
- Rank statistics are invariant to the kernel preprocessing, so they are consistent with the kernel
  test while remaining interpretable on raw medians.
- A static pool level is NOT a flux. Severity association is NOT causation. None of these are
  validated biomarkers or predictors, and no neutrophil function is demonstrated.
- No sample-level fusion with any other source was performed.

## 7. Next steps (tiered, no fusion)
- Treat M05 and the bootstrap-stable candidates as descriptive anchors for the metabolic-state axis.
- Connect to other layers only as evidence-tiered support (NeuMap RNA state, Sadiku protein state,
  Chapman NET material, PXD029046 phosphosignaling state, GSE141285 chromatin potential) — never as
  sample-level fusion across unpaired sources.

> This localization analysis identifies candidate contributors to distributional separation. It does
> not identify validated biomarkers, fluxes or causal mechanisms.
