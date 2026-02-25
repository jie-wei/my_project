# CLAUDE.md — Project Template

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `docs/quality_reports/plans/`
- **Verify after** — run/compile and confirm output at the end of every task
- **Quality gates** — nothing ships below 80/100
- **Session logging** — log after plan approval, incrementally during work, at session end

## Folder Structure

```
code/
  src/mypackage/core/       # Pure logic (no I/O)
  src/mypackage/exploration/ # Experimental logic
  scripts/core/              # Numbered pipeline scripts (I/O)
  scripts/exploration/       # Notebooks and experiments
  tests/                     # Tests for src/ logic
data/
  raw/                       # Sacred — never modify
  intermediate/              # Rebuilt by scripts
  processed/                 # Rebuilt by scripts
docs/
  core/                      # Analysis notes (promoted)
  exploration/               # Analysis notes (experimental)
  quality_reports/
    plans/                   # Saved plans (survive compaction)
    session_logs/            # Session logs
    merges/                  # Quality reports at merge time
    specs/                   # Requirements specifications
  templates/                 # Reusable markdown templates
output/
  core/                      # Pipeline outputs
  exploration/               # Experiment outputs
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

## Commands

- `python3` / `pytest` — run and test Python code
- `uv` — Python package management
- `xelatex` / `pdflatex` / `latexmk` — LaTeX compilation
- `bibtex` — bibliography processing

## Rules Reference

- `.claude/rules/project-conventions.md` — code organization, data flow, parallel structure
- `.claude/rules/plan-first-workflow.md` — planning protocol, requirements specs
- `.claude/rules/session-logging.md` — when to update session logs

## Hooks (Automatic)

- **context-monitor** — warns at 40/55/65/80/90% context usage
- **verify-reminder** — reminds to run/compile after editing .py/.tex files
- **log-reminder** — blocks if 15+ responses without session log update
- **pre-compact / post-compact** — saves and restores plan state across compaction
- **protect-files** — blocks edits to protected files (references.bib, settings.json)
