---
name: review-summary
description: >-
  Review a summary document. Two modes: (A) empirics — fact-check numerical
  claims against pipeline outputs; (B) theory — audit mathematical proofs for
  logical gaps, incorrect claims, and missing boundary cases. Use this skill
  whenever the user asks to verify a summary, fact-check a draft, check a proof,
  review math, audit a theory note, or review a summary against data. Also use
  when the orchestrator routes docs/*.tex files for review. Distinct from
  /review-manuscript (qualitative academic review) and /review-details
  (grammar/typos). Do NOT use for writing summaries (use /write-summary).
disable-model-invocation: false
argument-hint: "[summary to review, e.g. 'review the {variant_name} summary']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# Review Summary

Review a summary document with fresh, harsh eyes. Treat every claim as potentially wrong until independently verified — both the summary AND the source materials it draws from.

**Input:** `$ARGUMENTS` — what to review (e.g., "fact-check the {variant_name} summary", "review the proof in {variant_name}", "audit the math in {variant_name}").

---

## Step 1: Locate the Summary and Detect Mode

Find the `.tex` file from `$ARGUMENTS` or context:
- Direct path if provided
- `docs/{tier}/{variant_name}/summary-{variant_name}.tex`
- Glob for matches in `docs/`

If the summary doesn't exist, tell the user and stop.

Determine the mode: if the summary contains `\begin{lemma}`, `\begin{theorem}`, `\begin{proof}`, or proof-style structure → **Theory**. If it contains `\input{`, `\includegraphics`, or references pipeline outputs → **Empirics**. If ambiguous, check whether `output/{tier}/tables/{variant_name}/` exists (Empirics) or only `docs/{tier}/{variant_name}/` notes exist (Theory).

**Empirics:** Read `references/workflow-empirics.md` and follow it.

**Theory:** Read `references/workflow-theory.md` and follow it.

---

## Step 2–9: Mode-Specific Workflow

Follow the workflow file loaded in Step 1. It covers: reading sources, inventorying ground truth, reading the summary, verifying claims, and checking consistency.

---

## Step 10: Produce the Report

The workflow file specifies the report format (empirics: fact-check report; theory: math review report). Generate it according to the template in the workflow.

---

## Step 11: Save

Save the report to `docs/quality_reports/reviews/{tier}/review-summary-{variant_name}.md`. Create the directory if it does not exist. The report replaces the previous one on re-run — no date suffix.

---

## Principles

**Why treat everything as wrong until checked.** Both summaries and source notes can be written by LLMs. LLMs produce plausible-looking text with subtle errors — each step looks correct in isolation but the overall argument has a hole. Treat every claim as a conjecture until independently verified.

**Why read sources before the summary.** If you read the summary first, you'll be anchored to its framing. Reading the sources first lets you form an independent view, then compare. Discrepancies jump out.
