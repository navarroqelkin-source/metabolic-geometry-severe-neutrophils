"""
Simulation-based measurement-design identifiability map (NEUTRAL, not a benchmark).

Question: given KNOWN latent truth, which measurement breakers reduce which ambiguities that
burden-only NET-burden readouts cannot resolve, and where does each fail?

This is an in silico measurement-design analysis. It validates neither biological parameter values
nor patient mechanisms. Simulated parameters are not biological parameters. Synthetic data are used
only as a supplementary illustration of method/design behaviour, not a result.

Method (information-content / distinguishability map):
  GENERATOR (richer): saturable removal k_eff(B) = k0/(1+alpha*B) at the operating point and during decay,
    with lognormal (multiplicative) observation noise and a sparse/irregular time-course.
  For each ambiguity we fix two latent hypotheses that are BURDEN-EQUIVALENT (same expected cross-sectional
    Y, so burden alone cannot separate them). For each breaker we ask whether the breaker's measurement(s)
    distinguish the two hypotheses: a noisy observation is classified to the nearest hypothesis's
    generator-expected observable (log-space). Score = 2*(accuracy-0.5) in [0,1] (0 = indistinguishable,
    1 = fully resolved). No metric term is tuned to favour any breaker. This tests information content of
    each measurement, not the adequacy of any one recovery model.
"""
import os, csv
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(20260612)
ALPHA = 0.15  # saturable removal

def steady_B(F, k0, alpha=ALPHA):
    denom = k0 - F * alpha
    return F / denom if denom > 1e-6 else F / 1e-6

def decay_series(B0, k0, t, alpha=ALPHA):
    # production off; dB/dt = -k0*B/(1+alpha*B); sample at times t (saturable -> non-exponential)
    B = float(B0); dt = 0.02; ts = sorted(t); idx = 0; samp = {}
    for tau in np.arange(0, max(ts) + dt, dt):
        while idx < len(ts) and tau >= ts[idx] - 1e-9:
            samp[ts[idx]] = B; idx += 1
        B = max(0.0, B - (k0 / (1 + alpha * B)) * B * dt)
    for tau in ts:
        samp.setdefault(tau, B)
    return np.array([samp[tau] for tau in t])

def lognoise(x, cv, rng):
    sig = np.sqrt(np.log(1 + cv**2))
    x = np.asarray(x, dtype=float)
    return x * rng.lognormal(mean=-0.5 * sig**2, sigma=sig, size=x.shape)

# burden-equivalent hypotheses per ambiguity (latents: F, k0, KR, V, G)
def hypotheses():
    b = dict(F=1.0, k0=1.0, KR=1.0, V=1.0, G=1.0)
    return {
        # A1 formation vs clearance: high F (3,1) vs low clearance (1,0.333); both Y~5.45
        "A1": (dict(b, F=3.0, k0=1.0), dict(b, F=1.0, k0=0.333)),
        # A2 true burden vs detectability: SAME F=1; high burden (low k) vs high KR; both Y~5.46
        "A2": (dict(b, F=1.0, k0=0.333, KR=1.0), dict(b, F=1.0, k0=1.0, KR=4.64)),
        # A3 ongoing production vs persistence (= formation/removal axis, persistence framing)
        "A3": (dict(b, F=3.0, k0=1.0), dict(b, F=1.0, k0=0.333)),
        # A4 viable forming capacity vs accumulated material: differ in V only (same Y)
        "A4": (dict(b, V=2.0), dict(b, V=0.5)),
        # A5 burden vs functional execution: differ in G only (same Y)
        "A5": (dict(b, G=2.0), dict(b, G=0.5)),
    }

TPTS = [0.0, 0.5, 1.0, 2.0]
BREAKERS = ["M0","M1","M2","M3","M4","M5","M6","M7"]
AMB = ["A1","A2","A3","A4","A5"]

def expected_obs(L, breaker):
    F, k0, KR, V, G = L["F"], L["k0"], L["KR"], L["V"], L["G"]
    B = steady_B(F, k0); keff = k0 / (1 + ALPHA * B)
    o = {"Y": np.array([KR * B])}
    if breaker == "M1": o["F"] = np.array([F])
    elif breaker == "M2": o["k"] = np.array([keff])
    elif breaker == "M3": o["decay"] = KR * decay_series(B, k0, TPTS)
    elif breaker == "M4": o["V"] = np.array([V])
    elif breaker == "M5": o["G"] = np.array([G])
    elif breaker == "M6": o["KR"] = np.array([KR])
    elif breaker == "M7":
        o["F"] = np.array([F]); o["k"] = np.array([keff]); o["KR"] = np.array([KR]); o["G"] = np.array([G])
    return o

def gen_obs(L, breaker, cv, rng):
    return {k: lognoise(v, cv, rng) for k, v in expected_obs(L, breaker).items()}

def logdist(obs, exp, sig):
    s = 0.0
    for k in obs:
        o = np.maximum(obs[k], 1e-9); e = np.maximum(exp[k], 1e-9)
        s += float(np.sum((np.log(o) - np.log(e))**2))
    return s / (2 * sig**2)

def score(cv=0.15, tpts=(0.0,0.5,1.0,2.0), n=800):
    global TPTS
    TPTS = list(tpts)
    sig = np.sqrt(np.log(1 + cv**2))
    H = hypotheses(); mat = {}
    for A in AMB:
        ha, hb = H[A]; mat[A] = {}
        for M in BREAKERS:
            br = None if M == "M0" else M
            ea, eb = expected_obs(ha, br), expected_obs(hb, br)
            correct = 0
            for _ in range(n):
                truth = ha if RNG.random() < 0.5 else hb
                obs = gen_obs(truth, br, cv, RNG)
                pick = ha if logdist(obs, ea, sig) < logdist(obs, eb, sig) else hb
                correct += (pick is truth)
            mat[A][M] = round(max(0.0, 2*(correct/n - 0.5)), 3)
    return mat

def write_matrix(mat, path, note):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["# " + note + " | synthetic illustration of method/design behaviour, not a result"])
        w.writerow(["ambiguity"] + BREAKERS)
        for A in AMB:
            w.writerow([A] + [mat[A][M] for M in BREAKERS])

if __name__ == "__main__":
    base = score(cv=0.15, tpts=(0.0,0.5,1.0,2.0), n=1000)
    hi   = score(cv=0.45, tpts=(0.0,0.5,1.0,2.0), n=1000)   # high noise
    few  = score(cv=0.15, tpts=(0.0,2.0),         n=1000)   # 2 timepoints
    write_matrix(base, os.path.join(OUT, "ambiguity_reduction_matrix.tsv"),
                 "base cv=0.15, 4 timepoints")
    write_matrix(hi,  os.path.join(OUT, "ambiguity_reduction_highnoise.tsv"), "high-noise cv=0.45, 4 timepoints")
    write_matrix(few, os.path.join(OUT, "ambiguity_reduction_fewtimepoints.tsv"), "few-timepoints cv=0.15, 2 timepoints")
    print("BASE (cv=0.15, 4 tpts)   amb  " + " ".join(f"{m:>5}" for m in BREAKERS))
    for A in AMB: print(f"{'':22}{A}  " + " ".join(f"{base[A][M]:5.2f}" for M in BREAKERS))
    print("\nM3 time-course failure mode (score by regime):")
    for A in ["A1","A2","A3"]:
        print(f"  {A}: base={base[A]['M3']:.2f}  high-noise={hi[A]['M3']:.2f}  few-timepoints(2)={few[A]['M3']:.2f}")
    print("\nDONE. Synthetic design-map outputs are an illustration of method/design behaviour, not a result.")
