#!/usr/bin/env python3
"""Validate that no synthetic / conceptual / forbidden material is presented as an empirical result.

Scans MANUSCRIPT_FULL_DRAFT_v0.3.md (and the other manuscript_synthesis/ .md/.tsv files) for tokens
that mark synthetic, scaffold, superseded, speculative, or over-reaching material. Such tokens are
allowed ONLY inside contexts that explicitly mark them as excluded/limited/future: a limitations,
prohibited-claims, future-validation, do-not-use, excluded-material, or what-we-do-not-claim section,
a negated statement, or a register file whose job is to quote them.

Writes outputs/NO_SYNTHETIC_MIXING_VALIDATION_REPORT.md and prints one of:
    NO_SYNTHETIC_MIXING_PASS       no unguarded forbidden tokens
    NO_SYNTHETIC_MIXING_WARNINGS   guarded/contextual matches only
    NO_SYNTHETIC_MIXING_FAIL       at least one unguarded forbidden token in result-level text

No new data is read or downloaded; this only inspects manuscript_synthesis/ text.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # manuscript_synthesis/
OUTPUTS = ROOT / "outputs"
REPORT = OUTPUTS / "NO_SYNTHETIC_MIXING_VALIDATION_REPORT.md"

# Tokens that must not appear as result-level text.
FORBIDDEN = [
    r"\bsynthetic\b",
    r"\bsimulated\b",
    r"\btoy\b",
    r"\bmock\b",
    r"\btest manuscript\b",
    r"\bframework-only\b",
    r"\bROUTE_B_RECOMMENDED\b",
    r"\bEMPIRICAL_ABANDONED\b",
    r"\bMERIT-M\b",
    r"\blactylation\b",
    r"\bLDHA\b",
    r"\bsample-level fusion\b",
    r"\bco-measured\b",
    r"\bcauses\b",
    r"\bdrives\b",
    r"\bproves\b",
    r"\bvalidated biomarker\b",
    r"\bpredicts clinically\b",
    r"\bNETosis rate\b",
    r"\bflux increased\b",
    r"\benzyme activity\b",
    r"\bPAD4 activity\b",
    r"\bLDHA activity\b",
]

# Register / guide / limitation files whose purpose is to quote these tokens -> matches allowed.
ALLOWED_FILES = {
    "DO_NOT_USE_AS_EMPIRICAL_RESULT.md",
    "EMPIRICAL_ONLY_ALLOWED_RESULTS.tsv",
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
    "BIOLOGICAL_LANGUAGE_GUIDE.md",
    "LIMITATIONS.md",
    "NEXT_VALIDATION_STUDIES.md",
    # Forward-looking strategic positioning / proposal scaffolds: they propose future paired
    # measurements and quote perturbation vocabulary (LDHA/lactate, PAD4, PMA/A23187) as probes for
    # hypotheses to be tested, never as results. Allowed by design, like NEXT_VALIDATION_STUDIES.
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
    "CLAIM_CEILING_TABLE.tsv",
    "EVIDENCE_TIER_SUMMARY.tsv",
    "TABLE1_BIOLOGICAL.tsv",
}

# Section headings that open an allowed (exclusion/limit/future) context.
ALLOWED_SECTION_KEYS = (
    "limitation",
    "prohibited",
    "what we do not claim",
    "future validation",
    "next validation",
    "do not use",
    "excluded material",
    "do-not-use",
)

# Negation / exclusion cues on the current or previous line.
GUARD_CUES = (
    "no ", "not ", "n't", "without", "rather than", "instead of", "did not", "does not",
    "do not", "is not", "are not", "never", "no sample", "no causal", "we did not", "we do not",
    "prohibited", "must not", "avoid", "implies", "superseded", "history only", "not a result",
    "not claimed", "we do not claim", "we did not", "hypothes",  # hypothesis/hypotheses/hypothetical
    "future", "excluded", "only as", "not download", "not used",
    # "X vs. Y" / "gap between ..." are the contrast/limit constructions separating an allowed claim
    # from the over-reading it must avoid.
    "vs.", "gap between", "interpretive limit",
)

# The v0.3 manuscript body is where result-level mixing matters most; flagged explicitly.
RESULT_LEVEL_FILE = "MANUSCRIPT_FULL_DRAFT_v0.3.md"


def is_guarded_line(line: str) -> bool:
    # Strip markdown emphasis (*, _, `) so a bolded guard like "**not**" still matches "not ".
    # Trailing space so an end-of-line cue (e.g. "... material, not") still matches "not ".
    low = re.sub(r"[*_`]", "", line).lower() + " "
    return any(cue in low for cue in GUARD_CUES)


def section_is_allowed(heading: str) -> bool:
    low = heading.lower()
    return any(k in low for k in ALLOWED_SECTION_KEYS)


def scan_file(path: Path):
    unguarded, guarded_hits = [], []
    file_allowed = path.name in ALLOWED_FILES
    current_section_allowed = False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover
        return [(0, f"<could not read: {exc}>", "")], []

    prev_lines = ["", ""]  # up to 2 previous lines, to cover wrapped sentences
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip("\n")
        if line.lstrip().startswith("#"):
            current_section_allowed = section_is_allowed(line)
        for pat in FORBIDDEN:
            m = re.search(pat, line, flags=re.IGNORECASE)
            if not m:
                continue
            term = m.group(0)
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
        status = "NO_SYNTHETIC_MIXING_FAIL"
    elif n_guarded:
        status = "NO_SYNTHETIC_MIXING_WARNINGS"
    else:
        status = "NO_SYNTHETIC_MIXING_PASS"

    lines = [
        "# No-synthetic-mixing validation report",
        "",
        f"**Status:** {status}",
        f"**Files scanned:** {len(files)}",
        f"**Unguarded forbidden tokens (result-level risk):** {n_unguarded}",
        f"**Guarded/contextual matches (allowed):** {n_guarded}",
        "",
        "## Forbidden tokens checked",
        "",
    ]
    lines += [f"- `{p}`" for p in FORBIDDEN]
    lines.append("")

    lines.append("## Unguarded forbidden tokens (must fix)")
    lines.append("")
    if all_unguarded:
        for p, entries in all_unguarded.items():
            rel = p.relative_to(ROOT)
            flag = "  [RESULT-LEVEL]" if p.name == RESULT_LEVEL_FILE else ""
            for lineno, txt, term in entries:
                lines.append(f"- **{rel}:{lineno}**{flag} — `{term}` → {txt}")
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
