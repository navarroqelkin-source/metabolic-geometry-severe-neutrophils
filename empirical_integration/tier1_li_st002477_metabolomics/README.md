# Tier 1 — Li ST002477 neutrophil metabolomics

First real **Tier 1** quantitative layer of the project (DEC-040).

- Study: "Neutrophil metabolomics in COVID-19" (Metabolomics Workbench ST002477), LC-MS / HILIC.
- Content: 287 named metabolites; 89 biological samples (Control / Mild / Severe) + Blank + QC.
- Provenance: live Metabolomics Workbench REST API (endpoints recorded in `LI_ST002477_DATA_PROVENANCE.tsv`).
- Real intensity matrix retrieved (MS-reading units) — see `LI_ST002477_INTENSITY_MATRIX_STATUS.tsv`.

## Claim ceiling (strict) — see `LI_ST002477_CLAIM_CEILING.md`
Metabolic **state / constraint** only. NOT flux, NOT causal mechanism, NOT clinical prediction,
NOT executed neutrophil function. No sample-level fusion with unpaired sources.

## Files
- `LI_ST002477_TIER1_STATUS.tsv` — gate/status of this subflow
- `LI_ST002477_DATA_PROVENANCE.tsv` — every endpoint/file used (URL, size, sha256, retrieved_live)
- `LI_ST002477_SAMPLE_METADATA.tsv` — sample → group, with Blank/QC excluded from biology
- `LI_ST002477_METABOLITE_TABLE.tsv` — named metabolites + identifiers (no invented chemistry)
- `LI_ST002477_INTENSITY_MATRIX_STATUS.tsv` — whether the quantitative matrix was obtained
- `LI_ST002477_QC_REPORT.md` / `outputs/LI_ST002477_QC_SUMMARY.tsv` — minimal QC
- `LI_ST002477_CLAIM_CEILING.md` — permitted/prohibited interpretation
- `outputs/LI_ST002477_intensity_matrix.tsv` — real metabolite × sample matrix (if obtained)
- `outputs/LI_ST002477_GROUP_DESCRIPTIVE_SUMMARY.tsv` — prudent descriptive summary by severity
- `outputs/LI_ST002477_MODULE_MAPPING.tsv` — metabolite → pan-omic module map (tiered)
- `outputs/LI_ST002477_TIER1_VALIDATION_REPORT.md` — claim-ceiling validation

## Run
```
python scripts/01_fetch_li_st002477_data_matrix.py
python scripts/02_qc_li_st002477_matrix.py
python scripts/03_li_st002477_descriptive_state_summary.py
python scripts/04_map_li_metabolites_to_modules.py
python scripts/05_validate_li_tier1_claims.py
```
Scripts are stdlib-only (urllib/csv/json/statistics). They degrade safely: if the matrix
cannot be retrieved they record `MISSING_MATRIX` and do not fabricate data.
