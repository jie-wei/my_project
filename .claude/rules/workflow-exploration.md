---
paths:
  - "**/exploration/**"
  - "**/archive/**"
---

# Exploration Workflow

**All experimental work starts in `exploration/` folders.** Never directly into `core/` production folders. Quality threshold: 60/100 (vs 80 for production). No planning needed.

## Steps

1. **Research value check** — Does this help answer a research question or test an idea? If NO, don't build it.
2. **Pick a name** — short, descriptive, snake_case (e.g., `iv_approach`, `bootstrap_se`, `did_event_study`)
3. **Create named subfolder** across the layers you need:
   - Pure logic → `code/src/mypackage/exploration/[name]/`
   - Scripts/notebooks → `code/scripts/exploration/[name]/`
   - Outputs → `output/exploration/[name]/`
   - Notes → `docs/exploration/[name]/`
   - Only create layers you'll actually use.
4. **Code immediately** — no plan mode needed. Must-haves: code runs, results correct, goal documented in session log. Not needed: full tests, type hints, docstrings, numbered script prefixes.
5. **Log progress** — append to session log as you work (normal session logging rules apply)

## When to Stop (Kill Switch)

At any point: stop, ask user about archiving. No guilt — exploration is inherently uncertain.

## Tier Transitions (User-Initiated Only)

**User decides, never Claude.** Claude never promotes, archives, or suggests doing so. Only the user initiates tier transitions.

### Promote: `exploration/[name]/` → `core/`

Move across all layers:
- `code/src/mypackage/exploration/[name]/` → `code/src/mypackage/core/[name]/`
- `code/scripts/exploration/[name]/` → `code/scripts/core/[name]/` (add `NN_` prefix to scripts)
- `output/exploration/[name]/` → `output/core/[name]/`
- `docs/exploration/[name]/` → `docs/core/[name]/`

**Graduate checklist:**
- [ ] Quality score >= 80
- [ ] Tests added and passing
- [ ] Results replicate within tolerance
- [ ] Code follows project conventions (paths from config.py, pure logic in src/, I/O in scripts/)
- [ ] Approach documented in docs/core/

### Archive: `exploration/[name]/` → `archive/[name]/`

Move to `archive/` at the same level. Add brief note using `docs/templates/archive-readme.md`.

### Revive: `archive/[name]/` → `exploration/[name]/`

Move back to exploration to resume work.
