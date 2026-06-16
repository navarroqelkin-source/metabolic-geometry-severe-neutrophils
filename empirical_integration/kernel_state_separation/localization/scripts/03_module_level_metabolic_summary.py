"""03 — Module-level descriptive summary.

Joins the module mapping (M05 glycolysis/PPP, M08 lipid mediators, general pool) to the
per-metabolite contribution results by metabolite name, and summarizes descriptive support per
module. Claim: module-level metabolic STATE association only — never pathway flux or mechanism.
Writes MODULE_LEVEL_SUMMARY.tsv.
"""
import numpy as np
import _loc_common as L

ALLOWED = "module-level metabolic state association"
PROHIBITED = "pathway flux or causal mechanism"


def main():
    feats = L.read_tsv(L.locpath("LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv"))
    mapping = L.read_tsv(L.MODULE_MAP)
    if not feats or not mapping:
        L.set_status("module_summary", "BLOCKED", "missing contribution or mapping")
        L.write_tsv(L.locpath("outputs", "LI_ST002477_MODULE_LEVEL_SUMMARY.tsv"), ["module"], [])
        print("[03] BLOCKED")
        return

    by_name = {f["metabolite_name"]: f for f in feats}
    # module -> list of metabolite names (specific modules only; skip the general-pool aggregate row)
    mod_names = {}
    for r in mapping:
        mod = r.get("module", "")
        name = r.get("metabolite_or_pathway", "")
        if mod.startswith("(general") or "not assigned" in name:
            continue
        mod_names.setdefault(mod, []).append(name)

    mapped_all = {n for names in mod_names.values() for n in names}
    # general pool = features not mapped to any specific module
    mod_names["(general_metabolic_state)"] = [f["metabolite_name"] for f in feats
                                              if f["metabolite_name"] not in mapped_all]

    rows = []
    for mod, names in mod_names.items():
        recs = [by_name[n] for n in names if n in by_name]
        n_map = len(recs)
        if n_map == 0:
            continue
        n_sig = sum(1 for r in recs if _f(r["fdr_q"]) < 0.05)
        n_up = sum(1 for r in recs if r["severity_pattern"] == "monotonic_up")
        n_dn = sum(1 for r in recs if r["severity_pattern"] == "monotonic_down")
        med_cs = float(np.median([_f(r["cliffs_control_severe"]) for r in recs]))
        frac = n_sig / n_map
        if mod.startswith("(general"):
            level = "background_pool"
        elif frac >= 0.5 and n_map >= 3:
            level = "supported"
        elif frac >= 0.25:
            level = "partial"
        elif n_sig >= 1:
            level = "weak"
        else:
            level = "none"
        rows.append({
            "module": mod, "n_mapped_metabolites": n_map, "n_significant_fdr": n_sig,
            "n_monotonic_up": n_up, "n_monotonic_down": n_dn,
            "median_effect_control_severe": round(med_cs, 4),
            "module_support_level": level, "allowed_claim": ALLOWED, "prohibited_claim": PROHIBITED,
        })
    rows.sort(key=lambda r: (r["module"].startswith("(general"), -r["n_significant_fdr"]))
    L.write_tsv(L.locpath("outputs", "LI_ST002477_MODULE_LEVEL_SUMMARY.tsv"),
                ["module", "n_mapped_metabolites", "n_significant_fdr", "n_monotonic_up",
                 "n_monotonic_down", "median_effect_control_severe", "module_support_level",
                 "allowed_claim", "prohibited_claim"], rows)
    # also mirror into the localization-folder canonical TSV
    L.write_tsv(L.locpath("LI_ST002477_MODULE_LEVEL_SUMMARY.tsv"),
                ["module", "n_mapped_metabolites", "n_significant_fdr", "n_monotonic_up",
                 "n_monotonic_down", "median_effect_control_severe", "module_support_level",
                 "allowed_claim", "prohibited_claim"], rows)
    print("[03] modules:", "; ".join(f"{r['module']}={r['module_support_level']}"
                                      f"({r['n_significant_fdr']}/{r['n_mapped_metabolites']})" for r in rows))
    L.set_status("module_summary", "OK", f"{len(rows)} modules")


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 1.0


if __name__ == "__main__":
    main()
