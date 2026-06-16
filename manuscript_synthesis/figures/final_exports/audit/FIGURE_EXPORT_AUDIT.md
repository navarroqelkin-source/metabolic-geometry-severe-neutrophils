# FIGURE_EXPORT_AUDIT

## Export tool
**RESOLVED.** The export was completed with **headless system Chrome** (a browser — the same
engine class these SVGs were authored and previewed in, and the ground truth for the
middle-anchored-tspan lines that the rasterizers below mis-place). See "Local export result"
at the bottom. The original blocker analysis is retained below for traceability.

Earlier finding: no *rasterizer* (Inkscape / rsvg / cairosvg / svglib) gave a faithful render;
cairosvg and svglib mis-placed inline tspans. Browser rendering avoids that defect entirely.

Tools probed (2026-06-11):

| Tool | Available | Verdict |
|---|---|---|
| Inkscape (`inkscape`) | No (`command not found`) | Preferred tool — install locally |
| `rsvg-convert` (librsvg) | No (`command not found`) | Acceptable alternative — install locally |
| `cairosvg` + `cairo` | Installed here (cairo via conda-forge) | **Unfaithful for this set** — see defect below |
| `svglib` + `reportlab` | Installed here | **Unfaithful for this set** (worse than cairosvg) |
| `PyMuPDF` (`fitz`) | Yes (1.27.2) | PDF→PNG rasterizer only; cannot fix the upstream SVG defect |
| Pillow | Yes (12.0.0) | Cannot rasterize SVG on its own |

## Export date
2026-06-11 (probe + fidelity test + final render). Final render completed in-environment with
headless Chrome — see "Local export result" below.

## Input SVG set (final, XML-valid)
- Figure1_evidence_map_and_navigation.svg
- Figure2_NET_burden_identifiability.svg
- Figure3_metabolic_state_separation.svg
- Figure4_metabolic_contributors_M05.svg
- Figure5_NET_release_PTM_material.svg
- Figure6_NeuMap_reference_architecture.svg
- Figure7_four_layer_model.svg

All seven parse as well-formed XML.

## Output PDF set
7/7 committed in `final_exports/pdf/FigureN_*.pdf` (vector; headless Chrome). See result section.

## Output PNG 600 dpi set
7/7 committed in `final_exports/png_600dpi/FigureN_*.png` (600 dpi, white background; Chrome PDF → MuPDF).

## Checks performed
1. Tool availability probe (table above).
2. Fidelity test render of Figure 2 with **svglib→PDF→PNG (PyMuPDF)** and with **cairosvg→PNG**,
   inspected at high zoom.

## Problem detected — rasterizer text-placement defect (not an SVG defect)
Both available rasterizers (cairosvg and svglib) **mis-place inline `<tspan>` runs inside a
`<text text-anchor="middle">` element**: the coloured emphasis run is centred on the parent
`x` instead of flowing in sequence, so it overprints the surrounding text.

- Reproduced on **Figure 2, line 67** — the phrase `a [second, stacked] source of
  non-identifiability: even a known B …` renders with `second, stacked` overprinting
  `identifiability`.
- Per the SVG specification, a `<text>` with an unpositioned child `<tspan>` is a single
  addressable text chunk: the whole string is anchored as one unit and flows left-to-right.
  **Browsers (the engine these figures were authored and previewed in) render this correctly.**
  cairosvg/cairo and svglib diverge from the spec here.
- This is therefore a **rasterizer limitation, not a defect in the source SVG.** The SVGs were
  intentionally left unchanged; contorting correct source to satisfy a non-compliant rasterizer
  was rejected.

### At-risk lines (middle-anchored text containing an inline tspan)
| Figure | Line | Content | Risk |
|---|---|---|---|
| Figure 2 | 42 | `… are [observationally equivalent] at a single time point` | mis-place under cairosvg/svglib |
| Figure 2 | 67 | `a [second, stacked] source of non-identifiability …` | **confirmed overprint** |
| Figure 7 | 113 | `… read as complementary, [not co-measured].` | mis-place under cairosvg/svglib |

Start-anchored tspans (Figure 1 L126, Figure 5 L66) render cleanly and are not at risk.

## Figure-by-figure notes (blocker-era; superseded by the Local export result below)
- **Fig 1, 3, 4, 5, 6:** no confirmed defect under the available rasterizers; the whole set was
  ultimately produced with a single faithful toolchain (headless Chrome) for consistent fonts and colours.
