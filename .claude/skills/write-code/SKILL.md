---
name: write-code
description: >-
  Python code implementation following project structure and conventions.
  Use this skill whenever the user asks to implement, write, create, build, add,
  modify, refactor, or extend Python code — including new functions, modules,
  scripts, or tests. Covers placing code in the right tier and folder, reusing
  existing functions, registering paths in config.py, writing tests, and
  producing LaTeX-ready output. Do NOT use for pure data analysis questions
  (use /analyze-data instead). This skill is about building and modifying
  reusable code components.
disable-model-invocation: true
argument-hint: "[what to implement, e.g. 'add a function to compute HHI from firm-level data']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Write Code

Implement Python code (with optional R via rpy2 for regressions) following project conventions.

**Input:** `$ARGUMENTS` — what to implement (e.g., "write a function that computes Herfindahl index from firm-level shares", "add a script that runs IV regressions with county fixed effects", "refactor the cleaning pipeline to handle missing zip codes").

---

## Complexity Check

Before diving in, assess the task scope:

- **Trivial** (single function, clear placement): proceed directly to Step 1.
- **Non-trivial** (multi-file, unclear scope, design choices): enter plan mode first. Ask the user questions in plain text to resolve ambiguity before coding.

Things worth asking about:
- Which tier (core vs exploration) if not obvious from context
- Variable-to-label mappings for regression tables (no obvious default — ask)
- Whether to extend an existing module or create a new one
- Which fixed effects, clustering, or sample restrictions to use

Never use AskUserQuestion — always ask in plain text within your response.

---

## Step 1: Classify & Survey

**Classify the task:**

1. **Tier**: core / exploration / archive — check where the user is working (open files, recent edits, cwd). Default to exploration if unsure.
2. **Variant name**: snake_case approach name (e.g., `iv_approach`, `bootstrap_se`). This determines subfolder paths across all layers.

**Survey existing code — this is the most important step:**

Search `code/src/mypackage/` and `code/scripts/` for functions and patterns that already do what's needed. Use Grep and Glob to find:
- Functions with similar signatures or purposes
- Scripts that handle similar data loading, output saving, or plotting
- Existing config paths that might already cover what's needed

List what you can import or adapt vs what must be written fresh. The goal is to build on existing code, not reinvent it. If a function exists that does 80% of what's needed, extend it rather than writing a parallel version.

---

## Step 2: Set Up Folders & Paths

Read `references/folder-structure.md` for the full directory layout.

Check which folders and config.py paths already exist. Create only what's missing:
- Folders across layers (src/, scripts/, output/, etc.)
- Config.py constants for new variant-specific paths

**Output path convention:** Figures and tables go in separate subdirectories under `output/{tier}/`, not flat in a variant folder:
```
output/{tier}/figures/{variant_name}/   # .pdf + .png
output/{tier}/tables/{variant_name}/    # .tex + .csv
```
Register these in config.py as `FIGURES_{VARIANT_NAME}` and `TABLES_{VARIANT_NAME}`. Never save outputs directly into a flat `output/{tier}/{variant_name}/` folder.

Read `references/code-patterns.md` for the config.py extension pattern and all code conventions.

---

## Step 3: Write Code

Build on what you found in Step 1. Import existing functions first.

**src/ modules** (pure logic, no I/O):
- No `open()`, no `Path()`, no `print()`
- Functions take data in, return data out
- Type hints on public functions, docstrings with Args/Returns
- Seed passed as parameter when needed, not set globally

**scripts/** (I/O glue):
- Import paths from config.py, functions from src/
- Parameters as module-level constants (SEED, etc.)
- `DIR.mkdir(parents=True, exist_ok=True)` before saving
- Figures: save to `FIGURES_{VARIANT_NAME}` as `.pdf` + `.png`, `dpi=300, bbox_inches='tight'`
- Tables: save to `TABLES_{VARIANT_NAME}` as `.tex` (directly importable with `\input{}`) + `.csv` for quick viewing
- Never save outputs into a flat variant folder — always use the `figures/` and `tables/` subdirectories

**If regressions are needed:** read `references/regression-rpy2.md` for the rpy2 + fixest pattern.

---

## Step 4: Write Tests

Every new public function in `code/src/mypackage/` gets a test in `code/tests/`.

See `references/code-patterns.md` (Test Pattern section) for the full template with fixtures and examples.

Key conventions:
- Class-based, grouped by function
- Fake data only — never load real files in tests
- `pytest.approx()` for float comparisons
- Test edge cases: empty input, single row, missing values
- Test reproducibility if function uses randomness

---

## Step 5: Verify

1. **Run the code**: execute scripts, check outputs are created at expected paths
2. **Run tests**: `cd code && uv run pytest tests/test_{variant_name}.py -v`
3. **Run `/review-code`** on all new/modified files — report saves to `docs/quality_reports/reviews/{tier}/review-code-{variant_name}.md`
4. **Read the review report**: if issues are found, fix them and re-run `/review-code` until the report is clean
5. **Check quality gate**: 80/100 for core, 60/100 for exploration

---

## Checklist

Before finishing, confirm:

- [ ] All paths imported from config.py (no hardcoded paths)
- [ ] Pure logic in src/, I/O in scripts/
- [ ] Tests exist for new public src/ functions
- [ ] Seed set for any stochastic operations
- [ ] Output files saved to `output/{tier}/figures/{variant}/` and `output/{tier}/tables/{variant}/` (not flat)
- [ ] Figures saved as .pdf + .png
- [ ] Tables saved as .tex (LaTeX-importable) + .csv
- [ ] data/raw/ not modified
- [ ] No dead code or commented-out alternatives
- [ ] Existing functions reused where possible

---

## Principles

**Why reuse matters.** Every function written is a function to maintain. Before writing new code, spend a minute searching for existing implementations. A slightly imperfect existing function that you can extend is better than a pristine new function that duplicates logic. This keeps the codebase coherent and reduces the surface area for bugs.

**Why structure matters.** The src/scripts split exists because pure logic is testable and reusable, while I/O glue is not. When logic lives in scripts, it can't be imported elsewhere and can't be tested without touching the filesystem. Keeping them separate makes the codebase composable.

**Why config.py matters.** Hardcoded paths break when the project moves, when someone else clones it, or when you reorganize. Config.py is the single source of truth for where things live. It takes 30 seconds to add a path there and saves hours of debugging later.

**When to ask vs when to decide.** If there's a clear convention (naming, placement, format), follow it without asking. If there's genuine ambiguity that affects the user's research (which specification to run, what labels to use, which sample to restrict to), ask in plain text. The cost of asking is low; the cost of guessing wrong on a research decision is high.
