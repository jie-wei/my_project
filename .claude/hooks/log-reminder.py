#!/usr/bin/env python3
"""
Session Log Reminder Hook for Claude Code

A Stop hook that ensures each Claude Code session has its own log file.
On first encounter with a new session_id, it creates a stub log file.
After a threshold of responses without updating, it reminds Claude.

Session identification uses session_id from Claude Code's hook stdin JSON.
Log files use the naming convention: YYYY-MM-DD_HHMMSS_{session_hash}.md
where session_hash = md5(session_id)[:6].

Any hook can independently find a session's log by computing the hash
and globbing for *_{session_hash}_*.md — no cross-hook state dependency.

Usage (in .claude/settings.json):
    "Stop": [{ "hooks": [{ "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-reminder.py" }] }]
"""

import json
import sys
import os
import hashlib
import time
from pathlib import Path
from datetime import datetime

THRESHOLD = 15
STATE_DIR = Path("/tmp/claude-log-reminder")
CLEANUP_AGE_SECONDS = 7 * 24 * 3600  # 7 days


def get_hook_input() -> dict:
    """Read JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}


def get_project_dir(hook_input: dict) -> str:
    """Get project directory from hook input or environment."""
    return hook_input.get("cwd", "") or os.environ.get("CLAUDE_PROJECT_DIR", "")


def get_session_hash(session_id: str) -> str:
    """Compute 6-char hex hash from session_id."""
    return hashlib.md5(session_id.encode()).hexdigest()[:6]


def get_project_hash(project_dir: str) -> str:
    """Compute 12-char hex hash from project directory."""
    return hashlib.md5(project_dir.encode()).hexdigest()[:12]


def get_state_path(project_dir: str, session_hash: str) -> Path:
    """Return a project+session-keyed state file path."""
    project_hash = get_project_hash(project_dir)
    return STATE_DIR / f"{project_hash}_{session_hash}.json"


def load_state(state_path: Path) -> dict | None:
    """Load persisted state, or return None if no state file exists."""
    try:
        return json.loads(state_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_state(state_path: Path, state: dict):
    """Persist state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state))


def cleanup_old_state_files():
    """Delete state files older than CLEANUP_AGE_SECONDS."""
    if not STATE_DIR.is_dir():
        return
    now = time.time()
    for f in STATE_DIR.iterdir():
        if f.suffix == ".json":
            try:
                if now - f.stat().st_mtime > CLEANUP_AGE_SECONDS:
                    f.unlink()
            except OSError:
                pass


def get_logs_dir(project_dir: str) -> Path:
    """Return the session logs directory path."""
    return Path(project_dir) / "docs" / "quality_reports" / "session_logs"


def find_session_log(logs_dir: Path, session_hash: str) -> Path | None:
    """Find a log file matching this session's hash."""
    matches = list(logs_dir.glob(f"*_{session_hash}_*.md"))
    if not matches:
        # Also check for stub files without description suffix
        matches = list(logs_dir.glob(f"*_{session_hash}.md"))
    if matches:
        return matches[0]
    return None


def create_stub_log(logs_dir: Path, session_hash: str) -> Path:
    """Create a stub session log file. Returns the path."""
    now = datetime.now()
    timestamp_prefix = now.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{timestamp_prefix}_{session_hash}.md"
    log_path = logs_dir / filename

    logs_dir.mkdir(parents=True, exist_ok=True)

    content = f"""# Session Log — {now.strftime("%Y-%m-%d")}

**Session started:** {now.strftime("%H:%M")}
**Status:** IN PROGRESS

## Objective
[Update with current goal]

## Changes Made

| File | Change | Reason |
|------|--------|--------|

## Incremental Work Log

"""
    log_path.write_text(content)
    return log_path


def block(reason: str):
    """Output a block decision and exit."""
    json.dump({"decision": "block", "reason": reason}, sys.stdout)
    sys.exit(0)


def main():
    hook_input = get_hook_input()

    # Prevent infinite loops: if Claude is already continuing from a
    # previous Stop hook block, let it stop this time.
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    project_dir = get_project_dir(hook_input)
    if not project_dir:
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    if not session_id:
        # No session_id available — can't do session-aware tracking.
        # Fail open rather than break Claude's workflow.
        sys.exit(0)

    session_hash = get_session_hash(session_id)
    state_path = get_state_path(project_dir, session_hash)
    state = load_state(state_path)
    logs_dir = get_logs_dir(project_dir)

    # Periodically clean up old state files
    cleanup_old_state_files()

    # --- Case 1: New session (no state file) ---
    if state is None:
        log_path = find_session_log(logs_dir, session_hash)
        created_new = log_path is None

        if created_new:
            log_path = create_stub_log(logs_dir, session_hash)

        state = {
            "session_id": session_id,
            "session_hash": session_hash,
            "log_path": str(log_path),
            "counter": 0,
            "last_mtime": log_path.stat().st_mtime,
            "reminded": False,
        }
        save_state(state_path, state)

        rel_path = log_path.relative_to(Path(project_dir))
        if created_new:
            # Fresh stub — tell Claude to rename with a description and fill in.
            # When Claude renames, next invocation re-globs *_{hash}_*.md to find it.
            stub_name = log_path.stem  # e.g. 2026-02-25_191518_9cd6ad
            block(
                f"SESSION LOG: A session log stub was created at {rel_path}. "
                f"Rename it to {stub_name}_short-description.md (keep the existing prefix) "
                f"and update it with your current goal and context."
            )
        else:
            # Found an existing log for this session (e.g. state was cleared).
            # Just ask Claude to update it — no rename needed.
            block(
                f"SESSION LOG: Update the session log at {rel_path} "
                f"with your current goal and context."
            )
        return

    # --- Case 2: Existing session ---
    log_path = Path(state["log_path"])

    # Handle deleted log file: re-discover or re-create
    if not log_path.exists():
        found = find_session_log(logs_dir, session_hash)
        if found:
            log_path = found
        else:
            log_path = create_stub_log(logs_dir, session_hash)
        state["log_path"] = str(log_path)
        state["last_mtime"] = log_path.stat().st_mtime
        state["counter"] = 0
        state["reminded"] = False
        save_state(state_path, state)
        sys.exit(0)

    # Check if log was updated since last check
    current_mtime = log_path.stat().st_mtime
    if current_mtime != state["last_mtime"]:
        state["counter"] = 0
        state["last_mtime"] = current_mtime
        state["reminded"] = False
        save_state(state_path, state)
        sys.exit(0)

    # Log not updated — increment counter
    state["counter"] += 1

    if state["counter"] >= THRESHOLD and not state["reminded"]:
        state["reminded"] = True
        save_state(state_path, state)

        rel_path = log_path.relative_to(Path(project_dir))
        block(
            f"SESSION LOG REMINDER: {state['counter']} responses without "
            f"updating the session log. Append your recent progress to {rel_path}."
        )
        return

    save_state(state_path, state)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
