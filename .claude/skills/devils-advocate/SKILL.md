---
name: devils-advocate
description: Challenge research design, analysis, or manuscript with 5-7 tough questions. Checks assumptions, validity threats, and logical gaps.
disable-model-invocation: true
argument-hint: "[file path, analysis description, or research design]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Devil's Advocate Review

Critically examine a research design, analysis, or manuscript and challenge it with 5-7 specific, constructive questions.

**Philosophy:** "We arrive at the strongest possible research through active dialogue."

**Input:** `$ARGUMENTS` -- a file path (script, manuscript, analysis notes), a research design description, or a specific decision to challenge.

---

## Setup

1. **Read the target.** If `$ARGUMENTS` is a file path, read it. If it's a description, work from that.
2. **Read project context.** Check `docs/core/` and `docs/exploration/` for related analysis notes. Check `paper/` for manuscript context. Check `.claude/rules/` for project conventions.
3. **If applicable, read adjacent files** -- related scripts, data documentation (`data/codebook.md`), or earlier analysis in the same exploration.

---

## Challenge Categories

Generate 5-7 challenges from these categories (not all categories need to appear -- pick the ones that matter most):

### 1. Assumption Challenges
> "This analysis assumes X. What happens if X doesn't hold?"

Probe statistical assumptions (linearity, independence, normality), data assumptions (missing at random, measurement validity), and domain assumptions (equilibrium, rationality, stationarity).

### 2. Validity Threats
> "Could Y explain this result instead of your proposed mechanism?"

Identify confounders, reverse causality, selection bias, survivorship bias, p-hacking, or specification searching.

### 3. Alternative Approaches
> "Here are 2 other ways to answer this question. Why is yours better?"

Suggest alternative methods, estimators, or frameworks and ask why the current choice dominates.

### 4. Missing Steps
> "What happens between step A and step C? Is step B implicit?"

Find gaps in the pipeline, undocumented decisions, unexplained parameter choices, or missing robustness checks.

### 5. Data Challenges
> "Is this sample representative of the population you're making claims about?"

Question sample selection, external validity, measurement quality, data vintage, and whether the data can actually identify what's claimed.

### 6. Logical Gaps
> "The conclusion claims X, but the evidence only shows Y."

Find over-claims, unstated assumptions bridging evidence to conclusion, and places where correlation is treated as causation.

### 7. Reproducibility Concerns
> "Could someone replicate this from your description alone?"

Check for hardcoded values, missing seeds, undocumented preprocessing, environment dependencies, or results that depend on run order.

---

## Output Format

```markdown
# Devil's Advocate: [Target Description]

**Date:** [YYYY-MM-DD]
**Target:** [file path or description]

## Challenges

### Challenge 1: [Category] -- [Short title]
**Question:** [The specific question]
**Why it matters:** [What could go wrong if this isn't addressed]
**Suggested resolution:** [Specific action or analysis to resolve it]
**Location:** [File, section, line number, or step if applicable]
**Severity:** High / Medium / Low

[Repeat for 5-7 challenges]

## Summary Verdict
**Strengths:** [2-3 things done well]
**Critical changes:** [0-2 changes needed before this is solid]
**Suggested improvements:** [2-3 nice-to-have enhancements]
```

---

## Output Location

Determine the save path:
1. Check if recent context (open files, cwd, recent edits) is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/devils_advocate_[sanitized_target].md`.
3. If NO: save to `docs/core/devils_advocate_[sanitized_target].md`.
4. Create the directory if it does not exist.

---

## Principles

- **Be specific.** Reference exact lines, variables, equations, or steps -- not vague concerns.
- **Be constructive.** Every challenge must include a suggested resolution.
- **Be honest.** If the work is solid, say so. Don't manufacture problems.
- **Prioritize.** Validity threats and assumption failures outweigh style concerns.
- **Think like a skeptical reviewer.** What would make someone reject this paper or distrust these results?
- **Distinguish fatal from fixable.** A confounded identification strategy is different from a missing robustness check.
