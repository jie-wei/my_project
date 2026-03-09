---
name: review-summary
description: >-
  Fact-check a summary document against the actual pipeline outputs. Use this
  skill whenever the user asks to verify a summary, fact-check a draft, check
  numbers in a report, or review a summary against data. Also use when the
  orchestrator routes draft/*.tex files for review. This skill treats every
  number and claim in the summary as something to verify against source files.
  Distinct from /review-manuscript (qualitative academic review) and
  /review-details (grammar/typos). Do NOT use for writing summaries (use
  /write-summary) or reviewing code (use /review-code).
disable-model-invocation: false
argument-hint: "[summary to review, e.g. 'review the {variant-name} summary']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# Review Summary

Fact-check a summary document against the actual pipeline outputs. Treat the summary as a set of claims to verify — do NOT trust it. For every number you cite in the report, verify it matches the source data. Do NOT trust your own reading — treat each value as a claim to double-check before writing it down.

**Input:** `$ARGUMENTS` — what to review (e.g., "fact-check the {variant-name} summary", "verify the {variant-name} draft", "check numbers in the {variant-name} report").

---

## Step 1: Locate the Summary

Find the `.tex` file from `$ARGUMENTS` or context:
- Direct path if provided
- `draft/{tier}/{variant-name}/summary-{variant-name}.tex`
- Glob for matches in `draft/`

If the summary doesn't exist, tell the user and stop.

---

## Step 2: Read the Code Pipeline

Understanding which script produces which output is essential for knowing what source files to check against.

- List scripts in `code/scripts/{tier}/{variant-name}/` (exploration/archive) or numbered scripts in `code/scripts/{tier}/` (core)
- Read each script to identify: what data it loads, what it outputs, where it saves
- Read relevant src modules in `code/src/mypackage/{tier}/{variant-name}/`
- **Trace the full I/O chain**: for each script, verify that it reads from the correct input paths and writes to the correct output paths for this variant. A script reading from the wrong source or writing to the wrong directory means the summary will be checked against wrong data — catch this before proceeding.
- Build a map: output file → script that produced it → input data it used

---

## Step 3: Inventory All Source Files

Scan and read every source file that the summary could reference:

**Tables** (`output/{tier}/tables/{variant-name}/`):
- Read `.csv` files — column names, values, sample sizes
- Read `.tex` files — formatted regression output from fixest/etable

**Figures** (`output/{tier}/figures/{variant-name}/`):
- List all `.png` and `.pdf` files — these are the valid figure references

**Processed data** (`data/processed/{variant-name}/`):
- Read any `.csv` files that scripts use as intermediate inputs (diagnostics, summary stats)

Build a ground-truth reference from these files before reading the summary.

---

## Step 4: Read the Summary

Read the summary document section by section. For every number, statistical claim, or figure reference, note its location (section, approximate line) and what it claims.

---

## Step 5: Verify Numerical Claims

For each number in the summary — coefficients, standard errors, p-values, significance stars, N, R², accuracy, correlation, sample sizes, means, percentages, counts:

- Find the corresponding value in the source file
- Compare exactly (accounting for rounding conventions)
- If they don't match, record:
  - **Location:** section and line in the summary
  - **Claimed:** what the summary says
  - **Actual:** what the source file shows
  - **Source:** path to the source file

The most common errors are transcription mistakes (copying a number wrong), stale numbers (the pipeline was rerun but the summary wasn't updated), and rounding inconsistencies.

---

## Step 6: Verify Regression Tables

For each `\input{}` command that pulls in a `.tex` table:

- Read the actual `.tex` file from the output directory
- Compare every coefficient, standard error, and significance star
- Check that column headers and variable labels match
- Flag any discrepancy

This catches cases where the summary's `\input{}` path is correct but the surrounding prose misquotes a coefficient from the table.

---

## Step 7: Verify Figure References

For each `\includegraphics{}` command:

- Extract the file path (resolving `\outdir` to the actual output directory)
- Confirm the file exists
- Flag any missing figures

---

## Step 8: Check Qualitative Claims

Verify prose characterizations against the data:

- "Large positive effect" — is the coefficient actually large and positive?
- "Significant at the 1% level" — does the source show significance at that level?
- "Increases monotonically" — does the data actually show monotonic increase?
- "Robust across specifications" — do the robustness checks actually confirm this?
- "Similar to the baseline" — are the values actually comparable?

Flag claims that mischaracterize the direction, magnitude, significance, or pattern in the data.

---

## Step 9: Check for Orphaned Outputs

List any files in the output directories that are NOT referenced in the summary:
- `output/{tier}/tables/{variant-name}/` — unreferenced `.tex` or `.csv` files
- `output/{tier}/figures/{variant-name}/` — unreferenced `.png` or `.pdf` files

These may be results the summary should discuss but missed. Report them so the user can decide whether to add them or confirm they're intentionally excluded.

---

## Step 10: Produce the Report

Generate a structured markdown report.

**If discrepancies found:**

```markdown
# Fact-Check Report: {variant-name}

**Date:** YYYY-MM-DD
**Summary:** draft/{tier}/{variant-name}/summary-{variant-name}.tex
**Status:** DISCREPANCIES FOUND

## Numerical Errors

1. **[Section Name], line ~N:** Claims [value]. Actual value is [value] (source: `output/{tier}/tables/{variant-name}/file.csv`).
2. ...

## Table Mismatches

1. **Table N (label):** [description of mismatch]
2. ...

## Missing Figures

1. `\includegraphics` references `path/to/file.png` — file not found.
2. ...

## Qualitative Errors

1. **[Section Name]:** Claims "[quoted text]". Data shows [what it actually shows] (source: `file`).
2. ...

## Orphaned Outputs

These output files are not referenced in the summary:
- `output/{tier}/tables/{variant-name}/unreferenced_file.csv`
- ...
```

**If everything checks out:**

```markdown
# Fact-Check Report: {variant-name}

**Date:** YYYY-MM-DD
**Summary:** draft/{tier}/{variant-name}/summary-{variant-name}.tex
**Status:** CLEAN

All numerical claims verified against source files. All figure references valid. No orphaned outputs.
```

**Structured output block** (for orchestrator consumption):

```
--- REVIEW RESULT ---
STATUS: CLEAN | DISCREPANCIES_FOUND
TARGET: [path to summary]
NUMERICAL_ERRORS: [N]
TABLE_MISMATCHES: [N]
MISSING_FIGURES: [N]
QUALITATIVE_ERRORS: [N]
ORPHANED_OUTPUTS: [N]
OVERALL: [1-5]
--- END REVIEW RESULT ---
```

Scoring: 5 = all clean, 4 = orphaned outputs only, 3 = minor issues (rounding, 1-2 small errors), 2 = multiple errors, 1 = pervasive inaccuracies.

---

## Step 11: Save

Save the report to `docs/quality_reports/reviews/{tier}/review-summary-{variant-name}.md`. Create the directory if it does not exist. The report replaces the previous one on re-run — no date suffix.

---

## Principles

**Why read the pipeline first.** You can't verify a summary without knowing what the ground truth is. Reading the code tells you which scripts produce which outputs, so you know exactly which source files to check each claim against. Without this step, you might miss source files or check against the wrong ones.

**Why treat the summary as untrustworthy.** The summary was written by an LLM interpreting outputs. LLMs can misread numbers, round inconsistently, or describe patterns that aren't quite what the data shows. Every number and characterization needs independent verification against the source file — never assume the summary is correct just because it looks plausible.

**Why check qualitative claims.** A factually correct number paired with a misleading description is worse than a typo. "The effect is large" when the coefficient is 0.001 misleads the reader even though no specific number is wrong. Checking characterizations catches these subtle but important errors.

**Why flag orphaned outputs.** If the pipeline produced a table or figure that the summary doesn't mention, it might contain important results that were accidentally omitted. Better to flag them and let the user decide than to let results go unreported.
