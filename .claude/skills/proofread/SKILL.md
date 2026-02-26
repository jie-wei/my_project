---
name: proofread
description: Grammar, typos, and consistency check for manuscript files. Produces a report without editing source files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Proofread Manuscript

Run the proofreading protocol on manuscript files. This produces a report of all issues found WITHOUT editing any source files.

---

## Protocol (3 Phases)

This skill defines a 3-phase protocol. The proofreader agent (`.claude/agents/proofreader.md`) follows the same protocol when invoked by the orchestrator.

### Phase 1: Review & Propose (this skill handles)
- Read all target files
- Identify every issue across 5 categories
- Produce a detailed report with structured findings
- **NEVER edit source files in this phase**

### Phase 2: User Approval (interactive)
- Present the report to the user
- User reviews and approves/rejects individual findings

### Phase 3: Apply Fixes (separate invocation)
- Only apply user-approved fixes
- Use Edit tool with `replace_all: true` for issues with multiple instances
- Re-verify after application

---

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific filename: review that file in `paper/`
   - If `$ARGUMENTS` is "all": review all `.tex` files in `paper/`

2. **For each file, check for:**

   **GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency
   **TYPOS:** Misspellings, search-and-replace artifacts, duplicated words
   **CONSISTENCY:** Citation format, notation, terminology across sections
   **ACADEMIC_QUALITY:** Informal language, vague claims, missing qualifiers, awkward constructions
   **FORMATTING:** Overfull hbox, text exceeding margins, broken references, bad spacing

3. **Produce a detailed report** for each file listing every finding with:
   - Location (line number)
   - Current text (what's wrong)
   - Proposed fix (what it should be)
   - Category and severity

4. **Save the report** — see Output Location below.

5. **Present summary** to the user:
   - Total issues found per file
   - Breakdown by category
   - Most critical issues highlighted

---

## Structured Output

After review, emit this block for agent consumption:

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

Severity guidelines:
- **CRITICAL:** Meaning-changing errors, broken references, compilation-affecting issues
- **MAJOR:** Grammatical errors, inconsistent notation, unclear claims
- **MINOR:** Style preferences, optional improvements, minor formatting

---

## Output Location

Determine the save path:
1. Check if recent context is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/proofread_[filename]_[date].md`.
3. If NO: save to `docs/core/proofread_[filename]_[date].md`.
4. Create the directory if it does not exist.

---

## Important

- **NEVER edit source files.** Only produce the report. Fixes are applied separately after user review (Phase 3).
- **Handle empty stubs gracefully.** If `paper/main.tex` is empty (0 bytes), report "Manuscript is empty — nothing to proofread."
- **Use Task tool for parallel review.** For multiple files, launch a Task agent per file to review in parallel.
- **Be specific.** Every finding must include the exact current text and proposed fix with line number. Vague suggestions like "improve clarity" are not actionable.
