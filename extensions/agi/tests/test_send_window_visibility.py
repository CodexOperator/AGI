"""An UNREADABLE tmux listing is never reported as a window that is gone
(hypothesis:g1-send-says-cannot-list-windows-never-window-gone).

MEASURED 18:1xZ 10-01 (DG5): the live tmux server's socket dir /tmp/tmux-1000
is mode 0700 under another uid, so every director seat's `tmux list-windows`
fails (`error connecting to ... (Permission denied)`, rc != 0). send.py turned
that failure into `[]` and then printed a confident false statement about a
LIVE sanctuary-master: "row window @5 is gone and no window named
sanctuary-master is listed". The Prime DECLINED opening the socket, so the code
half is this round: the listing's readability must be a SEPARATE answer from
its contents.

Two fixtures drive the whole file:
  * `_fake_tmux_unreadable` -- every list-windows returns rc 1 (EACCES / no
    server). This is what the box actually did.
  * `_fake_tmux(monkeypatch, names)` -- today's readable fake: rc 0 and the
    given windows. The ABSENT case (rc 0, the target not listed) must keep its
    `gone` wording, or the fix would have silenced a true statement.

No live tmux, no MAIN comms: `subprocess.run` is monkeypatched in-process.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import send as send_mod  # noqa: E402

from test_send import _fake_tmux, _seats_md, _typed  # noqa: E402

EACCES_STDERR = ("error connecting to /tmp/tmux-1000/default "
                 "(Permission denied)")


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


def _write_seats(project: Path, rows):
    (project / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(_seats_md(rows))


def _fake_tmux_unreadable(monkeypatch, sleep_calls=None):
    """list-windows can NEVER be read (rc 1, the EACCES stderr) -- what a
    seat outside the socket dir's mode 0700 sees. Everything else is rc 0."""
    calls = []
    recorded = [] if sleep_calls is None else sleep_calls

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 1, stdout="",
                                              stderr=EACCES_STDERR)
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: recorded.append(s))
    return calls


# ── FALSIFIER 1: unreadable listing never prints `gone` ────────────────────

def test_unreadable_listing_is_never_reported_as_gone(project, monkeypatch,
                                                      capsys):
    """A stale @id whose listing could not be READ: send.py says it cannot
    list, and the words `is gone` / `no window named` appear NOWHERE."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "sanctuary-master", "role": "master",
                            "window": "@5", "pid": 424242}])
    calls = _fake_tmux_unreadable(monkeypatch)
    send_mod.send(project, "sanctuary-master", "body", "prime")
    err = capsys.readouterr().err
    assert "cannot list windows" in err, err
    for forbidden in ("is gone", "no window named", "nudge repair"):
        assert forbidden not in err, \
            f"an UNREADABLE listing printed {forbidden!r}: {err}"


def test_unreadable_listing_never_types_into_the_blind(project, monkeypatch,
                                                       capsys):
    """MEASURED 20:5xZ 10-01 (DG5, TMUX_TMPDIR on a mode-000 dir): with the
    socket dir unreadable, `tmux list-windows` rc=1 AND `tmux send-keys` rc=1
    with the SAME stderr -- so keeping the row's @id as a "best effort" target
    buys NOTHING; the landed arm returns None and is right. This test pins
    that: no send-keys at all on an unreadable box."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "sanctuary-master", "role": "master",
                            "window": "@5", "pid": 424242}])
    calls = _fake_tmux_unreadable(monkeypatch)
    send_mod.send(project, "sanctuary-master", "body", "prime")
    capsys.readouterr()
    assert _typed(calls) == [], \
        "an unreadable tmux server cannot be typed into either -- no send-keys"


def test_unreadable_listing_still_writes_the_message(project, monkeypatch):
    """The dm is the record and the file sweep is the delivery: unreadable
    tmux costs the WAKE, never the message."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "sanctuary-master", "role": "master",
                            "window": "@5", "pid": 424242}])
    _fake_tmux_unreadable(monkeypatch)
    send_mod.send(project, "sanctuary-master", "body", "prime")
    inbox = project / ".agi" / "sessions" / "inbox" / "sanctuary-master.md"
    assert inbox.exists() and "body" in inbox.read_text()


def test_rowless_recipient_stays_a_silent_no_op(project, monkeypatch, capsys):
    """A recipient with NO ROW at all keeps the silent no-op it has always had:
    there is no CLAIMED window to be wrong about, and an unreadable box must
    not become a per-tick stderr flood (the contract test
    test_read_refuses_a_target_that_is_not_you pins stderr to one line for
    exactly this shape)."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "director", "role": "director",
                            "window": "@246", "pid": 424242}])
    _fake_tmux_unreadable(monkeypatch)
    resolved = send_mod._nudge_target(project, "no-such-seat", None)
    assert resolved is None
    assert capsys.readouterr().err == ""


def test_empty_window_cell_says_cannot_list_not_gone(project, monkeypatch,
                                                     capsys):
    """A row whose `window` cell is EMPTY still CLAIMED a window, so an
    unreadable box is named -- `cannot list`, never `gone`. This is the ONE
    place my parked implementation and the landed one differ: I keyed the line
    on `stale_ref` (so this shape stayed silent) and DG2 keyed it on the row's
    CLAIMED ref. DG2 is right -- the READER is what is unreadable, and saying
    so costs one line per send. This test pins the landed semantics."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "director", "role": "director",
                            "window": "", "pid": 424242}])
    _fake_tmux_unreadable(monkeypatch)
    resolved = send_mod._nudge_target(project, "director", None)
    assert resolved is None
    err = capsys.readouterr().err
    assert "cannot list windows" in err, err
    assert "is gone" not in err, err


def test_list_windows_returns_none_when_unreadable_and_a_list_when_read(
        project, monkeypatch):
    """The seam itself: None == could not look, [] == looked and it is not
    there. A falsifier that cannot tell the two apart is not a falsifier."""
    _fake_tmux_unreadable(monkeypatch)
    assert send_mod._list_windows("agi") is None
    _fake_tmux(monkeypatch, [])
    assert send_mod._list_windows("agi") == []
    _fake_tmux(monkeypatch, ["@246", "director"])
    assert send_mod._list_windows("agi") == ["@246", "director"]


# ── FALSIFIER 2: the TRUE `gone` case must survive ────────────────────────

def test_readable_listing_without_the_target_still_says_gone(project,
                                                             monkeypatch,
                                                             capsys):
    """rc 0 and the target absent: `gone` is TRUE here and must keep being
    said (clause b: never silent). A fix that silences it is not a fix."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "sanctuary-master", "role": "master",
                            "window": "@5", "pid": 424242}])
    _fake_tmux(monkeypatch, ["some-other-window"])
    resolved = send_mod._nudge_target(project, "sanctuary-master", None)
    assert resolved is None
    err = capsys.readouterr().err
    assert "nudge repair: sanctuary-master row window @5 is gone" in err, err
    assert "cannot list windows" not in err, err


def test_readable_listing_without_the_name_never_targets_it(project,
                                                            monkeypatch):
    """rc 0 and the NAME absent: no send-keys at all."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [{"name": "director", "role": "director",
                            "window": "", "pid": 424242}])
    calls = _fake_tmux(monkeypatch, ["some-other-window"])
    assert send_mod._nudge_target(project, "director", None) is None
    assert _typed(calls) == []
