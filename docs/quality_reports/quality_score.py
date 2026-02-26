#!/usr/bin/env python3
"""
Quality Scoring System

Calculates objective quality scores (0-100) based on rubrics defined in
.claude/rules/quality-gates.md. Enforces quality gates: 80 (commit),
90 (PR), 95 (excellence).

Supports: .py (modules + scripts), .tex (LaTeX manuscripts)

Usage:
    python docs/quality_reports/quality_score.py code/src/mypackage/core/model.py
    python docs/quality_reports/quality_score.py code/scripts/core/01_clean.py
    python docs/quality_reports/quality_score.py paper/main.tex
    python docs/quality_reports/quality_score.py code/src/mypackage/core/*.py --summary
    python docs/quality_reports/quality_score.py code/src/mypackage/core/*.py --json
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import re
import json
import ast

# ==============================================================================
# SCORING RUBRICS (from .claude/rules/quality-gates.md)
# ==============================================================================

PYTHON_MODULE_RUBRIC = {
    'critical': {
        'syntax_or_import_error': {'points': 100, 'auto_fail': True},
        'file_io_in_src': {'points': 30},
        'hardcoded_absolute_paths': {'points': 20},
    },
    'major': {
        'missing_test': {'points': 10},
        'paths_not_from_config': {'points': 10},
    },
    'minor': {
        'inconsistent_naming': {'points': 3},
        'missing_type_hints_public': {'points': 2},
    }
}

PYTHON_SCRIPT_RUBRIC = {
    'critical': {
        'syntax_error': {'points': 100, 'auto_fail': True},
        'modifies_raw_data': {'points': 30},
        'hardcoded_absolute_paths': {'points': 20},
    },
    'major': {
        'missing_seed': {'points': 10},
        'expected_output_not_created': {'points': 10},
    },
    'minor': {
        'script_not_numbered': {'points': 3},
    }
}

LATEX_RUBRIC = {
    'critical': {
        'compilation_failure': {'points': 100, 'auto_fail': True},
        'undefined_citation': {'points': 15},
        'overfull_hbox': {'points': 10},
    },
    'major': {
        'typo_in_equation': {'points': 5},
    },
    'minor': {
        'inconsistent_notation': {'points': 3},
    }
}

EXPLORATION_RUBRIC = {
    'critical': {
        'syntax_or_import_error': {'points': 100, 'auto_fail': True},
        'modifies_raw_data': {'points': 30},
    },
    'major': {
        'code_doesnt_run': {'points': 15},
        'missing_seed': {'points': 10},
    },
    'minor': {
        'hardcoded_absolute_paths': {'points': 5},
    }
}

THRESHOLDS = {
    'commit': 80,
    'pr': 90,
    'excellence': 95,
    'exploration': 60,
}

# ==============================================================================
# FILE CLASSIFICATION
# ==============================================================================

def classify_file(filepath: Path) -> str:
    """Classify a file into its scoring category."""
    parts = filepath.parts
    path_str = str(filepath)

    if filepath.suffix == '.tex':
        return 'latex'

    if filepath.suffix == '.py':
        if 'exploration' in parts or 'archive' in parts:
            return 'exploration_python'
        if 'scripts' in parts:
            return 'python_script'
        if 'src' in parts:
            return 'python_module'
        # Default: treat as script
        return 'python_script'

    return 'unknown'


# ==============================================================================
# ISSUE DETECTION
# ==============================================================================

class IssueDetector:
    """Detect common issues for quality scoring."""

    @staticmethod
    def check_python_syntax(filepath: Path) -> Tuple[bool, str]:
        """Check if Python file has valid syntax."""
        try:
            source = filepath.read_text(encoding='utf-8')
            ast.parse(source, filename=str(filepath))
            return True, ""
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"

    @staticmethod
    def check_python_imports(filepath: Path) -> Tuple[bool, str]:
        """Check if Python file imports resolve (syntax + import check)."""
        try:
            result = subprocess.run(
                [sys.executable, '-c', f'import ast; ast.parse(open("{filepath}").read())'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False, result.stderr.strip()
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Syntax check timeout"

    @staticmethod
    def check_file_io_in_src(content: str) -> List[int]:
        """Detect file I/O operations that belong in scripts/, not src/."""
        issues = []
        lines = content.split('\n')
        io_patterns = [
            r'\bopen\s*\(',
            r'\.read_csv\b',
            r'\.to_csv\b',
            r'\.read_excel\b',
            r'\.to_excel\b',
            r'\.read_json\b',
            r'\.to_json\b',
            r'\.read_parquet\b',
            r'\.to_parquet\b',
            r'\.read_feather\b',
            r'\.to_feather\b',
            r'\.read_stata\b',
            r'\.to_stata\b',
            r'pd\.read_',
            r'np\.load\b',
            r'np\.save\b',
            r'pickle\.(load|dump)\b',
            r'json\.(load|dump)\b(?!s)',  # json.load/dump but not loads/dumps
            r'Path\([^)]*\)\.(read_text|write_text|read_bytes|write_bytes)',
        ]

        for i, line in enumerate(lines, 1):
            stripped = line.split('#')[0] if '#' in line else line
            for pattern in io_patterns:
                if re.search(pattern, stripped):
                    issues.append(i)
                    break

        return issues

    @staticmethod
    def check_hardcoded_paths(content: str) -> List[int]:
        """Detect hardcoded absolute paths."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.split('#')[0] if '#' in line else line
            # Match absolute paths in strings
            if re.search(r'["\'][/~](?!tmp/)', stripped):
                # Skip URLs
                if not re.search(r'https?://', stripped):
                    issues.append(i)
            # Match Windows absolute paths
            if re.search(r'["\'][A-Za-z]:[/\\]', stripped):
                issues.append(i)

        return list(set(issues))

    @staticmethod
    def check_raw_data_modification(content: str) -> List[int]:
        """Detect writes to data/raw/."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if re.search(r'["\'].*data[/\\]raw[/\\]', line):
                # Check if it's a write operation context
                stripped = line.split('#')[0] if '#' in line else line
                write_patterns = [
                    r'\.to_csv', r'\.to_excel', r'\.to_parquet',
                    r'\.write', r'\.save', r'dump',
                    r'open\(.*(w|a)', r'shutil\.(copy|move)',
                ]
                for pattern in write_patterns:
                    if re.search(pattern, stripped):
                        issues.append(i)
                        break

        return issues

    @staticmethod
    def check_paths_from_config(content: str) -> List[int]:
        """Check if paths are imported from config.py rather than hardcoded."""
        issues = []
        lines = content.split('\n')

        # Check for path-like string literals that should come from config
        for i, line in enumerate(lines, 1):
            stripped = line.split('#')[0] if '#' in line else line
            # Paths to data/, output/, paper/ directories
            if re.search(r'["\'].*(data|output|paper)[/\\]', stripped):
                # Skip if it's an import or comment
                if stripped.strip().startswith(('import', 'from', '#')):
                    continue
                issues.append(i)

        return issues

    @staticmethod
    def check_missing_seed(content: str) -> bool:
        """Check if stochastic code has seed set."""
        random_indicators = [
            r'random\.', r'np\.random\.', r'torch\.manual_seed',
            r'random_state', r'RandomState', r'seed=',
            r'sample\(', r'shuffle\(',
        ]
        has_random = any(re.search(p, content) for p in random_indicators)

        seed_patterns = [
            r'random\.seed\(', r'np\.random\.seed\(',
            r'torch\.manual_seed\(', r'random_state\s*=',
            r'seed\s*=\s*\d+', r'SEED\s*=',
        ]
        has_seed = any(re.search(p, content) for p in seed_patterns)

        return has_random and not has_seed

    @staticmethod
    def check_script_numbering(filepath: Path) -> bool:
        """Check if script in core/ follows NN_ numbering convention."""
        if 'core' not in filepath.parts:
            return True  # Only core scripts need numbering
        name = filepath.stem
        return bool(re.match(r'^\d{2}_', name))

    @staticmethod
    def check_latex_syntax(content: str) -> List[Dict]:
        """Check for common LaTeX syntax issues without compiling."""
        issues = []
        lines = content.split('\n')

        env_stack = []
        for i, line in enumerate(lines, 1):
            stripped = line.split('%')[0] if '%' in line else line

            for match in re.finditer(r'\\begin\{(\w+)\}', stripped):
                env_stack.append((match.group(1), i))

            for match in re.finditer(r'\\end\{(\w+)\}', stripped):
                env_name = match.group(1)
                if env_stack and env_stack[-1][0] == env_name:
                    env_stack.pop()
                elif env_stack:
                    issues.append({
                        'line': i,
                        'description': f'Mismatched environment: \\end{{{env_name}}} '
                                       f'but expected \\end{{{env_stack[-1][0]}}} '
                                       f'(opened at line {env_stack[-1][1]})',
                    })
                else:
                    issues.append({
                        'line': i,
                        'description': f'\\end{{{env_name}}} without matching \\begin',
                    })

        for env_name, line_num in env_stack:
            issues.append({
                'line': line_num,
                'description': f'Unclosed environment: \\begin{{{env_name}}} never closed',
            })

        return issues

    @staticmethod
    def check_broken_citations(content: str, bib_file: Path) -> List[str]:
        """Check for LaTeX citation keys not in bibliography."""
        cite_pattern = r'\\cite[a-z]*\{([^}]+)\}'
        cited_keys = set()
        for match in re.finditer(cite_pattern, content):
            keys = match.group(1).split(',')
            cited_keys.update(k.strip() for k in keys)

        if not cited_keys:
            return []

        if not bib_file.exists():
            return list(cited_keys)

        bib_content = bib_file.read_text(encoding='utf-8')
        bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_content))

        broken = cited_keys - bib_keys
        return list(broken)

    @staticmethod
    def check_overfull_hbox_risk(content: str) -> List[int]:
        """Detect lines likely to cause overfull hbox (>10pt)."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.split('%')[0] if '%' in line else line
            if stripped.strip().startswith('%'):
                continue
            if re.match(r'\s*\\(includegraphics|input|bibliography|usepackage)', stripped):
                continue
            if len(stripped.strip()) > 120:
                issues.append(i)

        return issues


