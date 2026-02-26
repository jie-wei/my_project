---
paths:
  - "paper/**/*.tex"
---

# Proofreading Agent

**Orchestrator Step 3 (REVIEW)** — Checks grammar, typos, and consistency in manuscript files. Report only — never edits source files.

This rule activates during the orchestrator's REVIEW step when the task involves LaTeX manuscript files. It follows the `/proofread` skill's Phase 1 protocol and produces a structured findings report.

---

## When This Rule Activates

- After Step 2 (VERIFY) passes for LaTeX files
- During Step 3 (REVIEW) of the orchestrator loop, **before** `review-domain.md`
- Runs on all `.tex` files in `paper/` that were modified in the current task

---

## Protocol

Follow the `/proofread` skill Phase 1 protocol (see `.claude/skills/proofread/SKILL.md`).

### 1. Identify Files to Review

- Review all `.tex` files that were modified in the current task
- If the scope is unclear, review all `.tex` files in `paper/`

### 2. Check 5 Categories

For each file, check for issues across these categories:

**GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency

**TYPOS:** Misspellings, search-and-replace artifacts, duplicated words

**CONSISTENCY:** Citation format uniformity, notation consistency across sections, terminology consistency

**ACADEMIC_QUALITY:** Informal language, vague claims ("very large"), missing qualifiers, hedging without evidence, awkward constructions

**FORMATTING:** Overfull hbox indicators, text exceeding margins, broken references (`??`), bad spacing, inconsistent list formatting

### 3. Classify Each Finding

For each issue found:
- Assign a unique ID (P001, P002, ...)
- Record FILE and LINE number
- Assign CATEGORY (from the 5 above)
- Assign SEVERITY:
  - **CRITICAL:** Meaning-changing errors, broken references, compilation-affecting
  - **MAJOR:** Grammatical errors, inconsistent notation, unclear claims
  - **MINOR:** Style preferences, optional improvements, minor formatting
- Record exact CURRENT text and exact PROPOSED fix

### 4. Map to Quality Gate Deductions

Cross-reference findings with `quality-gates.md` LaTeX rubric:
- Undefined citation (from broken refs) → -15
- Overfull hbox > 10pt → -10
- Typo in equation → -5
- Inconsistent notation → -3

### 5. Report Results

Emit the structured output block, then provide a human-readable summary grouped by severity.

---

## Structured Output

Reuse the proofread skill's output format directly (already agent-consumable):

```
--- PROOFREAD RESULT ---
STATUS: CLEAN | ISSUES_FOUND
TOTAL_ISSUES: [N]
CRITICAL: [N]
MAJOR: [N]
MINOR: [N]
TARGET: [filename or "all"]

FINDINGS:
- ID: P001
  FILE: [filename]
  LINE: [N]
  CATEGORY: GRAMMAR | TYPO | CONSISTENCY | ACADEMIC_QUALITY | FORMATTING
  SEVERITY: CRITICAL | MAJOR | MINOR
  CURRENT: "[exact current text]"
  PROPOSED: "[exact proposed fix]"
  REASON: "[brief explanation]"

- ID: P002
  ...
--- END PROOFREAD RESULT ---
```

---

## Three-Phase Protocol

This rule only executes **Phase 1** (review and propose). The full protocol:

1. **Phase 1: Review & Propose** (this rule handles during orchestrator REVIEW step)
   - Read files, identify issues, produce report
   - **NEVER edit source files**

2. **Phase 2: User Approval** (interactive, outside orchestrator loop)
   - Present findings to user
   - User accepts/rejects individual findings

3. **Phase 3: Apply Fixes** (separate invocation, outside orchestrator loop)
   - Apply only user-approved fixes
   - Use Edit tool with exact replacements
   - Re-verify after application

---

## Integration

- **Orchestrator step:** 3 (REVIEW) — runs FIRST, before `review-domain.md`
- **Skill protocol:** `proofread/SKILL.md` (canonical Phase 1 procedure)
- **Output feeds:** Step 4 (FIX) — critical and major findings become fix targets
- **Sequencing:** Proofreading catches surface issues; domain review (next) catches content issues

---

## Important

- **NEVER edit source files.** This is Phase 1 — report only. Edits happen in Phase 3 after user approval.
- **Be specific.** Every finding must include exact current text, exact proposed fix, and line number. "Improve clarity" is not actionable.
- **Handle empty stubs gracefully.** If `paper/main.tex` is empty, report "Manuscript is empty — nothing to proofread" with STATUS: CLEAN.
- **Use Task tool for parallel review.** When reviewing multiple files, launch parallel Task agents per file for efficiency.
- **Do not over-flag style preferences.** Minor issues should be genuinely useful, not pedantic. Focus on clarity and correctness.
