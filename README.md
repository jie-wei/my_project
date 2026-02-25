# Project Structure

```
my-project/
├── code/                            # Engine → all code lives here
│   ├── pyproject.toml               # Dependencies + makes src/ installable
│   │
│   ├── src/                         # THINKS → pure logic, no file I/O
│   │   └── mypackage/               # importable package (named per project)
│   │       ├── __init__.py
│   │       ├── config.py            # All file paths, one place
│   │       ├── core/                # production logic
│   │       │   └── __init__.py
│   │       └── exploration/         # exploration code, not yet in pipeline
│   │           └── __init__.py
│   │
│   ├── scripts/                     # ORCHESTRATES → file I/O
│   │   ├── core/                    # numbered pipeline scripts
│   │   └── exploration/             # notebooks, ad-hoc analysis
│   │       └── archive/             # abandoned explorations
│   │
│   └── tests/                       # VERIFIES → tests src/ logic
│
├── data/
│   ├── raw/                         # sacred → never modify
│   ├── intermediate/                # rebuilt from raw via scripts
│   ├── processed/                   # results by specification
│   └── codebook.md                  # variable descriptions
│
├── docs/
│   ├── design_notes.md
│   ├── core/                         # analysis notes for core pipeline
│   │   └── archive/
│   ├── exploration/                  # analysis notes for exploration
│   │   └── archive/
│   └── quality_reports/              # session quality tracking
│       ├── quality_score.py          # scoring script
│       └── session_logs/             # per-session logs
│
├── output/
│   ├── core/                        # pipeline outputs
│   │   ├── tables/                  # rebuilt by scripts
│   │   └── figures/                 # rebuilt by scripts
│   └── exploration/                 # exploration outputs
│
├── paper/
│   ├── main.tex
│   └── references.bib               # includes data citations
│
├── README.md
└── .gitignore
```

## Getting Started

1. **Install [uv](https://docs.astral.sh/uv/)** (Python package manager):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create a virtual environment** and install dependencies:

   ```bash
   cd code
   uv venv --python 3.12
   source .venv/bin/activate      # macOS/Linux
   uv pip install -e ".[dev]"     # installs all deps + dev tools (pytest, ruff)
   ```

3. **Verify** the install:

   ```bash
   python -c "import mypackage; print('OK')"
   ```

## Using This Template

1. **Start a new project** — clone or fork, then rename the folder:

   ```bash
   git clone <this-repo-url> my-new-project
   ```

2. **Rename the package** — replace `mypackage` with your project name in three places:
   - Folder: `code/src/mypackage/` → `code/src/yourpackage/`
   - `code/pyproject.toml`: change `name = "mypackage"`
   - All imports: `from mypackage.config import ...` → `from yourpackage.config import ...`

3. **Edit dependencies** — add or remove packages in `code/pyproject.toml`, then re-run `uv pip install -e ".[dev]"`.

4. **Workflow**:
   - Place raw data in `data/raw/` (never modify it after)
   - Write pure logic (no file I/O) in `code/src/yourpackage/core/`
   - Write pipeline scripts in `code/scripts/core/`, numbered in order (`01_clean.py`, `02_merge.py`, …)
   - Use `code/scripts/exploration/` for notebooks and ad-hoc analysis
   - All file paths live in `code/src/yourpackage/config.py`

5. **Promote exploration → core** — when an idea is ready for the pipeline, swap `exploration` → `core` in the path, refactor, and add tests.
