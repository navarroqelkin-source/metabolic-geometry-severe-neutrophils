# Chapman–Li Evidence-Tiered Bridge Report

This bridge is not a sample-level integration. It is an evidence-tiered synthesis linking
independent NET/release proteome composition evidence with an independent Tier 1 metabolomic
severity-state axis.

## 1. What Chapman contributes
NET/release proteome **material composition** (Tier 3): NETs decorated with histones,
myeloperoxidase and neutrophil elastase; citrullinated peptides (RA) and nuclear neoepitopes (SLE);
quantitative NET proteome compared across healthy / RA / SLE (Front Immunol 2019, PMID 30915077).
Repository PXD011796 is raw/peak-list only — quantitative tables live in the open-access supplement
(Tier 2 only if that supplement is parsed).

## 2. What Li_ST002477 contributes
Tier 1 metabolomic **state** axis: kernel-supported severity separation (Control/Mild/Severe),
183/287 metabolites FDR-significant, 85 monotonic, module **M05 (glycolysis/PPP) SUPPORTED**;
top contributors include purine/redox (hypoxanthine), carnitines and amino acids (β-alanine).
M08 (lipid mediators) not represented in this HILIC panel.

## 3. Permitted bridge (3 links)
- **BR01** (material_state_alignment): NET/release material composition + Li global metabolic
  severity separation → metabolic state and extracellular effector material are complementary,
  non-equivalent neutrophil layers.
- **BR02** (module_context_alignment): NET/release material ↔ M05 central-carbon/PPP — context
  alignment, not a measured or mechanistic relationship.
- **BR03** (hypothesis_generating_cross_layer_link): NET/release oxidative/chromatin material ↔
  severity-associated purine/redox/carnitine/amino-acid contributors — a hypothesis to test with
  paired data.

## 4. Prohibited bridge
Sample-level correlation/fusion; co-measurement; causal mechanism; metabolism→NETosis inference;
NETosis **rate**; NET **clearance**; NET **pathogenicity**; "Li demonstrates NETosis"; "Chapman
measures NETosis rate"; metabolic flux; biomarker; executed function.

## 5. How NET/release material connects to metabolic state without claiming NETosis
Chapman reports the **composition** of released NET material (which proteins are present), and Li
reports the **state** of the metabolite pool by severity. Both are static descriptions of
activated-neutrophil biology. Placing them side by side is a material/module context alignment — it
says nothing about how fast NETs form, whether they are cleared, or whether metabolism drives their
release. A static pool is not a flux; a proteome inventory is not a rate.

## 6. Why this strengthens evidence-tiered pan-omic integration
With NeuMap–Li and now Chapman–Li, three independent layers are articulated under explicit claim
ceilings: RNA/multiome state architecture (NeuMap), quantitative metabolic state (Li), and
extracellular effector material (Chapman). Together they support the neutrophil-as-multilayer,
temporally-desynchronized-state hypothesis — without any fabricated sample-level link.

## 7. Next steps
- If the Chapman open-access supplement is parsed into a processed table, Chapman moves toward
  Tier 2 and BR02/BR03 become more structured (still no NETosis-rate or causal claim).
- Consider PXD029046 (phosphosignaling state) as a fourth layer, again as an evidence-tiered bridge.

> This bridge is not a sample-level integration. It is an evidence-tiered synthesis linking
> independent NET/release proteome composition evidence with an independent Tier 1 metabolomic
> severity-state axis.

## Tier 2 refresh (DEC-046)
Chapman is now Tier 2 (752 structured proteins). Its NET/release side is refined into effector-material
modules — chromatin/histone (32), granule/protease (31), MPO/oxidative (14), cytoskeletal (46),
nuclear-antigen (17) — mapped by gene-symbol markers (141 assigned; 611 in NET_other; citrullinated
PTM data live in Table_6, not this protein list). Tier 2 bridges to the Li axis: T2_BR01/02
(histone, granule-protease ↔ global metabolic state), T2_BR03 (MPO/oxidative ↔ purine/redox
contributors, hypothesis-generating), T2_BR05 (NET material modules ↔ M05). Claim ceiling unchanged:
NET material composition only — not NETosis rate, clearance, pathogenicity or causality.
See `../chapman_tier2_module_mapping/`.
