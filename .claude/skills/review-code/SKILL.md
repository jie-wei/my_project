---
name: review-code
description: Python code review for academic research. Checks quality, reproducibility, convention compliance, and test coverage. Use after writing or modifying Python scripts or modules in any tier (core, exploration, archive).
disable-model-invocation: false
argument-hint: "[file path or 'all' for changed .py files]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Python Code Review

Review Python modules and scripts for quality, reproducibility, and convention compliance. Produce a thorough, actionable report — never edit source files.

Standards: production-grade data pipeline + published replication package rigor.

**Input:** `$ARGUMENTS` — a file path (`code/src/mypackage/core/utils.py`), a directory, or `all` for recently changed `.py` files.

---

## Steps

1. **Read the target file(s)** end-to-end.
2. **Classify each file:** module (`code/src/mypackage/{tier}/`), script (`code/scripts/{tier}/`), or test (`code/tests/`). The tier (core / exploration / archive) determines the score threshold, not which checks apply.
3. **Check every category** below systematically.
4. **Score** using the rubric from `standalone-quality.md` (auto-loaded for `.py` files).
5. **Save the report** — see Output Location.
6. **Present summary** to the user.

---

## Review Categories

### 1. Module Structure (all tiers)

Applies to all files in `code/src/mypackage/` — whether `core/`, `exploration/{variant_name}/`, or `archive/{variant_name}/`.

- Pure logic — no file I/O (open, read, write, pathlib operations)
- Functions take data in, return data out
- No side effects (printing, logging to file, modifying global state)
- Clean imports at top of file
- `__all__` defined if module exports specific names

**Critical flag:** Any file I/O in src/ (-30 deduction).

### 2. Script Structure (all tiers)

Applies to all files in `code/scripts/` — whether `core/` (numbered scripts), `exploration/{variant_name}/`, or `archive/{variant_name}/`.

- Core scripts: numbered prefix (`01_clean.py`, `02_merge.py`, etc.)
- Exploration/archive scripts: named subfolder (`code/scripts/{tier}/{variant_name}/`)
- Clear sections: imports, setup, main logic, output
- Imports from `src/mypackage/` — not copy-pasted logic
- Script can be run standalone

**Flag:** Missing NN_ prefix (core), copy-pasted logic from src/.

### 3. Reproducibility

- Seed set at top for stochastic code
- All packages imported at top
- All paths relative to repository root
- Paths imported from `config.py` — never hardcoded
- Script produces identical output on re-run

**Critical flag:** Hardcoded absolute paths (-20), missing seed for stochastic work (-10).

### 4. Function Design

- `snake_case` naming for functions and variables
- Verb-noun pattern for functions (e.g., `compute_effect`, `load_data`)
- Type hints on public API functions
- Docstrings on public functions (what it does, params, returns)
- No magic numbers — use named constants or parameters
- Return values are well-structured (dicts, dataclasses, named tuples)

### 5. Domain Correctness

- Implementation matches the methodology described in the paper
- Statistical methods are appropriate for the data
- Results are substantively meaningful (not just statistically significant)
- Edge cases handled (empty data, missing values, division by zero)

**Flag:** Implementation doesn't match theory, wrong statistical method, unhandled edge cases.

### 6. Data Handling & I/O Tracing

- `data/raw/` is NEVER modified
- Data flows: raw/ -> scripts -> intermediate/ -> scripts -> processed/ -> scripts -> output/
- Intermediate data written to `data/intermediate/`
- Processed data written to `data/processed/{variant_name}/`
- Output files written to `output/{tier}/tables/{variant_name}/` and `output/{tier}/figures/{variant_name}/`

**Trace the I/O chain for each script.** For every script in the variant, verify: what does it read, what does it write, and do those paths match the variant's expected data pipeline? A script that reads from the wrong input or writes to the wrong output directory is a silent correctness bug — the code runs fine but produces results in the wrong place or from the wrong data.

**Critical flag:** Any modification to data/raw/ (-30). Script reads/writes to wrong variant paths (-10).

### 7. Test Coverage (modules only)

- Every new public function has at least one test
- Tests use synthetic/fake data (not real data files)
- Tests in `code/tests/` directory
- Edge cases tested (empty input, boundary values)
- Tests are independent and can run in any order

