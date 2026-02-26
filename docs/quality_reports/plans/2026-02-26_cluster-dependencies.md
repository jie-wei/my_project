# Cross-Cluster Dependency Map

## Clusters

```
BUILT                              UNBUILT
─────                              ───────
A ── context survival              E ── research skills (7 skills)
B ── plan→execute→verify           F ── meta/memory (3 items)
B2 ── session logging              C ── agents (4 agents)
D ── exploration lifecycle
```

## Built → Unbuilt Dependencies

```
A (context survival)
│
├──→ E   context-monitor fires during long skills (lit-review, interview-me)
└──→ E   pre/post-compact preserves state across compression

B (orchestrator)
│
├──→ E   orchestrator review step consumes skill output
├──→ C   agents plug into orchestrator step 2 (VERIFY) and step 3 (REVIEW)
└──→ F   meta-governance dogfoods plan-first workflow

B2 (session logging)
│
├──→ E   log-reminder enforces logging during interview-me (conversational)
└──→ D   exploration sessions log to session_logs/

D (exploration lifecycle)
│
└──→ E   docs/ tier structure determines where skill outputs land
```

## Unbuilt ↔ Unbuilt Dependencies

```
E ↔ C   HARD CYCLE (2 of 7 skills)
│
├── /proofread ────────── spawns ──→ proofreader agent
├── /review-paper ─────── spawns ──→ domain-reviewer agent
├── verifier agent ────── plugs into orchestrator (not E)
└── python-reviewer ───── plugs into orchestrator (not E)

F → E, C   SOFT (advisory only)
│
├── meta-governance guides how to create skills (E)
├── meta-governance guides how to create agents (C)
└── defines memory tiers for MEMORY.md

E → F   SOFT
│
└── /learn extracts patterns from research skills into new skills
```

## Decision Point

```
Which ordering minimizes rework?
│
├── Option 1: E → F → C (original)
│   ├── 5 of 7 E skills ship clean
│   ├── 2 skills (/proofread, /review-paper) work standalone
│   └── Rework when C arrives: update 2 SKILL.md files to spawn agents
│
├── Option 2: C → E → F
│   ├── Agents exist before skills that invoke them
│   ├── Zero rework
│   └── But C is least scoped — needs design work first
│
└── Option 3: F → C → E
    ├── Meta-governance in place before building anything
    ├── Most principled
    └── But F is advisory — doesn't block construction
```
