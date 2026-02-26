#!/usr/bin/env python3
"""
File Protection Hook for Claude Code

Blocks accidental edits to protected files.
Customize PROTECTED_PATTERNS below for your project.

Hook Event: PreToolUse (matcher: Edit|Write)
Exit code 0 = allow, exit code 2 = block (message shown to Claude).
"""

import json
import sys
from pathlib import Path

# ============================================================
# CUSTOMIZE: Add filenames you want to protect.
# Uses basename matching — add full paths for more precision.
# ============================================================
PROTECTED_PATTERNS = [
    "references.bib",
    "settings.json",
]


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # Extract file path based on tool type
    file_path = ""
    if tool_name in ("Edit", "Write"):
        file_path = hook_input.get("tool_input", {}).get("file_path", "")

    # No file path = not a file operation, allow
    if not file_path:
        sys.exit(0)

    basename = Path(file_path).name
    for pattern in PROTECTED_PATTERNS:
        if basename == pattern:
            print(
                f"Protected file: {basename}. "
                f"Edit manually or remove protection in .claude/hooks/protect-files.py",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
