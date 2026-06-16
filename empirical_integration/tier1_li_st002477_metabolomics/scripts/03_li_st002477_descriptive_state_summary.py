"""03 — Prudent descriptive state summary by COVID-19 severity (Control/Mild/Severe).

Median/mean per group per metabolite; relative direction across severity. Descriptive ONLY:
no statistics that imply causality, prediction, flux or function. Blank/QC excluded.
Writes outputs/LI_ST002477_GROUP_DESCRIPTIVE_SUMMARY.tsv. Degrades safely if matrix missing.
"""
import csv
import os
import statistics as st
import _li_common as L

MATRIX = os.path.join(L.OUTDIR, "LI_ST002477_intensity_matrix.tsv")
META = {"metabolite_id", "metabolite_name", "analysis_id", "units"}
ALLOWED = "descriptive metabolic STATE difference across severity (relative pool level)"
PROHIBITED = "flux / causal mechanism / clinical prediction / executed neutrophil function"


def fmt(xs):
    if not xs:
        return "NA"
    return f"median={st.median(xs):.3g}; mean={st.fmean(xs):.3g}; n={len(xs)}"


def main():
    status = L.read_tsv(L.path("LI_ST002477_INTENSITY_MATRIX_STATUS.tsv"))
    if not (status and status[0].get("matrix_found") == "YES" and os.path.exists(MATRIX)):
        L.write_tsv(os.path.join(L.OUTDIR, "LI_ST002477_GROUP_DESCRIPTIVE_SUMMARY.tsv"),
                    ["metabolite_id", "metabolite_name", "control_summary", "mild_summary",
                     "severe_summary", "relative_pattern", "allowed_interpretation",
                     "prohibited_interpretation"],
                    [{"metabolite_id": "MISSING_MATRIX", "allowed_interpretation": "none",
                      "prohibited_interpretation": PROHIBITED}])
        print("[03] MISSING_MATRIX — descriptive summary skipped safely.")
        return

    meta = {r["sample_id"]: r["group_or_condition"]
            for r in L.read_tsv(L.path("LI_ST002477_SAMPLE_METADATA.tsv"))}
    with open(MATRIX, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    header = list(rows[0].keys())
    samples = [c for c in header if c not in META]
    by_group = {g: [s for s in samples if meta.get(s) == g] for g in ("Control", "Mild", "Severe")}

    out = []
    for r in rows:
        def grp_vals(g):
            xs = []
            for s in by_group[g]:
                v = (r.get(s, "") or "").strip()
                if v:
                    try:
                        xs.append(float(v))
                    except ValueError:
                        pass
            return xs
        c, m, sv = grp_vals("Control"), grp_vals("Mild"), grp_vals("Severe")
        meds = {k: (st.median(v) if v else None) for k, v in (("C", c), ("M", m), ("S", sv))}
        if all(meds[k] is not None for k in meds):
            order = sorted(meds, key=lambda k: meds[k])
            pattern = "<".join(order) + " (by median)"
            if meds["C"] <= meds["M"] <= meds["S"]:
                pattern = "monotonic_increase_C<=M<=S"
            elif meds["C"] >= meds["M"] >= meds["S"]:
                pattern = "monotonic_decrease_C>=M>=S"
        else:
            pattern = "insufficient_data"
        out.append({
            "metabolite_id": r.get("metabolite_id", ""),
            "metabolite_name": r.get("metabolite_name", ""),
            "control_summary": fmt(c), "mild_summary": fmt(m), "severe_summary": fmt(sv),
            "relative_pattern": pattern, "allowed_interpretation": ALLOWED,
            "prohibited_interpretation": PROHIBITED,
        })
    L.write_tsv(os.path.join(L.OUTDIR, "LI_ST002477_GROUP_DESCRIPTIVE_SUMMARY.tsv"),
                ["metabolite_id", "metabolite_name", "control_summary", "mild_summary",
                 "severe_summary", "relative_pattern", "allowed_interpretation",
                 "prohibited_interpretation"], out)
    mono = sum(1 for r in out if r["relative_pattern"].startswith("monotonic"))
    print(f"[03] wrote {len(out)} metabolite descriptives; monotonic-with-severity={mono}")


if __name__ == "__main__":
    main()
