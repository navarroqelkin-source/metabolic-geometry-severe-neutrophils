# Feature Contribution Policy — Li ST002477

Feature contribution analysis is descriptive and post hoc.
It localizes candidate metabolites or modules associated with distributional separation.
It does not establish causality, metabolic flux, mechanism, biomarker validity or executed neutrophil function.

## Scope
- Runs only after `KERNEL_STATE_SEPARATION_SUPPORTED` on the same Tier 1 matrix.
- Rank-based, distribution-free statistics (Kruskal-Wallis, Cliff's delta) computed on the real
  intensity values for the 75 biological samples (Control/Mild/Severe). Blank/QC excluded.
- Rank statistics are invariant to the kernel preprocessing (log1p + robust scale), so they are
  consistent with the kernel test while remaining interpretable on raw medians.

## Vocabulary discipline
- "candidate state-associated metabolite" — allowed.
- "biomarker" / "predictor" / "driver" / "cause" — prohibited.
- Module statements are "module-level metabolic state association", never "pathway flux" or "mechanism".
