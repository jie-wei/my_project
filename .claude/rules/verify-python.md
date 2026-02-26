---
paths:
  - "code/**/*.py"
---

# Python Verification Agent

**Orchestrator Step 2 (VERIFY)** — Verifies Python files compile, run, and follow project conventions.

This rule activates during the orchestrator's VERIFY step when the task involves Python files. It operationalizes the checks defined in `verification-protocol.md` into a focused, structured protocol.

---

## When This Rule Activates

- After implementing changes to any `.py` file in `code/`
- During Step 2 (VERIFY) of the orchestrator loop
- Applies to modules, scripts, and exploration code

---

## Protocol

### 1. Classify the File

Determine the file type to select the right verification path:

| Path Pattern | Type | Verification Level |
|-------------|------|-------------------|
| `code/src/mypackage/core/*.py` | MODULE | Full (80/100) |
| `code/scripts/core/*.py` | SCRIPT | Full (80/100) |
| `code/src/mypackage/exploration/**/*.py` | EXPLORATION | Light (60/100) |
| `code/scripts/exploration/**/*.py` | EXPLORATION | Light (60/100) |
| `code/tests/**/*.py` | TEST | N/A (tests verify other code) |

### 2. Execute Verification Checks

#### For MODULE files (`code/src/mypackage/core/`):

1. **IMPORT check:** `python3 -c "from mypackage.core.MODULE import ..."` — imports clean, no syntax errors
2. **TESTS:** `pytest code/tests/ -x` — existing tests pass (if tests exist for this module)
3. **CONVENTIONS:**
   - No file I/O (open, read, write, pathlib operations) — belongs in scripts/
   - No hardcoded absolute paths (`/Users/...`, `../data/`)
   - Paths imported from `config.py`, not defined locally
   - Functions take data in, return data out (pure logic)

#### For SCRIPT files (`code/scripts/core/`):

1. **EXECUTION:** `python3 code/scripts/core/NN_name.py` — runs without error
2. **OUTPUT_FILES:** Check expected output files exist and have non-zero size
3. **CONVENTIONS:**
   - Does not modify `data/raw/` (sacred)
   - Imports from `src/mypackage/`, not copy-pasted logic
   - Seed set if stochastic operations present
   - Script follows `NN_` numbering convention

#### For EXPLORATION files:

1. **IMPORT or EXECUTION:** Code runs without syntax/import errors
2. **CONVENTIONS (light):**
   - Does not modify `data/raw/`
   - Seed set if stochastic (warning only, not blocking)

### 3. Report Results

Emit the structured output block, then provide a human-readable summary of any issues found.

---

## Structured Output

After verification, emit this block for orchestrator consumption:

```
--- VERIFY PYTHON RESULT ---
STATUS: PASS | FAIL
FILE_TYPE: MODULE | SCRIPT | EXPLORATION
TARGET: [file path]
CHECKS:
- IMPORT: PASS | FAIL | SKIP — [detail]
- TESTS: PASS | FAIL | SKIP — [detail]
- EXECUTION: PASS | FAIL | SKIP — [detail]
- CONVENTIONS: PASS | FAIL — [list of violations]
- OUTPUT_FILES: PASS | FAIL | SKIP — [detail]
BLOCKING_ISSUES: [N]
--- END VERIFY PYTHON RESULT ---
```

STATUS is FAIL if any check fails. SKIP means the check is not applicable for this file type (e.g., EXECUTION is skipped for modules, TESTS is skipped for scripts).

---

## Integration

- **Orchestrator step:** 2 (VERIFY)
- **Source of truth:** `verification-protocol.md` defines WHAT to check; this rule defines HOW to check it within the orchestrator loop
- **On FAIL:** Orchestrator loops back to fix, then re-verifies (max 2 retries per step)
- **On PASS:** Orchestrator proceeds to Step 3 (REVIEW)

---

## Important

- **Do not skip verification.** Every Python file change must pass before review.
- **Exploration gets lighter checks** but still must run without errors.
- **Test files are not verified by this rule** — they ARE the verification for modules.
- **If pytest fails, report which tests failed** and the error messages, not just "FAIL".
- **Convention violations are blocking** for core files (MODULE, SCRIPT) but advisory for EXPLORATION.
