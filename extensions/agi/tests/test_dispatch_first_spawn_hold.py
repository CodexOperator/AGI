"""Falsifier for goal:g7.31.1.2.2: first-spawn pane hold.

The production first-spawn path must not silently use a direct Popen while
only the restart path has a tmux-hold seam.  This test is deliberately a
negative wire test: it inspects the actual dispatch.py source and fails if
_open_round has acquired a hold/start call without the corresponding test
seam.  It is intentionally named as a falsifier, not a positive claim.
"""
from __future__ import annotations

import ast
from pathlib import Path

DISPATCH = Path(__file__).resolve().parents[1] / "bin" / "dispatch.py"


def _open_round_source() -> str:
    tree = ast.parse(DISPATCH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_open_round":
            return ast.get_source_segment(DISPATCH.read_text(encoding="utf-8"), node) or ""
    raise AssertionError("dispatch.py no longer has _open_round")


def test_first_spawn_has_no_named_hold_seam_negative_falsifier():
    """Record the current first-spawn wire: direct Popen, no tmux hold."""
    source = _open_round_source()
    assert "subprocess.Popen" in source
    assert "tmux_hold" not in source
    assert "pane_id" not in source
