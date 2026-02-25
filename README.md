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
│   │       └── _experimental/       # exploration code, not yet in pipeline
│   │           └── __init__.py
│   │
│   ├── scripts/                     # ORCHESTRATES → file I/O
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
├── exploration/                     # EXPLORES → notebooks, messy is fine
│   └── archive/                     # abandoned code and explorations
│
├── output/
│   ├── tables/                      # rebuilt by scripts
│   └── figures/                     # rebuilt by scripts
│
├── paper/
│   ├── main.tex
│   └── references.bib               # includes data citations
│
├── README.md
└── .gitignore
```
