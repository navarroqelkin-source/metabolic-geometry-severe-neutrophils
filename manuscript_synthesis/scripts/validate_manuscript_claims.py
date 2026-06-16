#!/usr/bin/env python3
"""Validate manuscript_synthesis claim language.

Scans every .md and .tsv under manuscript_synthesis/ for prohibited claim language and reports any
occurrence that is NOT inside an allowed context (a prohibition / limitations / claim-ceiling
section, a negated statement, or a designated prohibition column/file). Writes a report to
outputs/MANUSCRIPT_CLAIM_VALIDATION_REPORT.md and prints one of:

    MANUSCRIPT_CLAIM_VALIDATION_PASS       no unguarded prohibited claims
    MANUSCRIPT_CLAIM_VALIDATION_WARNINGS   guarded/ambiguous matches only
    MANUSCRIPT_CLAIM_VALIDATION_FAIL       at least one unguarded prohibited claim

No new data is read or downloaded; this only inspects manuscript_synthesis/ text.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # manuscript_synthesis/
OUTPUTS = ROOT / "outputs"
REPORT = OUTPUTS / "MANUSCRIPT_CLAIM_VALIDATION_REPORT.md"

# Prohibited claim language (case-insensitive substrings / small regexes).
PROHIBITED = [
    r"\bcauses\b",
    r"\bcausal\b",
    r"\bdrives\b",
    r"\bproves\b",
    r"\bdemonstrates? (?:a )?mechanism\b",
    r"\bmechanism (?:is )?demonstrated\b",
    r"\bvalidated biomarker\b",
    r"\bbiomarker (?:is )?validated\b",
    r"\bpredicts mortality\b",
    r"\bpredicts? clinical\b",
    r"\bclinical prediction\b",
    r"\bNETosis rate\b",
    r"\bflux increased\b",
    r"\bincreased flux\b",
    r"\bLDHA activity proven\b",
    r"\bPAD4 activity proven\b",
    r"\bexecuted function\b",
    r"\bkinase activity proven\b",
    r"\bsample-level fusion\b",
    # Biological-audience over-reach phrases (added for the biological revision).
    r"\bproves NETosis\b",
    r"\bdemonstrates? flux\b",
    r"\bvalidates? (?:a )?biomarker\b",
    r"\bpredicts? clinically\b",
    r"\bcauses severity\b",
    r"\bdrives disease\b",
    r"\bdrives severity\b",
]

# Files that are entirely prohibition/limitations/ceiling/proposed-future contexts.
# NEXT_VALIDATION_STUDIES proposes assays that *would* measure these quantities; proposing a
# measurement is the inverse of claiming a result, so its matches are allowed.
ALLOWED_FILES = {
    "LIMITATIONS.md",
    "CLAIM_CEILING_TABLE.tsv",
    "EVIDENCE_TIER_SUMMARY.tsv",
    "TABLE1_BIOLOGICAL.tsv",
    "NEXT_VALIDATION_STUDIES.md",
    # Forward-looking strategic positioning / proposal scaffolds. Like NEXT_VALIDATION_STUDIES, they
    # propose future paired measurements and quote perturbation/limitation vocabulary as hypotheses to
    # be tested, never as results. Allowed by design.
    "WELLCOME_STRATEGIC_POSITIONING.md",
    "WELLCOME_ONE_PAGE_CORE.md",
    "WELLCOME_SCHEME_FIT_MATRIX.md",
    "WELLCOME_NEXT_DECISION.md",
    "WELLCOME_CAREER_DEVELOPMENT_POSITIONING.md",
    "CAREER_DEVELOPMENT_PERSONAL_SCIENTIFIC_NARRATIVE.md",
    "CAREER_DEVELOPMENT_GAP_MATRIX.tsv",
    "CAREER_DEVELOPMENT_ELIGIBILITY_AND_CAPACITY_AUDIT.md",
    "WELLCOME_PREVIOUS_APPLICATION_LEARNING.md",
    "CAREER_DEVELOPMENT_COLLABORATOR_PLATFORM_MAP.tsv",
    "CICV_CAPACITY_BUILDING_PLAN.md",
    "WELLCOME_DECISION_LETTER_RESPONSE_STRATEGY.md",
    "TRACK_RECORD_AND_LEADERSHIP_EVIDENCE_REGISTER.tsv",
    "M0_FEASIBILITY_PACKAGE.md",
    "BROAD_AUDIENCE_METHODS_REWRITE_PLAN.md",
    "M0_OPERATIONAL_CHECKLIST.tsv",
    "TRACK_RECORD_EVIDENCE_TO_COLLECT.md",
    "WELLCOME_DECISION_REPAIR_MATRIX.tsv",
    "WELLCOME_RESUBMISSION_GO_HOLD_MATRIX.tsv",
    "WELLCOME_RESUBMISSION_READINESS_SUMMARY.md",
    "HOST_ADMIN_ELIGIBILITY_QUERY_TEMPLATE.md",
    "SPAIN_COLLABORATOR_EVIDENCE_TEMPLATE.md",
    "TRACK_RECORD_USER_INPUT_TEMPLATE.tsv",
    "M0_GO_EVIDENCE_COLLECTION_TEMPLATE.tsv",
    "NEXT_HUMAN_ACTIONS_BEFORE_APPLICATION.md",
    "ACADEMIC_IDENTITY_HYGIENE_CHECKLIST.md",
    "PUBLIC_TRACK_RECORD_EVIDENCE_SEED.tsv",
    "MANUSCRIPT_PUBLICATION_PRIORITY_PLAN.md",
    "MANUSCRIPT_SUBMISSION_GO_HOLD_MATRIX.tsv",
    "NEXT_FIGURES_EXECUTION_PLAN.md",
    # The language guide is a glossary that necessarily quotes the prohibited vocabulary as the
    # examples it teaches writers to avoid.
    "BIOLOGICAL_LANGUAGE_GUIDE.md",
    # Integrity-audit registers: their job is to quote prohibited/excluded vocabulary as the
    # material they catalogue. Allowed by design.
    "EMPIRICAL_ONLY_ALLOWED_RESULTS.tsv",
    "DO_NOT_USE_AS_EMPIRICAL_RESULT.md",
    "MANUSCRIPT_v0.3_RISK_PHRASES.tsv",
    "MANUSCRIPT_v0.3_INTEGRITY_REVIEW.md",
    "MANUSCRIPT_v0.4_CHANGELOG.md",
    "MANUSCRIPT_v0.4_CONTENT_REVIEW.md",
    "MANUSCRIPT_v0.5_CHANGELOG.md",
    "MANUSCRIPT_v0.6_CHANGELOG.md",
    "FINAL_ADVERSARIAL_SCIENTIFIC_REVIEW.md",
    "PRE_SUBMISSION_FIX_MATRIX.tsv",
    "FIGURE_FINALIZATION_AUDIT.md",
    "FIGURE_FINALIZATION_MATRIX.tsv",
    "IDENTIFIABILITY_V0_8_REPOSITIONING_PLAN.md",
    "MEASUREMENT_BREAKERS_TABLE_DRAFT.tsv",
}

# Section heading keywords that open an allowed (prohibition) context for the lines beneath them.
ALLOWED_SECTION_KEYS = (
    "prohibited",
    "claim ceiling",
    "interpretive limit",
    "limitation",
    "does not",
    "does not measure",
    "what it does not",
    "what we do not claim",
    "scope statement",
    "over-claim",
    "ceiling",
    "future validation",
    "next validation",
    "biological language guide",  # the guide quotes prohibited terms as examples
)

# Negation / guard cues that, when present on the SAME line, mark the match as guarded.
GUARD_CUES = (
    "no ", "not ", "n't", "without", "rather than", "instead of", "did not", "does not",
    "do not", "is not", "are not", "never", "not a ", "not the ", "no causal", "no sample",
    "prohibited", "claim ceiling", "does not measure", "we did not", "we do not",
    # "X vs. Y" and "the gap between ..." are the contrast/limit constructions used in this
    # manuscript to separate an allowed claim from the over-reading it must avoid.
    "vs.", "gap between", "cannot tell us", "interpretive limit",
    # a line that tells writers to AVOID a phrase, or warns it IMPLIES an overclaim, is guidance,
    # not a claim.
    "avoid", "implies", "must not", "over-state", "overclaim", "over-reach",
)


def is_guarded_line(line: str) -> bool:
    # Strip markdown emphasis (*, _, `) so a bolded guard like "**not**" still matches "not ".
    # Trailing space so an end-of-line cue (e.g. "... material, not") still matches "not ".
    low = re.sub(r"[*_`]", "", line).lower() + " "
    return any(cue in low for cue in GUARD_CUES)


def section_is_allowed(heading: str) -> bool:
    low = heading.lower()
    return any(k in low for k in ALLOWED_SECTION_KEYS)


def scan_file(path: Path):
    """Return (unguarded, guarded) lists of (lineno, line, term)."""
    unguarded, guarded_hits = [], []
    file_allowed = path.name in ALLOWED_FILES
    current_section_allowed = False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover
        return [(0, f"<could not read: {exc}>", "")], []

    raw_lines = text.splitlines()
    prev_lines = ["", ""]  # up to 2 previous lines, to cover sentences wrapped across ~3 lines
    for i, raw in enumerate(raw_lines, start=1):
        line = raw.rstrip("\n")
        # Track markdown section context.
        if line.lstrip().startswith("#"):
            current_section_allowed = section_is_allowed(line)
        for pat in PROHIBITED:
            m = re.search(pat, line, flags=re.IGNORECASE)
            if not m:
                continue
            term = m.group(0)
            # A guard on the current OR the previous two lines covers wrapped sentences
            # (e.g. "We do not claim ... \n a causal mechanism, ... \n or a clinical prediction.").
            guarded = is_guarded_line(line) or any(is_guarded_line(p) for p in prev_lines)
            allowed = file_allowed or current_section_allowed or guarded
            entry = (i, line.strip(), term)
            (guarded_hits if allowed else unguarded).append(entry)
        prev_lines = [prev_lines[1], line]
    return unguarded, guarded_hits


def main() -> int:
    OUTPUTS.mkdir(exist_ok=True)
    files = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and p.suffix in {".md", ".tsv"} and "outputs" not in p.parts
    )

    all_unguarded, all_guarded = {}, {}
    for p in files:
        u, g = scan_file(p)
        if u:
            all_unguarded[p] = u
        if g:
            all_guarded[p] = g

    n_unguarded = sum(len(v) for v in all_unguarded.values())
    n_guarded = sum(len(v) for v in all_guarded.values())

    if n_unguarded:
        status = "MANUSCRIPT_CLAIM_VALIDATION_FAIL"
    elif n_guarded:
        status = "MANUSCRIPT_CLAIM_VALIDATION_WARNINGS"
    else:
        status = "MANUSCRIPT_CLAIM_VALIDATION_PASS"

    lines = [
        "# Manuscript claim validation report",
        "",
        f"**Status:** {status}",
        f"**Files scanned:** {len(files)}",
        f"**Unguarded prohibited claims:** {n_unguarded}",
        f"**Guarded/contextual matches (allowed):** {n_guarded}",
        "",
        "## Prohibited patterns checked",
        "",
    ]
    lines += [f"- `{p}`" for p in PROHIBITED]
    lines.append("")

    lines.append("## Unguarded prohibited claims (must fix)")
    lines.append("")
    if all_unguarded:
        for p, entries in all_unguarded.items():
            rel = p.relative_to(ROOT)
            for lineno, txt, term in entries:
                lines.append(f"- **{rel}:{lineno}** — `{term}` → {txt}")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Guarded / contextual matches (allowed)")
    lines.append("")
    if all_guarded:
        for p, entries in all_guarded.items():
            rel = p.relative_to(ROOT)
            lines.append(f"- **{rel}** — {len(entries)} guarded match(es)")
    else:
        lines.append("_None._")
    lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(status)
    print(f"report: {REPORT}")
    print(f"files={len(files)} unguarded={n_unguarded} guarded={n_guarded}")
    return 1 if status.endswith("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
