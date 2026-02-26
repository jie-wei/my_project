# CLAUDE.md — Project Template

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `docs/quality_reports/plans/`
- **Verify after** — compile/run and confirm output at the end of every task
- **Quality gates** — nothing ships below 80/100
- **Session logging** — log after plan approval, incrementally during work, at session end
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to `MEMORY.md`

**IMPORTANT: Never use the AskUserQuestion tool. Always ask questions in plain text within your response.**
**IMPORTANT: Never use the ExitPlanMode tool to request approval. Always ask for approval in plain text within your response.**

## Master Routing [read: .claude/rules/workflow-start.md, standalone-conventions.md]

```
Your instruction
    │
    ├─ Exploration? ────────────── EXPLORATION FAST-TRACK
    │  (new idea to test)            read: .claude/rules/workflow-exploration.md
    │
    ├─ Trivial production? ──────── JUST DO IT
    │  (typo, one-line fix)          read: .claude/rules/protocol-verification.md, standalone-quality.md
    │
    └─ Non-trivial production? ──── PLAN-FIRST WORKFLOW
       (multi-file, unclear)         read: .claude/rules/workflow-plan.md, protocol-orchestrator.md
```

