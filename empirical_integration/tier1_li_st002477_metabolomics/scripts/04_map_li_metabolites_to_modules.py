"""04 — Map ST002477 named metabolites to pan-omic modules (tiered, claim-ceiling bounded).

Conservative name-based membership against MODULE_REGISTRY_v0.1.tsv. Only metabolites whose
reported names clearly belong to a module's pathway are mapped; the rest are pooled as a single
'general metabolic state' row (no invented pathway membership). This is supporting tiered
evidence, NOT sample-level fusion.
Writes outputs/LI_ST002477_MODULE_MAPPING.tsv.
"""
import os
import _li_common as L

# Curated name-substring -> module (lowercased). Modules from MODULE_REGISTRY_v0.1.tsv.
# M05 = GAPDH_glycolysis_PPP (central carbon / glycolysis / pentose phosphate).
# M08 = lipid_mediator_resolution (lipid mediators).
M05_KEYS = ["bisphosphoglycerate", "phosphoglycerate", "phosphoenolpyruvate", "pyruvate",
            "lactate", "glucose", "fructose", "glyceraldehyde", "dihydroxyacetone",
            "6-phosphogluconate", "ribose", "ribulose", "sedoheptulose", "erythrose",
            "glucose-6-phosphate", "fructose-1,6", "phosphoglucon", "glycerate", "hexose",
            "citrate", "isocitrate", "succinate", "fumarate", "malate", "aconitate",
            "oxaloacetate", "alpha-ketoglutarate", "2-oxoglutarate", "acetyl-coa"]
M08_KEYS = ["prostaglandin", "leukotriene", "lipoxin", "resolvin", "arachidon",
            "thromboxane", "eicosa", "hydroxyeicosa", "hete", "docosa"]
ALLOWED = "metabolic_state_or_constraint (supporting tiered evidence)"
PROHIBITED = "flux / causal_mechanism / executed_neutrophil_function / sample-level_fusion"
MODNAME = {"M05": "GAPDH_glycolysis_PPP", "M08": "lipid_mediator_resolution"}


def main():
    metabs = L.read_tsv(L.path("LI_ST002477_METABOLITE_TABLE.tsv"))
    rows, mapped_names = [], set()
    for mod, keys in (("M05", M05_KEYS), ("M08", M08_KEYS)):
        for m in metabs:
            name = m.get("metabolite_name", "")
            low = name.lower()
            if any(k in low for k in keys):
                mapped_names.add(name)
                rows.append({
                    "module": f"{mod}:{MODNAME[mod]}", "metabolite_or_pathway": name,
                    "evidence_tier": "1", "source_id": "Li_ST002477",
                    "support_type": "named_metabolite_membership_by_name",
                    "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED,
                })
    unmapped = [m for m in metabs if m.get("metabolite_name", "") not in mapped_names]
    rows.append({
        "module": "(general_metabolic_state)",
        "metabolite_or_pathway": f"{len(unmapped)} named metabolites not assigned to a specific module",
        "evidence_tier": "1", "source_id": "Li_ST002477",
        "support_type": "general_metabolic_state_pool (no invented pathway membership)",
        "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED,
    })
    L.write_tsv(os.path.join(L.OUTDIR, "LI_ST002477_MODULE_MAPPING.tsv"),
                ["module", "metabolite_or_pathway", "evidence_tier", "source_id",
                 "support_type", "allowed_claim", "prohibited_claim"], rows)
    print(f"[04] mapped={len(mapped_names)} (M05/M08) unmapped_pool={len(unmapped)} rows={len(rows)}")


if __name__ == "__main__":
    main()
