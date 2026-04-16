# Review Workflow: Theory

Steps 2–9 for auditing a theory summary's mathematical correctness.

**Mindset:** Treat everything as wrong until you have independently checked it — both the summary AND the source notes it draws from. The most valuable catches are not algebra typos but structural gaps: proofs that claim to handle all cases but actually leave one open.

---

## Step 2: Read the Source Math Formulations

The source material typically lives in `docs/{tier}/{variant_name}/` and follows the structure produced by `/solve-econ-as-math`. Read files in this order:

1. **`question.md`** — The model, question, and verification conditions. This is your reference for what the summary should be proving.
2. **`definitions.md`** and **`assumptions.md`** (if present) — Shared vocabulary and assumptions in force. Check the summary's notation against these.
3. **`findings.md`** — The guided walkthrough, dependency tree, and result index with statuses. This is the primary source of truth for what was proved and what remains open.
4. **`results/` directory** — Individual result files with IF/THEN/BECAUSE/FAILS WHEN structure. Read these for detailed proofs.
5. **Any `reviews/` files** — Past review reports flagging known issues.

If the source material doesn't follow this structure, read all `.md` files and reconstruct the picture yourself.

Build an independent understanding of:
- What is the question?
- What results are established (active) vs. superseded?
- What is the logical dependency tree?
- What are the key mathematical objects and their properties?

**Do NOT read the summary yet.** Form your own view first, then compare. This prevents anchoring.

---

## Step 3: (No separate inventory step — the source notes are the ground truth.)

---

## Step 4: Read the Summary

Read the theory summary end-to-end. For each lemma, theorem, and proof step, note:
- What is claimed (the formal statement)
- What is the proof strategy
- What assumptions are used

---

## Step 5: Verify Each Proof Step

Work **top-down**: start by asking "is the main conclusion even true?" and try to construct counterexamples. If you can't, work backward through the proof steps.

**First pass — challenge the conclusion:**
- Assume the theorem is wrong. What would a counterexample look like?
- Try to construct one. If you can't, that's evidence the theorem is correct — but now you know *where* the proof needs to be airtight.
- If you can construct one, the proof has a gap. Find it.

**Second pass — check each step:**
- Does the conclusion actually follow from the premises?
- Are there implicit assumptions that are not stated?
- Is the proof complete, or does it only handle the "generic" case and miss boundaries?

**Boundary and degenerate cases:**
- What happens at the extremes of parameter ranges?
- Are there edge cases where a strict inequality becomes an equality, breaking the argument?
- Does the proof handle all possible configurations, or only the "obvious" ones?

**Quantifier errors:**
- Does a "for all" claim actually hold for all cases, or only for a subset?
- Does an "exists" claim actually have a valid construction?
- Are uniqueness claims truly ruling out all alternatives, or just the obvious ones? (Common failure mode: a proof rules out the "natural" alternatives but misses an exotic construction.)

---

## Step 6: Check Cross-References

- Does each lemma that cites a prior result actually use it correctly?
- Are the dependency claims accurate (e.g., "By Lemma 3" — does Lemma 3 actually give what's needed)?
- Are there circular dependencies?

---

## Step 7: Verify Consistency with Source Notes

**Treat both the summary AND the source notes as potentially wrong.** The source notes may also contain errors. Your job is to independently verify the math, not to rubber-stamp either document.

- Does the summary accurately represent what was proved in the notes?
- Are any results marked as "superseded" in the notes but presented as active in the summary? (Note: the summary may intentionally correct or update the notes — flag the discrepancy but don't assume the notes are right.)
- Does the summary's logical flow match the dependency tree from the source notes?
- Are there results in the source notes that the summary omits without explanation?
- **Critically: do the source results themselves contain errors?** If you find a bug in a source `.md` result file, report it — this is the most valuable kind of catch.

---

## Step 8: Check Notation and Definitions

- Are all symbols defined before use?
- Is notation consistent throughout (same symbol for the same object)?
- **Notation policy:** the project convention is to use model primitives directly rather than shorthand, unless notation has been explicitly registered. Do NOT flag verbose primitives as a problem. Instead, if you notice a recurring expression that would genuinely benefit from shorthand, **suggest** the notation to the user as a MINOR item — they can approve it and register it as project notation.

---

## Step 9: Assess Scope Claims

- Does the "Discussion" or "What is established" section accurately describe the scope?
- Are the "remaining gaps" genuinely open, or have they been resolved in the source notes?
- Are the assumptions identified as the ones that actually drive the results?

---

## Report Template

```markdown
# Math Review Report: {variant_name}

**Date:** YYYY-MM-DD
**Summary:** docs/{tier}/{variant_name}/summary-{variant_name}.tex
**Status:** CLEAN | ISSUES_FOUND

## Summary
- CRITICAL: [N] (proof gaps that invalidate a claim)
- MAJOR: [N] (missing boundary cases, incomplete arguments)
- MINOR: [N] (notation issues, unclear exposition)

## Critical Issues

1. **[Lemma/Theorem N], [section]:** [description of the gap]. The proof claims [X] but does not rule out [Y]. [Why this matters for the overall argument.]

## Major Issues

1. **[Lemma N], boundary case:** [description]. The proof works for [generic case] but fails when [boundary condition]. [Suggested fix or what needs to be checked.]

## Minor Issues

1. **[Section], line ~N:** [notation inconsistency / unclear step / missing definition]

## Consistency with Source Notes

- [Any discrepancies between summary and source .md files]
- [Any errors found in the source notes themselves]

## Scope Assessment

- [Whether the "what is established vs. open" section is accurate]
```

**Structured output block** (for orchestrator):

```
--- REVIEW RESULT ---
STATUS: CLEAN | ISSUES_FOUND
MODE: THEORY
TARGET: [path to summary]
CRITICAL: [N]
MAJOR: [N]
MINOR: [N]
OVERALL: [1-5]
--- END REVIEW RESULT ---
```

Scoring: 5 = all proofs correct, no issues, 4 = minor notation/clarity issues only, 3 = one major issue (missing boundary case, incomplete argument), 2 = critical gap in a proof, 1 = fundamental logical error.

**Action thresholds:** Score <= 3 means the summary should not be used until issues are fixed. Score <= 2 means the underlying source results may also need re-examination.
