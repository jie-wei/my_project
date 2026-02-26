# Plan: Remaining Clusters (E → C → F)

**Status:** DRAFT
**Date:** 2026-02-26
**Depends on:** Clusters A, B, B2, D (all built)

## Summary

Build E (research skills) first, designed with C (agents) in mind, then C as thin agent wrappers, then F (meta/governance). This ordering emerged from dependency analysis: C's agents consume E's skills (compile-latex, validate-bib, proofread, review-paper), so skills must exist before agents can wrap them.

## Ordering Rationale

```
Naive plan:     E → F → C     (rework 2 skills when C arrives)
Alternative:    C → E → F     (C agents need E skills — blocked)
Alternative:    C+E together   (complex interleave)
Final plan:     E → C → F     (E designed for C from day one, zero rework)
```

Key insight: B's orchestrator has a hollow REVIEW step (step 3) that C's agents fill. But those agents consume E's skills. So: E provides the tools, C wires them into the orchestrator, F governs the whole system.

---

## Phase 1: Cluster E — Research Skills

### E.1: Settings change (prerequisite)

**File:** `.claude/settings.json`

Add WebSearch and WebFetch permissions (required by /lit-review):
```json
"// --- Web search for literature review ---",
"WebSearch(query *)",
"WebFetch(url:*, prompt:*)"
```

### E.2: Standalone skills (no C dependency)

These 3 skills are pure research tools with no agent interaction.

| Skill | File | Reference | Adaptation |
|-------|------|-----------|------------|
| `/research-ideation` | `.claude/skills/research-ideation/SKILL.md` | Reference has economics framing (DiD, IV, RDD) | Generalize to domain-agnostic: keep descriptive→causal progression, replace economics-specific methods with general categories (experimental, quasi-experimental, observational, computational) |
| `/interview-me` | `.claude/skills/interview-me/SKILL.md` | Reference mostly generic | Minor: swap "econometric" → "methodology", "identification" → "research design". Add session logging note (conversational skill, log-reminder fires at 15 responses) |
| `/lit-review` | `.claude/skills/lit-review/SKILL.md` | Reference generic | Minimal adaptation. Add: honest uncertainty note, no fabricated citations. Needs WebSearch/WebFetch from E.1 |

**Output location for all 3:** Default to `docs/exploration/[name]/` if inside an exploration, otherwise `docs/core/`. Tier-aware, consistent with project structure.

### E.3: Agent-consumable skills (C will wrap these)

These 4 skills serve double duty: user-invoked AND consumed by C's agents. Design with structured, parseable output from day one.

| Skill | File | Future C consumer | Design-for-C notes |
|-------|------|-------------------|-------------------|
| `/compile-latex` | `.claude/skills/compile-latex/SKILL.md` | verifier agent (LaTeX path) | Retarget: `Slides/` → `paper/`, `Preambles/` → `docs/preambles/`, Beamer → generic article. Output: structured result with success/failure, warning count, undefined citations list, page count. |
| `/validate-bib` | `.claude/skills/validate-bib/SKILL.md` | verifier agent (LaTeX path) | Retarget: `Bibliography_base.bib` → `paper/references.bib`, `Slides/*.tex` → `paper/*.tex`. Add Write to allowed-tools. Output: structured lists of missing entries, unused entries, potential typos. |
| `/proofread` | `.claude/skills/proofread/SKILL.md` | proofreader agent | Retarget: `Slides/`+`Quarto/` → `paper/`. Define protocol once in SKILL.md. Agent rule (Phase 2) will reference this protocol. Report-only: never edit source files. |
| `/review-paper` | `.claude/skills/review-paper/SKILL.md` | domain-reviewer agent | Generalize 6 review dimensions: replace "econometric specification" → "methodology/analytical approach". Keep referee-style framing. Protocol defined once, agent rule references it. |

### E.4: CLAUDE.md update

Add all 7 skills to the Skills table.

### E.5: Verification

- Check all 7 SKILL.md files have valid YAML frontmatter
- Check allowed-tools reference real tools
- Check file paths in skills match actual project structure (paper/, docs/preambles/, etc.)
- Confirm WebSearch/WebFetch permissions work in settings.json

---

## Phase 2: Cluster C — Agents

Agents are **rules** with path scoping (auto-loaded by orchestrator), not skills. They live in `.claude/rules/` and reference E's skill protocols where applicable.

### C.1: Python-path verifier

**File:** `.claude/rules/verify-python.md`
**Scoped to:** `code/**/*.py`
**Orchestrator step:** 2 (VERIFY)

What it does:
- Python modules: import check, pytest, convention check (no I/O in src/)
- Python scripts: run script, check output exists, spot-check values
- Already defined in `verification-protocol.md` — this agent operationalizes those checks as a focused protocol

Note: This is the only agent with zero E skill dependency. Uses bash (python3, pytest) directly.

### C.2: Python reviewer

**File:** `.claude/rules/review-python.md`
**Scoped to:** `code/**/*.py`
**Orchestrator step:** 3 (REVIEW)

What it does:
- Apply quality-gates.md Python rubrics
- Check: file I/O in src/ (-30), hardcoded paths (-20), missing tests (-10), naming (-3)
- Produce structured score with deductions itemized

### C.3: LaTeX-path verifier

**File:** `.claude/rules/verify-latex.md`
**Scoped to:** `paper/**/*.tex`
**Orchestrator step:** 2 (VERIFY)

What it does:
- Invoke `/compile-latex` protocol from E.3
- Invoke `/validate-bib` protocol from E.3
- Parse structured output: compilation success, overfull warnings, undefined citations, missing bib entries
- Report pass/fail with specific issues

