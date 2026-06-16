"""01 — Structured Chapman PXD011796 evidence for the bridge.

Reuses the verified Chapman extraction (../../evidence_tiered_extraction/), re-encoding the
NET/release proteome composition into the bridge schema. Light PRIDE re-confirmation when network
is available. Claim ceiling: NET material/release composition, not NET formation rate, clearance or
pathogenicity. evidence_tier stays Tier_3 unless a processed supplement table is parsed (Tier_2).
"""
import csv
import os
from urllib.request import urlopen, Request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
SRC_TABLE = os.path.join(EMP, "evidence_tiered_extraction", "SOURCE_LEVEL_EVIDENCE_TABLE.tsv")
ART_TABLE = os.path.join(EMP, "evidence_tiered_extraction", "ARTICLE_LEVEL_RESULT_TABLE.tsv")
CITE = "PXD011796;PMID_30915077;DOI_10.3389/fimmu.2019.00423"
CEIL = "NET material or release proteome composition, not NET formation rate, clearance or pathogenicity"


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def confirm():
    try:
        req = Request("https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD011796",
                      headers={"User-Agent": "cosmos-bridge/1.0"})
        with urlopen(req, timeout=20) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    src = [r for r in read_tsv(SRC_TABLE) if r.get("source_id") == "Chapman_PXD011796"]
    art = [r for r in read_tsv(ART_TABLE) if r.get("source_id") == "Chapman_PXD011796"]
    live = confirm()

    out = []
    for r in src:
        out.append({
            "source_id": "Chapman_PXD011796", "evidence_tier": "Tier_" + r.get("evidence_tier", "3"),
            "evidence_item": r.get("evidence_item", ""), "item_type": r.get("item_type", ""),
            "protein_or_feature": r.get("molecular_entities", ""),
            "context": r.get("condition_or_context", ""),
            "reported_metric_or_status": r.get("reported_statistic_or_metric", ""),
            "allowed_claim": r.get("allowed_claim", "NET/release material composition"),
            "prohibited_claim": r.get("prohibited_claim", "NET formation rate, clearance or pathogenicity"),
            "citation_or_identifier": r.get("citation_or_identifier", CITE),
        })
    for a in art:
        out.append({
            "source_id": "Chapman_PXD011796", "evidence_tier": "Tier_" + a.get("evidence_tier", "3"),
            "evidence_item": a.get("reported_finding", ""), "item_type": "article_result",
            "protein_or_feature": a.get("entities_or_features", ""),
            "context": a.get("context", ""),
            "reported_metric_or_status": f"extraction_confidence={a.get('extraction_confidence','')}; "
            + ("PRIDE reachable (live)" if live else "not re-confirmed (offline)"),
            "allowed_claim": "reported NET protein composition differences across HC/RA/SLE",
            "prohibited_claim": "NETosis rate / clearance / pathogenicity / executed function",
            "citation_or_identifier": CITE,
        })

    header = ["source_id", "evidence_tier", "evidence_item", "item_type", "protein_or_feature",
              "context", "reported_metric_or_status", "allowed_claim", "prohibited_claim",
              "citation_or_identifier"]
    with open(os.path.join(ROOT, "CHAPMAN_EVIDENCE_EXTRACTION.tsv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(out)
    tiers = sorted({r["evidence_tier"] for r in out})
    print(f"[01] Chapman evidence rows={len(out)} tiers={tiers} live_confirm={'YES' if live else 'NO'}")


if __name__ == "__main__":
    main()
