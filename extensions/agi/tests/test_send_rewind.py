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


def _croot(root):
    """The RESOLVED comms root (the module's own resolver), so dm/room fixture
    conversations land where production conversations actually live -- never
    under `root/dm` / `root/room`, which rewind_read_cursors would never see."""
    return send_mod.comms_root(root)


def _make_conv(root, rel: str, n_blocks: int, start_i: int = 1):
    """Write a conversation file with `n_blocks` blocks whose ts are
    `2026-09-12T09:00:{i:02d}Z` for i = start_i..start_i+n_blocks-1. Written
    under the RESOLVED comms root (the production dm/room layout), never
    `root/dm` or `root/room`."""
    p = _croot(root) / rel
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


def test_rewind_reads_dm_under_the_comms_root_not_root_dm(project):
    """THE PRODUCTION SHAPE (the falsifier P-f): a dm state file carrying the
    seat key lives under `<graph>/comms/season-<N>/dm`, and `root/dm` never
    exists -- so a rewind that scanned `root/dm` would rewind NOTHING. Uses
    the module's own resolver to place the fixture, and asserts the legacy
    `root/dm` directory is absent to prove there is no other scan site."""
    croot = _croot(project)
    assert not (project / "dm").exists()            # no legacy root/dm at all
    p = _make_conv(project, "dm/conv6.md", 12)
    assert str(p).startswith(str(croot / "dm")), p
    _state(p, {"seat": 12})
    changes = send_mod.rewind_read_cursors(project, "seat", SINCE)
    assert changes == [("conv6.md", 12, 10)], changes
    state = json.loads(Path(str(p) + send_mod.STATE_SUFFIX).read_text())
    assert state["seat"] == 10


def _make_inbox(project: Path, seat: str, n_blocks: int,
                marker_after: int | None = None):
    """Write an inbox for `seat` with `n_blocks` messages ts 09:00:01.., and
    the READ_MARKER line after the first `marker_after` blocks (None = no
    marker, so all unread). The inbox lives at `_inbox_path`, the SAME path
    send.py `read` rewrites -- this is the exact gap the SM.03b slice must
    close (a seat inbox has NO `.state.json`; its cursor is the marker)."""
    p = send_mod._inbox_path(project, seat)
    p.parent.mkdir(parents=True, exist_ok=True)
    blocks = [send_mod._block(
        f"2026-09-12T09:00:{i:02d}Z", "other", seat, f"msg-{i}")
        for i in range(1, n_blocks + 1)]
    if marker_after is None:
        text = "".join(blocks)
    else:
        text = ("".join(blocks[:marker_after]) + send_mod.READ_MARKER
                + "".join(blocks[marker_after:]))
    p.write_text(text, encoding="utf-8")
    return p


def _assert_marker_after(p: Path, count: int):
    """Assert the READ_MARKER line sits after exactly `count` blocks (one
    `---` separator precedes every block)."""
    text = p.read_text()
    lines = text.splitlines(keepends=False)
    mi = lines.index(send_mod.READ_MARKER.rstrip("\n"))
    n = sum(1 for ln in lines[:mi] if ln == send_mod.MSG_SEP.rstrip("\n"))
    assert n == count, (n, count)


INBOX_SINCE = "2026-09-12T09:00:11Z"   # blocks 1..10 older, 11-12 at/after


def test_rewind_moves_inbox_marker_back_after_older_blocks(project):
    """(a) inbox marker after 12 blocks, since before the last two -> the
    marker now sits after 10: blocks 11-12 become UNREAD (re-carried by the
    re-seat STARTUP [inbox]); blocks 1-10 stay read."""
    p = _make_inbox(project, "seat", 12, marker_after=12)
    changes = send_mod.rewind_read_cursors(project, "seat", INBOX_SINCE)
    assert changes == [("seat.md", 12, 10)], changes
    _assert_marker_after(p, 10)
    unread, _ = send_mod._scan_messages(p)
    joined = "\n".join(unread)
    assert "msg-11" in joined and "msg-12" in joined, joined
    assert "msg-10" not in joined, joined      # exactly the last two re-carried


def test_rewind_never_advances_an_already_earlier_marker(project):
    """(b) a marker already BEFORE N (block 8 < 10 older) is untouched: a
    rewind must never move the read position FORWARD (that would silently
    mark unread mail as read). Byte-identical file, no change reported."""
    p = _make_inbox(project, "seat", 12, marker_after=8)
    before = p.read_bytes()
    assert send_mod.rewind_read_cursors(project, "seat", INBOX_SINCE) == []
    assert p.read_bytes() == before


def test_rewind_inbox_dry_run_returns_change_and_writes_nothing(project):
    """(c) dry_run reports the would-rewind change but writes NO bytes:
    the marker stays after 12."""
    p = _make_inbox(project, "seat", 12, marker_after=12)
    changes = send_mod.rewind_read_cursors(project, "seat", INBOX_SINCE,
                                           dry_run=True)
    assert changes == [("seat.md", 12, 10)], changes
    _assert_marker_after(p, 12)                 # on disk, marker still after 12


def test_rewind_leaves_a_no_marker_inbox_alone(project):
    """(e) an inbox with NO READ_MARKER (every block unread) is left alone:
    the rewind never invents a read position to lower."""
    p = _make_inbox(project, "seat", 12)
    before = p.read_bytes()
    assert send_mod.rewind_read_cursors(project, "seat", INBOX_SINCE) == []
    assert p.read_bytes() == before