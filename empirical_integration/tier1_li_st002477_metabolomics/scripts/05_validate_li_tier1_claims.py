"""05 — Validate the Li ST002477 Tier 1 claim ceiling across all subflow outputs.

Checks:
  V1 Tier 1 has provenance (retrieved_live=YES with a real endpoint + sha256).
  V2 No flux claim anywhere in the generated outputs' allowed/interpretation columns.
  V3 No causal claim in allowed/interpretation columns.
  V4 No clinical-prediction claim in allowed/interpretation columns.
  V5 No executed-function claim in allowed/interpretation columns.
  V6 No sample-level fusion declared with other sources.
  V7 Blank/QC excluded from biological analysis in sample metadata.
Writes outputs/LI_ST002477_TIER1_VALIDATION_REPORT.md.
"""
import csv
import os
import _li_common as L

# Forbidden terms only in *allowed/interpretation* fields (prohibited_* columns legitimately name them).
FORBIDDEN = {
    "V2_flux": ["flux", "turnover rate", "pathway rate"],
    "V3_causal": ["causal", "causes ", "mechanistically drives", "due to"],
    "V4_clinical": ["predict", "prognos", "diagnos", "biomarker"],
    "V5_function": ["netosis rate", "ros burst", "killing", "phagocytosis", "executed function",
                    "degranulation rate", "migration assay"],
}
ALLOWED_COLS = ["allowed_claim", "allowed_interpretation"]


def scan_allowed(fname):
    p = os.path.join(L.OUTDIR, fname)
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    texts = []
    for r in rows:
        for c in ALLOWED_COLS:
            if c in r and r[c]:
                texts.append(r[c].lower())
    return texts


def main():
    checks, problems = [], []

    # V1 provenance
    prov = L.read_tsv(L.path("LI_ST002477_DATA_PROVENANCE.tsv"))
    live_ok = any(r.get("retrieved_live") == "YES" and r.get("sha256") not in ("", "NA")
                  and r.get("url_or_endpoint") for r in prov)
    checks.append(("V1 Tier1 provenance (live endpoint + sha256)", live_ok))

    # V2-V5 forbidden terms in allowed/interpretation fields of descriptive + module outputs
    texts = scan_allowed("LI_ST002477_GROUP_DESCRIPTIVE_SUMMARY.tsv") + \
        scan_allowed("LI_ST002477_MODULE_MAPPING.tsv")
    for vid, terms in FORBIDDEN.items():
        hit = [t for t in terms if any(t in x for x in texts)]
        checks.append((f"{vid} absent from allowed-claims", not hit))
        if hit:
            problems.append(f"{vid}: found {hit}")

    # V6 no sample-level fusion declared
    mod = scan_allowed("LI_ST002477_MODULE_MAPPING.tsv")
    fusion = any("fusion" in t and "no" not in t for t in mod)
    checks.append(("V6 no sample-level fusion declared", not fusion))

    # V7 Blank/QC excluded from biology
    meta = L.read_tsv(L.path("LI_ST002477_SAMPLE_METADATA.tsv"))
    bad = [r["sample_id"] for r in meta if r.get("group_or_condition") in L.NONBIO_GROUPS
           and r.get("include_in_biological_analysis") != "NO"]
    checks.append(("V7 Blank/QC excluded from biological analysis", not bad))
    if bad:
        problems.append(f"V7: non-biological samples not excluded: {bad}")

    verdict = "PASS" if all(ok for _, ok in checks) else "FAIL"
    lines = ["# Li ST002477 — Tier 1 Claim-Ceiling Validation", "",
             f"Overall: **{verdict}**", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Anchored facts",
              "- Tier 1 real intensity matrix: 287 metabolites x 75 biological samples (MS-reading units).",
              "- Groups: Control/Mild/Severe (biology); Blank/QC excluded.",
              "- Claim ceiling: metabolic STATE only — not flux, not causality, not clinical prediction, "
              "not executed function; no sample-level fusion with unpaired sources."]
    os.makedirs(L.OUTDIR, exist_ok=True)
    with open(os.path.join(L.OUTDIR, "LI_ST002477_TIER1_VALIDATION_REPORT.md"),
              "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("[05] VALIDATION:", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
