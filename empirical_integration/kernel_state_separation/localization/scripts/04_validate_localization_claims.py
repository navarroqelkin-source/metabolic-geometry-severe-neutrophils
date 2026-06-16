"""04 — Validate that localization outputs stay descriptive (no overclaim).

Scans the generated result tables' interpretation/claim columns for forbidden vocabulary,
confirms every row carries allowed + prohibited interpretation, and that module claims remain
descriptive. Writes LI_ST002477_LOCALIZATION_VALIDATION_REPORT.md.
"""
import csv
import os
import _loc_common as L

FORBIDDEN_IN_ALLOWED = ["biomarker", "predict", "prognos", "diagnos", "flux", "causal",
                        "causes", "driver", "mechanism", "executed function", "netosis"]
FILES = [
    ("LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv",
     ["allowed_interpretation"], ["allowed_interpretation", "prohibited_interpretation"]),
    ("outputs/LI_ST002477_FEATURE_STABILITY.tsv",
     ["allowed_interpretation"], ["allowed_interpretation"]),
    ("outputs/LI_ST002477_MODULE_LEVEL_SUMMARY.tsv",
     ["allowed_claim"], ["allowed_claim", "prohibited_claim"]),
]


def load(fname):
    p = L.locpath(*fname.split("/"))
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    checks, problems = [], []
    for fname, allowed_cols, required_cols in FILES:
        rows = load(fname)
        if rows is None:
            checks.append((f"{fname} present", False))
            problems.append(f"{fname}: missing")
            continue
        checks.append((f"{fname} present", True))
        # forbidden vocab in allowed columns
        bad = []
        for r in rows:
            for c in allowed_cols:
                val = (r.get(c, "") or "").lower()
                for term in FORBIDDEN_IN_ALLOWED:
                    if term in val:
                        bad.append((c, term))
        checks.append((f"{fname}: no forbidden vocab in allowed-claim", not bad))
        if bad:
            problems.append(f"{fname}: forbidden in allowed -> {set(bad)}")
        # required interpretation columns populated
        missing = [r for r in rows if any(not r.get(c) for c in required_cols)]
        checks.append((f"{fname}: all rows carry interpretation cols", not missing))
        if missing:
            problems.append(f"{fname}: {len(missing)} rows missing interpretation cols")

    # module claims remain descriptive
    mods = load("outputs/LI_ST002477_MODULE_LEVEL_SUMMARY.tsv") or []
    nondesc = [m for m in mods if "flux" in (m.get("allowed_claim", "").lower())
               or "mechanism" in (m.get("allowed_claim", "").lower())]
    checks.append(("module claims remain descriptive", not nondesc))

    verdict = "LOCALIZATION_VALIDATION_PASS" if all(ok for _, ok in checks) else "LOCALIZATION_VALIDATION_FAIL"
    lines = ["# Li ST002477 — Localization Claim Validation", "", f"Status: **{verdict}**", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Note",
              "Localization is descriptive and post hoc: candidate state-associated metabolites and "
              "module-level associations only. No biomarker, flux, causal, prediction or executed-function "
              "claim; no pan-omic sample-level fusion."]
    os.makedirs(L.OUTDIR, exist_ok=True)
    with open(L.locpath("outputs", "LI_ST002477_LOCALIZATION_VALIDATION_REPORT.md"),
              "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    L.set_status("validation", verdict, f"{sum(1 for _,ok in checks if ok)}/{len(checks)} checks pass")
    print("[04]", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict.endswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
