---
paths:
  - "**/exploration/**"
  - "**/archive/**"
---

# Exploration Lifecycle

**All experimental work starts in `exploration/` folders.** Never directly into `core/` production folders.

## Three-Tier Structure

Each layer has three parallel tiers:
```
{core, exploration, archive}/
```
Transitions are just swapping the tier name in the path.

## Lifecycle

1. **Create** — pick a name, create subfolder across needed layers (see exploration-fast-track.md)
2. **Develop** — work within exploration folders. Quality threshold: 60/100.
3. **Decide** — **user decides, never Claude.** Claude never promotes, archives, or suggests doing so. Only the user initiates tier transitions.

## Tier Transitions (User-Initiated Only)

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
