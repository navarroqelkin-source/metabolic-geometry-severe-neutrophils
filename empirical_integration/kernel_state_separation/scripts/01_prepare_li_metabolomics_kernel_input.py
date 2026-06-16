"""01 — Prepare the Li ST002477 metabolomics matrix for kernel two-sample tests.

Reads the real Tier 1 matrix (metabolite x sample), confirms groups, excludes Blank/QC,
orients to sample x metabolite, drops constant metabolites, applies log1p (non-negative only)
and per-metabolite robust scaling (median / IQR). Writes prepared matrix + metadata + report.
No real matrix -> MISSING_REAL_MATRIX, no fabricated outputs.
"""
import csv
import os

import numpy as np
import _kernel_common as K

MATRIX = K.emp_path("tier1_li_st002477_metabolomics/outputs/LI_ST002477_intensity_matrix.tsv")
META = K.emp_path("tier1_li_st002477_metabolomics/LI_ST002477_SAMPLE_METADATA.tsv")
METACOLS = {"metabolite_id", "metabolite_name", "analysis_id", "units"}


def main():
    os.makedirs(K.OUTDIR, exist_ok=True)
    if not os.path.exists(MATRIX):
        K.set_status("prepare", "MISSING_REAL_MATRIX", MATRIX)
        with open(K.path("outputs", "LI_ST002477_KERNEL_PREP_REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write("# Kernel prep\n\nStatus: **MISSING_REAL_MATRIX** — no input matrix. Nothing fabricated.\n")
        print("[01] MISSING_REAL_MATRIX")
        return

    with open(MATRIX, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    header = list(rows[0].keys())
    samples = [c for c in header if c not in METACOLS]      # metabolite x sample -> sample cols
    feat_ids = [r["metabolite_id"] or r["metabolite_name"] for r in rows]

    # group labels, exclude Blank/QC
    meta = {r["sample_id"]: r for r in K.read_tsv(META)}
    keep = [s for s in samples if meta.get(s, {}).get("group_or_condition") in K.GROUPS
            and meta.get(s, {}).get("include_in_biological_analysis") == "YES"]
    excluded = [s for s in samples if s not in keep]

    # build sample x metabolite
    X = np.zeros((len(keep), len(rows)), dtype=float)
    for j, r in enumerate(rows):
        for i, s in enumerate(keep):
            v = (r.get(s, "") or "").strip()
            X[i, j] = float(v) if v != "" else np.nan

    # drop constant / all-nan metabolites
    col_ok = []
    for j in range(X.shape[1]):
        col = X[:, j]
        finite = col[np.isfinite(col)]
        col_ok.append(finite.size > 0 and np.nanstd(col) > 0)
    col_ok = np.asarray(col_ok)
    n_const = int((~col_ok).sum())
    X = X[:, col_ok]
    feat_ids = [f for f, ok in zip(feat_ids, col_ok) if ok]

    # impute remaining nans with per-metabolite median (kept minimal; matrix had 0 missing)
    n_imputed = 0
    for j in range(X.shape[1]):
        col = X[:, j]
        mask = ~np.isfinite(col)
        if mask.any():
            med = np.nanmedian(col)
            col[mask] = med
            n_imputed += int(mask.sum())

    # log1p only if all non-negative
    nonneg = bool(np.all(X >= 0))
    transform = "none"
    if nonneg:
        X = np.log1p(X)
        transform = "log1p"

    # per-metabolite robust scaling: (x - median) / IQR
    med = np.median(X, axis=0)
    q75, q25 = np.percentile(X, 75, axis=0), np.percentile(X, 25, axis=0)
    iqr = q75 - q25
    iqr[iqr == 0] = 1.0
    Xs = (X - med) / iqr
    transform += " + robust_scale(median/IQR)"

    groups = [meta[s]["group_or_condition"] for s in keep]

    # write prepared matrix (sample x metabolite)
    with open(K.PREP_MATRIX, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["sample_id"] + feat_ids)
        for i, s in enumerate(keep):
            w.writerow([s] + [f"{v:.6g}" for v in Xs[i, :]])
    K.write_tsv(K.PREP_META, ["sample_id", "group_or_condition"],
                [{"sample_id": s, "group_or_condition": meta[s]["group_or_condition"]} for s in keep])

    gc = {g: groups.count(g) for g in K.GROUPS}
    with open(K.path("outputs", "LI_ST002477_KERNEL_PREP_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "# Kernel prep — Li ST002477\n\n"
            "Status: **OK**\n\n"
            f"- Input matrix orientation: metabolite x sample -> transposed to **sample x metabolite**\n"
            f"- Samples kept (biological): {len(keep)}  ({', '.join(f'{g}={gc[g]}' for g in K.GROUPS)})\n"
            f"- Samples excluded (Blank/QC/other): {len(excluded)} -> {excluded}\n"
            f"- Metabolites in: {len(rows)}; constant/all-nan dropped: {n_const}; kept: {X.shape[1]}\n"
            f"- NaNs imputed (per-metabolite median): {n_imputed}\n"
            f"- Non-negative input: {nonneg}; transform: {transform}\n\n"
            "Claim ceiling: distributional metabolic state only; not flux/causal/biomarker/function.\n")

    K.set_status("prepare", "OK", f"{len(keep)} samples x {X.shape[1]} metabolites; {transform}")
    print(f"[01] OK samples={len(keep)} {gc} metabolites_kept={X.shape[1]} dropped_const={n_const} "
          f"transform='{transform}' excluded={len(excluded)}")


if __name__ == "__main__":
    main()
