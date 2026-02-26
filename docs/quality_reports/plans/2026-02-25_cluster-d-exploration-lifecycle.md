# Plan: Cluster D — Exploration Lifecycle

**Status:** COMPLETED
**Date:** 2026-02-25

## Context

We have `core/` and `exploration/` folders across 4 layers (src, scripts, output, docs) but **no rules governing how exploration work flows**. The quality-gates rule already defers exploration scoring to this cluster. Without these rules, Claude treats exploration like production (requiring planning, 80/100 threshold), which kills the low-friction intent.

## What We're Building

Two new rules + updates to two existing files. Total: ~4 files touched.

### File 1: `.claude/rules/exploration-fast-track.md` (NEW)

Path-scoped to `code/src/mypackage/exploration/**` and `code/scripts/exploration/**`.

Content:
- **60/100 quality threshold** (vs. 80 for production)
- **No planning required** — skip plan mode for exploration work
- 5-step workflow: research value check → create files → code immediately → log progress → decide (promote / keep / archive)
- Kill switch: stop anytime, archive with brief note, no guilt
- Must-haves: code runs, results correct, goal documented
- Not needed: full tests, type hints, perfect style

### File 2: `.claude/rules/exploration-lifecycle.md` (NEW)

Path-scoped to `**/exploration/**`.

Content:
- **Lifecycle**: Create → Develop → Decide (promote, keep exploring, archive)
- **Promotion protocol**: swap `exploration/` → `core/` in path, refactor to project conventions, add tests, hit 80/100. Covers all 4 layers:
  - `src/mypackage/exploration/` → `src/mypackage/core/`
  - `scripts/exploration/` → `scripts/core/` (number the script)
  - `output/exploration/` → `output/core/`
  - `docs/exploration/` → `docs/core/`
- **Archive protocol**: move to `archive/` subfolder within the same exploration layer, with brief explanation
- **Graduate checklist**: quality >= 80, tests pass, results replicate, code clear, approach documented

### File 3: `.claude/rules/quality-gates.md` (EDIT)

Replace the placeholder at line 48 with exploration-specific scoring:

- **Exploration Python** (`code/src/mypackage/exploration/*.py`, `code/scripts/exploration/*.py`):
  - Critical: syntax/import error (-100), modifies data/raw/ (-30)
  - Major: code doesn't run (-15), results not reproducible (-10)
  - Minor deductions relaxed (no penalty for missing tests, type hints, numbering)
- **Threshold: 60/100** (not 80)

### File 4: `CLAUDE.md` (EDIT)

Add the two new rules to the Rules Reference section:
- `.claude/rules/exploration-fast-track.md` — lightweight workflow, 60/100 threshold
- `.claude/rules/exploration-lifecycle.md` — promotion, archiving, graduation checklist

## What We're NOT Building

- **No `ACTIVE_PROJECTS.md` tracker** — our distributed structure + session logs already track what's active.
- **No per-exploration SESSION_LOG.md** — our per-session logs already capture incremental work.
- **No exploration-specific templates** — can add later if needed.

## Verification

1. Check all path scoping is correct (rules fire only for exploration paths)
2. Confirm quality-gates.md exploration rubric is consistent with fast-track threshold
3. Verify CLAUDE.md rules reference lists both new rules
4. Cross-check with project-conventions.md — no contradictions
5. Review existing `archive/` .gitkeep files exist in exploration folders
