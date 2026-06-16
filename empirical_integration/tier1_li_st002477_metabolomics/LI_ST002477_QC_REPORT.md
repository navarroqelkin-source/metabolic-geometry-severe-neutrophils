# Li ST002477 QC Report

Status: **OK** (real intensity matrix)

- Metabolites: 287
- Samples in matrix: 75 (biological=75, non-biological=0)
- Samples in metadata: 89 (Blank=3, QC=11)
- Group counts in matrix: Control=19, Mild=30, Severe=26
- Data cells: 21525; missing: 0 (0.0%); non-numeric: 0

## QC notes
- The MW `/data` quantitative table contains only the biological samples (Control/Mild/Severe = 75); Blank (3) and QC (11) appear in the factor sheet but are not present in the quantitative matrix.
- All Blank/QC are excluded from biological contrasts by `LI_ST002477_SAMPLE_METADATA.tsv`.
- Values are MS-reading intensities (relative), suitable for STATE comparison only — not flux.
