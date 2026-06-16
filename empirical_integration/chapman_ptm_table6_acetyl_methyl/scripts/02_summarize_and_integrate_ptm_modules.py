"""02 — Summarize NET_acetylated_material / NET_methylated_material and integrate.

Builds the module summary, then idempotently adds these PTM modules to the Chapman Tier 2
protein-module map + module summary and annotates the integrated outputs. Claim ceiling unchanged.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
PARSED = os.path.join(ROOT, "CHAPMAN_TABLE6_PARSED_PTM.tsv")
T2 = os.path.join(EMP, "chapman_tier2_module_mapping")
PMAP = os.path.join(T2, "CHAPMAN_TIER2_PROTEIN_MODULE_MAP.tsv")
MODSUM = os.path.join(T2, "CHAPMAN_TIER2_MODULE_SUMMARY.tsv")
OUTBASE = os.path.join(EMP, "evidence_tiered_outputs")
MODNAME = {"Acetylation": "NET_acetylated_material", "Methylation": "NET_methylated_material"}
ALLOWED = "structured NET/release material module representation (PTM)"
PROHIBITED = "enzyme activity (HAT/HDAC/PRMT), modification rate, NETosis rate, clearance, pathogenicity, causal mechanism"


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def rw(p, header, rows):
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def main():
    parsed = read_tsv(PARSED)
    if not parsed:
        print("[02] no parsed PTM entries — nothing to integrate")
        return
    by_type = {}
    for r in parsed:
        by_type.setdefault(r["ptm_type"], []).append(r)

    # module summary
    summ = []
    for ptm, recs in by_type.items():
        mod = MODNAME[ptm]
        prots = sorted({r["gene_symbol"] for r in recs if r["gene_symbol"]})
        # prioritise NET-relevant targets (histones, MPO)
        prio = [p for p in prots if p.startswith("H3") or p in ("H31", "H32", "H33", "H31T", "PERM", "MPO")]
        reps = (prio + [p for p in prots if p not in prio])[:10]
        summ.append({"module": mod, "ptm_type": ptm, "n_entries": str(len(recs)),
                     "n_proteins": str(len(prots)), "representative_proteins": "; ".join(reps),
                     "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED})
    rw(os.path.join(ROOT, "CHAPMAN_PTM_MODULE_SUMMARY.tsv"),
       ["module", "ptm_type", "n_entries", "n_proteins", "representative_proteins",
        "allowed_claim", "prohibited_claim"], summ)

    # integrate into Tier 2 protein-module map (idempotent)
    if os.path.exists(PMAP):
        pmap = read_tsv(PMAP)
        hdr = list(pmap[0].keys()) if pmap else []
        pmap = [r for r in pmap if r.get("assigned_module") not in MODNAME.values()]
        for r in parsed:
            pmap.append({
                "source_id": "Chapman_PXD011796", "protein_or_peptide": r["protein_or_peptide"],
                "gene_symbol": r["gene_symbol"], "uniprot_accession": r["uniprot_accession"],
                "condition_or_group": r["condition_or_group"],
                "assigned_module": MODNAME[r["ptm_type"]],
                "module_assignment_basis": f"{r['ptm_type']}_PTM:Table_6#{r['ptm_type']}",
                "reported_metric_or_status": r["reported_metric_or_status"],
                "evidence_tier": "Tier_2", "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED,
            })
        if hdr:
            rw(PMAP, hdr, pmap)

    # Tier 2 module summary (idempotent add of the two modules)
    if os.path.exists(MODSUM):
        ms = read_tsv(MODSUM)
        hdr = list(ms[0].keys()) if ms else []
        ms = [r for r in ms if r.get("module") not in MODNAME.values()]
        for s in summ:
            ms.append({"module": s["module"], "n_proteins": s["n_proteins"],
                       "n_hc": "NA", "n_ra_sle": "NA", "n_with_q_value": "0", "n_significant_q": "0",
                       "representative_proteins": s["representative_proteins"],
                       "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED})
        if hdr:
            rw(MODSUM, hdr, ms)

    # annotate integrated outputs (idempotent)
    note = (f"[PTM material extended: NET_acetylated_material ({len(by_type.get('Acetylation',[]))} "
            f"entries) + NET_methylated_material ({len(by_type.get('Methylation',[]))} entries, incl. "
            "histone H3 + MPO) from Table_6 — material composition, not enzyme activity/rate]")
    p = os.path.join(OUTBASE, "NEUTROPHIL_MODULE_EVIDENCE_MAP.tsv")
    rows = read_tsv(p); hdr = list(rows[0].keys()) if rows else []
    c = 0
    for r in rows:
        if r.get("supporting_source_id") == "Chapman_PXD011796" and "PTM material extended" not in r.get("evidence_summary", ""):
            r["evidence_summary"] += " " + note; c += 1
    if hdr:
        rw(p, hdr, rows)
    pc = os.path.join(OUTBASE, "CLAIM_CEILING_BY_SOURCE.tsv")
    rows = read_tsv(pc); hdr = list(rows[0].keys()) if rows else []
    for r in rows:
        if r.get("source_id") == "Chapman_PXD011796" and "acetyl/methyl PTM" not in r.get("reason", ""):
            r["reason"] = (r["reason"] + " | acetyl/methyl PTM material added from Table_6 (DEC-050)").strip()
    if hdr:
        rw(pc, hdr, rows)

    print(f"[02] modules: " + "; ".join(f"{s['module']}={s['n_entries']}entries/{s['n_proteins']}prot" for s in summ)
          + f" | outputs module_map annotated={c}")


if __name__ == "__main__":
    main()
