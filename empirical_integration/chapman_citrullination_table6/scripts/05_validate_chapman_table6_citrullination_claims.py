"""05 — Validate citrullination evidence + bridge keep the claim ceiling and fabricate nothing.

Checks forbidden vocabulary in allowed columns, presence of allowed+prohibited claims, that every
parsed entry traces to Table_6, and that the bridge bars rate/PAD4/NETosis/clearance/causal/fusion.
Writes outputs/CHAPMAN_TABLE6_CITRULLINATION_VALIDATION_REPORT.md.
"""
import os

import _cit_common as C

PARSED = os.path.join(C.ROOT, "CHAPMAN_TABLE6_PARSED_CITRULLINATION.tsv")
BRIDGE = os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_BRIDGE_UPDATE.tsv")
FORBIDDEN = ["citrullination rate", "pad4 activity", "pad4 rate", "netosis rate", "clearance",
             "pathogenic", "causal", "causes", "metabolism causes", "co-measured", "co-measurement",
             "sample-level fusion", "fusion of samples", "demonstrates citrullination"]


def main():
    parsed = C.read_tsv(PARSED)
    bridge = C.read_tsv(BRIDGE)
    checks, problems = [], []

    structurable = bool(parsed)
    checks.append(("citrullinated entries parsed (structurable)", structurable))

    if structurable:
        # forbidden vocab in allowed columns
        bad = []
        for r in parsed:
            v = (r.get("allowed_claim", "") or "").lower()
            for t in FORBIDDEN:
                if t in v:
                    bad.append(("parsed", t))
        for r in bridge:
            v = (r.get("allowed_synthesis", "") or "").lower()
            for t in FORBIDDEN:
                if t in v:
                    bad.append(("bridge", t))
        checks.append(("no forbidden vocab in allowed columns", not bad))
        if bad:
            problems.append(f"forbidden: {sorted(set(bad))}")
        # allowed + prohibited present
        miss = [r for r in parsed if not r.get("allowed_claim") or not r.get("prohibited_claim")]
        miss += [r for r in bridge if not r.get("allowed_synthesis") or not r.get("prohibited_synthesis")]
        checks.append(("all rows carry allowed + prohibited", not miss))
        # provenance: every parsed entry cites Table_6
        noprov = [r for r in parsed if "Table_6" not in (r.get("table_source", ""))]
        checks.append(("every citrullinated entry traces to Table_6 (no fabrication)", not noprov))
        # bridge prohibitions
        weak = [r for r in bridge if any(k not in (r.get("prohibited_synthesis", "").lower())
                for k in ("citrullination rate", "netosis rate", "clearance", "causal", "sample-level fusion"))]
        checks.append(("bridge bars rate/NETosis/clearance/causal/fusion", not weak))

    if not structurable:
        verdict = "CHAPMAN_TABLE6_NOT_STRUCTURABLE"
    elif all(ok for _, ok in checks):
        verdict = "CHAPMAN_TABLE6_CITRULLINATION_VALIDATION_PASS"
    else:
        verdict = "CHAPMAN_TABLE6_CITRULLINATION_VALIDATION_FAIL"

    lines = ["# Chapman Table_6 Citrullination — Validation", "", f"Status: **{verdict}**", "",
             f"Parsed citrullinated entries: {len(parsed)}", "", "## Checks"]
    for name, ok in checks:
        lines.append(f"- {'PASS' if ok else 'FAIL'} — {name}")
    if problems:
        lines += ["", "## Problems"] + [f"- {p}" for p in problems]
    lines += ["", "## Note",
              "Structured citrullinated NET/release material (Tier 2 PTM). Detection counts are "
              "presence counts, not rates. Not citrullination rate, PAD4 activity, NETosis rate, "
              "clearance, pathogenicity or causal metabolism-to-citrullination; no sample-level fusion."]
    os.makedirs(C.OUTDIR, exist_ok=True)
    with open(os.path.join(C.OUTDIR, "CHAPMAN_TABLE6_CITRULLINATION_VALIDATION_REPORT.md"),
              "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("[05]", verdict)
    for name, ok in checks:
        print(f"   {'PASS' if ok else 'FAIL'} {name}")
    if verdict.endswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
