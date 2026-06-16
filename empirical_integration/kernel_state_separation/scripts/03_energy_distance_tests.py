"""03 — Energy-distance two-sample tests with permutation p-values.

Energy distance E = 2*mean(||x-y||) - mean(||x-x'||) - mean(||y-y'||) (>=0).
Same comparisons and permutation budget as the MMD module. Fixed seed. Bandwidth-free contrast.
"""
import numpy as np
import _kernel_common as K


def pair_dist(Z):
    sq = np.sum(Z * Z, axis=1)
    D2 = np.maximum(sq[:, None] + sq[None, :] - 2.0 * (Z @ Z.T), 0.0)
    return np.sqrt(D2)


def energy_stat(D, m):
    n = D.shape[0] - m
    dxy = D[:m, m:].mean()
    dxx = (D[:m, :m].sum()) / (m * m)      # includes zeros on diagonal (standard V-statistic form)
    dyy = (D[m:, m:].sum()) / (n * n)
    return 2.0 * dxy - dxx - dyy


def main():
    prep = K.load_prepared()
    if prep is None:
        K.set_status("energy_distance", "BLOCKED", "no prepared matrix")
        K.write_tsv(K.path("outputs", "LI_ST002477_ENERGY_DISTANCE_RESULTS.tsv"),
                    ["comparison", "n_group_1", "n_group_2", "energy_statistic",
                     "permutation_p_value", "n_permutations", "robustness_note",
                     "allowed_claim", "prohibited_claim"], [])
        print("[03] BLOCKED — no prepared matrix")
        return
    X, groups, _, _ = prep
    groups = np.asarray(groups)
    rng = np.random.default_rng(K.SEED + 1)
    rows = []
    for g1, g2 in K.COMPARISONS:
        Z = np.vstack([X[groups == g1], X[groups == g2]])
        m, n = int((groups == g1).sum()), int((groups == g2).sum())
        n_perm = 1000 if min(m, n) >= 5 else 200
        warn = "" if min(m, n) >= 5 else "small_group_n_perm_reduced"
        D = pair_dist(Z)
        obs = energy_stat(D, m)
        N = m + n
        ge = 1
        for _ in range(n_perm):
            perm = rng.permutation(N)
            Dp = D[np.ix_(perm, perm)]
            if energy_stat(Dp, m) >= obs:
                ge += 1
        p = ge / (n_perm + 1)
        rows.append({
            "comparison": f"{g1}_vs_{g2}", "n_group_1": m, "n_group_2": n,
            "energy_statistic": round(float(obs), 6), "permutation_p_value": round(p, 5),
            "n_permutations": n_perm, "robustness_note": warn or "ok",
            "allowed_claim": K.ALLOWED, "prohibited_claim": K.PROHIBITED,
        })
        print(f"[03] {g1}_vs_{g2} E={obs:.4g} p={p:.4g} (perm={n_perm})")
    K.write_tsv(K.path("outputs", "LI_ST002477_ENERGY_DISTANCE_RESULTS.tsv"),
                ["comparison", "n_group_1", "n_group_2", "energy_statistic",
                 "permutation_p_value", "n_permutations", "robustness_note",
                 "allowed_claim", "prohibited_claim"], rows)
    K.set_status("energy_distance", "OK", f"{len(rows)} comparisons")


if __name__ == "__main__":
    main()
