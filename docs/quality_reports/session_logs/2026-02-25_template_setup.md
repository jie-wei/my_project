# 2026-02-25 — Template Setup Session

## Goal
Continue building out the project template: restructure folders, set up dependencies, configure tooling.

## Progress

### Project restructuring
- Implemented parallel `core/` and `exploration/` naming across 4 layers: src, scripts, output, docs
- Split `output/` into `output/core/` (tables, figures) and `output/exploration/`
- Renamed `_experimental/` → `exploration/` in `src/mypackage/`, added `core/` subpackage
- Moved root `exploration/` into `code/scripts/exploration/` with `archive/`
- Created `scripts/core/` for numbered pipeline scripts
- Added `docs/core/archive/` and `docs/exploration/archive/`
- Updated config.py, README.md, project-conventions.md throughout
- Discussed config splitting — decided single shared config
- PR #4: merged structural changes

### Dependencies (pyproject.toml)
- Added 16 packages in groups: data, stats/econometrics, visualization, output, R interop, utilities
- Put pytest and ruff under `[project.optional-dependencies] dev`
- Added rpy2 for R interop

### Bug fix
- Fixed log_reminder.py Case 3: now checks if latest log filename matches today's date
- If not today's date, tells Claude to create a new daily log instead of appending to old one

### Tooling discussion
- Compared black vs ruff — chose ruff (faster, replaces black+flake8+isort)
- Discussed ruff config options for pyproject.toml
- Discussed VS Code Ruff extension for format-on-save

### Ruff config
- Added minimal ruff config to pyproject.toml: line-length 88, py312, F + I lint rules

### .gitignore & data structure
- Updated .gitignore: added uv.lock, egg-info, .ipynb_checkpoints
- Added .gitkeep pattern for data/ dirs (ignore contents, keep folder structure)
- Kept output/ tracked (no gitignore for output)

### README — Getting Started & Template Usage
- Added "Getting Started" section: uv install, venv creation, editable install
- Added "Using This Template" section: clone, rename package, workflow overview

### Pre-compact hook fix
- Diagnosed pre-compact.sh not working — missing execute bit (chmod +x)
- Switched to Python-based hooks matching original repo (pedrohcgs/claude-code-my-workflow)
- Created `.claude/hooks/pre-compact.py` — captures plan state, decisions, appends log note
- Created `.claude/hooks/post-compact-restore.py` — restores context after compaction
- Updated settings.json: PreCompact → python3 pre-compact.py, added SessionStart hook
- Adapted all paths from `quality_reports/` → `docs/quality_reports/`

### Comparison with pedrohcgs/claude-code-my-workflow
- Cloned their repo to /tmp for local reading (GitHub API kept hitting 500 errors)
- Read all files: 17 rules, 10 agents, 21 skills, 7 templates, 7 hooks, scripts
- Produced full item-by-item comparison grouped by category
- Mapped the interdependency graph — their setup has 6 interlocking clusters:
  - A: Context Survival (hooks, logging, compact state)
  - B: Plan → Execute → Verify Loop (plan-first, orchestrator, quality gates)
  - C: Quality & Review (agents, scoring, proofreading protocol)
  - D: Exploration Lifecycle (protocols, fast-track, templates)
  - E: Research Skills (lit-review, ideation, interview, paper review — standalone)
  - F: Institutional Memory (/learn skill, MEMORY.md, context-monitor)
- Key insight: items can't be cherry-picked — must adopt in coherent clusters
- Identified minimum viable foundation: plan-first rule + session-logging rule + context-monitor hook + verify-reminder hook + templates + richer CLAUDE.md
- This completes the loop: compact hooks already save/restore plans, but nothing currently creates plans in docs/quality_reports/plans/

### Decision
- Adopt cluster-by-cluster, starting with Cluster A (context survival) + minimal Cluster B splice (plan-first rule) as the domain-agnostic foundation
- Research skills (Cluster E) are standalone and can come any time
- Agents/full orchestrator (Cluster C) deferred — most effort, add later

### Foundation Set Implementation (completed)
- Created `docs/templates/` with 5 templates: session-log.md, quality-report.md, requirements-spec.md, exploration-readme.md, archive-readme.md
- Created `docs/quality_reports/specs/` with .gitkeep (consistent with plans/ and merges/)
- Created `.claude/hooks/context-monitor.py` — PostToolUse on Bash|Task, progressive warnings at 40/55/65/80/90% context
- Created `.claude/hooks/verify-reminder.py` — PostToolUse on Write|Edit, reminds to run/compile .py/.tex files
- Moved `log_reminder.py` from `docs/quality_reports/session_logs/` to `.claude/hooks/` — fixed quoting inconsistency, added CLAUDE_PROJECT_DIR fallback
- Created `.claude/rules/plan-first-workflow.md` — plan mode protocol, requirements spec protocol, context survival strategy
- Created `.claude/rules/session-logging.md` — 3 triggers (post-plan, incremental, end-of-session), quality reports at merge time
- Updated `.claude/settings.json` — added PostToolUse hooks (context-monitor, verify-reminder), fixed Stop hook path
- Rewrote `CLAUDE.md` — richer entry point with principles, folder structure, quality thresholds, skills, commands, rules reference, hooks reference

### Still TODO
- Add example files (sample script, function, test)
- Consider Makefile for common commands
- Commit all changes since PR #4


---
**Context compaction (auto) at 12:41**
Check git log and docs/quality_reports/plans/ for current state.
