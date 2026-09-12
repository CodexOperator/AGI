"""Tests for bin/send.py — one-verb agent comms.

Design source: .agi/context/season-ladder-and-morals-brief.md §2 (Comms).
The testable claim: a send then read returns the block once and peek still
shows it; two senders interleave without loss.
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

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _fixture_text(name: str) -> str:
    """A real-pane capture pasted as a test fixture. See the fixture files:
    claude_pane_busy.txt / claude_pane_idle.txt carry `tmux capture-pane -p`
    output of live Claude Code panes (the burn-in is in the file header)."""
    return (FIXTURES / name).read_text()

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project with a config.json so locations.resolve works."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


# ── red-first: send one message, read returns it once, peek still shows it ──


def test_send_creates_inbox_file(project: Path):
    """First message to a recipient creates the inbox file."""
    send_mod.send(project, "director", "hello world", "a00-xxxx")
    # The inbox is the SHARED room under the graph root: `project` is a G11
    # project (its markers live at `.agi/`), so sessions live at `.agi/sessions`.
    inbox = project / ".agi" / "sessions" / "inbox" / "director.md"
    assert inbox.is_file()
    content = inbox.read_text()
    assert "hello world" in content
    assert "from: a00-xxxx" in content
    assert "to: director" in content


def test_send_prints_inbox_path(project: Path, capsys):
    send_mod.send(project, "test-agent", "message one", "parent")
    captured = capsys.readouterr()
    expected = str((project / ".agi" / "sessions" / "inbox" / "test-agent.md").resolve())
    assert captured.out.strip() == expected


# ── hypothesis:l3w4-seat-transport: best-effort tmux nudge ───────────────


def _fake_tmux(monkeypatch, window_names, capture_text="", sleeps=None):
    """Fake subprocess.run so send can nudge without a live tmux; records
    every tmux invocation. `window_names` are returned by list-windows (a
    NAME fallback must see the recipient listed); `capture_text` is what
    capture-pane returns (empty = idle pane). A fixture pane only, never a
    live session (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message, 5).
    `sleeps`, when given, receives every `time.sleep` send.py asks for;
    whether given or not, sleep is monkeypatched to RECORD and never wait --
    residue 3: the plain `_fake_tmux` tests must not pay a real 0.3 s each."""
    calls = []
    recorded = [] if sleeps is None else sleeps

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="\n".join(window_names),
                                               stderr="")
        if cmd[:2] == ["tmux", "capture-pane"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout=capture_text,
                                               stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: recorded.append(s))
    return calls


def _typed(calls):
    """The send-keys calls that TYPE the token (`-l`), one per delivered
    token; the separate Enter calls are counted by `_enters`."""
    return [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]]


def _enters(calls):
    return [c for c in calls
            if c[:2] == ["tmux", "send-keys"] and c[-1] == "Enter"]


def _typed_text(calls):
    """The `-l` payloads send.py types across all its send-keys calls. A
    stranded resubmit types EXACTLY one printable space -- never a bare
    Enter-only retry and never a second nudge line (hypothesis:l4-a-stranded-
    nudge-is-resubmitted-by-typing-not-enter); an ordinary delivery types the
    full line/token."""
    return [c[5] for c in _typed(calls)]


class _FixturePane:
    """A model of a Claude Code input box driven by `tmux send-keys`, pinned
    by the prime on a REAL pane (nudge node 83fe8049c, 2026-09-11) as four
    probes:
      (A) short text + Enter in ONE send-keys call  -> delivered;
      (B) a long chunk + Enter in ONE call          -> STRANDED: the Enter
          becomes a newline (the paste heuristic), nothing submitted;
      (C) a later bare `send-keys Enter`            -> submits the stranded
          text;
      (D) `send-keys -l <text>`, a pause, then `send-keys Enter` as a
          SEPARATE call                             -> delivered.
    The paste threshold is a MODEL (the prime measured a 200-char chunk
    stranded and short text delivered; the 101-char token of the one-call
    shape sat stranded on the live sanctuary-director pane at 02:38Z); the
    SHAPE is the fact under test. `capture()` wraps the input at `width`
    columns the way the box does, so a wide token shows on two lines.
    `busy=True` renders the mid-turn spinner line."""

    PASTE_CHARS = 100

    def __init__(self, width: int = 80, busy: bool = False,
                 cell: bool = False):
        self.input = ""
        self.submitted: list = []
        self.width = width
        self.busy = busy
        self.cell = cell

    def send_keys(self, argv: list) -> None:
        """`argv` = everything after `tmux send-keys`."""
        args = list(argv)
        literal = False
        if args and args[0] == "-l":
            literal = True
            args = args[1:]
        assert args[:1] == ["-t"], f"send-keys without -t: {argv}"
        keys = args[2:]
        if literal:                       # -l: text only, no key parsing
            self.input += "".join(keys)
            return
        paste = False
        for k in keys:
            if k == "Enter":
                if paste:                 # (B) the Enter is a newline
                    self.input += "\n"
                else:                     # (A) / (C) submit
                    self.submitted.append(self.input)
                    self.input = ""
            else:
                self.input += k
                paste = len(k) >= self.PASTE_CHARS

    def capture(self) -> str:
        import textwrap
        if self.busy:
            # A BUSY Claude Code pane KEEPS its `\u276f` input box (the box
            # stays rendered through the turn); `esc to interrupt` sits in the
            # FOOTER immediately BELOW the box's `\u2500\u2500\u2500\u2500`
            # separator, still INSIDE the input region (which starts at that
            # `\u276f`). This is a REAL capture (`tmux capture-pane -p`) pasted
            # as fixtures/claude_pane_busy.txt -- not the box-less spinner line
            # the old fixture invented. Because the signal lives in the footer
            # under the box, a region narrowed to drop the box also drops it:
            # the busy test is only honest against this real shape.
            busy = _fixture_text("claude_pane_busy.txt")
            if not self.input:
                # empty-typed busy pane: byte-for-byte the committed fixture.
                return busy
            # A line stranded in a busy pane is a REAL part of the capture: it
            # sits in the box body. Rebuild box + separator + footer from the
            # fixture's constant parts and put the wrapped input in the box
            # line, the same way the idle path renders it.
            prefix, box_and_rest = busy.split("\u276f", 1)
            footer_and_blanks = box_and_rest[box_and_rest.index("\n"):]
            box = []
            if self.cell:
                for raw in self.input.split("\n"):
                    chunked = [raw[i:i + self.width]
                               for i in range(0, len(raw), self.width)] or [""]
                    box.append("\u276f " + chunked[0])
                    box.extend("  " + c for c in chunked[1:])
            else:
                wrapped = textwrap.wrap(self.input, self.width) or [""]
                box.append("\u276f " + wrapped[0])
                box.extend("  " + w for w in wrapped[1:])
            return prefix + "\n".join(box) + footer_and_blanks
        lines = []
        body = []
        if self.cell:
            # CELL wrap (real tmux): the box splits at the pane width even in
            # the MIDDLE of a word -- no whitespace at the boundary, unlike the
            # word-boundary `textwrap` below. Chunk at `width` chars so the
            # split is mid-word for a line longer than the width.
            for raw in self.input.split("\n"):
                chunked = [raw[i:i + self.width]
                           for i in range(0, len(raw), self.width)] or [""]
                body.extend(chunked)
        else:
            for raw in self.input.split("\n"):
                body.extend(textwrap.wrap(raw, self.width) or [""])
        lines.append("\u276f " + (body[0] if body else ""))
        lines.extend("  " + b for b in body[1:])
        return "\n".join(lines) + "\n"


def _fake_tmux_pane(monkeypatch, window_names, pane: _FixturePane,
                    sleeps: list | None = None):
    """Like `_fake_tmux`, but send-keys and capture-pane go through a
    `_FixturePane`, so the SHAPE of the typing decides delivery. `sleeps`
    records every `time.sleep` send.py asks for (never actually sleeps)."""
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="\n".join(window_names),
                                               stderr="")
        if cmd[:2] == ["tmux", "capture-pane"]:
            return subprocess.CompletedProcess(cmd, 0, stdout=pane.capture(),
                                               stderr="")
        if cmd[:2] == ["tmux", "send-keys"]:
            pane.send_keys(cmd[2:])
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    if sleeps is not None:
        monkeypatch.setattr(send_mod.time, "sleep", lambda s: sleeps.append(s))
    return calls


#: the one-call token shape as it was before the fix (101 chars for
#: sanctuary-director) -- the negative control's payload
_OLD_TOKEN = ("[agi-nudge] unread for sanctuary-director:"
              " python3 extensions/agi/bin/send.py read sanctuary-director")


def test_fixture_pane_reproduces_the_four_probes():
    """The prime's four probes, on the fixture pane (nudge node 83fe8049c):
    A delivered, B stranded, C submits the stranded text, D delivered."""
    long = "x" * 200
    pane = _FixturePane()
    pane.send_keys(["-t", "w", "hi", "Enter"])                    # (A)
    assert pane.submitted == ["hi"] and pane.input == ""
    pane.send_keys(["-t", "w", long, "Enter"])                    # (B)
    assert pane.submitted == ["hi"], "a long one-call chunk must strand"
    assert pane.input == long + "\n", "the Enter became a newline"
    pane.send_keys(["-t", "w", "Enter"])                          # (C)
    assert pane.submitted[-1] == long + "\n" and pane.input == ""
    pane.send_keys(["-l", "-t", "w", long])                       # (D)
    assert pane.submitted[-1] != long, "-l alone submits nothing"
    pane.send_keys(["-t", "w", "Enter"])
    assert pane.submitted[-1] == long and pane.input == ""
    assert len(_OLD_TOKEN) == 101


def test_nudge_types_literal_token_then_separate_enter(project: Path,
                                                       monkeypatch):
    """THE FIX (prime, verbatim): `-l` token, then Enter in a SECOND call
    after >= 0.3 s; token short (< 100 chars); never `text Enter` in one
    call. Measured on the fixture pane: the token is SUBMITTED."""
    pane = _FixturePane()
    sleeps: list = []
    calls = _fake_tmux_pane(monkeypatch, ["director"], pane, sleeps)
    send_mod.send(project, "director", "a body of some length " * 8, "kid")
    typed, enters = _typed(calls), _enters(calls)
    assert len(typed) == 1 and len(enters) == 1, calls
    assert typed[0][:5] == ["tmux", "send-keys", "-l", "-t", "agi-rc:director"]
    token = typed[0][5]
    assert token == send_mod._build_nudge_token("director")
    assert len(token) < 100
    assert "Enter" not in typed[0], "never `text Enter` in one call"
    assert enters[0] == ["tmux", "send-keys", "-t", "agi-rc:director", "Enter"]
    assert calls.index(typed[0]) < calls.index(enters[0])
    assert sleeps and sleeps[0] >= 0.3, sleeps
    assert pane.submitted == [token], (pane.submitted, pane.input)
    assert pane.input == ""
    assert send_mod._last_nudge_age(project, "director") is not None


def test_one_call_token_enter_strands_on_the_fixture():
    """NEGATIVE CONTROL: the shape the round shipped (`send-keys -t T token
    Enter`, one call, 101-char token) strands on the fixture pane exactly as
    it did on the live pane -- the fixture would have caught it."""
    pane = _FixturePane()
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])
    assert pane.submitted == []
    assert pane.input == _OLD_TOKEN + "\n"
    # and the wrapped capture no longer contains the whole token ...
    cap = pane.capture()
    assert _OLD_TOKEN not in cap
    # ... but its HEAD is what send.py's unsubmitted check looks for
    assert send_mod._nudge_token_head(_OLD_TOKEN) in cap


def test_wrapped_stranded_token_is_detected_as_unsubmitted():
    """The unsubmitted check matches the token HEAD (`[agi-nudge] unread
    for <seat>:`), so a token the input box wrapped across two lines is
    still seen; a pane holding unrelated text is not."""
    token = send_mod._build_nudge_token("sanctuary-director")
    wrapped = ("\u276f [agi-nudge] unread for sanctuary-director: python3"
               " extensions/agi/bin/send.py read\n  sanctuary-director\n")
    assert send_mod._nudge_coalesce_reason(wrapped, token, None) \
        == "token already unsubmitted"
    assert send_mod._nudge_coalesce_reason("\u276f hello\n", token, None) is None
    assert send_mod._nudge_token_head(token) == \
        "[agi-nudge] unread for sanctuary-director:"


def test_stranded_token_is_resubmitted_by_typing_not_enter(
        project: Path, monkeypatch, capsys):
    """The stranded-wake retry resubmits by TYPING a printable space (its
    own `-l` call) then a SEPARATE Enter -- never Enter-only
    (hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter). A
    bare Enter NEVER submits the stranded line on the master-sensei pane the
    target measured (three failed attempts 13:59Z/14:00Z/14:04Z); typing +
    Enter does. The fixture models exactly that pane: the `-l` space appears
    in the argv BEFORE the Enter call."""
    pane = _FixturePane(width=60)
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])      # stranded, wrapped
    assert pane.submitted == []
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    send_mod.send(project, "sanctuary-director", "the body", "kid")
    # the retry is a TYPED space in its own -l call BEFORE a separate Enter
    # -- a bare Enter-with-nothing is never the whole retry.
    typed = _typed(calls)
    assert len(typed) == 1, calls
    assert typed[0][:5] == ["tmux", "send-keys", "-l", "-t",
                            "agi-rc:sanctuary-director"], typed
    assert typed[0][5] == " ", "the only typed retry key is a single space"
    enters = _enters(calls)
    assert enters == [["tmux", "send-keys", "-t",
                       "agi-rc:sanctuary-director", "Enter"]], calls
    assert calls.index(typed[0]) < calls.index(enters[0]), \
        "the typed space must come BEFORE the Enter call"
    # the single stranded line (with the appended space) was submitted.
    assert pane.submitted and pane.input == ""
    assert "submitted a stranded token" in capsys.readouterr().err
    assert send_mod._last_nudge_age(project, "sanctuary-director") is not None


def test_send_wake_verb_submits_a_stranded_line(project: Path, monkeypatch,
                                                capsys):
    """`send.py wake <seat>` on a fixture pane holding a stranded nudge line
    resubmits it by TYPING (space + Enter) and delivers it -- the XIV->XV
    rotation-alert that stranded reaches the now-idle Sensei."""
    pane = _FixturePane(width=60)
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])      # stranded, wrapped
    assert pane.submitted == []
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    send_mod.wake(project, "sanctuary-director")
    typed = _typed(calls)
    assert len(typed) == 1, calls
    assert typed[0][5] == " "
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               "agi-rc:sanctuary-director", "Enter"]], calls
    assert pane.submitted and pane.input == ""
    assert "submitted a stranded token" in capsys.readouterr().err


def test_send_wake_verb_busy_pane_coalesces(project: Path, monkeypatch,
                                            capsys):
    """`send.py wake <seat>` on a BUSY fixture pane with something pending
    coalesces to ONE stderr line and types nothing (the deferred record is
    already written)."""
    # seed an unread inbox block so wake has something to announce
    inbox = send_mod._inbox_path(project, "sanctuary-director")
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    pane = _FixturePane(busy=True)
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    send_mod.wake(project, "sanctuary-director")
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    assert "nudge: coalesced (pane busy" in capsys.readouterr().err


def test_send_wake_verb_idle_nothing_is_a_silent_noop(project: Path,
                                                      monkeypatch, capsys,
                                                      tmp_path):
    """No stranded line and nothing pending -> `wake` types nothing and
    prints the ONE `nothing-pending` outcome (exit 1); an ungated bare token
    would retype once the coalesce window lapses (the heal polls every seat).
    The outcome also writes its ONE reaper log line (clause (3))."""
    logf = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logf))
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    assert send_mod.wake(project, "sanctuary-director") is False
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    cap = capsys.readouterr()
    assert cap.out.strip() == "nothing-pending"
    assert cap.err == ""
    lines = logf.read_text().splitlines()
    assert len(lines) == 1 and "nothing-pending" in lines[0], lines


# hypoth:l4-wake-repair-is-quiet-honest-and-readable -- clauses (1)-(3) ─────


def test_wake_unchanged_inbox_types_once_even_after_window(project: Path,
                                                          monkeypatch,
                                                          capsys):
    """Clause (1) falsifier: TWO consecutive `wake` passes over ONE unchanged
    unread inbox -> exactly ONE typed token. Age the 30s coalesce window
    between the passes so the guarantee is the DIGEST gate, not the window.
    Assert the argv sequence (_send_keys calls), not the return value (a
    return-value assertion passes on an implementation that types and then
    reports nothing happened)."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])

    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 1, calls
    assert capsys.readouterr().out.strip() == "typed-token"

    # age the coalesce window: only the digest gate keeps the SAME state
    # quiet once the window no longer would.
    send_mod._nudge_marker_path(project, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")
    assert send_mod.wake(project, seat) is False
    assert len(_typed(calls)) == 1, \
        "an unchanged unread inbox must not retype the token"
    assert capsys.readouterr().out.strip() == "nothing-pending"


def test_wake_changed_inbox_types_again(project: Path, monkeypatch, capsys):
    """Clause (1): a NEW unread block CHANGES the inbox state, so a later
    wake types again (a second token) once the coalesce window has lapsed."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])

    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 1
    capsys.readouterr()                       # clear the first outcome line
    # the inbox CHANGES: a second unread block arrives
    inbox.write_text(inbox.read_text() + "---\n hi2\n")
    send_mod._nudge_marker_path(project, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")
    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 2, calls
    assert capsys.readouterr().out.strip() == "typed-token"


def test_read_clears_announced_so_new_state_types(project: Path, monkeypatch,
                                                  capsys):
    """Clause (1): the seat's own read clears the announced sidecar, so a
    new unread state after a read is never mistaken for already-announced."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])

    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 1
    send_mod.read(project, seat, "prime")     # the seat consumes its unread
    assert send_mod._announced_digest(project, seat) is None, \
        "a read must clear the announced-state sidecar"
    # a fresh message now looks not-yet-announced -> a second token types
    inbox.write_text(inbox.read_text() + "---\n hi2\n")
    send_mod._nudge_marker_path(project, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")
    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 2, calls


def test_two_inbox_alerts_ten_seconds_apart_produce_two_wakes(
        project: Path, monkeypatch, capsys):
    """Clause (2) falsifier (hypothesis:l4-a-rotation-alert-lands-in-the-
    inbox-...): two rotation alerts 10 s apart -> TWO inbox blocks AND TWO
    wakes. The SECOND `send` lands inside the 30 s coalesce window, so its
    bare nudge coalesces (nothing typed) -- the coalesced alert's OWN wake
    is owed AFTER the window closes. `heal._repair_stranded_wakes` polls
    every seat each pass via `send.wake`, and `wake` gates on the unread
    digest, so a heal-style wake once the window lapses MUST type the second
    token. Assert the typed `-l` calls, not a return value."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])

    # ALERT 1: writes block 1 AND types the first wake token
    send_mod.send(project, seat, "ALERT rotation a", sender="master")
    assert len(_typed(calls)) == 1, calls
    capsys.readouterr()                        # clear the coalesce stderr

    # ALERT 2 ten seconds later: inside the window -> coalesced, NOT typed
    send_mod.send(project, seat, "ALERT rotation b", sender="master")
    assert len(_typed(calls)) == 1, \
        "the second alert's nudge coalesces inside the 30s window"
    assert "nudge: coalesced" in capsys.readouterr().err
    # the inbox now carries TWO blocks (the alert is in the INBOX, clause 1)
    assert len(send_mod._scan_messages(inbox)[0]) == 2

    # heal polls after the window lapses: the coalesced alert's wake appears
    send_mod._nudge_marker_path(project, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")
    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 2, calls
    assert capsys.readouterr().out.strip() == "typed-token"


def test_two_dms_ten_seconds_apart_still_wake_twice(project: Path,
                                                    monkeypatch, capsys):
    """Clause (2) for the DM path: two dms 10 s apart -- the second, inside
    the coalesce window, is counted (`(+N more)`) not typed, and the heal-
    style wake after the window lapses still produces the second wake. The
    DM body is in the log (record); the coalesced wake is the deliverable."""
    seat = "sanctuary-director"
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])

    assert send_mod._nudge_window(project, seat, body="dm one") is True
    assert len(_typed(calls)) == 1, calls
    capsys.readouterr()
    # second dm inside the window: counted as pending, not typed
    assert send_mod._nudge_window(project, seat, body="dm two") is False
    assert len(_typed(calls)) == 1
    assert "nudge: coalesced" in capsys.readouterr().err
    assert send_mod._pending_more(project, seat) == 1

    send_mod._nudge_marker_path(project, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")
    assert send_mod.wake(project, seat) is True
    assert len(_typed(calls)) == 2, calls


# ── a consuming read clears the coalesced nudge count ──
# (hypothesis:l4-a-read-clears-the-coalesced-nudge-count): the count is
# "how many sends coalesced into the one token", and a read drains them
# all. An empty read and a peek must NOT touch the sidecars.


def test_read_clears_coalesced_nudge_count(project: Path):
    """A read that consumes unread resets `.nudge.pending` to 0, drops the
    announced digest, and leaves `_seat_has_pending` False -- the repaired
    outcome: heal no longer types a bare nudge at an empty idle pane after
    every read."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    # three dms coalesced while the pane was busy/queued -> count becomes 3
    for _ in range(3):
        send_mod._bump_pending(project, seat)
    assert send_mod._pending_more(project, seat) == 3

    send_mod.read(project, seat, "prime")

    assert send_mod._pending_more(project, seat) == 0, \
        "a consuming read must clear the coalesced nudge count"
    assert send_mod._announced_digest(project, seat) is None
    assert send_mod._seat_has_pending(project, seat) is False, \
        "no fresh wake after a consuming read with nothing new sent"


def test_read_on_already_empty_inbox_leaves_count_untouched(project: Path):
    """An empty read must NOT touch the sidecars: a pre-existing coalesced
    count survives a read that consumed nothing."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    # an already-read inbox: only the marker, nothing after it -> no unread
    inbox.write_text("to: sanctuary-director\n" + send_mod.READ_MARKER)
    for _ in range(2):
        send_mod._bump_pending(project, seat)
    assert send_mod._pending_more(project, seat) == 2

    send_mod.read(project, seat, "prime")

    assert send_mod._pending_more(project, seat) == 2, \
        "an empty read must not clear the pre-existing count"


def test_peek_leaves_the_coalesced_nudge_count(project: Path):
    """peek is unchanged: it shows unread without consuming, so the count
    and the announced digest survive a peek."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    send_mod._bump_pending(project, seat)   # one coalesced dm
    send_mod._record_announced(project, seat, "digest")
    assert send_mod._pending_more(project, seat) == 1

    send_mod.peek(project, seat)

    assert send_mod._pending_more(project, seat) == 1, \
        "peek must not clear the coalesced count"
    assert send_mod._announced_digest(project, seat) == "digest"
    # and peek consumed nothing: a read now drains the count
    send_mod.read(project, seat, "prime")
    assert send_mod._pending_more(project, seat) == 0
    assert send_mod._announced_digest(project, seat) is None


def test_read_preserves_a_bump_made_during_the_read(
        project: Path, monkeypatch):
    """L4.294: a dm that coalesces DURING a consuming read is not lost. The
    clear is compare-and-clear (max(0, current - observed)) -- the read
    observes the count once before it consumes, then subtracts that value --
    so a bump made after the observe but before the clear survives instead
    of being silently zeroed by an unconditional write."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    send_mod._bump_pending(project, seat)   # count 1, observed pre-read
    assert send_mod._pending_more(project, seat) == 1

    real_print = send_mod._print_blocks_with_labels
    bumped = []

    def _bump_during_consume(root, me, blocks, wrap=160):  # SL2#8 seam: SL5.04 added `me` (quarantine path)
        # a send coalesces in the middle of the read's consume step, after
        # the read already observed the count: bump exactly once.
        if not bumped:
            send_mod._bump_pending(project, seat)
            bumped.append(True)
        real_print(root, me, blocks, wrap=wrap)

    monkeypatch.setattr(send_mod, "_print_blocks_with_labels",
                        _bump_during_consume)

    send_mod.read(project, seat, "prime")

    assert bumped, "the consume-step bump must actually fire"
    assert send_mod._pending_more(project, seat) == 1, \
        "a count bumped DURING the read must survive the compare-and-clear"


def test_clear_pending_observed_decrements_not_zeroes(project: Path):
    """_clear_pending with a caller-observed value subtracts it, never
    rewriting the count to 0 outright; absent observed still clears to 0."""
    seat = "sanctuary-director"
    _inbox = send_mod._inbox_dir(project)
    _inbox.mkdir(parents=True, exist_ok=True)
    send_mod._bump_pending(project, seat)   # current 1 (observed 1 pre-read)
    send_mod._bump_pending(project, seat)   # +1 coalesced during the read
    assert send_mod._pending_more(project, seat) == 2

    send_mod._clear_pending(project, seat, observed=1)
    assert send_mod._pending_more(project, seat) == 1, \
        "observed clear decrements by the observed value, not to zero"

    send_mod._clear_pending(project, seat)   # absent observed clears to 0
    assert send_mod._pending_more(project, seat) == 0


def test_wake_stale_id_is_named_and_falls_back_to_name(project: Path,
                                                       monkeypatch, capsys):
    """Clause (3): when the row window @id is no longer a LISTED window,
    wake prints `nudge repair: <seat> row window <@id> is gone; falling back
    to name` and THEN uses the by-NAME target (the same `_window_listed` path
    a name-addressed row uses). Test both halves: the line appears AND the
    fallback target is actually the send-keys target."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    inbox = send_mod._inbox_path(project, "sanctuary-director")
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    pane = _FixturePane()
    # the fake lists ONLY the seat NAME -- the @id @246 is stale (gone)
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    assert send_mod.wake(project, "sanctuary-director") is True
    cap = capsys.readouterr()
    assert "nudge repair: sanctuary-director row window @246 is gone; " \
           "falling back to name" in cap.err, cap.err
    typed = _typed(calls)
    assert typed, "the by-name fallback must have typed a token"
    assert typed[0][4] == "agi-rc:sanctuary-director", \
        f"fallback target must be the seat NAME, not the stale @id: " \
        f"{typed[0][4]}"
    assert cap.out.strip() == "typed-token"


def test_wake_live_id_keeps_id_target(project: Path, monkeypatch, capsys):
    """Clause (3) control: a @id that IS still a listed window is used as
    the target -- no `nudge repair:` line, no by-name fallback."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    inbox = send_mod._inbox_path(project, "sanctuary-director")
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    pane = _FixturePane()
    # the fake lists @246 as a CURRENT window -> the @id is live and wins
    calls = _fake_tmux_pane(monkeypatch, ["@246", "sanctuary-director"],
                            pane, [])
    assert send_mod.wake(project, "sanctuary-director") is True
    typed = _typed(calls)
    assert typed[0][4] == "agi-rc:@246", typed[0][4]
    assert "nudge repair:" not in capsys.readouterr().err


def test_send_stale_id_repairs_by_name(project: Path, monkeypatch, capsys):
    """Clause (b): the ORDINARY send path (not wake) never swallows a stale
    @id -- it prints `nudge repair:` and falls back to the by-NAME target,
    so the wake still reaches the seat and the inbox message stays intact.
    Before the fix `send` left the stale @id alone (best-effort) and the
    wake failed inside tmux send-keys with no line at all."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    pane = _FixturePane()
    # the fake lists ONLY the seat NAME -- @246 is stale (gone)
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    send_mod.send(project, "sanctuary-director", "hi from this kid", "kid")
    cap = capsys.readouterr()
    assert "nudge repair: sanctuary-director row window @246 is gone; " \
           "falling back to name" in cap.err, cap.err
    typed = _typed(calls)
    assert typed, "the by-name fallback must have typed a token"
    assert typed[0][4] == "agi-rc:sanctuary-director", \
        f"fallback target must be the seat NAME, not the stale @id: " \
        f"{typed[0][4]}"
    inbox = send_mod._inbox_path(project, "sanctuary-director")
    assert "hi from this kid" in inbox.read_text(), \
        "the message must still land in the inbox"


def test_send_stale_id_no_name_fallback_prints_one_line(
        project: Path, monkeypatch, capsys):
    """Clause (b): when the stale @id repair falls back by name AND no
    window named <seat> is listed either, send prints ONE named line (never
    silence) and the message STILL lands in the inbox."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    pane = _FixturePane()
    # the fake lists NEITHER @246 NOR the name -> both lookups fail
    calls = _fake_tmux_pane(monkeypatch, [], pane, [])
    send_mod.send(project, "sanctuary-director", "body still written", "kid")
    cap = capsys.readouterr()
    assert "nudge repair: sanctuary-director row window @246 is gone; " \
           "falling back to name" in cap.err, cap.err
    assert "nudge: sanctuary-director row window @246 is gone and no " \
           "window named sanctuary-director is listed -- message written, " \
           "no wake" in cap.err, cap.err
    assert not _typed(calls), "no window could be typed into"
    inbox = send_mod._inbox_path(project, "sanctuary-director")
    assert "body still written" in inbox.read_text()


def test_dm_stale_id_repairs_by_name(project: Path, monkeypatch, capsys):
    """Clause (b): the DM path also repairs a stale @id by name -- never
    swallowed -- and the dm body lands in the dm file."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    # send_dm resolves its nudge root via find_project_root -> the .agi
    # graph root; seats must be where THAT reader looks.
    (project / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (project / ".agi" / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "liaison", "role": "liaison",
                    "window": "@999", "pid": 424242}]))
    pane = _FixturePane()
    # the fake lists ONLY the seat NAME -- @999 is stale
    calls = _fake_tmux_pane(monkeypatch, ["liaison"], pane, [])
    path = send_mod.send_dm(project, "lion", "liaison", "rdm body", "lion")
    cap = capsys.readouterr()
    assert "nudge repair: liaison row window @999 is gone; " \
           "falling back to name" in cap.err, cap.err
    typed = _typed(calls)
    assert typed, "the by-name fallback must have typed a token"
    assert typed[0][4] == "agi-rc:liaison", typed[0][4]
    assert "rdm body" in Path(path).read_text()


