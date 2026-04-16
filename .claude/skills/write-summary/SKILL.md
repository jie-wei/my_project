---
name: write-summary
description: >-
  LaTeX summary document from existing work. Two modes: (A) empirics — summarize
  pipeline outputs (tables, figures) into a report with methodology, results,
  discussion; (B) theory — synthesize math formulation notes (.md result files)
  into a self-contained proof walkthrough. Use this skill whenever the user asks
  to summarize results, write up findings, draft a summary, compile results into
  a document, create a report, write up a proof, or synthesize theory notes.
  Do NOT use for implementing code (use /write-code) or running new analyses
  (use /analyze-data). This skill turns existing work into a coherent LaTeX document.
disable-model-invocation: true
argument-hint: "[what to summarize, e.g. 'summarize the {variant_name} results']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
---

# Write Summary

Produce a LaTeX summary document for one variant. Two modes: empirics (from pipeline outputs) and theory (from math formulation notes).

**Input:** `$ARGUMENTS` — what to summarize (e.g., "summarize the {variant_name} results", "write up the {variant_name} findings").

---

## Step 1: Identify Variant, Tier, and Mode

Determine the tier (core / exploration / archive) and variant_name from context (user instruction, open files, cwd).

Determine the mode by checking what exists:

**Empirics:** `output/{tier}/tables/{variant_name}/` or `output/{tier}/figures/{variant_name}/` exist → read `references/workflow-empirics.md` and follow it.

**Theory:** No pipeline outputs, but `docs/{tier}/{variant_name}/` contains `.md` result files, notes, or formulations → read `references/workflow-theory.md` and follow it.

If neither exists, tell the user and stop.

---

## Step 2–7: Mode-Specific Workflow

Follow the workflow file loaded in Step 1. It covers: reading sources, scanning outputs, identifying connections, brainstorming interpretations, reading the LaTeX template, and writing the document.

---

## Step 8: Assemble & Save

- Create `docs/{tier}/{variant_name}/` directory (if not already present)
- Save to `docs/{tier}/{variant_name}/summary-{variant_name}.tex`
- **Important:** compile from the directory containing the `.tex` file so relative paths resolve correctly

---

## Step 9: Compile & Verify

- `cd` to `docs/{tier}/{variant_name}/` and compile with `latexmk -xelatex summary-{variant_name}.tex`
- Clean auxiliary files (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`)
- If compilation fails, fix the issues and recompile

---

## Step 10: Fact-Check

Run `/review-summary` on the completed document — report saves to `docs/quality_reports/reviews/{tier}/review-summary-{variant_name}.md`. Read the report and fix issues:

**Empirics:** Fix all numerical discrepancies and recompile until the report is clean.

**Theory:** Fix all CRITICAL and MAJOR issues (proof gaps, missing boundary cases). MINOR issues (notation, clarity) are at your discretion. Recompile and re-run until no CRITICAL or MAJOR issues remain.

---

## Principles

**Why interpret, not just describe.** A table of coefficients or a lemma statement is useless without context. The reader needs to know: is this expected or surprising? What does it mean economically? Every result should be connected to a story about what it means.

**Why write the introduction last.** The introduction promises what the document will deliver. If written first, it either makes vague promises or locks you into a narrative before you understand the results. Writing it last ensures the introduction accurately previews the actual findings.
