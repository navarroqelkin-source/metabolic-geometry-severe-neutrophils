CURRENT_STATUS: CHAPMAN_TABLE6_CITRULLINATION_EXTRACTION_ACTIVE
PURPOSE: parse Chapman supplementary Table_6 to extract structured citrullinated peptide/protein or PTM material evidence.
INPUT: chapman_supplement_tier2_extraction/raw/Table_6.XLSX
EVIDENCE_TIER: Tier_2_SUPPLEMENTARY_TABLE
CLAIM_CEILING: citrullinated NET/release material composition, not citrullination rate, PAD4 activity, NETosis rate, clearance, pathogenicity or causality.

## What Table_6 contains
Sheet "Citrullination": citrullinated peptides (Arg +0.98 Da deamidation) per protein, with
detection counts under two NET-induction stimuli (A23187, PMA). Sheets "Acetylation" and
"Methylation" hold other PTMs (out of scope here).

## Discipline
- Detection counts are presence/identification counts, NOT rates. A count is not a rate.
- Citrullinated entries describe WHICH material carries the PTM, never how fast PAD4 acts, whether
  NETs form/clear, or whether the modification is pathogenic.
- If a field is absent, leave it blank — do not invent sites, conditions or metrics.
