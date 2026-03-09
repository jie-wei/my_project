# Interpretation Guide

Patterns for reasoning about empirical results. Read this before writing the Discussion section.

---

## 1. Proposing Mechanisms

Don't just report what the data shows — explain *why* the pattern might exist.

**From coefficient to mechanism:**
- "The positive coefficient on X suggests that [mechanism], possibly because [channel]."
- "One explanation for the [pattern] is that [economic logic]. Under this view, [implication for other variables]."

**Multiple mechanisms for one result:**
- Generate 2-3 candidate explanations for each key finding
- For each: what economic behavior would produce this pattern?
- Prefer mechanisms that are specific and falsifiable over vague ones

**Connecting to theory:**
- Which standard economic models predict this sign/magnitude?
- Does the effect size make economic sense? (e.g., a 1 SD change in X produces a Y% change — is that plausible?)
- Are there known results in the literature that this aligns with or contradicts?

---

## 2. Testing Conjectures Against Data

Each conjecture should generate predictions that can be checked against the current outputs.

**The if-then pattern:**
- "If [mechanism A] drives this result, we would expect [prediction]. Table N [confirms/contradicts] this: [evidence]."
- "Under [mechanism B], the effect should be [stronger/weaker/absent] for [subgroup]. Figure N shows [what we actually see]."

**Cross-result validation:**
- Does a pattern in one table explain an anomaly in another?
- If two results seem contradictory, is there a mechanism that reconciles them?
- Do robustness checks strengthen or weaken the main finding?

**Dose-response and monotonicity:**
- If the mechanism is real, does the effect scale as expected? (e.g., stronger treatment → larger coefficient)
- Are there nonlinearities that suggest threshold effects or saturation?

---

## 3. Distinguishing Competing Explanations

When multiple mechanisms could produce the same pattern, identify what would differentiate them.

**Separation strategies:**
- "This pattern is consistent with both [A] and [B]. To distinguish them, one would examine [variable/subgroup/specification], because [A] predicts [X] while [B] predicts [Y]."
- "The [heterogeneity analysis / interaction term / subsample] in Table N helps separate these: [what it shows and what that implies]."

**Ranking explanations:**
- Which explanation is most parsimonious?
- Which requires the fewest auxiliary assumptions?
- Which is consistent with the broadest set of results?
- Flag the leading explanation and the strongest alternative

---

## 4. Identifying Artifacts vs. Real Effects

Before interpreting a result as economically meaningful, consider whether it could be mechanical or spurious.

**Compositional artifacts:**
- Could the result reflect changes in the *composition* of the sample rather than changes in *behavior*? (e.g., firms that exit the sample differ systematically from those that remain)
- If a group-level pattern appears, does it hold within groups or only between them? (ecological fallacy)

**Selection effects:**
- Is the sample selected on an outcome related to the variable of interest?
- Could survivorship bias, self-selection, or non-random attrition explain the pattern?

**Mechanical relationships:**
- Is the result a tautological consequence of how variables are defined? (e.g., regressing revenue/employee on firm size when both use employee counts)
- Could measurement conventions create artificial correlations?

**Methodology-driven patterns:**
- Would a different estimation approach produce the same result?
- Is the result sensitive to functional form, sample window, or variable construction?
- Do the robustness checks in the appendix speak to this?

---

## 5. Framing Null Results

A null result is not a failure — it's information. Frame it productively.

**Informative nulls:**
- "The absence of a significant effect on [X], combined with the strong effect on [Y], suggests that the mechanism operates through [channel Y] rather than [channel X]."
- "The null result rules out [explanation], narrowing the set of plausible mechanisms to [remaining candidates]."

**Precision matters:**
- A precise zero (tight confidence interval around zero) is much more informative than an imprecise zero (wide confidence interval)
- "We can rule out effects larger than [bound] at the 95% level" is more useful than "the effect is not significant"

**Null vs. underpowered:**
- Is the sample large enough to detect an economically meaningful effect?
- If power is low, frame the null as "inconclusive" rather than "no effect"

---

## 6. Synthesizing Across Results

The Discussion should tell a coherent story, not summarize results one by one.

**Narrative arc:**
- What is the central finding when all results are considered together?
- Which results are the backbone of the story, and which are supporting evidence?
- Are there results that complicate the story? (Don't hide them — they add credibility)

**Limitations as research opportunities:**
- Each limitation suggests a future analysis: "This analysis cannot distinguish [A] from [B] because [reason]. A future study with [data/method] could resolve this."
- Frame open questions as contributions: identifying what we don't know is valuable

**Confidence calibration:**
- Clearly distinguish: well-established findings (multiple consistent results) vs. suggestive patterns (single result, plausible but not confirmed) vs. speculative conjectures (interesting but untested)
- Use language that matches the evidence strength: "demonstrates" vs. "suggests" vs. "raises the possibility"
