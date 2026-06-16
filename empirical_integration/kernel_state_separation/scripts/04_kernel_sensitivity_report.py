"""04 — Sensitivity, agreement and final separation verdict.

Assesses: bandwidth sensitivity (MMD p across scales), MMD/energy agreement, permutation budget,
severity ordering (Control_vs_Severe stronger than Control_vs_Mild), simple outlier robustness
(leave-one-out on the most extreme sample per group for energy distance). Writes the sensitivity
summary, consolidated KERNEL_TEST_RESULTS.tsv, and KERNEL_VALIDATION_REPORT.md with a final status.
"""
import numpy as np
import _kernel_common as K

ALPHA = 0.05


def pair_dist(Z):
    sq = np.sum(Z * Z, axis=1)
    return np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2.0 * (Z @ Z.T), 0.0))


def energy_stat(D, m):
    n = D.shape[0] - m
    return 2.0 * D[:m, m:].mean() - D[:m, :m].sum() / (m * m) - D[m:, m:].sum() / (n * n)


def energy_p(Z, m, rng, n_perm):
    D = pair_dist(Z)
    obs = energy_stat(D, m)
    N = D.shape[0]
    ge = 1
    for _ in range(n_perm):
        perm = rng.permutation(N)
        if energy_stat(D[np.ix_(perm, perm)], m) >= obs:
            ge += 1
    return obs, ge / (n_perm + 1)


