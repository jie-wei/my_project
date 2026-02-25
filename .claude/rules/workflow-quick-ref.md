# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, verify, done
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (fast) vs. Option B (robust). Which?"
- **Code ambiguity:** "Spec unclear on X. Assume Y?"
- **Tolerance edge case:** "Just missed tolerance. Investigate?"
- **Scope question:** "Also refactor Y while here, or focus on X?"

---

## I Just Execute When

- Code fix is obvious (bug, pattern application)
- Verification (tolerance checks, tests, compilation)
- Documentation (logs, commits)
- Plotting (per established standards)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables (Customize These)

<!-- Replace with YOUR project's locked-in preferences -->

- **Path convention:** All paths from `config.py`, never hardcoded
- **Seed convention:** <!-- e.g., set seed once at top for stochastic code -->
- **Figure standards:** <!-- e.g., white bg, 300 DPI, custom theme -->
- **Color palette:** <!-- e.g., institutional colors -->
- **Tolerance thresholds:** <!-- e.g., 1e-6 for point estimates -->

---

## Preferences

<!-- Fill in as you discover your working style -->

**Visual:** <!-- How you want figures/plots handled -->
**Reporting:** <!-- Concise bullets? Detailed prose? Details on request? -->
**Session logs:** Always (post-plan, incremental, end-of-session)
**Replication:** <!-- How strict? Flag near-misses? -->
