# CLAUDE.md — Project Template

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `docs/quality_reports/plans/`
- **Verify after** — compile/run and confirm output at the end of every task
- **Quality gates** — nothing ships below 80/100
- **Session logging** — log after plan approval, incrementally during work, at session end
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to `MEMORY.md`

**IMPORTANT: Never use the AskUserQuestion tool. Always ask questions in plain text within your response.**
**IMPORTANT: Never use the ExitPlanMode tool to request approval. Always ask for approval in plain text within your response.**

**On every session start, read:** `.claude/rules/workflow-start.md`, `.claude/rules/standalone-conventions.md`

## LaTeX

- **Always `cd paper/` before running `latexmk`.** The `.latexmkrc` in `paper/` only takes effect from that directory. Running from the project root dumps aux files in the wrong place and fails to find template classes.
