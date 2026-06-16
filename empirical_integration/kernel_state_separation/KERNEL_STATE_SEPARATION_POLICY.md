CURRENT_STATUS: KERNEL_STATE_SEPARATION_ACTIVE_FOR_TIER1_LI_ST002477
PURPOSE: detect distributional state separation in real omic matrices.
ELIGIBLE_INPUTS: Tier 1 or Tier 2 real matrices with provenance and QC.
CURRENT_ELIGIBLE_SOURCE: Li_ST002477 metabolomics.
DISALLOWED_INPUTS: article-level evidence, qualitative anchors, simulated data, placeholders.
PRIMARY_METHODS: MMD, energy distance, permutation testing, bandwidth sensitivity.
CLAIM_CEILING: distributional metabolic state separation, not mechanism.

A positive kernel test authorizes downstream biological exploration; it does not establish mechanism, flux, biomarker validity or executed neutrophil function.

## Why kernel here, and only here
The question is distributional: do Control / Mild / Severe occupy distinguishable metabolomic
state distributions (including non-linear / covariance / heterogeneity differences) — not "which
metabolite is a biomarker". This requires a real sample x feature matrix. It is therefore valid
for Li_ST002477 (Tier 1 matrix) and INVALID for Tier 3/4 sources that have no compatible matrix
(NeuMap, Sadiku, Chapman, PXD029046, GSE141285). Forcing kernel methods onto narrative evidence
would be mathematical decoration, not analysis.

## Eligibility gate (all must hold)
1. Real matrix with provenance.   2. Clear biological groups.   3. QC/Blank separated.
4. Goal = global state change.     5. No causal-mechanism claim.  6. Validated by permutation + bandwidth sensitivity.

## Permitted claim
"The metabolomic distributions show evidence of state separation between groups under
permutation-tested kernel discrepancy."

## Prohibited claims
metabolic flux altered; causal mechanism demonstrated; clinical biomarker validated; severity
prediction clinically actionable; NETosis executed; neutrophil function demonstrated; sample-level
pan-omic fusion performed.

## Methodological note (deferred, not productized)
Kernel covariance/mean embeddings as a *productive result* are deferred to methodological
discussion/extension (more emergent). Operational reproducible analysis = MMD + energy distance +
permutation + bandwidth sensitivity.
