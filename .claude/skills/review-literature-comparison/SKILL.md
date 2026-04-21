---
name: review-literature-comparison
description: Literature review that compares existing work against our paper's thesis. Use when the user asks to survey literature relative to our idea, find related work, check novelty of results, position our paper, or says "compare with literature", "how does our paper relate to X", "what's the related literature on X". Also triggers when the user wants to compare their paper's results against existing work. Has a "deepen" mode (triggers on "deepen", "enrich entries") and a "merge" mode (triggers on "merge", "add new papers"). This is the COMPARISON skill — it reads the literature through the lens of our paper's thesis. For a neutral, thesis-free understanding of what the literature contains, use /review-literature-comparison-synoptic instead.
disable-model-invocation: true
argument-hint: "[topic, paper title, or research question]"
---

# Literature Review

Conduct a structured literature search and synthesis on the given topic.

**Input:** `$ARGUMENTS` — a topic, paper title, research question, or phenomenon to investigate. If `$ARGUMENTS` is `deepen`, run the Deepen workflow instead (see below).

---

## Mode Detection

Parse `$ARGUMENTS`:
- **`deepen`** → run the Deepen workflow (enriches existing `[UNSUMMARIZED]` entries using `/read-paper` summaries)
- **`merge`** → run the Merge workflow (integrates newly summarized papers into an existing literature review)
- **Anything else** → standard literature review (Steps 1-7 below)

---

## Steps (Standard Review)

1. **Parse the topic** from `$ARGUMENTS`. If a specific paper is named, use it as the anchor.

2. **Establish the comparison target.** The review should position literature findings against *our* work. What counts as "our work" depends on the project stage:
   - If the conversation already makes the target clear (e.g., the user just discussed a result, or pointed to a file), use that context directly — no need to ask.
   - If `paper/main.tex` (or `paper/main.pdf`) exists and hasn't been read this session, read it as the default anchor. `main.tex` holds only the preamble and `\subfile{...}` chain — the actual prose lives in `paper/sections/*.tex` (especially the introduction and related-literature sections) and `paper/appendices/*.tex`, so read those files, not just `main.tex`.
   - If no draft exists yet, check `docs/core/` and `docs/exploration/` for analysis notes that capture the project's current thinking.
   - If none of the above applies — or if the topic is narrow enough that the general draft isn't the right comparator — ask the user what to compare against before proceeding.

3. **Search for related work** using available tools:
   - Check `docs/literature/` for existing literature review files
   - Check `docs/core/` and `docs/exploration/` for existing analysis notes
   - Check `paper/references.bib` for papers already in the project
   - Use `WebSearch` to find recent publications
   - Use `WebFetch` to access working paper repositories and abstracts

4. **Organize findings** using the template structure (see Output Format). The key organizational principle: group papers by their *role in the paper's argument*, not by topic or chronology. Distinguish between:
   - **Literature through the lens** — existing work reread through the paper's framework (organized by dimensions/themes that serve the argument)
   - **Closest predecessors** — the 3-6 papers most similar to ours, with detailed positioning (what they do, what they miss)
   - **Formal tools** — methodology papers the paper draws on (not direct predecessors but essential building blocks)

5. **Identify gaps and opportunities:**
   - What questions remain unanswered?
   - What remains open even after our paper?
   - Do NOT mix paper-planning material (specific contributions, theorems to prove) into the gaps section — that belongs in a separate plan document.

6. **Extract citations** in BibTeX format for all papers discussed.

7. **Save the report** — see Output Location below.

### Parallelization Guidance (Standard Review)

For a literature with 30+ papers, building the comparison review in a single pass may exceed context. The work has a natural dependency structure — some parts can run in parallel, others must wait. Think in terms of *information independence*, not section numbers.

**Step 1 — Sequential: Establish comparison target.** Read our paper's thesis. This must happen first — every subsequent step needs it.

**Step 2 — Parallel: Per-paper extraction.** Spawn one agent per paper (or per batch of 5-10 papers). Each agent reads one `summary-*.md` file and extracts: model, main contribution, key finding, and *connection to our thesis*. These are independent once the thesis is known. Each agent writes its output to a temp file.

**Step 3 — Sequential: Assembly.** The main agent reads all extraction outputs and assembles: group papers by dimension (organized around our claims), identify closest predecessors, assign papers to themes. This requires seeing all papers together — it cannot be parallelized.

