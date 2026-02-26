---
paths:
  - "code/**/*.py"
  - "paper/**/*.tex"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for review
- **95/100 = Excellence** -- aspirational

## Python Modules (`code/src/mypackage/core/*.py`)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax or import error | -100 |
| Critical | File I/O in src/core/ (belongs in scripts/) | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing test for new public function | -10 |
| Major | Paths not imported from config.py | -10 |
| Minor | Inconsistent naming conventions | -3 |
| Minor | Missing type hints on public API | -2 |

## Python Scripts (`code/scripts/core/*.py`)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax error | -100 |
| Critical | Modifies data/raw/ | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing seed for stochastic work | -10 |
| Major | Expected output not created | -10 |
| Minor | Script not numbered (NN_ prefix) | -3 |

## LaTeX Manuscripts (`paper/*.tex`)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Compilation failure | -100 |
| Critical | Undefined citation | -15 |
| Critical | Overfull hbox > 10pt | -10 |
| Major | Typo in equation | -5 |
| Minor | Inconsistent notation across sections | -3 |

## Exploration Python (`code/src/mypackage/exploration/**`, `code/scripts/exploration/**`)

**Threshold: 60/100** (not 80). Exploration is intentionally low-friction.

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax or import error | -100 |
| Critical | Modifies data/raw/ | -30 |
| Major | Code doesn't run | -15 |
| Major | Results not reproducible (missing seed) | -10 |
| Minor | Hardcoded absolute paths | -5 |

**No penalty for:** missing tests, missing type hints, missing docstrings, unnumbered scripts, inconsistent style.

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Use `docs/templates/quality-report.md` for format.
Save to `docs/quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Tolerance Thresholds

<!-- Customize for your domain -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | <!-- e.g., 1e-6 --> | <!-- Numerical precision --> |
| Standard errors | <!-- e.g., 1e-4 --> | <!-- MC variability --> |
| p-values | <!-- e.g., +/- 0.005 --> | <!-- Significance boundary --> |
| Coverage rates | <!-- e.g., +/- 0.01 --> | <!-- MC with B reps --> |
