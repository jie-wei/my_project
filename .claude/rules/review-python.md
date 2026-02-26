---
paths:
  - "code/**/*.py"
---

# Python Quality Review Agent

**Orchestrator Step 3 (REVIEW)** — Scores Python files against quality rubrics with itemized deductions.

This rule activates during the orchestrator's REVIEW step when the task involves Python files. It operationalizes the scoring rubrics defined in `quality-gates.md` into a structured scoring protocol.

---

## When This Rule Activates

- After Step 2 (VERIFY) passes for Python files
- During Step 3 (REVIEW) of the orchestrator loop
- Applies to modules, scripts, and exploration code

---

## Protocol

### 1. Classify the File

Same classification as `verify-python.md`:

| Path Pattern | Type | Threshold |
|-------------|------|-----------|
| `code/src/mypackage/core/*.py` | MODULE | 80/100 |
| `code/scripts/core/*.py` | SCRIPT | 80/100 |
| `code/src/mypackage/exploration/**/*.py` | EXPLORATION | 60/100 |
| `code/scripts/exploration/**/*.py` | EXPLORATION | 60/100 |

### 2. Apply the Correct Rubric

Read the file and check each item. Start at 100 and apply deductions.

#### MODULE rubric (`code/src/mypackage/core/`):

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax or import error | -100 |
| Critical | File I/O in src/core/ (belongs in scripts/) | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing test for new public function | -10 |
| Major | Paths not imported from config.py | -10 |
| Minor | Inconsistent naming conventions | -3 |
| Minor | Missing type hints on public API | -2 |

#### SCRIPT rubric (`code/scripts/core/`):

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax error | -100 |
| Critical | Modifies data/raw/ | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing seed for stochastic work | -10 |
| Major | Expected output not created | -10 |
| Minor | Script not numbered (NN_ prefix) | -3 |

#### EXPLORATION rubric (60/100 threshold):

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax or import error | -100 |
| Critical | Modifies data/raw/ | -30 |
| Major | Code doesn't run | -15 |
| Major | Results not reproducible (missing seed) | -10 |
| Minor | Hardcoded absolute paths | -5 |

**No penalty for:** missing tests, missing type hints, missing docstrings, unnumbered scripts, inconsistent style.

### 3. Calculate Score

- Start at 100
- Apply each applicable deduction
- Floor at 0 (no negative scores)
- Compare to threshold (80 for core, 60 for exploration)

### 4. Determine Status

- **PASS:** Score >= threshold
- **FAIL:** Score < threshold

### 5. Report Results

Emit the structured output block with every deduction itemized, then provide a human-readable summary.

---

## Structured Output

After review, emit this block for orchestrator consumption:

```
--- REVIEW PYTHON RESULT ---
STATUS: PASS | FAIL
FILE_TYPE: MODULE | SCRIPT | EXPLORATION
TARGET: [file path]
SCORE: [N]/100
THRESHOLD: [80 or 60]

DEDUCTIONS:
- SEVERITY: CRITICAL | MAJOR | MINOR
  ISSUE: [description]
  DEDUCTION: -[N]
  LOCATION: [file:line]

SUMMARY: [1-2 sentence assessment]
--- END REVIEW PYTHON RESULT ---
```

If no deductions, the DEDUCTIONS section should say `(none)`.

---

## Integration

- **Orchestrator step:** 3 (REVIEW)
- **Source of truth:** `quality-gates.md` defines the rubrics; this rule applies them
- **On FAIL:** Orchestrator proceeds to Step 4 (FIX) to address issues by severity (critical first)
- **On PASS:** Orchestrator proceeds to Step 6 (SCORE) for final assessment
- **Threshold enforcement:** Score < 80 blocks commit for core files; score < 60 blocks for exploration

---

## Important

- **Be specific.** Every deduction must include the file, line number, and exact issue. "Code has problems" is not actionable.
- **Apply the RIGHT rubric.** Module rubric for src/core/, script rubric for scripts/core/, exploration rubric for exploration/. Using the wrong rubric produces wrong scores.
- **Do not invent deductions.** Only apply items listed in the rubric tables above. If something seems wrong but isn't in the rubric, note it in the SUMMARY but don't deduct points.
- **Critical issues are show-stoppers.** A single critical issue drops the score to 0 or below threshold. Flag them prominently.
