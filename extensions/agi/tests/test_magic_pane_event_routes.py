"""goal:g7.16.1.7.3.1 — event-kind → one-route table SoT (pane-as-post-anchor).

Non-destructive census fixture: one row per event kind, target_route is always
tool_call_turn, and the four delivery routes measured on goal:g7.16.1.7.3 appear
as legacy_routes. Messaging adapter stays out of this SoT (g7.32.2* owns that).
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
TARGET = "tool_call_turn"
THIS = Path(__file__).resolve()


def _load() -> dict:
    return json.loads(FIX.read_text(encoding="utf-8"))


def test_fixture_has_unique_required_kinds():
    data = _load()
    required = data["required_kinds"]
    rows = data["routes"]
    kinds = [r["event_kind"] for r in rows]
    assert len(kinds) == len(set(kinds)), f"duplicate event_kind in routes: {kinds}"
    assert set(kinds) == set(required), (
        f"routes kinds {sorted(kinds)} != required {sorted(required)}"
    )


def test_every_target_route_is_tool_call_turn():
    data = _load()
    bad = [r for r in data["routes"] if r.get("target_route") != TARGET]
    assert not bad, f"non-{TARGET} rows: {bad}"


def test_parent_measured_legacy_routes_appear():
    data = _load()
    measured = set(data["parent_measured_legacy_routes"])
    seen: set[str] = set()
    for r in data["routes"]:
        seen.update(r.get("legacy_routes") or [])
    missing = measured - seen
    assert not missing, f"parent-measured legacy routes absent from table: {sorted(missing)}"


def test_fixture_and_test_do_not_import_messaging_adapter():
    """Negative falsifier: this SoT is not messaging integration."""
    tree = ast.parse(THIS.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    assert "adapters" not in imported
    assert "magic_pane" not in imported
    assert "send" not in imported
    fix = FIX.read_text(encoding="utf-8")
    assert "import " not in fix
    assert "send.py" not in fix
