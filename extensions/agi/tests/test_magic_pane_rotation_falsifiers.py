"""goal:g7.16.1.7.3.8 — live pane-id×rotation falsifiers (dry-safe).

Falsifiers:
1. prove_pane_rotations(n=3) → ONE pane_id survives; generation==3; orphans==0.
2. mismatched pane_id on rotate raises survival; orphans stay 0 (no second pin).
3. each rotate drains engine.rotation_prompt tool_call_turn.
4. free_lane_probe pi/free + pi.toml; pi_adapter REQUIRED-only.
5. Negative: proof/tests import neither adapters.magic_pane nor send transport;
   prove_pane_rotations(dry=False) refuses; parent g7.16.1.7.3 stays horizon.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
NODES = ROOT / ".agi" / "nodes" / "goal"
sys.path.insert(0, str(BIN))

import magic_pane_cutover as cut  # noqa: E402
import magic_pane_lifecycle as life  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_lifecycle.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _data():
    return cut.load_cutover(FIX)


def test_three_rotations_one_pane_id_zero_orphans(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    post = "seat-rot3"
    out = life.prove_pane_rotations(
        root, post, n=3, routes=data, dry=True
    )
    assert out["action"] == "prove_pane_rotations"
    assert out["pane_id"] == life.dry_pane_id(post)
    assert out["rotations"] == 3
    assert out["final_generation"] == 3
    assert out["generations"] == [0, 1, 2, 3]
    assert out["orphan_count"] == 0
    assert out["pin_count"] == 1
    assert out["live_tmux"] is False
    assert out["drained_kind_tags"] == [
        "engine.rotation_prompt",
        "engine.rotation_prompt",
        "engine.rotation_prompt",
    ]
    pin = life.get_pane(root, post)
    assert pin["pane_id"] == out["pane_id"]
    assert pin["generation"] == 3
    census = life.orphan_pane_census(root, post)
    assert census["orphan_count"] == 0 and census["pin_count"] == 1


def test_mismatched_pane_id_refuses_and_no_orphan(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    post = "seat-orphan"
    life.from_stand_up(root, post, "spawn", routes=data, dry=True)
    have = life.get_pane(root, post)["pane_id"]
    with pytest.raises(life.MagicPaneLifecycleError, match="survival"):
        life.from_stand_up(
            root, post, "rotate", pane_id="dry:OTHER", routes=data, dry=True
        )
    # pin unchanged; no second file
    pin = life.get_pane(root, post)
    assert pin["pane_id"] == have
    assert pin["generation"] == 0  # rotate never applied
    census = life.orphan_pane_census(root, post)
    assert census["orphan_count"] == 0
    assert census["pin_count"] == 1
    posts = root / "posts" / post
    assert list(posts.glob("pane*.json")) == [posts / "pane.json"]


def test_orphan_census_flags_extra_pane_file(tmp_path):
    root = tmp_path / "agi"
    post = "seat-dup"
    life.register_pane(root, post, "dry:a", dry=True)
    # plant a second pin file (orphan)
    extra = root / "posts" / post / "pane-orphan.json"
    extra.write_text(
        json.dumps({"post_id": post, "pane_id": "dry:b", "generation": 0}),
        encoding="utf-8",
    )
    census = life.orphan_pane_census(root, post)
    assert census["orphan_count"] == 1
    assert post in census["orphans"]
    assert census["pin_count"] == 2


def test_prove_refuses_non_dry_and_free_lane():
    with pytest.raises(life.MagicPaneLifecycleError, match="deferred"):
        life.prove_pane_rotations(Path("/tmp"), "p", n=3, dry=False)
    spec = life.free_lane_probe()
    assert spec["harness"] == "pi" and spec["row"] == "free"
    assert spec["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    assert list(PI_TOML.parent.glob("pi*.toml")) == [PI_TOML]
    probe = life.pi_adapter_probe()
    assert probe["required_ok"] is True
    assert probe["pane_interface"] == []
    data = _data()
    pr = data["cutover"]["pane_rotation_falsifiers"]
    assert pr["goal"] == "goal:g7.16.1.7.3.8"
    assert pr["entry"] == "prove_pane_rotations"
    assert pr["rotations"] == 3


def test_parent_stays_horizon_and_no_messaging_imports():
    parent = NODES / "g7.16.1.7.3.md"
    text = parent.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    assert "status: horizon" in fm
    assert "goal:g7.16.1.7.3.8" in fm  # seeded
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
