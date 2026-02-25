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
│   ├── decisions.md                  # why you made each research choice
│   ├── design_notes.md
│   └── quality_reports/              # session quality tracking
│       ├── quality_score.py          # scoring script
│       └── session_logs/             # per-session logs
│           └── log_reminder.py       # hook: reminds to log sessions
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