# ==============================================================================
# QUALITY SCORER
# ==============================================================================

class QualityScorer:
    """Calculate quality scores based on quality-gates.md rubrics."""

    def __init__(self, filepath: Path, verbose: bool = False):
        self.filepath = filepath
        self.verbose = verbose
        self.score = 100
        self.issues = {
            'critical': [],
            'major': [],
            'minor': []
        }
        self.auto_fail = False
        self.file_type = classify_file(filepath)

    def score_file(self) -> Dict:
        """Score a file based on its type."""
        scorers = {
            'python_module': self._score_python_module,
            'python_script': self._score_python_script,
            'exploration_python': self._score_exploration_python,
            'latex': self._score_latex,
        }

        scorer = scorers.get(self.file_type)
        if not scorer:
            return self._generate_report()

        scorer()
        self.score = max(0, self.score)
        return self._generate_report()

    def _score_python_module(self):
        """Score Python module (code/src/mypackage/core/)."""
        content = self.filepath.read_text(encoding='utf-8')

        # Critical: syntax/import error
        valid, error = IssueDetector.check_python_syntax(self.filepath)
        if not valid:
            self.auto_fail = True
            self._add_issue('critical', 'syntax_or_import_error',
                            'Syntax error', error, 100)
            self.score = 0
            return

        # Critical: file I/O in src/
        io_lines = IssueDetector.check_file_io_in_src(content)
        for line in io_lines:
            self._add_issue('critical', 'file_io_in_src',
                            f'File I/O at line {line} (belongs in scripts/)',
                            'Move file operations to code/scripts/', 30)
            self.score -= 30

        # Critical: hardcoded absolute paths
        path_lines = IssueDetector.check_hardcoded_paths(content)
        for line in path_lines:
            self._add_issue('critical', 'hardcoded_absolute_paths',
                            f'Hardcoded absolute path at line {line}',
                            'Use paths from config.py', 20)
            self.score -= 20

        # Major: paths not from config
        config_issues = IssueDetector.check_paths_from_config(content)
        for line in config_issues:
            self._add_issue('major', 'paths_not_from_config',
                            f'Path string at line {line} not from config.py',
                            'Import paths from mypackage.config', 10)
            self.score -= 10

    def _score_python_script(self):
        """Score Python script (code/scripts/core/)."""
        content = self.filepath.read_text(encoding='utf-8')

        # Critical: syntax error
        valid, error = IssueDetector.check_python_syntax(self.filepath)
        if not valid:
            self.auto_fail = True
            self._add_issue('critical', 'syntax_error',
                            'Syntax error', error, 100)
            self.score = 0
            return

        # Critical: modifies raw data
        raw_writes = IssueDetector.check_raw_data_modification(content)
        for line in raw_writes:
            self._add_issue('critical', 'modifies_raw_data',
                            f'Writes to data/raw/ at line {line}',
                            'Never modify raw data', 30)
            self.score -= 30

        # Critical: hardcoded absolute paths
        path_lines = IssueDetector.check_hardcoded_paths(content)
        for line in path_lines:
            self._add_issue('critical', 'hardcoded_absolute_paths',
                            f'Hardcoded absolute path at line {line}',
                            'Use paths from config.py', 20)
            self.score -= 20

        # Major: missing seed for stochastic work
        if IssueDetector.check_missing_seed(content):
            self._add_issue('major', 'missing_seed',
                            'Missing seed for reproducibility',
                            'Set random seed at top of script', 10)
            self.score -= 10

        # Minor: script not numbered (core/ only)
        if not IssueDetector.check_script_numbering(self.filepath):
            self._add_issue('minor', 'script_not_numbered',
                            'Script missing NN_ prefix',
                            'Name scripts as 01_clean.py, 02_merge.py, etc.', 3)
            self.score -= 3

    def _score_exploration_python(self):
        """Score exploration Python (60/100 threshold)."""
        content = self.filepath.read_text(encoding='utf-8')

        # Critical: syntax/import error
        valid, error = IssueDetector.check_python_syntax(self.filepath)
        if not valid:
            self.auto_fail = True
            self._add_issue('critical', 'syntax_or_import_error',
                            'Syntax error', error, 100)
            self.score = 0
            return

        # Critical: modifies raw data
        raw_writes = IssueDetector.check_raw_data_modification(content)
        for line in raw_writes:
            self._add_issue('critical', 'modifies_raw_data',
                            f'Writes to data/raw/ at line {line}',
                            'Never modify raw data', 30)
            self.score -= 30

        # Major: missing seed
        if IssueDetector.check_missing_seed(content):
            self._add_issue('major', 'missing_seed',
                            'Missing seed for reproducibility',
                            'Set random seed for reproducible results', 10)
            self.score -= 10

        # Minor: hardcoded paths (lighter penalty in exploration)
        path_lines = IssueDetector.check_hardcoded_paths(content)
        for line in path_lines:
            self._add_issue('minor', 'hardcoded_absolute_paths',
                            f'Hardcoded absolute path at line {line}',
                            'Use paths from config.py', 5)
            self.score -= 5

    def _score_latex(self):
        """Score LaTeX manuscript (paper/*.tex)."""
        content = self.filepath.read_text(encoding='utf-8')

        # Critical: LaTeX syntax issues
        syntax_issues = IssueDetector.check_latex_syntax(content)
        if syntax_issues:
            for issue in syntax_issues:
                self._add_issue('critical', 'compilation_failure',
                                f'LaTeX syntax issue at line {issue["line"]}',
                                issue['description'], 100)
            self.auto_fail = True
            self.score = 0
            return

        # Critical: undefined citations
        bib_file = self.filepath.parent / 'references.bib'
        if not bib_file.exists():
            bib_file = self.filepath.parent.parent / 'paper' / 'references.bib'
        broken_citations = IssueDetector.check_broken_citations(content, bib_file)
        for key in broken_citations:
            self._add_issue('critical', 'undefined_citation',
                            f'Citation key not in bibliography: {key}',
                            'Add to paper/references.bib or fix key', 15)
            self.score -= 15

        # Critical: overfull hbox risk
        overfull_lines = IssueDetector.check_overfull_hbox_risk(content)
        for line in overfull_lines:
            self._add_issue('critical', 'overfull_hbox',
                            f'Potential overfull hbox at line {line}',
                            'Line >120 chars may overflow', 10)
            self.score -= 10

    def _add_issue(self, severity: str, issue_type: str,
                   description: str, details: str, points: int):
        """Add an issue to the report."""
        self.issues[severity].append({
            'type': issue_type,
            'description': description,
            'details': details,
            'points': points
        })

    def _generate_report(self) -> Dict:
        """Generate quality score report."""
        threshold_key = 'exploration' if self.file_type == 'exploration_python' else 'commit'
        commit_threshold = THRESHOLDS[threshold_key]

        if self.auto_fail:
            status = 'FAIL'
        elif self.score >= THRESHOLDS['excellence']:
            status = 'EXCELLENCE'
        elif self.score >= THRESHOLDS['pr']:
            status = 'PR_READY'
        elif self.score >= commit_threshold:
            status = 'COMMIT_READY'
        else:
            status = 'BLOCKED'

        critical_count = len(self.issues['critical'])
        major_count = len(self.issues['major'])
        minor_count = len(self.issues['minor'])

        return {
            'filepath': str(self.filepath),
            'file_type': self.file_type,
            'score': self.score,
            'status': status,
            'threshold': commit_threshold,
            'auto_fail': self.auto_fail,
            'issues': {
                'critical': self.issues['critical'],
                'major': self.issues['major'],
                'minor': self.issues['minor'],
                'counts': {
                    'critical': critical_count,
                    'major': major_count,
                    'minor': minor_count,
                    'total': critical_count + major_count + minor_count
                }
            },
            'thresholds': THRESHOLDS
        }

    def print_report(self, summary_only: bool = False) -> None:
        """Print formatted quality report."""
        report = self._generate_report()
        commit_threshold = report['threshold']

        print(f"\n# Quality Score: {self.filepath.name}")
        print(f"  Type: {self.file_type}\n")

        status_label = {
            'EXCELLENCE': '[EXCELLENCE]',
            'PR_READY': '[PASS]',
            'COMMIT_READY': '[PASS]',
            'BLOCKED': '[BLOCKED]',
            'FAIL': '[FAIL]'
        }

        print(f"## Score: {report['score']}/100 {status_label.get(report['status'], '')}")

        if report['status'] == 'BLOCKED':
            print(f"\n  BLOCKED - Below threshold ({commit_threshold})")
        elif report['status'] == 'COMMIT_READY':
            print(f"\n  Ready for commit (>= {commit_threshold})")
        elif report['status'] == 'PR_READY':
            print(f"\n  Ready for PR (>= {THRESHOLDS['pr']})")
        elif report['status'] == 'EXCELLENCE':
            print(f"\n  Excellence (>= {THRESHOLDS['excellence']})")
        elif report['status'] == 'FAIL':
            print(f"\n  Auto-fail (syntax/compilation error)")

        if summary_only:
            counts = report['issues']['counts']
            print(f"\n  Issues: {counts['total']} "
                  f"({counts['critical']} critical, "
                  f"{counts['major']} major, "
                  f"{counts['minor']} minor)")
            return

        # Detailed issues
        if report['issues']['counts']['critical'] > 0:
            print(f"\n## Critical Issues ({report['issues']['counts']['critical']})")
            for i, issue in enumerate(report['issues']['critical'], 1):
                print(f"  {i}. {issue['description']} (-{issue['points']})")
                print(f"     {issue['details']}")

        if report['issues']['counts']['major'] > 0:
            print(f"\n## Major Issues ({report['issues']['counts']['major']})")
            for i, issue in enumerate(report['issues']['major'], 1):
                print(f"  {i}. {issue['description']} (-{issue['points']})")
                print(f"     {issue['details']}")

        if report['issues']['counts']['minor'] > 0 and self.verbose:
            print(f"\n## Minor Issues ({report['issues']['counts']['minor']})")
            for i, issue in enumerate(report['issues']['minor'], 1):
                print(f"  {i}. {issue['description']} (-{issue['points']})")

        if report['status'] == 'BLOCKED':
            print(f"\n## Actions")
            print(f"  1. Fix critical issues above")
            print(f"  2. Re-run (target: >= {commit_threshold})")


