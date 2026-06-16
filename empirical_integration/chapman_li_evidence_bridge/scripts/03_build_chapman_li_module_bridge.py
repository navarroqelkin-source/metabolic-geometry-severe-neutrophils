"""03 — Build the Chapman–Li evidence-tiered material/module bridge.

Curated, biologically-grounded bridges between Chapman NET/release proteome material and the Li
metabolic state axis. Every bridge is material/module/concept context or hypothesis-generating —
never sample-level correlation, co-measurement, NETosis rate, clearance, pathogenicity or causal
mechanism. Reads the summaries written by scripts 01-02 so it only references real evidence.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPMAN = os.path.join(ROOT, "CHAPMAN_EVIDENCE_EXTRACTION.tsv")
LIAXIS = os.path.join(ROOT, "LI_METABOLIC_AXIS_SUMMARY.tsv")
TIERS = "Chapman_PXD011796:Tier3; Li_ST002477:Tier1"
PROHIBIT = ("sample-level correlation; co-measurement; causal mechanism; metabolism-to-NETosis "
            "inference; NETosis rate; NET clearance; NET pathogenicity; executed neutrophil function")
NEXTVAL = "paired design (NET proteome + metabolome on the same samples) before any joint/quantitative claim"


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    chap = read_tsv(CHAPMAN)
    liaxis = read_tsv(LIAXIS)
    have_net = any(r.get("item_type") in ("NET_material_feature", "protein", "article_result") for r in chap)
    have_m05 = any(r["module"].startswith("M05") and r["n_supporting_metabolites"] not in ("0", "")
                   for r in liaxis)
    have_global = any(r["metabolic_axis"] == "global_metabolomic_severity_state" for r in liaxis)
    global_keys = next((r["key_metabolites"].lower() for r in liaxis
                        if r["metabolic_axis"] == "global_metabolomic_severity_state"), "")
    # only assert BR03 if redox/purine/carnitine/amino-acid contributors are actually present
    redox_present = any(k in global_keys for k in
                        ["hypoxanthine", "carnitine", "alanine", "histamine", "glutathione", "purine"])

    bridges = []

    def add(bid, cf, mod, axis, btype, allowed):
        bridges.append({
            "bridge_id": bid, "chapman_feature_or_context": cf, "li_metabolic_module": mod,
            "li_metabolites_or_axis": axis, "bridge_type": btype, "evidence_tiers": TIERS,
            "allowed_synthesis": allowed, "prohibited_synthesis": PROHIBIT,
            "next_validation_needed": NEXTVAL,
        })

    if have_net and have_global:
        add("BR01", "NET/release proteome material composition (histones, MPO, neutrophil elastase)",
            "(all metabolites)", "global_metabolomic_severity_state", "material_state_alignment",
            "Chapman defines NET/release material composition while Li_ST002477 defines a "
            "severity-associated metabolomic state; together they support an evidence-tiered link "
            "between metabolic state and neutrophil extracellular effector material as complementary "
            "non-equivalent layers.")
    if have_net and have_m05:
        add("BR02", "NET/release proteome material composition",
            "M05:GAPDH_glycolysis_PPP", "central_carbon_glycolysis_PPP", "module_context_alignment",
            "A supported central-carbon/PPP metabolic-state module and NET/release material are "
            "independently observed neutrophil-state features; their co-listing is a hypothesis-"
            "generating context alignment, not a measured relationship and not a mechanism.")
    if have_net and redox_present:
        add("BR03", "NET/release proteome (oxidative/chromatin-associated effector material)",
            "(state-associated contributors)",
            "purine/redox/carnitine/amino-acid contributors (e.g. hypoxanthine, carnitines, beta-alanine)",
            "hypothesis_generating_cross_layer_link",
            "NET/release material and severity-associated redox/purine/carnitine/amino-acid metabolic "
            "contributors are both features of activated-neutrophil biology; this is a hypothesis to "
            "test with paired data, not an inferred link and not a NETosis-rate statement.")

    header = ["bridge_id", "chapman_feature_or_context", "li_metabolic_module", "li_metabolites_or_axis",
              "bridge_type", "evidence_tiers", "allowed_synthesis", "prohibited_synthesis",
              "next_validation_needed"]
    with open(os.path.join(ROOT, "CHAPMAN_LI_MODULE_BRIDGE.tsv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(bridges)
    print(f"[03] bridges={len(bridges)} types={sorted({b['bridge_type'] for b in bridges})} "
          f"redox_present={redox_present}")


if __name__ == "__main__":
    main()
