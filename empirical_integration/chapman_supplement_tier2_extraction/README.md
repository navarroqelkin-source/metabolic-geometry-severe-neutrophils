# Chapman supplement Tier 2 extraction

Attempts to upgrade `Chapman_PXD011796` from Tier 3 (article-level) to **Tier 2** (structured
supplementary table) by parsing the open-access Frontiers supplementary protein tables
(PMC6421309, CC BY).

Source of supplements: Europe PMC supplementary-files bundle for PMC6421309
(`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6421309/supplementaryFiles`).
Key tables: **Table_2.XLSX** (272 healthy-control NET proteins), **Table_4.XLSX** (480 RA/SLE NET
proteins), Table_6.XLSX (PTMs incl. citrullination). Columns: gene ID, description, UniProt
accession, peptide count, unique peptides, Anova p, q value, max fold change.

Claim ceiling (unchanged): NET/release material composition only — not NETosis rate, clearance,
pathogenicity or causal mechanism.

## Files
- `CHAPMAN_SUPPLEMENT_POLICY.md` — download + claim discipline
- `CHAPMAN_SUPPLEMENT_SEARCH.tsv` — located supplement(s)
- `CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv` — downloaded tables (size, sha256, parse status)
- `processed/CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv` — parsed structured NET proteome
- `CHAPMAN_TIER_UPGRADE_DECISION.md` — Tier 2 vs Tier 3 decision
- `CHAPMAN_SUPPLEMENT_EXTRACTION_REPORT.md` — full report
- `scripts/` 01 find, 02 download, 03 parse, 04 decide, 05 validate
- `raw/` downloaded tables · `outputs/` validation report

## Run
```
python scripts/01_find_chapman_open_access_supplement.py
python scripts/02_download_chapman_supplement_tables.py
python scripts/03_parse_chapman_supplement_tables.py
python scripts/04_decide_chapman_tier_upgrade.py
python scripts/05_validate_chapman_supplement_claims.py
```
