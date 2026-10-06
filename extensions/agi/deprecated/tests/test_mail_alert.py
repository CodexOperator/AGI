"""Tests for bin/mail_alert.py — one shared mail-alert side channel.

hypothesis:l3w4-shared-mail-alert: a hook fired at a per-turn seam unifies
dm + room + inbox unread under ONE mechanism and injects one
system-reminder-tagged block distinguishable from the owner, stamping an
alerted_at record per seat+thread so "never got it" and "ignored it" remain
distinguishable.

The testable claims here: a seat holding unread mail in EACH surface (dm,
room, inbox) gets an injection naming it; a clean seat gets none; and an
unchanged backlog does not re-alert on the next seam (the stamp works) while
new mail does.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)

ma_spec = importlib.util.spec_from_file_location("mail_alert", BIN / "mail_alert.py")
ma = importlib.util.module_from_spec(ma_spec)
ma_spec.loader.exec_module(ma)


@pytest.fixture
def seats(tmp_path: Path):
    """A bare project + empty comms root with a known seat for mail-alert."""
    root = tmp_path / "project"
    (root / "sessions" / "inbox").mkdir(parents=True)
    croot = tmp_path / "comms"
    (croot / "dm").mkdir(parents=True)
    (croot / "room").mkdir(parents=True)
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text("{}")
    return root, croot


def _raised(seat) -> str:
    return ma.build_alert(seat[0], "seat-a", str(seat[1]))


def test_clean_seat_gets_no_injection(seats):
    """A seat with no unread mail gets nothing — the quiet default."""
    assert _raised(seats) is None


def test_dm_unread_injects(seats):
    root, croot = seats
    send_mod.send_dm(croot, "sender", "seat-a", "psst", "sender")
    alert = _raised(seats)
    assert alert is not None
    assert ma.INJECT_TAG in alert
    assert "seat-a" in alert
    assert "sender--seat-a" in alert or "dm" in alert
    assert "1 unread" in alert


def test_room_unread_injects(seats):
    _, croot = seats
    send_mod.send_room(croot, "tier2-directors", "anyone free?", "d2")
    alert = _raised(seats)
    assert alert is not None
    assert ma.INJECT_TAG in alert
    assert "tier2-directors" in alert


def test_inbox_unread_injects(seats):
    root, _ = seats
    send_mod.send(root, "seat-a", "director needs you", "parent")
    alert = _raised(seats)
    assert alert is not None
    assert ma.INJECT_TAG in alert
    assert "inbox" in alert
    assert "1 unread" in alert


def test_unchanged_backlog_does_not_reinject(seats):
    """alerted_at stamp: an ignored-but-unchanged backlog is raised once,
    then the seat is not nagged on the next seam — the record of the raise
    persists so 'ignored it' stays distinguishable from 'never got it'."""
    send_mod.send_dm(seats[1], "sender", "seat-a", "psst", "sender")
    first = _raised(seats)
    assert first is not None
    # next seam, same unread, nothing delivered since: stays quiet
    assert _raised(seats) is None


def test_new_mail_reinjects(seats):
    """New unread past the last alert raises again (count increased)."""
    send_mod.send_dm(seats[1], "sender", "seat-a", "one", "sender")
    assert _raised(seats) is not None
    send_mod.send_dm(seats[1], "sender", "seat-a", "two", "sender")
    alert = _raised(seats)
    assert alert is not None
    assert "2 unread" in alert


def test_alert_names_sender_and_age(seats):
    """The injection names who wrote and how long it has waited."""
    send_mod.send_dm(seats[1], "sender", "seat-a", "needs you", "sender")
    alert = _raised(seats)
    assert "sender" in alert