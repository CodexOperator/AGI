"""Falsifier tests for goal:g7.32.2 — magic-pane messaging.

1. same-harness => NATIVE via the injected pane seam; send.py NEVER runs.
2. cross-harness => nudge artifact THEN send.py, in ONE measured trace.
3. messaging.py imports no rotate/dispatch internals; seams fail closed.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

_BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(_BIN))

import messaging  # noqa: E402


def test_same_harness_is_native_and_never_runs_send():
    calls = []

    def pane_send(recipient, body):
        calls.append(("pane", recipient, body))
        return "delivered-to-pane"

    def explode(nudge):  # if this runs, the native claim is false
        raise AssertionError("send_runner must NOT be called on the native path")

    out = messaging.deliver(
        "grok-a", "grok-b", "hello", sender_harness="grok-bot",
        recipient_harness="grok-bot", pane_send=pane_send, send_runner=explode)

    assert out.route == "native"
    assert out.steps == ["native"]
    assert calls == [("pane", "grok-b", "hello")]
    assert messaging.plan("a", "b", "grok-bot", "grok-bot") is messaging.Routing.NATIVE


def test_cross_harness_nudge_then_send_in_one_trace():
    sent = []

    def pane_forbidden(*a):
        raise AssertionError("pane_send must NOT be called cross-harness")

    out = messaging.deliver(
        "grok-a", "claude-b", "ping", sender_harness="grok-bot",
        recipient_harness="claude-code", pane_send=pane_forbidden,
        send_runner=sent.append)

    assert out.steps == ["nudge", "send"], out.steps
    assert out.route == "nudge"
    assert out.nudge["body"] == "ping"
    assert out.nudge["to"] == "claude-b"
    assert out.nudge["pane_intent"] is True
    assert sent and sent[0] is out.nudge
    assert messaging.plan("a", "b", "grok-bot", "claude-code") is messaging.Routing.NUDGE


def test_nudge_sink_sees_the_artifact():
    seen = []
    out = messaging.deliver(
        "grok-a", "pi-b", "hi", sender_harness="grok-bot",
        recipient_harness="pi", send_runner=lambda n: None,
        nudge_sink=seen.append)
    assert seen == [out.nudge]
    assert seen[0]["reason"] == ""


def test_default_send_runner_names_send_py_and_recipient(monkeypatch):
    argv_seen = {}

    class _Done:
        returncode = 0

    def fake_run(argv, **kw):
        argv_seen["argv"] = argv
        return _Done()

    monkeypatch.setattr(messaging.subprocess, "run", fake_run)
    nudge = messaging.build_nudge("grok-a", "claude-b", "payload")
    messaging.default_send_runner(nudge)

    argv = argv_seen["argv"]
    assert argv[0] == sys.executable
    assert argv[1].endswith("send.py")
    assert argv[2] == "send"
    assert "claude-b" in argv and "payload" in argv


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(sender_harness="grok-bot", recipient_harness="grok-bot"),
        dict(sender_harness="grok-bot", recipient_harness="claude-code"),
    ],
)
def test_missing_seam_fails_closed_by_name(kwargs):
    with pytest.raises(messaging.MessagingError):
        messaging.deliver("a", "b", "x", **kwargs)


def test_no_rotate_or_dispatch_imports():
    src = (_BIN / "messaging.py").read_text()
    tree = ast.parse(src)
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names.append(node.module or "")
    bad = [n for n in names if n.split(".")[0] in {"rotate", "dispatch"}]
    assert bad == [], bad
