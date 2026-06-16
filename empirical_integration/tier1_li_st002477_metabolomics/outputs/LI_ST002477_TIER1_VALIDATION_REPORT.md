# Li ST002477 — Tier 1 Claim-Ceiling Validation

Overall: **PASS**

## Checks
- PASS — V1 Tier1 provenance (live endpoint + sha256)
- PASS — V2_flux absent from allowed-claims
- PASS — V3_causal absent from allowed-claims
- PASS — V4_clinical absent from allowed-claims
- PASS — V5_function absent from allowed-claims
- PASS — V6 no sample-level fusion declared
- PASS — V7 Blank/QC excluded from biological analysis

## Anchored facts
- Tier 1 real intensity matrix: 287 metabolites x 75 biological samples (MS-reading units).
- Groups: Control/Mild/Severe (biology); Blank/QC excluded.
- Claim ceiling: metabolic STATE only — not flux, not causality, not clinical prediction, not executed function; no sample-level fusion with unpaired sources.
