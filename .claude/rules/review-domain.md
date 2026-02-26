---
paths:
  - "paper/**/*.tex"
---

# Domain Review Agent

**Orchestrator Step 3 (REVIEW)** — Referee-quality content review across 6 dimensions with scoring and objections.

This rule activates during the orchestrator's REVIEW step when the task involves LaTeX manuscript files. It follows the `/review-paper` skill protocol to produce a structured assessment of the manuscript's content, methodology, and argumentation.

---

## When This Rule Activates

- After Step 2 (VERIFY) passes for LaTeX files
- During Step 3 (REVIEW) of the orchestrator loop, **after** `proofread-manuscript.md`
- Runs on the full manuscript (not individual files) to assess coherence across sections

---

## Protocol

Follow the `/review-paper` skill protocol (see `.claude/skills/review-paper/SKILL.md`).

### 1. Read the Full Manuscript

- Read all `.tex` files in `paper/` to understand the complete document
- For long PDFs, read in chunks (5 pages at a time)

### 2. Evaluate Across 6 Dimensions

#### Dimension 1: Argument Structure
- Is the research question clearly stated?
- Does the introduction motivate the question effectively?
- Is the logical flow sound (question -> method -> results -> conclusion)?
- Are conclusions supported by evidence?
- Are limitations acknowledged?

#### Dimension 2: Research Design & Validity
- Are claims supported by the design?
- Are key assumptions stated explicitly?
- What threats to validity exist?
- Are robustness checks adequate?

#### Dimension 3: Methodology / Analytical Approach
- Are methods appropriate for the research question?
- Are statistical or computational choices justified?
- Are results robust to alternative specifications?
- Are results substantively meaningful?

#### Dimension 4: Literature Positioning
- Are key papers cited?
- Is prior work characterized accurately?
- Is the contribution clearly differentiated?
- Any missing citations a referee would flag?

#### Dimension 5: Writing Quality
- Clarity and concision
- Academic tone
- Consistent notation
- Abstract summarizes effectively
- Tables and figures are self-contained

#### Dimension 6: Presentation
- Are tables and figures well-designed?
- Is notation consistent throughout?
- Typos, grammatical errors, formatting issues?
- Is the paper the right length for the contribution?

### 3. Generate Referee Objections

Produce 3-5 tough questions a top referee would ask:
- Why this could be a fatal flaw
- How to address it (suggested response or additional analysis)

### 4. Score Each Dimension

Use 1-5 scale:
- 5 = Excellent (no significant issues)
- 4 = Good (minor issues only)
- 3 = Acceptable (some concerns but addressable)
- 2 = Weak (major concerns)
- 1 = Unacceptable (fundamental flaws)

### 5. Determine Recommendation

Based on dimensional scores:
- **STRONG_ACCEPT:** All dimensions >= 4, overall >= 4.5
- **ACCEPT:** Most dimensions >= 3, no dimension = 1, overall >= 3.5
- **REVISE_AND_RESUBMIT:** Some dimensions = 2, addressable concerns
- **REJECT:** Any dimension = 1, or fundamental unaddressable flaws

### 6. Report Results

Emit the structured output block, then provide the full narrative review.

---

## Structured Output

Reuse the review-paper skill's output format directly (already agent-consumable):

```
--- REVIEW RESULT ---
STATUS: REVIEWED
RECOMMENDATION: STRONG_ACCEPT | ACCEPT | REVISE_AND_RESUBMIT | REJECT
TARGET: [file path]

DIMENSION_SCORES:
- ARGUMENT_STRUCTURE: [1-5]
- RESEARCH_DESIGN: [1-5]
- METHODOLOGY: [1-5]
- LITERATURE: [1-5]
- WRITING: [1-5]
- PRESENTATION: [1-5]
- OVERALL: [1-5]

MAJOR_CONCERNS: [N]
MINOR_CONCERNS: [N]
REFEREE_OBJECTIONS: [N]
--- END REVIEW RESULT ---
```

---

## Integration

- **Orchestrator step:** 3 (REVIEW) — runs SECOND, after `proofread-manuscript.md`
- **Skill protocol:** `review-paper/SKILL.md` (canonical 6-dimension framework)
- **Output feeds:** Step 4 (FIX) — major concerns become fix targets; referee objections inform revisions
- **Sequencing:** Proofreading (previous) catches surface issues; this review catches content and argumentation issues

---

## Important

- **Be constructive.** Every criticism should come with a suggestion for improvement.
- **Be specific.** Reference exact sections, equations, tables, page numbers.
- **Think like a referee at a top journal.** What would make them reject?
- **Distinguish fatal flaws from minor issues.** Not everything is equally important.
- **Acknowledge what's done well.** Good research deserves recognition.
- **Do NOT fabricate details.** If you can't read a section clearly, say so.
- **Handle empty stubs gracefully.** If the manuscript is empty, report "Manuscript is empty — nothing to review" with RECOMMENDATION: N/A.
- **Do not duplicate proofreading.** Surface issues (grammar, typos) are covered by `proofread-manuscript.md`. Focus on content, methodology, and argumentation.
