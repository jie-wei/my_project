#!/usr/bin/env python3
"""
LaTeX Auxiliary File Cleanup Hook

Detects LaTeX compilation commands (xelatex, pdflatex, latexmk, bibtex)
and auto-deletes auxiliary files after compilation.

Hook Event: PostToolUse (matcher: "Bash")
Returns: Exit code 0 (non-blocking)
"""

import json
import os
import re
import sys
from pathlib import Path

# Auxiliary file extensions to clean up
AUX_EXTENSIONS = {
    ".aux", ".log", ".bbl", ".blg", ".out", ".toc",
    ".lof", ".lot", ".fls", ".fdb_latexmk", ".synctex.gz",
    ".bcf", ".run.xml", ".nav", ".snm", ".vrb",
}

# Commands that indicate LaTeX compilation
LATEX_COMMANDS = {"xelatex", "pdflatex", "latexmk", "bibtex"}

# Colors for terminal output
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
NC = "\033[0m"


def find_latex_dir(command: str) -> Path | None:
    """Extract the working directory from a LaTeX compilation command.

    Handles patterns like:
      - cd paper && latexmk -xelatex main.tex
      - xelatex paper/main.tex
      - latexmk -xelatex paper/main.tex
      - cd paper && xelatex main.tex
    """
    # Check if any latex command is in the string
    if not any(cmd in command for cmd in LATEX_COMMANDS):
        return None

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # Pattern 1: cd <dir> && <latex command>
    cd_match = re.search(r"cd\s+([^\s&;]+)", command)
    if cd_match:
        cd_target = cd_match.group(1)
        candidate = Path(project_dir) / cd_target
        if candidate.is_dir():
            return candidate

    # Pattern 2: <latex command> ... <dir>/<file>.tex
    tex_match = re.search(r"(\S+)\.tex", command)
    if tex_match:
        tex_path = Path(tex_match.group(0))
        if tex_path.parent != Path("."):
            candidate = Path(project_dir) / tex_path.parent
            if candidate.is_dir():
                return candidate

    # Pattern 3: command run from project root, .tex file in current dir
    # Check paper/ as default LaTeX directory
    default = Path(project_dir) / "paper"
    if default.is_dir():
        return default

    return None


def cleanup_aux_files(directory: Path) -> int:
    """Delete auxiliary files in the given directory. Returns count deleted."""
    count = 0
    for f in directory.iterdir():
        if f.is_file() and f.suffix in AUX_EXTENSIONS:
            try:
                f.unlink()
                count += 1
            except OSError:
                pass
    return count


def main() -> int:
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        return 0

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        return 0

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    if not any(cmd in command for cmd in LATEX_COMMANDS):
        return 0

    latex_dir = find_latex_dir(command)
    if latex_dir is None or not latex_dir.is_dir():
        return 0

    count = cleanup_aux_files(latex_dir)
    if count > 0:
        rel_dir = latex_dir.name
        print(f"\n{CYAN}LaTeX cleanup:{NC} removed {GREEN}{count}{NC} auxiliary file(s) from {rel_dir}/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
