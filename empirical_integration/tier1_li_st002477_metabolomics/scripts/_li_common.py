"""Shared helpers for the Li ST002477 Tier 1 metabolomics subflow. Stdlib only."""
import csv
import hashlib
import os

try:
    from urllib.request import urlopen, Request
except Exception:  # pragma: no cover
    urlopen = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "outputs")

STUDY = "ST002477"
REST = "https://www.metabolomicsworkbench.org/rest/study/study_id/ST002477"
ENDPOINTS = {
    "summary": REST + "/summary",
    "factors": REST + "/factors",
    "metabolites": REST + "/metabolites",
    "data": REST + "/data",
}
BIO_GROUPS = {"Control", "Mild", "Severe"}
NONBIO_GROUPS = {"Blank", "QC"}


def path(*p):
    return os.path.join(ROOT, *p)


def fetch(url, timeout=60):
    """Return (ok, text). Never raises."""
    if urlopen is None:
        return False, "no urllib"
    try:
        req = Request(url, headers={"User-Agent": "cosmos-li-tier1/1.0"})
        with urlopen(req, timeout=timeout) as r:
            return True, r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def vals(obj):
    return list(obj.values()) if isinstance(obj, dict) else (obj or [])