**Step 4 — Parallel: Write dimension/theme sections.** Once themes are identified and papers assigned, spawn one agent per dimension. Each agent gets: (a) the theme definition and our claim, (b) the papers assigned to it with their extracted connections, (c) our thesis for reference. Each dimension section is independent. Separately, spawn an agent for Section 5 (closest predecessors) — it needs the predecessor papers + our thesis but not the dimension sections.

**Step 5 — Sequential: Final assembly.** The main agent merges all sections and writes: thesis, framework, scope, assessment summary table, formal tools, gaps, and key papers index. These require the full picture.

**Summary:** sequential → parallel → sequential → parallel → sequential. If using cloud sync (Dropbox), all agents should write to temp files; the main agent merges at the end.

---

## Output Format

Read the bundled template at `templates/template-summary-literature.md` (relative to this skill's directory) as the starting structure. The template has 8 sections:

1. **Thesis** — one paragraph stating the paper's central claim
2. **Framework** — the conceptual ideas that organize the reading (stated ONCE, not repeated later)
3. **Scope** — where the thesis applies and where it doesn't
4. **Literature through the lens** — existing work organized by dimensions/themes that serve the argument. Each dimension has: definition, key papers (1-2 lines each), and a "reading through our lens" paragraph
5. **Closest predecessors** — detailed positioning against 3-6 closest papers (what they do, what they miss). Includes an assessment summary table
6. **Formal tools** — methodology papers (2-3 lines each)
7. **Gaps and research opportunities** — pure research questions (no paper-planning)
8. **Key papers index** — dimension-organized reference list with summary links

**Why this structure matters.** A flat list of papers ordered by relevance breaks down beyond ~15 papers. The 8-section structure separates three things that are easy to conflate: (a) what the literature says (sections 4-5), (b) how we position against it (section 5), and (c) what tools we draw on (section 6). It also prevents a common failure mode: mixing paper-planning material (contributions, theorems to prove) into the literature review. Research agenda belongs in a separate plan document, not here.

**Citation format.** When referring to any paper, always include the journal abbreviation: **Author (Year, Journal)**. Examples: Stigler (1964, JPE), Bergemann & Morris (2019, JEL), Athey, Bagwell & Sanchirico (2004, REStud). Standard abbreviations: AER, Ecma, JPE, QJE, REStud, RAND, JIE, TE, JET, AEJ:Micro, MS. For working papers, use "WP" instead of a journal. This lets the reader immediately gauge a paper's venue without clicking through.

**Key paper entry format** (used in sections 4 and 8). Always use bullet points and sub-bullets when describing specific papers — a dense paragraph mixing multiple ideas is hard to scan. Each sub-bullet should make one claim or state one fact. Sub-bullet titles are bold:
```
- **Author (Year, Journal)** — [Summary](summary-year-author.md)
    - **Model:** [setting — e.g., "repeated Bertrand duopoly with differentiated products"]
    - **Main contribution:** [what the paper does]
    - **Key finding:** [specific result, with theorem/proposition number]
    - **Connection to thesis:** [how it relates to our argument]
```

**Closest predecessor format** (used in section 5):
```
### Author (Year, Journal) — Short Title
[~10-15 lines. What they do. What they miss. Why the comparison matters.]
```

**Summary links are mandatory.** Every paper entry — in Section 4, Section 5, Section 6, and Section 8 — must include a `[Summary](summary-year-author.md)` link if a corresponding summary file exists in `docs/literature/`. Before writing entries, scan `docs/literature/summary-*.md` to build a list of available summaries. The link goes right after the author-year-journal citation: `**Author (Year, Journal)** — [Summary](summary-year-author.md)`. Papers without a summary file get no link (and keep the `[UNSUMMARIZED]` tag). The reason: clicking through to the full summary is one of the most common reader actions — a missing link forces them to hunt for the file manually.

**Anti-patterns to avoid:**
- Do NOT repeat the framework/thesis in every dimension's "reading through our lens" paragraph — apply it, don't restate it
- Do NOT mix per-paper detailed entries into the dimensions section — keep dimensions concise (1-2 lines per paper), save detail for section 5 (predecessors) or individual summary files
- Do NOT include paper-planning material (contributions, specific research questions, "extremal information structures to discover") — that belongs in `docs/quality_reports/plans/`
- Do NOT omit summary links on paper entries when the summary file exists — every entry must link to its summary

### Tags

Every paper entry starts with **two tags** by default:

- **`[UNSUMMARIZED]`** — the literature review entry has not been enriched with a deep reading. Removed only by `/review-literature-comparison deepen` after it reads the corresponding `summary-*.md` file produced by `/read-paper` and updates the entry.
- **`[UNVERIFIED]`** — citation details come from LLM memory, not a verified source. Remove only after confirming via WebSearch/WebFetch (verified URL, correct journal/volume/pages) or if the entry already exists in `paper/references.bib`.

**Tag lifecycle for `[UNSUMMARIZED]`:**
1. `/review-literature-comparison` adds the tag when creating the entry
2. User downloads the PDF and runs `/read-paper` → produces a `summary-*.md` file (tag stays)
3. User runs `/review-literature-comparison deepen` → reads the summary, enriches the entry, replaces `[UNSUMMARIZED]` with a clickable link to the summary file

Papers already in `paper/references.bib` can drop `[UNVERIFIED]`. Papers with a verified URL from WebSearch can drop `[UNVERIFIED]`. Neither tag should be removed just because the information *seems* correct.

### Thematic Organization

Themes must be organized around **our paper's claims**, not around the existing literature's categories. Each theme corresponds to one of our paper's main claims or contributions. For each theme, the question is: "who else said this, and what did they miss?" This ensures the literature review serves the paper's argument rather than just cataloging related work.

**How to construct themes:**
1. Identify the paper's 3-5 core claims (from the comparison target — our draft, analysis notes, or conversation context)
2. For each claim, create a theme: "Claim: [our claim in one sentence]"
3. Under each theme, assess which existing papers come closest, what each does, and what it misses relative to our specific claim
4. End each theme with a clear statement of the gap our paper fills

**Within each theme:** discuss how existing papers relate to each other *and* to our specific claim. The value is in the assessment — "who came closest and what's missing" — not in listing papers by topic. Include a theme for empirical evidence if relevant.

### Gaps and Opportunities, Suggested Next Steps, BibTeX Entries

See template for structure.

---

## Deepen Workflow

When the user says `deepen`, "enrich the lit review", "update entries with summaries", or similar — this mode upgrades literature review entries using the deep summaries produced by `/read-paper`.

The idea: initial entries are written from abstracts and LLM memory (shallow). After `/read-paper` produces a `summary-*.md` file, you can go back and enrich the entry with real understanding — better descriptions, more accurate "Relevance to our paper" assessments, and updated thematic synthesis.

### Steps

1. **Find literature review files** — scan for entries with `[UNSUMMARIZED]` tags in:
   - `docs/literature/summary-literature-comparison*.md`
   - `docs/literature/review-literature-comparison*.md` (legacy naming)
   - `docs/core/lit_review_*.md`
   - `docs/exploration/**/lit_review_*.md`

2. **Find matching summary files** — for each `[UNSUMMARIZED]` entry, search for a corresponding `summary-{year}-{author}.md` file (match by author name and year). Check these locations:
   - The directory where the paper's PDF lives (most common — `/read-paper` places summaries alongside PDFs)
   - `docs/literature/` and its subdirectories
   - The project root's `paper/` directory

3. **Report what's available** — show the user which `[UNSUMMARIZED]` entries have summary files ready, and which don't (those need `/read-paper` first). Let the user confirm which entries to deepen, or proceed with all that have summaries.

4. **For each entry with a summary file:**
   a. Read the `summary-*.md` file — focus on the story summary, narrative tree, and core assessment.
   b. Re-read the comparison target (Step 2 of the standard review) if not already in context.
   c. **Update the entry:**
      - Rewrite **Main contribution** and **Key finding** based on actual paper content, not abstract-level guesses.
      - Rewrite **Relevance to our paper** with specific, grounded comparisons — now that you've read the actual arguments, you can say precisely how they relate.
      - Add a **Summary** field with a link to the summary file: `**Summary:** [Full summary](relative/path/to/summary-year-author.md)`
   d. **Remove `[UNSUMMARIZED]`** from the entry heading.

5. **Update thematic sections** — with deeper understanding of several papers, the thematic groupings and synthesis paragraphs may need revision. Re-read the themes and update if the deep readings reveal connections or tensions the shallow pass missed.

6. **Update gaps and next steps** — deep readings often reveal new gaps or close ones that seemed open from the abstract.

### Entry format after deepening

```markdown
### [Author (Year)](URL) — Short Title `[UNVERIFIED]`

- **Summary:** [Full summary](relative/path/to/summary-year-author.md)
- **Publication:** *Journal Name*, vol. X(Y), pp. Z
- **Main contribution:**
  - [Updated point 1 — grounded in actual paper content]
  - [Updated point 2 — with specific theorem/proposition numbers]
- **Method:** [Updated if needed]
- **Key finding:**
  - [Updated finding 1 — specific, with result numbers]
  - [Updated finding 2 — if applicable]
- **Relevance to our paper:**
  - [Updated connection 1 — names our specific results]
  - [Updated connection 2 — precise comparison grounded in both papers]
```

Note: `[UNSUMMARIZED]` is gone, replaced by the clickable Summary link. `[UNVERIFIED]` stays until citation details are independently confirmed.

---

## Merge Workflow

When the user says `merge`, "add new papers", "integrate these into the review", or similar — this mode integrates newly read papers into an existing literature review. Unlike `deepen` (which enriches *existing* entries), merge handles papers that are *not yet in the review at all*.

### Why this is different from `deepen`

`Deepen` assumes the entry already exists with `[UNSUMMARIZED]` tags. `Merge` handles a harder problem: new papers need to be *placed* in the right sections, may require *new subsections*, and trigger *cascading updates* across multiple sections. The failure modes are: (a) putting a paper in the wrong dimension, (b) forgetting to update the index, (c) adding a paper to section 4 but not section 8, (d) needing a new subsection but not creating one.

### Steps

1. **Identify new papers.** Find summary files in `docs/literature/` that are *not* referenced anywhere in the literature review file. Compare the set of `summary-*.md` files against all summary links in the review.

2. **Triage each paper.** For each new paper, read its summary (Story Summary + Core Assessment) and classify it:
   - **Dimension paper** → goes in section 4 (which subsection?) and section 8 (mirror)
   - **Formal tool** → goes in section 6 and section 8's "Formal Tools" subsection
   - **Closest predecessor** → goes in section 5 (detailed positioning)
   - **Needs a new subsection** → if the paper doesn't fit any existing dimension, consider creating a new 4.N subsection. Ask the user before creating new subsections.

3. **Plan the merge.** Before editing, produce a merge plan listing:
   - Which section(s) each paper will be added to
   - Whether any new subsections are needed
   - Whether any "reading through our lens" paragraphs need updating
   - Whether the assessment table (section 5) needs a new row

   Present the plan to the user for approval.

4. **Execute the merge.** For each paper, update ALL relevant sections:

   **Checklist per paper:**
   - [ ] Section 4: add entry to the appropriate dimension (with Model, Main contribution, Key finding, Connection to thesis sub-bullets)
   - [ ] Section 4: update "reading through our lens" paragraph if the new paper changes the synthesis
   - [ ] Section 5: add positioning paragraph if this is a close predecessor
   - [ ] Section 5: update assessment table if the paper relates to one of our claims
   - [ ] Section 6: add entry if this is a formal tool
   - [ ] Section 8: add to the matching subsection (must mirror section 4 structure)

   **Parallelization guidance.** Think in terms of information independence:

   **Step A — Parallel: Per-paper triage.** Spawn one agent per new paper (or per batch). Each agent reads the paper's summary + our thesis and classifies it: which dimension? closest predecessor? formal tool? Each writes its classification to a temp file.

   **Step B — Sequential: Merge plan.** The main agent reads all classifications, builds the merge plan (which papers go where), and presents it to the user.

   **Step C — Parallel: Per-dimension edits.** Spawn one agent per dimension that has new papers. Each agent edits only its dimension in Section 4 + the matching subsection in Section 8. Separately, spawn an agent for Section 5 if new predecessors were identified. Each agent writes to a temp file.

   **Step D — Sequential: Final merge + consistency check.** The main agent merges all edits into the file and runs the consistency checklist.

   **Step E — Sequential: Revisit Sections 1-3.** After merging new papers, re-read Sections 1 (Thesis), 2 (Framework), and 3 (Scope). These are high-level summaries that can only be written well after understanding the full literature. New papers may shift the framing, broaden the scope, or refine the thesis. Update as needed.

   If using cloud sync (Dropbox), all agents write to temp files; the main agent merges at the end. Provide each agent with: (a) the summary file(s) for its papers, (b) the merge plan, (c) our thesis.

5. **Verify consistency.** After all edits, run through this checklist. These checks catch the most common failure mode — sections drifting out of sync after incremental additions:
   - Every subsection in section 8 should correspond to a subsection in section 4 (same names, same numbering). If you added a new 4.N, section 8 must have a matching subsection.
   - Every paper in section 4 should appear in section 8, and vice versa
   - No `[UNSUMMARIZED]` tags should remain on papers that have summary files
   - New "reading through our lens" paragraphs exist for any new subsections
   - The overarching perspective table (if present) includes any new dimensions
   - The assessment summary table in section 5 is updated if new papers are closer predecessors than existing ones

### When to create new subsections

Create a new subsection (4.N) when:
- 2+ new papers share a theme not covered by existing subsections
- A single paper introduces a fundamentally new dimension (not just a variant of an existing one)
- The user explicitly requests it

Label cross-cutting subsections explicitly (e.g., "4.6 Competitive Information Provision (Cross-Cutting)") to distinguish them from the core dimensions.

---

## Output Location

All literature reviews go in `docs/literature/`:

| Type | Filename | When |
|------|----------|------|
| Overall comparison review | `summary-literature-comparison.md` | Comprehensive comparison of related work against our paper |
| Topic-specific comparison | `summary-literature-comparison-[short-description].md` | Focused comparison on a specific question or result |

Examples of topic-specific naming:
- `summary-literature-comparison-search-technology-collusion.md`
- `summary-literature-comparison-optimal-punishments.md`

If `docs/literature/` doesn't exist, create it.

If the project has `paper/references.bib`, offer to append new BibTeX entries there. Note: `references.bib` is a protected file — the user must confirm before editing.

---

## Important

- **Use 4-space indentation for nested lists.** Pandoc (used by `/convert-md-to-pdf`) requires 4-space indentation per nesting level — 2-space nesting gets flattened into a single paragraph. Also add a blank line between a bold header (like `**Buyers**`) and the list that follows it, so pandoc treats them as separate blocks.
- **Write math for PDF compatibility.** The literature review markdown will likely be converted to PDF via pandoc + XeLaTeX. Three rules prevent rendering failures:
  - **Multi-symbol expressions must be explicit `$...$` math.** Write `$\mu \to 1$`, not `(μ→1)`. The preprocessor handles isolated Unicode symbols (a standalone `β` or `→`) but breaks on expressions that mix Unicode with text and parentheses.
  - **Subscripts longer than one character need braces.** Write `$N_{eff}$`, not `N_eff`. Without braces, LaTeX subscripts only the first character (`N_e` + `ff`).
  - **Isolated Unicode symbols are fine.** A standalone `β` or `δ` in prose will be auto-converted. But if in doubt, use `$\beta$` explicitly — it always works.
- **Use bullet points and sub-bullets whenever you are listing multiple distinct facts about a single subject** — whether that subject is a paper, a dimension, or a research gap. Each bullet should make one claim or state one fact. This applies to paper descriptions in the dimensions section, formal tools entries, gap discussions, and the key papers index. Reserve prose paragraphs for (a) narrative content (thesis, framework, scope), (b) argumentative positioning (closest predecessors — "here's why this paper differs from ours"), and (c) synthesis paragraphs ("reading through our lens"). The reason: bullet-point structure makes factual content scannable, while positioning arguments read better as connected prose.
- **All papers get `[UNSUMMARIZED]` and `[UNVERIFIED]` tags by default.** `[UNSUMMARIZED]` is removed only by the `deepen` workflow after reading the summary file and enriching the entry. `[UNVERIFIED]` is removed after citation verification. Neither tag is removed by judgment alone.
- **Do NOT fabricate citations.** If you are unsure about a paper's details (authors, year, journal, title), flag it for the user to verify. Getting a citation wrong is worse than omitting it.
- **BibTeX fields from memory are unreliable.** Even when a paper is real, LLM-recalled volume, pages, and DOI are often wrong. Mark individual fields you cannot verify with `% UNVERIFIED` comments in the BibTeX entry.
- **Compare against our paper.** The "Relevance to our paper" field in each entry should be specific: name which of our results the paper relates to, whether it's a predecessor, competitor, complement, or something we extend.
- **Prioritize recent work** (last 5-10 years) unless seminal papers are older.
- **Note working papers vs published papers** — working papers may change before publication.
- **Handle web tool failures gracefully.** If WebSearch or WebFetch are unavailable or fail, analyze only local files and note what could not be searched.
- **Verify URLs.** Use WebSearch to find real, clickable URLs for each paper. Prefer stable links: journal publisher pages, EconPapers/IDEAS/RePEC, SSRN, NBER. Never guess URLs.
