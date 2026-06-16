# Chapman Supplement Extraction Report

## 1. Supplement found
Yes. Open-access Frontiers supplementary tables for Chapman et al. 2019 (Front Immunol 10:423),
article PMC6421309 (CC BY), located via the Europe PMC supplementary-files bundle
(`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6421309/supplementaryFiles`). Seven
`Table_*.XLSX` tables present (Table_1 demographics … Table_7 PTM peptides).

## 2. Files downloaded
Open-access bundle (CC BY, ~11.6 MB, clear table index) → only the 7 tabular `Table_*.XLSX`
members extracted into `raw/`; images (TIFF/JPG) and any non-tabular members ignored. No raw
proteomics / mzML / mgf / vendor files. (The bundle zip is cached under `raw/` for reproducibility
and git-ignored; the small extracted XLSX tables are retained.)

## 3. Size and sha256 (key NET proteome tables)
- `Table_2.XLSX` — 37,771 bytes — sha256 44715f06ef3d5709f1885005…
- `Table_4.XLSX` — 61,226 bytes — sha256 e4249847d60d9524b94eb4a0…
(full set with sizes/sha256 in `CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv`.)

## 4. Tables detected
- **Table_2.XLSX** — NET proteins in healthy controls.
- **Table_4.XLSX** — NET proteins in RA/SLE patients.
- Table_6.XLSX — PTMs (citrullination/acetylation/methylation) — downloaded, context-only.
Columns parsed: gene ID, description, UniProt accession, peptide count, unique peptides, Anova (p),
q value, max fold change.

## 5. Rows / columns parsed
`processed/CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv`: **752 protein rows** (272 healthy-control +
480 RA/SLE), 10 structured columns. No OCR; no raw reanalysis.

## 6. Tier decision
**CHAPMAN_TIER2_CONFIRMED** → `Chapman_PXD011796 evidence_tier = Tier_2_SUPPLEMENTARY_TABLE`.

## 7. Claims permitted
Structured NET/release proteome **material composition** (which proteins, with peptide/Anova/q/fold
metrics) across healthy vs RA/SLE NETs; mappable to neutrophil effector-material modules.

## 8. Claims still prohibited (claim ceiling unchanged)
NETosis rate, NET clearance, pathogenicity, causal metabolism-to-NETosis, raw reanalysis, flux,
biomarker, executed function. A protein inventory is not a rate.

## 9. Chapman–Li bridge updated
Yes. `chapman_li_evidence_bridge/CHAPMAN_EVIDENCE_EXTRACTION.tsv` gains a Tier_2 structured-table
row; `CHAPMAN_LI_MODULE_BRIDGE.tsv` evidence_tiers now read `Chapman_PXD011796:Tier2`. Integrated
outputs (`CLAIM_CEILING_BY_SOURCE`, `NEUTROPHIL_LAYER_EVIDENCE_SUMMARY`, `NEUTROPHIL_MODULE_EVIDENCE_MAP`)
and `MASTER_SOURCE_EVIDENCE_TIER_MATRIX` now record Chapman at Tier 2. The claim ceiling is unchanged.

Validation: `CHAPMAN_SUPPLEMENT_VALIDATION_PASS`.
