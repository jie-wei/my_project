# Orchestrator Protocol

**After a plan is approved, the orchestrator takes over autonomously.**

## The Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run/compile, check outputs (see protocol-verification.md)
  │         If verification fails → fix → re-verify
  │
  ├─ Scripts (code/scripts/) → skip to Step 5
  │
  Step 3: REVIEW — Review against quality rubric, by file type (see standalone-quality.md)
  │
  Step 4: FIX — Apply fixes (critical → major → minor)
  │         RE-VERIFY — Confirm fixes are clean
  │
  Step 5: SCORE — Apply quality-gates rubric
  │
  └── Score >= threshold?
        YES → Present summary to user
        NO  → Loop back to Step 3 (max 5 rounds)
              After max rounds → present with remaining issues
```

## File-Type Routing

Skills are in `.claude/skills/`. Use them for review steps.

| File Pattern             | Step 2 (VERIFY) | Step 3 (REVIEW)                            |
| ------------------------ | --------------- | ------------------------------------------ |
| `code/src/**/*.py`     | verifier        | `/review-python`                         |
| `code/scripts/**/*.py` | verifier        | `/review-python`                         |
| `paper/*.tex`          | verifier        | `/review-manuscript and /review-details` |

When multiple review perspectives apply, run them in parallel (they check different things).
The domain-reviewer template is at `docs/templates/domain-reviewer.md` — customize it for your field, then copy to `.claude/agents/` and add it to this table.

For exploration files, use 60/100 threshold per standalone-quality.md.

## Script Verification Checklist

For `code/scripts/**/*.py` (the simplified path):

- [ ] Script runs without errors
- [ ] All imports at top
- [ ] No hardcoded absolute paths (use config.py)
- [ ] Seed set if stochastic
- [ ] Output files created at expected paths
- [ ] Tolerance checks pass (if applicable)

## Limits

- **Main loop:** max 5 review-fix rounds
- **Verification retries:** max 2 attempts per step
- Never loop indefinitely

## "Just Do It" Mode

When user says "just do it" / "handle it":

- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary
