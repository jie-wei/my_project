# Workflow: Theory Summary

Steps 2–7 for producing a self-contained proof walkthrough from math formulation notes.

---

## Step 2: Read the Math Formulations

The source material typically lives in `docs/{tier}/{variant_name}/` and follows the structure produced by `/solve-econ-as-math`. Read files in this order:

**1. `question.md`** — The model specification, the question, and verification conditions. This tells you what the summary needs to explain.

**2. `definitions.md`** and **`assumptions.md`** (if present) — The shared vocabulary and assumptions in force. These determine the notation and scope.

**3. `findings.md`** — The central document. Contains the guided proof walkthrough, the logical dependency tree, and the result index with statuses. Start here for the big picture: what was the answer, what are the key steps, what is the proof architecture.

**4. `results/` directory** — Individual result files (one per lemma/theorem), each with IF/THEN/BECAUSE/FAILS WHEN structure. Read these for the detailed proofs and boundary conditions.

**5. Any `reviews/` files** — Past review reports that may flag known issues or superseded results.

From these, extract:
- The logical dependency tree: which results build on which
- The status of each result (active, superseded, open) — check the result index in `findings.md`
- The key definitions, lemmas, theorems, and their proofs
- What is established vs. what remains open

If the source material does not follow this structure (e.g., it's just free-form notes), read all `.md` files and reconstruct the dependency tree yourself.

The summary document should follow the logical flow of the proofs, not the chronological order of discovery. Use the dependency tree to determine the right presentation order.

---

## Step 3: (No separate scan step — the "outputs" are the result files themselves.)

---

## Step 4: Map the Proof Architecture

- Identify which results close gaps vs. open new questions
- What is the main theorem? What are the supporting lemmas?
- What is the logical skeleton: which lemmas feed into which?
- Are there alternative proof paths?

This architecture determines the document structure.

---

## Step 5: Plan the Discussion

Think like a theorist. This planning informs what goes in the Discussion section, not the proofs themselves (all proofs should be detailed regardless).

- Translate mathematical results back to economic language
- Note which steps carry the real insight vs. which are routine
- What are the key mathematical properties that drive the result?

### Interpretation Patterns

**What drives the result:**
- Identify the 1-2 key mathematical properties that make the proof work (e.g., convexity, monotonicity, a cancellation)
- State them explicitly: "The proof relies on [property]. Without it, [what would break]."

**What the result does NOT depend on:**
- List aspects of the model that the proof never touches
- "The argument works for any [object] satisfying [condition] — it never examines [aspect]."
- This is where the reader learns the true scope of the theorem

**Where the intellectual content lives:**
- Routine steps: standard arguments. Acknowledge them but don't dwell in the Discussion.
- Key steps: the moves specific to this problem. These deserve intuition paragraphs and discussion of what would happen if they failed.
- Surprising steps: results that contradict naive intuition. Flag them.

**Connecting results to economics:**
- "Lemma N says [math]. Economically, this means [plain language]."
- When a parameter changes, trace through the proof to see which steps are affected.

**Remaining gaps and open questions:**
- Be precise about what is proved vs. assumed vs. conjectured
- State assumptions clearly: "The argument assumes [X]. Whether this is without loss is [open/proved elsewhere]."
- What happens if the model is generalized? Which proof steps would survive, which would break?
- State conjectures precisely with evidence for/against from the current proof structure

---

## Step 6: Read the Template

Read `references/template-latex-theory.tex` for the proof walkthrough structure. Key patterns:
- Introduction states the question, the answer, and the proof strategy upfront
- Main Result section with formal theorem statement
- Proof section: list ALL steps as a numbered overview first, then each step as a subsection following the pattern: Lemma statement → Proof → Implication
- A "Combining the steps" subsection that restates the skeleton with cross-references
- Discussion: what the argument does NOT use (clarifies generality), remaining gaps
- Optional appendix for alternative proofs or extensions

---

## Step 7: Write the Summary (body first, introduction last)

The document is a self-contained proof walkthrough. Use a standalone article class with theorem environments. Do not use the empirics template.

**Phase A — Overview:**
- State the question precisely
- State the answer (theorem/result)
- Roadmap of the document sections

**Phase B — Setup:**
- Model primitives and notation
- Key definitions (feasible set, equilibrium concept, etc.)
- Prior results assumed (with references to where they are proved)

**Phase C — Proof (one section, with subsections per step):**
- Start with a numbered overview listing ALL proof steps (one sentence each) — this gives the reader the full architecture before diving in
- Then one subsection per step, following the pattern: Lemma statement → Proof → Implication (what this step buys us for the overall argument)
- **Proofs should be detailed and crystal clear.** Every step should be expanded enough that a reader with fresh eyes can follow without filling in gaps. Do not compress proofs for brevity — clarity is the priority. If a step takes half a page, that's fine.
- End with a "Combining the steps" subsection that restates the proof skeleton with cross-references
- Use intuition paragraphs after proofs to explain the economic content
- Cross-reference related results via `\ref{}`
- **Notation:** use model primitives directly in equations rather than introducing shorthand notation. If you notice a recurring expression that would benefit from shorthand, suggest it to the user — they can approve it and register it as project notation. Do not introduce shorthand on your own.

**Phase D — Discussion:**
- What the argument does NOT use (clarifies generality): identify the 1-2 key mathematical properties that drive the result and what would break without them
- What the argument does NOT depend on: aspects of the model the proof never touches
- Remaining gaps: what is assumed but not proved
- Which steps are routine vs. where the real intellectual content lives

**Phase E — Introduction (written last):**
- Question, answer, and proof strategy in miniature
- Preview the key steps and where the intellectual content lives

### Assemble

- No `\outdir` needed (no external figures/tables to reference)
- Assemble sections in document order: Introduction, Main Result, Proof (with subsections per step), Discussion, optional Appendix

### Checklist

- [ ] Question and answer stated upfront in Introduction
- [ ] All proof steps listed as numbered overview before details
- [ ] Each step follows Lemma → Proof → Implication pattern
- [ ] Every proof is detailed and crystal clear — no gaps for the reader to fill
- [ ] Cross-references (`\ref{}`) link related lemmas/theorems
- [ ] Intuition paragraphs explain economic content after proofs
- [ ] Model primitives used directly; no shorthand introduced without user approval
- [ ] "Combining the steps" subsection restates the skeleton with cross-references
- [ ] Discussion: what drives the result, what it does NOT use, remaining gaps
- [ ] Introduction written last, reflects actual findings
- [ ] Document compiles without errors
- [ ] Auxiliary files cleaned up
- [ ] `/review-summary` Mode B passes with no CRITICAL or MAJOR issues
