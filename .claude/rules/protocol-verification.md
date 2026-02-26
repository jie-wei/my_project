---
paths:
  - "code/**/*.py"
  - "paper/**/*.tex"
  - "output/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

## For Python Modules (`code/src/mypackage/core/*.py`):
1. `python3 -c "from mypackage.core.MODULE import ..."` -- imports clean
2. `pytest code/tests/ -x` -- tests pass (if tests exist for this module)
3. Convention check: no file I/O, no hardcoded paths, paths from config.py

## For Python Scripts (`code/scripts/core/*.py`):
1. `python3 code/scripts/core/NN_name.py` -- runs without error
2. Check output files exist and have non-zero size
3. Spot-check: data shape, column names, value ranges are reasonable
4. If stochastic: verify seed is set

## For LaTeX Manuscripts (`paper/*.tex`):
1. Compile: `cd paper && latexmk -xelatex main.tex` (or `xelatex main.tex` x2 + `bibtex main` + `xelatex main.tex`)
2. Verify PDF created: `ls -la paper/main.pdf`
3. Check for overfull hbox warnings: grep compilation log
4. Check for undefined citations: `grep "undefined" paper/main.log`
5. Open PDF if visual check needed: `open paper/main.pdf`

## For Data Pipeline (end-to-end):
1. Run scripts in numbered order: `python3 code/scripts/core/01_*.py`, then `02_*.py`, etc.
2. Verify `data/intermediate/` is populated after early scripts
3. Verify `data/processed/` is populated after later scripts
4. Verify `output/core/` has expected files (tables, figures)
5. Spot-check final outputs for reasonable values

## Common Pitfalls

- **Hardcoded paths** -- always use config.py; never `/Users/...` or `../data/`
- **File I/O in src/** -- if a function reads/writes files, it belongs in scripts/
- **Stale intermediate data** -- when in doubt, rerun pipeline from script 01
- **Missing seeds** -- stochastic results are unreproducible without explicit seeds
- **data/raw/ modification** -- NEVER modify raw data; copy to intermediate/ first

## Verification Checklist

```
[ ] Output file(s) created successfully
[ ] No compilation/execution errors
[ ] Tests pass (for src/ modules)
[ ] Paths resolve correctly (imported from config.py)
[ ] Spot-checked output values for reasonableness
[ ] Reported results to user
```
