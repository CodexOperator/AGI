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
    inbox = project / "sessions" / "inbox" / "director.md"
    assert inbox.is_file()
    content = inbox.read_text()
    assert "hello world" in content
    assert "from: a00-xxxx" in content
    assert "to: director" in content


def test_send_prints_inbox_path(project: Path, capsys):
    send_mod.send(project, "test-agent", "message one", "parent")
    captured = capsys.readouterr()
    expected = str((project / "sessions" / "inbox" / "test-agent.md").resolve())
    assert captured.out.strip() == expected


# ── hypothesis:l3w4-seat-transport: best-effort tmux nudge ───────────────


def _fake_tmux(monkeypatch, window_names):
    """Fake subprocess.run so send can nudge without a live tmux; records
    every tmux invocation. `window_names` are returned by list-windows."""
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="\n".join(window_names),
                                               stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    return calls


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
    calls = _fake_tmux(monkeypatch, ["director"])
    send_mod.send(project, "director", "hello world", "a00-xxxx")
    nudges = [c for c in calls if c[:2] == ["tmux", "send-keys"]]
    assert nudges, "expected a nudge to the director's tmux window"
    assert nudges[0][:4] == ["tmux", "send-keys", "-t", "agi-rc:director"]
    assert nudges[0][4] == "hello world"
    assert nudges[0][5] == "Enter"
    # the inbox contract is unchanged
    assert (project / "sessions" / "inbox" / "director.md").is_file()


def test_send_dm_nudges_other_party(project: Path, monkeypatch):
    calls = _fake_tmux(monkeypatch, ["adv-alive"])
    send_mod.send_dm(project, "mee", "adv-alive", "psst", "mee")
    nudges = [c for c in calls if c[:2] == ["tmux", "send-keys"]]
    assert nudges
    assert nudges[0][3] == "agi-rc:adv-alive"


def test_send_skips_nudge_when_no_window(project: Path, monkeypatch):
    calls = _fake_tmux(monkeypatch, [])  # an empty/absent window listing
    send_mod.send(project, "ephemeral-kid", "fire and forget", "parent")
    assert not any(c[:2] == ["tmux", "send-keys"] for c in calls)
    inbox = project / "sessions" / "inbox" / "ephemeral-kid.md"
    assert inbox.is_file()
    assert "fire and forget" in inbox.read_text()


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
    content = (project / "sessions" / "inbox" / "agent-x.md").read_text()
    assert "ts: " in content


def test_message_has_from_to_and_text(project: Path):
    send_mod.send(project, "recip", "the message body", "sender-id")
    content = (project / "sessions" / "inbox" / "recip.md").read_text()
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
    inbox = project / "sessions" / "inbox" / "prime.md"
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
    assert not (project / "sessions" / "inbox" / "prime.md").exists()


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
    assert (project / "sessions" / "inbox" / "prime.md").is_file()


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
    inbox = root / "sessions" / "inbox" / "prime.md"
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
