# Chapman Table_6 acetylation + methylation PTM layer

Parses the Acetylation and Methylation sheets of Chapman `Table_6.XLSX` to complete the NET/release
**PTM material layer** alongside the already-parsed citrullination (`chapman_citrullination_table6/`).

- Acetylation (+42.01): ~85 peptides / ~52 proteins (ACTB, annexins, catalase, cofilin, 14-3-3…).
- Methylation (+14.02/+28.03): ~32 peptides / ~13 proteins — incl. histones H3 (H31/H32/H33) and
  MPO (PERM), biologically central to NET chromatin/oxidative material.

Claim ceiling: acetylated/methylated NET/release **material composition** — NOT enzyme activity
(HAT/HDAC/PRMT), NOT modification rate, NOT NETosis rate / clearance / pathogenicity / causality.

## Files
- `CHAPMAN_PTM_POLICY.md`
- `CHAPMAN_TABLE6_ACETYL_METHYL_INDEX.tsv` — sheet inventory
- `CHAPMAN_TABLE6_PARSED_PTM.tsv` — parsed acetylated/methylated entries
- `CHAPMAN_PTM_MODULE_SUMMARY.tsv` — NET_acetylated_material / NET_methylated_material summaries
- `CHAPMAN_PTM_REPORT.md`
- `scripts/` 01 parse, 02 summarize+integrate, 03 validate · `outputs/`

## Run
```
python scripts/01_parse_acetyl_methyl_ptm.py
python scripts/02_summarize_and_integrate_ptm_modules.py
python scripts/03_validate_ptm_claims.py
```
