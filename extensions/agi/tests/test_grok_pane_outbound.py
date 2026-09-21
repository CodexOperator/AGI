"""Tests for a non-Claude harness pane's outbound: inbox write + wake nudge.

Falsifier 1 of goal:g7.31.4.1: from a grok-harness pane, one outbound
``send.py`` message must land in the recipient inbox **and** a wake-token
nudge must be typed into the recipient pane -- even when that pane's input
box does NOT carry the Claude ``\u276f`` glyph. The engine fix makes the box
glyph DATA on the recipient's own ``config:posts``/``config:seats`` row
(``prompt_marker``, string or list), never a harness-NAME branch: the
transport has zero ``grok`` in its code, so any harness pane works by
carrying its glyph.

Deliverable (2), the negative control, is the SHAPE-A safety kept intact:
a non-``\u276f`` box with NO ``prompt_marker`` cell is an unrecognized box
and is NEVER typed into (``"no rendered box"``), exactly as before.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


#: The grok pane's own box glyph, deliberately NOT U+276F and never a bare
#: ``>`` (``>`` collides with transcript blockquote lines and would defeat
#: SHAPE-A safety). U+258C LEFT HALF BLOCK.
GROK_MARKER = "\u258c"

SENDER = "grok-seat"
RECIPIENT = "grok-recipient"
WINDOW_ID = "@5"
TARGET = f"agi-rc:{WINDOW_ID}"
BODY = "hello from the grok pane\nsecond line"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project with a config.json so locations.resolve works."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / ".agi" / "sessions" / "inbox").mkdir(parents=True)
    return root


def _write_seats(project: Path, rows: list) -> None:
    """A seats node body the engine parser reads (same shape test_send.py
    fixtures use, re-stated here so this file imports no private helper)."""
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "type: config", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    (d / "seats.md").write_text("\n".join(lines) + "\n")


class _MarkerPane:
    """A ``tmux`` input box whose prompt glyph is the pane's OWN marker --
    the same shape test_send.py's ``_FixturePane`` models for Claude, with
    the glyph parameterised. ``capture()`` renders transcript, box, and
    separator so ``_input_region`` can find the box by the row's marker."""

    def __init__(self, marker: str, busy: bool = False):
        self.marker = marker
        self.busy = busy
        self.input = ""
        self.submitted: list = []

    def send_keys(self, argv: list) -> None:
        args = list(argv)
        literal = False
        if args and args[0] == "-l":
            literal = True
            args = args[1:]
        assert args[:1] == ["-t"], f"send-keys without -t: {argv}"
        keys = args[2:]
        if keys[:1] == ["-X"]:                     # a tmux subcommand, not text
            return
        if literal:
            self.input += "".join(keys)
            return
        for k in keys:
            if k == "Enter":
                self.submitted.append(self.input)
                self.input = ""
            else:
                self.input += k

    def capture(self) -> str:
        sep = "\u2500" * 24
        lines = ["previous transcript output", sep,
                 f"{self.marker} {self.input}", sep]
        if self.busy:
            lines.append("esc to interrupt")
        return "\n".join(lines) + "\n"


def _fake_tmux_pane(monkeypatch, window_names, pane, sleeps=None):
    """Fake every ``subprocess.run`` tmux call (never a real pane); records
    the calls so the send-keys SHAPE can be asserted."""
    calls = []
    recorded = [] if sleeps is None else sleeps

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(
                cmd, 0, stdout="\n".join(window_names), stderr="")
        if cmd[:2] == ["tmux", "capture-pane"]:
            return subprocess.CompletedProcess(
                cmd, 0, stdout=pane.capture(), stderr="")
        if cmd[:2] == ["tmux", "display-message"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="0", stderr="")
        if cmd[:2] == ["tmux", "send-keys"]:
            pane.send_keys(cmd[2:])
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: recorded.append(s))
    return calls


def _typed(calls):
    return [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]]


def _enters(calls):
    return [c for c in calls
            if c[:2] == ["tmux", "send-keys"] and c[-1] == "Enter"]


@pytest.fixture(autouse=True)
def _clean_identity(monkeypatch):
    """The sender identity is the one passed in, never an ambient harness
    export (the ordering AGI_AGENT_ID > AGI_SEAT > sender would otherwise
    decide the ``from:`` line from the test runner's own env)."""
    for key in ("AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"):
        monkeypatch.delenv(key, raising=False)