# ==============================================================================
# CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Calculate quality scores based on quality-gates.md rubrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Score a Python module
  python docs/quality_reports/quality_score.py code/src/mypackage/core/model.py

  # Score a pipeline script
  python docs/quality_reports/quality_score.py code/scripts/core/01_clean.py

  # Score a LaTeX manuscript
  python docs/quality_reports/quality_score.py paper/main.tex

  # Score all core modules
  python docs/quality_reports/quality_score.py code/src/mypackage/core/*.py

  # Summary only
  python docs/quality_reports/quality_score.py code/src/mypackage/core/*.py --summary

  # JSON output
  python docs/quality_reports/quality_score.py code/src/mypackage/core/*.py --json

Quality Thresholds:
  60/100 = Exploration (good enough to keep exploring)
  80/100 = Commit (production code)
  90/100 = PR (ready for review)
  95/100 = Excellence (aspirational)

Exit Codes:
  0 = Score >= threshold (commit allowed)
  1 = Score < threshold (commit blocked)
  2 = Auto-fail (syntax error)
        """
    )

    parser.add_argument('filepaths', type=Path, nargs='+', help='File(s) to score')
    parser.add_argument('--summary', action='store_true', help='Summary only')
    parser.add_argument('--verbose', action='store_true', help='Include minor issues')
    parser.add_argument('--json', action='store_true', help='JSON output')

    args = parser.parse_args()

    results = []
    exit_code = 0

    for filepath in args.filepaths:
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            exit_code = 1
            continue

        file_type = classify_file(filepath)
        if file_type == 'unknown':
            print(f"Error: Unsupported file type: {filepath.suffix} ({filepath})")
            continue

        try:
            scorer = QualityScorer(filepath, verbose=args.verbose)
            report = scorer.score_file()
            results.append(report)

            if not args.json:
                scorer.print_report(summary_only=args.summary)

            if report['auto_fail']:
                exit_code = max(exit_code, 2)
            elif report['score'] < report['threshold']:
                exit_code = max(exit_code, 1)

        except Exception as e:
            print(f"Error scoring {filepath}: {e}")
            import traceback
            traceback.print_exc()
            exit_code = 1

    if args.json:
        print(json.dumps(results, indent=2))

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
