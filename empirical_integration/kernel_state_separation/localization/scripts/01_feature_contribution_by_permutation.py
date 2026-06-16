"""01 — Per-metabolite descriptive contribution to severity separation.

Kruskal-Wallis across Control/Mild/Severe + BH-FDR; Cliff's delta for each pairwise contrast;
raw group medians; severity pattern (monotonic_up/down/non_monotonic). Descriptive only — no
biomarker/flux/causal/prediction/function language. Writes FEATURE_CONTRIBUTION_RESULTS.tsv.
"""
import numpy as np
from scipy.stats import kruskal
from statsmodels.stats.multitest import multipletests

import _loc_common as L


def support_class(q, dcs):
    if np.isnan(q):
        return "ns"
    ad = abs(dcs)
    if q < 0.01 and ad >= 0.474:   # large effect
        return "strong"
    if q < 0.05 and ad >= 0.33:    # medium effect
        return "moderate"
    if q < 0.05:
        return "weak"
    return "ns"


def main():
    data = L.load_raw_bio()
    if data is None:
        L.set_status("feature_contribution", "BLOCKED", "missing real matrix/metadata")
        L.write_tsv(L.locpath("LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv"),
                    ["metabolite_id"], [])
        print("[01] BLOCKED — missing input")
        return
    X, groups, _, feat_ids, feat_names = data
    iC, iM, iS = (groups == "Control"), (groups == "Mild"), (groups == "Severe")

    pvals, recs = [], []
    for j in range(X.shape[1]):
        c, m, s = X[iC, j], X[iM, j], X[iS, j]
        cf = c[np.isfinite(c)]; mf = m[np.isfinite(m)]; sf = s[np.isfinite(s)]
        try:
            _, p = kruskal(cf, mf, sf)
        except ValueError:
            p = float("nan")
        pvals.append(p)
        recs.append({
            "metabolite_id": feat_ids[j], "metabolite_name": feat_names[j],
            "kruskal_p": p,
            "cliffs_control_mild": L.cliffs_delta(c, m),
            "cliffs_control_severe": L.cliffs_delta(c, s),
            "cliffs_mild_severe": L.cliffs_delta(m, s),
            "median_control": float(np.nanmedian(c)) if cf.size else float("nan"),
            "median_mild": float(np.nanmedian(m)) if mf.size else float("nan"),
            "median_severe": float(np.nanmedian(s)) if sf.size else float("nan"),
        })

    pv = np.array([p if np.isfinite(p) else 1.0 for p in pvals])
    qv = multipletests(pv, method="fdr_bh")[1]

    out = []
    for r, p, q in zip(recs, pvals, qv):
        pat = L.severity_pattern(r["median_control"], r["median_mild"], r["median_severe"])
        sup = support_class(q, r["cliffs_control_severe"])
        out.append({
            "metabolite_id": r["metabolite_id"], "metabolite_name": r["metabolite_name"],
            "kruskal_p": round(p, 6) if np.isfinite(p) else "NA",
            "fdr_q": round(float(q), 6),
            "cliffs_control_mild": round(r["cliffs_control_mild"], 4),
            "cliffs_control_severe": round(r["cliffs_control_severe"], 4),
            "cliffs_mild_severe": round(r["cliffs_mild_severe"], 4),
            "median_control": round(r["median_control"], 4),
            "median_mild": round(r["median_mild"], 4),
            "median_severe": round(r["median_severe"], 4),
            "severity_pattern": pat, "descriptive_support": sup,
            "allowed_interpretation": L.ALLOWED_FEAT,
            "prohibited_interpretation": L.PROHIBITED_FEAT,
        })
    out.sort(key=lambda r: (r["fdr_q"], -abs(r["cliffs_control_severe"])))
    L.write_tsv(L.locpath("LI_ST002477_FEATURE_CONTRIBUTION_RESULTS.tsv"),
                ["metabolite_id", "metabolite_name", "kruskal_p", "fdr_q", "cliffs_control_mild",
                 "cliffs_control_severe", "cliffs_mild_severe", "median_control", "median_mild",
                 "median_severe", "severity_pattern", "descriptive_support",
                 "allowed_interpretation", "prohibited_interpretation"], out)

    n_sig = sum(1 for r in out if r["fdr_q"] < 0.05)
    n_mono = sum(1 for r in out if r["severity_pattern"].startswith("monotonic"))
    print(f"[01] metabolites={len(out)} fdr_sig(q<0.05)={n_sig} monotonic={n_mono} "
          f"strong={sum(1 for r in out if r['descriptive_support']=='strong')}")
    L.set_status("feature_contribution", "OK",
                 f"{len(out)} metabolites; fdr_sig={n_sig}; monotonic={n_mono}")


if __name__ == "__main__":
    main()
