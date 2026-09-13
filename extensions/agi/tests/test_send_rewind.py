"""Tests for send.py rewind_read_cursors (hypothesis:l4-a-re-seat-after-a-dead-
predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time).

A re-seat after a DEAD predecessor rewinds the post's read cursors to the dead
session's seating time, so the re-seat's STARTUP [inbox] re-carries what the
killed session consumed. Proves, on tmp paths only (never the live checkout):
  (1) cursor 12, since_ts before the last two messages -> 10;
  (2) a cursor already at/below the re-count -> untouched;
  (3) another participant's key in the SAME state file is intact;
  (4) a room state WITHOUT the seat key is untouched; one WITH it is rewound;
  (5) dry_run returns the changes but writes NO state file.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402  (resolves through BIN, already on sys.path)

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project so locations.resolve works."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


def _make_conv(root, rel: str, n_blocks: int, start_i: int = 1):
    """Write a conversation file with `n_blocks` blocks whose ts are
    `2026-09-12T09:00:{i:02d}Z` for i = start_i..start_i+n_blocks-1."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    text = ""
    for i in range(start_i, start_i + n_blocks):
        ts = f"2026-09-12T09:00:{i:02d}Z"
        text += send_mod._block(ts, "other", "seat", f"msg-{i}")
    p.write_text(text, encoding="utf-8")
    return p


def _state(p, d):
    Path(str(p) + send_mod.STATE_SUFFIX).write_text(json.dumps(d),
                                                     encoding="utf-8")


SINCE = "2026-09-12T09:00:11Z"   # after messages 1..10, at message 11


def test_rewind_lowers_a_high_cursor_to_the_since_count(project):
    """(1) 12 messages, cursor 12, since before the last two -> cursor 10."""
    p = _make_conv(project, "dm/conv1.md", 12)
    _state(p, {"seat": 12})
    changes = send_mod.rewind_read_cursors(project, "seat", SINCE)
    assert changes == [("conv1.md", 12, 10)], changes
    state = json.loads(Path(str(p) + send_mod.STATE_SUFFIX).read_text())
    assert state["seat"] == 10


def test_rewind_leaves_a_cursor_already_lower_untouched(project):
    """(2) cursor 5 is already below the 10 older messages -> untouched."""
    p = _make_conv(project, "dm/conv2.md", 12)
    _state(p, {"seat": 5})
    assert send_mod.rewind_read_cursors(project, "seat", SINCE) == []
    state = json.loads(Path(str(p) + send_mod.STATE_SUFFIX).read_text())
    assert state["seat"] == 5


def test_rewind_keeps_other_participant_key_intact(project):
    """(3) the other participant's key in the SAME state file is untouched."""
    p = _make_conv(project, "dm/conv3.md", 12)
    _state(p, {"seat": 12, "other": 7})
    changes = send_mod.rewind_read_cursors(project, "seat", SINCE)
    assert changes == [("conv3.md", 12, 10)], changes
    state = json.loads(Path(str(p) + send_mod.STATE_SUFFIX).read_text())
    assert state["seat"] == 10
    assert state["other"] == 7


def test_rewind_skips_room_without_seat_key_and_rewinds_one_with_it(project):
    """(4) a room state that does NOT carry the seat key is untouched; a room
    keyed on the seat IS rewound. Both are rooms, so favours the falsifier."""
    rp = _make_conv(project, "room/room1.md", 12)
    _state(rp, {"other": 9})                      # no seat key -> skip
    rp2 = _make_conv(project, "room/room2.md", 12)
    _state(rp2, {"seat": 12})                     # seat key -> rewind
    changes = send_mod.rewind_read_cursors(project, "seat", SINCE)
    names = {c[0] for c in changes}
    assert names == {"room2.md"}, changes
    assert json.loads(Path(str(rp) + send_mod.STATE_SUFFIX).read_text()) \
        == {"other": 9}                            # room1 untouched
    assert json.loads(Path(str(rp2) + send_mod.STATE_SUFFIX).read_text()) \
        ["seat"] == 10


def test_rewind_dry_run_returns_changes_and_writes_nothing(project):
    """(5) dry_run returns the would-rewind changes but writes NO state."""
    p = _make_conv(project, "dm/conv5.md", 12)
    _state(p, {"seat": 12})
    changes = send_mod.rewind_read_cursors(project, "seat", SINCE,
                                           dry_run=True)
    assert changes == [("conv5.md", 12, 10)], changes
    state = json.loads(Path(str(p) + send_mod.STATE_SUFFIX).read_text())
    assert state["seat"] == 12                      # not written