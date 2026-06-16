"""05 — Validate the parsed Chapman supplement keeps the claim ceiling.

Confirms no NETosis-rate/clearance/pathogenicity/causal/metabolism-to-NETosis/raw-reanalysis
language in allowed_claim, and that every parsed row carries allowed_claim + prohibited_claim.
Writes outputs/CHAPMAN_SUPPLEMENT_VALIDATION_REPORT.md.
"""
import os

import _chap_common as C

PARSED = os.path.join(C.PROCESSED, "CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv")
FORBIDDEN = ["netosis rate", "rate of netosis", "clearance", "pathogenic", "causal", "causes",
             "metabolism causes", "raw reanalysis", "reanalysis of raw", "flux", "biomarker"]


def main():
    rows = C.read_tsv(PARSED)
    checks, problems = [], []

    checks.append(("parsed NET proteome table present", bool(rows)))
    if rows:
        bad = []
        for r in rows:
            a = (r.get("allowed_claim", "") or "").lower()
            for t in FORBIDDEN:
                if t in a:
                    bad.append(t)
        checks.append(("no forbidden notions in allowed_claim", not bad))
        if bad:
            problems.append(f"forbidden in allowed_claim: {sorted(set(bad))}")
        miss = [i for i, r in enumerate(rows)
                if not r.get("allowed_claim") or not r.get("prohibited_claim")]
        checks.append(("every row has allowed + prohibited claim", not miss))
        if miss:
            problems.append(f"{len(miss)} rows missing claim columns")
        # tier is Tier_2 on parsed rows
        non2 = [r for r in rows if r.get("evidence_tier") != "Tier_2"]
        checks.append(("parsed rows tagged Tier_2", not non2))
        # prohibited_claim explicitly bars NETosis rate + clearance
        weak = [r for r in rows if "netosis rate" not in (r.get("prohibited_claim", "").lower())
                or "clearance" not in (r.get("prohibited_claim", "").lower())]
        checks.append(("prohibited_claim bars NETosis-rate + clearance", not weak))

    verdict = "CHAPMAN_SUPPLEMENT_VALIDATION_PASS" if all(ok for _, ok in checks) and rows \
        else ("CHAPMAN_SUPPLEMENT_VALIDATION_PASS" if all(ok for _, ok in checks) else "CHAPMAN_SUPPLEMENT_VALIDATION_FAIL")
    lines = ["# Chapman Supplement — Claim Validation", "", f"Status: **{verdict}**", "",
             f"Parsed NET proteome rows: {len(rows)}", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Note",
              "Structured NET/release proteome composition (Tier 2). NOT NETosis rate, clearance, "
              "pathogenicity, or causal metabolism-to-NETosis; no raw reanalysis was performed."]
    os.makedirs(C.OUTDIR, exist_ok=True)
    with open(os.path.join(C.OUTDIR, "CHAPMAN_SUPPLEMENT_VALIDATION_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("[05]", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict.endswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
