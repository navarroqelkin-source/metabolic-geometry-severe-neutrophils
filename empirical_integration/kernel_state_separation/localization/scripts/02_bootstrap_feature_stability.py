"""02 — Bootstrap stability of the top state-associated metabolites.

Resamples within each group (with replacement), re-ranks metabolites by Kruskal-Wallis H
(vectorized) plus |Cliff's Control-vs-Severe| as tiebreak, and records how often each metabolite
lands in the top 20 / top 50. Descriptive stability only. Writes FEATURE_STABILITY.tsv.
"""
import numpy as np
from scipy.stats import rankdata

import _loc_common as L


def kw_H_vectorized(X, groups):
    """Kruskal-Wallis H per column (metabolite). X: n x p. groups: array of labels."""
    n, p = X.shape
    R = rankdata(X, axis=0)                      # average-tie ranks per column
    N = n
    H = np.zeros(p)
    for g in L.GROUPS:
        idx = (groups == g)
        ng = idx.sum()
        if ng == 0:
            continue
        Rg = R[idx, :].sum(axis=0)
        H += (Rg * Rg) / ng
    H = 12.0 / (N * (N + 1)) * H - 3.0 * (N + 1)
    return H


def main():
    data = L.load_raw_bio()
    if data is None:
        L.set_status("bootstrap_stability", "BLOCKED", "missing real matrix/metadata")
        L.write_tsv(L.locpath("outputs", "LI_ST002477_FEATURE_STABILITY.tsv"),
                    ["metabolite_id"], [])
        print("[02] BLOCKED")
        return
    X, groups, _, feat_ids, feat_names = data
    # replace NaN with column median for ranking stability (matrix had 0 missing)
    for j in range(X.shape[1]):
        col = X[:, j]; mask = ~np.isfinite(col)
        if mask.any():
            col[mask] = np.nanmedian(col)

    iS = (groups == "Severe"); iC = (groups == "Control")
    cliffs_cs = np.array([L.cliffs_delta(X[iC, j], X[iS, j]) for j in range(X.shape[1])])

    rng = np.random.default_rng(L.SEED)
    n_iter = 500
    p = X.shape[1]
    grp_idx = {g: np.where(groups == g)[0] for g in L.GROUPS}
    top20 = np.zeros(p); top50 = np.zeros(p)
    rank_acc = [[] for _ in range(p)]
    for _ in range(n_iter):
        sel = np.concatenate([rng.choice(grp_idx[g], size=grp_idx[g].size, replace=True)
                              for g in L.GROUPS])
        gb = groups[sel]
        Xb = X[sel, :]
        H = kw_H_vectorized(Xb, gb)
        # rank: higher H first; tiebreak higher |cliffs_cs|
        order = np.lexsort((-np.abs(cliffs_cs), -H))   # primary -H, secondary -|cliffs|
        ranks = np.empty(p, dtype=int)
        ranks[order] = np.arange(1, p + 1)
        top20 += (ranks <= 20)
        top50 += (ranks <= 50)
        for j in range(p):
            rank_acc[j].append(ranks[j])

    rows = []
    for j in range(p):
        med_rank = float(np.median(rank_acc[j]))
        t20 = top20[j] / n_iter; t50 = top50[j] / n_iter
        if t20 >= 0.5:
            cls = "stable_top20"
        elif t50 >= 0.5:
            cls = "stable_top50"
        elif t50 >= 0.2:
            cls = "borderline"
        else:
            cls = "unstable"
        rows.append({
            "metabolite_id": feat_ids[j], "metabolite_name": feat_names[j],
            "top20_frequency": round(t20, 3), "top50_frequency": round(t50, 3),
            "median_rank": med_rank, "stability_class": cls,
            "allowed_interpretation": L.ALLOWED_FEAT,
        })
    rows.sort(key=lambda r: (r["median_rank"], -r["top20_frequency"]))
    L.write_tsv(L.locpath("outputs", "LI_ST002477_FEATURE_STABILITY.tsv"),
                ["metabolite_id", "metabolite_name", "top20_frequency", "top50_frequency",
                 "median_rank", "stability_class", "allowed_interpretation"], rows)
    n_stable = sum(1 for r in rows if r["stability_class"].startswith("stable"))
    print(f"[02] n_iter={n_iter} metabolites={p} stable(top20/50)={n_stable}")
    L.set_status("bootstrap_stability", "OK", f"{n_iter} iters; stable={n_stable}")


if __name__ == "__main__":
    main()
