"""02 — Multiscale MMD two-sample tests (Gaussian kernel, permutation p-values).

Comparisons: Control_vs_Mild, Control_vs_Severe, Mild_vs_Severe.
Bandwidth = median heuristic (on the pooled pair) x scale in {0.5,1,2,4}. Unbiased MMD^2.
Permutation: 1000 (fallback 200 with a warning if pooled n is tiny). Fixed seed.
"""
import numpy as np
import _kernel_common as K


def sq_dists(Z):
    sq = np.sum(Z * Z, axis=1)
    D2 = sq[:, None] + sq[None, :] - 2.0 * (Z @ Z.T)
    return np.maximum(D2, 0.0)


def mmd2_unbiased(Kmat, m):
    Kxx, Kyy, Kxy = Kmat[:m, :m], Kmat[m:, m:], Kmat[:m, m:]
    n = Kmat.shape[0] - m
    sx = (Kxx.sum() - np.trace(Kxx)) / (m * (m - 1))
    sy = (Kyy.sum() - np.trace(Kyy)) / (n * (n - 1))
    sxy = Kxy.sum() / (m * n)
    return sx + sy - 2.0 * sxy


def main():
    prep = K.load_prepared()
    if prep is None:
        K.set_status("mmd", "BLOCKED", "no prepared matrix")
        K.write_tsv(K.path("outputs", "LI_ST002477_MMD_RESULTS.tsv"),
                    ["comparison", "kernel", "bandwidth_scale", "bandwidth_value", "n_group_1",
                     "n_group_2", "mmd_statistic", "permutation_p_value", "n_permutations",
                     "robustness_note", "allowed_claim", "prohibited_claim"], [])
        print("[02] BLOCKED — no prepared matrix")
        return
    X, groups, _, _ = prep
    groups = np.asarray(groups)
    rng = np.random.default_rng(K.SEED)
    rows = []
    for g1, g2 in K.COMPARISONS:
        Z = np.vstack([X[groups == g1], X[groups == g2]])
        m, n = int((groups == g1).sum()), int((groups == g2).sum())
        n_perm = 1000 if min(m, n) >= 5 else 200
        warn = "" if min(m, n) >= 5 else "small_group_n_perm_reduced"
        D2 = sq_dists(Z)
        base = K.median_heuristic(Z)
        labels = np.array([0] * m + [1] * n)
        for scale in K.BANDWIDTH_SCALES:
            sigma = base * scale
            Kmat = np.exp(-D2 / (2.0 * sigma * sigma))
            obs = mmd2_unbiased(Kmat, m)
            ge = 1
            N = m + n
            for _ in range(n_perm):
                perm = rng.permutation(N)
                Kp = Kmat[np.ix_(perm, perm)]
                if mmd2_unbiased(Kp, m) >= obs:
                    ge += 1
            p = ge / (n_perm + 1)
            rows.append({
                "comparison": f"{g1}_vs_{g2}", "kernel": "gaussian",
                "bandwidth_scale": scale, "bandwidth_value": round(sigma, 6),
                "n_group_1": m, "n_group_2": n,
                "mmd_statistic": round(float(obs), 6), "permutation_p_value": round(p, 5),
                "n_permutations": n_perm,
                "robustness_note": warn or "ok",
                "allowed_claim": K.ALLOWED, "prohibited_claim": K.PROHIBITED,
            })
            print(f"[02] {g1}_vs_{g2} scale={scale} sigma={sigma:.3g} MMD2={obs:.4g} p={p:.4g} (perm={n_perm})")
    K.write_tsv(K.path("outputs", "LI_ST002477_MMD_RESULTS.tsv"),
                ["comparison", "kernel", "bandwidth_scale", "bandwidth_value", "n_group_1",
                 "n_group_2", "mmd_statistic", "permutation_p_value", "n_permutations",
                 "robustness_note", "allowed_claim", "prohibited_claim"], rows)
    K.set_status("mmd", "OK", f"{len(rows)} (comparison x bandwidth) tests")


if __name__ == "__main__":
    main()
