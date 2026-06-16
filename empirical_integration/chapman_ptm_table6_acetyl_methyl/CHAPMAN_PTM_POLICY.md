CURRENT_STATUS: CHAPMAN_TABLE6_ACETYL_METHYL_EXTRACTION_ACTIVE
PURPOSE: parse Chapman Table_6 sheets Acetylation and Methylation into structured PTM material evidence, completing the Chapman NET/release PTM layer (citrullination + acetylation + methylation).
INPUT: chapman_supplement_tier2_extraction/raw/Table_6.XLSX (sheets Acetylation, Methylation)
EVIDENCE_TIER: Tier_2_SUPPLEMENTARY_TABLE
CLAIM_CEILING: acetylated/methylated NET/release material composition, not enzyme activity (HAT/HDAC/PRMT), not acetylation/methylation rate, not NETosis rate, clearance, pathogenicity or causality.

## What the sheets contain
- Acetylation (+42.01): peptides identified in >=22/23 RA and SLE samples with an acetylation modification.
- Methylation (+14.02 / +28.03): peptides with methylation/dimethylation in >=22/23 RA and SLE samples.
- Columns: Protein Accession (UniProt|entry), Protein name, Peptide, PTM.

## Discipline
- A PTM identification is presence of the modification on detected material, NOT a rate and NOT
  evidence of the modifying enzyme's activity.
- Rows with empty peptide AND empty PTM are skipped (no fabrication). No OCR.
