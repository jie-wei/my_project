---
paths:
  - "code/src/mypackage/exploration/**"
  - "code/scripts/exploration/**"
---

# Exploration Fast-Track

**Lightweight workflow for experimental work.** Quality threshold: 60/100 (vs 80 for production). No planning needed.

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
