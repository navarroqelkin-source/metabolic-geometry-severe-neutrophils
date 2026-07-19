# SCIENTIFIC SUPERSESSION NOTICE — 2026-07-19

**A central claim in material published in this repository has been withdrawn from use by the
repository maintainer following a post-results methodological audit.** Coauthor review of the
corrected manuscript remains pending; this notice is issued by the maintainer and does not record
a collective authorship decision.

The correction is issued in the same place the claim was published. Nothing is being deleted: the affected files and the commit history are preserved so the correction is traceable.

## 1. What is withdrawn

```
Control–Severe > Control–Mild > Mild–Severe          cross-pair ordering
Control–Severe is the largest / dominant contrast    dominance
MMD and energy distance agree on that ordering       metric agreement
"stable to removing any single sample"               exhaustive leave-one-out  [added 2026-07-19]
```

**The fourth item is independent of the other three and of both estimator defects.** The published
analysis did not perform exhaustive leave-one-out. `04_kernel_sensitivity_report.py` removes
exactly **one** maximum-L2-norm sample from **each** group simultaneously and recomputes the
energy distance once. That is a max-norm outlier stress test. It cannot support "stable to
removing any single sample", and the field name `energy_p_outlier_LOO` and the report line
"Outlier robustness (LOO): 3/3 stable" both overstate what was run.

```
RAW75_EXHAUSTIVE_LOO_CLAIM = WITHDRAWN
ACTUAL_PROCEDURE           = ONE_MAX_NORM_SAMPLE_REMOVED_PER_GROUP
```

An exhaustive 74-fold leave-one-out **was** executed — but in the later source-adjusted analysis,
on a different matrix with a different control group size. It does not retroactively validate the
published claim.

## 1b. Two distinct analyses, not one

The published analysis and the later source-adjusted gate are separate, and must not be conflated:

| | published (raw) | source-adjusted gate |
|---|---|---|
| samples | Control 19 / Mild 30 / Severe 26 | Control 18 / Mild 30 / Severe 26 |
| transform | `log1p` | none (11,886 of 21,238 cells negative) |
| scaling | robust median / IQR | robust median / MAD |
| robustness | one max-norm sample per group | exhaustive 74-fold |
| features | 287 | 276 primary, 282 sensitivity |

The estimator defects below are qualitative and apply to both. The **finite-sample bias terms are
not identical**, because they depend on group sizes, and the sizes differ. Where this notice
quotes 18/30/26 it refers to the source-adjusted arm.

These appear in `manuscript_synthesis/MANUSCRIPT_FULL_DRAFT_v0.8.md` (Abstract and Results),
in Figure 3 (`.svg` and the exported `.pdf`), in
`empirical_integration/kernel_state_separation/localization/LI_ST002477_LOCALIZATION_REPORT.md`,
and in the two `chapman_li_evidence_bridge` files that label the ordering "kernel SUPPORTED".

## 2. Why

Two defects in the implemented estimators, both found after the results were opened:

1. **The MMD bandwidth was pair-specific.** The Gaussian median heuristic was recomputed
   separately for each pairwise comparison, so the three MMD values are defined in three
   different reproducing-kernel Hilbert spaces. Each pairwise test remains interpretable inside
   its own kernel; the three magnitudes are not comparable to one another.

2. **The energy distance used the biased V-statistic.** Denominators `m²` and `n²` including the
   zero diagonal, rather than the unbiased `m(m−1)` and `n(n−1)`. The finite-sample correction is

   ```
   E_V − E_U = A_X/m + A_Y/n
   ```

   where `A` is the mean within-group pairwise distance excluding the diagonal. This term differs
   per comparison because the groups are unequal in size (Control 18, Mild 30, Severe 26), so it
   does not cancel when magnitudes are ranked against each other. **The signs of both
   differential-bias terms are indeterminate before the within-group dispersions are computed;
   no prior ordering of `A_C`, `A_M`, `A_S` is assumed.**

Consequently the preregistered terminal decision rule, which turns on the word *"largest"*,
presupposes a cross-pair comparison that neither implemented estimator licenses.

```
PREREGISTERED_TERMINAL_GATE = NOT_EVALUABLE_DUE_TO_METRIC_SPECIFICATION_DEFECT
```

**This is not a negative finding about the data.** The gate could not be executed. The
preregistration worked as intended: it made the hidden dependency visible instead of allowing it
to pass as a result.

## 3. What remains available

- Within-pair distributional discrepancy statistics, each inside its own kernel.
- Within-pair energy-distance values as descriptive statistics.
- Leave-one-out stability of an individual pairwise contrast.
- Fixed-product label-permutation diagnostics.

**The diagnostic permutation values do not constitute independent covariate-adjusted
significance tests.** The source-adjusted matrix was produced by a model that included the
clinical labels, so independent exchangeability is not justified.

No licensed cross-pair magnitude comparison. No dominant-contrast claim.

Permitted formulation:

> The three clinical contrasts produced pairwise distributional discrepancies under the
> statistics used. The relative magnitude of those discrepancies across pairs was not
> established by the estimators executed.

## 4. What readers and users of this repository should do

- **Do not cite or reuse** the ordering, the Control–Severe dominance statement, or the
  two-metric agreement statement.
- Within-pair discrepancy statistics remain available **under the limitations in section 3**.
  They are not a licence to compare magnitudes across pairs, and the permutation diagnostics are
  not independent covariate-adjusted significance tests.
- The Zenodo deposit `10.5281/zenodo.20717146` archives the same material and carries the same
  withdrawn claim. A supersession note is being added there; the deposit is **not** being
  deleted.
- If you have built on the ordering claim, please contact the corresponding author.

## 5. Status

```
INDEPENDENT_METRIC_AUDIT    commissioned, read-only, outcome not prejudged
MANUSCRIPT_REPAIR           HOLD
FIGURE_REPAIR               HOLD
PUBLIC_REPLACEMENT          HOLD
CORRECTED_PACKAGE           will follow after the audit
GIT_HISTORY                 preserved; no rebase, no force-push, nothing deleted
```

A repair using the unbiased U-statistic is permitted only **after** the independent audit, as a
declared post-hoc transparent sensitivity analysis. It can never retroactively restore the
preregistration.

## 6. Provenance of this correction

The defects were identified by internal post-results audit and independently reviewed at the
level of methodological characterization. A fully independent numerical reproduction remains in
progress.
The full technical record, including the withdrawn intermediate positions and the corrections
applied to those, is maintained in the working repository and will accompany the corrected
package.