def test_grok_pane_send_lands_inbox_and_types_a_nudge(project: Path,
                                                     monkeypatch):
    """Falsifier 1: a grok sender, a non-``\u276f`` recipient box, and a
    ``prompt_marker`` cell on the recipient row -> the inbox gets the block
    AND the pane gets exactly one literal wake token plus a separate Enter.
    The token is NOT the body (the send.py nudge contract)."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [
        # the SENDER's own row names its harness -- data, not a branch: the
        # recipient's marker cell is what the transport reads.
        {"name": SENDER, "role": "director", "harness": "grok-bot"},
        {"name": RECIPIENT, "role": "director", "window": WINDOW_ID,
         "prompt_marker": GROK_MARKER},
    ])
    pane = _MarkerPane(GROK_MARKER)
    calls = _fake_tmux_pane(monkeypatch, [WINDOW_ID, RECIPIENT], pane, [])

    # failing-then-passing: the pre-fix (default-marker-only) engine reads
    # this box as NO box; the recipient row's own marker is what finds it.
    assert send_mod._input_region(pane.capture()) == ""
    assert send_mod._input_region(
        pane.capture(), send_mod._prompt_markers(project, RECIPIENT)) != ""

    send_mod.send(project, RECIPIENT, BODY, SENDER)

    # (a) exactly one inbox block, from the grok seat, body byte-exact.
    inbox = send_mod._inbox_path(project, RECIPIENT)
    recs = send_mod._read_conv(inbox)
    assert len(recs) == 1, recs
    assert recs[0]["from"] == SENDER, recs[0]
    assert recs[0]["to"] == RECIPIENT, recs[0]
    assert recs[0]["text"] == BODY, recs[0]["text"]

    # (b) exactly one `-l` typing and one separate Enter -- never
    # `text Enter` in one call.
    typed, enters = _typed(calls), _enters(calls)
    assert len(typed) == 1, calls
    assert len(enters) == 1, calls
    assert typed[0][:5] == ["tmux", "send-keys", "-l", "-t", TARGET], typed
    assert enters[0] == ["tmux", "send-keys", "-t", TARGET, "Enter"], enters
    assert calls.index(typed[0]) < calls.index(enters[0])

    # (c) the typed string is the wake token, and it does not carry the body.
    token = typed[0][5]
    assert token == send_mod._build_nudge_token(RECIPIENT), token
    assert BODY not in token
    assert pane.submitted == [token], (pane.submitted, pane.input)
    assert pane.input == ""


def test_no_prompt_marker_keeps_shape_a_safety(project: Path, monkeypatch):
    """NEGATIVE CONTROL: the SAME non-``\u276f`` box with NO ``prompt_marker``
    cell is an unrecognized box. The coalesce reason stays ``no rendered
    box`` and NOTHING is typed -- the SHAPE-A safety that a box the engine
    cannot recognise is never typed into is preserved."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [
        {"name": SENDER, "role": "director", "harness": "grok-bot"},
        {"name": RECIPIENT, "role": "director", "window": WINDOW_ID},
    ])
    pane = _MarkerPane(GROK_MARKER)
    calls = _fake_tmux_pane(monkeypatch, [WINDOW_ID, RECIPIENT], pane, [])

    # the unmarked row resolves to the Claude default, which this box lacks
    assert send_mod._prompt_markers(project, RECIPIENT) == \
        (send_mod.DEFAULT_PROMPT_MARKER,)
    reason = send_mod._nudge_coalesce_reason(
        pane.capture(), send_mod._build_nudge_token(RECIPIENT), None)
    assert reason == "no rendered box", reason

    send_mod.send(project, RECIPIENT, BODY, SENDER)

    assert _typed(calls) == [], "an unrecognized box must never be typed into"
    assert _enters(calls) == [], "not even a bare Enter"
    assert pane.submitted == []
    # the durable half still happened: the message is in the inbox.
    recs = send_mod._read_conv(send_mod._inbox_path(project, RECIPIENT))
    assert len(recs) == 1 and recs[0]["from"] == SENDER
    assert recs[0]["text"] == BODY