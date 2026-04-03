"""Entry point for the avian expert system GUI."""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
PYKE_DIR = ROOT_DIR / "pyke-master"

for path in (SRC_DIR, PYKE_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from animal_expert_system.gui import run_app


if __name__ == "__main__":
    run_app()
