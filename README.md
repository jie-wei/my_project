# Economics Research Project Template

A project template for economics research with Claude Code integration. Includes a plan-first workflow, quality gates with scoring rubrics, automated verification, and session logging.

**Built on [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)** — adapted from Pedro H.C. Sant'Anna's Claude Code workflow template for economics research.

## Project Structure

```
my-project/
├── code/
│   ├── pyproject.toml               # Dependencies + makes src/ installable
│   ├── src/mypackage/               # Pure logic (no file I/O)
│   │   ├── __init__.py
│   │   ├── config.py                # All file paths, one place
│   │   ├── core/                    # Production logic
│   │   ├── exploration/             # Experimental logic
│   │   └── archive/                 # Retired experiments
│   ├── scripts/
│   │   ├── core/                    # Numbered pipeline scripts (01_clean.py, 02_merge.py, …)
│   │   ├── exploration/             # Notebooks, ad-hoc analysis
│   │   └── archive/                 # Retired scripts
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
│   ├── archive/                     # Retired notes
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
│   ├── exploration/                 # Experiment outputs
│   └── archive/                     # Retired outputs
│
├── paper/
│   ├── main.tex                     # Manuscript
│   └── references.bib               # Bibliography
│
├── .claude/
│   ├── agents/                      # Subagent prompts (reviewer, verifier, etc.)
│   ├── rules/                       # Behavioral rules (auto-loaded)
│   ├── hooks/                       # Automation hooks
│   └── skills/                      # Custom skills
│
├── CLAUDE.md                        # Claude Code entry point
└── .gitignore
```

## Setup

1. **Clone and rename:**

   ```bash
   git clone <this-repo-url> my-new-project
   ```

2. **Rename the package** — replace `mypackage` in three places:
   - Folder: `code/src/mypackage/` → `code/src/yourpackage/`
   - `code/pyproject.toml`: change `name = "mypackage"`
   - All imports: `from mypackage.config import ...` → `from yourpackage.config import ...`

