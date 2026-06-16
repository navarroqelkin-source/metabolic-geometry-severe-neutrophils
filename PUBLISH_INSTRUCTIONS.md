# How to publish this repository (GitHub + Zenodo) — RUN BY THE PI

This folder is a ready-to-upload public-repository package. **Nothing has been published.** Two blockers
must be resolved first:

1. **Author metadata** — replace every `TODO_PI_INPUT_REQUIRED` in `CITATION.cff` and `.zenodo.json`
   (names, ORCID, affiliation), and the `[AUTHORS ...]` line in `LICENSE`.
2. **License confirmation** — defaults are MIT (code) + CC BY 4.0 (text/figures/derived data). Change if needed.

## A. Create the GitHub repo and push
```
# from inside this folder (it is already a local git repo with an initial commit):
gh repo create <owner>/metabolic-geometry-severe-neutrophils --public --source . --remote origin --push
# or, without gh:
#   create an empty public repo on github.com, then:
#   git remote add origin https://github.com/<owner>/<repo>.git
#   git branch -M main && git push -u origin main
```

## B. Create the release (triggers Zenodo if connected)
```
git tag -a v0.8.2 -m "v0.8.2"
git push origin v0.8.2
# or: gh release create v0.8.2 --title "v0.8.2" --notes-file CHANGELOG.md
```

## C. Zenodo
- Easiest: log in to Zenodo with GitHub, enable the repository under Settings → GitHub, then make the
  GitHub release (step B); Zenodo mints a version DOI automatically (`.zenodo.json` supplies the metadata).
- Or: upload this folder as a .zip directly at zenodo.org/uploads, paste the metadata from `.zenodo.json`,
  and publish to mint the DOI.

## D. After the DOI exists
Insert the **version-specific** Zenodo DOI into `CITATION.cff`, `.zenodo.json`, the manuscript Data/Code
Availability statements, and the cover letter — then proceed with the bioRxiv preprint and the Frontiers submission.
