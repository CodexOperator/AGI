"""goal:g7.16.1.7.3.4 — legacy-route cutover (inject+poll = THE path).

Falsifiers:
1. route_table: one active_route=tool_call_turn per v2 event kind; legacy only under legacy_bypassed.
2. deliver(kind, body) → enqueue via inject; idle poll returns tool_call_turn with kind_tag + tool_return.
3. refuse_legacy_delivery / assert_not_legacy raises for each parent-measured legacy route.
4. free_lane_probe still pi/free + pi.toml; no second pi template.
5. Negative: cutover helper + this test import neither adapters.magic_pane nor send transport.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import magic_pane_cutover as cut  # noqa: E402
import magic_pane_inject as inj  # noqa: E402
import magic_pane_poll as poll  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_cutover.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _data():
    return cut.load_cutover(FIX)


def test_route_table_one_active_per_kind_legacy_only_bypassed():
    data = _data()
    table = cut.route_table(data=data)
    required = data["required_kinds"]
    assert [r["event_kind"] for r in table] == [
        r["event_kind"] for r in data["routes"]
    ]
    assert {r["event_kind"] for r in table} == set(required)
    measured = set(data["parent_measured_legacy_routes"])
    seen_legacy: set[str] = set()
    for row in table:
        assert row["active_route"] == "tool_call_turn"
        assert row["channel"] in {"dm", "engine"}
        assert row["kind_tag"].startswith(row["channel"] + ".")
        for name in row["legacy_bypassed"]:
            assert name in cut.LEGACY_ROUTES
            st = cut.legacy_status(name, data=data)
            assert st["status"] == "bypassed"
            assert st["replaced_by"] == "tool_call_turn"
            seen_legacy.add(name)
    assert seen_legacy == measured


def test_deliver_uses_inject_poll_only_path(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:cutover"
    for row in data["routes"]:
        kind = row["event_kind"]
        body = f"CUTOVER:{kind}"
        path = cut.deliver(root, post, kind, body, routes=data)
        assert path.is_file()
    got = poll.poll(root, post, busy=False)
    assert len(got) == len(data["routes"])
    for delivery, row in zip(got, data["routes"]):
        assert delivery["target_route"] == "tool_call_turn"
        assert delivery["message_is"] == "tool_return"
        assert delivery["kind_tag"] == row["kind_tag"]
        assert delivery["channel"] == row["channel"]
        assert delivery["tool_return"] == f"CUTOVER:{row['event_kind']}"
        assert inj.tool_return_payload(delivery) == delivery["tool_return"]


def test_legacy_routes_refused():
    for name in sorted(cut.LEGACY_ROUTES):
        with pytest.raises(cut.MagicPaneCutoverError, match="bypassed"):
            cut.assert_not_legacy(name)
        with pytest.raises(cut.MagicPaneCutoverError, match="bypassed"):
            cut.refuse_legacy_delivery(name, post="x", body="y")
    # unknown non-active also refused
    with pytest.raises(cut.MagicPaneCutoverError, match="non-active|unknown"):
        cut.assert_not_legacy("some_other_paste_path")
    # active route is allowed through the gate
    cut.assert_not_legacy("tool_call_turn")


def test_busy_respected_through_cutover_deliver(tmp_path):
    root = tmp_path / "pane"
    post = "post:busy-cut"
    data = _data()
    cut.deliver(root, post, "memory_alarm", "HOLD", routes=data)
    poll.mark_busy(root, post)
    assert poll.poll(root, post) == []
    assert poll.pending_count(root, post) == 1
    poll.mark_idle(root, post)
    got = poll.poll(root, post)
    assert len(got) == 1
    assert got[0]["tool_return"] == "HOLD"
    assert got[0]["kind_tag"] == "engine.memory_alarm"


def test_free_lane_probe_one_pi_toml():
    lane = cut.free_lane_probe()
    assert lane["harness"] == "pi"
    assert lane["row"] == "free"
    assert lane["template"].endswith("pi.toml")
    assert lane["alias"] == "pi-free"
    assert PI_TOML.is_file()
    extras = [p.name for p in PI_TOML.parent.glob("pi-*.toml")]
    assert extras == [], extras


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module)
    return imported


def test_helper_and_test_do_not_import_messaging_or_send():
    for path in (HELPER, THIS):
        imported = _imported_modules(path)
        parts: set[str] = set()
        for name in imported:
            parts.add(name)
            parts.add(name.split(".")[0])
            parts.update(name.split("."))
        assert "adapters" not in parts, (path.name, imported)
        assert "send" not in parts, (path.name, imported)
        # bare magic_pane = messaging leaf; magic_pane_inject/poll/cutover ok
        assert "magic_pane" not in parts, (path.name, imported)
