"""goal:g7.16.1.7.3.2 — uniform tool-call inject (DM|engine) via ONE-pi free row.

Falsifiers:
1. Each v2 fixture row → envelope {channel, kind_tag, body}; body = sole tool-return.
2. harness_template.render(pi.toml) for free row emits provider/model/thinking;
   no second pi template / pi-free.toml.
3. Negative: this module + helper import neither the messaging adapter nor send transport.
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

import magic_pane_inject as inj  # noqa: E402
import harness_template  # noqa: E402
import adapters  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_inject.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"
CFG = ROOT / ".agi" / "config.json"


def _routes():
    return inj.load_event_routes(FIX)


def test_each_v2_row_builds_envelope_tool_return_is_body():
    data = _routes()
    for row in data["routes"]:
        kind = row["event_kind"]
        body = f"MSG:{kind}:hello"
        env = inj.build_envelope(kind, body, routes=data)
        assert env["channel"] in {"dm", "engine"}
        assert env["channel"] == row["channel"]
        assert env["kind_tag"] == row["kind_tag"]
        assert env["kind_tag"].startswith(env["channel"] + ".")
        assert env["body"] == body
        assert inj.tool_return_payload(env) == body
        assert env["tool_return"] == body
        assert env["target_route"] == "tool_call_turn"
        assert env["message_is"] == "tool_return"


def test_channel_exactly_dm_or_engine_kind_tag_shape():
    data = _routes()
    for row in data["routes"]:
        env = inj.build_envelope(row["event_kind"], "x", routes=data)
        assert env["channel"] in inj.CHANNELS
        assert env["kind_tag"] == f"{env['channel']}.{env['event_kind']}"


def test_refuses_unknown_kind():
    with pytest.raises(inj.MagicPaneInjectError, match="unknown event_kind"):
        inj.build_envelope("not_a_real_kind", "x", routes=_routes())


def test_free_lane_harness_template_render_emits_free_row_slots():
    """Falsifier 2: ONE pi.toml via harness_template; free row provider/model/thinking."""
    data = _routes()
    lane = inj.free_lane_spec(data)
    assert lane["harness"] == "pi"
    assert lane["row"] == "free"
    assert lane["template"].endswith("pi.toml")
    assert PI_TOML.is_file()
    tmpl_dir = PI_TOML.parent
    # ONE pi harness template only (pi.toml). pi-free is an alias/row, not a file.
    assert (tmpl_dir / "pi.toml").is_file()
    assert not (tmpl_dir / "pi-free.toml").exists()
    extras = [p.name for p in tmpl_dir.glob("pi-*.toml")]
    assert extras == [], f"second pi template present: {extras}"

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    harness = adapters.harness_block(cfg, lane["alias"])  # pi-free → free row
    assert harness.get("row") == "free"
    assert harness.get("zero_usd") is True
    provider = harness["provider"]
    thinking = harness["thinking"]
    model = harness["models"]["kid"]

    argv = harness_template.render(
        "pi",
        prompt="inject-probe",
        provider=provider,
        model=model,
        thinking=thinking,
        bin_path="pi",
    )
    assert "--provider" in argv
    assert provider in argv
    assert "--model" in argv
    assert model in argv
    assert "--thinking" in argv
    assert thinking in argv
    assert "inject-probe" in argv
    joined = " ".join(argv)
    assert "pi-free.toml" not in joined
    assert "harnesses/pi-free" not in joined


def test_cc_compat_probe_mirrors_cc_hooks_not_npm_cc_mirror():
    probe = inj.cc_compat_probe()
    mirror = probe["mirror"]
    assert set(mirror) >= {"session_start", "before_agent_start", "tool_result"}
    assert mirror["session_start"]["cc_hook"] == "SessionStart"
    assert mirror["before_agent_start"]["cc_hook"] == "UserPromptSubmit"
    assert mirror["tool_result"]["cc_hook"] == "PostToolUse"
    data = _routes()
    measured = set(data["parent_measured_legacy_routes"])
    named = {row["legacy_route"] for row in mirror.values()}
    assert "session_start_hook_paste" in named
    assert "user_prompt_submit_meter" in named
    assert "cc_send_message" in named
    assert measured
    note = probe["note"].lower()
    assert "cc-mirror" in note or "not npm" in note
    assert "extension" in note
    installed = probe["pi_events_in_types"]
    if any(installed.values()):
        for ev in ("session_start", "before_agent_start", "tool_result"):
            assert installed.get(ev) is True, installed


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


def test_helper_and_test_do_not_import_messaging_adapter_or_send():
    """Falsifier 3: no messaging-adapter / send-transport imports."""
    for path in (HELPER, THIS):
        imported = _imported_modules(path)
        parts: set[str] = set()
        for name in imported:
            parts.add(name)
            parts.add(name.split(".")[0])
            parts.update(name.split("."))
        assert "magic_pane" not in parts, (path.name, imported)
        assert "send" not in parts, (path.name, imported)
        assert "send_transport" not in parts, (path.name, imported)
