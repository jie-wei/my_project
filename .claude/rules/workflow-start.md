# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)

---

## Routing

```
Your instruction
    │
    ├─ Exploration? ──────────── read: workflow-exploration.md
    │  (new idea to test)          Code immediately. 60/100 threshold.
    │
    ├─ Trivial production? ────── read: protocol-verification.md, standalone-quality.md
    │  (typo, one-line fix)        Just do it. Verify. 80/100 threshold.
    │
    └─ Non-trivial production? ── read: workflow-plan.md, protocol-orchestrator.md
       (multi-file, unclear)       Plan first → orchestrator executes.
```

After any task completes, run the appropriate verification protocol and score against `standalone-quality.md`.

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

| Context | Threshold | Action if below |
|---------|-----------|-----------------|
| Production (`core/`) | 80/100 | Fix blocking issues |
| Exploration | 60/100 | Fix blocking issues |

---

## Non-Negotiables

- **Path convention:** All paths from `config.py`, never hardcoded
- **Seed convention:** Set seed once at top for stochastic code
- **Data:** `data/raw/` is sacred — never modify
- **src/ vs scripts/:** Pure logic in `src/`, file I/O in `scripts/`

---

## Preferences

**Session logs:** Always (post-plan, incremental, end-of-session)
**Reporting:** Concise summaries, details on request
