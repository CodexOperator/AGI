"""goal:g7.32.4 falsifier 1 -- send.py carries ZERO `import rotate`; every
rotate-dependent call it makes goes through the sibling seam module
(`send_seat_seam`), and the seam still reaches the REAL rotate functions.

A BOUNDARY, not a decoupling: send_seat_seam imports rotate, so rotate stays
on send.py's import graph through exactly one edge.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


def test_send_py_carries_no_import_rotate_or_dispatch():
    """AST, not substring: a `from rotate import foo` slips past
    `"import rotate" not in src` because that substring never appears
    (goal:g7.32.4 R2). Parse the module and refuse the NAME in any
    Import / ImportFrom node -- `from rotate import x`, `import rotate`,
    and `import rotate.x` all fail alike.
    """
    tree = ast.parse((BIN / "send.py").read_text())
    hit = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            hit += [a.name for a in node.names
                    if a.name.split(".")[0] in ("rotate", "dispatch")]
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in (
                    "rotate", "dispatch"):
                hit.append(node.module)
    assert hit == [], f"send.py imports orchestration: {hit}"


def test_seam_owns_the_orchestration_call_and_reaches_real_rotate(
        monkeypatch, tmp_path):
    """The four orchestration CALLS moved into the seam: monkeypatch
    rotate._commit_spawn_row and keygen's own-row path must call it through
    the seam."""
    import rotate

    calls = []

    def fake(root, *, seat, generation, session_id, window, pid):
        calls.append((root, seat, generation, session_id, window, pid))
        return "committed seat row"

    monkeypatch.setattr(rotate, "_commit_spawn_row", fake)
    send_mod._commit_push_seat_row(
        tmp_path,
        {"generation": 7, "session_id": "s1", "window": "@1", "pid": 42},
        "seat-a", "keygen")
    assert calls == [(tmp_path, "seat-a", 7, "s1", "@1", 42)]


def test_seam_normalize_settings_and_session_reach_real_rotate(monkeypatch):
    import rotate
    import send_seat_seam

    monkeypatch.setattr(
        rotate, "_normalize_settings",
        lambda s: {"quiet": True} if s == "quiet" else {})
    assert send_seat_seam.normalize_settings("quiet") == {"quiet": True}
    assert send_seat_seam.DEFAULT_TMUX_SESSION == rotate.DEFAULT_TMUX_SESSION