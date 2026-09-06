"""Regression: .agi/bin/ must not exist (goal:s4 / CLAUDE.md rule S1).

CLAUDE.md specifies that driver.sh prefers <project-root>/bin/{scripts}.py
over the engine's own, and .agi/bin/ is forbidden — it is a staging area that
can shadow safe engine scripts (S1). The lone file that lived there
(analyze-chat-structure.py) has been re-homed to extensions/agi/bin/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402


def test_agi_bin_directory_does_not_exist() -> None:
    """Assert no .agi/bin/ directory exists anywhere in the project tree."""
    root = locations.find_project_root(Path(__file__).resolve())
    agi_bin = root / ".agi" / "bin"
    assert not agi_bin.exists(), f"Forbidden directory exists: {agi_bin}"