---
name: validate-bib
description: Cross-reference citations in manuscript against bibliography entries
disable-model-invocation: true
argument-hint: "[optional: path to .bib file, default: paper/references.bib]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Validate Bibliography

Cross-reference all citations in manuscript files against bibliography entries.

**Input:** `$ARGUMENTS` — optional path to a `.bib` file. Defaults to `paper/references.bib`.

---

## Steps

1. **Read the bibliography file** and extract all citation keys.

2. **Scan all manuscript files for citation keys:**
   - `.tex` files in `paper/`: look for `\cite{`, `\citet{`, `\citep{`, `\citeauthor{`, `\citeyear{`, `\citealp{`, `\textcite{`, `\parencite{`, `\autocite{`
   - Extract all unique citation keys used

3. **Cross-reference:**
   - **Missing entries:** Citations used in manuscript but NOT in bibliography
   - **Unused entries:** Entries in bibliography not cited anywhere
   - **Potential typos:** Similar-but-not-matching keys (edit distance <= 2)

4. **Check entry quality** for each bib entry:
   - Required fields present (author, title, year, journal/booktitle)
   - Author field properly formatted
   - Year is reasonable (1800-current)
   - No malformed characters or encoding issues

5. **Report findings** using the structured output format below.

6. **Save the report** — see Output Location below.

---

## Structured Output

After validation, emit this block for agent consumption:

```
--- VALIDATION RESULT ---
STATUS: PASS | FAIL
MISSING_COUNT: [N]
UNUSED_COUNT: [N]
TYPO_COUNT: [N]
QUALITY_COUNT: [N]

MISSING (CRITICAL):
- [citation_key] — used in [file:line]

UNUSED (INFO):
- [citation_key]

TYPOS (WARNING):
- [used_key] → did you mean [bib_key]? (in [file:line])

QUALITY (WARNING):
- [citation_key] — [issue: missing field, bad year, encoding error, etc.]
--- END VALIDATION RESULT ---
```

STATUS is FAIL if MISSING_COUNT > 0. Otherwise PASS.

---

## Output Location

Determine the save path:
1. Check if recent context is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/bib_validation_[date].md`.
3. If NO: save to `docs/core/bib_validation_[date].md`.
4. Create the directory if it does not exist.

---

## Files to scan

```
paper/*.tex          — manuscript files
paper/references.bib — bibliography (or $ARGUMENTS)
```

---

## Important

- **Handle empty stubs gracefully.** If `paper/references.bib` is empty, report "Bibliography file is empty — no entries to validate" rather than failing.
- **Handle empty manuscript gracefully.** If `paper/main.tex` is empty, report "Manuscript is empty — no citations to check."
- **Do not modify any files.** This is a read-only analysis. Report findings; do not fix them.
