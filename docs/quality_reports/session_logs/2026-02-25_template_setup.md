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

### Still TODO
- Add example files (sample script, function, test)
- Consider Makefile for common commands
- Commit all changes since PR #4
