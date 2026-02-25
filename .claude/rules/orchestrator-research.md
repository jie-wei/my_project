---
paths:
  - "code/scripts/**/*.py"
---

# Research Project Orchestrator (Simplified)

**For Python scripts, simulations, and data analysis** -- use this simplified loop instead of the full multi-agent orchestrator.

## The Simple Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run code, check outputs
  │         Python scripts: runs without error
  │         Simulations: seed reproducibility
  │         Plots: files created, correct format
  │         If verification fails → fix → re-verify
  │
  Step 3: SCORE — Apply quality-gates rubric
  │
  └── Score >= 80?
        YES → Done (commit when user signals)
        NO  → Fix blocking issues, re-verify, re-score
```

**No multi-agent review. Just: write, test, done.**

## Verification Checklist

- [ ] Script runs without errors
- [ ] All imports at top
- [ ] No hardcoded absolute paths (use config.py)
- [ ] Seed set if stochastic
- [ ] Output files created at expected paths
- [ ] Tolerance checks pass (if applicable)
- [ ] Quality score >= 80
