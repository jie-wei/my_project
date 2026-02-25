# Research Project Infrastructure for Economics

A guide to organizing Python-based economics research projects. Designed for clean separation of logic and execution, and practical management of exploration.

---

## Getting Started

1. Clone the template and rename to your project.
2. Rename `code/src/mypackage/` to your project name. Update `name` in `pyproject.toml` to match.
3. Set up the environment:
   ```bash
   cd code
   uv venv --python 3.12
   source .venv/bin/activate
   uv pip install -e .
   ```
4. Place raw data in `data/raw/`. Never modify these files.
5. Write pure logic in `src/` → functions that take data in and return data out, no file paths.
6. Write scripts in `scripts/` → each script reads data, calls `src/` functions, and saves results. Number them in order: `01_clean.py`, `02_merge.py`, `03_estimate.py`, etc.
7. Write tests in `tests/` to verify `src/` logic with fake data.
8. Use `exploration/` notebooks to try ideas. Always import from `src/`, never copy-paste.
9. Record every research decision in `docs/decisions.md`.

### Data Flow

```
data/raw/ → scripts → data/intermediate/ → scripts → data/processed/ → scripts → output/
  sacred    (calls src/)    rebuilt          (calls src/)    rebuilt        (calls src/)  rebuilt
```
