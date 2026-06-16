# Chapman Table_6 Acetylation/Methylation PTM Report

## 1. Source
Chapman `Table_6.XLSX` sheets **Acetylation** (+42.01) and **Methylation** (+14.02/+28.03),
already downloaded under `chapman_supplement_tier2_extraction/raw/`. Peptides identified in
≥22/23 RA and SLE samples carrying the modification. Columns: Protein Accession, Protein name,
Peptide, PTM.

## 2. Parsed entries
- **Acetylation: 60 entries / 49 proteins.** Representative: histones H3 (H31/H32/H33), actins
  (ACTB/ACTG), annexins (ANXA1/ANXA3), catalase (CATA), cofilin, 14-3-3, ARPC4, CALM2, CAPZB.
- **Methylation: 16 entries / 12 proteins.** Representative: histones H3 (H31/H32/H33), **MPO
  (PERM)**, ceruloplasmin (CERU), spectrin (SPTN1), HSP7C, actins.
Header-repeat and empty rows were skipped (no fabrication).

## 3. Biological note
Histone H3 carries co-occurring acetylation, methylation and citrullination in this dataset — the
classic chromatin-PTM signature of NET material. MPO methylation adds an oxidative-material PTM.
These are **material composition** facts, not enzyme-activity or rate claims.

## 4. Modules populated (refine registry M03 NET_release_material)
- `NET_acetylated_material` (49 proteins)
- `NET_methylated_material` (12 proteins)
- (with the prior `NET_citrullinated_material`, 46 proteins, the PTM layer is now complete)

## 5. Integration
Added to the Chapman Tier 2 protein-module map (`module_assignment_basis = <PTM>_PTM:Table_6#<sheet>`)
and module summary; integrated outputs (module map + claim ceiling) annotated. No Chapman–Li bridge
change required (PTM enriches the existing NET/release material side; the bridge already links NET
material to the Li axis).

## 6. Claims permitted
Structured acetylated/methylated NET/release material composition; PTM-level material annotation
(which proteins/residues carry the PTM), including histone and MPO PTMs.

## 7. Claims prohibited
Enzyme activity (HAT/HDAC/PRMT); acetylation/methylation **rate**; NETosis rate; NET clearance;
pathogenicity; causal mechanism; metabolism→PTM; sample-level fusion. A PTM identification is
presence on detected material, not a rate.

## 8. Validation
`CHAPMAN_PTM_VALIDATION_PASS` (6/6 checks, incl. provenance/no-fabrication).
