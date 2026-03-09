---
name: write-summary
description: >-
  LaTeX summary document from saved analysis outputs. Use this skill whenever
  the user asks to summarize results, write up findings, draft a summary,
  compile results into a document, or create a report from output tables and
  figures. Covers scanning outputs, reading the code pipeline, interpreting
  results, brainstorming economic explanations, and producing a LaTeX document
  with methodology, results, discussion, and appendices. Do NOT use for
  implementing code (use /write-code) or running new analyses (use /analyze-data).
  This skill is about turning existing outputs into a coherent research document.
disable-model-invocation: true
argument-hint: "[what to summarize, e.g. 'summarize the {variant-name} results']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
---

# Write Summary

Produce a LaTeX summary document from saved output (tables, figures) for one variant.

**Input:** `$ARGUMENTS` — what to summarize (e.g., "summarize the {variant-name} results", "write up the {variant-name} findings", "draft a report for the {variant-name} exploration").

---

## Step 1: Identify Variant & Tier

Determine the tier (core / exploration / archive) and variant-name from context (user instruction, open files, cwd).

Verify outputs exist:
- `output/{tier}/tables/{variant-name}/`
- `output/{tier}/figures/{variant-name}/`

If no outputs are found, tell the user and stop.

---

## Step 2: Read the Code Pipeline

Understanding the methodology is essential for writing the Methodology section and the Appendix.

- List scripts in `code/scripts/{tier}/{variant-name}/` (exploration/archive) or numbered scripts in `code/scripts/{tier}/` (core)
- Read each script: what data it loads, what transformations it applies, what it outputs
- Read relevant src modules in `code/src/mypackage/{tier}/{variant-name}/` for the pure logic
- Note which script produces which output file (for appendix cross-references)
- Extract mathematical operations that should become LaTeX equations

Also check `docs/{tier}/{variant-name}/` for any analysis notes the user may have written.

---

## Step 3: Scan & Read All Outputs

Go through every output file:

**Tables** (`output/{tier}/tables/{variant-name}/`):
- Read `.csv` files to understand the data (column names, values, sample sizes)
- Read `.tex` table files to see formatted results (coefficients, standard errors, significance stars)

**Figures** (`output/{tier}/figures/{variant-name}/`):
- View `.png` files to understand distributions, trends, comparisons

For each output, write a short internal summary of what it shows. This inventory drives the Results section.

---

## Step 4: Identify Connections Across Results

After reading all outputs, look for:
- Results that explain or qualify each other (e.g., a distribution plot that explains a regression coefficient)
- Patterns recurring across multiple tables/figures
- Results that contradict or complicate each other
- A narrative arc: what story do these results tell together?

This cross-result analysis informs the Discussion and the Introduction.

---

## Step 5: Brainstorm Explanations & Conjectures

Read `references/interpretation-guide.md` for reasoning patterns.

Think like an economist:
- Propose 2-4 possible economic explanations for the key findings. What mechanisms could generate these patterns?
- For each conjecture: (a) which results support it, (b) which complicate or contradict it, (c) what additional analysis or data would help distinguish between competing explanations
- Flag which conjectures are well-supported vs speculative
- Consider alternative interpretations: compositional artifact? Selection effect? Mechanical consequence of the methodology?

The goal is to turn the summary from a report ("here's what we found") into a research document ("here's what we found, here's what it might mean, and here's how to tell").

---

## Step 6: Read the Template

Read `references/latex-template.tex` for the document structure and preamble.

---

## Step 7: Write the Summary (body first, introduction last)

The writing order matters because the introduction must reference findings from later sections — it can only be written after everything else is understood.

**Phase A — Methodology (main body, brief):**
- High-level overview: data sources, key methodological choices, estimation strategy
- Key equations from the src/ modules
- Point to the appendix for the detailed pipeline walkthrough

**Phase B — Results (one subsection per logical group):**
For each table or figure:
- Include via `\input{\outdir/tables/{variant-name}/{filename}}` or `\includegraphics[width=0.9\textwidth]{\outdir/figures/{variant-name}/{filename}.png}`
- Write a caption with descriptive text and a `\label{}`
- Write 1-3 paragraphs of interpretive prose: what the numbers mean, what patterns emerge, how they relate to other results
- Cross-reference related tables/figures via `\ref{}`

Where appropriate, create hand-coded summary tables that synthesize across multiple outputs (e.g., collecting key coefficients across specifications into one comparison table).

**Phase C — Discussion:**
- Synthesize cross-result connections from Step 4
- Present the conjectures from Step 5: supporting evidence, complications, what further analysis could resolve each
- Distinguish well-supported explanations from speculative ones
- Central finding and its implications
- Limitations of the current analysis

**Phase D — Conclusion:**
- Main takeaways concisely
- Open questions and promising directions (from unresolved conjectures)

**Phase E — Appendix A: Detailed Methodology:**
- Step-by-step pipeline walkthrough
- For each stage: what it does, key parameters, which script implements it (e.g., "implemented in `03_estimate.py`")
- Equations where code implements mathematical procedures

**Phase F — Appendix B: Additional Results (if applicable):**
- Robustness checks, variant comparisons
- Additional figures across pipeline variants
- Organize by diagnostic type (e.g., all density plots together, all classification plots together)

**Phase G — Introduction (written last):**
- Overview of the approach and key innovations
- Preview key findings (from results already written)
- Frame findings in terms of the conjectures — what they mean, not just what they show
- Set up the narrative arc: the introduction should make promises the body delivers on

---

## Step 8: Assemble & Save

- Compute `\outdir` relative path: from `draft/{tier}/{variant-name}/` to `output/{tier}/` = `../../../output/{tier}`
- Fill in the template preamble, then assemble sections in document order: Introduction, Methodology, Results, Discussion, Conclusion, Appendices
- Create `draft/{tier}/{variant-name}/` directory
- Save to `draft/{tier}/{variant-name}/summary-{variant-name}.tex`

---

## Step 9: Compile & Verify

- Compile with `latexmk -xelatex`
- Clean auxiliary files (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`)
- If compilation fails, fix the issues and recompile

---

## Checklist

- [ ] All output files referenced (no orphaned tables/figures)
- [ ] `\outdir` relative path is correct
- [ ] Every table has caption, label, and interpretive prose
- [ ] Every figure has caption, label, and interpretive prose
- [ ] Cross-references (`\ref{}`) link related results
- [ ] Connections across results are discussed
- [ ] Economic conjectures presented with supporting/contradicting evidence
- [ ] Hand-coded summary tables where needed
- [ ] Main methodology is brief; detailed pipeline in appendix with script references
- [ ] Introduction written last, reflects actual findings and conjectures
- [ ] Document compiles without errors
- [ ] Auxiliary files cleaned up

---

## Principles

**Why interpret, not just describe.** A table of coefficients is useless without context. The reader needs to know: is this coefficient large or small? Expected or surprising? Consistent with or contradictory to other findings? Every number in the document should be connected to a story about what it means.

**Why brainstorm conjectures.** Research advances not by stating facts but by proposing explanations and identifying what would distinguish them. A summary that says "the coefficient on X is zero" is less valuable than one that says "the coefficient on X is zero, which is consistent with explanation A but rules out explanation B, and could be tested further by examining C." The conjectures section is where the document generates its research value.

**Why write the introduction last.** The introduction promises what the document will deliver. If written first, it either makes vague promises or locks you into a narrative before you understand the results. Writing it last ensures the introduction accurately previews the actual findings and frames them in terms of the conjectures that emerged from reading the data.
