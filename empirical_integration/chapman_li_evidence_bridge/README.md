# Chapman–Li evidence-tiered bridge

Connects **independent, unpaired** layers at the material/module/concept level:
- **Chapman_PXD011796** (Tier 3): NET/release proteome composition (histones, MPO, neutrophil
  elastase, citrullinated peptides; HC/RA/SLE). Repository raw-only; quantitative lists in the
  open-access article supplement.
- **Li_ST002477** (Tier 1): severity-associated metabolomic state separation; module **M05** supported.

This is **not** a sample-level integration. No co-measurement, no causality, no metabolism→NETosis
mechanism, no NETosis rate / clearance / pathogenicity. See `CHAPMAN_LI_BRIDGE_POLICY.md` /
`CHAPMAN_LI_CLAIM_CEILING.md`.

## Files
- `CHAPMAN_LI_BRIDGE_POLICY.md`, `CHAPMAN_LI_CLAIM_CEILING.md`
- `CHAPMAN_EVIDENCE_EXTRACTION.tsv` — structured NET/release proteome evidence (reused/confirmed)
- `LI_METABOLIC_AXIS_SUMMARY.tsv` — Li metabolic-state axis (M05 supported, M08 not represented)
- `CHAPMAN_LI_MODULE_BRIDGE.tsv` — allowed material/module bridges with prohibited counterparts
- `CHAPMAN_LI_BRIDGE_REPORT.md` — synthesis + inferential limits
- `scripts/` — 01 Chapman evidence, 02 Li axis, 03 bridge, 04 validation
- `outputs/` — validation report

## Run
```
python scripts/01_extract_chapman_structured_evidence.py
python scripts/02_summarize_li_metabolic_axis.py
python scripts/03_build_chapman_li_module_bridge.py
python scripts/04_validate_chapman_li_bridge_claims.py
```
Reuses the verified Chapman extraction (`../evidence_tiered_extraction/`) and the Li localization
outputs; light live re-confirmation via PRIDE when network is available.
