"""goal:g7.16.1.7.3.1 — event-kind → one-route table SoT (pane-as-post-anchor).

Owner update: uniform tool-call turn; tool RETURN is the message; always tagged
DM vs engine. Build lane = ONE-pi free row via pi_adapter + harness template;
CC-compat via pi extension events that mirror CC hooks.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
TARGET = "tool_call_turn"
CHANNELS = {"dm", "engine"}
THIS = Path(__file__).resolve()


def _load() -> dict:
    return json.loads(FIX.read_text(encoding="utf-8"))


def test_fixture_has_unique_required_kinds():
    data = _load()
    required = data["required_kinds"]
    rows = data["routes"]
    kinds = [r["event_kind"] for r in rows]
    assert len(kinds) == len(set(kinds)), f"duplicate event_kind in routes: {kinds}"
    assert set(kinds) == set(required)


def test_every_target_route_is_tool_call_turn():
    data = _load()
    bad = [r for r in data["routes"] if r.get("target_route") != TARGET]
    assert not bad, f"non-{TARGET} rows: {bad}"


def test_inject_contract_tool_return_is_message():
    data = _load()
    inj = data["inject"]
    assert inj["shape"] == "tool_call_turn"
    assert inj["message_is"] == "tool_return"
    assert set(inj["channels"]) == CHANNELS


def test_every_row_tagged_dm_or_engine_with_kind_tag():
    data = _load()
    for r in data["routes"]:
        assert r["channel"] in CHANNELS, r
        assert r["kind_tag"].startswith(r["channel"] + "."), r
        assert r["event_kind"] in r["kind_tag"], r


def test_parent_measured_legacy_routes_appear():
    data = _load()
    measured = set(data["parent_measured_legacy_routes"])
    seen: set[str] = set()
    for r in data["routes"]:
        seen.update(r.get("legacy_routes") or [])
    missing = measured - seen
    assert not missing, sorted(missing)


def test_build_lane_names_one_pi_free_and_cc_compat():
    data = _load()
    lane = data["build_lane"]
    assert lane["harness"] == "pi"
    assert lane["row"] == "free"
    assert lane["adapter"].endswith("pi_adapter.py")
    assert lane["template"].endswith("pi.toml")
    assert "session_start" in lane["cc_compat"]
    assert Path(lane["adapter"]).exists()
    assert Path(lane["template"]).exists()


def test_fixture_and_test_do_not_import_messaging_adapter():
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
