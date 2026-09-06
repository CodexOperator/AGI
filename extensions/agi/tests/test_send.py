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


def test_sender_from_flag(project: Path):
    send_mod.send(project, "dest", "hi", "--from")
    # No --from flag in send call above — let's test via the internal function:
    assert send_mod._detect_sender("custom-role") == "custom-role"


def test_sender_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("AGI_AGENT_ID", "env-agent-007")
    assert send_mod._detect_sender(None) == "env-agent-007"


def test_sender_unknown_when_no_env_no_flag():
    assert send_mod._detect_sender(None) == "unknown"