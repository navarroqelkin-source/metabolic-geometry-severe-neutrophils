"""04 — Decide whether Chapman upgrades to Tier 2.

CHAPMAN_TIER2_CONFIRMED if a real structured protein table was parsed; otherwise the appropriate
not-upgraded state. Writes CHAPMAN_TIER_UPGRADE_DECISION.md. Claim ceiling unchanged regardless.
"""
import os

import _chap_common as C

PARSED = os.path.join(C.PROCESSED, "CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv")


def main():
    idx = C.read_tsv(C.path("CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv"))
    parsed = C.read_tsv(PARSED)
    downloaded = [r for r in idx if r.get("status") == "DOWNLOADED_TABLE"]
    blocked = [r for r in idx if r.get("status") in ("DOWNLOAD_FAILED",)]

    if parsed:
        status = "CHAPMAN_TIER2_CONFIRMED"
        tier = "Tier_2_SUPPLEMENTARY_TABLE"
    elif blocked and not downloaded:
        status = "CHAPMAN_SUPPLEMENT_ACCESS_BLOCKED"
        tier = "Tier_3_ARTICLE_LEVEL_RESULT"
    elif downloaded and not parsed:
        status = "CHAPMAN_SUPPLEMENT_NOT_STRUCTURABLE"
        tier = "Tier_3_ARTICLE_LEVEL_RESULT"
    else:
        status = "CHAPMAN_REMAINS_TIER3"
        tier = "Tier_3_ARTICLE_LEVEL_RESULT"

    groups = {}
    for r in parsed:
        groups[r["condition_or_group"]] = groups.get(r["condition_or_group"], 0) + 1

    lines = [
        "# Chapman Tier Upgrade Decision", "",
        f"Status: **{status}**", "",
        f"Chapman_PXD011796 evidence_tier = **{tier}**", "",
        f"- Tabular supplements downloaded: {len(downloaded)}",
        f"- Parsed NET proteome rows: {len(parsed)}"
        + (f" ({', '.join(f'{k}={v}' for k,v in groups.items())})" if groups else ""),
        "",
        "## Rationale",
        ("Open-access Frontiers supplementary tables (PMC6421309, CC BY) provide structured NET "
         "proteome composition (gene, UniProt accession, peptide counts, Anova p, q value, fold "
         "change) for healthy-control and RA/SLE NETs. This is a processed supplementary table, "
         "qualifying Tier 2." if parsed else
         "No structurable supplementary protein table could be parsed; Chapman remains Tier 3."),
        "",
        "## Claim ceiling (UNCHANGED)",
        "NET/release material composition only — NOT NETosis rate, clearance, pathogenicity, or "
        "causal metabolism-to-NETosis. A protein inventory is not a rate.",
    ]
    with open(C.path("CHAPMAN_TIER_UPGRADE_DECISION.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[04] {status} -> {tier} (parsed_rows={len(parsed)})")


if __name__ == "__main__":
    main()
