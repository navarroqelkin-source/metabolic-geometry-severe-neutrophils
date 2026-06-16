"""04 — Integrate citrullination evidence: refresh Tier 2 mapping, build T2_BR04, update outputs.

Only acts if real citrullinated entries were parsed. Idempotent. Adds NET_citrullinated_material to
the Chapman Tier 2 protein-module map + module summary, builds the Chapman–Li T2_BR04 bridge, and
annotates the integrated outputs. Claim ceiling unchanged.
"""
import csv
import os

import _cit_common as C

T2 = os.path.join(C.EMP, "chapman_tier2_module_mapping")
PMAP = os.path.join(T2, "CHAPMAN_TIER2_PROTEIN_MODULE_MAP.tsv")
MODSUM = os.path.join(T2, "CHAPMAN_TIER2_MODULE_SUMMARY.tsv")
OUTBASE = os.path.join(C.EMP, "evidence_tiered_outputs")
TIERS = "Chapman_PXD011796:Tier2; Li_ST002477:Tier1"
PROHIBIT = ("metabolic state causes citrullination; citrullination rate; PAD4 activity; NETosis rate; "
            "NET clearance; pathogenicity; sample-level fusion; co-measurement; causal mechanism")
NEXTVAL = "paired citrullinated-NET + metabolome design (same samples) before any joint/quantitative claim"


def rw(p, header, rows):
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def main():
    cit = C.read_tsv(os.path.join(C.ROOT, "CHAPMAN_TABLE6_PARSED_CITRULLINATION.tsv"))
    summ = C.read_tsv(os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_MODULE_SUMMARY.tsv"))
    if not cit:
        # honest negative: emit empty bridge update, do not touch Tier 2 mapping
        C.write_tsv(os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_BRIDGE_UPDATE.tsv"),
                    ["bridge_id", "chapman_citrullination_feature", "li_metabolic_axis", "bridge_type",
                     "evidence_tiers", "allowed_synthesis", "prohibited_synthesis", "next_validation_needed"], [])
        print("[04] no citrullinated entries — NET_citrullinated_material stays empty; no bridge T2_BR04")
        return

    n_entries = len(cit)
    n_prot = len({r["gene_symbol"] for r in cit if r["gene_symbol"]})

    # 1) Tier 2 protein-module map: replace any prior NET_citrullinated_material rows, then append
    if os.path.exists(PMAP):
        pmap_rows = C.read_tsv(PMAP)
        pmap_hdr = list(pmap_rows[0].keys()) if pmap_rows else []
        pmap_rows = [r for r in pmap_rows if r.get("assigned_module") != "NET_citrullinated_material"]
        for r in cit:
            pmap_rows.append({
                "source_id": "Chapman_PXD011796", "protein_or_peptide": r["protein_or_peptide"],
                "gene_symbol": r["gene_symbol"], "uniprot_accession": r["uniprot_accession"],
                "condition_or_group": r["condition_or_group"],
                "assigned_module": "NET_citrullinated_material",
                "module_assignment_basis": "citrullination_PTM:Table_6#Citrullination",
                "reported_metric_or_status": r["reported_metric_or_status"],
                "evidence_tier": "Tier_2",
                "allowed_claim": C.ALLOWED, "prohibited_claim": C.PROHIBITED,
            })
        if pmap_hdr:
            rw(PMAP, pmap_hdr, pmap_rows)

    # 2) Tier 2 module summary: replace/add NET_citrullinated_material row
    if os.path.exists(MODSUM):
        ms = C.read_tsv(MODSUM)
        ms_hdr = list(ms[0].keys()) if ms else []
        ms = [r for r in ms if r.get("module") != "NET_citrullinated_material"]
        reps = (summ[0]["representative_entries"] if summ else "")
        ms.append({"module": "NET_citrullinated_material", "n_proteins": str(n_prot),
                   "n_hc": "NA", "n_ra_sle": "NA", "n_with_q_value": "0", "n_significant_q": "0",
                   "representative_proteins": reps,
                   "allowed_claim": "structured NET/release material module representation (citrullination PTM)",
                   "prohibited_claim": "citrullination rate, PAD4 activity, NETosis rate, clearance, pathogenicity, causal mechanism"})
        if ms_hdr:
            rw(MODSUM, ms_hdr, ms)

    # 3) Chapman–Li T2_BR04 bridge
    C.write_tsv(os.path.join(C.ROOT, "CHAPMAN_CITRULLINATION_BRIDGE_UPDATE.tsv"),
                ["bridge_id", "chapman_citrullination_feature", "li_metabolic_axis", "bridge_type",
                 "evidence_tiers", "allowed_synthesis", "prohibited_synthesis", "next_validation_needed"],
                [{
                    "bridge_id": "T2_BR04",
                    "chapman_citrullination_feature": f"NET_citrullinated_material ({n_entries} citrullinated peptides / {n_prot} proteins)",
                    "li_metabolic_axis": "global_metabolomic_severity_state",
                    "bridge_type": "material_state_alignment", "evidence_tiers": TIERS,
                    "allowed_synthesis": ("Structured citrullinated NET/release material evidence can be "
                                          "represented as a material layer adjacent to the Li metabolic "
                                          "severity-state axis; complementary non-equivalent layers."),
                    "prohibited_synthesis": PROHIBIT, "next_validation_needed": NEXTVAL,
                }])

    # 4) Integrated outputs annotations (idempotent)
    def annotate(fn, mc, mv, tc, suffix):
        p = os.path.join(OUTBASE, fn)
        rows = C.read_tsv(p)
        hdr = list(rows[0].keys()) if rows else []
        n = 0
        for r in rows:
            if r.get(mc) == mv and suffix not in r.get(tc, ""):
                r[tc] = (r[tc] + " " + suffix).strip(); n += 1
        if hdr:
            rw(p, hdr, rows)
        return n
    note = (f"[NET_citrullinated_material populated: {n_entries} citrullinated peptides / {n_prot} "
            "proteins (Table_6, Tier 2 PTM) — material composition, not citrullination rate/PAD4/NETosis rate]")
    a = annotate("NEUTROPHIL_MODULE_EVIDENCE_MAP.tsv", "supporting_source_id", "Chapman_PXD011796",
                 "evidence_summary", note)
    b = annotate("CLAIM_CEILING_BY_SOURCE.tsv", "source_id", "Chapman_PXD011796", "reason",
                 "| NET_citrullinated_material resolved from Table_6 (DEC-048)")

    print(f"[04] citrullination integrated: tier2_map+summary updated, T2_BR04 built, "
          f"outputs annotated (module_map={a}, claim_ceiling={b})")


if __name__ == "__main__":
    main()
