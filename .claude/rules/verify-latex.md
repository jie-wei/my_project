---
paths:
  - "paper/**/*.tex"
---

# LaTeX Verification Agent

**Orchestrator Step 2 (VERIFY)** — Compiles LaTeX documents and validates bibliography integrity.

This rule activates during the orchestrator's VERIFY step when the task involves LaTeX manuscript files. It invokes the `/compile-latex` and `/validate-bib` skill protocols and parses their structured output.

---

## When This Rule Activates

- After implementing changes to any `.tex` file in `paper/`
- During Step 2 (VERIFY) of the orchestrator loop
- Also triggered when bibliography (`paper/references.bib`) is modified

---

## Protocol

### 1. Compile the Manuscript

Follow the `/compile-latex` skill protocol (see `.claude/skills/compile-latex/SKILL.md`):

1. Check that the target file exists (`paper/main.tex` or as specified)
2. If the file is empty (0 bytes), report "Manuscript is empty — cannot compile" and set STATUS: FAIL
3. Run the 3-pass compilation sequence as a **single compound Bash command** (critical — the `latex-cleanup` hook deletes .log files after each Bash call):

```bash
cd paper && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex && \
BIBINPUTS=.:$BIBINPUTS bibtex main && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex && \
echo "=== PARSE LOG ===" && \
grep -c "Warning" main.log 2>/dev/null || echo "0" && \
grep -c "^! " main.log 2>/dev/null || echo "0" && \
grep "Citation.*undefined" main.log 2>/dev/null || echo "none" && \
grep -c "Overfull" main.log 2>/dev/null || echo "0" && \
pdfinfo main.pdf 2>/dev/null | grep Pages || echo "Pages: unknown"
```

4. Parse the `--- COMPILATION RESULT ---` block from the skill output

### 2. Validate the Bibliography

Follow the `/validate-bib` skill protocol (see `.claude/skills/validate-bib/SKILL.md`):

1. Read `paper/references.bib` and extract all citation keys
2. Scan all `paper/*.tex` files for citation commands (`\cite{`, `\citet{`, `\citep{`, etc.)
3. Cross-reference: missing entries, unused entries, potential typos
4. Check entry quality: required fields, author format, year range
5. Parse the `--- VALIDATION RESULT ---` block

### 3. Combine Results

Merge compilation and bibliography results into a unified verification report.

- **FAIL if:** compilation fails OR any missing citations exist
- **PASS if:** PDF created successfully AND no missing citations

---

## Structured Output

After verification, emit this block for orchestrator consumption:

```
--- VERIFY LATEX RESULT ---
STATUS: PASS | FAIL
TARGET: [file path]

COMPILATION:
  STATUS: SUCCESS | FAILURE
  WARNINGS: [N]
  ERRORS: [N]
  PAGES: [N]
  UNDEFINED_CITATIONS: [list or "none"]
  OVERFULL_HBOX: [N]

BIBLIOGRAPHY:
  STATUS: PASS | FAIL
  MISSING: [N]
  UNUSED: [N]
  TYPOS: [N]
  QUALITY_ISSUES: [N]

BLOCKING_ISSUES: [N]
--- END VERIFY LATEX RESULT ---
```

BLOCKING_ISSUES = compilation errors + missing citations. Warnings and unused entries are advisory.

---

## Integration

- **Orchestrator step:** 2 (VERIFY)
- **Skill protocols:** `compile-latex/SKILL.md` and `validate-bib/SKILL.md` (canonical procedures)
- **On FAIL:** Orchestrator loops back to fix compilation errors or missing citations, then re-verifies (max 2 retries)
- **On PASS:** Orchestrator proceeds to Step 3 (REVIEW) — `proofread-manuscript.md` then `review-domain.md`

---

## Hook Interaction

The `latex-cleanup` hook automatically deletes auxiliary files (`.aux`, `.log`, `.bbl`, `.blg`, etc.) after each Bash command that contains LaTeX compilation commands. **All log parsing must happen in the same Bash invocation as the compilation** — use compound commands with `&&`.

---

## Important

- **Empty stubs:** If `paper/main.tex` is empty, report gracefully instead of running LaTeX (which produces cryptic errors).
- **TEXINPUTS:** Always set `TEXINPUTS=../docs/preambles:$TEXINPUTS` to find custom preamble files.
- **BIBINPUTS:** Set `BIBINPUTS=.:$BIBINPUTS` to find `references.bib` in `paper/`.
- **XeLaTeX default.** Fall back to pdflatex only if the document requires it (e.g., eps figures).
- **Do not modify source files.** This is verification only. Fixes happen in Step 4.
