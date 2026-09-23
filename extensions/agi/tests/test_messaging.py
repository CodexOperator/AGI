"""Tests for bin/messaging.py — the magic-pane messaging seam (goal:g7.32.2).

Falsifiers under test:
  1. same-harness grok<->grok is native, never touches send.py transport;
  2. cross-harness is nudge (intent) then real send.py, in that order, one
     measured trace;
  3. the messaging module imports no rotate/dispatch internals.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import messaging  # noqa: E402


def _load_send():
    spec = importlib.util.spec_from_file_location("send_real", BIN / "send.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class RecordingPane:
    """Records exactly what the native path typed; nothing else."""

    def __init__(self):
        self.typed = []

    def type(self, to, text):
        self.typed.append((to, text))


class RecordingNudge:
    """Writes one intent artifact per call and records the event."""

    def __init__(self, events):
        self.events = events
        self.artifact = None

    def write(self, to, text):
        self.events.append(("nudge.write", to, text))
        self.artifact = f"{to}:{text}"


class RecordingSend:
    def __init__(self, events, sink=None):
        self.events = events
        self.sink = sink

    def send(self, to, text):
        self.events.append(("send.send", to, text))
        if self.sink is not None:
            self.sink(to, text)


# ---- falsifier 3: no rotate / dispatch internals -------------------------

@pytest.mark.parametrize("needle", ["import rotate", "import dispatch",
                                    "from rotate", "from dispatch"])
def test_messaging_source_has_no_rotate_or_dispatch_import(needle):
    src = (BIN / "messaging.py").read_text()
    assert needle not in src


# ---- falsifier 1: same-harness is native ---------------------------------

def test_route_same_harness_is_native():
    assert messaging.route("grok-bot", "grok-bot") == "native"


def test_route_different_harness_is_nudge_send():
    assert messaging.route("grok-bot", "claude-code") == "nudge_send"
    assert messaging.route("claude-code", "grok-bot") == "nudge_send"


@pytest.mark.parametrize("sender,recipient", [("", "grok-bot"),
                                              ("grok-bot", ""),
                                              (None, "grok-bot"),
                                              ("grok-bot", None),
                                              (None, None)])
def test_route_unknown_harness_raises_named_error(sender, recipient):
    with pytest.raises(messaging.UnknownHarness):
        messaging.route(sender, recipient)


@pytest.mark.parametrize("sender,recipient", [("  ", "  "),
                                              ("  ", "grok-bot"),
                                              ("grok-bot", "\t")])
def test_whitespace_only_harness_is_unknown(sender, recipient):
    with pytest.raises(messaging.UnknownHarness):
        messaging.route(sender, recipient)


def test_padded_harness_routes_by_stripped_identity():
    assert messaging.route("  grok-bot  ", "grok-bot") == "native"


def test_native_send_never_touches_transport_and_types_exactly():
    pane = RecordingPane()
    out = messaging.native_send(pane, sender_harness="grok-bot",
                                recipient_harness="grok-bot",
                                to="B", text="hello")
    assert pane.typed == [("B", "hello")]
    assert out["route"] == "native"
    assert out["steps"] == [("pane.type", "B", "hello")]


def test_native_send_refuses_cross_harness():
    pane = RecordingPane()
    with pytest.raises(messaging.CrossHarnessOnNative):
        messaging.native_send(pane, sender_harness="grok-bot",
                              recipient_harness="claude-code",
                              to="B", text="hello")
    assert pane.typed == []


# ---- falsifier 2: cross-harness is nudge then send, in order -------------

def test_cross_harness_records_nudge_then_send_in_order():
    events = []
    nudge = RecordingNudge(events)
    send_py = RecordingSend(events)
    out = messaging.cross_harness_send(
        send_py, nudge, sender_harness="grok-bot",
        recipient_harness="claude-code", to="claude", text="hi")
    assert out["route"] == "nudge_send"
    assert out["steps"] == [("nudge.write", "claude", "hi"),
                            ("send.send", "claude", "hi")]
    assert events == out["steps"]


def test_cross_harness_send_refuses_same_harness():
    events = []
    nudge = RecordingNudge(events)
    send_py = RecordingSend(events)
    with pytest.raises(messaging.SameHarnessOnCross):
        messaging.cross_harness_send(send_py, nudge, sender_harness="grok-bot",
                                     recipient_harness="grok-bot",
                                     to="B", text="hi")
    assert events == []
    assert nudge.artifact is None


def test_cross_harness_trace_invokes_real_send_py(tmp_path):
    """Bind transport to the REAL send.send into a temp root; one trace."""
    send_real = _load_send()
    events = []
    nudge = RecordingNudge(events)
    send_py = RecordingSend(
        events,
        sink=lambda to, text: send_real.send(
            tmp_path, to, text, sender=None, nudge=False))
    out = messaging.cross_harness_send(
        send_py, nudge, sender_harness="grok-bot",
        recipient_harness="claude-code", to="claude", text="ping")
    # nudge artifact exists...
    assert nudge.artifact == "claude:ping"
    # ...THEN the real send.py wrote the inbox block.
    inbox = tmp_path / "sessions" / "inbox" / "claude.md"
    assert inbox.is_file()
    assert "ping" in inbox.read_text()
    assert out["steps"] == events == [("nudge.write", "claude", "ping"),
                                      ("send.send", "claude", "ping")]


def test_native_path_never_reaches_real_send_py(monkeypatch, tmp_path):
    send_real = _load_send()

    def _boom(*a, **k):
        raise AssertionError("native path reached send.py transport")

    monkeypatch.setattr(send_real, "send", _boom)
    # the binding is exercised once and must raise -- proving the hook is live
    with pytest.raises(AssertionError):
        send_real.send(tmp_path, "claude", "ping", sender=None, nudge=False)
    # ...and the native path never calls it.
    pane = RecordingPane()
    messaging.native_send(pane, sender_harness="grok-bot",
                          recipient_harness="grok-bot", to="B", text="hi")
    assert pane.typed == [("B", "hi")]
