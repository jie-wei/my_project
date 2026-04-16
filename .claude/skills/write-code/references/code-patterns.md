# Code Patterns Reference

## Config.py

All paths live in `code/src/mypackage/config.py`. Never hardcode paths in scripts or modules.

### Existing general paths

These are already defined — don't duplicate or modify them:

```python
from pathlib import Path

def _find_root():
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    raise FileNotFoundError("Could not find project root")

ROOT = _find_root()

RAW = ROOT / "data" / "raw"
INTERMEDIATE = ROOT / "data" / "intermediate"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "output" / "core" / "tables"
FIGURES = ROOT / "output" / "core" / "figures"
EXPLORATION_OUTPUT = ROOT / "output" / "exploration"
```

### Adding variant-specific paths

Extend config.py by adding new constants below the existing ones:

```python
# {variant_name} paths
PROCESSED_{VARIANT_NAME} = ROOT / "data" / "processed" / "{variant_name}"
TABLES_{VARIANT_NAME} = ROOT / "output" / "{tier}" / "tables" / "{variant_name}"
FIGURES_{VARIANT_NAME} = ROOT / "output" / "{tier}" / "figures" / "{variant_name}"
```

**Naming convention:** `{CATEGORY}_{VARIANT_NAME}` in ALL_CAPS_SNAKE_CASE.

Examples:
- `PROCESSED_IV_APPROACH = ROOT / "data" / "processed" / "iv_approach"`
- `TABLES_IV_APPROACH = ROOT / "output" / "exploration" / "tables" / "iv_approach"`
- `FIGURES_IV_APPROACH = ROOT / "output" / "exploration" / "figures" / "iv_approach"`

Rules:
- Use simple `Path` joins (`/` operator) — no string formatting or f-strings
- One constant per path — don't build paths dynamically at import time
- Group related constants together with a comment header

---

## src/ Module Pattern

Functions in `code/src/mypackage/` are pure logic — no file system interaction.

```python
"""Short description of what this module does."""

import numpy as np
import pandas as pd


def compute_hhi(shares: pd.Series) -> float:
    """Compute Herfindahl-Hirschman Index from market shares.

    Args:
        shares: Market shares (should sum to ~1.0).

    Returns:
        HHI value between 0 and 1.
    """
    return (shares**2).sum()


def winsorize(series: pd.Series, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
    """Winsorize a series at given quantiles.

    Args:
        series: Data to winsorize.
        lower: Lower quantile cutoff.
        upper: Upper quantile cutoff.

    Returns:
        Winsorized series.
    """
    bounds = series.quantile([lower, upper])
    return series.clip(lower=bounds.iloc[0], upper=bounds.iloc[1])
```

Key rules:
- No `open()`, no `Path()`, no `print()`, no `plt.show()`
- Type hints on all public functions
- Docstrings with Args/Returns on public functions
- Seed passed as parameter, not set globally: `def bootstrap(data, n=1000, seed=42)`
- Private helpers prefixed with `_`

---

## Script Pattern

Scripts in `code/scripts/` handle I/O — reading files, calling src/ functions, saving results.

```python
"""
Descriptive Title

Purpose: What this script does
Inputs: Data files (use config.py path names)
Outputs: Figures, tables, processed data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mypackage.config import RAW, PROCESSED_{VARIANT_NAME}, TABLES_{VARIANT_NAME}, FIGURES_{VARIANT_NAME}
from mypackage.{tier}.{variant_name}.module import function_name

# -- Parameters ---------------------------------------------------------------
SEED = 42
np.random.seed(SEED)

# -- Data Loading --------------------------------------------------------------
df = pd.read_csv(RAW / "dataset.csv")

# -- Analysis ------------------------------------------------------------------
result = function_name(df)

# -- Save Outputs --------------------------------------------------------------
TABLES_{VARIANT_NAME}.mkdir(parents=True, exist_ok=True)
FIGURES_{VARIANT_NAME}.mkdir(parents=True, exist_ok=True)

# Tables: .tex + .csv
result.to_csv(TABLES_{VARIANT_NAME} / "summary.csv", index=False)
# For .tex tables, see regression-rpy2.md or use df.to_latex()

# Figures: .pdf + .png
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(result["x"], result["y"])
ax.set_xlabel("X variable")
ax.set_ylabel("Y variable")
for ext in (".pdf", ".png"):
    fig.savefig(FIGURES_{VARIANT_NAME} / f"main_plot{ext}", dpi=300, bbox_inches="tight")
plt.close(fig)
```

Key rules:
- All imports at top — stdlib/third-party first, then config paths, then src/ functions
- Parameters as module-level constants (SEED, sample restrictions, etc.)
- `DIR.mkdir(parents=True, exist_ok=True)` before saving
- Figures always saved as both `.pdf` and `.png`
- Tables saved as `.tex` (LaTeX-importable) and `.csv`
- Close figures after saving: `plt.close(fig)`
- No function definitions that belong in src/ — if logic is reusable, put it there

---

## Test Pattern

Tests live in `code/tests/` and test only src/ functions.

```python
import pytest
import numpy as np
import pandas as pd

from mypackage.{tier}.{variant_name}.module import function_name


@pytest.fixture
def sample_data():
    """Small fake dataset for testing."""
    return pd.DataFrame({
        "firm_id": [1, 2, 3, 4],
        "share": [0.4, 0.3, 0.2, 0.1],
        "revenue": [100, 200, 150, 50],
    })


class TestFunctionName:
    def test_basic(self, sample_data):
        result = function_name(sample_data)
        assert result == pytest.approx(0.3, abs=1e-6)

    def test_empty_input(self):
        df = pd.DataFrame({"share": []})
        result = function_name(df)
        assert result == 0.0

    def test_single_firm(self):
        df = pd.DataFrame({"share": [1.0]})
        result = function_name(df)
        assert result == pytest.approx(1.0)

    def test_reproducible(self, sample_data):
        r1 = function_name(sample_data, seed=42)
        r2 = function_name(sample_data, seed=42)
        assert r1 == r2
```

Key rules:
- Use `pytest.fixture` for shared test data
- Class-based grouping by function
- `pytest.approx()` for all float comparisons
- Fake data only — never load real files
- Test edge cases: empty, single row, missing values, boundary conditions
- Test reproducibility if function involves randomness
- Run with: `cd code && uv run pytest tests/test_{variant_name}.py -v`
