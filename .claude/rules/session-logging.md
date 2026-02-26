# Session Logging

**Location:** `docs/quality_reports/session_logs/YYYY-MM-DD_HHMMSS_{session_hash}_description.md`

Each Claude Code session gets its own log file. The `log-reminder` hook creates a stub automatically on the first Stop event. Rename the stub to add a short description (keep the existing prefix). The `{session_hash}` is derived from the session's unique ID, so any hook can independently find the correct log.

**Compaction:** stays in the same session log (session_id doesn't change across compaction).

## Three Triggers (all proactive)

### 1. Post-Plan Log

After plan approval, update the session log with: goal, approach, rationale, key context.

### 2. Incremental Logging

Append 1-3 lines whenever: a design decision is made, a problem is solved, the user corrects something, or the approach changes. Do not batch.

### 3. End-of-Session Log

When wrapping up: high-level summary, quality scores, open questions, blockers.

## Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Save to `docs/quality_reports/merges/YYYY-MM-DD_[branch-name].md` using `docs/templates/quality-report.md`.
