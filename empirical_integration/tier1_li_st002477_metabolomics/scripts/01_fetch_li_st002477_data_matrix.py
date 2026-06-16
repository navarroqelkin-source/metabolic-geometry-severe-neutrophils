"""01 — Fetch ST002477 from Metabolomics Workbench REST and build the real intensity matrix.

Pulls summary, factors, metabolites and the quantitative /data endpoint. Writes:
  - LI_ST002477_DATA_PROVENANCE.tsv   (endpoints, sizes, sha256, retrieved_live)
  - LI_ST002477_SAMPLE_METADATA.tsv   (sample -> group; Blank/QC excluded from biology)
  - LI_ST002477_METABOLITE_TABLE.tsv  (named metabolites + identifiers; no invented chemistry)
  - outputs/LI_ST002477_intensity_matrix.tsv (metabolite_id x sample, MS-reading units)
  - LI_ST002477_INTENSITY_MATRIX_STATUS.tsv
No simulated data: every value is copied verbatim from the REST response. If a fetch fails the
matrix status is recorded as MISSING_MATRIX and downstream scripts degrade safely.
"""
import json
import os
import _li_common as L


def main():
    os.makedirs(L.OUTDIR, exist_ok=True)
    prov = []
    bodies = {}
    for name, url in L.ENDPOINTS.items():
        ok, body = L.fetch(url)
        bodies[name] = body if ok else None
        prov.append({
            "source_id": "Li_ST002477", "repository": "Metabolomics_Workbench",
            "accession": L.STUDY, "data_object": name, "url_or_endpoint": url,
            "local_path": "(in-memory; matrix saved to outputs/)" if name == "data" else "(in-memory)",
            "file_size_bytes": str(len(body)) if ok else "0",
            "sha256": L.sha256_text(body) if ok else "NA",
            "retrieved_live": "YES" if ok else "NO",
            "parse_status": "OK" if ok else "FETCH_FAILED",
            "evidence_tier": "1",
            "notes": "" if ok else f"error: {body[:120]}",
        })
    L.write_tsv(L.path("LI_ST002477_DATA_PROVENANCE.tsv"),
                ["source_id", "repository", "accession", "data_object", "url_or_endpoint",
                 "local_path", "file_size_bytes", "sha256", "retrieved_live", "parse_status",
                 "evidence_tier", "notes"], prov)

    # ---- Sample metadata (from factors) ----
    sample_rows = []
    factor_group = {}
    if bodies.get("factors"):
        for r in L.vals(json.loads(bodies["factors"])):
            sid = r.get("local_sample_id", "")
            grp = (r.get("factors", "") or "").split(":")[-1].strip()
            factor_group[sid] = grp
            include = "YES" if grp in L.BIO_GROUPS else "NO"
            reason = ("biological comparison set" if grp in L.BIO_GROUPS else
                      "Blank = process blank, exclude from biology" if grp == "Blank" else
                      "QC = pooled QC, QC-only use" if grp == "QC" else "unknown group")
            sample_rows.append({
                "sample_id": sid, "group_or_condition": grp,
                "sample_type": r.get("sample_source", ""),
                "include_in_biological_analysis": include, "reason": reason,
            })
    L.write_tsv(L.path("LI_ST002477_SAMPLE_METADATA.tsv"),
                ["sample_id", "group_or_condition", "sample_type",
                 "include_in_biological_analysis", "reason"], sample_rows)

    # ---- Metabolite table (from metabolites) ----
    metab_rows = []
    if bodies.get("metabolites"):
        for it in L.vals(json.loads(bodies["metabolites"])):
            name = it.get("metabolite_name", "")
            if not name:
                continue
            ident = it.get("kegg_id") or it.get("hmdb_id") or it.get("pubchem_id") or ""
            itype = ("KEGG" if it.get("kegg_id") else "HMDB" if it.get("hmdb_id")
                     else "PubChem" if it.get("pubchem_id") else "name_only")
            metab_rows.append({
                "metabolite_id": it.get("metabolite_id", "") or name,
                "metabolite_name": name, "identifier_type": itype,
                "chemical_class_or_pathway_if_available": "",  # not reported -> left blank, not invented
                "source_field": "MW REST /metabolites", "evidence_status": "reported_named_metabolite",
            })
    L.write_tsv(L.path("LI_ST002477_METABOLITE_TABLE.tsv"),
                ["metabolite_id", "metabolite_name", "identifier_type",
                 "chemical_class_or_pathway_if_available", "source_field", "evidence_status"],
                metab_rows)

    # ---- Intensity matrix (from /data) ----
    matrix_found, n_samples, n_metab, reason = "NO", 0, 0, ""
    if bodies.get("data"):
        try:
            data = json.loads(bodies["data"])
            entries = L.vals(data)
            samples = []
            for e in entries:
                for s in (e.get("DATA", {}) or {}).keys():
                    if s not in samples:
                        samples.append(s)
            header = ["metabolite_id", "metabolite_name", "analysis_id", "units"] + samples
            mrows = []
            for e in entries:
                d = e.get("DATA", {}) or {}
                row = {
                    "metabolite_id": e.get("metabolite_id", ""),
                    "metabolite_name": e.get("metabolite_name", ""),
                    "analysis_id": e.get("analysis_id", ""),
                    "units": e.get("units", ""),
                }
                for s in samples:
                    row[s] = d.get(s, "")
                mrows.append(row)
            # write matrix verbatim
            import csv
            with open(os.path.join(L.OUTDIR, "LI_ST002477_intensity_matrix.tsv"),
                      "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", lineterminator="\n")
                w.writeheader()
                w.writerows(mrows)
            matrix_found, n_samples, n_metab = "YES", len(samples), len(mrows)
        except Exception as ex:  # noqa: BLE001
            reason = f"parse_error: {ex}"
    else:
        reason = "data endpoint fetch failed"

    L.write_tsv(L.path("LI_ST002477_INTENSITY_MATRIX_STATUS.tsv"),
                ["source_id", "matrix_found", "endpoint_or_url", "local_path", "n_samples",
                 "n_metabolites", "parse_status", "reason_if_missing", "next_action"],
                [{
                    "source_id": "Li_ST002477", "matrix_found": matrix_found,
                    "endpoint_or_url": L.ENDPOINTS["data"],
                    "local_path": ("outputs/LI_ST002477_intensity_matrix.tsv" if matrix_found == "YES" else ""),
                    "n_samples": str(n_samples), "n_metabolites": str(n_metab),
                    "parse_status": "OK" if matrix_found == "YES" else "MISSING_MATRIX",
                    "reason_if_missing": reason,
                    "next_action": ("run 02_qc" if matrix_found == "YES"
                                    else "retry fetch / consider server for large pulls"),
                }])

    print(f"[01] matrix_found={matrix_found} n_metabolites={n_metab} n_samples={n_samples} "
          f"samples_meta={len(sample_rows)} metabolites_meta={len(metab_rows)}")
    if reason:
        print("     reason:", reason)


if __name__ == "__main__":
    main()
