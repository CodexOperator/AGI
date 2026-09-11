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
            return _fixture_text("claude_pane_busy.txt")
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


def test_stranded_token_is_submitted_by_a_bare_enter(project: Path,
                                                     monkeypatch, capsys):
    """Probe (C) as the heal: an IDLE pane already holding the token
    unsubmitted (the old shape left it there) gets ONE bare Enter -- no
    second token, no body -- the stranded wake is delivered and the marker
    stamped. Without it every later send coalesces forever on that pane."""
    pane = _FixturePane(width=60)
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])      # stranded, wrapped
    assert pane.submitted == []
    calls = _fake_tmux_pane(monkeypatch, ["sanctuary-director"], pane, [])
    send_mod.send(project, "sanctuary-director", "the body", "kid")
    assert _typed(calls) == [], "no second token into a pane holding one"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               "agi-rc:sanctuary-director", "Enter"]]
    assert pane.submitted == [_OLD_TOKEN + "\n"] and pane.input == ""
    assert "submitted a stranded token" in capsys.readouterr().err
    assert send_mod._last_nudge_age(project, "sanctuary-director") is not None


def test_stranded_token_in_a_busy_pane_gets_no_enter(project: Path,
                                                     monkeypatch, capsys):
    """The heal never types into a mid-turn pane: busy wins over stranded."""
    pane = _FixturePane(busy=True)
    pane.send_keys(["-t", "w", _OLD_TOKEN, "Enter"])
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
    assert [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]] \
        == [], "the retry must type NO second line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               "agi-rc:adv-alive", "Enter"]]
    assert pane.submitted == ["[nudge: mee]: first body"], pane.submitted
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
    assert [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]] \
        == [], "the dm must not type an inline line after the token"
    assert pane.submitted == [tok], pane.submitted
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
    assert [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]] \
        == [], "the dm must not type an inline line after rotation-alert"
    assert pane.submitted == ["[rotation-alert] changing seats"], \
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
    assert pane.submitted == ["[rotation-alert] rotating"], pane.submitted
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
    assert pane.submitted == ["[nudge: mee]: urgent"], pane.submitted
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
    assert [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]] \
        == [], "the new dm must not type a second line after the stranded one"
    assert pane.submitted == ["[nudge: mee]: older body"], pane.submitted
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
    assert _typed(calls) == [], "nothing new typed after the own stranded line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line], pane.submitted
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
    assert _typed(calls) == [], "nothing new typed after the own stranded line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line], pane.submitted
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
    assert _typed(calls) == [], "nothing new typed after the own stranded line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line], pane.submitted
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
    assert _typed(calls) == [], \
        "the own stranded deferred line must not be typed again"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls2) == [], \
        "the own stranded deferred line must not be typed again"
    assert _enters(calls2) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls2
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls) == [], "nothing new typed after the own stranded line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line], pane.submitted
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
    assert _typed(calls) == [], "no second line after the own stranded line"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]]
    assert pane.submitted == [line], pane.submitted
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
    """Falsifier (3): a row that carries a window @id must be addressed by
    @id, never by name — a namesake/predecessor window has a different @id.

    HERMETIC: the fixture row's pid would stat ~/.claude/sessions/<pid>.json
    on the host, an ambient home-dir read that must not decide this test
    (fixture-leak). Neutralized: registry status is forced None so the test
    deterministically falls to the capture-pane fake."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@246", "pid": 424242}]))
    # NB the fake lists a window that shares the seat NAME but not its @id;
    # the @id target must win and the name must never be addressed.
    calls = _fake_tmux(monkeypatch, ["sanctuary-director"])
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


def test_row_at_id_target_used_verbatim_without_listing(project: Path,
                                                        monkeypatch):
    """Residue 1b: a row whose `window` cell IS an @id is used verbatim as
    the target — the name is NEVER looked up — even when no window named like
    the id is listed."""
    (project / "nodes" / ".geometry").mkdir(parents=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([{"name": "sanctuary-director", "role": "director",
                    "window": "@250"}]))
    calls = _fake_tmux(monkeypatch, ["director"])   # no "@250" in listing
    send_mod.send(project, "sanctuary-director", "body", "kid")
    nudges = _typed(calls)
    assert nudges and nudges[0][4] == "agi-rc:@250", nudges


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
    assert _typed(calls) == [], \
        "the own TAILED truncated strand must not be typed again"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls) == [], "the own UNTAILED truncated strand retyped"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls) == [], \
        "a FOREIGN truncated strand must not be typed after"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls) == [], \
        "the own more=2 stratum must not be typed again at pending=3"
    assert _enters(calls) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls
    assert pane.submitted == [strand], pane.submitted
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
    assert _typed(calls2) == [], \
        "the retry must NOT type the already-delivered body a second time"
    assert _enters(calls2) == [["tmux", "send-keys", "-t",
                               f"agi-rc:{seat}", "Enter"]], calls2
    assert pane.submitted == [strand], pane.submitted
    # ONE delivery total: the single `[nudge:`-shaped line ever put in the box
    assert send_mod._read_deferred(root, seat) is None, \
        "the body was delivered -- the record is cleared, never typed twice"
