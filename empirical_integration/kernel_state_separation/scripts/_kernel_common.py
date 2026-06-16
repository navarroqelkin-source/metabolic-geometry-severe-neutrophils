"""Shared helpers for the kernel state-separation module. numpy + stdlib."""
import csv
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # kernel_state_separation/
EMP = os.path.dirname(ROOT)                                                  # empirical_integration/
OUTDIR = os.path.join(ROOT, "outputs")
SEED = 20260610
GROUPS = ["Control", "Mild", "Severe"]
COMPARISONS = [("Control", "Mild"), ("Control", "Severe"), ("Mild", "Severe")]
BANDWIDTH_SCALES = [0.5, 1.0, 2.0, 4.0]

PREP_MATRIX = os.path.join(OUTDIR, "LI_ST002477_kernel_input_matrix.tsv")
PREP_META = os.path.join(OUTDIR, "LI_ST002477_kernel_input_metadata.tsv")

ALLOWED = "distributional metabolic state separation between groups (permutation-tested)"
PROHIBITED = "flux / causal mechanism / clinical biomarker / severity prediction / executed function / sample-level fusion"


def path(*p):
    return os.path.join(ROOT, *p)


def emp_path(rel):
    return os.path.join(EMP, rel.replace("/", os.sep))


def write_tsv(fpath, header, rows):
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})


def read_tsv(fpath):
    if not os.path.exists(fpath):
        return []
    with open(fpath, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def set_status(step, status, detail=""):
    rows = read_tsv(path("KERNEL_ANALYSIS_STATUS.tsv")) or [
        {"step": s, "status": "PENDING", "detail": ""}
        for s in ("prepare", "mmd", "energy_distance", "sensitivity_validation")]
    found = False
    for r in rows:
        if r["step"] == step:
            r["status"], r["detail"] = status, detail
            found = True
    if not found:
        rows.append({"step": step, "status": status, "detail": detail})
    write_tsv(path("KERNEL_ANALYSIS_STATUS.tsv"), ["step", "status", "detail"], rows)


def load_prepared():
    """Return (X sample x feature float array, groups list, sample_ids, feature_names) or None."""
    if not (os.path.exists(PREP_MATRIX) and os.path.exists(PREP_META)):
        return None
    with open(PREP_MATRIX, "r", encoding="utf-8", newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        header = next(rd)
        feats = header[1:]
        ids, vals = [], []
        for row in rd:
            ids.append(row[0])
            vals.append([float(x) for x in row[1:]])
    X = np.asarray(vals, dtype=float)
    meta = {r["sample_id"]: r["group_or_condition"] for r in read_tsv(PREP_META)}
    groups = [meta.get(s, "UNKNOWN") for s in ids]
    return X, groups, ids, feats


def median_heuristic(X):
    """Median of pairwise euclidean distances (the sigma scale)."""
    from scipy.spatial.distance import pdist
    d = pdist(X, metric="euclidean")
    d = d[d > 0]
    return float(np.median(d)) if d.size else 1.0
