"""goal:g7.16.1.7.3.6 — spawn/attach lifecycle hooks call runner tick/consume (dry).

Falsifiers:
1. dry on_spawn registers pane + consume first_turn_docs → one tool_call_turn.
2. dry on_attach same pane_id survives + tick drains; different pane_id refuses.
3. pi session_start → spawn_or_attach; before_agent_start holds; tool_result idle+tick.
4. free_lane_probe pi/free + pi.toml; pi_adapter_probe REQUIRED-only (no OPTIONAL_PANE).
5. Negative: lifecycle + this test import neither adapters.magic_pane nor send transport;
   dry path never invokes live tmux.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import magic_pane_cutover as cut  # noqa: E402
import magic_pane_inject as inj  # noqa: E402
import magic_pane_lifecycle as life  # noqa: E402
import magic_pane_runner as run  # noqa: E402
import adapters  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_lifecycle.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _data():
    return cut.load_cutover(FIX)


def test_dry_on_spawn_registers_and_consumes_first_turn(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:spawn"
    out = life.on_spawn(
        root, post, pane_id="%42", body="DOCS:v1", routes=data, dry=True
    )
    assert out["action"] == "spawn"
    assert out["dry"] is True
    assert out["live_tmux"] is False
    assert out["pane"]["pane_id"] == "%42"
    assert out["pane"]["post_id"] == post
    assert len(out["turns"]) == 1
    turn = out["turns"][0]
    assert turn["inject_shape"] == "tool_call_turn"
    assert turn["kind_tag"] == "engine.first_turn_docs"
    assert turn["message"] == "DOCS:v1"
    assert turn["message_is"] == "tool_return"
    assert life.get_pane(root, post)["pane_id"] == "%42"
    # exactly-once
    assert run.tick(root, post, busy=False) == []


def test_dry_on_attach_pane_id_survives_and_tick_drains(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:attach"
    life.on_spawn(root, post, pane_id="@7", body="first", routes=data, dry=True)
    # enqueue while busy so attach tick has something to drain
    run.mark_busy(root, post)
    run.deliver(root, post, "memory_alarm", "ALARM", routes=data)
    assert run.tick(root, post) == []  # held
    # attach with SAME pane_id
    out = life.on_attach(root, post, pane_id="@7", routes=data, dry=True)
    assert out["action"] == "attach"
    assert out["pane"]["pane_id"] == "@7"
    assert out["pane"]["generation"] == 1  # bumped
    assert len(out["turns"]) == 1
    assert out["turns"][0]["message"] == "ALARM"
    assert out["turns"][0]["kind_tag"] == "engine.memory_alarm"
    # different pane_id refused (survival)
    with pytest.raises(life.MagicPaneLifecycleError, match="survival"):
        life.on_attach(root, post, pane_id="@99", routes=data, dry=True)
    # second spawn refused
    with pytest.raises(life.MagicPaneLifecycleError, match="already registered"):
        life.on_spawn(root, post, pane_id="@7", routes=data, dry=True)


def test_pi_events_route_to_lifecycle_hooks(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:pi"
    # session_start first → spawn
    s1 = life.handle_pi_event(
        root, post, "session_start", pane_id="%1", body="BOOT", routes=data, dry=True
    )
    assert s1["action"] == "spawn"
    assert s1["turns"][0]["message"] == "BOOT"
    # before_agent_start → busy
    run.deliver(root, post, "message_receipt", "DM1", routes=data)
    busy = life.handle_pi_event(root, post, "before_agent_start", routes=data, dry=True)
    assert busy["action"] == "mark_busy"
    assert busy["turns"] == []
    assert run.tick(root, post) == []
    # tool_result → idle + tick
    done = life.handle_pi_event(root, post, "tool_result", routes=data, dry=True)
    assert done["action"] == "mark_idle_and_tick"
    assert len(done["turns"]) == 1
    assert done["turns"][0]["kind_tag"] == "dm.message_receipt"
    # session_start again → attach (same pane)
    run.deliver(root, post, "rotation_prompt", "ROT", routes=data)
    run.mark_busy(root, post)
    a = life.handle_pi_event(
        root, post, "session_start", pane_id="%1", routes=data, dry=True
    )
    assert a["action"] == "attach"
    assert a["pane"]["pane_id"] == "%1"
    assert any(t["message"] == "ROT" for t in a["turns"])
    # mirror table intact
    for ev, cc in (
        ("session_start", "SessionStart"),
        ("before_agent_start", "UserPromptSubmit"),
        ("tool_result", "PostToolUse"),
    ):
        assert inj.CC_COMPAT_MIRROR[ev]["cc_hook"] == cc
        assert ev in life.PI_LIFECYCLE_MAP


def test_free_lane_and_pi_adapter_probe():
    spec = life.free_lane_probe()
    assert spec["harness"] == "pi"
    assert spec["row"] == "free"
    assert spec["harness_name"] == "pi:free"
    assert spec["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    pi_tomls = list(PI_TOML.parent.glob("pi*.toml"))
    assert pi_tomls == [PI_TOML]
    probe = life.pi_adapter_probe()
    assert probe["required_ok"] is True
    assert probe["pane_interface"] == []  # pi omits OPTIONAL_PANE (g7.32.3)
    assert probe["lifecycle_hooks"] == ["spawn", "attach"]
    # adapters.load still works
    pi = adapters.load("pi")
    assert adapters.pane_interface(pi) == ()


def test_live_tmux_refused_on_non_dry():
    with pytest.raises(life.MagicPaneLifecycleError, match="deferred"):
        life.register_pane(Path("/tmp"), "post:x", "%1", dry=False)


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
        assert "send" not in parts, (path.name, imported)
        # bare magic_pane = messaging leaf; magic_pane_* helpers + adapters package ok
        assert "magic_pane" not in parts, (path.name, imported)
        # must not import adapters.magic_pane messaging module by name
        assert "adapters.magic_pane" not in imported, (path.name, imported)
