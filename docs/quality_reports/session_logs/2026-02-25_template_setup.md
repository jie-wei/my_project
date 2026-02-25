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


---
**Context compaction (auto) at 14:26**
Check git log and docs/quality_reports/plans/ for current state.

---
### Session 2: Cluster B-rest Planning (in progress)

**Goal:** Add orchestrator-protocol, quality-gates, verification-protocol to complete the plan→execute→verify→score loop. Adapted from pedrohcgs/claude-code-my-workflow.

**Key decisions made so far:**
1. Step 3 (REVIEW) says "by file type" not agent names — matches original's pattern, agents slot in later via Cluster C
2. verify-reminder.py unchanged — hook nudges, verification-protocol is formal methodology
3. Exploration scoring deferred to Cluster D — matches original's separation
4. Adding workflow-quick-ref.md to `.claude/rules/` — splits behavioral guidance out of CLAUDE.md (original puts it at `.claude/` but rules/ auto-loads)
5. Adding orchestrator-research.md — simplified 3-step loop, prepares for Cluster C agent split
6. Adding latex-cleanup.py hook — PostToolUse on Bash, auto-deletes .aux/.log/.bbl etc. after compilation
7. Tolerance thresholds are `<!-- Customize -->` templates — per-project economics calibration

**Plan file:** `/Users/weijie/.claude/plans/lovely-skipping-widget.md`
**Status:** IMPLEMENTED

**Files created:**
- `.claude/rules/orchestrator-protocol.md` — 6-step loop (implement→verify→review→fix→re-verify→score)
- `.claude/rules/orchestrator-research.md` — simplified 3-step loop for scripts, scoped to `code/scripts/**/*.py`
- `.claude/rules/quality-gates.md` — deduction rubrics for Python modules, scripts, LaTeX
- `.claude/rules/verification-protocol.md` — verification procedures per file type
- `.claude/rules/workflow-quick-ref.md` — contractor model, ask-vs-execute, non-negotiables
- `.claude/hooks/latex-cleanup.py` — auto-deletes LaTeX auxiliary files after compilation

**Files edited:**
- `.claude/rules/plan-first-workflow.md` — step 8 links to orchestrator
- `CLAUDE.md` — 5 new rules in Rules Reference, latex-cleanup in Hooks
- `.claude/settings.json` — wired latex-cleanup.py

**Verification:** All cross-references valid, settings.json valid JSON, hook syntax OK, 8 rules + 8 hooks total


---
**Context compaction (auto) at 15:58**
Check git log and docs/quality_reports/plans/ for current state.

---
### Session 3: Workflow Enforcement Gaps

**Goal:** Investigate why `docs/quality_reports/plans/` and `docs/quality_reports/merges/` are empty, compare with original, and fix.

**Findings:**
- Both plan saving and quality report generation are instruction-based in the original — no automation
- The original has the same gaps: rules say "save plan" and "generate report at merge," but nothing enforces it
- The `/commit` skill (both ours and original) doesn't include quality report generation
- `plan-first-workflow.md` rule is always loaded and says "save to disk" as step 4, but Claude didn't follow it
- Key insight: when skill gives explicit step-by-step instructions, Claude follows those steps; background rules get overlooked

**Fix #1 — Quality reports (done):**
- Added step 7 to `/commit` skill: generate quality report after merge using template, score files, save to `docs/quality_reports/merges/`, commit to main
- Added `Write` to skill's allowed-tools

**Fix #2 — Plan saving (in discussion):**
- No `ExitPlanMode` hook event exists — can't hook into plan mode transitions
- Claude Code auto-creates plans at `~/.claude/plans/` when in plan mode — plans always exist there
- Our pre-compact hook searches `docs/quality_reports/plans/` (project folder), not `~/.claude/plans/`
- Discussing: is the real problem that Claude doesn't enter plan mode, or that hooks look in the wrong place?
