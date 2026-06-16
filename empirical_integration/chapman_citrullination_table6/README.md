# Chapman Table_6 citrullination

Parses Chapman supplementary `Table_6.XLSX` (sheet **Citrullination**) to populate the
`NET_citrullinated_material` module that was empty after the Tier 2 protein-list mapping (the
citrullination evidence lives in a separate PTM table, not the general protein list).

Sheet "Citrullination": citrullinated peptides (Arg +0.98 Da) per protein, with detection counts
under two NET-induction stimuli (A23187, PMA). Tier 2 supplementary evidence.

Claim ceiling: citrullinated NET/release **material composition** — NOT citrullination rate, PAD4
activity, NETosis rate, clearance, pathogenicity or causality. A detection count is not a rate.

## Files
- `CHAPMAN_TABLE6_CITRULLINATION_POLICY.md`
- `CHAPMAN_TABLE6_INDEX.tsv` — sheet/column inventory
- `CHAPMAN_TABLE6_PARSED_CITRULLINATION.tsv` — parsed citrullinated entries
- `CHAPMAN_CITRULLINATION_MODULE_SUMMARY.tsv` — NET_citrullinated_material summary
- `CHAPMAN_CITRULLINATION_BRIDGE_UPDATE.tsv` — Chapman–Li bridge update (T2_BR04) if populated
- `CHAPMAN_TABLE6_CITRULLINATION_REPORT.md`
- `scripts/` 01 inspect, 02 parse, 03 summarize, 04 bridge update, 05 validate · `outputs/`

## Run
```
python scripts/01_inspect_chapman_table6.py
python scripts/02_parse_chapman_table6_citrullination.py
python scripts/03_summarize_citrullinated_material_module.py
python scripts/04_update_chapman_li_bridge_with_citrullination.py
python scripts/05_validate_chapman_table6_citrullination_claims.py
```
