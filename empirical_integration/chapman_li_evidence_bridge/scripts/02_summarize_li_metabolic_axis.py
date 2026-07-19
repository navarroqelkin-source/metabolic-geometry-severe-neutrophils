# SUPERSEDED FOR CROSS-PAIR ORDERING: the "severity-ordered separation (kernel SUPPORTED)"
# string emitted by this script is withdrawn. Cross-pair magnitude comparison is not licensed.
# See NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md at the repository root.
"""02 — Summarize the Li_ST002477 metabolic-state axis for the Chapman bridge.

Reads the localization feature-contribution + module-level summary + module mapping and condenses
them into LI_METABOLIC_AXIS_SUMMARY.tsv. Descriptive state axis only — not flux/causal/biomarker.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = os.path.dirname(ROOT)
LOC = os.path.join(EMP, "kernel_state_separation", "localization")
FEAT = os.path.join(LOC, "LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv")
MODSUM = os.path.join(LOC, "LI_ST002477_MODULE_LEVEL_SUMMARY.tsv")
MODMAP = os.path.join(EMP, "tier1_li_st002477_metabolomics", "outputs", "LI_ST002477_MODULE_MAPPING.tsv")
ALLOWED = "Tier 1 metabolomic state association by severity (descriptive)"
PROHIBITED = "metabolic flux / causal mechanism / biomarker / clinical prediction / executed function"


def read_tsv(p):
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def fq(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 1.0


def main():
    feats = read_tsv(FEAT)
    modsum = {m["module"]: m for m in read_tsv(MODSUM)}
    modmap = read_tsv(MODMAP)
    by_name = {f["metabolite_name"]: f for f in feats}
    m05_names = [r["metabolite_or_pathway"] for r in modmap if r.get("module", "").startswith("M05")]

    def key_metabs(names, k=6):
        recs = [by_name[n] for n in names if n in by_name and fq(by_name[n]["fdr_q"]) < 0.05]
        recs.sort(key=lambda r: -abs(fq(r["cliffs_control_severe"])))
        return "; ".join(f"{r['metabolite_name']}({r['severity_pattern']})" for r in recs[:k])

    rows = []
    m05 = modsum.get("M05:GAPDH_glycolysis_PPP", {})
    rows.append({
        "source_id": "Li_ST002477", "evidence_tier": "1",
        "metabolic_axis": "central_carbon_glycolysis_PPP", "module": "M05:GAPDH_glycolysis_PPP",
        "n_supporting_metabolites": m05.get("n_significant_fdr", "0"),
        "key_metabolites": key_metabs(m05_names),
        "pattern": f"up={m05.get('n_monotonic_up','0')};down={m05.get('n_monotonic_down','0')};"
                   f"median_cliff_CvS={m05.get('median_effect_control_severe','')}",
        "allowed_claim": ALLOWED + " — M05 SUPPORTED descriptively", "prohibited_claim": PROHIBITED,
    })
    rows.append({
        "source_id": "Li_ST002477", "evidence_tier": "1",
        "metabolic_axis": "lipid_mediator_resolution", "module": "M08:lipid_mediator_resolution",
        "n_supporting_metabolites": "0", "key_metabolites": "(none)",
        "pattern": "not_represented_in_HILIC_central_carbon_panel",
        "allowed_claim": "M08 UNSUPPORTED / not represented in this panel (honest negative)",
        "prohibited_claim": PROHIBITED,
    })
    sig = [f for f in feats if fq(f["fdr_q"]) < 0.05]
    mono = [f for f in sig if f["severity_pattern"].startswith("monotonic")]
    top = sorted(sig, key=lambda r: -abs(fq(r["cliffs_control_severe"])))[:8]
    rows.append({
        "source_id": "Li_ST002477", "evidence_tier": "1",
        "metabolic_axis": "global_metabolomic_severity_state", "module": "(all metabolites)",
        "n_supporting_metabolites": str(len(sig)),
        "key_metabolites": "; ".join(r["metabolite_name"] for r in top),
        "pattern": f"{len(mono)} monotonic of {len(sig)} FDR-sig; severity-ordered separation (kernel SUPPORTED)",
        "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED,
    })
    header = ["source_id", "evidence_tier", "metabolic_axis", "module", "n_supporting_metabolites",
              "key_metabolites", "pattern", "allowed_claim", "prohibited_claim"]
    with open(os.path.join(ROOT, "LI_METABOLIC_AXIS_SUMMARY.tsv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    print(f"[02] Li axis rows={len(rows)} (M05 sig={m05.get('n_significant_fdr','?')}, "
          f"global_sig={len(sig)}, monotonic={len(mono)})")


if __name__ == "__main__":
    main()
