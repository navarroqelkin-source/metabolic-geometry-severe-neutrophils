"""03 — Parse the downloaded NET proteome tables into a structured TSV.

Parses Table_2.XLSX (healthy control, 272 proteins) and Table_4.XLSX (RA/SLE, 480 proteins).
Header is the second row (first row is the table title). Columns: ID, Description, Accession,
Peptide count, Unique peptides, Anova (p), q Value, Max fold change. No OCR. No raw reanalysis.
Writes processed/CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv. If no table exists, writes nothing false.
"""
import os

import openpyxl

import _chap_common as C

CONTEXT = "NET proteome (PMA/A23187-induced NETs)"


def parse_table(local_path, group):
    wb = openpyxl.load_workbook(local_path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    # find header row (contains 'Accession')
    hidx = next((i for i, r in enumerate(rows)
                 if r and any(str(c).strip().lower() == "accession" for c in r if c is not None)), None)
    if hidx is None:
        return []
    header = [str(c).strip() if c is not None else "" for c in rows[hidx]]
    col = {h.lower(): j for j, h in enumerate(header)}
    out = []
    for r in rows[hidx + 1:]:
        if not r or all(c is None for c in r):
            continue
        def g(key):
            j = col.get(key)
            return "" if j is None or j >= len(r) or r[j] is None else str(r[j]).strip()
        gene = g("id")
        acc = g("accession")
        if not gene and not acc:
            continue
        metric = (f"peptides={g('peptide count')};unique={g('unique peptides')};"
                  f"Anova_p={g('anova (p)')};q={g('q value')};max_fold={g('max fold change')}")
        out.append({
            "source_id": "Chapman_PXD011796",
            "protein_or_peptide": gene or acc,
            "identifier_type": f"UniProt:{acc}" if acc else "gene_symbol",
            "condition_or_group": group,
            "NET_or_release_context": CONTEXT,
            "reported_metric_or_status": metric,
            "table_source": os.path.basename(local_path),
            "evidence_tier": "Tier_2",
            "allowed_claim": C.CEIL_ALLOWED,
            "prohibited_claim": C.CEIL_PROHIBITED,
        })
    return out


def main():
    idx = C.read_tsv(C.path("CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv"))
    available = {r["supplement_file"]: r for r in idx if r.get("status") == "DOWNLOADED_TABLE"}
    all_rows = []
    for fname, group in C.NET_TABLES.items():
        rec = available.get(fname)
        local = os.path.join(C.RAW, fname)
        if not rec or not os.path.exists(local):
            print(f"[03] {fname} not available — skipped (no false output)")
            continue
        parsed = parse_table(local, group)
        print(f"[03] {fname} ({group}): parsed {len(parsed)} proteins")
        all_rows.extend(parsed)

    if not all_rows:
        print("[03] no structurable table parsed — no output written")
        return
    os.makedirs(C.PROCESSED, exist_ok=True)
    C.write_tsv(os.path.join(C.PROCESSED, "CHAPMAN_NET_RELEASE_PROTEOME_TABLE.tsv"),
                ["source_id", "protein_or_peptide", "identifier_type", "condition_or_group",
                 "NET_or_release_context", "reported_metric_or_status", "table_source",
                 "evidence_tier", "allowed_claim", "prohibited_claim"], all_rows)
    by_group = {}
    for r in all_rows:
        by_group[r["condition_or_group"]] = by_group.get(r["condition_or_group"], 0) + 1
    print(f"[03] TOTAL rows={len(all_rows)} by_group={by_group}")


if __name__ == "__main__":
    main()
