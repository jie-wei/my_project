---
name: review-manuscript
description: Referee-quality manuscript review across 6 dimensions with structured scoring
disable-model-invocation: true
argument-hint: "[paper filename in paper/ or path to .tex/.pdf]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Manuscript Review

Produce a thorough, constructive review of an academic manuscript — the kind of report a top-journal referee would write.

**Input:** `$ARGUMENTS` — path to a paper (`.tex` or `.pdf`), or a filename in `paper/`.

---

## Steps

1. **Locate and read the manuscript.** Check:
   - Direct path from `$ARGUMENTS`
   - `paper/$ARGUMENTS` (with or without extension)
   - Glob for partial matches in `paper/`

2. **Read the full paper** end-to-end. For long PDFs, read in chunks (5 pages at a time).

3. **Evaluate across 6 dimensions** (see below).

4. **Generate 3-5 "referee objections"** — the tough questions a top referee would ask.

5. **Produce the review report** using the structured output format.

6. **Save the report** — see Output Location below.

---

## Review Dimensions

### 1. Argument Structure
- Is the research question clearly stated?
- Does the introduction motivate the question effectively?
- Is the logical flow sound (question → method → results → conclusion)?
- Are the conclusions supported by the evidence?
- Are limitations acknowledged?

### 2. Research Design & Validity
- Are the claims supported by the design?
- What are the key assumptions? Are they stated explicitly?
- What threats to validity exist (confounding, selection bias, measurement error, external validity)?
- Are robustness checks adequate?
- Is the research design appropriate for the question?

### 3. Methodology / Analytical Approach
- Are the methods appropriate for the research question?
- Are statistical or computational choices justified?
- Are results robust to alternative specifications?
- Sample selection issues?
- Are results substantively meaningful (not just statistically significant)?

### 4. Literature Positioning
- Are the key papers cited?
- Is prior work characterized accurately?
- Is the contribution clearly differentiated from existing work?
- Any missing citations that a referee would flag?

### 5. Writing Quality
- Clarity and concision
- Academic tone
- Consistent notation throughout
- Abstract effectively summarizes the paper
- Tables and figures are self-contained (clear labels, notes, sources)

### 6. Presentation
- Are tables and figures well-designed?
- Is notation consistent throughout?
- Are there any typos, grammatical errors, or formatting issues?
- Is the paper the right length for the contribution?

---

## Structured Output

After review, emit this block for agent consumption:

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

Scoring key:
- 5 = Excellent (no significant issues)
- 4 = Good (minor issues only)
- 3 = Acceptable (some concerns but addressable)
- 2 = Weak (major concerns)
- 1 = Unacceptable (fundamental flaws)

---

## Report Format

```markdown
# Manuscript Review: [Paper Title]

**Date:** [YYYY-MM-DD]
**Reviewer:** review-paper skill
**File:** [path to manuscript]

## Summary Assessment

**Overall recommendation:** [Strong Accept / Accept / Revise & Resubmit / Reject]

[2-3 paragraph summary: main contribution, strengths, and key concerns]

## Strengths

1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Major Concerns

### MC1: [Title]
- **Dimension:** [Argument / Research Design / Methodology / Literature / Writing / Presentation]
- **Issue:** [Specific description]
- **Suggestion:** [How to address it]
- **Location:** [Section/page/table if applicable]

[Repeat for each major concern]

## Minor Concerns

### mc1: [Title]
- **Issue:** [Description]
- **Suggestion:** [Fix]

[Repeat]

## Referee Objections

These are the tough questions a top referee would likely raise:

### RO1: [Question]
**Why it matters:** [Why this could be fatal]
**How to address it:** [Suggested response or additional analysis]

[Repeat for 3-5 objections]

## Specific Comments

[Line-by-line or section-by-section comments, if any]

## Summary Statistics

| Dimension | Rating (1-5) |
|-----------|-------------|
| Argument Structure | [N] |
| Research Design | [N] |
| Methodology | [N] |
| Literature | [N] |
| Writing | [N] |
| Presentation | [N] |
| **Overall** | **[N]** |
```

---

## Output Location

Determine the save path:
1. Check if recent context is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/paper_review_[sanitized_name].md`.
3. If NO: save to `docs/core/paper_review_[sanitized_name].md`.
4. Create the directory if it does not exist.

---

## Important

- **Be constructive.** Every criticism should come with a suggestion.
- **Be specific.** Reference exact sections, equations, tables.
- **Think like a referee at a top journal.** What would make them reject?
- **Distinguish fatal flaws from minor issues.** Not everything is equally important.
- **Acknowledge what's done well.** Good research deserves recognition.
- **Do NOT fabricate details.** If you can't read a section clearly, say so.
- **Handle empty stubs gracefully.** If the manuscript is empty, report "Manuscript is empty — nothing to review."
