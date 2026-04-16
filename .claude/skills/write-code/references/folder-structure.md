# Folder Structure Reference

This project uses a three-tier structure (core / exploration / archive) mirrored across multiple layers. When implementing code for a variant, you may need to create folders across several of these layers.

## Code Layers

### src/ — pure logic

```
code/src/mypackage/{tier}/{variant_name}/
├── __init__.py
├── module_a.py
└── module_b.py
```

- Create `__init__.py` in every new package directory (even if empty)
- One module per logical unit (e.g., `cleaning.py`, `estimation.py`, `formatting.py`)
- No I/O — functions take data in, return data out

### scripts/ — I/O glue

**Core tier** — numbered scripts, flat:
```
code/scripts/core/NN_{descriptive_name}.py
```
- Check existing scripts to find the next number in sequence
- Numbers reflect execution order, not importance

**Exploration tier** — named subfolder:
```
code/scripts/exploration/{variant_name}/
├── run_analysis.py
└── explore_results.py
```

**Archive tier** — same as exploration:
```
code/scripts/archive/{variant_name}/
```

### tests/

```
code/tests/test_{variant_name}.py
```

- One test file per variant
- Test only src/ functions — scripts are verified by running them

## Data Layers

```
data/
├── raw/                           # Sacred — never modify
├── intermediate/                  # Shared across variants (commonly used cleaned data)
└── processed/{variant_name}/      # Variant-specific processed data
```

- `raw/` is read-only. Scripts read from it but never write to it.
- `intermediate/` holds data that multiple variants share (e.g., a cleaned panel used by several analyses).
- `processed/{variant_name}/` holds data specific to one variant's pipeline.

## Output Layers

```
output/{tier}/
├── tables/{variant_name}/    # .tex and .csv files
└── figures/{variant_name}/   # .pdf and .png files
```

- Tables: `.tex` files directly importable with `\input{}` in LaTeX, plus `.csv` for quick inspection
- Figures: `.pdf` for LaTeX inclusion, `.png` for quick viewing. Save with `dpi=300, bbox_inches='tight'`

## Documentation (optional)

```
docs/{tier}/{variant_name}/
```

- Analysis notes, methodology docs — create only if needed
- Not required for every variant

## Before Creating

Check what already exists:

1. **Glob for existing folders**: `code/src/mypackage/{tier}/`, `code/scripts/{tier}/`
2. **Read config.py**: check if paths for this variant are already registered
3. **Create only what's missing** — don't recreate existing directories or duplicate config paths

Use `os.makedirs(..., exist_ok=True)` in scripts to create output directories at runtime.
