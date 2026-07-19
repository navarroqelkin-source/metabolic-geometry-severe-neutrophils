> **SUPERSEDED FOR CROSS-PAIR ORDERING.** Do not use this document to rank the three clinical
> contrasts against each other, to support Control-Severe dominance, or to support agreement
> between MMD and energy distance. Statements confined to a single pairwise contrast are
> unaffected, subject to the limitations in the root notice.
> See `NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md`.

# Kernel State Separation — Validation Report

Final status: **KERNEL_STATE_SEPARATION_SUPPORTED**

Source: Li_ST002477 (Tier 1 metabolomics). Input: real matrix, 19/30/26 Control/Mild/Severe.

## Per-comparison
- **Control_vs_Mild**: MMD sig in 1.0 of bandwidths (p∈[0.001,0.001]); energy p=0.001 (LOO p=0.001, STABLE); agree=YES → SUPPORTED
- **Control_vs_Severe**: MMD sig in 1.0 of bandwidths (p∈[0.001,0.001]); energy p=0.001 (LOO p=0.001, STABLE); agree=YES → SUPPORTED
- **Mild_vs_Severe**: MMD sig in 1.0 of bandwidths (p∈[0.001,0.001]); energy p=0.001 (LOO p=0.001, STABLE); agree=YES → SUPPORTED

## Sensitivity
- Severity ordering (Control_vs_Severe MMD ≥ Control_vs_Mild MMD): YES
- MMD/energy agreement: 3/3 comparisons
- Outlier robustness (LOO): 3/3 stable

## Claim ceiling
- Allowed: distributional metabolic state separation between groups (permutation-tested).
- Prohibited: flux / causal mechanism / clinical biomarker / severity prediction / executed function / sample-level fusion.
- A positive result authorizes downstream biological exploration only; it does not establish mechanism, flux, biomarker validity or executed neutrophil function.