**Depends on E.3:** compile-latex and validate-bib skills must exist.

### C.4: Proofreader agent

**File:** `.claude/rules/proofread-manuscript.md`
**Scoped to:** `paper/**/*.tex`
**Orchestrator step:** 3 (REVIEW)

What it does:
- Follow `/proofread` protocol from E.3
- Three-phase: review & propose (no edits) → user approves → apply fixes
- Check: grammar, typos, overflow, consistency, academic quality

**Depends on E.3:** proofread skill protocol.

### C.5: Domain reviewer agent

**File:** `.claude/rules/review-domain.md`
**Scoped to:** `paper/**/*.tex`
**Orchestrator step:** 3 (REVIEW)

What it does:
- Follow `/review-paper` protocol from E.3
- Review dimensions: argument structure, methodology, literature positioning, writing, presentation
- Generate referee objections
- Produce structured review with dimensional scores

**Depends on E.3:** review-paper skill protocol.

### C.6: Orchestrator integration

**File:** `.claude/rules/orchestrator-protocol.md` (modify existing)

Update Step 2 and Step 3 to reference the agent rules:
- Step 2 (VERIFY): "Use verify-python.md for Python files, verify-latex.md for LaTeX files"
- Step 3 (REVIEW): "Use review-python.md for Python, proofread-manuscript.md + review-domain.md for LaTeX"

### C.7: CLAUDE.md update

Add agents section documenting all 5 agent rules and how they integrate with the orchestrator.

### C.8: Verification

- Verify path scoping is correct (test with sample .py and .tex files)
- Verify agents reference existing skill protocols
- Verify orchestrator-protocol.md updates are consistent
- Walkthrough: simulate orchestrator loop with a Python file, then a LaTeX file

---

## Phase 3: Cluster F — Meta/Memory

### F.1: Meta-governance rule

**File:** `.claude/rules/meta-governance.md`
**Reference:** `/tmp/claude-code-my-workflow/.claude/rules/meta-governance.md`

Adapt for our template:
- Generic vs specific content guidelines
- Two-tier memory: MEMORY.md (committed, generic) + `.claude/state/personal-memory.md` (gitignored, local)
- Amendment process for rules/skills/agents
- Template maintenance principles (keep generic, use examples from multiple domains)

### F.2: /learn skill

**File:** `.claude/skills/learn/SKILL.md`
**Reference:** `/tmp/claude-code-my-workflow/.claude/skills/learn/SKILL.md`

Minimal adaptation needed — reference is already generic:
- 4-phase: evaluate → check existing → create → quality gate
- Extracts session discoveries into persistent skills
- Follows meta-governance rules for what goes where

### F.3: MEMORY.md restructure

Restructure per meta-governance two-tier model:
- MEMORY.md: generic learnings that help all users (committed)
- `.claude/state/personal-memory.md`: machine/user-specific (gitignored)
- Add `.claude/state/` to `.gitignore`

### F.4: CLAUDE.md update

- Add `/learn` to skills table
- Add meta-governance to rules reference

### F.5: Verification

- Verify meta-governance rule loads (no path scoping — global)
- Verify /learn skill creates valid SKILL.md structure
- Verify .claude/state/ is gitignored

---

## Files Created (15 total)

### Phase 1 — E (7 skills + 1 settings change)
```
.claude/skills/research-ideation/SKILL.md    (new)
.claude/skills/interview-me/SKILL.md         (new)
.claude/skills/lit-review/SKILL.md           (new)
.claude/skills/compile-latex/SKILL.md        (new)
.claude/skills/validate-bib/SKILL.md         (new)
.claude/skills/proofread/SKILL.md            (new)
.claude/skills/review-paper/SKILL.md         (new)
.claude/settings.json                        (modify — add WebSearch/WebFetch)
CLAUDE.md                                    (modify — add 7 skills to table)
```

### Phase 2 — C (5 agent rules + 1 orchestrator update)
```
.claude/rules/verify-python.md               (new)
.claude/rules/review-python.md               (new)
.claude/rules/verify-latex.md                (new)
.claude/rules/proofread-manuscript.md        (new)
.claude/rules/review-domain.md              (new)
.claude/rules/orchestrator-protocol.md       (modify — add agent references)
CLAUDE.md                                    (modify — add agents section)
```

### Phase 3 — F (1 rule + 1 skill + restructure)
```
.claude/rules/meta-governance.md             (new)
.claude/skills/learn/SKILL.md                (new)
.claude/state/personal-memory.md             (new, gitignored)
.gitignore                                   (modify — add .claude/state/)
CLAUDE.md                                    (modify — add /learn + meta-governance)
MEMORY.md                                    (modify — restructure)
```

---

## Open Design Decisions

| Decision | Proposed | Status |
|----------|----------|--------|
| Domain generalization | Fully generic — strip economics framing, use general methodology terms | PROPOSED |
| Skill output location | Tier-aware: `docs/exploration/[name]/` or `docs/core/` | PROPOSED |
| Include all 7 E skills? | Yes — all 7 (5 standalone + 2 paired with agents) | PROPOSED |
| Include all 5 C agents? | Yes — 2 verifiers (Python, LaTeX) + 3 reviewers (Python, proofreader, domain) | PROPOSED |
| `master_supporting_docs/` directory | Skip — users add it themselves if needed | PROPOSED |
| Additional skills (/context-status, /devils-advocate, /data-analysis) | Defer to future work | PROPOSED |

---

## Commit Strategy

Each phase gets its own branch, PR, and merge:
- `add-research-skills` (Phase 1)
- `add-orchestrator-agents` (Phase 2)
- `add-meta-governance` (Phase 3)

Quality reports generated at each merge per existing workflow.
