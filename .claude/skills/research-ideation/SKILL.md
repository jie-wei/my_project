---
name: research-ideation
description: Generate research questions, hypotheses, and strategies from a topic or dataset
disable-model-invocation: true
argument-hint: "[topic, phenomenon, or dataset description]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Research Ideation

Generate structured research questions, testable hypotheses, and empirical strategies from a topic, phenomenon, or dataset.

**Input:** `$ARGUMENTS` — a topic (e.g., "minimum wage effects on employment"), a phenomenon (e.g., "why do firms cluster geographically?"), or a dataset description (e.g., "panel of US counties with pollution and health outcomes, 2000-2020").

---

## Steps

1. **Understand the input.** Read `$ARGUMENTS` and any referenced files. Check `docs/core/` and `docs/exploration/` for related analysis notes. Check `paper/` for existing manuscript context. Check `.claude/rules/` for domain conventions.

2. **Generate 3-5 research questions** ordered from descriptive to causal:
   - **Descriptive:** What are the patterns? (e.g., "How has X evolved over time?")
   - **Correlational:** What factors are associated? (e.g., "Is X correlated with Y after controlling for Z?")
   - **Causal:** What is the effect? (e.g., "What is the causal effect of X on Y?")
   - **Mechanism:** Why does the effect exist? (e.g., "Through what channel does X affect Y?")
   - **Policy:** What are the implications? (e.g., "Would intervention X improve outcome Y?")

3. **For each research question, develop:**
   - **Hypothesis:** A testable prediction with expected sign/magnitude
   - **Research design / analytical strategy:** How to establish validity (experimental, quasi-experimental, observational, computational, mixed-methods, etc.)
   - **Data requirements:** What data would be needed? Is it available?
   - **Key assumptions:** What must hold for the results to be valid?
   - **Potential pitfalls:** Common threats to validity
   - **Related literature:** 2-3 papers using similar approaches

4. **Rank the questions** by feasibility and contribution.

5. **Save the output** — see Output Location below.

---

## Output Format

```markdown
# Research Ideation: [Topic]

**Date:** [YYYY-MM-DD]
**Input:** [Original input]

## Overview

[1-2 paragraphs situating the topic and why it matters]

## Research Questions

### RQ1: [Question] (Feasibility: High/Medium/Low)

**Type:** Descriptive / Correlational / Causal / Mechanism / Policy

**Hypothesis:** [Testable prediction]

**Research Design:**
- **Method:** [e.g., Randomized experiment, Difference-in-differences, Regression discontinuity, Instrumental variables, Simulation, Qualitative coding]
- **Treatment / variation:** [What varies and when]
- **Comparison group:** [Control or counterfactual]
- **Key assumption:** [What must hold for validity]

**Data Requirements:**
- [Dataset 1 — what it provides]
- [Dataset 2 — what it provides]

**Potential Pitfalls:**
1. [Threat 1 and possible mitigation]
2. [Threat 2 and possible mitigation]

**Related Work:** [Author (Year)], [Author (Year)]

---

[Repeat for RQ2-RQ5]

## Ranking

| RQ | Feasibility | Contribution | Priority |
|----|-------------|-------------|----------|
| 1  | High        | Medium      | ...      |
| 2  | Medium      | High        | ...      |

## Suggested Next Steps

1. [Most promising direction and immediate action]
2. [Data to obtain]
3. [Literature to review deeper]
```

---

## Output Location

Determine the save path:
1. Check if recent context (open files, cwd, recent edits) is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/research_ideation_[sanitized_topic].md`.
3. If NO: save to `docs/core/research_ideation_[sanitized_topic].md`.
4. Create the directory if it does not exist.

---

## Principles

- **Be creative but grounded.** Push beyond obvious questions, but every suggestion must be empirically feasible.
- **Think like a reviewer.** For each causal or inferential claim, immediately identify the validity threat.
- **Consider data availability.** A brilliant question with no available data is not actionable.
- **Suggest specific data sources** where possible (public repositories, administrative data, survey data, etc.).
