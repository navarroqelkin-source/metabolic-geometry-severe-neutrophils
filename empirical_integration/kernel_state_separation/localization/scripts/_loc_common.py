"""Shared helpers for Li ST002477 descriptive localization. numpy/scipy/statsmodels + stdlib."""
import csv
import os

import numpy as np

LOCROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # localization/
KSROOT = os.path.dirname(LOCROOT)                                        # kernel_state_separation/
EMP = os.path.dirname(KSROOT)                                           # empirical_integration/
OUTDIR = os.path.join(LOCROOT, "outputs")
SEED = 20260610
GROUPS = ["Control", "Mild", "Severe"]

# Real intensity matrix (metabolite x sample) and biological-sample metadata.
RAW_MATRIX = os.path.join(EMP, "tier1_li_st002477_metabolomics", "outputs",
                          "LI_ST002477_intensity_matrix.tsv")
PREP_META = os.path.join(KSROOT, "outputs", "LI_ST002477_kernel_input_metadata.tsv")
MODULE_MAP = os.path.join(EMP, "tier1_li_st002477_metabolomics", "outputs",
                          "LI_ST002477_MODULE_MAPPING.tsv")
METACOLS = {"metabolite_id", "metabolite_name", "analysis_id", "units"}

ALLOWED_FEAT = "candidate state-associated metabolite (descriptive)"
PROHIBITED_FEAT = "biomarker / driver / cause / flux / clinical prediction / executed function"


def locpath(*p):
    return os.path.join(LOCROOT, *p)


def read_tsv(fpath):
    if not os.path.exists(fpath):
        return []
    with open(fpath, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(fpath, header, rows):
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})


def set_status(step, status, detail=""):
    p = locpath("LI_ST002477_LOCALIZATION_STATUS.tsv")
    rows = read_tsv(p) or [{"step": s, "status": "PENDING", "detail": ""}
                           for s in ("feature_contribution", "bootstrap_stability",
                                     "module_summary", "validation")]
    found = False
    for r in rows:
        if r["step"] == step:
            r["status"], r["detail"] = status, detail
            found = True
    if not found:
        rows.append({"step": step, "status": status, "detail": detail})
    write_tsv(p, ["step", "status", "detail"], rows)


def load_raw_bio():
    """Load real intensities for the 75 biological samples.
    Returns (X sample x metabolite float, groups, sample_ids, feat_ids, feat_names) or None."""
    if not (os.path.exists(RAW_MATRIX) and os.path.exists(PREP_META)):
        return None
    with open(RAW_MATRIX, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    header = list(rows[0].keys())
    all_samples = [c for c in header if c not in METACOLS]
    meta = {r["sample_id"]: r["group_or_condition"] for r in read_tsv(PREP_META)}
    keep = [s for s in all_samples if meta.get(s) in GROUPS]
    feat_ids = [r.get("metabolite_id") or r.get("metabolite_name") for r in rows]
    feat_names = [r.get("metabolite_name", "") for r in rows]
    X = np.zeros((len(keep), len(rows)), dtype=float)
    for j, r in enumerate(rows):
        for i, s in enumerate(keep):
            v = (r.get(s, "") or "").strip()
            X[i, j] = float(v) if v != "" else np.nan
    groups = np.array([meta[s] for s in keep])
    return X, groups, keep, feat_ids, feat_names


def cliffs_delta(a, b):
    """Cliff's delta of a vs b: P(a>b) - P(a<b). Positive => a tends larger."""
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if a.size == 0 or b.size == 0:
        return float("nan")
    gt = lt = 0
    for x in a:
        gt += np.sum(x > b)
        lt += np.sum(x < b)
    return (gt - lt) / (a.size * b.size)


def severity_pattern(mc, mm, ms):
    if any(np.isnan(v) for v in (mc, mm, ms)):
        return "insufficient_data"
    if mc < mm < ms:
        return "monotonic_up"
    if mc > mm > ms:
        return "monotonic_down"
    return "non_monotonic"