**Flag:** Missing tests for new public functions (-10).

### 8. Path Conventions

- All paths imported from `code/src/mypackage/config.py`
- No hardcoded absolute paths (`/Users/...`, `C:\...`)
- No relative paths with `..` that break when cwd changes
- `config.py` is the single source of truth for all paths
- Variant-specific paths follow the pattern: `TABLES_{VARIANT_NAME}`, `FIGURES_{VARIANT_NAME}`, `PROCESSED_{VARIANT_NAME}`

### 9. Error Handling

- Missing values handled explicitly (not silently dropped)
- Division by zero guarded where relevant
- File operations wrapped in try/except or existence checks
- Meaningful error messages that help debugging

**Flag:** Silent data loss, unguarded division, cryptic error messages.

### 10. Output Format Conventions

Scripts that produce outputs should save in paired formats:

- **Tables:** `.tex` (directly importable with `\input{}` in LaTeX) + `.csv` (for quick inspection)
- **Figures:** `.pdf` (for LaTeX inclusion) + `.png` (for quick viewing), saved with `dpi=300, bbox_inches='tight'`
- Output directories created with `DIR.mkdir(parents=True, exist_ok=True)` before saving
- Figures closed after saving: `plt.close(fig)`

**Flag:** Missing format pair (-5), missing `mkdir` before save (-3).

### 11. Professional Polish

- PEP 8 compliant (consistent indentation, spacing, line length)
- No dead code (commented-out blocks, unused imports)
- Comments explain WHY, not WHAT
- Consistent style throughout the file

---

## Scoring

Start at 100, apply deductions per `standalone-quality.md`. Quick reference:

**Module rubric** (threshold 80 for core, 60 for exploration/archive):
- File I/O in src/ (-30), hardcoded paths (-20), missing tests (-10), naming (-3), type hints (-2)

**Script rubric** (threshold 80 for core, 60 for exploration/archive):
- Modifies raw/ (-30), hardcoded paths (-20), missing seed (-10), no prefix (-3), missing output format pair (-5)

**Exploration rubric** (threshold 60):
- Syntax error (-100), modifies raw/ (-30), doesn't run (-15), missing seed (-10), hardcoded paths (-5)

---

## Structured Output

After review, emit this block for agent consumption:

```
--- PYTHON REVIEW RESULT ---
STATUS: CLEAN | ISSUES_FOUND
SCORE: [N]/100
THRESHOLD: [80 or 60]
PASS: YES | NO
FILE_TYPE: MODULE | SCRIPT | EXPLORATION
TARGET: [file path]

ISSUES:
- ID: PY001
  FILE: [path]
  LINE: [N]
  CATEGORY: STRUCTURE | REPRODUCIBILITY | FUNCTIONS | DOMAIN | DATA | TESTS | PATHS | ERRORS | OUTPUT_FORMAT | POLISH
  SEVERITY: CRITICAL | MAJOR | MINOR
  DEDUCTION: [N]
  CURRENT: "[code snippet]"
  PROPOSED: "[fix]"
  REASON: "[why this matters]"

- ID: PY002
  ...
--- END PYTHON REVIEW RESULT ---
```

---

## Output Location

Save to `docs/quality_reports/reviews/{tier}/review-code-{variant_name}.md`. Create the directory if it does not exist. The report replaces the previous one on re-run — no date suffix.

---

## Important

- **NEVER edit source files.** Only produce the report.
- **Verify every claim you write.** For every number, line reference, or code snippet in the report, confirm it matches the actual source file. Do NOT trust your own reading — treat each claim as something to double-check before writing it down.
- **Be specific.** Include line numbers and exact code snippets for every issue.
- **Be actionable.** Every issue must have a concrete proposed fix.
- **Prioritize correctness.** Domain bugs and data handling matter more than style.
- **Apply the RIGHT rubric.** The tier determines the threshold (80 for core, 60 for exploration/archive). The structural checks (pure logic in src/, I/O in scripts/) apply equally to all tiers.
- **Handle empty stubs gracefully.** If the target file is empty, report "File is empty — nothing to review."
