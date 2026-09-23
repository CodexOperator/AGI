"""goal:g7.32.4 — pin send.py's coupling to the rotate/dispatch orchestration modules.

Nothing here imports send.py, tmux or the network: the census is pure `ast` over
the committed source, so it stays cheap and cannot flake on a missing runtime.
A change in EITHER direction (new coupling or removed coupling) fails the pin,
which is the point: extraction of these six helpers is then a deliberate,
visible event rather than a silent drift.
"""

from __future__ import annotations

import ast
from pathlib import Path

# extensions/agi/tests/test_send_router_thinness.py -> extensions/agi/bin/send.py
SEND_PY = Path(__file__).resolve().parents[2] / "agi" / "bin" / "send.py"


def census(path=None) -> dict:
    """Parse send.py; return its rotate/dispatch coupling as four lists.

    module_level: sorted ["rotate"/"dispatch"] imported in the TOP-LEVEL body.
    lazy_imports: sorted "rotate@613" style strings for imports inside any
                  function/class body (walk every node, but classify top-level
                  body separately).
    rotate_attrs / dispatch_attrs: sorted attribute names read off a Name node
                  whose id is "rotate"/"dispatch".
    """
    src_path = Path(path) if path is not None else SEND_PY
    assert src_path.is_file(), f"send.py not found: {src_path}"
    tree = ast.parse(src_path.read_text(encoding="utf-8"))

    module_level: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            module_level += [a.name for a in node.names if a.name in ("rotate", "dispatch")]
        elif isinstance(node, ast.ImportFrom):
            if node.module in ("rotate", "dispatch"):
                module_level.append(node.module)

    lazy_imports: list[str] = []
    rotate_attrs: set[str] = set()
    dispatch_attrs: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name in ("rotate", "dispatch") and node not in tree.body:
                    lazy_imports.append(f"{a.name}@{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if node.module in ("rotate", "dispatch") and node not in tree.body:
                lazy_imports.append(f"{node.module}@{node.lineno}")
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "rotate":
                rotate_attrs.add(node.attr)
            elif node.value.id == "dispatch":
                dispatch_attrs.add(node.attr)

    return {
        "module_level": sorted(module_level),
        "lazy_imports": sorted(lazy_imports),
        "rotate_attrs": sorted(rotate_attrs),
        "dispatch_attrs": sorted(dispatch_attrs),
    }


def test_no_module_level_rotate_or_dispatch_import():
    assert census()["module_level"] == []


def test_census_is_pinned():
    got = census()
    # sorted() is lexicographic, so the line numbers are not in numeric order.
    assert got["lazy_imports"] == [
        "rotate@1580",  # in _row_is_quiet: _normalize_settings
        "rotate@1608",  # in _row_is_quiet_system: _normalize_settings
        "rotate@2188",  # in _nudge_target: DEFAULT_TMUX_SESSION
        "rotate@613",   # in _commit_push_seat_row: _commit_spawn_row
        "rotate@727",   # in _commit_push_all_live: _git_toplevel
        "rotate@825",   # in _run_pending_swap_completion: _finish_pending_swap_on_push
        "rotate@843",   # in _all_live_origin_sync_line: _git_toplevel
    ]
    assert got["rotate_attrs"] == [
        "DEFAULT_TMUX_SESSION",          # constant: default tmux session name
        "_commit_spawn_row",             # persistence: commit a spawned seat row
        "_finish_pending_swap_on_push",  # persistence: finalize a deferred swap
        "_git_toplevel",                 # helper: resolve the git root
        "_normalize_settings",           # helper: parse a row's settings tokens
        "_push_season_branch",           # persistence: push the season branch
    ]
    assert got["dispatch_attrs"] == []


def test_census_shape():
    got = census()
    assert sorted(got) == ["dispatch_attrs", "lazy_imports", "module_level", "rotate_attrs"]
    assert all(isinstance(v, list) for v in got.values())
