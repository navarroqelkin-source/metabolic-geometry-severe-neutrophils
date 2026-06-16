# Kernel prep — Li ST002477

Status: **OK**

- Input matrix orientation: metabolite x sample -> transposed to **sample x metabolite**
- Samples kept (biological): 75  (Control=19, Mild=30, Severe=26)
- Samples excluded (Blank/QC/other): 0 -> []
- Metabolites in: 287; constant/all-nan dropped: 0; kept: 287
- NaNs imputed (per-metabolite median): 0
- Non-negative input: True; transform: log1p + robust_scale(median/IQR)

Claim ceiling: distributional metabolic state only; not flux/causal/biomarker/function.
