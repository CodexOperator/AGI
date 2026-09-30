"""goal:g7.16.1.7.3.5 — pane runner consumes cutover.deliver + live hook uninstall.

Falsifiers:
1. deliver → idle tick: one tool_call_turn per v2 kind; message=tool_return=body.
2. busy tick empty; after mark_idle, same envelopes once.
3. live_hook_uninstall removes legacy SessionStart/UserPromptSubmit; 2nd apply no-op; unrelated kept.
4. free_lane_probe still pi/free + pi.toml; no second pi template.
5. Negative: runner + this test import neither adapters.magic_pane nor send transport.
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
import magic_pane_runner as run  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_runner.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _data():
    return cut.load_cutover(FIX)


def test_deliver_then_idle_tick_renders_tool_call_turns(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:runner"
    for row in data["routes"]:
        kind = row["event_kind"]
        body = f"RUN:{kind}"
        path = run.deliver(root, post, kind, body, routes=data)
        assert path.is_file()
    turns = run.tick(root, post, busy=False)
    assert len(turns) == len(data["routes"])
    for turn, row in zip(turns, data["routes"]):
        assert turn["inject_shape"] == "tool_call_turn"
        assert turn["target_route"] == "tool_call_turn"
        assert turn["message_is"] == "tool_return"
        assert turn["channel"] == row["channel"]
        assert turn["kind_tag"] == row["kind_tag"]
        assert turn["message"] == f"RUN:{row['event_kind']}"
        assert turn["tool_return"] == turn["message"]
        assert turn["body"] == turn["message"]
        assert inj.tool_return_payload(turn) == turn["message"]
    # exactly-once
    assert run.tick(root, post, busy=False) == []


def test_busy_holds_until_idle_then_once(tmp_path):
    data = _data()
    root = tmp_path / "pane"
    post = "post:busy"
    assert run.consume(root, post, "memory_alarm", "ALARM", busy=True, routes=data) == []
    assert run.tick(root, post) == []  # still busy
    run.mark_idle(root, post)
    got = run.tick(root, post)
    assert len(got) == 1
    assert got[0]["message"] == "ALARM"
    assert got[0]["kind_tag"] == "engine.memory_alarm"
    assert run.tick(root, post, busy=False) == []


def test_live_hook_uninstall_surgical_and_idempotent(tmp_path):
    settings = {
        "theme": "dark",
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "bash /data/work/agi/extensions/agi/hooks/cc-session-start.sh",
                            "timeout": 30,
                        },
                        {
                            "type": "command",
                            "command": "echo keep-me-session",
                        },
                    ]
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3 /data/work/agi/extensions/agi/hooks/rotation_alert.py",
                            "timeout": 10,
                        },
                        {
                            "type": "command",
                            "command": "echo keep-me-prompt",
                        },
                    ]
                }
            ],
            "OtherEvent": [
                {"hooks": [{"type": "command", "command": "echo unrelated"}]}
            ],
        },
    }
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    plan = run.live_hook_uninstall(path, dry_run=True)
    assert plan["already_clean"] is False
    assert set(plan["legacy_found"]) == {
        "session_start_hook_paste",
        "user_prompt_submit_meter",
    }
    assert plan["written"] is False
    # file unchanged on dry-run
    assert json.loads(path.read_text())["hooks"]["SessionStart"]

    out = run.live_hook_uninstall(path, apply=True)
    assert out["written"] is True
    assert out["already_clean"] is False
    after = json.loads(path.read_text())
    # legacy gone
    ss_cmds = [
        h["command"]
        for m in after["hooks"]["SessionStart"]
        for h in m["hooks"]
    ]
    up_cmds = [
        h["command"]
        for m in after["hooks"]["UserPromptSubmit"]
        for h in m["hooks"]
    ]
    assert all("cc-session-start" not in c for c in ss_cmds)
    assert all("rotation_alert" not in c for c in up_cmds)
    assert "echo keep-me-session" in ss_cmds
    assert "echo keep-me-prompt" in up_cmds
    assert after["hooks"]["OtherEvent"][0]["hooks"][0]["command"] == "echo unrelated"
    assert after["theme"] == "dark"

    # idempotent
    again = run.live_hook_uninstall(path, apply=True)
    assert again["already_clean"] is True
    assert again["written"] is False
    assert again["removals"] == []

    # refuse non-hook legacy still
    for name in ("send_py_nudge", "cc_send_message"):
        with pytest.raises(cut.MagicPaneCutoverError):
            run.refuse_legacy(name)


def test_free_lane_probe_one_pi_free_no_second_template():
    spec = run.free_lane_probe()
    assert spec["harness"] == "pi"
    assert spec["row"] == "free"
    assert spec["harness_name"] == "pi:free"
    assert spec["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    # no second pi template beside the ONE
    harness_dir = PI_TOML.parent
    pi_tomls = list(harness_dir.glob("pi*.toml"))
    assert pi_tomls == [PI_TOML]


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
        # bare magic_pane = messaging leaf; magic_pane_* helpers ok
        assert "magic_pane" not in parts, (path.name, imported)
