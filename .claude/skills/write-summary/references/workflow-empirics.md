# Workflow: Empirics Summary

Steps 2–7 for producing a LaTeX summary from pipeline outputs (tables, figures).

---

## Step 2: Read the Code Pipeline

Understanding the methodology is essential for writing the Methodology section and the Appendix.

- List scripts in `code/scripts/{tier}/{variant_name}/` (exploration/archive) or numbered scripts in `code/scripts/{tier}/` (core)
- Read each script: what data it loads, what transformations it applies, what it outputs
- Read relevant src modules in `code/src/mypackage/{tier}/{variant_name}/` for the pure logic
- Note which script produces which output file (for appendix cross-references)
- Extract mathematical operations that should become LaTeX equations

Also check `docs/{tier}/{variant_name}/` for any analysis notes the user may have written.

---

## Step 3: Scan & Read All Outputs

Go through every output file:

**Tables** (`output/{tier}/tables/{variant_name}/`):
- Read `.csv` files to understand the data (column names, values, sample sizes)
- Read `.tex` table files to see formatted results (coefficients, standard errors, significance stars)

**Figures** (`output/{tier}/figures/{variant_name}/`):
- View `.png` files to understand distributions, trends, comparisons

For each output, write a short internal summary of what it shows. This inventory drives the Results section.

---

## Step 4: Identify Connections Across Results

After reading all outputs, look for:
- Results that explain or qualify each other
- Patterns recurring across multiple tables/figures
- Results that contradict or complicate each other
- A narrative arc: what story do these results tell together?

This cross-result analysis informs the Discussion and the Introduction.

---

## Step 5: Brainstorm Explanations & Conjectures

Think like an empirical economist:
- Propose 2-4 possible economic explanations for the key findings. What mechanisms could generate these patterns?
- For each conjecture: (a) which results support it, (b) which complicate or contradict it, (c) what additional analysis or data would help distinguish between competing explanations
- Flag which conjectures are well-supported vs speculative
- Consider alternative interpretations: compositional artifact? Selection effect? Mechanical consequence of the methodology?

### Interpretation Patterns

**From coefficient to mechanism:**
- "The positive coefficient on X suggests that [mechanism], possibly because [channel]."
- Generate 2-3 candidate explanations for each key finding
- Prefer mechanisms that are specific and falsifiable over vague ones

**Testing conjectures against data:**
- "If [mechanism A] drives this result, we would expect [prediction]. Table N [confirms/contradicts] this."
- Does a pattern in one table explain an anomaly in another?
- Do robustness checks strengthen or weaken the main finding?

**Distinguishing competing explanations:**
- "This pattern is consistent with both [A] and [B]. To distinguish them, one would examine [variable/subgroup]."
- Which explanation is most parsimonious? Consistent with the broadest set of results?

**Identifying artifacts vs. real effects:**
- Could the result reflect changes in sample composition rather than behavior?
- Is the result a tautological consequence of how variables are defined?
- Would a different estimation approach produce the same result?

**Framing null results:**
- A null result is information: "The absence of effect on [X], combined with the strong effect on [Y], suggests the mechanism operates through [channel Y]."
- Distinguish precise zeros (tight CI) from underpowered tests (wide CI)

**Synthesizing across results:**
- What is the central finding when all results are considered together?
- Clearly distinguish: well-established findings vs. suggestive patterns vs. speculative conjectures
- Use language that matches evidence strength: "demonstrates" vs. "suggests" vs. "raises the possibility"

The goal is to turn the summary from a report ("here's what we found") into a research document ("here's what we found, here's what it might mean, and here's how to tell").

---

## Step 6: Read the Template

Read `references/template-latex-empirics.tex` for the document structure and preamble.

---

## Step 7: Write the Summary (body first, introduction last)

The writing order matters because the introduction must reference findings from later sections.

**Phase A — Methodology (main body, brief):**
- High-level overview: data sources, key methodological choices, estimation strategy
- Key equations from the src/ modules
- Point to the appendix for the detailed pipeline walkthrough

**Phase B — Results (one subsection per logical group):**
For each table or figure:
- Include via `\input{\outdir/tables/{variant_name}/{filename}}` or `\includegraphics[width=0.9\textwidth]{\outdir/figures/{variant_name}/{filename}.png}`
- Write a caption with descriptive text and a `\label{}`
- Write 1-3 paragraphs of interpretive prose: what the numbers mean, what patterns emerge, how they relate to other results
- Cross-reference related tables/figures via `\ref{}`

Where appropriate, create hand-coded summary tables that synthesize across multiple outputs.

**Phase C — Discussion:**
- Synthesize cross-result connections from Step 4
- Present the conjectures from Step 5: supporting evidence, complications, what further analysis could resolve each
- Distinguish well-supported explanations from speculative ones
- Central finding and its implications
- Limitations of the current analysis

**Phase D — Conclusion:**
- Main takeaways concisely
- Open questions and promising directions

**Phase E — Appendix A: Detailed Methodology:**
- Step-by-step pipeline walkthrough
- For each stage: what it does, key parameters, which script implements it
- Equations where code implements mathematical procedures

**Phase F — Appendix B: Additional Results (if applicable):**
- Robustness checks, variant comparisons
- Additional figures across pipeline variants

**Phase G — Introduction (written last):**
- Overview of the approach and key innovations
- Preview key findings (from results already written)
- Frame findings in terms of the conjectures — what they mean, not just what they show
- Set up the narrative arc: the introduction should make promises the body delivers on

### Assemble

- Compute `\outdir` relative path: from `docs/{tier}/{variant_name}/` to `output/{tier}/` = `../../../output/{tier}`
- Fill in the template preamble, then assemble sections in document order: Introduction, Methodology, Results, Discussion, Conclusion, Appendices

### Checklist

- [ ] All output files referenced (no orphaned tables/figures)
- [ ] `\outdir` relative path is correct
- [ ] Every table has caption, label, and interpretive prose
- [ ] Every figure has caption, label, and interpretive prose
- [ ] Cross-references (`\ref{}`) link related results
- [ ] Connections across results are discussed
- [ ] Economic conjectures presented with supporting/contradicting evidence
- [ ] Hand-coded summary tables where needed
- [ ] Main methodology is brief; detailed pipeline in appendix with script references
- [ ] Introduction written last, reflects actual findings
- [ ] Document compiles without errors
- [ ] Auxiliary files cleaned up
- [ ] `/review-summary` passes (all numbers verified, no missing figures)