3. **Install [uv](https://docs.astral.sh/uv/)** and dependencies:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   cd code
   uv venv --python 3.12
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   python -c "import mypackage; print('OK')"
   ```

4. **Customize** for your project:
   - `.claude/rules/workflow-start.md` — non-negotiables (seed convention, figure standards)
   - `.claude/rules/quality-gates.md` — tolerance thresholds for your domain

5. **Start Claude Code** — open the panel in VS Code (or run `claude` in terminal), then paste:

   > I am starting to work on **[PROJECT NAME]** in this repo. **[Describe your project in 2–3 sentences — what you're building, what data you're using, what methods you plan to apply.]**
   >
   > I want our collaboration to be structured and rigorous. The Claude Code workflow is already configured in this repo. Please read CLAUDE.md and the rules in .claude/rules/, understand the workflow, and then **update all configuration files to fit my project** — fill in placeholders in workflow-start.md (non-negotiables, preferences) and quality-gates.md (tolerance thresholds).
   >
   > After that, use the plan-first workflow for all non-trivial tasks. Once I approve a plan, switch to contractor mode — coordinate everything autonomously and only come back to me when there's ambiguity or a decision to make.
   >
   > Enter plan mode and start by adapting the workflow configuration for this project.

   **What this does:** Claude reads all configuration files, fills in your project-specific preferences, then enters contractor mode — planning before acting, verifying after, scoring against quality gates.

## Workflow

### Master Routing

Every instruction is routed based on its nature:

```
Your instruction
    │
    ├─ Exploration? ────────────── EXPLORATION FAST-TRACK
    │  (new idea to test)            60/100, no planning
    │                                → see "Exploration Workflow"
    │
    ├─ Trivial production? ──────── JUST DO IT
    │  (typo, one-line fix)          verify → score (80/100) → done
    │
    └─ Non-trivial production? ──── PLAN-FIRST WORKFLOW
       (multi-file, unclear)         → see "Production Workflow"
```

### Production Workflow (Plan → Orchestrate → Verify)

```
NON-TRIVIAL INSTRUCTION
    │
    ▼
PLAN-FIRST WORKFLOW
    1. Enter plan mode
    2. Requirements spec (if ambiguous — ask user)
    3. Draft plan → save to docs/quality_reports/plans/
    4. Present to user → wait for approval
    │
    ▼
ORCHESTRATOR (selected by file type)
    │
    ├── Scripts (code/scripts/) → Simplified loop
    │   IMPLEMENT → VERIFY → SCORE (>= 80?)
    │                                YES → done
    │                                NO  → fix → re-verify
    │
    └── Everything else → Full loop
        IMPLEMENT → VERIFY → REVIEW → FIX → RE-VERIFY → SCORE
                                                           │
                                                     >= 80? → done
                                                      < 80  → loop (max 5)
```

Rules: `workflow-plan.md`, `protocol-orchestrator.md`

### Exploration Workflow (Fast-Track → Decide)

The project uses a **three-tier structure** across four layers: `core/` (production), `exploration/` (active experiments), and `archive/` (retired). Transitions are just swapping the tier name.

```
User: "Let's explore [idea]"
    │
    ▼
┌─ RESEARCH VALUE CHECK
│  Worth investigating?  NO → Stop.  YES ↓
│
├─ PICK A NAME (short, descriptive, snake_case)
│  e.g., "iv_approach", "bootstrap_se", "did_event_study"
│
├─ CREATE NAMED SUBFOLDER across needed layers:
│  code/src/mypackage/exploration/[name]/
│  code/scripts/exploration/[name]/
│  output/exploration/[name]/
│  docs/exploration/[name]/
│
├─ CODE IMMEDIATELY (60/100 threshold, no plan mode)
│  ✓ Must: code runs, results correct, goal in session log
│  ✗ Skip: tests, type hints, docstrings, script numbering
│
├─ LOG PROGRESS (session log)
│
▼
┌─ DECISION POINT (user decides, never Claude) ────┐
│                                                   │
├─ PROMOTE                 ├─ KEEP          ├─ ARCHIVE
│  exploration/[name]/     │  Stay in       │  exploration/[name]/
│    → core/[name]/        │  exploration/  │    → archive/[name]/
│  Graduate checklist:     │                │  with brief note
│  □ Quality >= 80         │                │
│  □ Tests added & pass    │                │
│  □ Follows conventions   │                │
│  □ Documented            │                │
└──────────────────────────┴────────────────┘
```

**Promotion re-enters the production workflow:** when the user decides to promote, the promoted code goes through the full plan-first → orchestrator pipeline at the 80/100 threshold.

Rules: `workflow-exploration.md`

## Conventions

### Code Organization

| Location | Purpose | Rule |
|----------|---------|------|
| `code/src/mypackage/core/` | Pure logic | No file I/O, no hardcoded paths |
| `code/scripts/core/` | Pipeline scripts | File I/O, numbered in order |
| `code/tests/` | Tests | Test src/ logic with fake data |
| `code/src/mypackage/config.py` | Paths | All file paths defined here |

**Litmus test:** Needs the file system? → `scripts/`. No? → `src/`.

### Data Flow

`data/raw/` → scripts → `data/intermediate/` → scripts → `data/processed/` → scripts → `output/core/`

Exploration outputs go to `output/exploration/[name]/`. Raw data is sacred — never modify.

### Quality Gates

| Score | Gate | Meaning |
|-------|------|---------|
| 60 | Exploration | Good enough to keep exploring |
| 80 | Commit | Good enough to save (production) |
| 90 | PR | Ready for review |
| 95 | Excellence | Aspirational |

Scoring rubrics are defined per file type in `.claude/rules/quality-gates.md`.

## Automation

### Session Logging

**Session logging** runs throughout all workflow paths:
- **Post-plan**: goal, approach, key context
- **Incremental**: 1-3 lines on decisions, problems, corrections
- **End-of-session**: summary, scores, open questions

The `log-reminder` hook auto-creates one session log per Claude Code session. Naming: `YYYY-MM-DD_HHMMSS_{hash}_description.md`.

### Context Survival & Session Lifecycle

Hooks fire automatically throughout a session to maintain continuity:

```
SESSION START
    │
    ├─ log-reminder creates session log stub
    ├─ post-compact restores state (if resuming after compression)
    │
    ▼
DURING WORK (hooks fire on every tool use)
    │
    ├─ verify-reminder ─── after .py/.tex edit → "run/compile to verify"
    ├─ protect-files ───── blocks edits to references.bib, settings.json
    ├─ latex-cleanup ───── after LaTeX compilation → deletes .aux/.log/.bbl
    ├─ log-reminder ────── blocks if 15+ responses without session log update
    │
    ▼
APPROACHING CONTEXT LIMIT
    │
    ├─ pre-compact saves: session log path, active plan, open questions
    ├─ auto-compression happens
    ├─ post-compact restores saved state
    └─ Resume: read plan + git log + state current task
```

### Rules Reference

| Rule | Purpose |
|------|---------|
| `conventions.md` | Code organization, data flow, three-tier structure |
| `workflow-plan.md` | Planning protocol, requirements specs |
| `session-logging.md` | When to update session logs |
| `protocol-orchestrator.md` | Post-plan execution loop (full + simplified for scripts) |
| `quality-gates.md` | Scoring rubrics by file type |
| `protocol-verification.md` | How to verify each file type |
| `workflow-start.md` | Contractor model, when to ask vs execute |
| `workflow-exploration.md` | Exploration fast-track, promotion, archiving |
| `pdf-processing.md` | Safe PDF reading workflow (chunked, size-checked) |

### Hooks Reference

| Hook | Trigger | Action |
|------|---------|--------|
| `verify-reminder.py` | PostToolUse (Write/Edit) | Reminds to run/compile .py/.tex |
| `latex-cleanup.py` | PostToolUse (Bash) | Deletes .aux/.log/.bbl after compilation |
| `log-reminder.py` | Stop | Blocks if 15+ responses without log update |
| `pre-compact.py` | PreCompact | Saves plan state before compression |
| `post-compact-restore.py` | SessionStart (compact) | Restores state after compression |
| `protect-files.py` | PreToolUse (Edit/Write) | Blocks edits to references.bib, settings.json |
| `notify.py` | Notification | Desktop notifications |
