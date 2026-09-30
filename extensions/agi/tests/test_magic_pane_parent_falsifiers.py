"""goal:g7.16.1.7.3.9 — parent falsifiers #1+#3+#4 (idle multi-event · N-post box-fetch · legacy zero).

Falsifiers:
1. prove_idle_multi_event → memory_alarm + message_receipt + rotation_prompt
   each idle-delivered as tool_call_turn with kind_tag + tool_return.
3. prove_n_post_single_box_fetch(N=3) → box_network_pulls==1; pane_network_pulls==0.
4. prove_legacy_route_zero → all LEGACY_ROUTES refuse; 0 legacy deliveries;
   route_table one active per kind; cutover positive control still works.
5. prove_parent_falsifiers_134 combines 1+3+4; free_lane + pi_adapter REQUIRED-only.
6. Negative: helper + tests import neither adapters.magic_pane nor send transport;
   parent g7.16.1.7.3 stays horizon.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
NODES = ROOT / ".agi" / "nodes" / "goal"
sys.path.insert(0, str(BIN))

import magic_pane_cutover as cut  # noqa: E402
import magic_pane_parent_falsifiers as pf  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_parent_falsifiers.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _data():
    return cut.load_cutover(FIX)


def test_idle_multi_event_tool_call_turn(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    out = pf.prove_idle_multi_event(root, "post:idle", routes=data)
    assert out["action"] == "prove_idle_multi_event"
    assert out["kinds"] == [
        "memory_alarm",
        "message_receipt",
        "rotation_prompt",
    ]
    assert out["kind_tags"] == [
        "engine.memory_alarm",
        "dm.message_receipt",
        "engine.rotation_prompt",
    ]
    assert out["count"] == 3
    assert out["idle"] is True
    for d, tag, kind in zip(
        out["deliveries"], out["kind_tags"], out["kinds"]
    ):
        assert d["target_route"] == "tool_call_turn"
        assert d["message_is"] == "tool_return"
        assert d["inject_shape"] == "tool_call_turn"
        assert d["kind_tag"] == tag
        assert d["tool_return"] == f"IDLE-MULTI:{kind}"


def test_n_post_single_box_fetch(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    posts = ["post:a", "post:b", "post:c"]
    out = pf.prove_n_post_single_box_fetch(root, posts, routes=data)
    assert out["n_posts"] == 3
    assert out["box_network_pulls"] == 1
    assert out["pane_network_pulls"] == 0
    assert out["fetch"]["fetch_count"] == 1
    assert out["fetch"]["moved_count"] == 3
    for post in posts:
        assert len(out["deliveries"][post]) == 1
        assert out["deliveries"][post][0]["target_route"] == "tool_call_turn"


def test_n_post_requires_at_least_two(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    with pytest.raises(pf.MagicPaneParentFalsifierError, match="N>=2"):
        pf.prove_n_post_single_box_fetch(root, ["post:only"], routes=data)


def test_legacy_route_zero(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    out = pf.prove_legacy_route_zero(root, "post:leg0", routes=data)
    assert out["legacy_events_delivered"] == 0
    assert set(out["legacy_routes_refused"]) == set(cut.LEGACY_ROUTES)
    assert out["active_route"] == "tool_call_turn"
    assert out["cutover_positive_control"]["tool_return"] == "VIA-CUTOVER"
    assert "memory_alarm" in out["route_table_kinds"]


def test_combined_prove_and_lane_probes(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    out = pf.prove_parent_falsifiers_134(root, routes=data)
    assert out["goal"] == "goal:g7.16.1.7.3.9"
    assert out["falsifiers_closed"] == [1, 3, 4]
    assert out["parent_stays_horizon"] is True
    assert out["live_tmux"] is False
    assert out["idle_multi_event"]["count"] == 3
    assert out["n_post_single_box_fetch"]["box_network_pulls"] == 1
    assert out["legacy_route_zero"]["legacy_events_delivered"] == 0

    lane = pf.free_lane_probe()
    assert lane["harness"] == "pi" and lane["row"] == "free"
    assert lane["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    assert list(PI_TOML.parent.glob("pi*.toml")) == [PI_TOML]
    probe = pf.pi_adapter_probe()
    assert probe["required_ok"] is True
    assert probe["pane_interface"] == []
    block = data["cutover"]["parent_falsifiers_134"]
    assert block["goal"] == "goal:g7.16.1.7.3.9"
    assert block["entry"] == "prove_parent_falsifiers_134"
    assert block["falsifiers_closed"] == [1, 3, 4]


def test_parent_stays_horizon_and_no_messaging_imports():
    parent = NODES / "g7.16.1.7.3.md"
    text = parent.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    assert "status: horizon" in fm
    assert "goal:g7.16.1.7.3.9" in fm  # seeded
    for path in (HELPER, THIS):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        parts: set[str] = set()
        for name in imported:
            parts.add(name)
            parts.add(name.split(".")[0])
            parts.update(name.split("."))
        assert "send" not in parts, (path.name, imported)
        assert "magic_pane" not in parts, (path.name, imported)
        assert "adapters.magic_pane" not in imported