def main():
    mmd = K.read_tsv(K.path("outputs", "LI_ST002477_MMD_RESULTS.tsv"))
    energy = K.read_tsv(K.path("outputs", "LI_ST002477_ENERGY_DISTANCE_RESULTS.tsv"))
    prep = K.load_prepared()
    if not mmd or not energy or prep is None:
        K.set_status("sensitivity_validation", "BLOCKED", "missing results or matrix")
        with open(K.path("KERNEL_VALIDATION_REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write("# Kernel validation\n\nFinal status: **KERNEL_ANALYSIS_BLOCKED** "
                     "(missing prepared matrix or results). Nothing fabricated.\n")
        print("[04] BLOCKED")
        return

    X, groups, _, _ = prep
    groups = np.asarray(groups)
    rng = np.random.default_rng(K.SEED + 7)

    # index MMD by comparison
    comps = [f"{a}_vs_{b}" for a, b in K.COMPARISONS]
    mmd_by = {c: [r for r in mmd if r["comparison"] == c] for c in comps}
    en_by = {r["comparison"]: r for r in energy}

    sens_rows, consolidated = [], []
    supported = {}
    for c in comps:
        ms = mmd_by[c]
        ps = [float(r["permutation_p_value"]) for r in ms]
        sig_frac = sum(p < ALPHA for p in ps) / len(ps) if ps else 0.0
        mmd_p1 = next((float(r["permutation_p_value"]) for r in ms
                       if abs(float(r["bandwidth_scale"]) - 1.0) < 1e-9), float("nan"))
        mmd_stat1 = next((float(r["mmd_statistic"]) for r in ms
                          if abs(float(r["bandwidth_scale"]) - 1.0) < 1e-9), float("nan"))
        en = en_by.get(c, {})
        en_p = float(en.get("permutation_p_value", "1"))
        en_stat = float(en.get("energy_statistic", "nan"))
        agree = (sig_frac >= 0.5) and (en_p < ALPHA)
        supported[c] = agree

        # outlier robustness: drop most extreme sample (max L2 norm) per group, recompute energy
        g1, g2 = c.split("_vs_")
        i1 = np.where(groups == g1)[0]
        i2 = np.where(groups == g2)[0]
        def drop_extreme(idx):
            norms = np.linalg.norm(X[idx], axis=1)
            return np.delete(idx, np.argmax(norms))
        Zr = np.vstack([X[drop_extreme(i1)], X[drop_extreme(i2)]])
        mr = len(i1) - 1
        n_perm = 1000 if min(len(i1), len(i2)) >= 5 else 200
        _, en_p_loo = energy_p(Zr, mr, np.random.default_rng(K.SEED + 99), n_perm)
        loo_stable = (en_p_loo < ALPHA) == (en_p < ALPHA)

        sens_rows.append({
            "comparison": c,
            "mmd_p_min": round(min(ps), 5), "mmd_p_max": round(max(ps), 5),
            "mmd_sig_fraction_across_bandwidths": round(sig_frac, 3),
            "energy_p": round(en_p, 5), "energy_p_outlier_LOO": round(en_p_loo, 5),
            "mmd_energy_agree": "YES" if agree else "NO",
            "outlier_robustness": "STABLE" if loo_stable else "SENSITIVE",
            "verdict": "SUPPORTED" if agree else "WEAK_OR_NOT",
        })
        consolidated.append({
            "source_id": "Li_ST002477", "layer": "metabolomics", "comparison": c,
            "method": "MMD_gaussian_multiscale", "statistic": round(mmd_stat1, 6),
            "p_value": round(mmd_p1, 5), "n_permutations": ms[0]["n_permutations"] if ms else "",
            "robustness_status": f"sig_in_{int(sig_frac*len(ps))}/{len(ps)}_bandwidths",
            "allowed_interpretation": K.ALLOWED, "prohibited_interpretation": K.PROHIBITED,
            "next_step": "map contributing metabolites/modules only if SUPPORTED",
        })
        consolidated.append({
            "source_id": "Li_ST002477", "layer": "metabolomics", "comparison": c,
            "method": "energy_distance", "statistic": round(en_stat, 6),
            "p_value": round(en_p, 5), "n_permutations": en.get("n_permutations", ""),
            "robustness_status": f"outlier_LOO={'stable' if loo_stable else 'sensitive'}",
            "allowed_interpretation": K.ALLOWED, "prohibited_interpretation": K.PROHIBITED,
            "next_step": "map contributing metabolites/modules only if SUPPORTED",
        })

    # severity ordering: Control_vs_Severe MMD(scale1) >= Control_vs_Mild MMD(scale1)
    def mmd1(c):
        return next((float(r["mmd_statistic"]) for r in mmd_by[c]
                     if abs(float(r["bandwidth_scale"]) - 1.0) < 1e-9), float("nan"))
    ordering_ok = mmd1("Control_vs_Severe") >= mmd1("Control_vs_Mild")

    K.write_tsv(K.path("outputs", "LI_ST002477_KERNEL_SENSITIVITY_SUMMARY.tsv"),
                ["comparison", "mmd_p_min", "mmd_p_max", "mmd_sig_fraction_across_bandwidths",
                 "energy_p", "energy_p_outlier_LOO", "mmd_energy_agree", "outlier_robustness",
                 "verdict"], sens_rows)
    K.write_tsv(K.path("KERNEL_TEST_RESULTS.tsv"),
                ["source_id", "layer", "comparison", "method", "statistic", "p_value",
                 "n_permutations", "robustness_status", "allowed_interpretation",
                 "prohibited_interpretation", "next_step"], consolidated)

    n_sup = sum(supported.values())
    if supported.get("Control_vs_Severe") and n_sup >= 2:
        status = "KERNEL_STATE_SEPARATION_SUPPORTED"
    elif n_sup >= 1:
        status = "KERNEL_STATE_SEPARATION_WEAK_OR_INCONSISTENT"
    else:
        status = "KERNEL_STATE_SEPARATION_NOT_SUPPORTED"

    lines = [
        "# Kernel State Separation — Validation Report", "",
        f"Final status: **{status}**", "",
        "Source: Li_ST002477 (Tier 1 metabolomics). Input: real matrix, "
        f"{int((groups==K.GROUPS[0]).sum())}/{int((groups==K.GROUPS[1]).sum())}/"
        f"{int((groups==K.GROUPS[2]).sum())} Control/Mild/Severe.", "",
        "## Per-comparison",
    ]
    for r in sens_rows:
        lines.append(
            f"- **{r['comparison']}**: MMD sig in "
            f"{r['mmd_sig_fraction_across_bandwidths']} of bandwidths "
            f"(p∈[{r['mmd_p_min']},{r['mmd_p_max']}]); energy p={r['energy_p']} "
            f"(LOO p={r['energy_p_outlier_LOO']}, {r['outlier_robustness']}); "
            f"agree={r['mmd_energy_agree']} → {r['verdict']}")
    lines += [
        "", "## Sensitivity",
        f"- Severity ordering (Control_vs_Severe MMD ≥ Control_vs_Mild MMD): "
        f"{'YES' if ordering_ok else 'NO'}",
        f"- MMD/energy agreement: {sum(1 for r in sens_rows if r['mmd_energy_agree']=='YES')}/3 comparisons",
        f"- Outlier robustness (LOO): {sum(1 for r in sens_rows if r['outlier_robustness']=='STABLE')}/3 stable",
        "", "## Claim ceiling",
        f"- Allowed: {K.ALLOWED}.",
        f"- Prohibited: {K.PROHIBITED}.",
        "- A positive result authorizes downstream biological exploration only; it does not "
        "establish mechanism, flux, biomarker validity or executed neutrophil function.",
    ]
    with open(K.path("KERNEL_VALIDATION_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    K.set_status("sensitivity_validation", status,
                 f"supported={n_sup}/3; ordering_ok={ordering_ok}")
    print(f"[04] {status} supported={n_sup}/3 ordering_ok={ordering_ok}")


if __name__ == "__main__":
    main()
