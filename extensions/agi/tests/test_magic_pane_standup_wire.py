"""goal:g7.16.1.7.3.7 — wire on_spawn/on_attach from stand-up/rotate paths (dry).

Falsifiers:
1. stand_up(mode=spawn) → from_stand_up → pane pin + engine.first_turn_docs turn.
2. stand_up(mode=rotate) after spawn → same pane_id survives; dry-run rotate wires too.
3. free_lane_probe pi/free + pi.toml; pi_adapter REQUIRED-only.
4. Negative: wire/tests import neither adapters.magic_pane nor send transport;
   from_stand_up(dry=False) refuses; parent g7.16.1.7.3 stays horizon.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
NODES = ROOT / ".agi" / "nodes" / "goal"
sys.path.insert(0, str(BIN))

import magic_pane_cutover as cut  # noqa: E402
import magic_pane_lifecycle as life  # noqa: E402
import rotate  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_lifecycle.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"
ROTATE_PY = BIN / "rotate.py"


def _data():
    return cut.load_cutover(FIX)


def test_stand_up_spawn_wires_on_spawn(tmp_path):
    root = tmp_path / "agi"
    root.mkdir()
    post = "seat-wire"
    seen: list = []

    def body():
        seen.append("launched")
        return "ok"

    held, out = rotate.stand_up(root, post, body, mode="spawn")
    assert (held, out) == (True, "ok") and seen == ["launched"]
    pin = life.get_pane(root, post)
    assert pin is not None
    assert pin["pane_id"] == life.dry_pane_id(post)
    assert pin["dry"] is True
    # consume already drained first_turn; tick empty
    import magic_pane_runner as run

    assert run.tick(root, post, busy=False) == []


def test_stand_up_rotate_survives_same_pane_id(tmp_path):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    post = "seat-rot"
    # spawn first
    held, _ = rotate.stand_up(root, post, lambda: 0, mode="spawn")
    assert held
    pin1 = life.get_pane(root, post)["pane_id"]
    # enqueue while busy so attach tick has work
    import magic_pane_runner as run

    run.mark_busy(root, post)
    run.deliver(root, post, "rotation_prompt", "ROTATE-ME", routes=data)
    assert run.tick(root, post) == []
    held, _ = rotate.stand_up(root, post, lambda: 0, mode="rotate")
    assert held
    pin2 = life.get_pane(root, post)
    assert pin2["pane_id"] == pin1
    assert pin2["generation"] == 1
    # drained
    assert run.tick(root, post, busy=False) == []


def test_from_stand_up_direct_and_dry_run_spawn_path(tmp_path, monkeypatch):
    data = _data()
    root = tmp_path / "agi"
    root.mkdir()
    post = "p-dry"
    out = life.from_stand_up(
        root, post, "spawn", body="BOOT", routes=data, dry=True
    )
    assert out["wired_from"] == "stand_up"
    assert out["stand_up_mode"] == "spawn"
    assert out["action"] == "spawn"
    assert out["turns"][0]["kind_tag"] == "engine.first_turn_docs"
    assert out["pane"]["pane_id"] == f"dry:{post}"
    # dry-run cmd_spawn wired path (no live tmux / no lock)
    monkeypatch.setattr(rotate, "_cmd_spawn", lambda args, r: 0)
    calls: list = []
    real = rotate._magic_pane_after_stand_up

    def spy(root, post, mode, *, pane_id=None, dry=True):
        calls.append((post, mode, dry))
        return real(root, post, mode, pane_id=pane_id, dry=dry)

    monkeypatch.setattr(rotate, "_magic_pane_after_stand_up", spy)
    # use a fresh post so spy sees the dry-run wire (spawn already pinned above)
    rc = rotate.cmd_spawn(NS(seat="p-dry2", dry_run=True), root)
    assert rc == 0
    assert calls == [("p-dry2", "spawn", True)]


def test_from_stand_up_refuses_non_dry_and_free_lane():
    with pytest.raises(life.MagicPaneLifecycleError, match="deferred"):
        life.from_stand_up(Path("/tmp"), "p", "spawn", dry=False)
    spec = life.free_lane_probe()
    assert spec["harness"] == "pi" and spec["row"] == "free"
    assert spec["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    assert list(PI_TOML.parent.glob("pi*.toml")) == [PI_TOML]
    probe = life.pi_adapter_probe()
    assert probe["required_ok"] is True
    assert probe["pane_interface"] == []
    # fixture notes standup_wire
    data = _data()
    sw = data["cutover"]["standup_wire"]
    assert sw["goal"] == "goal:g7.16.1.7.3.7"
    assert sw["entry"] == "from_stand_up"


def test_parent_stays_horizon_and_no_messaging_imports():
    parent = NODES / "g7.16.1.7.3.md"
    text = parent.read_text(encoding="utf-8")
    # frontmatter status
    fm = text.split("---", 2)[1]
    assert "status: horizon" in fm
    assert "goal:g7.16.1.7.3.7" in fm  # seeded
    for path in (HELPER, THIS, ROTATE_PY):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        # rotate imports many things; only forbid messaging adapter module name
        # and top-level `send` import from the lifecycle helper / this test.
        if path in (HELPER, THIS):
            parts: set[str] = set()
            for name in imported:
                parts.add(name)
                parts.add(name.split(".")[0])
                parts.update(name.split("."))
            assert "send" not in parts, (path.name, imported)
            assert "magic_pane" not in parts, (path.name, imported)
            assert "adapters.magic_pane" not in imported
        else:
            assert "adapters.magic_pane" not in imported
            # rotate may import send historically; standup wire must not ADD it
            # via the lifecycle helper path — checked via HELPER above.
