# CLAUDE.md — Project Template

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `docs/quality_reports/plans/`
- **Verify after** — run/compile and confirm output at the end of every task
- **Quality gates** — nothing ships below 80/100
- **Session logging** — log after plan approval, incrementally during work, at session end

**IMPORTANT: Never use the AskUserQuestion tool. Always ask questions in plain text within your response.**
**IMPORTANT: Never use the ExitPlanMode tool to request approval. Always ask for approval in plain text within your response.**

## Folder Structure

```
code/
  src/mypackage/
    core/                    # Pure logic (no I/O) — production
    exploration/             # Experimental logic
    archive/                 # Retired experiments
  scripts/
    core/                    # Numbered pipeline scripts (I/O)
    exploration/             # Notebooks and experiments
    archive/                 # Retired scripts
  tests/                     # Tests for src/ logic
data/
  raw/                       # Sacred — never modify
  intermediate/              # Rebuilt by scripts
  processed/                 # Rebuilt by scripts
docs/
  core/                      # Analysis notes (promoted)
  exploration/               # Analysis notes (experimental)
  archive/                   # Retired notes
  quality_reports/
    plans/                   # Saved plans (survive compaction)
    session_logs/            # Session logs
    merges/                  # Quality reports at merge time
    specs/                   # Requirements specifications
  templates/                 # Reusable markdown templates
output/
  core/                      # Pipeline outputs
  exploration/               # Experiment outputs
  archive/                   # Retired outputs
paper/                       # Manuscript files
.claude/
  hooks/                     # Automation hooks
  rules/                     # Behavioral rules
  skills/                    # Custom skills
```

## Quality Thresholds

80 = Commit | 90 = PR | 95 = Excellence

## Skills

| Command | What It Does |
|---------|--------------|
| `/commit [msg]` | Stage, commit, PR, merge |
| `/research-ideation [topic]` | Generate RQs, hypotheses, strategies |
| `/interview-me [topic]` | Conversational interview → research spec |
| `/lit-review [topic]` | Literature search, synthesis, BibTeX |
| `/compile-latex [file]` | Multi-pass xelatex + bibtex compilation |
| `/validate-bib` | Cross-reference citations vs .bib |
| `/proofread [file or 'all']` | Grammar, typos, consistency check (report only) |
| `/review-paper [file]` | Referee-quality 6-dimension manuscript review |

## Commands

- `python3` / `pytest` — run and test Python code
- `uv` — Python package management
- `xelatex` / `pdflatex` / `latexmk` — LaTeX compilation
- `bibtex` — bibliography processing

## Rules Reference

- `.claude/rules/project-conventions.md` — code organization, data flow, parallel structure
- `.claude/rules/plan-first-workflow.md` — planning protocol, requirements specs
- `.claude/rules/session-logging.md` — when to update session logs
- `.claude/rules/orchestrator-protocol.md` — post-plan execution loop
- `.claude/rules/orchestrator-research.md` — simplified loop for scripts/data analysis
- `.claude/rules/quality-gates.md` — scoring rubrics by file type
- `.claude/rules/verification-protocol.md` — how to verify each file type
- `.claude/rules/workflow-quick-ref.md` — contractor model, when to ask vs execute
- `.claude/rules/exploration-fast-track.md` — lightweight exploration workflow, 60/100 threshold
- `.claude/rules/exploration-lifecycle.md` — promotion, archiving, graduation checklist

## Agents (Orchestrator)

Path-scoped rules that fill Steps 2 (VERIFY) and 3 (REVIEW) of the orchestrator loop.

| Rule | Scope | Step | What It Does |
|------|-------|------|-------------|
| `verify-python.md` | `code/**/*.py` | VERIFY | Import check, pytest, run script, convention check |
| `review-python.md` | `code/**/*.py` | REVIEW | Quality scoring against Python rubrics |
| `verify-latex.md` | `paper/**/*.tex` | VERIFY | Compile LaTeX, validate bibliography |
| `proofread-manuscript.md` | `paper/**/*.tex` | REVIEW | Grammar, typos, consistency (report only) |
| `review-domain.md` | `paper/**/*.tex` | REVIEW | 6-dimension content review with referee objections |

## Hooks (Automatic)

- **context-monitor** — warns at 40/55/65/80/90% context usage
- **verify-reminder** — reminds to run/compile after editing .py/.tex files
- **log-reminder** — blocks if 15+ responses without session log update
- **pre-compact / post-compact** — saves and restores plan state across compaction
- **protect-files** — blocks edits to protected files (references.bib, settings.json)
- **latex-cleanup** — auto-deletes auxiliary files after LaTeX compilation
