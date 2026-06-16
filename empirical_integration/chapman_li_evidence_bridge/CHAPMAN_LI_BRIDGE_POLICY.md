CURRENT_STATUS: CHAPMAN_LI_EVIDENCE_TIERED_BRIDGE_ACTIVE
PURPOSE: connect Chapman NET/release proteome evidence with Li_ST002477 metabolomic severity-state evidence at material/module/concept level.
NOT_ALLOWED: sample-level fusion, co-measurement claim, causal inference, metabolism-to-NETosis mechanism, NETosis rate claim, clearance claim, pathogenicity claim.
ALLOWED: evidence-tiered material-state bridge, NET/release composition context, metabolic-state context, hypothesis-generating synthesis.

## Why this is allowed and what it is not
Chapman_PXD011796 (Tier 3, NET/release proteome; repository raw-only) and Li_ST002477 (Tier 1,
real metabolomics matrix) are INDEPENDENT, UNPAIRED datasets (different cohorts/conditions, no
shared samples). Therefore:
- No sample-level correlation, co-measurement, or joint embedding.
- No conversion of NET proteome into NETosis rate, clearance, or pathogenicity.
- No conversion of metabolite state into flux, causation, or NET formation.
- The only legitimate connection is a material/module/concept synthesis under claim ceilings.

## Claim ceilings carried into the bridge
- Chapman: NET material / release composition, not NET formation rate, clearance or pathogenicity.
- Li_ST002477: metabolite levels define metabolic STATE, not flux/causality/biomarker/function.
- Bridge: hypothesis-generating cross-layer link only; never mechanism, never co-measurement.
