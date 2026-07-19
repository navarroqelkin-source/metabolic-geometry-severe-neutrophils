"""Regression test: the status table must stay readable by the real parser.

A human-readable banner was once prepended to KERNEL_ANALYSIS_STATUS.tsv. csv.DictReader has no
comment support, so the banner became the header row and read_tsv() returned garbage. The public
correction simultaneously left the withdrawn verdict active AND broke reproducible reading.
Never put comment banners in a TSV that code consumes.
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ("  " + detail if detail else ""))
    if not ok:
        FAILED.append(name)

def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

status = os.path.join(HERE, "..", "KERNEL_ANALYSIS_STATUS.tsv")
rows = read(status)
check("status_schema_intact",
      rows and set(rows[0].keys()) == {"step", "status", "detail"},
      str(sorted(rows[0].keys())) if rows else "no rows")
check("no_comment_banner_in_header",
      rows and not any(str(k).lstrip().startswith("#") for k in rows[0].keys()))
check("every_row_has_step", all(r.get("step") for r in rows))
check("no_active_ordering_ok_true",
      not any("ordering_ok=true" in str(r.get("detail", "")).lower()
              and not str(r.get("step", "")).startswith("legacy") for r in rows))

cur = os.path.join(HERE, "..", "CURRENT_SCIENTIFIC_STATUS_V1.tsv")
crows = read(cur)
check("current_status_present", len(crows) > 0, str(len(crows)) + " rows")
check("ordering_marked_superseded",
      all(r["current_status"] == "SUPERSEDED_NOT_EVALUABLE"
          for r in crows if r["analysis_scope"] == "cross_pair_ordering"))

sys.exit(1 if FAILED else 0)
