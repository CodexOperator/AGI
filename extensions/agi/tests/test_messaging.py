"""Messaging router tests — the scripted evidence for goal:g7.32.2.

Each test maps to one falsifier clause:

1. same-harness grok<->grok never invokes send.py (native path).
2. cross-harness grok -> claude/pi shows `nudge_artifact` THEN `send_py`
   in one ordered trace, with the send.py invocation visible.
3. `messaging.py` imports no `rotate`/`dispatch` symbols (AST guard, the
   same check the falsifier grep runs).
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import messaging  # noqa: E402


class FakePane:
    """Records the native channel call; the only native surface used."""

    def __init__(self):
        self.calls = []

    def pane_send(self, text):
        self.calls.append(text)


class NoSendPane:
    """A pane whose optional method is absent (g7.32.3 absence case)."""


class SpyRunner:
    """Stands in for subprocess.run so no live send.py is ever spawned."""

    def __init__(self):
        self.argv = []

    def __call__(self, argv, **kwargs):
        self.argv.append(list(argv))


def test_route_native_iff_same_harness():
    assert messaging.route("grok-bot", "grok-bot") == "native"
    assert messaging.route("grok-bot", "pi") == "cross"
    assert messaging.route("grok-bot", "claude-code") == "cross"


def test_native_uses_pane_and_never_send_py():
    pane, runner = FakePane(), SpyRunner()
    trace = messaging.send(sender_harness="grok-bot", target_harness="grok-bot",
                           sender="grok-a", text="hi", pane=pane, runner=runner)
    assert pane.calls == ["hi"]
    assert trace[0][0] == "pane_send"
    assert runner.argv == [], "native path must not touch send.py"


def test_native_missing_pane_method_fails_closed_named():
    for pane in (None, NoSendPane()):
        try:
            messaging.send_native(pane=pane, sender="grok-a", text="hi")
        except messaging.PaneMethodMissing as exc:
            assert "pane_send" in str(exc)
        else:  # pragma: no cover
            raise AssertionError(f"{pane!r} did not fail closed")


def test_cross_is_nudge_then_send_py_and_never_native():
    pane, runner = FakePane(), SpyRunner()
    trace = messaging.send(sender_harness="grok-bot", target_harness="claude-code",
                           sender="grok-a", text="hello", pane=pane,
                           seat="claude-1", runner=runner)
    assert [ev[0] for ev in trace] == ["nudge_artifact", "send_py"]
    art = trace[0][1]
    assert (art.seat, art.sender, art.body) == ("claude-1", "grok-a", "hello")
    assert "[agi-nudge]" in art.wake_intent
    argv = trace[1][1]
    assert runner.argv == [argv]
    assert "send" in argv and "claude-1" in argv and "hello" in argv
    assert pane.calls == [], "cross-harness must never claim native"


def test_no_rotate_or_dispatch_import():
    src = (BIN / "messaging.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    assert not any(n == "rotate" or n.startswith("rotate.")
                   or n == "dispatch" or n.startswith("dispatch.")
                   for n in imported), imported
