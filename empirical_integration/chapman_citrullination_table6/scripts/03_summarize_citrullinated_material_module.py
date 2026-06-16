"""03 — Summarize the NET_citrullinated_material module from parsed Table_6 evidence.

Populates the module only if real citrullinated entries exist. Writes
CHAPMAN_CITRULLINATION_MODULE_SUMMARY.tsv. Detection counts are presence counts, not rates.
"""
import os

import _cit_common as C


def main():
    rows = C.read_tsv(os.path.join(C.ROOT, "CHAPMAN_TABLE6_PARSED_CITRULLINATION.tsv"))
    header = ["module", "n_entries", "n_proteins_or_peptides", "n_with_condition",
              "n_with_metric", "representative_entries", "allowed_claim", "prohibited_claim"]
    if not rows:
        C.write_tsv(os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_MODULE_SUMMARY.tsv"), header,
                    [{"module": "NET_citrullinated_material", "n_entries": "0",
                      "n_proteins_or_peptides": "0", "representative_entries": "(none — NOT_STRUCTURABLE)",
                      "allowed_claim": C.ALLOWED, "prohibited_claim": C.PROHIBITED}])
        print("[03] NET_citrullinated_material EMPTY (no parsed entries)")
        return
    proteins = sorted({r["gene_symbol"] for r in rows if r["gene_symbol"]})
    n_cond = sum(1 for r in rows if r.get("condition_or_group"))
    n_metric = sum(1 for r in rows if "count=" in (r.get("reported_metric_or_status", "")))
    # representatives: prioritise classic NET-relevant citrullination targets if present
    priority = [p for p in proteins if p in (
        "AZU1", "CATG", "ELNE", "PRTN3", "H4", "H2B1", "H2A", "H31", "H32", "MPO", "LYSC", "CAMP")]
    reps = (priority + [p for p in proteins if p not in priority])[:10]
    C.write_tsv(os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_MODULE_SUMMARY.tsv"), header,
                [{"module": "NET_citrullinated_material",
                  "n_entries": str(len(rows)), "n_proteins_or_peptides": str(len(proteins)),
                  "n_with_condition": str(n_cond), "n_with_metric": str(n_metric),
                  "representative_entries": "; ".join(reps),
                  "allowed_claim": C.ALLOWED, "prohibited_claim": C.PROHIBITED}])
    print(f"[03] NET_citrullinated_material POPULATED entries={len(rows)} proteins={len(proteins)}")
    print(f"     representatives: {reps}")


if __name__ == "__main__":
    main()
