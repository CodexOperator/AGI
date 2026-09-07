"""Tests for bin/send.py — one-verb agent comms.

Design source: .agi/context/season-ladder-and-morals-brief.md §2 (Comms).
The testable claim: a send then read returns the block once and peek still
shows it; two senders interleave without loss.
"""
from __future__ import annotations

import importlib.util
import json
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
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "need a ruling on g7", None, False)
    inbox = project / "sessions" / "inbox" / "prime.md"
    assert inbox.is_file()
    content = inbox.read_text()
    assert "to: prime" in content
    assert "need a ruling on g7" in content


def test_audience_one_per_rotation(project: Path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_AGENT_ID", "parent-y")
    monkeypatch.setenv("AGI_LOOP", "L3.02@1")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "first", None, False)
    with pytest.raises(SystemExit):
        send_mod.audience_prime(croot, project, "second", None, False)


def test_audience_morals_bypasses_gate(project: Path, monkeypatch):
    """--morals bypasses the one-per-rotation gate."""
    monkeypatch.setenv("AGI_AGENT_ID", "parent-z")
    monkeypatch.setenv("AGI_LOOP", "L3.02@1")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "one", None, False)
    send_mod.audience_prime(croot, project, "two-morals", None, True)  # passes


def test_audience_rule_printed_back(project: Path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_AGENT_ID", "parent-q")
    croot = project / "comms"
    send_mod.audience_prime(croot, project, "please", None, False)
    captured = capsys.readouterr()
    assert "inbox-only" in captured.out
    assert "one audience per sender per rotation" in captured.out


# ── red-first: --from && --comms-root are honored BEFORE the subcommand ──


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
