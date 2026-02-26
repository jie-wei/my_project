---
name: data-analysis
description: End-to-end Python data analysis workflow from exploration through modeling to publication-ready tables and figures
disable-model-invocation: true
argument-hint: "[dataset path or description of analysis goal]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Data Analysis Workflow

Run an end-to-end data analysis in Python: load, explore, analyze, and produce publication-ready output.

**Input:** `$ARGUMENTS` -- a dataset path (e.g., `data/raw/county_panel.csv`) or a description of the analysis goal (e.g., "regress wages on education with state fixed effects using CPS data").

---

## Constraints

- **Follow project conventions** in `.claude/rules/standalone-conventions.md`
- **Pure logic in `src/`, I/O in `scripts/`.** Functions that transform data go in `code/src/mypackage/`. Scripts that read files, call those functions, and save results go in `code/scripts/`.
- **All paths from `config.py`** -- import from `code/src/mypackage/config.py`, never hardcode.
- **Never modify `data/raw/`** -- it is sacred.
- **Save all outputs** (figures, tables, processed data) to appropriate `output/` directories.
- **Run reviewer-python** on generated code before presenting results.

---

## Workflow Phases

### Phase 1: Setup and Data Loading

1. Read `.claude/rules/standalone-conventions.md` and `.claude/rules/standalone-quality.md` for project standards.
2. Check `code/src/mypackage/config.py` for existing path definitions. Add new paths if needed.
3. Create script with proper header (see Script Structure below).
4. Load required packages at top.
5. Set seed once at top for any stochastic operations: `np.random.seed(42)` or `random.seed(42)`.
6. Load and inspect the dataset.

### Phase 2: Exploratory Data Analysis

Generate diagnostic outputs:
- **Summary statistics:** shape, dtypes, missingness rates, descriptive stats
- **Distributions:** histograms for key continuous variables
- **Relationships:** scatter plots, correlation matrices
- **Time patterns:** if panel data, plot trends over time
- **Group comparisons:** if treatment/control, compare pre-treatment means

Save diagnostic figures to `output/exploration/[name]/` or `output/core/diagnostics/`.

### Phase 3: Main Analysis

Based on the research question:
- **Regression analysis:** Use `statsmodels`, `linearmodels` (for panel/IV), or `scikit-learn` as appropriate
- **Standard errors:** Cluster at the appropriate level (document why)
- **Multiple specifications:** Start simple, progressively add controls
- **Effect sizes:** Report standardized effects alongside raw coefficients
- **Robustness checks:** Alternative samples, specifications, or estimators

### Phase 4: Publication-Ready Output

**Tables:**
- Use `stargazer` (Python port), `statsmodels.summary`, or manual formatting
- Include all standard elements: coefficients, SEs, significance stars, N, R-squared
- Export as `.tex` for LaTeX inclusion and `.csv` for quick viewing

**Figures:**
- Use `matplotlib` or `seaborn`
- Include proper axis labels (sentence case, units)
- Save with explicit dimensions and DPI: `fig.savefig(..., dpi=300, bbox_inches='tight')`
- Save as both `.pdf` (for LaTeX) and `.png` (for quick viewing)

### Phase 5: Save and Review

1. Save processed data to `data/intermediate/` or `data/processed/` as appropriate.
2. Save all figures and tables to `output/`.
3. Create output directories as needed with `os.makedirs(..., exist_ok=True)`.
4. Run the reviewer-python agent on generated code:

```
Delegate to the reviewer-python agent:
"Review the script at code/scripts/[tier]/[script_name].py"
```

5. Address any Critical or High issues from the review.

---

## Code Organization

Decide where code goes based on the src/scripts split:

**Goes in `code/src/mypackage/` (pure logic):**
- Data cleaning/transformation functions
- Statistical model specifications
- Table/figure formatting functions
- Anything reusable across scripts

**Goes in `code/scripts/` (I/O):**
- Loading data from disk
- Calling src/ functions with specific datasets
- Saving outputs to disk
- The orchestration script that ties it all together

For a quick exploration, it's fine to put everything in a single script under `code/scripts/exploration/[name]/`. For production analysis, split properly.

---

## Script Structure

Follow this template for scripts:

```python
"""
[Descriptive Title]

Purpose: [What this script does]
Inputs: [Data files -- use config.py path names]
Outputs: [Figures, tables, processed data]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mypackage.config import RAW_DIR, PROCESSED_DIR, OUTPUT_DIR
# from mypackage.core.analysis import your_function  # if using src/ functions

# ── Setup ──────────────────────────────────────────
np.random.seed(42)

# ── Data Loading ───────────────────────────────────
# [Load and clean data]

# ── Exploratory Analysis ───────────────────────────
# [Summary stats, diagnostic plots]

# ── Main Analysis ──────────────────────────────────
# [Regressions, estimation]

# ── Tables and Figures ─────────────────────────────
# [Publication-ready output]

# ── Export ─────────────────────────────────────────
# [Save all outputs]
```

---

## Output Location

Determine the save paths:
1. Check if the analysis is part of an exploration (`exploration/[name]/`).
2. If YES:
   - Script: `code/scripts/exploration/[name]/`
   - Functions: `code/src/mypackage/exploration/[name]/`
   - Outputs: `output/exploration/[name]/`
   - Notes: `docs/exploration/[name]/`
3. If NO (production analysis):
   - Script: `code/scripts/core/NN_descriptive_name.py` (next number in sequence)
   - Functions: `code/src/mypackage/core/`
   - Outputs: `output/core/figures/`, `output/core/tables/`
   - Data: `data/intermediate/` or `data/processed/`
4. Create directories if they do not exist.

---

## Principles

- **Reproduce, don't guess.** If the user specifies an analysis, run exactly that.
- **Show your work.** Print summary statistics before jumping to modeling.
- **Check for issues.** Look for multicollinearity, outliers, missing data patterns, perfect prediction.
- **Use config.py paths.** All paths imported from config, never hardcoded.
- **No dead code.** Remove commented-out alternatives before finishing.
- **Explain choices.** If you pick a specific estimator or specification, say why in a code comment.
