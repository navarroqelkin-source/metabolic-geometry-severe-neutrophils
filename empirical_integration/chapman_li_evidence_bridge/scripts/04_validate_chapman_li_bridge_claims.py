"""04 — Validate the Chapman–Li bridge stays evidence-tiered (no overclaim).

Scans allowed_synthesis for forbidden notions (incl. NETosis rate / clearance / pathogenicity /
metabolism-to-NETosis), confirms every bridge row carries allowed + prohibited synthesis and only
allowed bridge_type values. Writes CHAPMAN_LI_BRIDGE_VALIDATION_REPORT.md.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE = os.path.join(ROOT, "CHAPMAN_LI_MODULE_BRIDGE.tsv")
OUTDIR = os.path.join(ROOT, "outputs")
ALLOWED_TYPES = {"material_state_alignment", "module_context_alignment",
                 "hypothesis_generating_cross_layer_link"}
# Forbidden notions in allowed_synthesis (negations elsewhere are fine).
FORBIDDEN = ["co-measured", "co-measurement", "correlat", "causal", "causes", "flux",
             "netosis rate", "rate of netosis", "clearance", "pathogenic", "demonstrates netosis",
             "metabolism causes", "biomarker", "predicts severity", "sample-level integration",
             "fusion of samples"]


def read_tsv(p):
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    rows = read_tsv(BRIDGE)
    checks, problems = [], []
    if not rows:
        checks.append(("bridge table present and non-empty", False))
        problems.append("CHAPMAN_LI_MODULE_BRIDGE.tsv missing or empty")
    else:
        checks.append(("bridge table present and non-empty", True))
        bad = []
        for r in rows:
            a = (r.get("allowed_synthesis", "") or "").lower()
            for t in FORBIDDEN:
                if t in a:
                    bad.append((r.get("bridge_id"), t))
        checks.append(("no forbidden notions in allowed_synthesis "
                       "(incl. NETosis rate/clearance/pathogenicity)", not bad))
        if bad:
            problems.append(f"forbidden notions: {bad}")
        miss = [r["bridge_id"] for r in rows if not r.get("allowed_synthesis") or not r.get("prohibited_synthesis")]
        checks.append(("every row has allowed + prohibited synthesis", not miss))
        if miss:
            problems.append(f"rows missing synthesis: {miss}")
        badtype = [r["bridge_id"] for r in rows if r.get("bridge_type") not in ALLOWED_TYPES]
        checks.append(("all bridge_type values are allowed (no fusion/causal types)", not badtype))
        if badtype:
            problems.append(f"disallowed bridge_type: {badtype}")
        weak = [r["bridge_id"] for r in rows
                if any(k not in (r.get("prohibited_synthesis", "").lower())
                       for k in ("sample-level", "causal", "netosis rate", "clearance"))]
        checks.append(("prohibited_synthesis bars sample-level + causal + NETosis-rate + clearance", not weak))
        if weak:
            problems.append(f"prohibited_synthesis too weak: {weak}")

    verdict = "CHAPMAN_LI_BRIDGE_VALIDATION_PASS" if all(ok for _, ok in checks) else "CHAPMAN_LI_BRIDGE_VALIDATION_FAIL"
    lines = ["# Chapman–Li Bridge — Validation Report", "", f"Status: **{verdict}**", "",
             f"Bridges checked: {len(rows) if rows else 0}", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Note",
              "The bridge is an evidence-tiered synthesis linking independent NET/release proteome "
              "composition (Chapman, Tier 3) with an independent Tier 1 metabolomic severity-state "
              "axis (Li_ST002477). It is NOT a sample-level integration, co-measurement, NETosis-rate, "
              "clearance, pathogenicity or causal claim."]
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "CHAPMAN_LI_BRIDGE_VALIDATION_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("[04]", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict.endswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
