# Economics Research Project Template

A project template for economics research with Claude Code integration. Includes a plan-first workflow, quality gates with scoring rubrics, automated verification, and session logging.

## Project Structure

```
my-project/
├── code/
│   ├── pyproject.toml               # Dependencies + makes src/ installable
│   ├── src/mypackage/               # Pure logic (no file I/O)
│   │   ├── __init__.py
│   │   ├── config.py                # All file paths, one place
│   │   ├── core/                    # Production logic
│   │   └── exploration/             # Experimental logic
│   ├── scripts/
│   │   ├── core/                    # Numbered pipeline scripts (01_clean.py, 02_merge.py, …)
│   │   └── exploration/             # Notebooks, ad-hoc analysis
│   │       └── archive/             # Abandoned explorations
│   └── tests/                       # Tests for src/ logic
│
├── data/
│   ├── raw/                         # Sacred — never modify
│   ├── intermediate/                # Rebuilt by scripts
│   ├── processed/                   # Rebuilt by scripts
│   └── codebook.md                  # Variable descriptions
│
├── docs/
│   ├── core/                        # Analysis notes (promoted)
│   ├── exploration/                 # Analysis notes (experimental)
│   ├── preambles/                   # LaTeX preamble files
│   ├── templates/                   # Reusable markdown templates
│   │   ├── session-log.md
│   │   ├── quality-report.md
│   │   ├── requirements-spec.md
│   │   ├── exploration-readme.md
│   │   └── archive-readme.md
│   └── quality_reports/
│       ├── plans/                   # Saved plans (survive compaction)
│       ├── session_logs/            # Per-session work logs
│       ├── merges/                  # Quality reports at merge time
│       └── specs/                   # Requirements specifications
│
├── output/
│   ├── core/                        # Pipeline outputs (tables, figures)
│   └── exploration/                 # Experiment outputs
│
├── paper/
│   ├── main.tex                     # Manuscript
│   └── references.bib               # Bibliography
│
├── .claude/
│   ├── rules/                       # Behavioral rules (auto-loaded)
│   ├── hooks/                       # Automation hooks
│   └── skills/                      # Custom skills
│
├── CLAUDE.md                        # Claude Code entry point
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
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

3. **Verify** the install:

   ```bash
   python -c "import mypackage; print('OK')"
   ```

## Start Claude Code

Open the Claude Code panel in VS Code (or run `claude` in terminal), then paste the following — fill in your project details:

> I am starting to work on **[PROJECT NAME]** in this repo. **[Describe your project in 2–3 sentences — what you're building, what data you're using, what methods you plan to apply.]**
>
> I want our collaboration to be structured and rigorous. The Claude Code workflow is already configured in this repo. Please read CLAUDE.md and the rules in .claude/rules/, understand the workflow, and then **update all configuration files to fit my project** — fill in placeholders in workflow-quick-ref.md (non-negotiables, preferences) and quality-gates.md (tolerance thresholds).
>
> After that, use the plan-first workflow for all non-trivial tasks. Once I approve a plan, switch to contractor mode — coordinate everything autonomously and only come back to me when there's ambiguity or a decision to make.
>
> Enter plan mode and start by adapting the workflow configuration for this project.

**What this does:** Claude reads all configuration files, fills in your project-specific preferences, then enters contractor mode — planning before acting, verifying after, scoring against quality gates.

## Using This Template

1. **Clone and rename:**

   ```bash
   git clone <this-repo-url> my-new-project
   ```

2. **Rename the package** — replace `mypackage` in three places:
   - Folder: `code/src/mypackage/` → `code/src/yourpackage/`
   - `code/pyproject.toml`: change `name = "mypackage"`
   - All imports: `from mypackage.config import ...` → `from yourpackage.config import ...`

3. **Edit dependencies** in `code/pyproject.toml`, then re-run `uv pip install -e ".[dev]"`.

4. **Customize** `.claude/rules/workflow-quick-ref.md` — fill in your project's non-negotiables (seed convention, figure standards, tolerance thresholds).

5. **Customize** `.claude/rules/quality-gates.md` — fill in tolerance thresholds for your domain.

## Workflow

The template enforces a **plan-first, verify-after** workflow:

```
Your instruction
    │
    ├── Trivial? → Just do it
    │
    └── Non-trivial?
        │
        ▼
    PLAN-FIRST WORKFLOW
    1. Enter plan mode
    2. Requirements spec (if ambiguous)
    3. Draft plan → save to docs/quality_reports/plans/
    4. Present to user → approval
    5. Implement via orchestrator
        │
        ▼
    ORCHESTRATOR (selected by file type)
    │
    ├── Scripts (code/scripts/) → Simplified loop
    │   IMPLEMENT → VERIFY → SCORE
    │
    └── Everything else → Full loop
        IMPLEMENT → VERIFY → REVIEW → FIX → RE-VERIFY → SCORE
                                                           │
                                                     >= 80? → done
                                                      < 80  → loop (max 5)
```

### Quality Gates

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for review |
| 95 | Excellence | Aspirational |

Scoring rubrics are defined per file type in `.claude/rules/quality-gates.md`.

### Code Organization

| Location | Purpose | Rule |
|----------|---------|------|
| `code/src/mypackage/core/` | Pure logic | No file I/O, no hardcoded paths |
| `code/scripts/core/` | Pipeline scripts | File I/O, numbered in order |
| `code/tests/` | Tests | Test src/ logic with fake data |
| `code/src/mypackage/config.py` | Paths | All file paths defined here |

**Litmus test:** Needs the file system? → `scripts/`. No? → `src/`.

**Data flow:** `data/raw/` → scripts → `data/intermediate/` → scripts → `data/processed/` → scripts → `output/core/`

### Exploration → Core Promotion

Work experimentally in `exploration/` folders across all four layers. When ready, swap `exploration` → `core` in the path, refactor, and add tests.

## Claude Code Rules

| Rule | Purpose |
|------|---------|
| `project-conventions.md` | Code organization, data flow, parallel structure |
| `plan-first-workflow.md` | Planning protocol, requirements specs |
| `session-logging.md` | When to update session logs |
| `orchestrator-protocol.md` | Post-plan execution loop (6-step) |
| `orchestrator-research.md` | Simplified loop for scripts/data analysis |
| `quality-gates.md` | Scoring rubrics by file type |
| `verification-protocol.md` | How to verify each file type |
| `workflow-quick-ref.md` | Contractor model, when to ask vs execute |

## Claude Code Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| `context-monitor.py` | PostToolUse (Bash/Task) | Warns at 40/55/65/80/90% context |
| `verify-reminder.py` | PostToolUse (Write/Edit) | Reminds to run/compile .py/.tex |
| `latex-cleanup.py` | PostToolUse (Bash) | Deletes .aux/.log/.bbl after compilation |
| `log_reminder.py` | Stop | Blocks if 15+ responses without log update |
| `pre-compact.py` | PreCompact | Saves plan state before compression |
| `post-compact-restore.py` | SessionStart (compact) | Restores state after compression |
| `protect-files.py` | PreToolUse (Edit/Write) | Blocks edits to references.bib, settings.json |
| `notify.py` | Notification | Desktop notifications |
