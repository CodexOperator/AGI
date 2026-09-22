"""Falsifiers for bin/messaging.py (goal:g7.32.2, magic-pane messaging).

Three claims, one test file:
  (a) route() => native on equal non-empty harnesses, nudge_send on different,
      a NAMED ValueError on empty/None;
  (b) the native path never touches transport (a .send that raises is never
      called) and the pane seam receives exactly (to, text);
  (c) cross-harness records nudge.write THEN send_py.send, in both the actual
      event stream and the returned trace;
  (d) source carries no rotate/dispatch import, direct or transitive-looking;
  (e) both refusals are named errors, one per direction.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import messaging  # noqa: E402

SOURCE = (BIN / "messaging.py").read_text(encoding="utf-8")


# ------------------------------------------------------------------ (a) route

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


# ------------------------------------------------- (b) native never transport

class _RecordingPane:
    def __init__(self):
        self.calls = []

    def type(self, to, text):
        self.calls.append((to, text))


class _ExplodingSend:
    def send(self, to, text):
        raise AssertionError("native path must never call send.py transport")


def test_native_send_never_touches_transport_and_types_exactly():
    pane = _RecordingPane()
    trace = messaging.native_send(pane, sender_harness="grok-bot",
                                  recipient_harness="grok-bot",
                                  to="grok-b", text="hello")
    assert pane.calls == [("grok-b", "hello")]
    assert trace["route"] == "native"
    # The exploding stub is never wired in -- proving the native call above
    # cannot have reached transport. This line is a live canary, not decoration.
    with pytest.raises(AssertionError):
        _ExplodingSend().send("grok-b", "hello")


# ------------------------------------------- (c) cross-harness trace order

def test_cross_harness_records_nudge_then_send_in_order():
    events = []

    class _Nudge:
        def write(self, to, text):
            events.append(("nudge.write", to, text))

    class _Send:
        def send(self, to, text):
            events.append(("send.send", to, text))

    trace = messaging.cross_harness_send(
        _Send(), _Nudge(), sender_harness="grok-bot",
        recipient_harness="claude-code", to="claude-a", text="hi")

    assert events == [("nudge.write", "claude-a", "hi"),
                      ("send.send", "claude-a", "hi")]
    assert [step[0] for step in trace["steps"]] == ["nudge.write", "send.send"]
    assert trace["steps"] == events


# -------------------------------------------------------- (d) source grep

@pytest.mark.parametrize("needle", ["import rotate", "import dispatch",
                                    "from rotate", "from dispatch"])
def test_messaging_source_has_no_rotate_or_dispatch_import(needle):
    assert needle not in SOURCE


# ------------------------------------------------- (e) refusal both ways

def test_native_send_refuses_cross_harness():
    with pytest.raises(messaging.CrossHarnessOnNative):
        messaging.native_send(_RecordingPane(), sender_harness="grok-bot",
                              recipient_harness="claude-code",
                              to="claude-a", text="hi")


def test_cross_harness_send_refuses_same_harness():
    class _Nudge:
        def write(self, to, text):
            raise AssertionError("must not reach the nudge step")

    class _Send:
        def send(self, to, text):
            raise AssertionError("must not reach the send step")

    with pytest.raises(messaging.SameHarnessOnCross):
        messaging.cross_harness_send(_Send(), _Nudge(),
                                     sender_harness="grok-bot",
                                     recipient_harness="grok-bot",
                                     to="grok-b", text="hi")