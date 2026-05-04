"""Pytest conftest — adds src/ to sys.path for clean test imports."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
