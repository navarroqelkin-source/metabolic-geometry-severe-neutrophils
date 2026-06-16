"""02 — Minimal QC of the real ST002477 intensity matrix.

Counts samples/metabolites, verifies groups, separates Blank/QC, counts missing values and
detects non-numeric cells. Writes outputs/LI_ST002477_QC_SUMMARY.tsv and LI_ST002477_QC_REPORT.md.
If the matrix is missing, records MISSING_MATRIX and exits without failing destructively.
"""
import csv
import os
import _li_common as L

MATRIX = os.path.join(L.OUTDIR, "LI_ST002477_intensity_matrix.tsv")
META = ["metabolite_id", "metabolite_name", "analysis_id", "units"]


def main():
    status = L.read_tsv(L.path("LI_ST002477_INTENSITY_MATRIX_STATUS.tsv"))
    found = status and status[0].get("matrix_found") == "YES" and os.path.exists(MATRIX)
    if not found:
        L.write_tsv(os.path.join(L.OUTDIR, "LI_ST002477_QC_SUMMARY.tsv"),
                    ["metric", "value"], [{"metric": "status", "value": "MISSING_MATRIX"}])
        with open(L.path("LI_ST002477_QC_REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write("# Li ST002477 QC Report\n\nStatus: **MISSING_MATRIX** — no intensity "
                     "matrix available; QC skipped. No data fabricated.\n")
        print("[02] MISSING_MATRIX — QC skipped safely.")
        return

    with open(MATRIX, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    header = list(rows[0].keys()) if rows else []
    samples = [c for c in header if c not in META]

    meta = {r["sample_id"]: r for r in L.read_tsv(L.path("LI_ST002477_SAMPLE_METADATA.tsv"))}
    group_of = {s: meta.get(s, {}).get("group_or_condition", "UNKNOWN") for s in samples}
    group_counts = {}
    for s in samples:
        group_counts[group_of[s]] = group_counts.get(group_of[s], 0) + 1

    n_cells = len(rows) * len(samples)
    n_missing = n_nonnumeric = 0
    for r in rows:
        for s in samples:
            v = (r.get(s, "") or "").strip()
            if v == "":
                n_missing += 1
                continue
            try:
                float(v)
            except ValueError:
                n_nonnumeric += 1

    bio = [s for s in samples if group_of[s] in L.BIO_GROUPS]
    nonbio = [s for s in samples if group_of[s] in L.NONBIO_GROUPS]
    meta_total = len(meta)
    meta_blank = sum(1 for r in meta.values() if r["group_or_condition"] == "Blank")
    meta_qc = sum(1 for r in meta.values() if r["group_or_condition"] == "QC")

    summary = [
        {"metric": "status", "value": "OK"},
        {"metric": "n_metabolites", "value": len(rows)},
        {"metric": "n_samples_in_matrix", "value": len(samples)},
        {"metric": "n_samples_in_metadata", "value": meta_total},
        {"metric": "n_biological_samples_in_matrix", "value": len(bio)},
        {"metric": "n_nonbiological_samples_in_matrix", "value": len(nonbio)},
        {"metric": "blank_samples_in_metadata", "value": meta_blank},
        {"metric": "qc_samples_in_metadata", "value": meta_qc},
        {"metric": "group_counts_in_matrix", "value": "; ".join(f"{k}:{v}" for k, v in sorted(group_counts.items()))},
        {"metric": "total_data_cells", "value": n_cells},
        {"metric": "missing_value_cells", "value": n_missing},
        {"metric": "missing_fraction", "value": round(n_missing / n_cells, 4) if n_cells else 0},
        {"metric": "nonnumeric_cells", "value": n_nonnumeric},
    ]
    L.write_tsv(os.path.join(L.OUTDIR, "LI_ST002477_QC_SUMMARY.tsv"), ["metric", "value"], summary)

    lines = [
        "# Li ST002477 QC Report", "", "Status: **OK** (real intensity matrix)", "",
        f"- Metabolites: {len(rows)}",
        f"- Samples in matrix: {len(samples)} (biological={len(bio)}, non-biological={len(nonbio)})",
        f"- Samples in metadata: {meta_total} (Blank={meta_blank}, QC={meta_qc})",
        f"- Group counts in matrix: {', '.join(f'{k}={v}' for k, v in sorted(group_counts.items()))}",
        f"- Data cells: {n_cells}; missing: {n_missing} ({round(100*n_missing/n_cells,2) if n_cells else 0}%); "
        f"non-numeric: {n_nonnumeric}", "",
        "## QC notes",
        "- The MW `/data` quantitative table contains only the biological samples "
        f"(Control/Mild/Severe = {len(bio)}); Blank ({meta_blank}) and QC ({meta_qc}) appear in the "
        "factor sheet but are not present in the quantitative matrix.",
        "- All Blank/QC are excluded from biological contrasts by `LI_ST002477_SAMPLE_METADATA.tsv`.",
        "- Values are MS-reading intensities (relative), suitable for STATE comparison only — not flux.",
    ]
    with open(L.path("LI_ST002477_QC_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"[02] OK metabolites={len(rows)} samples={len(samples)} bio={len(bio)} "
          f"missing={n_missing} nonnumeric={n_nonnumeric}")


if __name__ == "__main__":
    main()
