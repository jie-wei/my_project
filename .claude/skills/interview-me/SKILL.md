---
name: interview-me
description: Conversational interview to formalize a research idea into a structured specification
disable-model-invocation: true
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: ["Read", "Write"]
---

# Research Interview

Conduct a structured interview to help formalize a research idea into a concrete specification.

**Input:** `$ARGUMENTS` — a brief topic description or "start fresh" for an open-ended exploration.

---

## How This Works

This is a **conversational** skill. Instead of producing a report immediately, you conduct an interview by asking questions one at a time, probing deeper based on answers, and building toward a structured research specification.

**Do NOT use AskUserQuestion.** Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing.

---

## Interview Structure

### Phase 1: The Big Picture (1-2 questions)
- "What phenomenon or puzzle are you trying to understand?"
- "Why does this matter? Who should care about the answer?"

### Phase 2: Theoretical Motivation (1-2 questions)
- "What's your intuition for why X happens / what drives Y?"
- "What would standard theory predict? Do you expect something different?"

### Phase 3: Data and Setting (1-2 questions)
- "What data do you have access to, or what data would you ideally want?"
- "Is there a specific context, time period, or institutional setting you're focused on?"

### Phase 4: Research Design (1-2 questions)
- "What is your research design? Is there a natural experiment, randomized assignment, or other source of variation you can exploit?"
- "What is the biggest threat to the validity of your findings?"

### Phase 5: Expected Results (1-2 questions)
- "What would you expect to find? What would surprise you?"
- "What would the results imply for policy or theory?"

### Phase 6: Contribution (1 question)
- "How does this differ from what's already been done? What's the gap you're filling?"

---

## After the Interview

Once you have enough information (typically 5-8 exchanges), produce a **Research Specification Document**:

```markdown
# Research Specification: [Title]

**Date:** [YYYY-MM-DD]
**Researcher:** [from conversation context]

## Research Question

[Clear, specific question in one sentence]

## Motivation

[2-3 paragraphs: why this matters, theoretical context, policy relevance]

## Hypothesis

[Testable prediction with expected direction]

## Research Design

- **Method:** [e.g., Randomized experiment, Difference-in-differences, Regression discontinuity, Simulation, Mixed methods]
- **Treatment / variation:** [What varies]
- **Comparison group:** [Control or counterfactual]
- **Key assumption:** [What must hold for validity]
- **Robustness checks:** [Sensitivity analyses, alternative specifications, etc.]

## Data

- **Primary dataset:** [Name, source, coverage]
- **Key variables:** [Treatment, outcome, controls]
- **Sample:** [Unit of observation, time period, N]

## Expected Results

[What the researcher expects to find and why]

## Contribution

[How this advances the literature — 2-3 sentences]

## Open Questions

[Issues raised during the interview that need further thought]
```

---

## Output Location

Determine the save path:
1. Check if recent context is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/research_spec_[sanitized_topic].md`.
3. If NO: save to `docs/core/research_spec_[sanitized_topic].md`.
4. Create the directory if it does not exist.

---

## Important

- **CONVERSATIONAL SKILL.** Do NOT produce a report immediately. Ask questions one at a time.
- **Do NOT use AskUserQuestion tool.** Ask questions directly in your text responses.
- **Session logging.** This skill involves many exchanges. The log-reminder hook fires at 15 responses. Update the session log with the interview topic and key decisions between phases.
- **Be curious, not prescriptive.** Your job is to draw out the researcher's thinking, not impose your own ideas.
- **Probe weak spots gently.** If the research design sounds fragile, ask "What would a skeptic say about...?" rather than "This won't work because..."
- **Build on answers.** Each question should follow from the previous response.
- **Know when to stop.** If the researcher has a clear vision after 4-5 exchanges, move to the specification. Don't over-interview.
