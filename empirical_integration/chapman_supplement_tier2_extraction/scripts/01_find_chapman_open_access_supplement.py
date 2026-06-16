"""01 — Locate the Chapman open-access supplement.

Resolves the article (PMID 30915077 -> PMCID PMC6421309, CC BY) and records the open-access
supplementary tables and their bundle URL. Light live check that the bundle is reachable.
Writes CHAPMAN_SUPPLEMENT_SEARCH.tsv.
"""
import _chap_common as C

QUERIES = [
    "PXD011796",
    "Chapman NET proteome Front Immunol 2019",
    "NET proteome rheumatoid arthritis lupus citrullinated peptides",
]
# Known open-access supplementary tables (Frontiers data sheets, hosted via Europe PMC bundle).
TABLES = [
    ("Table_1.XLSX", "patient clinical demographics", "context"),
    ("Table_2.XLSX", "NET proteins identified in healthy controls (272 proteins)", "NET_proteome"),
    ("Table_3.XLSX", "proteins differing PMA vs A23187 NETs (healthy)", "NET_proteome_contrast"),
    ("Table_4.XLSX", "complete NET protein dataset RA and SLE (480 proteins)", "NET_proteome"),
    ("Table_5.XLSX", "proteins differing across RA/SLE x PMA/A23187", "NET_proteome_contrast"),
    ("Table_6.XLSX", "PTMs (citrullination/acetylation/methylation) on NET proteins", "NET_PTM"),
    ("Table_7.xlsx", "all peptides with PTMs across RA and SLE", "NET_PTM_peptides"),
]


def main():
    import os
    reachable = os.path.exists(C.CACHED_BUNDLE)
    err = ""
    if not reachable:
        data, err = C.fetch_bytes(C.SUPP_ZIP_URL, timeout=60, tries=2)
        reachable = data is not None and len(data) > 1000
    status = "FOUND_DIRECT_SUPPLEMENT" if reachable else "FOUND_ARTICLE_SUPPLEMENT_PAGE"
    rows = []
    art_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{C.PMCID}/"
    for fname, desc, _ctx in TABLES:
        rows.append({
            "source_id": "Chapman_PXD011796",
            "search_query": "; ".join(QUERIES),
            "article_or_repository_url": art_url,
            "supplement_url": C.SUPP_ZIP_URL,
            "file_name": fname, "file_type": "xlsx",
            "access_status": status if reachable else "NEEDS_VERIFICATION",
            "download_allowed": "YES",
            "required_action": "download bundle and extract this table" if reachable
                               else "retry bundle fetch / verify access",
        })
    C.write_tsv(C.path("CHAPMAN_SUPPLEMENT_SEARCH.tsv"),
                ["source_id", "search_query", "article_or_repository_url", "supplement_url",
                 "file_name", "file_type", "access_status", "download_allowed", "required_action"],
                rows)
    print(f"[01] PMCID={C.PMCID} bundle_reachable={reachable} tables_listed={len(rows)} "
          + ("" if reachable else f"(err: {err[:80]})"))


if __name__ == "__main__":
    main()
