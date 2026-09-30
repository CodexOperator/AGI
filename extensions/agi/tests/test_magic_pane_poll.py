"""goal:g7.16.1.7.3.3 — live pane delivery/poll of inject envelopes.

Falsifiers:
1. Each v2 kind enqueued → idle poll returns tool_call_turn with kind_tag + tool_return.
2. Busy holds; after mark_idle delivers once (no mid-turn / no double-deliver).
3. Two posts = isolated local queues; network-fetch spy stays at 0.
4. free_lane_spec still pi/free + pi.toml; no second pi template.
5. Negative: helper + this test import neither messaging adapter nor send transport.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import magic_pane_inject as inj  # noqa: E402
import magic_pane_poll as poll  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "magic_pane_event_routes.json"
HELPER = BIN / "magic_pane_poll.py"
THIS = Path(__file__).resolve()
PI_TOML = ROOT / "extensions" / "agi" / "templates" / "harness" / "pi.toml"


def _routes():
    return inj.load_event_routes(FIX)


def _env(kind: str, body: str | None = None):
    return inj.build_envelope(kind, body or f"MSG:{kind}", routes=_routes())


def test_idle_poll_delivers_each_v2_kind_as_tool_call_turn(tmp_path):
    root = tmp_path / "pane"
    data = _routes()
    post = "post:belam-test"
    expected = []
    for row in data["routes"]:
        kind = row["event_kind"]
        body = f"BODY:{kind}"
        env = inj.build_envelope(kind, body, routes=data)
        poll.enqueue(root, post, env)
        expected.append((row["kind_tag"], body, row["channel"]))

    got = poll.poll(root, post, busy=False)
    assert len(got) == len(expected)
    assert poll.pending_count(root, post) == 0
    for delivery, (kind_tag, body, channel) in zip(got, expected):
        assert delivery["target_route"] == "tool_call_turn"
        assert delivery["message_is"] == "tool_return"
        assert delivery["kind_tag"] == kind_tag
        assert delivery["channel"] == channel
        assert delivery["tool_return"] == body
        assert delivery["body"] == body
        assert inj.tool_return_payload(delivery) == body  # same contract


def test_busy_holds_until_turn_boundary_then_delivers_once(tmp_path):
    root = tmp_path / "pane"
    post = "post:busy"
    env = _env("memory_alarm", "ALARM")
    poll.enqueue(root, post, env)

    held = poll.poll(root, post, busy=True)
    assert held == []
    assert poll.is_busy(root, post) is True
    assert poll.pending_count(root, post) == 1

    # still busy (default state) — mid-turn must not leak
    assert poll.poll(root, post) == []
    assert poll.pending_count(root, post) == 1

    poll.mark_idle(root, post)
    got = poll.poll(root, post)
    assert len(got) == 1
    assert got[0]["tool_return"] == "ALARM"
    assert got[0]["kind_tag"] == "engine.memory_alarm"
    assert poll.pending_count(root, post) == 0

    # exactly-once: second idle poll is empty
    assert poll.poll(root, post, busy=False) == []


def test_posts_isolated_and_poll_never_network_fetches(tmp_path):
    root = tmp_path / "pane"
    calls = {"n": 0}

    def spy():
        calls["n"] += 1

    poll.set_network_fetch_hook(spy)
    try:
        poll.enqueue(root, "post:a", _env("message_receipt", "A"))
        poll.enqueue(root, "post:b", _env("rotation_prompt", "B"))

        a = poll.poll(root, "post:a", busy=False)
        b = poll.poll(root, "post:b", busy=False)
        assert [d["tool_return"] for d in a] == ["A"]
        assert [d["tool_return"] for d in b] == ["B"]
        # isolation: a's queue empty, b's empty, no cross-talk
        assert poll.pending_count(root, "post:a") == 0
        assert poll.pending_count(root, "post:b") == 0
        # pane owns no transport — spy never invoked
        assert calls["n"] == 0
    finally:
        poll.set_network_fetch_hook(None)


def test_free_lane_probe_one_pi_toml_no_second_template():
    lane = poll.free_lane_probe()
    assert lane["harness"] == "pi"
    assert lane["row"] == "free"
    assert lane["template"].endswith("pi.toml")
    assert lane["alias"] == "pi-free"
    assert PI_TOML.is_file()
    tmpl_dir = PI_TOML.parent
    assert (tmpl_dir / "pi.toml").is_file()
    assert not (tmpl_dir / "pi-free.toml").exists()
    extras = [p.name for p in tmpl_dir.glob("pi-*.toml")]
    assert extras == [], f"second pi template present: {extras}"


def test_refuses_bad_envelope_and_post_id(tmp_path):
    root = tmp_path / "pane"
    with pytest.raises(poll.MagicPanePollError, match="invalid post_id"):
        poll.enqueue(root, "../evil", _env("memory_alarm"))
    bad = dict(_env("memory_alarm"))
    bad["message_is"] = "chat_paste"
    with pytest.raises(poll.MagicPanePollError, match="tool_return"):
        poll.enqueue(root, "post:ok", bad)


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
    for path in (HELPER, THIS):
        imported = _imported_modules(path)
        parts: set[str] = set()
        for name in imported:
            parts.add(name)
            parts.add(name.split(".")[0])
            parts.update(name.split("."))
        # magic_pane_inject / magic_pane_poll are fine; adapters.magic_pane is not
        assert "adapters" not in parts, (path.name, imported)
        assert "send" not in parts, (path.name, imported)
        # bare "magic_pane" would be the messaging leaf module name
        assert "magic_pane" not in parts, (path.name, imported)
