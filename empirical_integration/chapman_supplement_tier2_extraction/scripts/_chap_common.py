"""Shared helpers for the Chapman supplement Tier 2 extraction. stdlib + openpyxl."""
import csv
import hashlib
import os
from urllib.request import urlopen, Request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
RAW = os.path.join(ROOT, "raw")
PROCESSED = os.path.join(ROOT, "processed")
OUTDIR = os.path.join(ROOT, "outputs")

PMCID = "PMC6421309"
PMID = "30915077"
DOI = "10.3389/fimmu.2019.00423"
CITE = f"PXD011796;PMID_{PMID};DOI_{DOI};PMCID_{PMCID}"
SUPP_ZIP_URL = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles"
# Cached open-access bundle (CC BY) saved under raw/ for reproducibility when the live endpoint
# (which is intermittently flaky with HTTP 500/timeouts) is unavailable.
CACHED_BUNDLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "raw", "PMC6421309_supplementaryFiles.zip")
# NET proteome composition tables to parse (gene/accession/quant columns).
NET_TABLES = {
    "Table_2.XLSX": "healthy_control",
    "Table_4.XLSX": "RA_SLE_patient",
}
CEIL_ALLOWED = "NET/release material composition (structured supplementary table)"
CEIL_PROHIBITED = "NETosis rate / clearance / pathogenicity / causal metabolism-to-NETosis / raw reanalysis"


def path(*p):
    return os.path.join(ROOT, *p)


def fetch_bytes(url, timeout=120, tries=3):
    last = "n/a"
    for _ in range(tries):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 cosmos-research"})
            with urlopen(req, timeout=timeout) as r:
                data = r.read()
                if data:
                    return data, ""
        except Exception as e:  # noqa: BLE001
            last = str(e)
    return None, last


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


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
