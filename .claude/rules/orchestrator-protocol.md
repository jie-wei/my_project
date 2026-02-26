# Orchestrator Protocol

**After a plan is approved, the orchestrator takes over autonomously.**

## The Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run/compile, check outputs (see verification-protocol.md)
  │         If verification fails → fix → re-verify
  │
  Step 3: REVIEW — Review against quality rubric, by file type (see quality-gates.md)
  │
  Step 4: FIX — Apply fixes (critical → major → minor)
  │
  Step 5: RE-VERIFY — Confirm fixes are clean
  │
  Step 6: SCORE — Apply quality-gates rubric
  │
  └── Score >= threshold?
        YES → Present summary to user
        NO  → Loop back to Step 3 (max 5 rounds)
              After max rounds → present with remaining issues
```

## File-Type Routing

| File Pattern | Step 2 (VERIFY) | Step 3 (REVIEW) |
|-------------|-----------------|-----------------|
| `code/src/mypackage/core/*.py` | verify-python.md | review-python.md |
| `code/scripts/core/*.py` | verify-python.md | review-python.md |
| `code/**/exploration/**/*.py` | verify-python.md (60/100) | review-python.md (60/100) |
| `paper/*.tex` | verify-latex.md | proofread-manuscript.md + review-domain.md |

When multiple review agents apply (LaTeX), run them sequentially:
proofread-manuscript.md first (surface issues), then review-domain.md (content depth).

For exploration files, use 60/100 threshold per quality-gates.md.

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
