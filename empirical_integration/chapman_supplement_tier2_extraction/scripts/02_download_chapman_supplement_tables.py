"""02 — Download the open-access supplement bundle and extract only tabular tables.

Downloads the Europe PMC supplementary-files zip for PMC6421309 (CC BY, ~11.6 MB, clear index),
extracts only Table_*.XLSX/.xlsx members into raw/ (images and any raw/vendor files are ignored),
and records size + sha256 per table. Writes CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv.
No raw proteomics, no mzML/mgf/vendor files.
"""
import io
import os
import zipfile

import _chap_common as C

ALLOWED_EXT = (".xlsx", ".xls", ".csv", ".tsv", ".txt")
FORBIDDEN_EXT = (".raw", ".mzml", ".mgf", ".d", ".wiff", ".tiff", ".tif", ".jpg", ".jpeg", ".gif", ".png")


def main():
    os.makedirs(C.RAW, exist_ok=True)
    rows = []
    # Prefer a cached open-access bundle (reproducible) if present; else download live (with retries).
    source = "live"
    if os.path.exists(C.CACHED_BUNDLE):
        with open(C.CACHED_BUNDLE, "rb") as fh:
            data = fh.read()
        err = ""
        source = "cached_bundle"
    else:
        data, err = C.fetch_bytes(C.SUPP_ZIP_URL, timeout=180, tries=6)
        if data is not None and len(data) > 1000:
            with open(C.CACHED_BUNDLE, "wb") as fh:   # cache for reproducibility
                fh.write(data)
    print(f"[02] bundle source={source} bytes={0 if data is None else len(data)}")
    header = ["source_id", "supplement_file", "local_path", "file_type", "file_size_bytes",
              "sha256", "table_detected", "table_description", "parse_allowed", "status",
              "required_action"]
    if data is None or len(data) < 1000:
        C.write_tsv(C.path("CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv"), header, [{
            "source_id": "Chapman_PXD011796", "supplement_file": "(bundle)",
            "local_path": "", "file_type": "zip", "file_size_bytes": "0", "sha256": "",
            "table_detected": "NO", "table_description": f"download failed: {err[:80]}",
            "parse_allowed": "NO", "status": "DOWNLOAD_FAILED",
            "required_action": "retry bundle fetch / verify access"}])
        print("[02] DOWNLOAD_FAILED:", err[:120])
        return
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        C.write_tsv(C.path("CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv"), header, [{
            "source_id": "Chapman_PXD011796", "supplement_file": "(bundle)", "status": "DOWNLOAD_FAILED",
            "table_detected": "NO", "table_description": "not a zip", "parse_allowed": "NO",
            "required_action": "verify endpoint"}])
        print("[02] bundle is not a zip")
        return

    desc = {t: d for t, (d, _ctx) in
            {"Table_2.XLSX": ("NET proteins healthy control (272)", ""),
             "Table_4.XLSX": ("NET proteins RA/SLE (480)", ""),
             "Table_6.XLSX": ("PTMs incl. citrullination", ""),
             "Table_1.XLSX": ("patient demographics", ""),
             "Table_3.XLSX": ("PMA vs A23187 contrast (healthy)", ""),
             "Table_5.XLSX": ("RA/SLE x PMA/A23187 contrast", ""),
             "Table_7.xlsx": ("PTM peptides", "")}.items()}

    for name in z.namelist():
        low = name.lower()
        if low.endswith(FORBIDDEN_EXT):
            continue
        if not low.endswith(ALLOWED_EXT):
            continue
        if not os.path.basename(low).startswith("table_"):
            continue
        content = z.read(name)
        base = os.path.basename(name)
        local = os.path.join(C.RAW, base)
        with open(local, "wb") as fh:
            fh.write(content)
        is_net = base in C.NET_TABLES or base in ("Table_6.XLSX",)
        rows.append({
            "source_id": "Chapman_PXD011796", "supplement_file": base,
            "local_path": os.path.relpath(local, C.EMP).replace(os.sep, "/"),
            "file_type": base.rsplit(".", 1)[-1].lower(),
            "file_size_bytes": str(len(content)), "sha256": C.sha256_bytes(content),
            "table_detected": "YES", "table_description": desc.get(base, "supplementary table"),
            "parse_allowed": "YES",
            "status": "DOWNLOADED_TABLE", "required_action": "PARSE_ALLOWED" if is_net else "context_only",
        })
    rows.sort(key=lambda r: r["supplement_file"])
    C.write_tsv(C.path("CHAPMAN_SUPPLEMENT_TABLE_INDEX.tsv"), header, rows)
    print(f"[02] extracted {len(rows)} tabular tables -> raw/ "
          f"(NET tables: {[r['supplement_file'] for r in rows if r['required_action']=='PARSE_ALLOWED']})")


if __name__ == "__main__":
    main()