- **Fig 2, 7:** require a spec-compliant engine (browser/Inkscape/rsvg) for the middle-anchored tspan
  lines; rendered correctly by headless Chrome (verified at 600 dpi).

## Decision
- **Do not** commit cairosvg/svglib output (would ship Fig 2 / Fig 7 with overprinted text).
- **Do not** alter the SVG source (it is spec-correct and renders correctly in browsers).
- **Export locally** with Inkscape (preferred) or `rsvg-convert`, then drop the files into
  `final_exports/pdf/` and `final_exports/png_600dpi/` and flip the manifest status to `OK`.

---

## Local export instructions (run on a machine with Inkscape ≥ 1.0)

```bash
cd <repo>/discovery/ORIGINAL_NEUTROPHIL_TEMPORAL_MULTIOMICS_IDENTIFIABILITY/manuscript_synthesis
FIGDIR=figures
OUT=figures/final_exports
for f in "$FIGDIR"/Figure*.svg; do
  base=$(basename "$f" .svg)
  inkscape "$f" --export-type=pdf --export-filename="$OUT/pdf/${base}.pdf"
  inkscape "$f" --export-type=png --export-dpi=600 --export-background=white \
           --export-filename="$OUT/png_600dpi/${base}.png"
done
```

Alternative with librsvg (`rsvg-convert`), if Inkscape is unavailable:

```bash
for f in "$FIGDIR"/Figure*.svg; do
  base=$(basename "$f" .svg)
  rsvg-convert -f pdf -o "$OUT/pdf/${base}.pdf" "$f"
  rsvg-convert -f png -d 600 -p 600 -b white -o "$OUT/png_600dpi/${base}.png" "$f"
done
```

After exporting, visually confirm on **Figure 2** and **Figure 7** that the coloured emphasis
phrases flow inline (no overprint), then update `FIGURE_EXPORT_MANIFEST.tsv` (status → `OK`).

**Do NOT** use cairosvg or svglib for the definitive export — both mis-place the middle-anchored
tspan lines documented above.

---

## Local export result

- **Renderer:** headless **Google Chrome 149.0.7827.55** (`--headless=new --print-to-pdf`,
  each SVG wrapped in a zero-margin `@page`-sized HTML so the PDF is tight to the figure bounds).
  Browser = ground-truth engine for these SVGs; chosen because Inkscape/rsvg were unavailable and
  uninstallable (conda solver broke during the probe — see note) and cairosvg/svglib are unfaithful.
- **PNG 600 dpi:** rasterised from each Chrome vector PDF with **PyMuPDF (MuPDF) 1.27.2** at 600 dpi,
  white background.
- **Date:** 2026-06-11.
- **PDF exports:** OK — 7/7 (`final_exports/pdf/`), vector, page sized to each figure (e.g. Fig 2 = 750×480 pt = 1000×640 px).
- **PNG 600 dpi exports:** OK — 7/7 (`final_exports/png_600dpi/`), e.g. Fig 1 6500×5300, Fig 2 6250×4000, Fig 7 6500×4126.
- **Visual inspection:** OK. Full-set contact sheet reviewed (`audit/FIGURE_SET_CONTACT_SHEET.png`):
  titles and footers not clipped, white backgrounds, faithful colours, no clipping.
- **Known cairo/svglib tspan issue:** avoided. Verified at 600 dpi that the previously-overprinting
  middle-anchored inline-tspan lines flow inline correctly: **Fig 2 L42** ("observationally equivalent"),
  **Fig 2 L67** ("second, stacked"), **Fig 7 L113** ("not co-measured").
- **Contact sheet:** created (`audit/FIGURE_SET_CONTACT_SHEET.png`, 7 figures, 2×4, labelled).
- **Decision:** **final figure exports ready for the submission package.** SVG sources unchanged.
  If a different production toolchain is required by the journal, re-export from the unchanged SVGs
  with Inkscape/rsvg using the commands above (browser and Inkscape both render these lines correctly).

### Environment note (conda)
During tool probing, `conda install` left the conda **solver** broken in the base env
(`conda-libmamba-solver: module 'libmambapy' has no attribute 'QueryFormat'`); `conda install`
now fails although Python itself is unaffected. This did not block the export (Chrome + MuPDF were
used). Repair, if desired: `conda install -n base conda-libmamba-solver libmambapy --solver classic`
or `conda config --set solver classic`.
