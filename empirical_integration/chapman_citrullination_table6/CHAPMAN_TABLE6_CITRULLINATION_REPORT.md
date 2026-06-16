# Chapman Table_6 Citrullination Report

## 1. Table_6 exists
Yes — `chapman_supplement_tier2_extraction/raw/Table_6.XLSX`, three sheets: **Citrullination**,
Acetylation, Methylation. The Citrullination sheet was the parse target.

## 2. Column structure (Citrullination sheet)
`Protein Accession` (UniProt|entry, sometimes with gene in parens), `Protein name`, `Peptide`
(citrulline marked +.98 on Arg), `A23187 (n=)`, `PMA (n=)` — detection counts under the two
NET-induction stimuli. (95 rows incl. title + header.)

## 3. Rows parsed
**87 citrullinated peptide entries** (every entry traces to Table_6#Citrullination; no fabrication).

## 4. Citrullinated entries
87 entries across **46 unique proteins**, each with the citrullinated residue site (Arg +0.98) and
per-stimulus detection counts (A23187 / PMA).

## 5. Representative proteins/peptides
AZU1 (azurocidin), CATG (cathepsin G / CTSG), ELNE (neutrophil elastase / ELANE) — classic
citrullinated NET granule targets — plus actins (ACTB/ACTG…), coronin-1A (COR1A), ARPC1B and others.

## 6. NET_citrullinated_material status
**POPULATED** (was 0). 87 entries / 46 proteins. The earlier zero was a parsing gap (PTM data live
in Table_6, not the general protein list), now resolved — not a biological absence.

## 7. Chapman–Li updated
- Chapman Tier 2 protein-module map gains NET_citrullinated_material rows (basis
  `citrullination_PTM:Table_6#Citrullination`).
- Tier 2 module summary adds NET_citrullinated_material (n_proteins=46; q-values NA — count-based PTM table).
- New bridge **T2_BR04** (material_state_alignment): NET_citrullinated_material ↔ Li global metabolic
  severity-state.
- Integrated outputs (module map + claim ceiling) annotated.

## 8. Claims permitted
Structured citrullinated NET/release material composition; PTM-level material annotation;
citrullinated peptide/protein representation; evidence-tiered material composition adjacent to the
Li metabolic axis.

## 9. Claims prohibited
Citrullination rate, PAD4 activity, NETosis rate, NET clearance, pathogenicity, causal
metabolism-to-citrullination, sample-level fusion, co-measurement. Detection counts are presence
counts, not rates.

## 10. Validation
`CHAPMAN_TABLE6_CITRULLINATION_VALIDATION_PASS` (5/5 checks, incl. provenance/no-fabrication).
