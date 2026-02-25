# Project Conventions

## Code Organization

- Pure logic in `code/src/mypackage/` — no file I/O, no paths. Functions take data in, return data out.
- File I/O in `code/scripts/` — read files, call `src/` functions, save results. Number scripts in order (`01_clean.py`, `02_merge.py`, etc.).
- All paths defined in `code/src/mypackage/config.py` — import from there, never hardcode paths.
- Tests in `code/tests/` — test `src/` logic with fake data.
- Litmus test: needs the file system? → `scripts/`. No? → `src/`.

## Data

- `data/raw/` is sacred — never modify raw data.
- `data/intermediate/` and `data/processed/` are rebuilt by scripts.
- Data flow: `raw/ → scripts → intermediate/ → scripts → processed/ → scripts → output/`

## Exploration

- Notebooks go in `exploration/` — always import from `src/`, never copy-paste.
- Reusable exploration code goes in `code/src/mypackage/_experimental/`. Promote to `src/` or delete.
- No dead code in `src/`. Move abandoned code to `_experimental/` or `exploration/archive/`. If fully abandoned, delete and let git history hold it.

## Versions and Variations

- Only separate what's actually different. Shared logic stays in shared files.
- Use CLI arguments to select versions — never duplicate scripts.

## Decisions

- Record every research decision in `docs/decisions.md`.

## Environment

- Use `uv` for Python and dependency management.