def test_wake_delivers_deferred_dm_inline(project: Path, monkeypatch,
                                          capsys):
    """Clause (2): a stored deferred dm body (no unread inbox needed) is
    delivered INLINE by wake -> the ONE `delivered-deferred` outcome, and a
    non-empty deferred proves a real delivery (exit 0)."""
    seat = "director"
    send_mod._store_deferred(project, seat, "prime", "the deferred body")
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    assert send_mod.wake(project, seat) is True
    cap = capsys.readouterr()
    assert cap.out.strip() == "delivered-deferred"
    assert send_mod._read_deferred(project, seat) is None, \
        "the deferred body must be cleared once delivered"
    assert _typed(calls) and _enters(calls), calls


def test_wake_busy_outcome(project: Path, monkeypatch, capsys):
    """Clause (2): a BUSY pane with something pending -> the ONE
    `busy-deferred` outcome, nothing typed (exit 1)."""
    seat = "director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: director\nfrom: prime\n\n---\n hi\n")
    pane = _FixturePane(busy=True)
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    assert send_mod.wake(project, seat) is False
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    cap = capsys.readouterr()
    assert cap.out.strip() == "busy-deferred"
    assert "nudge: coalesced (pane busy" in cap.err


def test_wake_no_target_outcome(project: Path, monkeypatch, capsys):
    """Clause (2): a seat with no addressable window -> the ONE `no-target`
    outcome (exit 1), and NOTHING is typed -- a no-target wake must not send
    `tmux send-keys` into nobody's pane."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux_pane(monkeypatch, [], _FixturePane(), [])
    assert send_mod.wake(project, "ghost-seat") is False
    assert capsys.readouterr().out.strip() == "no-target"
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls), \
        "a no-target wake must type nothing"


# ── hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box ───
# clause (1): `_input_region` is the box, or '' -- never the whole pane


def test_input_region_is_empty_when_no_rendered_box():
    """Clause (1): a capture with NO `\u276f` box -- the just-submitted
    `[agi-nudge] unread for <seat>` token echoed in the TRANSCRIPT above where
    the box would be (SHAPE A: a busy pane rendered the spinner in place of the
    box) -- yields an EMPTY input region, never the whole pane. The whole pane
    (old 'conservative' branch) read the echoed token as a stranded line and
    wake RE-TYPED it: the six phantom tokens 19:17-19:33Z on master-sensei
    with an empty inbox. MEASURED shape in this session: a real busy pane
    (@291 sanctuary-director, captured live) is the OTHER shape -- it KEEPS the
    box and puts `esc to interrupt` in the footer; this function must be safe
    for both, and this no-box branch is the SHAPE A half."""
    capture = ("[agi-nudge] unread for sanctuary-director:"
               " send.py read sanctuary-director\n"
               "  \u23f5\u23f5 ... esc to interrupt ...\n")
    assert "\u276f" not in capture
    assert send_mod._input_region(capture) == ""


# clause (2): wake never resubmits on a busy pane -- SHAPE A (box hidden)


def test_busy_no_box_echoed_token_never_retyped(project: Path, monkeypatch,
                                                capsys):
    """SHAPE A fake: a busy pane rendered WITHOUT its box -- the echoed
    `[agi-nudge] unread for <seat>` token and the busy footer in the capture, no
    `\u276f` anywhere. clause (2): wake must NOT take the resubmitted-strand
    branch (it would RE-TYPE the echoed token into the empty-inbox pane), must
    type nothing, and must leave the `.nudge` marker untouched (clause (4)).
    The busy footer is read off the WHOLE capture because there is no box to
    scope the region to."""
    seat = "sanctuary-director"
    capture = ("[agi-nudge] unread for sanctuary-director:"
               " send.py read sanctuary-director\n"
               "  \u23f5\u23f5 esc to interrupt \u00b7 \u2190 for agents\n")
    assert "\u276f" not in capture
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    marker = send_mod._nudge_marker_path(project, seat)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("2020-01-01T00:00:00+00:00\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, [seat], capture_text=capture)
    assert send_mod.wake(project, seat) is False
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls), calls
    assert marker.read_text() == "2020-01-01T00:00:00+00:00\n", \
        "busy/no-box path must not stamp the marker (clause 4)"
    assert capsys.readouterr().out.strip() == "busy-deferred"


# SHAPE A, but idle/unknown: no box, no busy footer -> no strand, no typing


def test_no_box_idle_capture_reads_no_strand(project: Path, monkeypatch,
                                             capsys):
    """clause (i)/(iii): a capture with no `\u276f` box AND no busy footer (a
    pane scrolled above its box) must never read a transcript-echoed token as a
    stranded in-box line. wake types nothing and, with nothing pending,
    reports nothing-pending."""
    seat = "sanctuary-director"
    capture = ("[agi-nudge] unread for sanctuary-director:"
               " send.py read sanctuary-director\n")
    assert "\u276f" not in capture and "esc to interrupt" not in capture
    calls = _fake_tmux(monkeypatch, [seat], capture_text=capture)
    assert send_mod.wake(project, seat) is False
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls), calls
    cap = capsys.readouterr()
    assert cap.out.strip() in ("nothing-pending", "busy-deferred"), cap.out
    assert "nudge: " not in cap.err


# clause (2): a box-less, footer-less capture on a seat WITH pending never
# gets typed into -> the ONE `nothing-pending`, marker untouched.

def test_wake_no_box_pending_is_nothing_pending(project: Path, monkeypatch,
                                                capsys, tmp_path):
    """Clause (2) of hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-
    input-box-and-wake-names-its-path: a NON-BLANK capture with NO rendered
    `\u276f` box AND NO busy footer is never a confirmed idle box, so a seat
    WITH pending unread state must NOT be typed into. `wake` types nothing,
    leaves the `.nudge` marker untouched (nothing announced), reports the ONE
    `nothing-pending` outcome, and writes the reaper log line
    `idle nothing-pending`. Pre-fix: `_nudge_coalesce_reason` returned None
    here, so `wake` fell through to the ordinary type path and typed a token
    into a capture that cannot be a box."""
    seat = "sanctuary-director"
    logf = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logf))
    capture = ("[agi-nudge] unread for sanctuary-director:"
               " send.py read sanctuary-director\n"
               "some transcript body scrolled above the box\n")
    assert "\u276f" not in capture and "esc to interrupt" not in capture
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    marker = send_mod._nudge_marker_path(project, seat)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("2020-01-01T00:00:00+00:00\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, [seat], capture_text=capture)
    assert send_mod.wake(project, seat) is False
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls), calls
    assert marker.read_text() == "2020-01-01T00:00:00+00:00\n", \
        "a no-box pending wake must not stamp the marker"
    assert capsys.readouterr().out.strip() == "nothing-pending"
    lines = logf.read_text().splitlines()
    assert len(lines) == 1 and "idle nothing-pending" in lines[0], lines


# clause (2) send-side: a dm nudged into a box-less, footer-less capture is
# a COALESCE (`no rendered box`) -- deferred, never typed.


def test_dm_coalesces_no_rendered_box_and_defers_the_body(
        project: Path, monkeypatch, capsys):
    """hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-
    three-tests-assert-what-they-claim (P2b): `send_dm` to a seat whose
    capture is a NON-BLANK, box-less, footer-less transcript (no `\u276f`,
    no `esc to interrupt`) is the clause-(2) `(no rendered box)` COALESCE:
    ZERO `tmux send-keys`, the ONE `nudge: coalesced (no rendered box)`
    stderr line, and the dm body DEFERRED (carried by `_read_deferred`) for
    an idle retry -- never typed into a capture that cannot be a box."""
    seat = "sanctuary-helper"
    capture = ("[agi-nudge] unread for sanctuary-director:"
               " send.py read sanctuary-director\n"
               "some transcript body scrolled above the box\n")
    assert "\u276f" not in capture and "esc to interrupt" not in capture
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, [seat], capture_text=capture)
    send_mod.send_dm(project, "sanctuary-director", seat, "the dm body",
                     "sanctuary-director")
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls), calls
    assert "nudge: coalesced (no rendered box)" in capsys.readouterr().err
    assert send_mod._read_deferred(project / ".agi", seat) \
        == {"sender": "sanctuary-director", "body": "the dm body"}, \
        "the unrenderable dm must be deferred for an idle retry, not dropped"


# clause (3): the typed token names its path, prefix stays byte-identical


def test_wake_typed_token_names_its_path(project: Path, monkeypatch, capsys):
    """Clause (3): the typed wake token names its path `(wake:idle)` while its
    PREFIX stays byte-identical (`[agi-nudge] unread for <seat>`), so every
    `_NUDGE_PREFIXES` match and every reader's `unread for` grep keeps working,
    and the token still stays under the length cap."""
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    assert send_mod.wake(project, seat) is True
    texts = _typed_text(calls)
    assert texts and "(wake:idle)" in texts[0], texts
    assert texts[0].startswith("[agi-nudge] unread for " + seat), texts[0]
    assert len(texts[0]) < 100, len(texts[0])
    # still a nudge shape: a stranded one of this shape is still detected
    assert send_mod._stranded_in_region(
        "[agi-nudge] unread for " + seat + " (wake:idle)") is not None
    assert send_mod._build_nudge_token(seat, "strand").endswith("(wake:strand)")


# clause (3): ONE per-seat outcome line through the SAME resolver heal uses


def test_wake_logs_one_outcome_line_via_reaper_resolver(
        project: Path, monkeypatch, capsys, tmp_path):
    """Clause (3): `wake` writes ONE per-seat outcome line through the SAME
    resolver heal.py's `_watch_log` uses (AGI_REAPER_LOG env else stderr) --
    never a second log path. Shape: `wake <seat>: <path> <state> @<id>`."""
    import reaper_log as rl
    assert send_mod.reaper_log is rl, \
        "send.py must log through the shared reaper_log resolver"
    logf = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logf))
    seat = "sanctuary-director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: sanctuary-director\nfrom: prime\n\n---\n hi\n")
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    assert send_mod.wake(project, seat) is True
    lines = logf.read_text().splitlines()
    assert len(lines) == 1, lines
    # exactly one field set: `wake <seat>: <path> <state> <window>`; the
    # window id carries a SINGLE leading @ (never `@@`)
    assert lines[0] == f"wake {seat}: idle delivered sanctuary-director" or \
        lines[0] == f"wake {seat}: idle delivered", lines[0]


def test_wake_busy_logs_deferred_outcome_line(
        project: Path, monkeypatch, capsys, tmp_path):
    """Clause (3): the busy/deferred wake also logs its ONE line, state
    `deferred` (marker untouched -- the deferral is not a delivery)."""
    logf = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logf))
    seat = "director"
    inbox = send_mod._inbox_path(project, seat)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("to: director\nfrom: prime\n\n---\n hi\n")
    marker = send_mod._nudge_marker_path(project, seat)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("2020-01-01T00:00:00+00:00\n")
    pane = _FixturePane(busy=True)
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    assert send_mod.wake(project, seat) is False
    lines = logf.read_text().splitlines()
    assert len(lines) == 1, lines
    assert "deferred" in lines[0], lines[0]
    assert marker.read_text() == "2020-01-01T00:00:00+00:00\n"

    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)


def test_wake_main_exit_code_honest(project: Path, monkeypatch):
    """Clause (2): `send.py wake <seat>` exits 0 ONLY when something was
    delivered, 1 otherwise -- main() maps the wake() bool to the code."""
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    for delivered, want in ((True, 0), (False, 1)):
        monkeypatch.setattr(send_mod, "wake", lambda root, to: delivered)
        assert send_mod.main(["wake", "director"]) == want


def test_stranded_token_in_a_busy_pane_gets_no_enter(project: Path,
                                                     monkeypatch, capsys):
    """The heal never types into a mid-turn pane: busy wins over stranded.
    The busy fixture actually HOLDS the stranded token (its box renders the
    typed line) -- busy must still win even with a stranded line in the box."""
    pane = _FixturePane(busy=True)
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])
    cap = pane.capture()
    assert send_mod._nudge_token_head(_OLD_TOKEN) in cap, \
        "the busy fixture must actually hold the stranded token in its box"
    calls = _fake_tmux_pane(monkeypatch, ["director"], pane, [])
    send_mod.send(project, "director", "the body", "kid")
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    assert "nudge: coalesced (pane busy" in capsys.readouterr().err


def test_real_busy_capture_reads_busy_from_the_footer():
    """The REAL busy capture (fixtures/claude_pane_busy.txt) KEEPS the `\u276f`
    box; `esc to interrupt` sits in the FOOTER below it. Scoped to the input
    region (from the last `\u276f`), the busy signal is still caught -- the
    box does not hide it. This is the shape the old box-less fixture lacked."""
    busy = _fixture_text("claude_pane_busy.txt")
    assert "\u276f" in busy, "a real busy pane keeps its input box"
    assert "esc to interrupt" in busy.lower()
    # the region starts at the box and reaches the footer
    region = send_mod._input_region(busy)
    assert "\u276f" in region
    assert "esc to interrupt" in region.lower()
    assert send_mod._nudge_coalesce_reason(busy, "any-token", None) \
        == "pane busy (spinner)"


def test_real_idle_capture_is_not_busy():
    """The REAL idle capture (fixtures/claude_pane_idle.txt) has the same box
    and separator but NO `esc to interrupt` in its footer -- not busy."""
    idle = _fixture_text("claude_pane_idle.txt")
    assert "\u276f" in idle
    assert "esc to interrupt" not in idle.lower()
    assert send_mod._nudge_coalesce_reason(idle, "any-token", None) is None


def test_real_busy_capture_narrowed_region_misses_the_busy_signal():
    """FALSIFIER (hypothesis:l4-the-busy-pane-fixture-is-a-real-capture): with
    the REAL busy capture the busy signal (`esc to interrupt`) lives in the
    FOOTER BELOW the `\u276f` box. A region narrowed to exclude the box --
    stopping at the box line, dropping the footer under it -- no longer reads
    as busy. The old box-less fixture could not expose this (its `esc to
    interrupt` WAS the box), which is exactly why it was a false capture."""
    busy = _fixture_text("claude_pane_busy.txt")
    lines = busy.splitlines()
    box_idx = max(i for i, l in enumerate(lines) if "\u276f" in l)
    box_only = lines[box_idx]              # `\u276f ` -- the box alone
    assert "esc to interrupt" not in box_only.lower()
    # current region reaches the footer -> busy
    assert send_mod._nudge_coalesce_reason(busy, "t", None) \
        == "pane busy (spinner)"
    # a narrowed region that stops at the box misses the footer -> not busy
    assert send_mod._nudge_coalesce_reason(box_only, "t", None) is None


def test_nudge_token_is_short_for_every_seat_name():
    """< 100 chars for the live seat names and for an absurd one (which
    falls back to the bare form rather than breaching the cap)."""
    for seat in ("sanctuary-director", "sanctuary-helper", "belam",
                 "seat-sanctuary-helper-bd", "x" * 60):
        token = send_mod._build_nudge_token(seat)
        assert len(token) < 100, (seat, len(token))
        assert token.startswith(f"[agi-nudge] unread for {seat}")
    assert send_mod._build_nudge_token("x" * 60) == \
        send_mod.NUDGE_TOKEN_BARE_TEMPLATE.format(seat="x" * 60)


class _SafeSubprocess:
    """A subprocess stand-in installed for EVERY test in this file (autouse
    below), so send.py's own calls stay under a STRICT guard -- not just the
    selective, project-wide one that conftest.py's `_no_real_tmux`
    (hypothesis:l4-conftest-tmux-guard) now also provides for every module.

    Restored 2026-09-10 (review, sanctuary-helper): the conftest-wide guard
    supersedes this one for coverage (it reaches rotate.py, season.py and
    mail_alert.py's own separate `send_mod` too, which this one never did)
    but NOT for drift protection. `_nudge_window` fires only after a
    successful `tmux list-windows`; this stub answers returncode 1 ("no such
    session"), so the nudge short-circuits to False for every test unless a
    test deliberately swaps in its own fake (the three `_fake_tmux` tests
    below do, and their setattr wins because it runs in the test body after
    this autouse fixture). The two guards compose rather than duplicate:
    this one replaces send_mod's OWN `subprocess` name with this instance,
    which is a strictly narrower and later rebinding than conftest's patch
    of the real `subprocess.run` -- so for calls that go through `send_mod`
    specifically, THIS is what actually answers them.

    Guard: if send.py ever grows a real non-tmux subprocess call, this
    raises instead of silently faking it -- the one thing a pass-through
    guard structurally cannot do, because passing non-tmux calls through is
    its entire point. Losing this when the project-wide guard landed was a
    named regression (hypothesis:l4-conftest-tmux-guard), not a rewrite.
    """
    TimeoutExpired = subprocess.TimeoutExpired

    def run(self, cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return subprocess.CompletedProcess(cmd, 1)
        raise AssertionError(f"send.py issued a non-tmux subprocess call "
                             f"under test: {cmd!r}")


@pytest.fixture(autouse=True)
def _no_real_tmux(monkeypatch):
    """hypothesis:l4b23-fixture-leak — send.py's own calls stay under the
    STRICT stand-in above, layered under conftest.py's project-wide one.
    """
    monkeypatch.setattr(send_mod, "subprocess", _SafeSubprocess())


def test_send_nudges_existing_window(project: Path, monkeypatch):
    sleeps: list = []
    calls = _fake_tmux(monkeypatch, ["director"], sleeps=sleeps)
    send_mod.send(project, "director", "hello world", "a00-xxxx")
    nudges = _typed(calls)
    # residue 3: the plain _fake_tmux tests never pay a real 0.3 s sleep -
    # the recorded sleep is from the monkeypatched recorder, so the suite
    # does not wait on the wall clock.
    assert sleeps == [send_mod._NUDGE_ENTER_DELAY_S], sleeps
    assert nudges, "expected a wake-token nudge to the director's window"
    assert nudges[0][:5] == ["tmux", "send-keys", "-l", "-t", "agi-rc:director"]
    # the typed text is the FIXED wake token, NEVER the message body
    token = nudges[0][5]
    assert "hello world" not in token
    assert token.startswith("[agi-nudge] unread for director:")
    assert token.endswith("send.py read director")
    assert "Enter" not in nudges[0], "the Enter is a SEPARATE call"
    assert _enters(calls) == [["tmux", "send-keys", "-t", "agi-rc:director",
                               "Enter"]]
    # the inbox contract is unchanged
    assert (project / ".agi" / "sessions" / "inbox" / "director.md").is_file()


def test_send_dm_nudges_other_party(project: Path, monkeypatch):
    """The DM wake now carries the body INLINE (hypothesis:l4-the-nudge-
    carries-the-dm-body-inline): `[nudge: <from>]: <body>` -- the recipient
    sees the message without a `send.py read` round-trip. The body still
    lands in the dm file (the record); the pane line is the delivery. The
    literal-then-Enter shape is unchanged: never `text Enter` in one call."""
    calls = _fake_tmux(monkeypatch, ["adv-alive"])
    send_mod.send_dm(project, "mee", "adv-alive", "psst over the wall",
                     "mee")
    nudges = _typed(calls)
    assert nudges
    assert nudges[0][4] == "agi-rc:adv-alive"
    line = nudges[0][5]
    assert line == "[nudge: mee]: psst over the wall", line
    assert line.startswith("[nudge: mee]: ")
    assert "psst over the wall" in line       # the body is INLINE now
    assert "send.py read" not in line, "no read round-trip needed"
    assert "Enter" not in nudges[0], "the Enter is a SEPARATE call"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               "agi-rc:adv-alive", "Enter"]]
    # the body still lands in the dm file (the record)
    dm = project / "dm" / "adv-alive--mee.md"
    assert dm.is_file() and "psst over the wall" in dm.read_text()


def test_dm_nudge_flattens_newlines(project: Path, monkeypatch):
    """A body with newlines FLATTENS to one ` / `-joined line in the pane
    line (a newline would paste as more than one line / Enter)."""
    calls = _fake_tmux(monkeypatch, ["adv-alive"])
    send_mod.send_dm(project, "mee", "adv-alive",
                     "line one\n\nline two", "mee")
    line = _typed(calls)[0][5]
    assert "\n" not in line
    assert line == "[nudge: mee]: line one / line two", line
    assert "send.py read" not in line


def test_dm_nudge_truncates_with_read_tail(project: Path, monkeypatch):
    """A body long enough to exceed the measured line cap is TRUNCATED with
    a `… (read <seat>)` tail; the whole delivered line stays under
    `_NUDGE_LINE_MAX` (95, safely under the 100-char paste threshold) and
    the body head survives."""
    long = "w" * 200
    calls = _fake_tmux(monkeypatch, ["adv-alive"])
    send_mod.send_dm(project, "mee", "adv-alive", long, "mee")
    line = _typed(calls)[0][5]
    assert len(line) <= send_mod._NUDGE_LINE_MAX, (len(line), line)
    assert line.endswith("… (read adv-alive)"), line
    assert line.startswith("[nudge: mee]: ")
    body = line[len("[nudge: mee]: "):]
    assert body, "a truncated body must not be entirely eaten"
    assert body.startswith("w") and "…" in body


def test_dm_nudge_line_head_matches_wrapped():
    """The inline line's HEAD (`[nudge: <from>:`) is what the unsubmitted
    check matches, so a line the input box wrapped across two lines is still
    seen; a pane holding unrelated text is not (the token-head contract,
    now applied to the inline body line)."""
    line = send_mod._nudge_line("adv-alive", "mee", "hello world")
    assert send_mod._nudge_token_head(line) == "[nudge: mee]:"
    wrapped = "\u276f [nudge: mee]: hello\n  world\n"
    assert send_mod._nudge_coalesce_reason(wrapped, line, None) \
        == "token already unsubmitted"
    assert send_mod._nudge_coalesce_reason("\u276f other\n", line, None) \
        is None


def test_every_delivered_line_within_nudge_line_max(project: Path,
                                                   monkeypatch):
    """CLAUSE (c) FALSIFIER (hypothesis:l4-send-py-same-sender-stranded-line-
    and-the-swallowed-wake): NO delivery path may emit a line longer than
    `_NUDGE_LINE_MAX`. Exercised on the three tails that reach a pane: a
    plain large dm (truncation tail), a large deferred-dm delivery riding an
    inbox retry (the `${_NUDGE_INBOX_TAIL}` case -- 127 chars on the OLD
    bytes, because the inbox tail was `+=`d AFTER `_nudge_line` had already
    truncated), and a `(+N more)` batch. Old bytes: 127 > 95."""
    seat, sender = "adv-alive", "mee"
    big = "word " * 80                      # flattened body well over the cap
    cap = send_mod._NUDGE_LINE_MAX
    # (1) plain large dm
    calls1 = _fake_tmux(monkeypatch, [seat])
    send_mod.send_dm(project, sender, seat, big, sender)
    plain = _typed(calls1)[0][5]
    assert len(plain) <= cap, (len(plain), plain)
    # (2) large deferred-dm delivery riding an inbox retry -- the real
    #     delivering_deferred branch of send(): the inbox tail is counted
    #     INSIDE the truncation budget, not `+=`d after it (old bytes 127)
    root = project / ".agi"
    assert send_mod._store_deferred(root, seat, sender, big)
    # age the per-seat marker left by part (1) so this inbox retry fires
    marker = root / "sessions" / "inbox" / f"{seat}.nudge"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("2020-01-01T00:00:00+00:00\n")
    pane = _FixturePane()                                  # idle
    calls2 = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")       # body=None -> defer
    typed = _typed(calls2)
    deferred = typed[0][5]
    assert len(deferred) <= cap, (len(deferred), deferred)
    assert deferred.endswith(send_mod._NUDGE_INBOX_TAIL.format(seat=seat)), \
        deferred                      # the tail still lands
    assert send_mod._read_deferred(root, seat) is None     # consumed
    # (3) (+N more) batch
    batch = send_mod._nudge_line(seat, sender, big, more=3)
    assert len(batch) <= cap, (len(batch), batch)


def test_nudge_line_never_exceeds_max_for_any_name_lengths():
    """PROPERTY FALSIFIER (residue of clause c, hypothesis:l4-send-py-same-
    sender-stranded-line-and-the-swallowed-wake): for EVERY seat and sender
    name length 1..40, `_nudge_line` never emits a line longer than
    `_NUDGE_LINE_MAX` -- even when the inbox tail rides the delivery and
    `more>0` -- and never grows the body slice past the budget (old bytes:
    `flat[:keep]` with a negative `keep` returned a LONG slice, emitting a
    494-char line against the 95-char cap for a long same-name pair).
    Flattened body `word `*80 is far over the cap, so the body is always
    needing truncation."""
    cap = send_mod._NUDGE_LINE_MAX
    big = "word " * 80
    for sender_len in range(1, 41):
        for seat_len in range(1, 41):
            sender = "A" * sender_len
            seat = "S" * seat_len
            for trailing, more in (
                    ("", 0),
                    (send_mod._NUDGE_INBOX_TAIL.format(seat=seat), 0),
                    (send_mod._NUDGE_INBOX_TAIL.format(seat=seat), 3),
                    ("", 3)):
                line = send_mod._nudge_line(seat, sender, big, more=more,
                                            trailing=trailing)
                assert len(line) <= cap, \
                    (sender_len, seat_len, more, len(line), line[:40])


def test_nudge_line_floors_keep_on_the_measured_counterexample():
    """PINNED FALSIFIER (residue of clause c): the exact measured
    counterexample -- the long same-name pair plus the inbox tail, which on
    the OLD bytes emitted a 494-char line (5.2x the 95-char cap) -- now
    stays at or under `_NUDGE_LINE_MAX` for every seat/sender length 1..40
    with `trailing=_NUDGE_INBOX_TAIL`."""
    cap = send_mod._NUDGE_LINE_MAX
    for n in range(1, 41):
        name = "x" * n
        trailing = send_mod._NUDGE_INBOX_TAIL.format(seat=name)
        line = send_mod._nudge_line(name, name, "word " * 80,
                                    trailing=trailing)
        assert len(line) <= cap, (n, len(line), line)


def test_nudge_line_max_derived_from_fixture_geometry():
    """CLAUSE (c): `_NUDGE_LINE_MAX` is (re)derivable from the REAL capture's
    geometry -- the `─` separator row is 104 columns and the input box
    renders a `❯ ` (U+276F + space, 2 columns) prefix -- NOT a magic number.
    Asserts the relationship, not a hardcoded int."""
    idle = _fixture_text("claude_pane_idle.txt").splitlines()
    busy = _fixture_text("claude_pane_busy.txt").splitlines()
    def sep_width(lines):
        return max(len(l) for l in lines if set(l.strip()) == {"─"})
    for lines in (idle, busy):
        assert lines, "fixture must carry the verbatim region"
        w = sep_width(lines)
        assert w >= 100, (w,)                     # a real wide pane
        box_prefix = 2                            # `❯ ` (U+276F + space)
        box_content = w - box_prefix              # one-row line budget
        assert send_mod._NUDGE_LINE_MAX <= box_content, \
            (send_mod._NUDGE_LINE_MAX, box_content)
        assert send_mod._NUDGE_LINE_MAX < 100, \
            send_mod._NUDGE_LINE_MAX  # under the paste threshold


def test_dm_nudge_defers_under_busy_pane(project: Path, monkeypatch, capsys):
    """BUSY DEFER UNCHANGED for the dm path: a busy pane receives NO typed
    inline line (no body text, no concatenation) and reports a coalesce --
    the inline body never types into a mid-turn pane. Runs on the REAL busy
    capture fixture (clause d of hypothesis:l4-send-py-same-sender-stranded-
    line-and-the-swallowed-wake): a test that passes only on the box-less
    synthetic spinner is the very defect this clause names."""
    busy = _fixture_text("claude_pane_busy.txt")
    calls = _fake_tmux(monkeypatch, ["adv-alive"], capture_text=busy)
    send_mod.send_dm(project, "mee", "adv-alive", "urgent", "mee")
    nudges = [c for c in calls if c[:2] == ["tmux", "send-keys"]]
    assert nudges == [], "busy dm pane must receive NO typed line"
    assert "nudge: coalesced (pane busy" in capsys.readouterr().err


def test_dm_batch_coalesces_with_more_tail(project: Path, monkeypatch,
                                           capsys):
    """Coalesced dms out of a batch: the first dm delivers its body; a dm
    inside the window is coalesced (not typed) and counted; the NEXT
    delivered line carries `(+N more, read <seat>)` -- coalesce stays as
    landed by L4.126 (one delivery per window), the tail is the enrichment."""
    calls = _fake_tmux(monkeypatch, ["adv-alive"])
    send_mod.send_dm(project, "mee", "adv-alive", "first", "mee")
    assert _typed(calls)[0][5] == "[nudge: mee]: first"
    send_mod.send_dm(project, "mee", "adv-alive", "second", "mee")
    assert len(_typed(calls)) == 1, "the second dm must NOT type"
    # age the marker so the next dm leaves the window and delivers
    marker = project / ".agi" / "sessions" / "inbox" / "adv-alive.nudge"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("2020-01-01T00:00:00+00:00\n")
    send_mod.send_dm(project, "mee", "adv-alive", "third", "mee")
    typed = _typed(calls)
    assert len(typed) == 2, typed
    assert typed[1][5] == \
        "[nudge: mee]: third (+1 more, read adv-alive)", typed[1][5]
    assert "nudge: coalesced" in capsys.readouterr().err
    # the pending count was consumed by the delivered line
    assert send_mod._pending_more(project, "adv-alive") == 0


def test_dm_deferred_under_busy_retries_inline(project: Path, monkeypatch,
                                                capsys):
    """FALSIFIER (hypothesis:l4-the-nudge-carries-the-dm-body-inline): a dm
    that coalesces on a BUSY pane must reach the pane INLINE when it
    eventually goes out, not as the old wake token. The busy send stores the
    deferred body; the idled retry (an inbox `send()`, body=None) delivers it
    as `[nudge: <from>]: <body>` -- the round-trip survives no longer.

    Old bytes: the busy dm stored nothing, so the idle retry typed the fixed
    `[agi-nudge] unread for <seat> ...` wake token -- the very round-trip
    this hypothesis exists to remove, exactly in the common mid-turn case.
    """
    captures = ["...⠋...\nesc to interrupt\n", ""]   # busy, then idle
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="adv-alive\n",
                                               stderr="")
        if cmd[:2] == ["tmux", "capture-pane"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout=captures.pop(0),
                                               stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: None)
    # a dm lands while the pane is busy -> coalesced, no typed line
    root = project / ".agi"
    send_mod.send_dm(project, "mee", "adv-alive", "urgent talk", "mee")
    assert _typed(calls) == [], "busy send must not type"
    assert send_mod._read_deferred(root, "adv-alive") is not None
    # the pane goes idle; an inbox retry (body=None) fires
    send_mod.send(project, "adv-alive", "placeholder", "ki")
    typed = _typed(calls)
    assert len(typed) == 1, typed
    line = typed[0][5]
    assert line == \
        "[nudge: mee]: urgent talk (+unread inbox, read adv-alive)", line
    assert "send.py read" not in line, "the deferred dm body, not the wake"
    assert "inbox" in line, \
        "the inbox send's own wake must not be swallowed (clause b)"
    assert "nudge: coalesced (pane busy" in capsys.readouterr().err
    # the deferred body was consumed by the delivered line
    assert send_mod._read_deferred(root, "adv-alive") is None


# ── L4.140 residues: never append a second line, never clear an
#    undelivered deferred ──────────────────────────────────────────────────

def test_stranded_inline_line_no_concat_on_inbox_retry(project: Path,
                                                      monkeypatch, capsys):
    """RESIDUE A FALSIFIER (1): an inline dm line stranded in the box (by a
    failed long delivery) followed by an inbox `send()` retry must NOT
    concatenate. Old bytes compared only the retry's own head
    (`[agi-nudge] ...`) against the box, found no match, and TYPED the wake
    token after the stranded inline line -- the separate Enter then submitted
    BOTH as one user turn (the owner's 2026-09-11 defect, a `[nudge: mee]:
    first body[agi-nudge] unread ...` concatenation). Fixed: ANY stranded
    nudge line is detected; the Enter submits the stranded line ALONE and
    nothing is typed after it."""
    pane = _FixturePane()
    pane.send_keys(["-l", "-t", "w", "[nudge: mee]: first body"])
    assert pane.submitted == [] and pane.input == "[nudge: mee]: first body"
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send(project, "adv-alive", "hello", "ki")   # inbox retry
    assert _typed_text(calls) == [" "], \
        "the only typed retry key is ONE space (never a second line)"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               "agi-rc:adv-alive", "Enter"]]
    assert pane.submitted == ["[nudge: mee]: first body" + " "], pane.submitted
    assert pane.input == ""


def test_stranded_wake_token_dm_no_concat(project: Path, monkeypatch,
                                          capsys):
    """RESIDUE A FALSIFIER (2a): a stranded `[agi-nudge]` wake token, then a
    dm -- the dm's inline line must not be typed after the token; the token
    is submitted ALONE and the dm's body is DEFERRED (carried by a later
    retry), never appended as a second line."""
    pane = _FixturePane()
    tok = send_mod._build_nudge_token("adv-alive")
    pane.send_keys(["-l", "-t", "w", tok])
    assert pane.submitted == [] and pane.input == tok
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send_dm(project, "mee", "adv-alive", "dm body", "mee")
    assert _typed_text(calls) == [" "], \
        "the only typed retry key is ONE space (never an inline line after the token)"
    assert pane.submitted == [tok + " "], pane.submitted
    assert pane.input == ""
    assert send_mod._read_deferred(project / ".agi", "adv-alive") \
        is not None, "the dm body must be deferred, not lost"


def test_rotation_alert_line_dm_no_concat(project: Path, monkeypatch, capsys):
    """RESIDUE A FALSIFIER (2c): a stale `[rotation-alert] ...` line left in
    the box by rotate.py (not send.py), then a dm -- the dm's inline line
    must never be typed after it (no concatenation). The stale line is
    submitted alone."""
    pane = _FixturePane()
    pane.send_keys(["-l", "-t", "w", "[rotation-alert] changing seats"])
    assert pane.submitted == [] and pane.input == "[rotation-alert] "\
        "changing seats"
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send_dm(project, "mee", "adv-alive", "dm body", "mee")
    assert _typed_text(calls) == [" "], \
        "the only typed retry key is ONE space (never a line after rotation-alert)"
    assert pane.submitted == ["[rotation-alert] changing seats" + " "], \
        pane.submitted
    assert pane.input == ""
    assert send_mod._read_deferred(project / ".agi", "adv-alive") \
        is not None, "the dm body must be deferred, not lost"


def test_deferred_kept_when_different_line_submitted(project: Path,
                                                     monkeypatch, capsys):
    """RESIDUE B FALSIFIER: a deferred dm body is cleared ONLY when a line
    CARRYING it is actually submitted (probe-C on its own stranded line / the
    plain delivery path). When the box holds a DIFFERENT stranded line, the
    probe-(C) Enter submits that line ALONE and the deferred body must
    SURVIVE for a later retry. Old bytes ran `_clear_deferred` unconditionally
    in the probe-(C) branch, dropping a deferred body that had never reached
    the pane."""
    root = project / ".agi"
    assert send_mod._store_deferred(root, "adv-alive", "mee", "urgent")
    pane = _FixturePane()
    pane.send_keys(["-l", "-t", "w", "[rotation-alert] rotating"])  # other
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send(project, "adv-alive", "placeholder", "ki")  # inbox retry
    assert pane.submitted == ["[rotation-alert] rotating" + " "], pane.submitted
    assert pane.input == ""
    assert send_mod._read_deferred(root, "adv-alive") is not None, \
        "the deferred body must survive (it never reached the pane)"


def test_deferred_cleared_when_its_own_line_stranded(project: Path,
                                                     monkeypatch, capsys):
    """RESIDUE B control: when the stranded line IS the deferred body's own
    line, the idle retry submitting it MAY clear the deferred -- a line
    carrying it reached the pane. Distinguishes the keep-on-different-line fix
    from a blanket 'never clear'."""
    root = project / ".agi"
    assert send_mod._store_deferred(root, "adv-alive", "mee", "urgent")
    pane = _FixturePane()
    pane.send_keys(["-l", "-t", "w", "[nudge: mee]: urgent"])
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send(project, "adv-alive", "placeholder", "ki")  # inbox retry
    assert pane.submitted == ["[nudge: mee]: urgent" + " "], pane.submitted
    assert pane.input == ""
    assert send_mod._read_deferred(root, "adv-alive") is None, \
        "the deferred body's own line was delivered -- cleared"


def test_same_sender_stranded_line_does_not_swallow_new_dm(
        project: Path, monkeypatch, capsys):
    """CLAUSE (a) FALSIFIER (hypothesis:l4-send-py-same-sender-stranded-line-
    and-the-swallowed-wake): a stranded inline line left by an EARLIER dm
    from the SAME sender (different body) shares the head `[nudge: <from>]:`
    with the new dm. Old bytes matched only that head, read the older line as
    "ours", Entered it, recorded the marker and cleared pending -- and never
    stored the NEW body, so the new dm is neither typed nor deferred: lost
    until the next wake. Fixed: the head alone is not proof our SPECIFIC
    body reached the pane; unless the new body is shown in the pane, the new
    dm must be carried (deferred), never dropped."""
    root = project / ".agi"
    pane = _FixturePane()
    pane.send_keys(["-l", "-t", "w", "[nudge: mee]: older body"])
    assert pane.submitted == [] and pane.input == "[nudge: mee]: older body"
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send_dm(project, "mee", "adv-alive", "newer body", "mee")
    # the stranded OLDER line alone is submitted -- no second line typed
    assert _typed_text(calls) == [" "], \
        "the new dm must type only ONE space, never a second line after the strand"
    assert pane.submitted == ["[nudge: mee]: older body" + " "], pane.submitted
    assert pane.input == ""
    # the NEW body survives -- deferred for a later idle retry, never dropped
    assert send_mod._read_deferred(root, "adv-alive") \
        == {"sender": "mee", "body": "newer body"}, \
        "the new same-sender dm body must be deferred, not lost"


def test_wrapped_own_stranded_line_is_recognised_as_ours(
        project: Path, monkeypatch, capsys):
    """FALSIFIER (hypothesis:l4-rendered-line-ownership-tolerates-the-wrap,
    clause (d) continuation): the box WRAPS a line wider than the pane
    across display rows (the fixture pane is 80 columns), inserting a `\n`
    mid-line. OLD bytes tested `own_line in region` against that split
    region, so OUR OWN 88-char stranded line (longer than the 80-col pane)
    showed on two rows and never matched -- it read as foreign and was
    re-deferred forever. Fixed: the ownership check collapses the wrap on
    the region side (joins the rows, drops the wrap-inserted whitespace)
    before the membership test, so a wrapped own line is recognised and
    submitted with Enter only."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    body = ("ask the sanctuary director about the merged seat rotation "
            "and home dir pad")
    line = send_mod._nudge_line(seat, sender, body)   # the rendered line
    assert len(line) > 80 \
        and len(line) <= send_mod._NUDGE_LINE_MAX, f"line {len(line)}"
    pane = _FixturePane(width=80)      # the panel wraps our >80-char line
    pane.send_keys(["-l", "-t", "w", line])
    assert pane.submitted == []
    assert len(pane.capture().splitlines()) > 1, "the pane wraps the line"
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, sender, seat, body, sender)
    # recognised as ours: Enter only, no second line, nothing deferred
    assert _typed_text(calls) == [" "], \
        "stranded resubmit types ONE space, never a new nudge line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own line is a real delivery -- nothing deferred"
    assert send_mod._last_nudge_age(project, seat) is not None, "marker stamped"
    assert "submitted a stranded token" in capsys.readouterr().err


def test_wrapped_own_line_recognised_at_measured_104(
        project: Path, monkeypatch, capsys):
    """FALSIFIER companion (hypothesis:l4-rendered-line-ownership-tolerates-
    the-wrap): the same >80-char rendered line at the MEASURED pane width (104
    columns -- the sanctuary-director pane) does NOT wrap, so ownership must
    hold there too. Guards the regression where a collapse fix only handled
    the fixture width and dropped the no-wrap case."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    body = ("ask the sanctuary director about the merged seat rotation "
            "and home dir pad")
    line = send_mod._nudge_line(seat, sender, body)
    assert len(line) <= 104, f"line {len(line)}"
    pane = _FixturePane(width=104)     # the measured width: no wrap
    pane.send_keys(["-l", "-t", "w", line])
    assert pane.submitted == [] and pane.input == line
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, sender, seat, body, sender)
    assert _typed_text(calls) == [" "], \
        "stranded resubmit types ONE space, never a new nudge line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own line is a real delivery -- nothing deferred"
    assert send_mod._last_nudge_age(project, seat) is not None, "marker stamped"
    assert "submitted a stranded token" in capsys.readouterr().err


def test_wrapped_own_line_cell_wrapped_recognised_at_80(
        project: Path, monkeypatch, capsys):
    """Fix-only #2 FALSIFIER (hypothesis:l4-rendered-line-ownership-tolerates-
    the-wrap): the earlier fix joined the wrapped rows with ONE SPACE, which
    recognises a WORD-boundary wrap but not the CELL wrap a real tmux pane
    performs -- a line split in the MIDDLE of a word has no whitespace at the
    break, so a space-join inserts a spurious space and the own line still
    never matches. This fixture CELL-wraps (mid-word) at width 80: the
    reconstructed region must be owned under BOTH joins, so the own stranded
    line is recognised and submitted with Enter only."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    body = ("the rotation merged five seats and repointed every pin "
            "from the sanctuary home")
    line = send_mod._nudge_line(seat, sender, body)
    assert len(line) > 80, f"line {len(line)}"
    pane = _FixturePane(width=80, cell=True)   # mid-word cell wrap
    pane.send_keys(["-l", "-t", "w", line])
    assert pane.submitted == []
    assert len(pane.capture().splitlines()) > 1, "the pane cell-wraps the line"
    # the cell wrap must actually split MID-WORD, else the space-join would
    # already reconstruct it and this would not be a cell-wrap falsifier
    region = pane.capture()
    first, second = region.splitlines()[0], region.splitlines()[1]
    tail = first.lstrip().lstrip("\u276f").lstrip()[-1]
    head = second.strip()[0]
    assert tail != " " and head != " " and tail != head, \
        f"boundary {tail!r}/{head!r} is not a mid-word cell split"
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, sender, seat, body, sender)
    # recognised as ours under the cell (empty) join: Enter only, nothing typed
    assert _typed_text(calls) == [" "], \
        "stranded resubmit types ONE space, never a new nudge line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own line is a real delivery -- nothing deferred"
    assert send_mod._last_nudge_age(project, seat) is not None, "marker stamped"
    assert "submitted a stranded token" in capsys.readouterr().err


def test_region_join_wrap_cell_wrapped_at_measured_104():
    """Fix-only #2 FALSIFIER (hypothesis:l4-rendered-line-ownership-tolerates-
    the-wrap): the `_region_join_wrap` FALLBACK (a region captured WITHOUT
    `-J`) must also reconstruct an own line that tmux CELL-wrapped mid-word at
    the MEASURED pane width (104 columns). A word-boundary (space) join cannot
    restore a mid-word break -- only the no-space (cell) join can -- so the
    helper must offer BOTH and ownership must accept either."""
    body = "abcdefghij" * 20                 # >104 chars, no spaces -> mid-word
    line = "[nudge: adv-alive]: " + body
    assert len(line) > 104, f"line {len(line)}"
    # cell-wrap it at 104 the way a real pane would (no space at the break)
    wrapped = line[:104] + "\n" + line[104:]
    assert wrapped[103] != " " and wrapped[104] != " "  # mid-word boundary
    region = "\u276f " + wrapped
    space, empty = send_mod._region_join_wrap(region)
    assert line not in space, \
        "a word-boundary (space) join cannot reconstruct a mid-word cell wrap"
    assert line in empty, "the no-space (cell) join restores a mid-word wrap"
    assert any(line in c for c in (space, empty)), "ownership accepts either"


def test_capture_pane_uses_join_flag(project, monkeypatch):
    """Fix-only #2 CLAIM (hypothesis:l4-rendered-line-ownership-tolerates-
    the-wrap): the ownership capture passes `-J` (`tmux capture-pane -p -J`) so
    a REAL capture joins soft-wrapped lines and carries no soft-wrap at all;
    `_region_join_wrap` remains the fallback for a region without `-J`. The
    argv of every capture-pane call a send makes must contain `-J`."""
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send_dm(project, "mee", "adv-alive", "hello world", "mee")
    caps = [c for c in calls if c[:2] == ["tmux", "capture-pane"]]
    assert caps, "a dm send must capture the pane for the ownership check"
    for c in caps:
        assert "-J" in c, f"capture-pane argv must carry -J: {c}"


def test_deferred_strand_judged_with_the_rendered_more_count(
        project: Path, monkeypatch, capsys):
    """FALSIFIER (hypothesis:l4-deferred-ownership-uses-the-rendered-count):
    a short deferred dm delivered by an inbox retry is stranded in the pane
    with the `(+N more, read <seat>)` tail count AT ITS render time. A later
    retry that renders its ownership line with the CURRENT pending count (a
    drift, e.g. more coalesced since) reads that own strand as FOREIGN, keeps
    the deferred record, and the NEXT retry types the body AGAIN -- delivered
    twice for one deferral. Fixed: the deferred record stores the `more`
    count each delivery rendered with, and ownership judges against THAT
    render, so the own strand is recognised (Enter only) and the deferred
    record cleared -- never typed twice."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    assert send_mod._store_deferred(root, seat, sender, "urgent")
    # simulate a PRIOR delivery render that typed the strand with more=1
    send_mod._record_deferred_render(root, seat, 1)
    assert send_mod._read_deferred(root, seat).get("more") == 1
    # the pending count has since grown to 3 (two more coalesced)
    send_mod._clear_pending(root, seat)
    send_mod._bump_pending(root, seat)
    send_mod._bump_pending(root, seat)
    send_mod._bump_pending(root, seat)
    assert send_mod._pending_more(root, seat) == 3
    # the pane holds the strand typed by that prior delivery (more=1 tail +
    # inbox tail, no Enter yet)
    strand = send_mod._nudge_line(seat, sender, "urgent", 1,
                                  trailing=send_mod._NUDGE_INBOX_TAIL
                                  .format(seat=seat))
    pane = _FixturePane(width=200)               # wide: no wrap distracts
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")   # inbox retry, body=None
    # OWN strand with the STORED more=1 render is recognised: Enter only, no
    # second line typed, and -- the double-delivery falsifier -- the deferred
    # record is CLEARED so the body can never be typed twice.
    assert _typed_text(calls) == [" "], \
        "the own stranded deferred line is resubmitted by a typed space, never re-typed as a line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [strand + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own deferred strand is a real delivery -- the record is cleared, " \
        "so the body is never typed twice for one deferral"


def test_render_that_never_types_does_not_move_the_stored_deferred_count(
        project: Path, monkeypatch, capsys):
    """RESIDUE FALSIFIER (hypothesis:l4-deferred-ownership-uses-the-rendered-
    count): the first fix recorded the render count when the deferred line was
    RENDERED, before it was TYPED. A deferred delivery that RENDERS but never
    TYPES (the coalesce-window, a busy pane, a failed literal send) still
    OVERWROTE the stored count, so after (Z) type-and-strands at more=1 and
    (B) renders at a different count without typing, the retry (C) judges the
    Z strand against B's count, reads it as FOREIGN, keeps the deferred
    record, and the NEXT retry types the already-delivered body AGAIN.
    Fixed: the count is recorded ONLY on the path where the line is actually
    TYPED into the pane; a render that never reaches the pane stays a no-op.
    A record with no `more` key still falls back to the current count."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    # (Z) a deferred delivery types its line (with the inbox tail) at more=1
    # and strands it in the pane (Enter never lands)
    assert send_mod._store_deferred(root, seat, sender, "urgent")
    send_mod._record_deferred_render(root, seat, 1)      # Z typed at more=1
    strand = send_mod._nudge_line(
        seat, sender, "urgent", 1,
        trailing=send_mod._NUDGE_INBOX_TAIL.format(seat=seat))
    pane = _FixturePane(width=200)               # wide: a straight line
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    # the pending count has grown to 2 since Z's render
    send_mod._clear_pending(root, seat)
    send_mod._bump_pending(root, seat)
    send_mod._bump_pending(root, seat)
    assert send_mod._pending_more(root, seat) == 2

    # (B) an intervening call that RENDERS at more=2 but does NOT type: a
    # fresh nudge marker forces the coalesce-window short-circuit (the window
    # check precedes the capture/typing path). OLD bytes recorded `more=2`
    # here; NEW bytes must leave the stored `more=1` untouched.
    send_mod._record_nudge(root, seat)           # inside the window
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "more mail", "ki")    # body=None nudge
    assert _typed(calls) == [], "B must not type (coalesce-window)"
    still = send_mod._read_deferred(root, seat)
    assert still is not None and still.get("more") == 1, \
        f"a render that never types must not move the stored count: " \
        f"{still!r}"

    # (C) the retry once the window passes: the Z strand is judged against
    # the STORED more=1 render -> OURS -> Enter only, record cleared.
    send_mod._nudge_marker_path(root, seat).write_text(
        "2020-01-01T00:00:00+00:00\n")         # long-stale marker
    calls2 = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "more mail", "ki")
    assert _typed_text(calls2) == [" "], \
        "own strand resubmitted by a typed space"
    assert _enters(calls2) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls2
    assert pane.submitted == [strand + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "the own strand is a real delivery -- the record is cleared, so the " \
        "body is never typed a second time for one deferral"


def test_deferred_delivery_names_the_unread_inbox(project: Path,
                                                  monkeypatch, capsys):
    """CLAUSE (b) FALSIFIER (hypothesis:l4-send-py-same-sender-stranded-line-
    and-the-swallowed-wake): an inbox `send()` (body=None) that retries while
    a deferred dm body is stored types the DEFERRED body's line, so the inbox
    message's OWN wake token is never typed -- the recipient is never told
    there is a new unread inbox message (the wake is swallowed). Fixed: the
    deferred delivery carries a tail naming the unread inbox, so the current
    send's wake is not lost."""
    root = project / ".agi"
    assert send_mod._store_deferred(root, "adv-alive", "mee", "urgent")
    pane = _FixturePane()                                  # idle
    calls = _fake_tmux_pane(monkeypatch, ["adv-alive"], pane, [])
    send_mod.send(project, "adv-alive", "inbox body", "ki")
    typed = _typed(calls)
    assert len(typed) == 1, typed
    line = typed[0][5]
    assert "[nudge: mee]: urgent" in line, line   # the deferred dm still goes
    assert "inbox" in line, \
        f"the current inbox send's wake is swallowed: {line!r}"
    # the deferred body was consumed by the delivered line
    assert send_mod._read_deferred(root, "adv-alive") is None
    assert pane.submitted == [line], pane.submitted


def test_truncated_own_stranded_line_is_recognised_as_ours(
        project: Path, monkeypatch, capsys):
    """CLAUSE (d) FALSIFIER (hypothesis:l4-ownership-matches-the-rendered-
    line-and-zero-body-retreats): the pane holds the RENDERED inline line, so
    OLD bytes' `body_for_match in region` against the RAW body (a 400-char
    body truncated to the 95-char rendered line) never matched OUR OWN
    stranded line -- it read as foreign, the dm was deferred, and the
    stranded line was re-deferred forever. Fixed: ownership matches region
    against `text`, the EXACT line send() renders for this body (the same
    flatten + truncation), so a truncated own line is recognised and
    submitted with Enter only."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 80                       # flattened over the cap -> truncated
    line = send_mod._nudge_line(seat, sender, big)   # the rendered line
    assert len(line) <= send_mod._NUDGE_LINE_MAX and "read" in line
    pane = _FixturePane(width=200)          # wide: the <=95-char line untruncated
    pane.send_keys(["-l", "-t", "w", line])          # strand OUR OWN truncated line
    assert pane.submitted == [] and pane.input == line
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, sender, seat, big, sender)
    # recognised as ours: Enter only, no second line typed, nothing deferred
    assert _typed_text(calls) == [" "], \
        "stranded resubmit types ONE space, never a new nudge line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own line is a real delivery -- nothing deferred"
    assert send_mod._last_nudge_age(project, seat) is not None, "marker stamped"
    assert "submitted a stranded token" in capsys.readouterr().err


def test_flattened_own_stranded_line_is_recognised_as_ours(
        project: Path, monkeypatch, capsys):
    """CLAUSE (d) FALSIFIER (newline body): a body containing newlines is
    rendered FLATTENED (`first line / second line`) in the pane, and the OLD
    raw-body match never saw it (the `\n`s are gone), so the own stranded
    line was read as foreign and re-deferred forever. Fixed: region is
    matched against the rendered `text`, so a flattened own line is
    recognised and submitted with Enter only."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    body = "first line\nsecond line\nthird line"
    line = send_mod._nudge_line(seat, sender, body)
    assert "/" in line and "first line" in line
    pane = _FixturePane()                   # short flattened line: no wrap
    pane.send_keys(["-l", "-t", "w", line])
    assert pane.submitted == [] and pane.input == line
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, sender, seat, body, sender)
    assert _typed_text(calls) == [" "], \
        "stranded resubmit types ONE space, never a second line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None
    assert "submitted a stranded token" in capsys.readouterr().err


def test_zero_body_line_is_refused_not_delivered(project: Path,
                                                 monkeypatch):
    """CLAUSE (d) FALSIFIER (hypothesis:l4-ownership-matches-the-rendered-
    line-and-zero-body-retreats): OLD bytes accepted `keep >= 0`, so a
    pathological sender whose `[nudge: <from>]:` prefix alone fills the
    `_NUDGE_LINE_MAX` budget produced a ZERO-BODY line (prefix + tail, no
    body) -- a delivered line carrying no dm. Fixed: the body must keep at
    least ONE character (keep < 1 retreats), and when no tail leaves room
    `_nudge_line` returns None so the caller DEFERS instead."""
    cap = send_mod._NUDGE_LINE_MAX
    # prefix `[nudge: <from>]: ` eats the whole budget -> keep == 0 for every
    # tail incl. ""; OLD bytes emitted prefix+tail with an empty body.
    pathological = "x" * (cap - 11)         # len("[nudge: ]: ") == 11
    assert len(f"[nudge: {pathological}]: ") == cap
    assert send_mod._nudge_line("adv-alive", pathological, "hello") is None
    # one char shorter leaves room for a body char -> a real line, not None
    shorter = "x" * (cap - 12)
    line = send_mod._nudge_line("adv-alive", shorter, "hello")
    assert line is not None and len(line) <= cap
    # full path: send_dm with the pathological sender types NOTHING and
    # defers the body (a zero-body line is unreachable)
    root = project / ".agi"
    seat = "adv-alive"
    pane = _FixturePane()
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send_dm(project, pathological, seat, "hello", pathological)
    assert _typed(calls) == [], "no zero-body line may be typed"
    assert send_mod._read_deferred(root, seat) \
        == {"sender": pathological, "body": "hello"}, \
        "the unrenderable dm is deferred for a later retry, not dropped"


def test_send_skips_nudge_when_no_window(project: Path, monkeypatch):
    calls = _fake_tmux(monkeypatch, [])  # an empty/absent window listing
    send_mod.send(project, "ephemeral-kid", "fire and forget", "parent")
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    inbox = project / ".agi" / "sessions" / "inbox" / "ephemeral-kid.md"
    assert inbox.is_file()
    assert "fire and forget" in inbox.read_text()


def _seats_md(rows):
    """A config:seats node body for the PARSER `_locally_loaded_rows` uses
    (the engine's frontmatter loader); rows are YAML mappings, `window` is
    the tmux @id a seat row carries in production."""
    import json as _j
    lines = ["---", "id: config:seats", "type: config", "seats:"]
    for r in rows:
        lines.append("  - " + _j.dumps(r))
    lines.append("---")
    return "\n".join(lines) + "\n"


def test_nudge_addressed_by_row_at_id(project: Path, monkeypatch):
    """Falsifier (3): a row that carries a LIVE window @id must be addressed
    by @id, never by name — a namesake/predecessor window has a different @id.

    HERMETIC: the fixture row's pid would stat ~/.claude/sessions/<pid>.json
    on the host, an ambient home-dir read that must not decide this test
    (fixture-leak). Neutralized: registry status is forced None so the test
    deterministically falls to the capture-pane fake."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    # NB the fake lists the seat NAME (a namespace window) AND the live @id;
    # the LIVE @id must win and the name must never be addressed.
    calls = _fake_tmux(monkeypatch, ["@246", "sanctuary-director"])
    send_mod.send(project, "sanctuary-director", "secret body", "kid")
    nudges = _typed(calls)
    assert nudges, "expected a nudge to the seat's @id window"
    assert nudges[0][4] == "agi-rc:@246", nudges[0][4]
    assert "sanctuary-director" not in nudges[0][4]
    assert nudges[0][5].startswith("[agi-nudge]")
    assert "secret body" not in nudges[0][5]
    assert _enters(calls)[0][3] == "agi-rc:@246"


def test_nudge_coalesces_under_busy_pane(project: Path, monkeypatch):
    """Falsifier (2): two nudges into a busy pane must yield ZERO typed
    tokens (no body text, no concatenation) and a `nudge: coalesced` stderr
    line — a busy Claude Code pane shows `esc to interrupt`. Runs on the REAL
    busy capture fixture (clause d of hypothesis:l4-send-py-same-sender-
    stranded-line-and-the-swallowed-wake) -- the busy signal lives in the
    FOOTER below the `\u276f` box, the shape the synthetic spinner lacked."""
    busy = _fixture_text("claude_pane_busy.txt")
    calls = _fake_tmux(monkeypatch, ["director"], capture_text=busy)
    send_mod.send(project, "director", "first", "kid")
    send_mod.send(project, "director", "second", "kid")
    nudges = [c for c in calls if c[:2] == ["tmux", "send-keys"]]
    assert nudges == [], "busy pane must receive NO typed token"
    # the wake token is still built but never sent; inbox bytes stay bodies
    inbox = (project / ".agi" / "sessions" / "inbox" / "director.md")
    assert "first" in inbox.read_text() and "second" in inbox.read_text()


def test_busy_then_idle_fires_token_on_retry(project: Path, monkeypatch,
                                            capsys):
    """Falsifier (F1): busy -> idle with NO third send — the idled retry
    must still fire the wake token once the pane goes idle.

    The pane MUST change state BETWEEN the two sends, so the fake reads a
    MUTABLE capture source (a list this test rewrites), never a static
    string — a static capture cannot express the sequence.

    Old behaviour (the defect): the busy send stamped the per-seat marker
    even though nothing was typed, so the idled retry inside the
    coalescing window was suppressed by the batch cap — ZERO tokens, the
    message never woken. Fixed: the marker records only a DELIVERED token,
    so the idle retry is not suppressed and the token fires.

    HERMETIC: recipient `director` carries no pid, so registry status is
    None and the capture-pane fake decides busy vs idle deterministically.
    """
    # busy pane first, idle (empty capture) on retry
    captures = ["...⠋...\nesc to interrupt\n", ""]   # busy, then idle
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="director\n",
                                               stderr="")
        if cmd[:2] == ["tmux", "capture-pane"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout=captures.pop(0),
                                               stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    send_mod.send(project, "director", "first", "kid")    # pane busy
    send_mod.send(project, "director", "second", "kid")   # pane now idle
    nudges = _typed(calls)
    assert len(nudges) == 1, \
        f"the idled retry must fire exactly one token, saw {nudges}"
    assert nudges[0][5].startswith("[agi-nudge]")
    assert "second" not in nudges[0][5], "token, never the body"
    err = capsys.readouterr().err
    assert "nudge: coalesced" in err   # the busy send still reports


def test_batch_of_dms_yields_one_token(project: Path, monkeypatch, capsys):
    """Falsifier (2): at most ONE token per unread batch — two sends in the
    coalescing window yield a single send-keys, the second absorbed by the
    per-seat nudge marker."""
    calls = _fake_tmux(monkeypatch, ["director"])  # idle pane (empty capture)
    send_mod.send(project, "director", "first", "kid")
    send_mod.send(project, "director", "second", "kid")
    nudges = _typed(calls)
    assert len(nudges) == 1, f"expected exactly one token, saw {nudges}"
    err = capsys.readouterr().err
    assert "nudge: coalesced" in err


# ── L4.120b residues ──


def test_row_window_name_is_refused_and_falls_back_to_listing(project: Path,
                                                              monkeypatch,
                                                              capsys):
    """Residue 1a: a row whose `window` cell is a NAME (not an @id) must be
    REFUSED as a send-keys target — a name-addressed window the row was
    supposed to carry as an @id could be a predecessor/namesake — with the
    reason on stderr and a FALL BACK to the genuinely-listed window NAME.
    Old bytes used any truthy window cell verbatim and addressed the NAME."""
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "sanctuary-director"}]))   # a NAME, not @id
    calls = _fake_tmux(monkeypatch, ["sanctuary-director"])
    send_mod.send(project, "sanctuary-director", "secret body", "kid")
    nudges = _typed(calls)
    assert nudges, "the NAME fallback must still nudge the listed window"
    assert nudges[0][4] == "agi-rc:sanctuary-director", nudges[0][4]
    assert "not an @id" in capsys.readouterr().err


def test_stale_unlisted_at_id_is_not_used_verbatim(project: Path,
                                                    monkeypatch, capsys):
    """Residue 1b (inverted by clause (b) of hypothesis:l4-send-py-same-
    sender-stranded-line-and-the-swallowed-wake): a row whose `window` cell
    IS an @id that is NOT a listed window is STALE — it is never used
    verbatim (that was the swallowed-wake defect); it prints the
    `nudge repair:` line and, the by-name fallback also finding nothing,
    the ONE named 'no window named …' line -- never silence -- and nothing
    is typed."""
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@250"}]))
    calls = _fake_tmux(monkeypatch, ["director"])   # neither @250 nor name
    send_mod.send(project, "sanctuary-director", "body", "kid")
    nudges = _typed(calls)
    assert nudges == [], f"a stale @id with no name fallback must not type: {nudges}"
    err = capsys.readouterr().err
    assert "nudge repair: sanctuary-director row window @250 is gone; " \
           "falling back to name" in err, err
    assert "nudge: sanctuary-director row window @250 is gone and no " \
           "window named sanctuary-director is listed -- message written, " \
           "no wake" in err, err
    inbox = (project / ".agi" / "sessions" / "inbox" / "sanctuary-director.md")
    assert "body" in inbox.read_text(), "the message still lands in the inbox"


def test_submitted_token_echo_in_transcript_does_not_coalesce(project: Path,
                                                              monkeypatch,
                                                              capsys):
    """Residue 2a: a SUBMITTED token echoed in the transcript ABOVE the
    input box must NOT read as stranded — the input line is empty, so the
    idle nudge fires. Old bytes scanned the WHOLE capture and coalesced
    forever (false 'token already unsubmitted'); the input-region scan is
    scoped to the box."""
    tok = send_mod._build_nudge_token("director")
    capture = f"\u276f {tok}\n{tok}\n\u276f \n"   # echoed above, empty box
    calls = _fake_tmux(monkeypatch, ["director"], capture_text=capture)
    send_mod.send(project, "director", "hello", "kid")
    nudges = _typed(calls)
    assert len(nudges) == 1, nudges
    assert "nudge: coalesced" not in capsys.readouterr().err


def test_token_in_input_region_still_reads_unsubmitted():
    """Residue 2b: the SAME transcript but with the token really in the
    input box (on/below the last prompt glyph) still reads as 'token already
    unsubmitted'. Distinguishes the input-region scoping from a naive 'scan
    nothing' -- the head match returns the reason when (and only when) the
    token is in the region. (End-to-end, an in-box token takes the probe-(C)
    heal -- a bare Enter, not a coalesce -- so this is asserted at the unit
    boundary the residue actually changes.)"""
    tok = send_mod._build_nudge_token("director")
    echoed = f"\u276f {tok}\n{tok}\n\u276f \n"      # echoed above, empty
    inbox = f"\u276f {tok}\n"                         # in-box, unsubmitted
    assert send_mod._nudge_coalesce_reason(echoed, tok, None) is None
    assert send_mod._nudge_coalesce_reason(inbox, tok, None) \
        == "token already unsubmitted"


def test_old_spinner_scrolled_up_does_not_read_as_busy(project: Path,
                                                       monkeypatch, capsys):
    """Residue 2c: an OLD `esc to interrupt` scrolled UP in the transcript,
    above an idle input box, must NOT read as busy — the nudge fires. Old
    bytes scanned the whole capture and coalesced (false 'pane busy
    (spinner)'); the input-region scan is scoped to the box."""
    capture = "... older transcript ...\nesc to interrupt\n\u276f \n"
    calls = _fake_tmux(monkeypatch, ["director"], capture_text=capture)
    send_mod.send(project, "director", "hello", "kid")
    nudges = _typed(calls)
    assert len(nudges) == 1, nudges
    assert "nudge: coalesced" not in capsys.readouterr().err


def test_read_returns_block_once_and_marks_read(project: Path, capsys):
    """Red-first: send then read returns the block and peek still shows it."""
    send_mod.send(project, "kid-a", "escalation: need help", "parent")
    send_mod.send(project, "kid-a", "second message", "parent")

    # Read — should return both messages
    send_mod.read(project, "kid-a", None)
    captured1 = capsys.readouterr()
    assert "escalation: need help" in captured1.out
    assert "second message" in captured1.out

    # Read again — should be empty (already read)
    send_mod.read(project, "kid-a", None)
    captured2 = capsys.readouterr()
    assert "empty" in captured2.out

    # Peek — should also be empty (read marked them)
    send_mod.peek(project, "kid-a")
    captured3 = capsys.readouterr()
    assert "empty" in captured3.out


def test_peek_does_not_mark_read(project: Path, capsys):
    """Peek shows unread messages without marking them."""
    send_mod.send(project, "council", "meeting at noon", "director")

    send_mod.peek(project, "council")
    captured1 = capsys.readouterr()
    assert "meeting at noon" in captured1.out

    # Peek again — still shows the message (not marked read)
    send_mod.peek(project, "council")
    captured2 = capsys.readouterr()
    assert "meeting at noon" in captured2.out

    # Read — should still show it
    send_mod.read(project, "council", None)
    captured3 = capsys.readouterr()
    assert "meeting at noon" in captured3.out

    # Now it's marked read
    send_mod.peek(project, "council")
    captured4 = capsys.readouterr()
    assert "empty" in captured4.out


# ── two senders interleave ─────────────────────────────────────────────────


def test_two_senders_interleave_without_loss(project: Path, capsys):
    """Two senders writing to the same recipient interleave without loss."""
    send_mod.send(project, "prime", "msg from a00-1111", "a00-1111")
    send_mod.send(project, "prime", "msg from a00-2222", "a00-2222")
    send_mod.send(project, "prime", "msg from a00-1111 again", "a00-1111")

    send_mod.read(project, "prime", None)
    captured = capsys.readouterr()
    assert "a00-1111" in captured.out
    assert "a00-2222" in captured.out
    assert "msg from a00-1111 again" in captured.out


def test_two_recipients_independent(project: Path, capsys):
    """Messages to different recipients are isolated."""
    send_mod.send(project, "director", "to director", "kid")
    send_mod.send(project, "parent", "to parent", "kid")

    send_mod.read(project, "director", None)
    captured1 = capsys.readouterr()
    assert "to director" in captured1.out
    assert "to parent" not in captured1.out

    send_mod.read(project, "parent", None)
    captured2 = capsys.readouterr()
    assert "to parent" in captured2.out


# ── timestamp and metadata ────────────────────────────────────────────────


def test_message_has_timestamp(project: Path):
    send_mod.send(project, "agent-x", "content", "sender-y")
    content = (project / ".agi" / "sessions" / "inbox" / "agent-x.md").read_text()
    assert "ts: " in content


def test_message_has_from_to_and_text(project: Path):
    send_mod.send(project, "recip", "the message body", "sender-id")
    content = (project / ".agi" / "sessions" / "inbox" / "recip.md").read_text()
    assert "from: sender-id" in content
    assert "to: recip" in content
    assert "the message body" in content


# ── empty inbox ────────────────────────────────────────────────────────────


def test_read_empty_inbox(project: Path, capsys):
    send_mod.read(project, "nobody", None)
    captured = capsys.readouterr()
    assert "empty" in captured.out


def test_peek_empty_inbox(project: Path, capsys):
    send_mod.peek(project, "nobody")
    captured = capsys.readouterr()
    assert "empty" in captured.out


# ── read/peek wrap message bodies at 160 (hypothesis:l4-send-read-and-peek-
# ── wrap-message-bodies-at-160-columns-display-only) ────────────────────


def _long_wrap_body(n: int = 200) -> str:
    """A single-line message body far over 160 columns."""
    return " ".join(f"word{i}" for i in range(n))


def _capture_peek(project: Path, seat: str, wrap: int) -> str:
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        send_mod.peek(project, seat, wrap)
    return buf.getvalue()


def test_read_peek_wrap_bodies_at_160_display_only(project: Path):
    """The motivating defect: a long single-line dm overflows one `send.py
    read`. With the default wrap the printed output has NO line over 160 cols,
    the header `from:` line still greps, and the inbox file bytes are
    UNCHANGED by a peek (display-only). `--wrap 0` restores the raw line."""
    long = _long_wrap_body()
    assert len(long) > 160
    send_mod.send(project, "kid-w", long, "parent")
    inbox = project / ".agi" / "sessions" / "inbox" / "kid-w.md"
    before = inbox.read_bytes()

    out = _capture_peek(project, "kid-w", 160)
    for ln in out.splitlines():
        assert len(ln) <= 160, f"default read printed a {len(ln)}-col line: {ln!r}"
    assert "from: parent" in out          # header lines byte-identical + greppable

    # peek marks nothing; default wrap left the inbox bytes untouched
    assert inbox.read_bytes() == before, "a read that wraps changed the inbox file"

    # --wrap 0 = today's raw single long line
    raw = _capture_peek(project, "kid-w", 0)
    assert any(len(l) > 160 for l in raw.splitlines()), \
        "--wrap 0 must print the original un-wrapped line"
    assert "word0 word1" in raw and " word199" in raw
    assert inbox.read_bytes() == before, "peek --wrap 0 changed the inbox file"


def test_read_wrap_marks_read_exactly_as_before(project: Path, capsys):
    """A wrapped read still marks the same blocks read (the marker advances),
    and the read marker is untouched by wrapping."""
    send_mod.send(project, "kid-w", _long_wrap_body(), "parent")
    send_mod.send(project, "kid-w", "short second", "parent")
    inbox = project / ".agi" / "sessions" / "inbox" / "kid-w.md"
    before = inbox.read_bytes()

    send_mod.read(project, "kid-w", None)      # default wrap 160, marks read
    text = inbox.read_text()
    # the READ marker was inserted (the mark side-effect still happens), but
    # the message bytes themselves before the marker are untouched by wrapping
    assert "read up to here" in text
    # read again → empty (already read)
    send_mod.read(project, "kid-w", None)
    assert "empty" in capsys.readouterr().out


def test_overlong_token_stays_whole_and_newlines_kept(project: Path):
    """fold -s rules: a token longer than width stays whole on its own line;
    a body with its own line breaks keeps them."""
    token = "x" * 200
    body = f"aa {token} bb\nthen on another line"
    send_mod.send(project, "kid-w", body, "parent")
    out = _capture_peek(project, "kid-w", 60)
    assert token in out, "an over-long token must never be split mid-token"
    assert "then on another line" in out, "existing newlines must be kept"
    assert all(len(l) <= 60 or token in l for l in out.splitlines()), \
        "no line over 60 except the untouched over-long token line"


def test_deferred_dm_body_wraps_under_default(project: Path):
    """A long deferred dm body (shown at a seam via peek) wraps too, without
    wrapping its `deferred dm from X (ts)` heading."""
    send_mod.send(project, "kid-d", _long_wrap_body(), "parent")
    # manufacture a deferred record for kid-d so peek shows it at the seam
    deferred = {"sender": "parent", "body": _long_wrap_body()}
    path = send_mod._nudge_deferred_path(project, "kid-d")
    path.parent.mkdir(parents=True, exist_ok=True)
    import json as _j
    path.write_text(_j.dumps(deferred))
    out = _capture_peek(project, "kid-d", 160)
    for ln in out.splitlines():
        assert len(ln) <= 160, f"deferred seams printed a {len(ln)}-col line: {ln!r}"
    assert "deferred dm from parent" in out  # heading unwrapped


def test_room_read_wraps_body_not_transcript_header(comms: Path):
    """A room read (`--room`) wraps the message bodies and never the
    transcript's own `**sender** HH:MM — ` header prefix."""
    long = _long_wrap_body()
    send_mod.send_room(comms, "council", long, "director")
    wrapped = send_mod.peek_room(comms, "council", "kid", None, wrap=160)
    # render_transcript returns ONE element per message, which may carry its
    # own newlines — check every physical line.
    for elem in wrapped:
        for sl in elem.split("\n"):
            assert len(sl) <= 160, f"a room line exceeded 160 cols: {sl!r}"
    assert any(l.startswith("**director**") for l in wrapped[0].split("\n")), \
        "prefix lost"
    raw = send_mod.peek_room(comms, "council", "kid", None, wrap=0)
    assert any(len(sl) > 160 for elem in raw for sl in elem.split("\n")), \
        "--wrap 0 must print a raw room line"


def test_wrap_zero_and_short_messages_byte_identical(project: Path):
    """The existing short-message read/mark tests stay green by construction:
    wrapping a short body is byte-for-byte identity, and `--wrap 0` never
    touches the inbox file."""
    send_mod.send(project, "kid-w", "meeting at noon", "director")
    inbox = project / ".agi" / "sessions" / "inbox" / "kid-w.md"
    before = inbox.read_bytes()
    out_default = _capture_peek(project, "kid-w", 160)
    out_raw = _capture_peek(project, "kid-w", 0)
    assert out_default == out_raw, \
        "a short message must print identically under default wrap and raw"
    assert inbox.read_bytes() == before
    assert "meeting at noon" in out_default


# ── wrap preserves leading whitespace and blank lines exactly ──────────────
# (hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly)


def test_wrap_preserves_leading_whitespace_and_blank_lines():
    """The motivating falsifier: a body carrying indented content (a diff, a
    table, a code fence, a nested list) used to have every line's leading
    whitespace stripped, so a dm printed flattened. Blank lines (interior
    and trailing) must survive byte-for-byte too."""
    bodies = [
        "  a\n    b\n\n",          # indentation on every line + trailing blank
        "a\n b\n \n",              # interior whitespace-only line survives
        "a\n\n",                   # trailing blank line survives
        "x  y  \nz\n",             # internal runs + trailing spaces survive
        "  \tcode\n  \tfence\n",   # tabs in the indent survive
    ]
    for b in bodies:
        assert send_mod._wrap_body(b, 160) == b, \
            f"leading whitespace / blank lines corrupted: {b!r}"


def test_wrap_unwrapped_line_is_byte_identical_next_to_long_lines():
    """Wrapping touches ONLY lines longer than width. A short line holding
    internal runs of spaces or trailing spaces must print byte-identical
    even when a neighbouring line in the same body is long enough to fold."""
    body = "  keep me  same   \n" + " ".join(["word"] * 40) + "\nshort line  "
    out = send_mod._wrap_body(body, 60)
    assert out.startswith("  keep me  same   \n"), \
        "a short line must print byte-identical despite a long neighbour"
    assert out.split("\n")[-1] == "short line  "
    for ln in out.splitlines():
        assert len(ln) <= 60, f"a folded line exceeded width: {ln!r}"


def test_wrap_long_line_keeps_indent_on_every_continuation():
    """A 200-char content line indented 4 spaces must print every physical
    line prefixed by the SAME 4-space indent -- the fold never happens inside
    the indent and every continuation re-emits it."""
    body = "    " + " ".join(["w"] * 120)      # 240 cols of words under a 4-space indent
    out = send_mod._wrap_body(body, 64)
    lines = out.split("\n")
    assert len(lines) > 1, "an over-width line must wrap"
    assert lines[0].startswith("    "), "first physical line lost the indent"
    for phys in lines:
        assert phys == "    " + phys.strip(), \
            "every continuation line must carry the full 4-space indent"
        assert len(phys) <= 64, f"physical line exceeded width: {phys!r}"


def test_wrap_folds_only_at_space_outside_indent_keeps_labels_whole():
    """A folded long line breaks only at a space outside the indent, and
    never splits inside a node id, sha, path, URL or label token -- an
    over-wide token stays whole on its own line."""
    node = "hypothesis:l4-long-node-id-that-exceeds-any-width-0123456789abcdef"
    body = "  see " + node + " and " + ("y" * 30)
    out = send_mod._wrap_body(body, 40)
    assert node in out, "a long node id must never be split mid-token"
    assert "y" * 30 in out
    for phys in out.split("\n"):
        assert phys.startswith("  ") and phys == "  " + phys.lstrip(" \t"), \
            "every physical line keeps the leading indent"


def test_wrap_block_preserves_trailing_blank_lines_and_indented_body():
    """A raw block with a trailing blank body line (a body ending `\n\n`) and
    an indented body prints byte-for-byte through `_wrap_block` -- the header
    stays grep-able and the trailing blank line is not re-collapsed to one."""
    block = (
        "ts: 2026-09-11T10:00:00Z\nfrom: parent\nto: kid\n\n"
        "  diff:\n  - a\n  + b\n\n"
    )
    assert send_mod._wrap_block(block, 160) == block, \
        "an indented body with a trailing blank line must survive byte-identical"
    assert send_mod._wrap_block(block, 0) == block
    multi = "ts: x\nfrom: p\nto: k\n\na\n\n\n"
    assert send_mod._wrap_block(multi, 160) == multi, \
        "two trailing blank lines must survive byte-identical"


def test_wrap_large_width_is_byte_identity_and_property_roundtrip():
    """Property (hypothesis clause 5): for N large enough `_wrap_body(body,
    N) == body` byte-for-byte; and a per-logical-line round trip -- strip the
    indent from every physical line and join the content tokens with a single
    space -- reconstructs the original logical line."""
    import random
    random.seed(11)
    for _ in range(1500):
        body = "\n".join(
            " ".join(f"w{i}" for i in range(random.randint(0, 40)))
            for _ in range(random.randint(0, 6)))
        if random.random() < 0.4:
            body += "\n" * random.randint(1, 3)
        assert send_mod._wrap_body(body, 10**6) == body, \
            "large N must be byte-for-byte identity"
        n = random.randint(8, 60)
        for logical in body.split("\n"):
            indent = logical[:len(logical) - len(logical.lstrip(" \t"))]
            got = send_mod._wrap_logical_line(logical, n)
            want = " ".join(logical.split())
            recon = " ".join(x.strip() for p in got.split("\n")
                              for x in p[len(indent):].split())
            assert recon == want, (logical, n, got)
            for p in got.split("\n"):
                if any(len(w) > n for w in p.split()):
                    continue          # over-long token kept whole, by design
                assert len(p) <= n, (logical, n, p)


# ── non-existent inbox file ────────────────────────────────────────────────


def test_read_nonexistent_recipient(project: Path, capsys):
    send_mod.read(project, "never-written", None)
    captured = capsys.readouterr()
    assert "empty" in captured.out


def test_peek_nonexistent_recipient(project: Path, capsys):
    send_mod.peek(project, "never-written")
    captured = capsys.readouterr()
    assert "empty" in captured.out


# ── multiple reads after marker ────────────────────────────────────────────


def test_accumulated_reads_after_multiple_sends(project: Path, capsys):
    """After read, new sends appear; old ones don't reappear."""
    send_mod.send(project, "worker", "first", "boss")
    send_mod.read(project, "worker", None)
    capsys.readouterr()  # discard

    send_mod.send(project, "worker", "second", "boss")
    send_mod.read(project, "worker", None)
    captured = capsys.readouterr()
    assert "first" not in captured.out
    assert "second" in captured.out


# ── sender detection ───────────────────────────────────────────────────────


def test_sender_from_flag(monkeypatch):
    # with no AGI_AGENT_ID and no tmux, --from wins
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "agi-rc")
    assert send_mod._detect_sender("custom-role") == "custom-role"


def test_sender_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("AGI_AGENT_ID", "env-agent-007")
    assert send_mod._detect_sender(None) == "env-agent-007"


def test_sender_unknown_when_no_env_no_flag(monkeypatch):
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "")
    monkeypatch.delenv("TMUX", raising=False)
    assert send_mod._detect_sender(None) == "unknown"


def test_sender_env_beats_flag(monkeypatch):
    """AGI_AGENT_ID outranks an explicit --from (l3-send-comms-root)."""
    monkeypatch.setenv("AGI_AGENT_ID", "env-win")
    assert send_mod._detect_sender("flag-loser") == "env-win"


def test_sender_seat_used_when_no_agent_id(monkeypatch):
    """Clause (c): with AGI_SEAT set and AGI_AGENT_ID unset, a spawned /
    seat-launched path dms under its SEAT name -- never "from: unknown"
    (rotate-self / spawn / seats-launch / recovery all export AGI_SEAT)."""
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_SEAT", "sanctuary-director")
    assert send_mod._detect_sender(None) == "sanctuary-director"
    # AGI_SEAT beats an explicit --from too (env outranks the flag)
    assert send_mod._detect_sender("flag-loser") == "sanctuary-director"


def test_sender_agent_id_beats_seat(monkeypatch):
    """Clause (c): AGI_AGENT_ID still outranks AGI_SEAT when both are set
    (the agent's own identity beats its seat name)."""
    monkeypatch.setenv("AGI_AGENT_ID", "env-agent-007")
    monkeypatch.setenv("AGI_SEAT", "sanctuary-director")
    assert send_mod._detect_sender(None) == "env-agent-007"
    monkeypatch.delenv("AGI_AGENT_ID")
    assert send_mod._detect_sender(None) == "sanctuary-director"


def test_sender_window_name_is_never_an_identity(monkeypatch):
    """hypothesis:l3-agent-id-never-exported — a seat/tmux window name is
    never a sender. With no env and no --from the message is signed
    "unknown", even inside a window named after the prime (which is exactly
    what used to sign this advisor as belam-S1-L3-III).
    """
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    # a window that once impersonated the prime must now be ignored
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "belam-S1-L3-III")
    assert send_mod._detect_sender(None) == "unknown"
    # an explicit --from still provides an identity
    assert send_mod._detect_sender("explicit-flag") == "explicit-flag"

# ══════════════════════════════════════════════════════════════════════════
# Rooms (hypothesis:l3w0-send-rooms)
# dm + quorum conversations as files under comms/, transcript render,
# standing rooms, prime inbox-only with the audience verb.
# RED-FIRST: each rule below was written first and asserted to fail before the
# implementation in bin/send.py made it pass.
# ══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def comms(tmp_path: Path) -> Path:
    """A bare comms root (nothing else required — room/dm verbs don't resolve
    the project root, they take the comms root explicitly)."""
    return tmp_path / "comms"


def _conf(proj: Path, cr: str):
    import json as _j
    cfg = _j.loads((proj / ".agi" / "config.json").read_text())
    cfg.setdefault("locations", {})["comms_root"] = cr
    (proj / ".agi" / "config.json").write_text(_j.dumps(cfg))


# ── dm ────────────────────────────────────────────────────────────────────

def test_dm_creates_sorted_file(comms: Path):
    """send --to writes comms/dm/<a>--<b>.md with names sorted; a<b in name."""
    send_mod.send_dm(comms, "director", "kid-a", "hello", "kid-a")
    path = comms / "dm" / "director--kid-a.md"
    assert path.is_file()
    assert "hello" in path.read_text()


def test_dm_to_or_from_prime_refused(comms: Path):
    """A dm may never address or originate from the prime, like a room
    (hypothesis:l3w4-quorum-reviews: the prime is inbox-only)."""
    with pytest.raises(SystemExit):
        send_mod.send_dm(comms, "adv-alive", "prime", "hi", "adv-alive")
    with pytest.raises(SystemExit):
        send_mod.send_dm(comms, "prime", "adv-alive", "hi", "prime")
    with pytest.raises(SystemExit):
        send_mod.send_dm(comms, "adv-alive", "prime-fans", "hi", "adv-alive")
    assert not (comms / "dm" / "adv-alive--prime.md").exists()


def test_dm_names_are_sorted(comms: Path):
    """File name sorts the two ids, independent of call order."""
    send_mod.send_dm(comms, "zz", "aa", "hi", "aa")
    path = comms / "dm" / "aa--zz.md"
    assert path.is_file()
    assert not (comms / "dm" / "zz--aa.md").exists()


def test_dm_writes_block_with_metadata(comms: Path):
    send_mod.send_dm(comms, "me", "you", "the body", "me")
    content = (comms / "dm" / "me--you.md").read_text()
    assert "ts: " in content
    assert "from: me" in content
    assert "the body" in content


def test_dm_render_shape(comms: Path, capsys):
    """Reading renders a transcript line: **sender** HH:MM — text."""
    send_mod.send_dm(comms, "parent", "director", "meet at noon", "parent")
    lines = send_mod.read_dm(comms, "director", "parent", None, None)
    assert len(lines) == 1
    line = lines[0]
    assert line.startswith("**parent** ")
    assert " — meet at noon" in line


def test_dm_read_marks_read_once(comms: Path):
    send_mod.send_dm(comms, "a", "b", "one", "a")
    send_mod.send_dm(comms, "a", "b", "two", "a")
    first = send_mod.read_dm(comms, "b", "a", None, None)
    assert len(first) == 2
    assert "one" in first[0] and "two" in first[1]
    # second read shows nothing new
    assert send_mod.read_dm(comms, "b", "a", None, None) == []


def test_dm_peek_does_not_mark_read(comms: Path):
    send_mod.send_dm(comms, "a", "b", "hi", "a")
    peek = send_mod.peek_dm(comms, "b", "a", None)
    assert len(peek) == 1
    # still shows after read is not called; peek twice shows it twice
    peek2 = send_mod.peek_dm(comms, "b", "a", None)
    assert len(peek2) == 1
    # read still returns it
    got = send_mod.read_dm(comms, "b", "a", None, None)
    assert len(got) == 1
    # and now it is marked
    assert send_mod.peek_dm(comms, "b", "a", None) == []


def test_dm_since_filter(comms: Path):
    send_mod.send_dm(comms, "a", "b", "older", "a")
    blocks = send_mod._conv_blocks(comms / "dm" / "a--b.md")
    ts0 = blocks[0]["ts"]
    send_mod.send_dm(comms, "a", "b", "newer", "a")
    # since = first ts -> both blocks are >= it
    assert len(send_mod.read_dm(comms, "b", "a", ts0, None)) == 2
    # a future anchor -> nothing
    assert send_mod.read_dm(
        comms, "b", "a", "9999-01-01T00:00:00+00:00", None) == []


# ── room ──────────────────────────────────────────────────────────────────

def test_room_creates_file_and_appends(comms: Path):
    send_mod.send_room(comms, "tier3-quorum", "first", "parent-a")
    send_mod.send_room(comms, "tier3-quorum", "second", "parent-b")
    content = (comms / "room" / "tier3-quorum.md").read_text()
    assert "first" in content
    assert "second" in content
    assert "from: parent-a" in content
    assert "from: parent-b" in content


def test_room_render_transcript(comms: Path):
    send_mod.send_room(comms, "tier1-directors", "anyone free?", "d1")
    send_mod.send_room(comms, "tier1-directors", "yes", "d2")
    lines = send_mod.read_room(comms, "tier1-directors", "d3", None, None)
    assert len(lines) == 2
    assert lines[0].startswith("**d1** ")
    assert " — anyone free?" in lines[0]
    assert lines[1].startswith("**d2** ")
    assert " — yes" in lines[1]


def test_room_read_positions_are_per_participant(comms: Path):
    send_mod.send_room(comms, "tier3-quorum", "one", "p1")
    send_mod.send_room(comms, "tier3-quorum", "two", "p2")
    # p1 reads both
    assert len(send_mod.read_room(comms, "tier3-quorum", "p1", None, None)) == 2
    # a third arrives; p3 (fresh) and p1 differ
    send_mod.send_room(comms, "tier3-quorum", "three", "p3")
    assert len(send_mod.read_room(comms, "tier3-quorum", "p1", None, None)) == 1
    assert len(send_mod.read_room(comms, "tier3-quorum", "p2", None, None)) == 3


def test_room_cannot_address_prime(comms: Path, capsys):
    """A room may never address the prime (inbox-only)."""
    with pytest.raises(SystemExit):
        send_mod.send_room(comms, "prime", "how are you", "advisor")
    assert not (comms / "room" / "prime.md").exists()
    with pytest.raises(SystemExit):
        send_mod.send_room(comms, "prime-fans", "hi", "advisor")


def test_standing_rooms_constant():
    assert send_mod.STANDING_ROOMS == (
        "tier3-quorum", "tier2-directors", "tier2-parents",
        "tier1-directors", "tier1-parents", "tier0-parents")


# ── rooms listing ─────────────────────────────────────────────────────────

def test_rooms_lists_rooms_with_unread_counts(comms: Path):
    send_mod.send_room(comms, "tier1-directors", "hi", "d1")
    send_mod.send_room(comms, "tier1-directors", "hello", "d2")
    send_mod.send_dm(comms, "d1", "d2", "psst", "d1")
    send_mod.read_room(comms, "tier1-directors", "d1", None, None)  # d1 reads all
    rows = send_mod.rooms(comms, "d1")
    kinds = {k for k, _, _ in rows}
    by_name = {n: u for _, n, u in rows}
    assert "room" in kinds
    assert "dm" in kinds
    assert by_name.get("tier1-directors") == 0  # d1 read both
    assert by_name.get("d1--d2") == 1  # d1's own dm, never read


# ── audience (prime is inbox-only) ────────────────────────────────────────

def test_audience_writes_to_prime_inbox(project: Path, monkeypatch):
    monkeypatch.setenv("AGI_AGENT_ID", "parent-x")
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "need a ruling on g7", None, False)
    inbox = project / ".agi" / "sessions" / "inbox" / "prime.md"
    assert inbox.is_file()
    content = inbox.read_text()
    assert "to: prime" in content
    assert "need a ruling on g7" in content


def test_audience_prime_refuses_non_quorum_caller(project: Path, monkeypatch,
                                                  capsys):
    """A non-tier3-parent audience request is refused; nothing reaches the
    prime's inbox (hypothesis:l3w4-quorum-reviews: the quorum IS Belam to
    anyone else)."""
    monkeypatch.setenv("AGI_AGENT_ID", "dir-t2")
    monkeypatch.setenv("AGI_ROLE", "director")
    monkeypatch.setenv("AGI_LADDER_TIER", "2")
    monkeypatch.setenv("AGI_LOOP", "L3.29@1")
    croot = project / "comms"
    with pytest.raises(SystemExit):
        send_mod.audience_prime(croot, project, "let me in", None, False)
    assert not (project / ".agi" / "sessions" / "inbox" / "prime.md").exists()


def test_audience_prime_morals_bypasses_quorum_gate(project: Path, monkeypatch):
    """--morals opens the quorum gate: morality outranks the quorum line
    (hypothesis:l3w4-quorum-reviews)."""
    monkeypatch.setenv("AGI_AGENT_ID", "kid-x")
    monkeypatch.setenv("AGI_ROLE", "kid")
    monkeypatch.setenv("AGI_LADDER_TIER", "1")
    monkeypatch.setenv("AGI_LOOP", "L3.29@1")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "morals: life is at stake",
                            None, True)
    assert (project / ".agi" / "sessions" / "inbox" / "prime.md").is_file()


def test_audience_one_per_rotation(project: Path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_AGENT_ID", "parent-y")
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    monkeypatch.setenv("AGI_LOOP", "L3.02@1")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "first", None, False)
    with pytest.raises(SystemExit):
        send_mod.audience_prime(croot, project, "second", None, False)


def test_audience_morals_bypasses_gate(project: Path, monkeypatch):
    """--morals bypasses the one-per-rotation gate."""
    monkeypatch.setenv("AGI_AGENT_ID", "parent-z")
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    monkeypatch.setenv("AGI_LOOP", "L3.02@1")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "one", None, False)
    send_mod.audience_prime(croot, project, "two-morals", None, True)  # passes


def test_audience_rule_printed_back(project: Path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_AGENT_ID", "parent-q")
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "please", None, False)
    captured = capsys.readouterr()
    assert "inbox-only" in captured.out
    assert "one audience per sender per rotation" in captured.out


# ── quorum review (hypothesis:l3w4-quorum-reviews) ────────────────────────


def test_vote_posts_structured_line(comms: Path):
    """vote posts a single structured VOTE line into the room, carrying the
    round, target, vision, alignment, reason and morals flag."""
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "aligned",
                  "adv-alive", False, "looks right", "L3.29")
    content = (comms / "room" / "tier3-quorum.md").read_text()
    assert "VOTE" in content
    assert "target=outcome:o1" in content
    assert "vision=alive" in content
    assert "alignment=aligned" in content
    assert "reason=looks right" in content
    assert "morals=0" in content


def test_vote_round_defaults_from_loop(comms: Path, monkeypatch):
    """vote without --round takes AGI_LOOP."""
    monkeypatch.setenv("AGI_LOOP", "L3.29@s2")
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "aligned",
                  "adv-alive", False, "", "")
    assert "round=L3.29@s2" in (comms / "room" / "tier3-quorum.md").read_text()


def test_vote_rejects_bad_vision_and_alignment(comms: Path, capsys):
    with pytest.raises(SystemExit):
        send_mod.vote(comms, "tier3-quorum", "outcome:o1", "bogus", "aligned",
                      "a1", False, "", "R")
    with pytest.raises(SystemExit):
        send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "banana",
                      "a1", False, "", "R")


def test_tally_votes_requires_all_three_visions(comms: Path):
    """A tally with a missing vision is an incomplete quorum (ERR, exit 1)."""
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "aligned",
                  "a1", False, "", "R")
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "all-is-one", "adjust",
                  "a2", False, "shift it", "R")
    with pytest.raises(SystemExit):
        send_mod.tally_votes(comms, "tier3-quorum", "outcome:o1", "R")


def test_tally_votes_groups_by_vision_last_write_wins(comms: Path):
    """With all three visions present the tally returns one vote per vision;
    a vision voted twice keeps the LAST write."""
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "aligned",
                  "a1", False, "first", "R")
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "all-is-one", "adjust",
                  "a2", False, "shift", "R")
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "self-perpetuating",
                  "aligned", "a3", False, "yes", "R")
    # a1 re-votes alive -> last write wins for the alive vision
    send_mod.vote(comms, "tier3-quorum", "outcome:o1", "alive", "adjust",
                  "a1", False, "changed my mind", "R")
    tally = send_mod.tally_votes(comms, "tier3-quorum", "outcome:o1", "R")
    assert set(tally) == {"alive", "all-is-one", "self-perpetuating"}
    assert tally["alive"]["alignment"] == "adjust"  # last write wins
    assert tally["alive"]["reason"] == "changed my mind"


def test_audience_close_sets_prime_excluded(comms: Path):
    """audience close excludes the prime for a round; prime-excluded then
    exits 0 for that round and 1 for others."""
    assert send_mod.prime_excluded(comms, "R2") == 1
    send_mod.audience_close(comms, "R2", "adjust: shift the model")
    assert send_mod.prime_excluded(comms, "R2") == 0
    assert send_mod.prime_excluded(comms, "R9") == 1
    state = json.loads((comms / "audience" / "state.json").read_text())
    rec = state["prime"]["R2"]
    assert "opened" in rec and "closed" in rec
    assert rec["decision"] == "adjust: shift the model"


# ── red-first: target/text positional split is mode-aware, not nargs-based ──
# (found while building hypothesis:l3w4-quorum-request-path, introduced by
# the very next-prior send.py change in this same file's history: making
# `target` nargs='?' precede `text` nargs='*' fixes plain `send TARGET TEXT`
# but breaks `send --room/--to TEXT...` the moment TEXT is a single argv
# token -- target (nargs='?', declared first) greedily claims it and text is
# left empty. The reverse order breaks the opposite case. Neither order can
# satisfy both; splitting explicitly in code (one `send_args` bucket) can.


def test_send_room_single_token_text_is_not_swallowed_by_target(tmp_path,
                                                                  monkeypatch):
    """A --room message passed as ONE argv token (the normal shape when a
    caller passes an already-built string, not several bare words) must not
    be silently claimed by the unused inbox `target` slot."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "CR3"
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    rc = send_mod.main(["--from", "alive", "--comms-root", str(croot),
                        "send", "--room", "quorum", "one whole message"])
    assert rc == 0
    text = (croot / "room" / "quorum.md").read_text()
    assert "one whole message" in text


def test_send_inbox_target_and_text_both_still_split_correctly(tmp_path,
                                                                 monkeypatch):
    """Plain inbox `send TARGET TEXT...` (no --room/--to) still separates the
    first token as target from the rest as text -- the case the target-
    before-text reorder was originally fixing must still hold."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    rc = send_mod.main(["--from", "alive", "send", "prime", "multi", "word",
                        "message"])
    assert rc == 0
    # `root` is a G11 project (markers at `.agi/`), so the shared inbox lives
    # under `.agi/sessions/`, not the legacy `root/sessions`.
    inbox = root / ".agi" / "sessions" / "inbox" / "prime.md"
    assert inbox.is_file()
    content = inbox.read_text()
    assert "to: prime" in content
    assert "multi word message" in content


def test_cli_from_flag_before_subcommand_honored(tmp_path, monkeypatch, capsys):
    """A --from placed before the subcommand is NOT silently dropped
    (hypothesis:l3-send-comms-root defect 3)."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "CR"
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "")
    rc = send_mod.main(["--from", "bidder1", "send", "--room", "t1",
                        "--comms-root", str(croot), "hello"])
    assert rc == 0
    assert "from: bidder1" in (croot / "room" / "t1.md").read_text()


def test_cli_comms_root_before_subcommand_honored(tmp_path, monkeypatch):
    """A --comms-root placed before the subcommand is NOT silently dropped;
    previously it wrote to the live default root (defect 1/3)."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "CR2"
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "")
    rc = send_mod.main(["--comms-root", str(croot), "send", "--room", "t1",
                        "message"])
    assert rc == 0
    assert (croot / "room" / "t1.md").is_file()
    assert not (root / ".agi" / "comms").exists()  # nothing wrote to the live root


# ── red-first: read --all does not advance the cursor (defect 4) ──────────


def test_read_room_all_returns_everything_without_advancing(comms: Path):
    send_mod.send_room(comms, "t1", "one", "p1")
    send_mod.send_room(comms, "t1", "two", "p1")
    send_mod.send_room(comms, "t1", "three", "p2")
    # --all returns the whole transcript and does NOT advance the cursor
    assert len(send_mod.read_room(comms, "t1", "reader", None, None,
                                  all_=True)) == 3
    # cursor still 0 -> a normal read re-returns everything (and advances)
    assert len(send_mod.read_room(comms, "t1", "reader", None, None)) == 3
    # and now it is marked read
    assert send_mod.read_room(comms, "t1", "reader", None, None) == []


def test_read_dm_all_does_not_advance(comms: Path):
    send_mod.send_dm(comms, "a", "b", "hi", "a")
    send_mod.read_dm(comms, "b", "a", None, None)  # cursor -> end
    # --all still returns the message
    assert len(send_mod.read_dm(comms, "b", "a", None, None, all_=True)) == 1
    # and the cursor stays put
    assert send_mod.read_dm(comms, "b", "a", None, None) == []


def test_peek_all_shows_transcript(comms: Path):
    send_mod.send_room(comms, "t1", "unread", "p1")
    assert len(send_mod.peek_room(comms, "t1", "reader", None, all_=True)) == 1
    # peek never commits; a later read still sees the message
    assert len(send_mod.read_room(comms, "t1", "reader", None, None)) == 1


# ══════════════════════════════════════════════════════════════════════════
# ask / report / escalate (hypothesis:l3w4-masters-comms-and-escalation)
# ══════════════════════════════════════════════════════════════════════════


def _seats_project(tmp_path: Path, rows: list[str]) -> Path:
    """A project with `.agi/nodes/.geometry/seats.md` declaring `rows`."""
    root = tmp_path / "seatproj"
    nodes = root / ".agi" / "nodes"
    (nodes / ".geometry").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    seats_yaml = "\n".join(f"  - {row}" for row in rows)
    (nodes / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n" + seats_yaml +
        "\n---\n<!-- BODY:BEGIN -->\n")
    return root


def test_ask_writes_tagged_dm_to_registered_master(tmp_path):
    root = _seats_project(tmp_path, [
        '{"name": "sanctuary-master"}',
    ])
    comms = tmp_path / "comms"
    path = send_mod.ask(comms, root / ".agi", "kid-a", "sanctuary-master",
                        "how do I rotate?", "kid-a")
    assert path.is_file()
    text = path.read_text()
    assert "[ask] how do I rotate?" in text


def test_ask_refuses_non_master_suffix(tmp_path):
    root = _seats_project(tmp_path, ['{"name": "sanctuary-master"}'])
    comms = tmp_path / "comms"
    with pytest.raises(SystemExit):
        send_mod.ask(comms, root / ".agi", "kid-a", "liaison", "hi", "kid-a")


def test_ask_refuses_unregistered_master_name(tmp_path):
    """A present registry that doesn't list the name fails closed."""
    root = _seats_project(tmp_path, ['{"name": "sanctuary-master"}'])
    comms = tmp_path / "comms"
    with pytest.raises(SystemExit):
        send_mod.ask(comms, root / ".agi", "kid-a", "ghost-master", "hi",
                    "kid-a")


def test_ask_fails_open_to_suffix_when_registry_absent(tmp_path):
    """No seats.md at all -> suffix-only check, per read_seat_registry's own
    fail-open contract."""
    root = tmp_path / "noseats"
    (root / ".agi" / "nodes").mkdir(parents=True)
    comms = tmp_path / "comms"
    path = send_mod.ask(comms, root / ".agi", "kid-a", "some-master", "hi",
                        "kid-a")
    assert path.is_file()


def test_report_refuses_without_matching_ask_from_named_asker(comms: Path):
    """Red-first: no prior [ask] from the named asker at that ts refuses and
    writes nothing; the identical call succeeds once a genuine [ask] from
    that asker sits at that exact ts."""
    with pytest.raises(SystemExit):
        send_mod.report(comms, "sanctuary-master", "kid-a", "2026-01-01T00:00:00Z",
                        "reply text", "sanctuary-master")
    assert not (comms / "dm" / "kid-a--sanctuary-master.md").exists()

    ask_path = send_mod.send_dm(comms, "kid-a", "sanctuary-master",
                                "[ask] how do I rotate?", "kid-a")
    blocks = send_mod._conv_blocks(ask_path)
    real_ts = blocks[0]["ts"]

    # wrong ts still refuses
    with pytest.raises(SystemExit):
        send_mod.report(comms, "sanctuary-master", "kid-a", "1999-01-01T00:00:00Z",
                        "reply text", "sanctuary-master")
    # wrong from (asker) at the right ts still refuses
    with pytest.raises(SystemExit):
        send_mod.report(comms, "sanctuary-master", "kid-b", real_ts,
                        "reply text", "sanctuary-master")

    # right ts and right asker succeeds
    reply_path = send_mod.report(comms, "sanctuary-master", "kid-a", real_ts,
                                 "here is how", "sanctuary-master")
    assert "[report ref=" in reply_path.read_text()


# ══════════════════════════════════════════════════════════════════════════
# audience quorum / report --room (hypothesis:l3w4-quorum-request-path)
# ══════════════════════════════════════════════════════════════════════════


def test_audience_quorum_writes_tagged_ask_to_request_room(comms: Path):
    """Any caller (no quorum gate on the ASK side) can request a quorum
    ruling; it lands in the dedicated request room, not the quorum's own
    private room."""
    path = send_mod.audience_quorum(comms, "how should the split work?",
                                    "master-sensei")
    assert path == comms / "room" / "quorum-requests.md"
    text = path.read_text()
    assert "[ask] how should the split work?" in text
    assert "from: master-sensei" in text


def test_report_room_refuses_without_matching_ask(comms: Path, monkeypatch):
    """Red-first: no [ask] at that ts in the room refuses and writes
    nothing; a genuine [ask] at that exact ts then succeeds."""
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    with pytest.raises(SystemExit):
        send_mod.report(comms, "alive", None, "2026-01-01T00:00:00Z",
                        "reply", "alive", room="quorum-requests")
    assert not (comms / "room" / "quorum-requests.md").exists()

    ask_path = send_mod.audience_quorum(comms, "need a ruling",
                                        "master-sensei")
    real_ts = send_mod._conv_blocks(ask_path)[0]["ts"]

    with pytest.raises(SystemExit):
        send_mod.report(comms, "alive", None, "1999-01-01T00:00:00Z",
                        "reply", "alive", room="quorum-requests")

    reply_path = send_mod.report(comms, "alive", None, real_ts,
                                 "ruling: split by affinity", "alive",
                                 room="quorum-requests")
    assert reply_path == ask_path  # same file, one thread
    text = reply_path.read_text()
    assert f"[report ref={real_ts}]" in text
    assert "ruling: split by affinity" in text


def test_report_quorum_requests_room_refuses_non_quorum_caller(
        comms: Path, monkeypatch):
    """A matching [ask] exists, but the replier is not a tier-3 parent --
    refused, even though the thread itself is genuine (mirrors
    test_audience_prime_refuses_non_quorum_caller for the answer side)."""
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_LADDER_TIER", raising=False)
    ask_path = send_mod.audience_quorum(comms, "need a ruling", "advisor-x")
    real_ts = send_mod._conv_blocks(ask_path)[0]["ts"]
    with pytest.raises(SystemExit):
        send_mod.report(comms, "impostor", None, real_ts, "fake ruling",
                        "impostor", room="quorum-requests")
    assert "fake ruling" not in ask_path.read_text()


def test_report_ordinary_room_has_no_quorum_gate(comms: Path, monkeypatch):
    """The quorum-only gate is scoped to QUORUM_REQUEST_ROOM specifically --
    an ordinary room's [ask]/report thread stays open to anyone, unchanged
    behavior for the general room-report path."""
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_LADDER_TIER", raising=False)
    ask_path = send_mod.send_room(comms, "tier1-directors", "[ask] status?",
                                  "d1")
    real_ts = send_mod._conv_blocks(ask_path)[0]["ts"]
    reply_path = send_mod.report(comms, "d2", None, real_ts, "on track",
                                 "d2", room="tier1-directors")
    assert "[report ref=" in reply_path.read_text()


def test_cli_audience_quorum_end_to_end(tmp_path, monkeypatch):
    """CLI-level: `send.py audience quorum --reason ...` reaches the request
    room through argument parsing, not just the direct function call."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "CR"
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    rc = send_mod.main(["--from", "master-sensei", "--comms-root", str(croot),
                        "audience", "quorum", "--reason", "split shape?"])
    assert rc == 0
    assert "[ask] split shape?" in (
        croot / "room" / "quorum-requests.md").read_text()


def test_cli_report_requires_exactly_one_of_to_or_room(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    # neither --to nor --room
    rc = send_mod.main(["--from", "alive", "report", "--ref", "x", "hi"])
    assert rc == 1
    # both --to and --room
    rc = send_mod.main(["--from", "alive", "report", "--to", "a", "--room",
                        "b", "--ref", "x", "hi"])
    assert rc == 1


def test_escalate_no_to_posts_concern_to_tier3_quorum(comms: Path):
    path = send_mod.escalate(comms, "context budget", None, "vision", "dir-g1")
    assert path == comms / "room" / "tier3-quorum.md"
    assert "[concern:vision]" in path.read_text()


def test_escalate_to_owner_refuses_without_quorum_env(comms: Path, monkeypatch):
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_LADDER_TIER", raising=False)
    with pytest.raises(SystemExit):
        send_mod.escalate(comms, "need owner call", "owner", "vision", "dir-g1")
    assert not (comms / "dm" / "dir-g1--liaison.md").exists()


def test_escalate_to_owner_dms_liaison_never_prime(comms: Path, monkeypatch):
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_LADDER_TIER", "3")
    monkeypatch.setenv("AGI_AGENT_ID", "dir-g1")
    path = send_mod.escalate(comms, "need owner call", "owner", "vision", None)
    assert path == comms / "dm" / "dir-g1--liaison.md"
    assert "[owner-decision] need owner call" in path.read_text()


def test_cli_read_all_flag(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "CR3"
    send_mod.send_room(croot, "t1", "hello", "p1")
    send_mod.send_room(croot, "t1", "world", "p2")
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_TMUX_WINDOW_NAME", "")
    rc = send_mod.main(["read", "--room", "t1", "--me", "reader",
                        "--comms-root", str(croot), "--all"])
    assert rc == 0
    assert len(send_mod._conv_blocks(croot / "room" / "t1.md")) == 2
    # cursor untouched -> a normal read still returns both
    assert len(send_mod.read_room(croot, "t1", "reader", None, None)) == 2


# ── comms root resolution ─────────────────────────────────────────────────

def test_comms_root_defaults_to_season_root(tmp_path: Path):
    """Default root is <graph_root>/comms/season-<N>, never the newest
    iteration (hypothesis:l3-send-comms-root). Season from the ladder."""
    root = tmp_path / "proj"
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 7\n---\n")
    (root / "sessions" / "inbox").mkdir(parents=True)
    assert str(send_mod.comms_root(root)) == str(
        root / ".agi" / "comms" / "season-7")


def test_comms_root_default_ignores_newest_iteration(tmp_path: Path):
    """A per-iteration dir must NOT win: the room must not reset each loop."""
    root = tmp_path / "proj"
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\n---\n")
    (root / "sessions" / "inbox").mkdir(parents=True)
    # an iteration dir exists but must not be the comms root
    (root / "sessions" / "iter-1088" / "comms").mkdir(parents=True)
    assert str(send_mod.comms_root(root)) == str(
        root / ".agi" / "comms" / "season-2")


def test_comms_root_honours_config(tmp_path: Path):
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage",
         "locations": {"comms_root": "/dev/shm/agi"}}))
    assert str(send_mod.comms_root(root)) == "/dev/shm/agi"


def test_comms_root_flag_wins(tmp_path: Path):
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"locations": {"comms_root": "/dev/shm/agi"}}))
    assert str(send_mod.comms_root(root, "/tmp/myc")) == "/tmp/myc"


# ---------------------------------------------------------------------------
# hypothesis:l3w4-parent-branch-merge-up — comms root stays the main checkout
# ---------------------------------------------------------------------------


def test_comms_root_resolves_to_main_from_a_linked_worktree(tmp_path: Path):
    """A `--branch` kid runs in its own git worktree carrying its own `.agi/`;
    the comms root must still be the MAIN checkout's `.agi/comms/season-N/`
    — one room per season, never one per worktree."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (repo / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 5\n---\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)

    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-abc@s2", str(wt), "season/s1"],
                   check=True, capture_output=True)

    main_comms = send_mod.comms_root(repo / ".agi")
    # The kid runs inside the worktree (its graph root is the worktree's .agi).
    wt_comms = send_mod.comms_root(wt / ".agi")
    assert str(main_comms) == str(repo / ".agi" / "comms" / "season-5")
    assert wt_comms == main_comms, (
        "a worktree kid must comms to the MAIN checkout's season room, "
        "not a per-worktree one")


def test_inbox_dir_resolves_to_main_from_a_linked_worktree(tmp_path: Path):
    """The MAIL inbox is ONE room across every git worktree, exactly like the
    comms root: a recipient who reads from the main checkout must see the mail
    a seat in a worktree sent, or the writer's message lands in a file the
    recipient never reads (falsifier g4's inbox face)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-abc@s2", str(wt), "season/s1"],
                   check=True, capture_output=True)
    main_inbox = send_mod._inbox_dir(repo / ".agi")
    wt_inbox = send_mod._inbox_dir(wt / ".agi")
    assert str(main_inbox) == str(repo / ".agi" / "sessions" / "inbox")
    assert wt_inbox == main_inbox, (
        "a worktree kid's mail must land in the MAIN checkout's inbox, "
        "not a per-worktree one the recipient never reads")


# ── hypothesis:l4-authority-verified-against-the-graph-not-the-message ────
# whois resolves a claimed session_ref against the PUSHED config:seats, never
# the working tree; provenance (ref + commit sha) rides in every verified
# answer; an unreachable pushed ref is UNVERIFIED and exits non-zero.
# ---------------------------------------------------------------------------

FAKE_SHA = "deadbeef0123456789"
FAKE_ROWS = [
    {"name": "belam", "role": "prime_director", "tier": 3,
     "session_ref": "7902ac"},
    {"name": "sanctuary-director", "role": "director", "tier": 1,
     "session_ref": "6f9bb5"},
    {"name": "sanctuary-helper", "role": "director", "tier": 1,
     "session_ref": "dc94bb"},
]


def _stub_pushed(monkeypatch, result):
    """Point _pushed_seats at a canned (rows, sha) or None (unreachable), so
    the whois path runs with no real git and no real tmux."""
    monkeypatch.setattr(send_mod, "_pushed_seats",
                        lambda root, ref, do_fetch: result)


def test_whois_claim_yes_has_provenance(monkeypatch):
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc, text = send_mod.whois(Path("."), "7902ac", claim="prime_director")
    assert rc == 0
    assert "IS-AUTHORIZED" in text
    assert "prime_director" in text
    # provenance in the answer: the ref it read and the commit sha it used
    assert "origin/season/s2" in text
    assert FAKE_SHA in text


def test_whois_claim_yes_by_seat_name(monkeypatch):
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc, text = send_mod.whois(Path("."), "dc94bb", claim="sanctuary-helper")
    assert rc == 0
    assert "IS-AUTHORIZED" in text
    assert "sanctuary-helper" in text


def test_whois_claim_different_row_is_no(monkeypatch):
    """Impersonation: the ref is present in the table but under a DIFFERENT
    seat/role than the claim. A presence-only check would pass this; whois must
    answer NO."""
    # EDITED by sanctuary-director gen V: this asserted `rc == 0` on a
    # REFUSAL, which encoded the defect rather than a correct declaration --
    # `whois <ref> --claim <role> && trust_them` would have proceeded on an
    # impersonator. Every original text assertion is kept; the exit code the
    # old version obscured is now asserted too.
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc, text = send_mod.whois(Path("."), "dc94bb", claim="belam")
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED
    assert "IS-NOT-AUTHORIZED" in text
    assert "sanctuary-helper" in text
    # belam is prime_director, not director — the claim mismatches the row role
    rc, text = send_mod.whois(Path("."), "7902ac", claim="director")
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED
    assert "IS-NOT-AUTHORIZED" in text


def test_whois_unknown_ref_is_no_not_error(monkeypatch):
    # EDITED by sanctuary-director gen V, same reason as the test above: a
    # NO-MATCH is a negative answer and must not exit 0. It also gets its OWN
    # code, distinct from NOT-AUTHORIZED, so a caller can tell "not in the
    # table at all" from "real, but not who they claim".
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc, text = send_mod.whois(Path("."), "cafebabe", claim=None)
    assert rc == send_mod.WHOIS_NO_MATCH
    assert "NO-MATCH" in text
    assert "cafebabe" in text
    rc, text = send_mod.whois(Path("."), "cafebabe", claim="belam")
    assert rc == send_mod.WHOIS_NO_MATCH
    assert "NO-MATCH" in text
    assert send_mod.WHOIS_NO_MATCH != send_mod.WHOIS_NOT_AUTHORIZED


def test_whois_unreachable_is_unverified_nonzero(tmp_path, monkeypatch):
    """Pushed ref unreachable → UNVERIFIED label AND a non-zero exit. Assert
    on the exit code, not only on the text."""
    _stub_pushed(monkeypatch, None)
    seats_dir = tmp_path / "nodes" / ".geometry"
    seats_dir.mkdir(parents=True)
    (seats_dir / "seats.md").write_text(
        "---\nseats:\n  - {\"name\": \"belam\", \"role\": \"prime_director\", "
    "\"session_ref\": \"7902ac\"}\n---\n")
    rc, text = send_mod.whois(tmp_path, "7902ac", claim="belam")
    assert rc == 1
    assert text.startswith("UNVERIFIED")
    assert "reading working tree" in text
    # the fallback still resolves the working-tree row, but it is labelled
    # non-authoritative and exits non-zero — never a silent success
    assert "belam" in text


def test_whois_ignores_working_tree_edit(monkeypatch, tmp_path):
    """The pushed ref is the authority: editing the working-tree file must not
    change a verified answer — the whole point of reading the pushed ref."""
    seats_dir = tmp_path / "nodes" / ".geometry"
    seats_dir.mkdir(parents=True)
    # working tree hands 7902ac to a DIFFERENT seat than the pushed ref does
    (seats_dir / "seats.md").write_text(
        "---\nseats:\n  - {\"name\": \"evil\", \"role\": \"hacker\", "
    "\"session_ref\": \"7902ac\"}\n---\n")
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc, text = send_mod.whois(tmp_path, "7902ac", claim="belam")
    assert rc == 0
    assert "IS-AUTHORIZED" in text
    assert "belam" in text
    assert "IS-NOT-AUTHORIZED" not in text


def test_whois_reuses_shared_loader_not_new_parse():
    """No sixth seats.md parser: seats are parsed ONLY through the engine's
  shared node-loader (graph_core frontmatter, the path hierarchy.load_seats
  takes), pointed at the pushed content — never a hand-rolled row regex."""
    src = Path(send_mod.__file__).read_text()
    assert "_fm.load_node_file" in src
    assert "_load_seats_rows" in src
    assert "re.split" not in src  # no regex row-parsing snuck in


def test_whois_cli_wiring_and_exit_code(monkeypatch, capsys):
    """`send.py whois <ref> --claim X` routes through main and returns the
    verified exit code (0), and an unreachable pushed ref returns 1 via the
    CLI, not only via the module function."""
    _stub_pushed(monkeypatch, (FAKE_ROWS, FAKE_SHA))
    rc = send_mod.main(["whois", "--no-fetch", "6f9bb5",
                        "--claim", "sanctuary-director"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "IS-AUTHORIZED" in out
    capsys.readouterr()
    _stub_pushed(monkeypatch, None)
    rc = send_mod.main(["whois", "--no-fetch", "6f9bb5", "--claim", "belam"])
    assert rc == 1
    assert "UNVERIFIED" in capsys.readouterr().out


# --------------------------------------------------------------------------
# whois exit codes — added by sanctuary-director gen V in review of L4.96.
#
# The round satisfied the falsifier I wrote, which specified a non-zero exit
# for the UNVERIFIED path ONLY. That was a gap in MY spec: a NEGATIVE answer
# still exited 0, so `send.py whois <ref> --claim <role> && trust_them` would
# have proceeded on an impersonator. A refusal that returns success is the
# failure this repo paid for three times in one day.
# --------------------------------------------------------------------------


def _seats_doc(rows):
    import json as _j
    body = "\n".join(f"  - {_j.dumps(r)}" for r in rows)
    return f"---\nid: config:seats\ntype: config\nseats:\n{body}\n---\n\nbody\n"


def _whois_rows():
    return [{"name": "belam", "role": "prime_director", "session_ref": "7902ac"},
            {"name": "sanctuary-helper", "role": "director",
             "session_ref": "9d073a"}]


def test_whois_exit_codes_distinguish_every_negative_answer(monkeypatch,
                                                            tmp_path):
    """0 only when authoritative AND affirmative; 2 not-authorized;
    3 no-match; 1 unverified. Distinct so a caller can tell 'not who they
    claim' from 'not in the table' from 'I could not reach the authority'."""
    import send as _send
    rows = _whois_rows()
    monkeypatch.setattr(_send, "_pushed_seats",
                        lambda root, ref, fetch: (rows, "cafe123"))

    assert _send.whois(tmp_path, "7902ac", None)[0] == _send.WHOIS_OK
    assert _send.whois(tmp_path, "9d073a", "sanctuary-helper")[0] == \
        _send.WHOIS_OK
    # the impersonation case: a REAL ref under the WRONG role
    code, text = _send.whois(tmp_path, "9d073a", "belam")
    assert code == _send.WHOIS_NOT_AUTHORIZED, text
    assert "IS-NOT-AUTHORIZED" in text
    # a ref in no row at all is a DIFFERENT answer from the above
    assert _send.whois(tmp_path, "deadbe", None)[0] == _send.WHOIS_NO_MATCH
    assert _send.WHOIS_NOT_AUTHORIZED != _send.WHOIS_NO_MATCH


def test_whois_unverified_outranks_a_working_tree_answer(monkeypatch,
                                                         tmp_path):
    """When the pushed authority is unreachable the exit is UNVERIFIED even if
    the working tree would have answered affirmatively. The caller must not
    act on an answer we could not authenticate -- and a working-tree file is
    exactly what an impersonator would edit."""
    import send as _send
    monkeypatch.setattr(_send, "_pushed_seats", lambda root, ref, fetch: None)
    monkeypatch.setattr(_send, "_locally_loaded_rows",
                        lambda root: _whois_rows())
    code, text = _send.whois(tmp_path, "7902ac", "belam")
    assert code == _send.WHOIS_UNVERIFIED, text
    assert "NOT authoritative" in text


# ── hypothesis:l4-a-truncated-deferred-body-delivers-once ──────────────────
#   a truncated deferred body reaches the pane EXACTLY ONCE: the stranded-line
#   ownership match tries the TAILED rendering of the deferred body at the
#   recorded count too (the old undo matched only the untailed render, which
#   for a truncated body is a DIFFERENT slice -- the tail is counted inside
#   _NUDGE_LINE_MAX, so the tailed render is SHORTER), and a record without a
#   recorded count is matched against every plausible render the strand could
#   have carried (each count 0..pending, tailed and untailed).

def test_truncated_tailed_deferred_strand_is_ours(project: Path, monkeypatch,
                                                  capsys):
    """(a) FALSIFIER: a deferred body long enough to truncate, stranded as the
    TAILED render an earlier deferred DELIVERY retry typed (count tail + inbox
    tail) before its Enter landed. Old bytes judged ownership against the
    UNTAILED render at the recorded count; for a truncated body that slice is
    LONGER than the tailed one (the tail is counted inside `_NUDGE_LINE_MAX`),
    so `own_line in region` missed OUR OWN strand, judged it FOREIGN, and the
    next retry typed the body AGAIN -- delivered twice. Fixed: the match also
    tries the TAILED rendering of the deferred body, so the own strand is
    recognised (Enter only) and the record cleared -- one delivery."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 80                          # flattened over the cap
    assert send_mod._store_deferred(root, seat, sender, big)
    send_mod._record_deferred_render(root, seat, 1)    # typed at more=1
    strand = send_mod._nudge_line(seat, sender, big, 1,
                                  trailing=send_mod._NUDGE_INBOX_TAIL
                                  .format(seat=seat))
    assert len(strand) <= send_mod._NUDGE_LINE_MAX
    # the FALSIFIER: the untailed render is a DIFFERENT (longer) slice, so the
    # old single untailed `own_line` is not a substring of the own tailed strand
    assert send_mod._nudge_line(seat, sender, big, 1) not in strand, \
        "the tailed strand must diverge from the untailed render (the tail is" \
        " counted inside the cap)"
    pane = _FixturePane(width=200)              # wide: no wrap distracts
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")
    assert _typed_text(calls) == [" "], \
        "the own TAILED truncated strand is resubmitted by a typed space"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "an own strand is a real delivery -- the record is cleared, so the " \
        "truncated body is never typed a second time"


def test_truncated_untailed_deferred_strand_is_ours(project: Path,
                                                    monkeypatch, capsys):
    """(b) CLAIM control: the UNTAILED truncated rendering of the deferred body
    (a strand left by the body's earlier deferred-under-busy attempt, before
    any inbox retry attached the tail) is also recognised as ours. Guards the
    tail fix from making the match TAIL-only -- the no-tail render at the
    recorded count must keep matching its own strand."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 80
    assert send_mod._store_deferred(root, seat, sender, big)
    send_mod._record_deferred_render(root, seat, 1)
    strand = send_mod._nudge_line(seat, sender, big, 1)   # NO inbox tail
    assert len(strand) <= send_mod._NUDGE_LINE_MAX
    pane = _FixturePane(width=200)
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")
    assert _typed_text(calls) == [" "], \
        "the own UNTAILED truncated strand is resubmitted by a typed space"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "the own strand is a real delivery -- cleared"


def test_truncated_different_same_sender_deferred_strand_is_foreign(
        project: Path, monkeypatch, capsys):
    """(c) FALSIFIER control (hypothesis:l4-send-py-same-sender-stranded-line-
    and-the-swallowed-wake, clause (a)): a stranded line holding a DIFFERENT
    body of a DIFFERENT length from the SAME sender must read as FOREIGN even
    when truncated -- the match is never widened to head-only. The foreign
    strand alone is submitted and the deferred body SURVIVES for a later
    retry (never typed twice, never dropped).
    (a)."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 80                                  # the deferred body
    other = "marker " * 80                              # different body, same sender
    assert send_mod._store_deferred(root, seat, sender, big)
    send_mod._record_deferred_render(root, seat, 1)
    strand = send_mod._nudge_line(seat, sender, other, 1,
                                  trailing=send_mod._NUDGE_INBOX_TAIL
                                  .format(seat=seat))
    pane = _FixturePane(width=200)
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")
    assert _typed_text(calls) == [" "], \
        "a FOREIGN truncated strand is submitted by a typed space, never a new line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand + " "], pane.submitted
    assert (lambda d: d is not None and d.get("sender") == "mee"
            and d.get("body") == big)(send_mod._read_deferred(root, seat)), \
        "a different same-sender body is NOT ours -- the deferred body kept"


def test_deferred_strand_without_recorded_count_matched_at_its_own_render(
        project: Path, monkeypatch, capsys):
    """(d) SECOND-HALF FALSIFIER: a deferred record with NO `more` key (stored
    by `_store_deferred` and never rendered, or written before L4.222) whose
    stranded line was typed at more=2 while pending is NOW 3. Old bytes
    judged it against the CURRENT pending (the `.get("more", more)` default),
    so the own strand -- truncated under the more=2 tail -- read as foreign
    and the body was typed again. Fixed: a record without a count is matched
    against every render the strand could have carried (each count 0..pending,
    tailed and untailed), so the more=2 strand is recognised (Enter only) and
    the record cleared -- one delivery."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 80
    # a LEGACY record with no `more` key (write the JSON directly: this is
    # the state a pre-L4.222 record or a stored-but-never-rendered record has)
    _nudge_deferred = send_mod._nudge_deferred_path(root, seat)
    _nudge_deferred.parent.mkdir(parents=True, exist_ok=True)
    _nudge_deferred.write_text(json.dumps({"sender": sender, "body": big}))
    assert send_mod._read_deferred(root, seat).get("more") is None
    # the strand the PRIOR delivery typed (more=2): the own body truncated
    strand = send_mod._nudge_line(seat, sender, big, 2,
                                  trailing=send_mod._NUDGE_INBOX_TAIL
                                  .format(seat=seat))
    # pending has since grown to 3 (one more dm coalesced)
    send_mod._clear_pending(root, seat)
    send_mod._bump_pending(root, seat)
    send_mod._bump_pending(root, seat)
    send_mod._bump_pending(root, seat)
    assert send_mod._pending_more(root, seat) == 3
    pane = _FixturePane(width=200)
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    calls = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")
    assert _typed_text(calls) == [" "], \
        "own more=2 stratum resubmitted by a typed space"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand + " "], pane.submitted
    assert send_mod._read_deferred(root, seat) is None, \
        "the own strand is a real delivery -- cleared, never typed twice"


def test_truncated_deferred_body_typed_once_across_busy_strand_retry(
        project: Path, monkeypatch, capsys):
    """(e) END-TO-END FALSIFIER: a 300-char deferred body across the full
    saga -- busy (deferred, nothing typed) -> a delivery retry that strands
    the TAILED truncated line -> a later inbox retry -- reaches the pane
    EXACTLY ONCE. Old bytes judged the stranded TAILED line foreign and the
    retry TYPED the body AGAIN (two `[nudge:` typed lines for one deferral).
    Fixed: the own strand is recognised, Entered alone, and never re-typed
    -- one body, one typed line, one delivery."""
    root = project / ".agi"
    seat, sender = "adv-alive", "mee"
    big = "word " * 60                              # 300 chars flattened
    # (1) BUSY: the dm coalesces, the body is deferred, nothing typed
    busy = _fixture_text("claude_pane_busy.txt")
    calls = _fake_tmux(monkeypatch, [seat], capture_text=busy)
    send_mod.send_dm(project, sender, seat, big, sender)
    assert _typed(calls) == [], "the busy send must type nothing"
    assert send_mod._read_deferred(root, seat) is not None, "deferred"
    # (2) STRANDED: a delivery retry typed the TAILED truncated line and its
    # Enter never landed (the line sits unsubmitted in the box)
    strand = send_mod._nudge_line(seat, sender, big, 0,
                                  trailing=send_mod._NUDGE_INBOX_TAIL
                                  .format(seat=seat))
    pane = _FixturePane(width=200)                  # wide: strand untruncated
    pane.send_keys(["-l", "-t", "w", strand])
    assert pane.submitted == [] and pane.input == strand
    # (3) RETRY: body=None inbox send recognises the own strand (a record with
    # no recorded count is matched across every plausible render count)
    calls2 = _fake_tmux_pane(monkeypatch, [seat], pane, [])
    send_mod.send(project, seat, "inbox body", "ki")
    assert _typed_text(calls2) == [" "], \
        "retry resubmits the already-delivered strand by a typed space"
    assert _enters(calls2) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls2
    assert pane.submitted == [strand + " "], pane.submitted
    # ONE delivery total: the single `[nudge:`-shaped line ever put in the box
    assert send_mod._read_deferred(root, seat) is None, \
        "the body was delivered -- the record is cleared, never typed twice"


# ── hypothesis:l4-a-seat-signs-with-a-swappable-scheme (clauses 2 & 3) ──
# seat keys under sessions/seats + signed inbox messages. send.py exercises
# ONLY seatsig.get() and the Scheme methods through the module IT imports
# (send_mod.seatsig), never the concrete ed25519 module directly. Rows are
# stubbed through _pushed_seats (the same resolver whois uses), so no test
# hits git or tmux.

import os as _os
import hashlib as _hl
import stat as _stat


class _DummyScheme:
    """A toy scheme in send.py's OWN seatsig table, to prove the only
    coupling is the interface: anything with keygen/sign/verify/
    public_from_secret plugs in with no change to send.py."""
    name = "dummy"

    def keygen(self):
        priv = _os.urandom(16)
        return priv, b"DUMMY" + priv

    def public_from_secret(self, priv):
        return b"DUMMY" + priv

    def sign(self, priv, msg):
        return _hl.sha256(bytes(priv) + msg).digest()

    def verify(self, pub, msg, sig):
        return sig == _hl.sha256(bytes(pub[5:]) + msg).digest()


def _stub_seat_rows(monkeypatch, rows):
    """Point _pushed_seats (whois's resolver) at canned rows, no git."""
    monkeypatch.setattr(send_mod, "_pushed_seats",
                        lambda root, ref, do_fetch: (rows, "deadbeef"))


def _seat_key_file(project, seat):
    return send_mod._seat_key_path(project, seat)


# --- clause (2): seat keys -------------------------------------------------


def test_keygen_writes_0600_seat_key_and_prints_cells(project, capsys):
    path = send_mod.keygen(project, "probe-a")
    assert path == _seat_key_file(project, "probe-a")
    assert path.is_file()
    mode = _stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o600, mode
    obj = json.loads(path.read_text())
    assert obj["scheme"] == "ed25519"
    assert len(bytes.fromhex(obj["priv_hex"])) == 32
    out = capsys.readouterr().out
    assert "pubkey: " in out
    assert "sig_scheme: ed25519" in out
    # the PRIVATE seed is never printed
    assert obj["priv_hex"] not in out


def test_keygen_unknown_scheme_is_a_keyerror(project):
    import pytest as _pt
    with _pt.raises(KeyError):
        send_mod.keygen(project, "probe-b", "not-a-scheme")


# --- clause (3): signed inbox messages -------------------------------------


def test_unsigned_send_is_byte_identical_to_today(project):
    send_mod.send(project, "recv", "hello", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    content = inbox.read_text()
    assert "sig:" not in content
    assert content.endswith("hello\n")
    # the plain header shape is exactly today's
    assert "to: recv\n\nhello\n" in content


def test_signed_send_and_read_prints_verified(project, capsys, monkeypatch):
    send_mod.keygen(project, "seat-a")
    pub = json.loads(_seat_key_file(project, "seat-a").read_text())
    pub_hex = None
    # recover the public key from the printed cells by re-reading via
    # _sign_line's own public_from_secret path: derive from the stored seed
    scheme = send_mod.seatsig.get("ed25519")
    priv = bytes.fromhex(pub["priv_hex"])
    pub_hex = scheme.public_from_secret(priv).hex()
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "hello world", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    content = inbox.read_text()
    assert "sig: ed25519:" in content
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED seat-a (ed25519)" in out
    assert "hello world" in out, "the label is never a drop"


def test_signed_bytes_are_exactly_ts_from_to_blank_text(project):
    send_mod.keygen(project, "seat-a")
    send_mod.send(project, "recv", "hello", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    block_text = inbox.read_text().split(send_mod.MSG_SEP)[1]
    meta, text = send_mod._parse_block(block_text)
    sig = meta["sig"].split(":", 2)[2]
    canonical = send_mod._canonical_msg(
        meta["ts"], meta["from"], meta["to"], text)
    # the canonical bytes assert EXACTLY the shape ts\nfrom\nto\n\ntext
    assert canonical == f"{meta['ts']}\n{meta['from']}\n{meta['to']}\n\nhello"
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, "seat-a").read_text())
    pub = scheme.public_from_secret(bytes.fromhex(obj["priv_hex"]))
    assert scheme.verify(pub, canonical.encode(), bytes.fromhex(sig))


def test_body_altered_on_disk_is_forged(project, capsys, monkeypatch):
    send_mod.keygen(project, "seat-a")
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, "seat-a").read_text())
    pub_hex = scheme.public_from_secret(
        bytes.fromhex(obj["priv_hex"])).hex()
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "hello world", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    # tamper with the BODY on disk; the header (ts/from/sig) is untouched
    tampered = inbox.read_text().replace("hello world", "tampered!!")
    inbox.write_text(tampered)
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "FORGED" in out
    assert "tampered!!" in out, "the block still prints in full under FORGED"


def test_sig_under_scheme_row_does_not_name_is_forged(project, capsys,
                                                      monkeypatch):
    send_mod.keygen(project, "seat-a")          # signs with ed25519
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, "seat-a").read_text())
    pub_hex = scheme.public_from_secret(
        bytes.fromhex(obj["priv_hex"])).hex()
    # the row declares a DIFFERENT scheme: the sig is under one the row does
    # not name -> FORGED even though the ed25519 signature is genuine
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "dummy", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "hello", "seat-a")
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "FORGED" in out


def test_no_key_file_is_unsigned_and_equals_todays_bytes(project):
    send_mod.send(project, "recv", "hello", "seat-a")   # no .key file
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    content = inbox.read_text()
    assert "sig:" not in content
    # today's unchanged block shape: `---\nts: T\nfrom: seat-a\nto: recv\n\nhello\n`
    ts = content.split("ts: ")[1].split("\n")[0]
    expected = (f"{send_mod.MSG_SEP}ts: {ts}\nfrom: seat-a\nto: recv\n"
                f"\nhello\n")
    assert content == expected


def test_dummy_scheme_plugs_in_without_changing_send(project, capsys,
                                                     monkeypatch):
    """The swappable-scheme claim, end to end: register a toy scheme in
    send.py's own seatsig table; keygen + send + read VERIFIED need no change
    to send.py beyond get()/Scheme calls."""
    send_mod.seatsig.SCHEMES["dummy"] = _DummyScheme()
    try:
        send_mod.keygen(project, "seat-d", "dummy")
        obj = json.loads(_seat_key_file(project, "seat-d").read_text())
        d = _DummyScheme()
        pub_hex = d.public_from_secret(bytes.fromhex(obj["priv_hex"])).hex()
        _stub_seat_rows(monkeypatch, [
            {"name": "seat-d", "sig_scheme": "dummy", "pubkey": pub_hex},
        ])
        send_mod.send(project, "recv", "hi", "seat-d")
        send_mod.read(project, "recv", None)
        out = capsys.readouterr().out
        assert "VERIFIED seat-d (dummy)" in out
        assert "hi" in out
    finally:
        send_mod.seatsig.SCHEMES.pop("dummy", None)


# ── hypothesis:l4-wake-repair-is-quiet-honest-and-readable, clause 4 ─────
# read drains a stored deferred dm (prints it as its own block, then clears
# the record); peek shows it WITHOUT clearing. The deferred sidecar lives at
# `.agi/sessions/inbox/<seat>.nudge.deferred` next to the inbox, and the
# record's own delivered-count semantics for the PANE path are untouched.


def test_read_drains_a_stored_deferred_dm(project: Path, capsys):
    """A stored deferred dm is printed as its own block and the record is
    cleared, so a director who never had an idle pane still sees it once."""
    send_mod._store_deferred(project, "sanctuary-director", "sanctuary-helper",
                             "rotation alert: handoff active")
    deferred_path = send_mod._nudge_deferred_path(
        project, "sanctuary-director")

    send_mod.read(project, "sanctuary-director", None)
    out = capsys.readouterr().out

    # its own block, headed with the sender and a timestamp
    assert "deferred dm from sanctuary-helper (" in out
    assert "rotation alert: handoff active" in out
    assert not deferred_path.exists(), \
        "read clears the deferred record after printing it"


def test_peek_shows_deferred_without_clearing(project: Path, capsys):
    """peek prints the stored deferred dm but leaves the record in place."""
    send_mod._store_deferred(project, "sanctuary-director", "sanctuary-helper",
                             "rotation alert: handoff active")
    deferred_path = send_mod._nudge_deferred_path(
        project, "sanctuary-director")

    send_mod.peek(project, "sanctuary-director")
    out1 = capsys.readouterr().out
    assert "deferred dm from sanctuary-helper (" in out1
    assert "rotation alert: handoff active" in out1

    # peek again — still there (not cleared)
    send_mod.peek(project, "sanctuary-director")
    out2 = capsys.readouterr().out
    assert "rotation alert: handoff active" in out2
    assert deferred_path.exists(), "peek must not clear the deferred record"


def test_read_deferred_prints_before_inbox_blocks(project: Path, capsys):
    """The deferred block comes FIRST, before any inbox blocks."""
    send_mod._store_deferred(project, "director", "sanctuary-helper",
                             "rotation alert: handoff active")
    send_mod.send(project, "director", "the inbox body", "some-kid")

    send_mod.read(project, "director", None)
    out = capsys.readouterr().out
    assert out.index("deferred dm from sanctuary-helper") < \
        out.index("the inbox body"), \
        "the deferred block is printed BEFORE the inbox blocks"

    # and read still clears the deferred while marking the inbox read
    assert not send_mod._nudge_deferred_path(project, "director").exists()
    send_mod.read(project, "director", None)
    assert "empty" in capsys.readouterr().out


def test_read_deferred_only_no_empty_and_no_inbox_touch(project: Path, capsys):
    """A deferred dm with an empty inbox prints the deferred (NOT 'empty')
    and does not create an inbox file."""
    send_mod._store_deferred(project, "lonely", "helper", "hello alone")
    send_mod.read(project, "lonely", None)
    out = capsys.readouterr().out
    assert "deferred dm from helper (" in out
    assert "empty" not in out
    inbox = project / ".agi" / "sessions" / "inbox" / "lonely.md"
    assert not inbox.exists(), \
        "reading a deferred dm must not fabricate an inbox file"


# ── hypothesis:l4-sign-exactly-the-bytes-the-reader-parses... (SL6.06) ─────
# One canonical form: the reader must parse back EXACTLY the bytes whose
# signature was computed, so a LEGITIMATE body never reads FORGED. Four named
# tests: LF-terminated, ---line, CRLF bodies each sign->store->read->VERIFIED,
# plus the TAMPER guard that must still read FORGED (never lowered).

def test_lf_terminated_body_verifies_not_forged(project, capsys, monkeypatch):
    """A body whose text legitimately ends in "\\n" must read VERIFIED, never
    FORGED. The writer appends EXACTLY one "\\n" after text; the reader must
    strip exactly that one (its exact inverse), never rstrip every trailing LF
    -- rstrip eats a genuine trailing LF and the sig no longer covers the
    signed bytes, so a genuine body reads FORGED."""
    send_mod.keygen(project, "seat-lf")
    body = "line one\nline two\n"
    pub_hex = _seat_pubkey_hex(project, "seat-lf")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-lf", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", body, "seat-lf")
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED" in out, out
    assert "FORGED" not in out, out


def test_dash_dash_dash_body_line_verifies_not_forged(project, capsys,
                                                      monkeypatch):
    """A body containing a line equal to the block separator "---" must read
    VERIFIED, never FORGED, and stay ONE block. The splitter must only split on
    a separator that is followed by a header ("ts:"), never on a body line
    equal to "---" (which currently fragments one signed block -- the head
    carries the sig over the WHOLE body, so the split tail verifies against
    nothing and reads FORGED)."""
    send_mod.keygen(project, "seat-dash")
    body = "before\n---\nafter\n"
    pub_hex = _seat_pubkey_hex(project, "seat-dash")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-dash", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", body, "seat-dash")
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED" in out, out
    assert "FORGED" not in out, out


def test_body_dash_dash_dash_then_ts_like_line_stays_one_block_verified(
        project, capsys, monkeypatch):
    """SL7.02 clause (4): a signed body containing a "---" line IMMEDIATELY
    followed by a line that starts "ts: " (a body line that merely STARTS like
    a header, with no "from:" after it) must stay ONE block and read VERIFIED,
    never FORGED. The boundary now requires a FULL header after the separator
    ("---\\n" + "ts: ...\\n" + "from: "), so the fake header inside the body
    no longer fragments the block and its own sig no longer reads FORGED on the
    split tail."""
    send_mod.keygen(project, "seat-bd")
    body = "before\n---\nts: 2026-01-01T00:00:00+00:00\nmid\n"
    pub_hex = _seat_pubkey_hex(project, "seat-bd")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-bd", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", body, "seat-bd")

    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    blocks = send_mod._parse_blocks(inbox.read_text())
    assert len(blocks) == 1, blocks  # ONE block, never split on the fake header
    assert blocks[0]["text"] == "before\n---\nts: 2026-01-01T00:00:00+00:00\nmid"

    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED" in out, out
    assert "FORGED" not in out, out


def test_crlf_body_verifies_not_forged(project, capsys, monkeypatch):
    """A body containing CRLF pairs round-trips byte-exact and reads VERIFIED,
    never FORGED (newline='' on both sides already preserves CR; the parser
    splits on "\\n" alone, so every "\\r" survives)."""
    send_mod.keygen(project, "seat-crlf")
    body = "line1\r\nline2\r\nline3\r\n"
    pub_hex = _seat_pubkey_hex(project, "seat-crlf")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-crlf", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", body, "seat-crlf")
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED" in out, out
    assert "FORGED" not in out, out


def test_tampered_body_still_reads_forged(project, capsys, monkeypatch):
    """GUARD (never lowered): bytes changed AFTER signing must still read
    FORGED -- a signature that no longer covers the stored bytes is exactly
    what FORGED means."""
    send_mod.keygen(project, "seat-tamp")
    pub_hex = _seat_pubkey_hex(project, "seat-tamp")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-tamp", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "original bytes", "seat-tamp")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    blob = inbox.read_text().replace("original bytes", "tampered bytes")
    inbox.write_text(blob)
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "FORGED" in out, out
    assert "VERIFIED" not in out, out


# ── hypothesis:l4-every-live-row-is-keyed-every-send-is-signed... clause (1) ──
# keygen now WRITES the seat-row cells it prints (pubkey, sig_scheme,
# enc_scheme: none) through write.submit (the sanctioned writer), with the
# prime keying every LIVE row (a live pid / session_id) that lacks a pubkey
# and a second keygen refusing to overwrite an existing .key by name. All
# tests here use a fake tmp-root config:seats node -- never the live tree.

def _write_seats_node(project, rows):
    d = project / ".agi" / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {r!r}" for r in rows)
    (d / "seats.md").write_text(
        "---\nid: config:seats\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nseats:\n" + body +
        "\n---\n\n# config:seats\n\nfixture body\n")


def _read_seats(project):
    nf = send_mod._fm.load_node_file(
        project / ".agi" / "nodes" / ".geometry" / "seats.md")
    return [dict(r) for r in (nf.frontmatter.get("seats") or [])
            if isinstance(r, dict)]


def test_keygen_refuses_to_overwrite_existing_key(project):
    """A second keygen against an existing .key refuses and the key bytes are
    unchanged (the never-overwrite clause, asserted by name)."""
    path = send_mod.keygen(project, "seat-a")
    assert path is not None and path.is_file()
    before = path.read_bytes()
    out = send_mod.keygen(project, "seat-a")
    assert out is None, "a second keygen must refuse, not return a path"
    assert path.read_bytes() == before, "the existing key bytes are unchanged"


def test_keygen_writes_own_row_cells_through_write_submit(project, capsys):
    """keygen <seat> writes pubkey/sig_scheme/enc_scheme into its OWN row via
    write.submit under the self-row carve-out; no other row is touched."""
    _write_seats_node(project, [
        {"name": "sanctuary-director", "role": "director", "pid": 1234},
        {"name": "belam", "role": "prime_director", "pid": 999},
    ])
    path = send_mod.keygen(project, "sanctuary-director",
                           actor="sanctuary-director-4e")
    assert path is not None
    seats = _read_seats(project)
    own = next(r for r in seats if r["name"] == "sanctuary-director")
    assert own["pubkey"], "the own row now carries the public key"
    assert own["sig_scheme"] == "ed25519"
    assert own["enc_scheme"] == "none"
    other = next(r for r in seats if r["name"] == "belam")
    assert "pubkey" not in other, "a self-row write must not touch another row"
    out = capsys.readouterr().out
    assert "enc_scheme: none" in out


def test_keygen_all_live_keys_live_rows_only_and_skips_keyed(project, capsys):
    """Prime's --all-live keys every LIVE row (pid/session_id) lacking a
    pubkey, leaves the dead row alone, and skips an already-keyed row."""
    _write_seats_node(project, [
        {"name": "s1", "role": "director", "pid": 111},
        {"name": "s2", "role": "director", "session_id": "abc"},
        {"name": "s3", "role": "director"},                     # dead
        {"name": "s4", "role": "director", "pid": 222,
         "pubkey": "already-keyed"},
    ])
    out = send_mod.keygen(project, all_live=True, actor="belam",
                          role="prime_director")
    assert out is not None and len(out) == 2
    seats = _read_seats(project)
    by = {r["name"]: r for r in seats}
    assert by["s1"]["pubkey"] and by["s1"]["sig_scheme"] == "ed25519"
    assert by["s1"]["enc_scheme"] == "none"
    assert by["s2"]["pubkey"], "a live row (session_id) still gets keyed"
    assert "pubkey" not in by["s3"], "the DEAD row must not gain a key"
    assert by["s4"]["pubkey"] == "already-keyed", "keyed row is skipped"
    stdout = capsys.readouterr().out
    assert "keyed s1" in stdout and "keyed s2" in stdout
    assert "skipped s4 (already keyed)" in stdout
    assert _seat_key_file(project, "s1").is_file()
    assert _seat_key_file(project, "s2").is_file()
    assert not _seat_key_file(project, "s3").exists(), "dead rows get no .key"
    # the private seed is never printed
    obj = json.loads(_seat_key_file(project, "s1").read_text())
    assert obj["priv_hex"] not in stdout


def test_keygen_all_live_refuses_non_prime_director_by_name(project, capsys,
                                                             monkeypatch):
    """mur-39 order (c), PRIME GATE: --all-live is a PRIME-ONLY backstop. A
    seat whose OWN row role is not prime_director is refused by name BEFORE any
    key file is minted -- the refusal names the seat and the role, and zero
    .key files land (today only the row write was refused and the keys leaked)."""
    _write_seats_node(project, [
        {"name": "sanctuary-director", "role": "director", "pid": 1234},
        {"name": "s1", "role": "director", "pid": 111},
    ])
    out = send_mod.keygen(project, all_live=True, actor="sanctuary-director")
    assert out is None, "--all-live must refuse a non-prime_director seat"
    # zero keys minted anywhere: the gate runs before the first _mint_seat_key
    assert not _seat_key_file(project, "sanctuary-director").exists()
    assert not _seat_key_file(project, "s1").exists()
    err = capsys.readouterr().err
    assert "REFUSED sanctuary-director" in err, err
    assert "director" in err and "prime_director" in err, \
        "the refusal names the seat AND the role"


def test_keygen_all_live_grants_a_row_prime_director(project, capsys,
                                                      monkeypatch):
    """mur-39 order (c): a caller whose OWN row holds role prime_director is
    allowed to run --all-live (the gate refuses by name, never blocks the
    prime)."""
    _write_seats_node(project, [
        {"name": "belam", "role": "prime_director"},   # not live -> not keyed
        {"name": "s1", "role": "director", "pid": 111},
    ])
    out = send_mod.keygen(project, all_live=True, actor="belam")
    assert out is not None and len(out) == 1
    assert _seat_key_file(project, "s1").is_file()
    stdout = capsys.readouterr().out
    assert "keyed s1" in stdout


# --- clause (1): a refused row write / missing seat row makes the CLI exit 2 --
# and every keyed row carries key_history: [] (hypothesis:l4-keygen-exits-on-
# a-refused-row...). Pre-fix, keygen discarded `_row_write_submit`'s bool and
# exited 0 -- a key on disk with no pubkey on the row read UNKEYED forever.


def _cli_keygen_args(**kw):
    import argparse as _ar
    base = dict(all_live=False, seat="", scheme="ed25519", from_id=None)
    base.update(kw)
    return _ar.Namespace(**base)


def test_cli_keygen_exits_2_when_seat_row_missing(project, capsys):
    """clause (1): a key minted for a seat whose row is NOT in the registry
    exits 2 with the ONE canonical stderr line -- pre-fix this exited 0 and
    the key read UNKEYED forever."""
    args = _cli_keygen_args(seat="ghost-seat")
    assert send_mod._cli_keygen(project, args) == 2
    err = capsys.readouterr().err
    assert "keygen: key minted but the row write was refused" in err, err
    assert "UNKEYED" in err, err
    # the key was still minted on disk (a keygen never fails to mint)
    assert _seat_key_file(project, "ghost-seat").is_file()


def test_cli_keygen_exits_2_when_row_write_refused(project, capsys,
                                                    monkeypatch):
    """clause (1): write.submit refusing to admit the row write (no admitted
    actor / no seating) still mints the key but the CLI exits 2 -- the row
    stays UNKEYED and the operator is told in one line."""
    _write_seats_node(project, [
        {"name": "refuse-seat", "role": "director", "pid": 1},
    ])
    monkeypatch.setattr(send_mod, "_row_write_submit", lambda *a, **k: False)
    args = _cli_keygen_args(seat="refuse-seat")
    assert send_mod._cli_keygen(project, args) == 2
    assert _seat_key_file(project, "refuse-seat").is_file()
    err = capsys.readouterr().err
    assert "keygen: key minted but the row write was refused" in err, err
    assert "refuse-seat" in err, err


def test_cli_keygen_exits_0_on_happy_row_write(project):
    """clause (1): a keyed row whose write lands returns exit 0 (unchanged
    happy path -- the refused-row exit is a NEW code, not a repurposed 1)."""
    _write_seats_node(project, [
        {"name": "ok-seat", "role": "director", "pid": 1},
    ])
    assert send_mod._cli_keygen(project, _cli_keygen_args(seat="ok-seat")) == 0


def test_keygen_seeds_key_history_on_keyed_row(project):
    """clause (1): keygen seeds an EMPTY key_history on the single keyed row
    so every keyed row carries the cell (the RETIRED reader tolerates absence,
    but the row shape now carries it)."""
    _write_seats_node(project, [
        {"name": "hist-seat", "role": "director", "pid": 1},
    ])
    send_mod.keygen(project, "hist-seat")
    own = next(r for r in _read_seats(project) if r["name"] == "hist-seat")
    assert own.get("key_history") == []


def test_keygen_all_live_seeds_key_history(project):
    """clause (1): --all-live seeds key_history: [] on every freshly keyed
    live row, and leaves the dead row untouched."""
    _write_seats_node(project, [
        {"name": "belam", "role": "prime_director", "pid": 999},
        {"name": "s1", "role": "director", "pid": 111},
        {"name": "s3", "role": "director"},                     # dead
    ])
    send_mod.keygen(project, all_live=True, actor="belam",
                    role="prime_director")
    by = {r["name"]: r for r in _read_seats(project)}
    assert by["s1"].get("key_history") == []
    assert "key_history" not in by["s3"], "the dead row is left untouched"


def test_cr_body_with_crlf_and_lone_cr_verifies_and_keeps_bytes(
        project, capsys, monkeypatch):
    """mur-39 order (d): a signed body carrying a CRLF, a LONE CR and a
    TRAILING CR must (i) read VERIFIED (never FORGED) and (ii) store the exact
    bytes the sender passed -- the parser must not normalize CR, or the
    canonical bytes the sig covers change and the message reads FORGED."""
    send_mod.keygen(project, "seat-cr")
    body = "line1\r\nline2\rline3\r"
    pub_hex = _seat_pubkey_hex(project, "seat-cr")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-cr", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", body, "seat-cr")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    # (ii) the stored body bytes equal the sent bytes, CR included. Read with
    # newline="" so the check measures what is ON DISK, not a universal-newline
    # read that collapses CR before we can compare.
    raw = inbox.open("r", newline="").read()
    _, parsed = send_mod._parse_block(raw.split(send_mod.MSG_SEP)[1])
    assert parsed == body, (
        "parser must return the exact sent bytes (CRLF/lone CR/trailing CR); "
        f"got {parsed!r}")
    # (i) the read label is VERIFIED, never FORGED
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED" in out, out
    assert "FORGED" not in out


# ── hypothesis:l4-every-live-row-is-keyed... clauses (2)+(3)+(4): envelope, ──
# key_history RETIRED, and whois verifies with INFORMATIONAL labels.
# (2) every signed message carries `env: v1` beside its `sig:` line and the
#     scheme name comes from the row; seatsig.Scheme has an OPTIONAL
#     encryption slot (enc_scheme/encrypt/decrypt = None today); no caller
#     outside src/seatsig names the "ed25519" literal (the keygen default now
#     flows through seatsig.DEFAULT_SCHEME). (3) a sig whose fingerprint is in
#     the from-seat's key_history AND verifies under that retired pub answers
#     RETIRED:<fp>, never FORGED. (4) whois verifies a signature against the
#     row and reports the label; the label is INFORMATIONAL -- whois's exit
#     code stays on the claim/role authority axis and never changes on it.

def _signed_send_and_canonical(project, seat, to, text):
    """Send a signed message and return (sig_line, canonical_msg) for the SAME
    message, so whois can verify the exact bytes the sig covers."""
    send_mod.send(project, to, text, seat)
    inbox = project / ".agi" / "sessions" / "inbox" / f"{to}.md"
    block_text = inbox.read_text().split(send_mod.MSG_SEP)[1]
    meta, body = send_mod._parse_block(block_text)
    canonical = send_mod._canonical_msg(meta["ts"], meta["from"], meta["to"],
                                        body)
    return meta["sig"], canonical


def _seat_pubkey_hex(project, seat):
    """Recover a seat's public key hex from its on-disk .key seed."""
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, seat).read_text())
    return scheme.public_from_secret(bytes.fromhex(obj["priv_hex"])).hex()


def _fp(project, seat):
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, seat).read_text())
    return send_mod.seatsig.fingerprint(
        scheme.public_from_secret(bytes.fromhex(obj["priv_hex"])))


# --- clause (2): envelope `env: v1` + the ONE plug point --------------------


def test_signed_message_carries_env_v1_beside_sig(project):
    """Every signed message carries `env: v1` immediately before its sig line."""
    send_mod.keygen(project, "seat-a")
    send_mod.send(project, "recv", "hello env", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    lines = inbox.read_text().splitlines()
    env_idx = next(i for i, l in enumerate(lines) if l == "env: v1")
    assert lines[env_idx + 1] and lines[env_idx + 1].startswith("sig: "), \
        "env: v1 sits directly beside the sig line"


def test_unsigned_message_has_no_env_line(project):
    """A message with no key file is unsigned and carries no env line."""
    send_mod.send(project, "recv", "hello", "seat-a")   # no .key file exists
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    assert "env:" not in inbox.read_text()


def test_scheme_has_optional_encryption_hook_slot():
    """seatsig.Scheme carries the encryption SEAM (enc_scheme/encrypt/decrypt
    = None today); SCHEMES is the ONE plug point. Prime ruling B: the seam,
    not the cipher -- dead slots that look like a feature are out."""
    scheme = send_mod.seatsig.get("ed25519")
    assert scheme.enc_scheme is None
    assert scheme.encrypt is None
    assert scheme.decrypt is None


def test_default_scheme_flows_through_registry_not_a_literal():
    """send.py names the REGISTRY (seatsig.DEFAULT_SCHEME), never the
    algorithm literal. Keygen's default and the --scheme default both resolve
    through it and stay equal to the registered default."""
    assert send_mod.seatsig.DEFAULT_SCHEME == "ed25519"
    from inspect import signature
    sig = signature(send_mod.keygen)
    assert sig.parameters["scheme_name"].default == \
        send_mod.seatsig.DEFAULT_SCHEME


def test_no_production_caller_names_ed25519_literal():
    """grep-assert: no caller OUTSIDE src/seatsig names the 'ed25519' literal
    (only the registry does). The literal today was the keygen default arg --
    routed through seatsig.DEFAULT_SCHEME, the caller now names the registry,
    not the algorithm."""
    import subprocess  # noqa: F401 (used via regex scan below)
    src = Path(send_mod.__file__).read_text()
    assert "ed25519" not in src, "send.py must not spell the algorithm literal"


# --- clause (3): key_history / RETIRED --------------------------------------


def test_retired_key_reads_retired_fp_not_forged(project, capsys,
                                                 monkeypatch):
    """A sig under a key moved into the from-seat's key_history, verifying
    under that retired pub, answers RETIRED:<fp> -- never FORGED."""
    send_mod.keygen(project, "seat-old")       # the key that will be retired
    send_mod.keygen(project, "seat-new")       # the current key of the seat
    # 'seat-old' row declares seat-new's pub as CURRENT and seat-old's pub as
    # a retired key in key_history.
    new_pub = _seat_pubkey_hex(project, "seat-new")
    old_pub = _seat_pubkey_hex(project, "seat-old")
    old_fp = _fp(project, "seat-old")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-old", "sig_scheme": "ed25519", "pubkey": new_pub,
         "key_history": [{"pub": old_pub, "fp": old_fp, "from": "t0",
                          "to": "t1", "rotated_by_sig": "sig"}]},
    ])
    # sign with the OLD key file (seat-old.key still holds the old priv)
    send_mod.send(project, "recv", "hello", "seat-old")
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert f"RETIRED:{old_fp}" in out
    assert "FORGED" not in out, "a retired key must never read FORGED"


def test_unknown_key_still_reads_forged(project, capsys, monkeypatch):
    """A sig with a fingerprint in NO key_history and failing the current pub
    still reads FORGED (the retired carve-out does not soften the real one)."""
    send_mod.keygen(project, "seat-a")
    send_mod.keygen(project, "seat-b")   # unrelated key, not retired
    a_pub = _seat_pubkey_hex(project, "seat-a")
    b_pub = _seat_pubkey_hex(project, "seat-b")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": a_pub},
        {"name": "seat-b", "sig_scheme": "ed25519", "pubkey": b_pub},
    ])
    # sign as seat-b but read the message into recv -- from: seat-b with the
    # seat-b row present is genuinely seat-b, so instead tamper the body.
    send_mod.send(project, "recv", "hello x", "seat-b")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    inbox.write_text(inbox.read_text().replace("hello x", "tampered!!"))
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    # seat-b's row has no key_history -> the tampered sig reads FORGED
    assert "FORGED" in out


# --- clause (4): whois verifies, label stays INFORMATIONAL ------------------


def test_whois_verifies_signed_line_and_reports_label(project, monkeypatch):
    """whois with a signed line verifies against the resolved row and reports
    the label; the authority exit code is untouched by the label."""
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a",
                                                     "recv", "whois me")
    pub_hex = _seat_pubkey_hex(project, "seat-a")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "session_ref": "seat-a",
         "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=canonical)
    assert rc == send_mod.WHOIS_OK, rc           # claim axis, label off it
    assert "VERIFIED seat-a (ed25519)" in text


def test_whois_unsigned_reports_unsigned_exit_unchanged(project, monkeypatch):
    """whois with no signed line reports UNSIGNED -- informational, exit code
    unchanged."""
    send_mod.keygen(project, "seat-a")
    pub_hex = _seat_pubkey_hex(project, "seat-a")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "session_ref": "seat-a",
         "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False)
    assert rc == send_mod.WHOIS_OK, rc
    assert "UNSIGNED" in text


def test_whois_forged_label_does_not_gate_exit(project, monkeypatch):
    """whois on a FORGED signature still returns the NORMAL authority exit
    code (here WHOIS_OK, a positive claim) -- the label is informational and
    never gates the decision (Prime ruling A)."""
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a",
                                                     "recv", "ok claim")
    pub_hex = _seat_pubkey_hex(project, "seat-a")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "session_ref": "seat-a",
         "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    # tamper the msg so the sig no longer verifies -> FORGED label
    forged_rc, forged_text = send_mod.whois(
        project, "seat-a", claim="seat-a", source="refs/x", do_fetch=False,
        sig_line=sig_line, msg_text=canonical + "x")
    assert "FORGED" in forged_text
    # the exit code is the authority axis answer (WHOIS_OK) -- NEVER keyed on
    # the FORGED label.
    assert forged_rc == send_mod.WHOIS_OK, forged_rc


# ── clause (3): whois --sig under comms.verify=="enforcing" refuses a FORGED
# ── label (hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-
# ── the-value-flips-after-a-named-review). Enforcement is the ONE exception to
# ── Prime ruling A: only an EXACTLY-FORGED label + a canonical --msg to
# ── withhold + the config saying "enforcing" turns the exit to 2. Everything
# ── else stays byte-identical to today.


def _seat_a_pub_rows(project, seat="seat-a"):
    """The stub rows whois needs to resolve `seat` both as a session_ref and
    resolve its row for the sig label (name == session_ref == seat)."""
    return [{"name": seat, "session_ref": seat,
             "sig_scheme": "ed25519", "pubkey": _seat_pubkey_hex(project, seat)}]


def _whois_forged_fixture(tmp_path, monkeypatch):
    """An enforcing project + a signed whois sig/canonical whose msg is
    tampered so the label is FORGED. Returns (project, forgeline, forged_msg)."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    # keygen FIRST (the send signs under the seat's key), THEN stub the rows
    # with the now-real pubkey, so whois can resolve the sig.
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "whois me")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    return project, sig_line, canonical + "x"


def test_whois_forged_under_enforcing_exits_2_and_quarantines(
        tmp_path, monkeypatch, capsys):
    """Clause (3): a whois --sig whose label is FORGED under verify=="enforcing"
    exits WHOIS_NOT_AUTHORIZED (2) EVEN on a positive authority answer, prints
    the SAME refusal line shape as clause (1), and appends the sig+msg to
    <inbox>/quarantine/<session_ref>.md (same append semantics)."""
    project, sig_line, forged_msg = _whois_forged_fixture(tmp_path, monkeypatch)
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=forged_msg)
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED, rc
    assert "REFUSED FORGED from seat-a " in text
    assert "withheld to " in text
    fp = sig_line.split(":", 2)[1]
    assert f"fp {fp}:" in text, "the refusal names the sig fingerprint"
    q = _quarantine_path(project, seat="seat-a")
    assert q.is_file()
    assert sig_line in q.read_text(), \
        "the quarantine record carries the --sig line verbatim"
    assert forged_msg in q.read_text(), \
        "the quarantine record carries the canonical --msg whois was handed"


def test_whois_verified_under_enforcing_exit_unchanged(
        tmp_path, monkeypatch):
    """A non-FORGED label (VERIFIED) under enforcing never changes the exit: it
    returns the normal authority code and nothing is quarantined."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-a")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "ok claim")
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=canonical)
    assert rc == send_mod.WHOIS_OK, rc
    assert "VERIFIED" in text
    assert "REFUSED" not in text
    assert not _quarantine_path(project, seat="seat-a").exists(), \
        "a VERIFIED whois is never quarantined"


def test_whois_forged_without_msg_still_refused_under_enforcing(
        tmp_path, monkeypatch):
    """A FORGED label with NO --msg to withhold is STILL refused (exit 2) under
    enforcing: the refusal line names that there is no --msg, and no quarantine
    file is fabricated (there were no bytes to withhold)."""
    project, sig_line, _ = _whois_forged_fixture(tmp_path, monkeypatch)
    # give the tampered sig but no --msg -> label is FORGED, nothing to withhold
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=None)
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED, rc
    assert "REFUSED" in text
    assert "FORGED" in text
    assert "no --msg" in text, \
        "the refusal names that there is no --msg to withhold"
    assert not _quarantine_path(project, seat="seat-a").exists(), \
        "no msg -> nothing quarantined (no fabricated file)"


def test_whois_forged_without_msg_informational_not_refused(
        tmp_path, monkeypatch):
    """Under a NON-enforcing (informational) verify, a FORGED label with no
    --msg keeps today's behavior: exit on the authority axis, FORGED line, no
    refusal, nothing quarantined."""
    project = _project_with_comms(tmp_path, {"verify": "informational"})
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "whois me")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=None)
    assert rc == send_mod.WHOIS_OK, rc
    assert "FORGED" in text
    assert "REFUSED" not in text
    assert not _quarantine_path(project, seat="seat-a").exists(), \
        "informational verify never refuses or quarantines"


def test_whois_quarantine_filename_sanitized_against_traversal(
        tmp_path, monkeypatch):
    """A session_ref shaped like a traversal (`../../x`, `a/b`) can never pick
    a path: the written file lands INSIDE <inbox>/quarantine with a sanitized
    name, the raw ref survives as the record's first line, and the refusal line
    names the raw ref."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "whois me")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    forged = canonical + "x"
    # a traversal-shaped ref under a FORGED label (row for it won't resolve)
    qdir = project / ".agi" / "sessions" / "inbox" / "quarantine"
    inbox = project / ".agi" / "sessions" / "inbox"
    before = {p for p in inbox.iterdir()}
    for raw in ("../../x", "a/b"):
        rc, text = send_mod.whois(project, raw, claim="seat-a",
                                  source="refs/x", do_fetch=False,
                                  sig_line=sig_line, msg_text=forged)
        assert rc == send_mod.WHOIS_NOT_AUTHORIZED, (raw, rc)
        # the refusal names the RAW ref
        assert repr(raw) in text, (raw, text)
        # find the file this call wrote (sanitized name, inside quarantine)
        sanitized = send_mod._sanitize_ref(raw)
        q = qdir / f"{sanitized}.md"
        assert q.is_file(), f"sanitized file {sanitized}.md missing"
        assert q.resolve().parent == qdir.resolve(), \
            f"{raw} escaped the quarantine dir"
        body = q.read_text()
        assert raw in body, "the RAW ref survives as the record's first line"
        assert sig_line in body
        assert forged in body
    # no NEW file appeared OUTSIDE the quarantine dir
    outside = [p for p in inbox.iterdir() if p not in before
               and p.name != "quarantine" and p.is_file()]
    assert outside == [], f"traversal-shaped ref escaped the quarantine: {outside}"


def test_whois_quarantine_refuses_empty_sanitized_ref(
        tmp_path, monkeypatch):
    """SL7.02 clause (5): a session_ref that sanitizes to empty (only
    stripped chars) is REFUSED in one line with exit 2 BEFORE any quarantine
    path is built -- no file (not even the old invalid-ref.md fallback) is
    written and no path is derived from the absent ref."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "whois me")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    forged = canonical + "x"
    qdir = project / ".agi" / "sessions" / "inbox" / "quarantine"
    with pytest.raises(SystemExit) as ex:
        send_mod.whois(project, "///", claim="seat-a",
                       source="refs/x", do_fetch=False,
                       sig_line=sig_line, msg_text=forged)
    assert ex.value.code == 2
    # nothing was written -- refusal happened BEFORE any path was built
    if qdir.exists():
        assert not any(qdir.iterdir()), f"empty ref must write nothing: {list(qdir.iterdir())}"
    qdir.mkdir(parents=True, exist_ok=True)  # guard: still nothing may appear


def test_whois_quarantine_refuses_overlong_ref(tmp_path, monkeypatch):
    """SL7.02 clause (5): a session_ref whose sanitized form exceeds 64 chars
    is REFUSED in one line with exit 2 BEFORE any quarantine path is built; a
    ref AT the 64-char cap is accepted and quarantined under its name."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a", "recv",
                                                     "whois me")
    _stub_seat_rows(monkeypatch, _seat_a_pub_rows(project))
    forged = canonical + "x"
    qdir = project / ".agi" / "sessions" / "inbox" / "quarantine"

    long_ref = "x" * 65
    with pytest.raises(SystemExit) as ex:
        send_mod.whois(project, long_ref, claim="seat-a",
                       source="refs/x", do_fetch=False,
                       sig_line=sig_line, msg_text=forged)
    assert ex.value.code == 2

    # at the 64-char cap it is accepted and lands under its (capped) name
    cap_ref = "y" * 64
    rc, text = send_mod.whois(project, cap_ref, claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=forged)
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED, rc
    q = qdir / f"{cap_ref}.md"
    assert q.is_file(), f"64-char ref must quarantine under its own name"


def test_sanitize_ref_accepts_and_refuses_bounds():
    """Unit-level bound for _sanitize_ref: keeps [A-Za-z0-9._-], accepts 1-64
    chars, and REFUSES (exit 2) on empty or >64 sanitized length."""
    assert send_mod._sanitize_ref("a-b.c_1") == "a-b.c_1"
    assert send_mod._sanitize_ref("../x/y") == "..xy"  # / stripped, . kept
    assert send_mod._sanitize_ref("y" * 64) == "y" * 64  # at the cap: OK
    for bad in ("", "///", "y" * 65, "/" * 10):
        with pytest.raises(SystemExit) as ex:
            send_mod._sanitize_ref(bad)
        assert ex.value.code == 2, bad


def test_whois_cli_threads_sig_and_msg(monkeypatch, capsys):
    """The --sig/--msg flags declared on the whois subparser actually reach the
    whois function (they were declared and never threaded before clause 3)."""
    seen = {}
    def capturing(root, ref, claim, source, do_fetch,
                  sig_line=None, msg_text=None):
        seen["sig"] = sig_line
        seen["msg"] = msg_text
        return (0, "x")
    monkeypatch.setattr(send_mod, "whois", capturing)
    rc = send_mod.main(["whois", "--no-fetch", "7902ac",
                        "--sig", "ed25519:aa11:bb22",
                        "--msg", "line1\nline2\nline3\n\ntext"])
    assert rc == 0
    assert seen["sig"] == "ed25519:aa11:bb22"
    assert seen["msg"] == "line1\nline2\nline3\n\ntext"


def test_whois_cli_forged_under_enforcing_exits_2(tmp_path, monkeypatch, capsys):
    """End-to-end: `send.py whois --sig <forged> --msg <tampered>` under an
    enforcing config returns 2 through the CLI, not only via the module fn."""
    project, sig_line, forged_msg = _whois_forged_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    capsys.readouterr()                      # drain keygen/send stdout
    rc = send_mod.main(["whois", "--no-fetch", "seat-a",
                        "--claim", "seat-a",
                        "--sig", sig_line, "--msg", forged_msg])
    out = capsys.readouterr().out
    assert rc == send_mod.WHOIS_NOT_AUTHORIZED, rc
    assert "REFUSED FORGED" in out
    assert "withheld to " in out
    assert _quarantine_path(project, seat="seat-a").is_file()


# ── comms.lockdown reserved flag (hypothesis:l4-lockdown-is-a-reserved-
# ── boolean-that-warns-and-encrypts-nothing-until-it-is-built) ──────────


def _project_with_comms(tmp_path: Path, comms: dict) -> Path:
    """Like the `project` fixture but with a `comms` config block. Guaranteed
    unique dir per call so one test may build several sibling projects."""
    _project_with_comms.n += 1
    root = tmp_path / f"project-{_project_with_comms.n}"
    (root / ".agi").mkdir(parents=True)
    cfg = {"metric_primary": "outcome_coverage"}
    if comms is not None:
        cfg["comms"] = comms
    (root / ".agi" / "config.json").write_text(json.dumps(cfg))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


_project_with_comms.n = 0


def _strip_ts(text: str) -> str:
    """Drop the `ts:` line so two near-identical sends are comparable (the
    claim allows the ts line to differ under lockdown; everything else must
    be byte-identical)."""
    return "\n".join(l for l in text.splitlines() if not l.startswith("ts: "))


def test_comms_config_defaults_without_block(project: Path):
    """Absent comms block -> all defaults, never raises."""
    cfg = send_mod._comms_config(project)
    assert cfg["lockdown"] is False
    assert cfg["verify"] == "informational"


def test_comms_config_reads_block(project: Path):
    """A declared block is read; unknown keys are ignored, defaults kept."""
    (project / ".agi" / "config.json").write_text(json.dumps({
        "metric_primary": "outcome_coverage",
        "comms": {"lockdown": True, "verify": "enforcing",
                   "future_unknown": 1},
    }))
    cfg = send_mod._comms_config(project)
    assert cfg["lockdown"] is True
    assert cfg["verify"] == "enforcing"
    assert "future_unknown" not in cfg


# ── g15.26 flip: reader refuses a FORGED block under comms.verify==
# ── "enforcing" (hypothesis:l4-a-reader-refuses-a-forged-block-under-
# ── enforcing-and-the-value-flips-after-a-named-review). The ONE delivery
# ── path `_print_blocks_with_labels` enforces for BOTH read and peek; only a
# ── label EXACTLY == "FORGED" is refused, and the block's RAW inbox bytes are
# ── appended (never rewritten/truncated) to `<inbox>/quarantine/<seat>.md`
# ── with `newline=""` so CR bytes survive.


def _forged_inbox_with_rows(project, monkeypatch, body="tampered!!"):
    """Build a one-block inbox whose block reads FORGED: sign a message,
    then tamper the BODY on disk so the sig no longer verifies (header
    ts/from/sig untouched — the same recipe as
    test_body_altered_on_disk_is_forged). Returns (inbox_path,
    inbox_bytes_before_read, sig_fp)."""
    send_mod.keygen(project, "seat-a")
    scheme = send_mod.seatsig.get("ed25519")
    obj = json.loads(_seat_key_file(project, "seat-a").read_text())
    pub_hex = scheme.public_from_secret(
        bytes.fromhex(obj["priv_hex"])).hex()
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "hello world", "seat-a")
    inbox = project / ".agi" / "sessions" / "inbox" / "recv.md"
    inbox_text = inbox.read_text().replace("hello world", body)
    inbox.write_text(inbox_text)
    block = inbox_text.split(send_mod.MSG_SEP)[1]
    meta, _ = send_mod._parse_block(block)   # sig key -> "ed25519:<fp>:<hex>"
    fp = meta["sig"].split(":", 2)[1]
    return inbox, inbox_text, fp


def _quarantine_path(project, seat="recv"):
    return (project / ".agi" / "sessions" / "inbox"
            / "quarantine" / f"{seat}.md")


def test_enforcing_refuses_forged_and_quarantines_raw_bytes(
        tmp_path, capsys, monkeypatch):
    """Under verify:"enforcing" a FORGED block prints ONE refusal line
    INSTEAD of the body, and its RAW inbox bytes land VERBATIM in the
    quarantine file."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    inbox, inbox_text, fp = _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "tampered!!" not in out, \
        "a FORGED body must NOT print under enforcing"
    assert f"REFUSED FORGED from seat-a " in out
    assert f"fp {fp}:" in out, "the refusal names the sig fingerprint"
    assert "withheld to " in out
    # the quarantine file holds the EXACT inbox bytes of the refused block
    q = _quarantine_path(project)
    assert q.is_file()
    assert q.read_text() == inbox_text, \
        "quarantine must equal the block's inbox bytes verbatim"


def test_peek_enforcing_refuses_forged_too(tmp_path, capsys, monkeypatch):
    """peek uses the SAME delivery path, so it refuses a FORGED block too
    (one place, both verbs)."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    inbox, inbox_text, fp = _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.peek(project, "recv", wrap=160)
    out = capsys.readouterr().out
    assert "tampered!!" not in out
    assert f"REFUSED FORGED from seat-a " in out
    assert _quarantine_path(project).read_text() == inbox_text


def test_enforcing_prints_verified_and_unsigned_in_full(
        tmp_path, capsys, monkeypatch):
    """VERIFIED and UNSIGNED blocks print in FULL under enforcing — nothing
    but a FORGED label is withheld."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    # VERIFIED: sign seat-b with its own correct row
    send_mod.keygen(project, "seat-b")
    pub_hex = _seat_pubkey_hex(project, "seat-b")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-b", "sig_scheme": "ed25519", "pubkey": pub_hex},
    ])
    send_mod.send(project, "recv", "verified hello", "seat-b")
    # UNSIGNED: a seat with no key file
    send_mod.send(project, "recv", "unsigned hello", "no-key-seat")
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED seat-b (ed25519)" in out
    assert "verified hello" in out
    assert "UNSIGNED" in out
    assert "unsigned hello" in out
    assert "REFUSED" not in out
    assert not _quarantine_path(project).exists(), \
        "no quarantine for a non-FORGED block"


def test_enforcing_prints_retired_in_full(tmp_path, capsys, monkeypatch):
    """RETIRED is a GOOD signature under a retired key — under enforcing it
    prints in FULL and is never refused (the carve-out refuses nothing but
    FORGED)."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-old")
    send_mod.keygen(project, "seat-new")
    new_pub = _seat_pubkey_hex(project, "seat-new")
    old_pub = _seat_pubkey_hex(project, "seat-old")
    old_fp = _fp(project, "seat-old")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-old", "sig_scheme": "ed25519",
         "pubkey": new_pub,
         "key_history": [{"pub": old_pub, "fp": old_fp,
                           "from": "t0", "to": "t1",
                           "rotated_by_sig": "sig"}]},
    ])
    send_mod.send(project, "recv", "retired hello", "seat-old")
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert f"RETIRED:{old_fp}" in out
    assert "retired hello" in out, "RETIRED prints in full, never withheld"
    assert "REFUSED" not in out
    assert not _quarantine_path(project).exists()


# ── g15.26 claim: a signed block from a row that NAMES no key reads
# ── UNKEYED <seat>, never FORGED (hypothesis:l4-a-sig-against-a-row-with-
# ── no-key-on-file-reads-unkeyed-never-forged). FORGED is reserved for a
# ── signature that FAILS against a key the row NAMES; an unkeyed row cannot
# ── refute its own signed bytes, so readers print UNKEYED like UNSIGNED --
# ── in full, never withheld, never REFUSED, under informational AND enforcing.


def _unkeyed_inbox(project, monkeypatch, body="unkeyed hello"):
    """Build a one-block SIGNED inbox whose from-seat's row NAMES no pubkey
    and no sig_scheme. The sig is genuine ed25519 (there IS a .key file); only
    the row is unkeyed, which is exactly the state a freshly rotated worktree
    post holds on MAIN until its merge-up carries the key."""
    send_mod.keygen(project, "seat-a")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a"},                 # names NO key -> UNKEYED
    ])
    send_mod.send(project, "recv", body, "seat-a")
    return project / ".agi" / "sessions" / "inbox" / "recv.md"


def test_unkeyed_row_signed_block_reads_unkeyed_not_forged(
        tmp_path, capsys, monkeypatch):
    """Claim (1): a signed block from a seat whose row names NO pubkey and NO
    sig_scheme reads `UNKEYED seat-a` -- never FORGED -- and prints in full
    under informational."""
    project = _project_with_comms(tmp_path, {"verify": "informational"})
    _unkeyed_inbox(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "UNKEYED seat-a" in out
    assert "unkeyed hello" in out, "UNKEYED prints in full, like UNSIGNED"
    assert "FORGED" not in out, "an unkeyed row must never read FORGED"
    assert "REFUSED" not in out


def test_unkeyed_row_not_withheld_under_enforcing(
        tmp_path, capsys, monkeypatch):
    """Claim (2): under comms.verify==enforcing an UNKEYED block prints in
    FULL. Only the EXACT label FORGED is withheld, so an unkeyed sender's
    signed dm is never lost at the one moment the channel matters -- read and
    peek share the ONE delivery path."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    _unkeyed_inbox(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert "UNKEYED seat-a" in out
    assert "unkeyed hello" in out, "an UNKEYED body must print under enforcing"
    assert "REFUSED" not in out, "UNKEYED is never refused"
    assert "FORGED" not in out
    assert not _quarantine_path(project).exists(), \
        "an UNKEYED block is never quarantined"


def test_unkeyed_row_peek_enforcing_prints_in_full(
        tmp_path, capsys, monkeypatch):
    """peek shares the SAME delivery path as read, so an UNKEYED block prints
    in full under peek + enforcing too (never quietly withheld)."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    _unkeyed_inbox(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.peek(project, "recv", wrap=160)
    out = capsys.readouterr().out
    assert "UNKEYED seat-a" in out
    assert "unkeyed hello" in out
    assert "REFUSED" not in out


def test_whois_sig_unkeyed_row_not_refused(tmp_path, monkeypatch):
    """Claim (2) whois half: a `--sig` on a row that names no key reports
    UNKEYED and is never REFUSED under enforcing -- the refusal is reserved
    for the EXACT label FORGED."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    send_mod.keygen(project, "seat-a")
    sig_line, canonical = _signed_send_and_canonical(project, "seat-a",
                                                     "recv", "whois me")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "session_ref": "seat-a"},  # no key
    ])
    rc, text = send_mod.whois(project, "seat-a", claim="seat-a",
                              source="refs/x", do_fetch=False,
                              sig_line=sig_line, msg_text=canonical)
    assert rc == send_mod.WHOIS_OK, rc       # claim axis, label off it
    assert "UNKEYED seat-a" in text
    assert "REFUSED" not in text, "an UNKEYED whois sig is never refused"
    assert "FORGED" not in text


def test_forged_still_fires_when_row_names_a_key(tmp_path, capsys,
                                                 monkeypatch):
    """The flip never lowers the guard: a tampered body, under a row that
    NAMES a pubkey, still reads FORGED (FORGED is reserved for a key the row
    names) and is still refused under enforcing. Regression anchor proving the
    UNKEYED carve-out is narrow."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    inbox, inbox_text, fp = _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert f"REFUSED FORGED from seat-a " in out, \
        "a row that NAMES a key but whose sig fails is still refused"
    assert "tampered!!" not in out
    assert _quarantine_path(project).read_text() == inbox_text


def test_absent_and_informational_print_identical_bytes(
        tmp_path, capsys, monkeypatch):
    """Clause (4): the SAME inbox under a comms block ABSENT and under
    verify:"informational" prints byte-identical output (both identical to
    today). The flip cannot change a byte until enforcing."""
    # pin ts so the two peeks carry identical timestamps.
    monkeypatch.setattr(send_mod, "_now",
                        lambda: "2026-09-11T00:00:00+00:00")
    project = _project_with_comms(tmp_path, None)   # abscomms block first
    _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.peek(project, "recv", wrap=160)        # absent block
    absent_out = capsys.readouterr().out
    # flip the SAME project to verify:"informational" and peek again; peek
    # never advances the read cursor, so the inbox is byte-identical.
    (project / ".agi" / "config.json").write_text(json.dumps({
        "metric_primary": "outcome_coverage",
        "comms": {"verify": "informational", "lockdown": False},
    }))
    send_mod.peek(project, "recv", wrap=160)        # informational
    info_out = capsys.readouterr().out
    assert absent_out == info_out, \
        "informational must be byte-identical to an absent comms block"
    assert "tampered!!" in absent_out, \
        "informational prints the FORGED body in full, like today"
    assert "REFUSED" not in absent_out


def test_quarantine_appends_never_truncates(tmp_path, capsys, monkeypatch):
    """Two refused blocks append to the SAME quarantine file — each is a
    fresh mode "a" open, never a rewrite, so nothing is ever lost."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    _forged_inbox_with_rows(project, monkeypatch, body="first forged")
    # a second forged block appended to the same unread inbox
    inbox_path = project / ".agi" / "sessions" / "inbox" / "recv.md"
    send_mod.send(project, "recv", "second message", "seat-a")
    inbox_path.write_text(
        inbox_path.read_text().replace("second message", "second forged"))
    # one read: BOTH blocks are unread (no marker yet), so both are refused
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    capsys.readouterr()
    q = _quarantine_path(project)
    qtext = q.read_text()
    assert qtext.count("first forged") == 1
    assert qtext.count("second forged") == 1
    assert qtext.count(send_mod.MSG_SEP) == 2, \
        "quarantine appends both RAW blocks, never truncating"


# ── g15.26 P1 (F3): quarantine DEDUPES by the sha256 of the block's raw
# ── bytes (hypothesis:l4-quarantine-dedupes-by-block-hash...). peek never
# ── advances the read cursor, so a repeated peek of one FORGED block must
# ── NOT grow the quarantine by one identical copy per call -- the quarantine
# ── is the durable RECORD of what was withheld, not an append event log.
# ── One distinct block is kept once; the REFUSED line still prints every
# ── event; and `read` still advances the cursor past a withheld block (the
# ── inbox drains; the quarantine holds the copy).


def test_peek_enforcing_n_peeks_of_one_forged_leave_one_copy(
        tmp_path, capsys, monkeypatch):
    """N peeks of one FORGED block keep EXACTLY ONE copy in the quarantine
    (deduped by block hash), while every peek still prints its REFUSED line
    and pins the SAME withheld path."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    inbox, inbox_text, fp = _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    path_str = None
    for _ in range(5):
        send_mod.peek(project, "recv", wrap=160)
        out = capsys.readouterr().out
        assert "tampered!!" not in out, "a FORGED body never prints"
        assert f"REFUSED FORGED from seat-a " in out, \
            "every peek still refuses the block"
        assert "withheld to " in out
        if path_str is None:
            path_str = out.split("withheld to ")[1].strip()
        else:
            assert out.split("withheld to ")[1].strip() == path_str, \
                "the refusal names the SAME withheld path every peek"
    q = _quarantine_path(project)
    qtext = q.read_text()
    assert qtext.count(send_mod.MSG_SEP) == 1, \
        "N peeks of one block leave exactly one copy in quarantine"
    assert qtext.count("tampered!!") == 1
    assert qtext == inbox_text, \
        "the retained copy is the block's inbox bytes verbatim"
    # the sidecar index holds exactly one hash line (append-only, one hex).
    hashes = _quarantine_path(project).with_suffix(".hashes")
    lines = hashes.read_text().splitlines()
    assert len(lines) == 1
    assert len(lines[0]) == 64, "the sidecar holds one sha256 hex per line"


def test_quarantine_distinct_forged_blocks_still_all_kept(
        tmp_path, capsys, monkeypatch):
    """Dedupe is by BYTES, not by quarantine slot: two DIFFERENT FORGED
    blocks (different hashes) are BOTH kept -- the never-lose guarantee of
    test_quarantine_appends_never_truncates is unchanged, only repeats of
    the SAME block are collapsed."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    _forged_inbox_with_rows(project, monkeypatch, body="first forged")
    inbox_path = project / ".agi" / "sessions" / "inbox" / "recv.md"
    send_mod.send(project, "recv", "second message", "seat-a")
    inbox_path.write_text(
        inbox_path.read_text().replace("second message", "second forged"))
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    capsys.readouterr()
    q = _quarantine_path(project)
    qtext = q.read_text()
    assert qtext.count("first forged") == 1
    assert qtext.count("second forged") == 1
    assert qtext.count(send_mod.MSG_SEP) == 2
    hashes = _quarantine_path(project).with_suffix(".hashes")
    assert len(hashes.read_text().splitlines()) == 2, \
        "two distinct blocks record two hashes"


def test_read_advances_cursor_past_withheld_block_copy_remains(
        tmp_path, capsys, monkeypatch):
    """Cursor decision, recorded (hypothesis clause (2)): `read` ADVANCES
    past a withheld FORGED block -- the inbox drains so the same bytes are
    never re-refused/re-appended on the next read, while the quarantine keeps
    the one copy as the durable record. A second read reports empty and does
    not grow the quarantine."""
    project = _project_with_comms(tmp_path, {"verify": "enforcing"})
    inbox, inbox_text, fp = _forged_inbox_with_rows(project, monkeypatch)
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.read(project, "recv", None)
    out = capsys.readouterr().out
    assert f"REFUSED FORGED from seat-a " in out
    q = _quarantine_path(project)
    assert q.read_text().count(send_mod.MSG_SEP) == 1
    # the read consumed the withheld block: a second read sees an empty inbox
    send_mod.read(project, "recv", None)
    out2 = capsys.readouterr().out
    assert "empty" in out2, "read advanced past the withheld block"
    assert q.read_text().count(send_mod.MSG_SEP) == 1, \
        "the second read does not re-append the already-whithheld block"
    assert q.read_text() == inbox_text, \
        "the one retained copy is still the exact inbox bytes"


def test_lockdown_requirements_named_seam():
    """The requirement list is the reserved seam -- named, asserts nothing is
    built yet."""
    reqs = send_mod._lockdown_requirements({"custodian": True})
    assert reqs == ["encrypted-at-rest", "custodian-signing-server: optional"]
    # same list regardless of any unrelated config key
    assert send_mod._lockdown_requirements({}) == reqs


def test_lockdown_true_send_is_byte_identical_and_warns_once(
        tmp_path, capsys):
    """lockdown:true changes NO bytes on the wire vs lockdown:false (except
    ts), prints exactly one warning per send, and never prints 'encrypted' as
    a STATE."""
    locked = _project_with_comms(tmp_path, {"lockdown": True})
    plain = _project_with_comms(tmp_path, {"lockdown": False})

    send_mod.send(locked, "director", "secret hello", "a00-xxxx")
    send_mod.send(plain, "director", "secret hello", "a00-xxxx")

    locked_inbox = (locked / ".agi" / "sessions" / "inbox" / "director.md").read_text()
    plain_inbox = (plain / ".agi" / "sessions" / "inbox" / "director.md").read_text()
    # identical except the ts line
    assert _strip_ts(locked_inbox) == _strip_ts(plain_inbox)
    # the flag encrypts nothing: the wire bytes carry no claim of a cipher
    assert "encrypted" not in locked_inbox
    assert "enc:v1" not in locked_inbox  # unsigned send stays unsigned
    err = capsys.readouterr().err
    # exactly one warning per send (only the locked project sent a warning)
    assert err.count("comms.lockdown is set") == 1
    assert "WARNING: comms.lockdown is set but lockdown is NOT BUILT" in err


def test_lockdown_false_and_absent_print_no_warning(tmp_path, capsys):
    """Warning appears never under false or absent block."""
    plain = _project_with_comms(tmp_path, {"lockdown": False})
    absent = _project_with_comms(tmp_path, None)
    send_mod.send(plain, "director", "x", "a00-xxxx")
    send_mod.send(absent, "director", "x", "a00-xxxx")
    err = capsys.readouterr().err
    assert "comms.lockdown" not in err


def test_lockdown_help_mentions_reserved(capsys):
    """Clause 4: send -h and keygen -h mention comms.lockdown and reserved,
    so the reserved flag is discoverable without reading source."""
    with pytest.raises(SystemExit):
        send_mod.main(["--help"])
    out = capsys.readouterr().out
    assert "comms.lockdown" in out
    assert "reserved" in out.lower()

    with pytest.raises(SystemExit):
        send_mod.main(["keygen", "--help"])
    out = capsys.readouterr().out
    assert "comms.lockdown" in out
    assert "reserved" in out.lower()


def test_lockdown_read_and_peek_warn_once(tmp_path, capsys):
    """read and peek each print exactly one warning under lockdown:true."""
    locked = _project_with_comms(tmp_path, {"lockdown": True})
    send_mod.send(locked, "director", "secret hello", "a00-xxxx")
    capsys.readouterr()  # drain the send's warning
    send_mod.read(locked, "director", "a00-xxxx")
    send_mod.peek(locked, "director", wrap=160)
    err = capsys.readouterr().err
    assert err.count("comms.lockdown is set") == 2  # one per read, one per peek


def test_lockdown_every_dm_room_verb_warns_once(tmp_path, capsys):
    """SL7.02 clause (2): each dm/room verb -- send_dm, send_room, read_dm,
    peek_dm, read_room, peek_room -- prints the SAME single warning through the
    SAME helper, exactly once per verb call under lockdown:true, and never a
    second copy of the text."""
    locked = _project_with_comms(tmp_path, {"lockdown": True})
    capsys.readouterr()  # nothing printed yet

    send_mod.send_dm(locked, "director", "kid-a", "hi dm", "kid-a")
    send_mod.send_room(locked, "tier2-directors", "hi room", "kid-a")
    send_mod.read_dm(locked, "director", "kid-a", None, "kid-a")
    send_mod.peek_dm(locked, "director", "kid-a", None)
    send_mod.read_room(locked, "tier2-directors", "director", None, "director")
    send_mod.peek_room(locked, "tier2-directors", "director", None)

    err = capsys.readouterr().err
    assert err.count("comms.lockdown is set") == 6  # exactly one per verb


def test_lockdown_absent_dm_room_verbs_print_no_warning(tmp_path, capsys):
    """Bare comms root (no project config) falls through with NO warning."""
    bare = tmp_path / "comms"
    send_mod.send_dm(bare, "director", "kid-a", "hi", "kid-a")
    send_mod.send_room(bare, "tier2-directors", "hi", "kid-a")
    send_mod.read_dm(bare, "director", "kid-a", None, "kid-a")
    send_mod.peek_dm(bare, "director", "kid-a", None)
    send_mod.read_room(bare, "tier2-directors", "director", None, "director")
    send_mod.peek_room(bare, "tier2-directors", "director", None)
    err = capsys.readouterr().err
    assert "comms.lockdown" not in err



# ════════════════════════════════════════════════════════════════════════════
# g15.26 hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-
# and-every-key-cell-writer-commits-and-pushes-its-own-row
#
# Clause (1): _load_rows falls back per-seat to MAIN's COMMITTED row (git show
# HEAD) when the PUSHED row names no key; a pushed row WITH a key stays
# authoritative. Clause (2): every key-cell writer (keygen) commits its own-row
# hunk through _commit_spawn_row and pushes the season branch; a failed push
# never fails the mint. Clause (3): the VERIFIED label names main-committed.
# These use REAL git fixtures (a bare remote for the push leg) -- send.py's own
# subprocess is restored to the real one while tmux stays faked, so nothing
# touches a live tmux session.
# ════════════════════════════════════════════════════════════════════════════


class _GitAllowFakeTmux:
    """Allows REAL git subprocess (clause-1 committed-row read + clause-2
    commit/push) while faking tmux exactly as `_no_real_tmux` does, so no test
    runs a live tmux command. Overrides the autouse `send_mod.subprocess`
    stand-in (LIFO) only for the tests that need git."""
    TimeoutExpired = subprocess.TimeoutExpired

    def run(self, cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return subprocess.CompletedProcess(cmd, 1)
        return subprocess.run(cmd, *a, **k)


def _git_project(tmp_path, rows, branch="season/s2", comms=None):
    """A REAL git repo (top = root) whose graph root carries a COMMITTED
    posts.md row set — MAIN's HEAD authority. Returns the project root, the
    root the send/read/client code resolves (has `.agi/config.json`)."""
    root = tmp_path / "proj"
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    cfg = {"metric_primary": "x"}
    if comms is not None:
        cfg["comms"] = comms
    (root / ".agi" / "config.json").write_text(json.dumps(cfg))
    (root / ".agi" / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md(rows))
    (root / ".agi" / "sessions" / "inbox").mkdir(parents=True, exist_ok=True)
    (root / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", "-b", branch, str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                   check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m",
                    "committed seats seed"], check=True)
    return root


def _seat_key_write(root, seat, priv_hex):
    """Write a seat key file directly (so a test can control WHICH private key
    signs), in send.py's exact JSON shape."""
    kp = send_mod._seat_key_path(root, seat)
    kp.parent.mkdir(parents=True, exist_ok=True)
    kp.write_text(json.dumps({"scheme": "ed25519", "priv_hex": priv_hex}))


def test_falsifier1_rotation_alert_verifies_main_committed_under_enforcing(
        tmp_path, capsys, monkeypatch):
    """g15.26 clause (1) FALSIFIER + ROTATION-ALERT, real git fixture: a
    freshly first-minted post's row on origin is still UNKEYED (the hourly
    push has not run), but MAIN's COMMITTED row IS keyed. Its signed
    rotation-alert must read `VERIFIED seat-a (ed25519, main-committed)`
    under comms.verify=enforcing on the RECIPIENT side -- never UNKEYED,
    never FORGED, never REFUSED, never withheld."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    root = _git_project(tmp_path, [{"name": "seat-a"}], branch="season/s2",
                        comms={"verify": "enforcing"})
    # first-mint: the unkeyed row mints its key AND commits it onto MAIN's
    # HEAD (clause 2) -- so HEAD is keyed while origin is still unkeyed.
    path = send_mod.keygen(root, "seat-a")
    assert path is not None, "the first mint must succeed"
    # origin's pushed row is still UNKEYED -- the pre-push authority.
    _stub_seat_rows(monkeypatch, [{"name": "seat-a"}])
    capsys.readouterr()                      # drain keygen/send stdout
    send_mod.send(root, "recv", "rotation-alert", "seat-a")
    capsys.readouterr()                      # drain send stdout
    send_mod.read(root, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED seat-a (ed25519, main-committed)" in out, out
    assert "rotation-alert" in out, "the alert prints in full, never withheld"
    assert "REFUSED" not in out and "withheld" not in out


def test_falsifier2_pushed_key_stays_authoritative_over_stale_main(
        tmp_path, capsys, monkeypatch):
    """g15.26 clause (1) FALSIFIER: a pushed row that DOES name a key stays
    authoritative -- MAIN's committed row names a DIFFERENT key B, but a sig
    under B must NOT verify (the pushed key A wins), so B's sig reads FORGED.
    A stale MAIN key never overrides origin, and no `main-committed` tag fires
    because the fallback did not."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    scheme = send_mod.seatsig.get("ed25519")
    priv_a, pub_a = scheme.keygen()
    priv_b, pub_b = scheme.keygen()
    root = _git_project(
        tmp_path,
        [{"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_b.hex()}],
        branch="season/s2")
    # the PUSHED (authoritative) row names key A -- it has a key, so no
    # fallback to MAIN (which names key B).
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_a.hex()}])
    _seat_key_write(root, "seat-a", priv_b.hex())   # sender signs under B
    send_mod.send(root, "recv", "hello", "seat-a")
    capsys.readouterr()                      # drain send stdout
    send_mod.read(root, "recv", None)
    out = capsys.readouterr().out
    assert "FORGED" in out, out
    assert "main-committed" not in out


def test_keygen_commits_and_pushes_own_row_to_bare_remote(
        tmp_path, monkeypatch, capsys):
    """g15.26 clause (2): keygen (a key-cell writer) commits its own-row hunk
    onto MAIN's season branch and PUSHES it -- after keygen on a bare-remote
    fixture, ORIGIN's row carries the pubkey and MAIN's working tree is not
    dirty."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    root = _git_project(tmp_path, [{"name": "seat-a"}], branch="season/s2")
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin",
                    str(bare)], check=True)
    subprocess.run(["git", "-C", str(root), "push", "-u", "origin",
                    "season/s2"], check=True)
    capsys.readouterr()
    path = send_mod.keygen(root, "seat-a")
    assert path is not None
    capsys.readouterr()                      # drain keygen stdout/stderr
    # origin's season/s2 row now carries the pubkey.
    shown = subprocess.run(
        ["git", "-C", str(root), "show",
         "origin/season/s2:.agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True)
    assert "pubkey" in shown.stdout and "seat-a" in shown.stdout, shown.stdout
    # MAIN is not left dirty (sessions/ is gitignored).
    st = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == "", st.stdout


def test_keygen_mint_survives_a_failed_push(tmp_path, monkeypatch, capsys):
    """g15.26 clause (2): a failed push must NOT abort the mint -- with no
    origin remote, the push leg prints ONE line naming the remote error
    (to stderr) and keygen still returns the minted key path."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    root = _git_project(tmp_path, [{"name": "seat-a"}], branch="season/s2")
    capsys.readouterr()
    path = send_mod.keygen(root, "seat-a")
    assert path is not None, "a failed push must not abort the mint"
    assert send_mod._seat_key_path(root, "seat-a").is_file()
    err = capsys.readouterr().err
    assert "push: FAILED --" in err, err


# ── g15.26 clause (3) SEAM RULE (hypothesis:l4-keygen-exits-on-a-refused-row-
#    every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-
#    reads-forged): a sig under a freshly minted SUCCESSOR key, read while
#    ORIGIN still holds the PREDECESSOR key, is NOT FORGED -- the reader
#    consults MAIN's COMMITTED row (git show HEAD, never the dirty copy) and,
#    when that row's key verifies AND is strictly fresher in generation,
#    answers VERIFIED ... main-committed. A sig under no key anywhere stays
#    FORGED; a seat absent from MAIN's committed rows reads UNVERIFIABLE
#    (printed like UNSIGNED, never refused). ────────────────────────────────


def test_clause3_successor_key_verifies_main_committed(tmp_path, monkeypatch,
                                                       capsys):
    """Clause (3) SEAM: origin's pushed row holds PREDECESSOR key A while
    MAIN's COMMITTED row already carries SUCCESSOR key B at generation+1. A
    sig under B must read `VERIFIED seat-a (ed25519, main-committed)` -- the
    lagging-origin row never reads FORGED for a genuine successor signature."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    scheme = send_mod.seatsig.get("ed25519")
    priv_b, pub_b = scheme.keygen()                # MAIN committed successor
    priv_a, pub_a = scheme.keygen()                # origin pushed predecessor
    root = _git_project(
        tmp_path,
        [{"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_b.hex(),
          "generation": 2}],
        branch="season/s2")
    # the PUSHED (pre-push) authority still holds key A at generation 1.
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_a.hex(),
         "generation": 1}])
    _seat_key_write(root, "seat-a", priv_b.hex())  # sender signs under B
    send_mod.send(root, "recv", "hello", "seat-a")
    capsys.readouterr()                            # drain send stdout
    send_mod.read(root, "recv", None)
    out = capsys.readouterr().out
    assert "VERIFIED seat-a (ed25519, main-committed)" in out, out
    assert "FORGED" not in out, out


def test_clause3_sig_under_third_key_reads_forged(tmp_path, monkeypatch,
                                                  capsys):
    """Clause (3) SEAM falsifier: origin holds key A, MAIN's committed row key
    B -- a sig under a THIRD key C verifies under NO row anywhere and must
    still read FORGED, never VERIFIED, never UNVERIFIABLE."""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    scheme = send_mod.seatsig.get("ed25519")
    _pub_b, pub_b = scheme.keygen()                # MAIN committed row
    _pub_a, pub_a = scheme.keygen()                # origin pushed row
    priv_c, _pub_c = scheme.keygen()               # the third, unknown key
    root = _git_project(
        tmp_path,
        [{"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_b.hex(),
          "generation": 2}],
        branch="season/s2")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_a.hex(),
         "generation": 1}])
    _seat_key_write(root, "seat-a", priv_c.hex())  # sender signs under C
    send_mod.send(root, "recv", "hello", "seat-a")
    capsys.readouterr()
    send_mod.read(root, "recv", None)
    out = capsys.readouterr().out
    assert "FORGED" in out, out
    assert "main-committed" not in out, out


def test_clause3_seat_absent_from_committed_reads_unverifiable(
        tmp_path, monkeypatch, capsys):
    """Clause (3) SEAM: the seat is NOT in MAIN's committed rows (its row is
    not on MAIN yet), so the seam cannot confirm or refute the sig -- it reads
    `UNVERIFIABLE seat-a (row not on origin yet)`, printed like UNSIGNED,
    never FORGED, never REFUSED. (A gitless root keeps the ordinary FORGED for
    a deterministically tampered/wrong sig: with no MAIN to lag against there
    is nothing to soften the verdict -- see the pre-existing forgery suite.)"""
    monkeypatch.setattr(send_mod, "subprocess", _GitAllowFakeTmux())
    scheme = send_mod.seatsig.get("ed25519")
    _pub_a, pub_a = scheme.keygen()                # origin pushed row
    priv_c, _pub_c = scheme.keygen()               # the unknown signer
    root = _git_project(
        tmp_path,
        [{"name": "seat-other", "sig_scheme": "ed25519",
          "pubkey": scheme.keygen()[1].hex(), "generation": 3}],
        branch="season/s2")
    _stub_seat_rows(monkeypatch, [
        {"name": "seat-a", "sig_scheme": "ed25519", "pubkey": pub_a.hex(),
         "generation": 1}])
    _seat_key_write(root, "seat-a", priv_c.hex())
    send_mod.send(root, "recv", "hello", "seat-a")
    capsys.readouterr()
    send_mod.read(root, "recv", None)
    out = capsys.readouterr().out
    assert "UNVERIFIABLE seat-a (row not on origin yet)" in out, out
    assert "FORGED" not in out, out
    assert "REFUSED" not in out, out
