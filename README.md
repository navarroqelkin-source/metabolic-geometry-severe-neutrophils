> # ⚠️ SCIENTIFIC SUPERSESSION NOTICE — 2026-07-19
>
> **A central claim in this repository has been withdrawn by the authors.** The
> severity-ordering claim (Control-Severe > Control-Mild > Mild-Severe), the statement that
> Control-Severe is the largest/dominant contrast, and the statement that the two metrics agree
> on that ordering are **not supported** and must not be cited or reused.
>
> Cause: the MMD bandwidth was pair-specific (three different RKHS, so the three magnitudes are
> not mutually comparable) and the energy distance used a biased V-statistic whose per-pair bias
> does not cancel in an ordering and whose direction is indeterminate before the within-group
> dispersions are computed.
>
> Statements about a **single** pairwise contrast are unaffected. Nothing has been deleted;
> history is preserved. Full detail: **[NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md](NOTICE_SCIENTIFIC_SUPERSESSION_2026-07-19.md)**
>
> An independent metric audit is underway. A corrected package will follow.

# The metabolic geometry of severe human neutrophils — analysis code and derived data

Reproducible code, derived data and figures for the manuscript
**"The metabolic geometry of severe human neutrophils: redox–carbon state separation and the limits of
inferring effector function"** (Hypothesis and Theory).

Archived on Zenodo: https://doi.org/10.5281/zenodo.20717146 · Repository: https://github.com/navarroqelkin-source/metabolic-geometry-severe-neutrophils

> Public datasets only. No patient-level or private data. This repository contains analysis code, the
> manuscript, figures, and **derived** result tables — not raw third-party data (obtain those from the
> accessions below).

## Layout
- `manuscript_synthesis/MANUSCRIPT_FULL_DRAFT_v0.8.md` — manuscript text.
- `manuscript_synthesis/figures/` — final figures (SVG) and exports (`final_exports/pdf`, `final_exports/png_600dpi`).
- `manuscript_synthesis/TABLE1_BIOLOGICAL.tsv`, `MEASUREMENT_BREAKERS_TABLE_DRAFT.tsv` — Tables 1–2.
- `manuscript_synthesis/VERIFIED_REFERENCES_MASTER.tsv` — references.
- `manuscript_synthesis/SUPPLEMENTARY_NOTE_SIMULATION_DESIGN_MAP.md` + `SIMULATION_DESIGN_MAP_*` — supplement.
- `manuscript_synthesis/scripts/` — claim-ceiling validators.
- `empirical_integration/kernel_state_separation/` — **metabolic state-separation reanalysis (Figures 3–4)**:
  MMD and energy-distance results, per-feature FDR / monotonicity / Cliff's delta / bootstrap stability,
  module-level summary, and reports (the complete outputs behind Figures 3–4).
- `empirical_integration/chapman_*` — released-material proteome + PTM structuring (Figure 5).
- `modeling/minimal_net_burden_model/`, `modeling/measurement_design_map/` — observation model + in silico
  measurement-design map (illustrations of method/design behaviour, not results).

## Reproduce
Python 3.10; `pip install -r requirements.txt`. Then:
```
python manuscript_synthesis/scripts/validate_manuscript_claims.py
python manuscript_synthesis/scripts/validate_no_synthetic_manuscript_mixing.py
python modeling/measurement_design_map/simulation_design_map.py
```
The metabolic reanalysis outputs (Figures 3–4) are in
`empirical_integration/kernel_state_separation/outputs/` and `.../localization/`.

## Source datasets (not redistributed here)
- Metabolome: Metabolomics Workbench **ST002477** (Li et al., Nat Commun 2023; 10.1038/s41467-023-37567-w).
- NET/release proteome + PTM: PRIDE **PXD011796** (Chapman et al., Front Immunol 2019; 10.3389/fimmu.2019.00423).
- Phosphosignaling: PRIDE **PXD029046** (Yedehalli Thimmappa et al., Cell Tissue Res 2022; 10.1007/s00441-022-03636-7).
- Cell-state atlas: **NeuMap** (Cerezo-Wallis et al., Nature 2026;649:1003-1012; 10.1038/s41586-025-09807-0).

## Claim ceilings
Evaluates layer-specific states/composition and measurement-design identifiability; does **not** estimate
biological parameter values, flux, ROS, NETosis, enzyme activity, executed function or clinical mechanism.
Simulation/design-map outputs are illustrations of method/design behaviour, not results.

## License & citation
Code: MIT (`LICENSE`). Manuscript text, figures and derived data: CC BY 4.0 (`LICENSE-DATA.md`).
Cite via `CITATION.cff`. **Before publishing:** confirm the license and complete author metadata in
`CITATION.cff` and `.zenodo.json` (see `PUBLISH_INSTRUCTIONS.md`).
