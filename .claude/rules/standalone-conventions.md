# Project Conventions

## Code Organization

- Pure logic in `code/src/mypackage/core/` — no file I/O, no paths. Functions take data in, return data out.
- File I/O in `code/scripts/core/` — read files, call `src/` functions, save results. Number scripts in order (`01_clean.py`, `02_merge.py`, etc.).
- All paths defined in `code/src/mypackage/config.py` — import from there, never hardcode paths.
- Tests in `code/tests/` — test `src/` logic with fake data.
- Litmus test: needs the file system? → `scripts/`. No? → `src/`.

## Data

- `data/raw/` is sacred — never modify raw data.
- `data/intermediate/` and `data/processed/` are rebuilt by scripts.
- Data flow: `raw/ → scripts → intermediate/ → scripts → processed/ → scripts → output/core/`
- Exploration outputs go in `output/exploration/`.

## Three-Tier Structure (core / exploration / archive)

- The project uses three parallel tiers across four layers:
  - `code/src/mypackage/{core, exploration, archive}/` — pure logic
  - `code/scripts/{core, exploration, archive}/` — file I/O scripts and notebooks
  - `output/{core, exploration, archive}/` — generated outputs
  - `docs/{core, exploration, archive}/` — analysis notes
- **Transitions** are just swapping the tier name in the path. User decides all tier transitions — Claude never promotes or archives on its own.
- Each exploration gets a **named subfolder** (e.g., `exploration/iv_approach/`) across the layers it uses.

## Exploration

- Notebooks go in `code/scripts/exploration/[name]/` — always import from `src/`, never copy-paste.
- Reusable exploration code goes in `code/src/mypackage/exploration/[name]/`.
- Analysis notes go in `docs/exploration/[name]/`.
- No dead code in `src/`. Move abandoned code to `archive/` or delete and let git history hold it.
- See `workflow-exploration.md` for workflow and tier transitions.

## Versions and Variations

- Only separate what's actually different. Shared logic stays in shared files.
- Use CLI arguments to select versions — never duplicate scripts.

## Generic vs Specific

- **Generic** (commit to repo): workflow patterns, templates, rules, skills that help all users
- **Specific** (keep local): machine paths, tool versions, personal preferences, API keys
- Litmus test: would a researcher in a different field benefit from this? Yes → commit. No → `.claude/state/personal-memory.md` (gitignored).

## LaTeX

- Always compile with `latexmk -xelatex` — never raw `xelatex`/`pdflatex`/`bibtex`. `latexmk` handles multi-pass compilation automatically.
- After `latexmk` finishes, delete auxiliary files (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, etc.) from the build directory.

## Environment

- Use `uv` for Python and dependency management.
