from pathlib import Path

def _find_root():
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    raise FileNotFoundError("Could not find project root")

ROOT = _find_root()

RAW = ROOT / "data" / "raw"
INTERMEDIATE = ROOT / "data" / "intermediate"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "output" / "tables"
FIGURES = ROOT / "output" / "figures"
