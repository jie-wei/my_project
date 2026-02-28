---
name: review-python
description: Python code review for academic research. Checks quality, reproducibility, convention compliance, and test coverage. Use after writing or modifying Python scripts or modules.
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
2. **Classify each file:** module (`code/src/mypackage/core/`), script (`code/scripts/core/`), or exploration.
3. **Check every category** below systematically.
4. **Score** using the rubric from `standalone-quality.md` (auto-loaded for `.py` files).
5. **Save the report** — see Output Location.
6. **Present summary** to the user.

---

## Review Categories

### 1. Module Structure (src/core/ only)

- Pure logic — no file I/O (open, read, write, pathlib operations)
- Functions take data in, return data out
- No side effects (printing, logging to file, modifying global state)
- Clean imports at top of file
- `__all__` defined if module exports specific names

**Critical flag:** Any file I/O in src/core/ (-30 deduction).

### 2. Script Structure (scripts/core/ only)

- Numbered prefix (`01_clean.py`, `02_merge.py`, etc.)
- Clear sections: imports, setup, main logic, output
- Imports from `src/mypackage/` — not copy-pasted logic
- Script can be run standalone: `python3 code/scripts/core/NN_name.py`

**Flag:** Missing NN_ prefix, copy-pasted logic from src/.

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

### 6. Data Handling

- `data/raw/` is NEVER modified
- Data flows: raw/ -> scripts -> intermediate/ -> scripts -> processed/ -> scripts -> output/
- Intermediate data written to `data/intermediate/`
- Processed data written to `data/processed/`
- Output files written to `output/core/` or `output/exploration/`

**Critical flag:** Any modification to data/raw/ (-30).

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

### 9. Error Handling

- Missing values handled explicitly (not silently dropped)
- Division by zero guarded where relevant
- File operations wrapped in try/except or existence checks
- Meaningful error messages that help debugging

**Flag:** Silent data loss, unguarded division, cryptic error messages.

### 10. Professional Polish

- PEP 8 compliant (consistent indentation, spacing, line length)
- No dead code (commented-out blocks, unused imports)
- Comments explain WHY, not WHAT
- Consistent style throughout the file

---

## Scoring

Start at 100, apply deductions per `standalone-quality.md`. Quick reference:

**Module rubric** (threshold 80):
- File I/O in src/ (-30), hardcoded paths (-20), missing tests (-10), naming (-3), type hints (-2)

**Script rubric** (threshold 80):
- Modifies raw/ (-30), hardcoded paths (-20), missing seed (-10), no prefix (-3)

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
  CATEGORY: STRUCTURE | REPRODUCIBILITY | FUNCTIONS | DOMAIN | DATA | TESTS | PATHS | ERRORS | POLISH
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

Determine the save path:
1. Check if recent context is inside `exploration/[name]/`.
2. If YES: save to `docs/exploration/[name]/python_review_[filename]_[date].md`.
3. If NO: save to `docs/quality_reports/reviews/[filename]_python_review.md`.
4. Create the directory if it does not exist.

---

## Important

- **NEVER edit source files.** Only produce the report.
- **Be specific.** Include line numbers and exact code snippets for every issue.
- **Be actionable.** Every issue must have a concrete proposed fix.
- **Prioritize correctness.** Domain bugs and data handling matter more than style.
- **Apply the RIGHT rubric.** Module vs script vs exploration — using the wrong one produces wrong scores.
- **Handle empty stubs gracefully.** If the target file is empty, report "File is empty — nothing to review."
