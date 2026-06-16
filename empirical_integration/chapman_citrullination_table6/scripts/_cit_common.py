"""Shared helpers for Chapman Table_6 citrullination extraction. stdlib + openpyxl."""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
OUTDIR = os.path.join(ROOT, "outputs")
TABLE6 = os.path.join(EMP, "chapman_supplement_tier2_extraction", "raw", "Table_6.XLSX")
CIT_SHEET = "Citrullination"
ALLOWED = "structured citrullinated NET/release material composition (Tier 2)"
PROHIBITED = ("citrullination rate / PAD4 activity / NETosis rate / NET clearance / pathogenicity / "
              "causal metabolism-to-citrullination / sample-level fusion")

_ACC_RE = re.compile(r"^([A-Z0-9]+)\|([A-Za-z0-9_]+)(?:\s*\(([^)]+)\))?")


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(p, header, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})


def parse_accession(s):
    """'P20160|CAP7 (AZU1)' -> (uniprot, entry_name, gene). Gene falls back to entry name."""
    s = (s or "").strip()
    m = _ACC_RE.match(s)
    if not m:
        return "", "", s
    uni, entry, paren = m.group(1), m.group(2), m.group(3)
    gene = (paren or entry or "").strip()
    return uni, entry, gene


def citrulline_site(peptide):
    """Return a compact site descriptor: the residue carrying +.98 (Arg->citrulline)."""
    p = peptide or ""
    # mark of +0.98 (sometimes '+.98'): residue immediately preceding the modification token
    m = re.search(r"([A-Z])\(\+\.?98", p)
    if m:
        return f"{m.group(1)}(+0.98_citrulline)"
    if "+.98" in p or "+0.98" in p:
        return "Arg(+0.98_citrulline)"
    return ""
