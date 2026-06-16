"""03 — Validate the acetylation/methylation PTM evidence keeps the claim ceiling.

Checks forbidden vocabulary in allowed columns, provenance to Table_6 (no fabrication), and
allowed+prohibited presence across parsed entries, module summary and the Tier 2 map rows.
Writes outputs/CHAPMAN_PTM_VALIDATION_REPORT.md.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
PARSED = os.path.join(ROOT, "CHAPMAN_TABLE6_PARSED_PTM.tsv")
SUMM = os.path.join(ROOT, "CHAPMAN_PTM_MODULE_SUMMARY.tsv")
OUTDIR = os.path.join(ROOT, "outputs")
FORBIDDEN = ["hat activity", "hdac activity", "prmt activity", "enzyme activity is", "acetylation rate",
             "methylation rate", "netosis rate", "clearance", "pathogenic", "causal", "causes",
             "metabolism causes", "co-measured", "sample-level fusion", "demonstrates"]


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    parsed = read_tsv(PARSED)
    summ = read_tsv(SUMM)
    checks, problems = [], []

    checks.append(("parsed PTM entries present", bool(parsed)))
    if parsed:
        bad = []
        for r in parsed + summ:
            v = (r.get("allowed_claim", "") or "").lower()
            for t in FORBIDDEN:
                if t in v:
                    bad.append(t)
        checks.append(("no forbidden vocab in allowed claims", not bad))
        if bad:
            problems.append(f"forbidden: {sorted(set(bad))}")
        miss = [r for r in parsed if not r.get("allowed_claim") or not r.get("prohibited_claim")]
        checks.append(("all parsed rows carry allowed + prohibited", not miss))
        noprov = [r for r in parsed if "Table_6" not in (r.get("table_source", ""))]
        checks.append(("every entry traces to Table_6 (no fabrication)", not noprov))
        notier = [r for r in parsed if r.get("evidence_tier") != "Tier_2"]
        checks.append(("parsed rows tagged Tier_2", not notier))
        types = {r.get("ptm_type") for r in parsed}
        checks.append(("only Acetylation/Methylation PTM types", types <= {"Acetylation", "Methylation"}))

    verdict = "CHAPMAN_PTM_VALIDATION_PASS" if (parsed and all(ok for _, ok in checks)) \
        else ("CHAPMAN_PTM_NOT_STRUCTURABLE" if not parsed else "CHAPMAN_PTM_VALIDATION_FAIL")
    lines = ["# Chapman Table_6 Acetylation/Methylation — Validation", "", f"Status: **{verdict}**", "",
             f"Parsed PTM entries: {len(parsed)}", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Note",
              "Structured acetylated/methylated NET/release material (Tier 2 PTM). A PTM "
              "identification is presence on detected material, NOT a rate and NOT evidence of "
              "enzyme (HAT/HDAC/PRMT) activity. Not NETosis rate, clearance, pathogenicity or causality."]
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "CHAPMAN_PTM_VALIDATION_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("[03]", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict.endswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
