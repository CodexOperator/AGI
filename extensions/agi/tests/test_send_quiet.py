"""Tests for the QUIET-POSTS settings token (hypothesis:l4-quiet-posts-
a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-
refires-a-stale-marker-and-wake-repair-skips-the-row).

A config:posts/`config:seats` row whose `settings` cell carries the `quiet`
token: send still WRITES the dm but types NO nudge (no send-keys, no copy-
mode cancel, no pending/deferred nudge file, and never re-fires a stale
marker); heal wake-repair skips the row BY NAME (no pane capture); `status`
prints `quiet`; a NON-quiet row keeps every nudge/wake behavior byte-for-byte.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import send as send_mod  # noqa: E402  (heal lazily imports THIS module)
import rotate  # noqa: E402

from test_send import (  # noqa: E402
    _enters,
    _fake_tmux,
    _seats_md,
    _typed,
)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


def _quiet_row(**extra):
    row = {"name": "director", "role": "director",
           "window": "@246", "pid": 424242}
    row.update(extra)
    return row


def _write_seats(project: Path, rows):
    (project / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(_seats_md(rows))


# (a) send quiet row -> inbox written, tmux fake untouched (no send-keys).
def test_send_quiet_row_writes_inbox_but_no_nudge(project, monkeypatch):
    _write_seats(project, [_quiet_row(settings="quiet")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "secret body", "kid")
    inbox = project / ".agi" / "sessions" / "inbox" / "director.md"
    assert "secret body" in inbox.read_text()
    assert _typed(calls) == [], "quiet row must type NO nudge token"
    assert _enters(calls) == [], "quiet row must type NO Enter"
    assert all(c[:2] != ["tmux", "capture-pane"] for c in calls), \
        "quiet row must not be capture-pane probed for a nudge"


# (b) stale marker on a quiet row -> no re-fire, marker untouched.
def test_wake_quiet_row_never_refires_stale_marker(project, monkeypatch):
    _write_seats(project, [_quiet_row(settings={"quiet": True})])
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    inbox = project / ".agi" / "sessions" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    marker = inbox / "director.nudge"
    marker.write_text("1")  # a stale marker (age well past the window)
    assert send_mod.wake(project, "director") is False
    assert marker.read_text() == "1", "stale marker must not be re-stamped"
    assert _typed(calls) == [] and _enters(calls) == []
    assert [c[:2] for c in calls] != [["tmux", "capture-pane"]]


# (c) heal wake-repair skips a quiet row by name (no pane capture).
def test_wake_repair_skips_quiet_row(project, monkeypatch):
    import heal as heal_mod  # noqa: PLC0415
    _write_seats(project, [_quiet_row(settings="quiet")])
    calls = []

    def fake_run(cmd, capture_output=None, text=False, timeout=None):
        calls.append(cmd)
        return __import__("subprocess").CompletedProcess(
            cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    heal_mod._repair_stranded_wakes(project)
    assert all(c[:2] != ["tmux", "capture-pane"] for c in calls), \
        "quiet row must not be capture-pane probed"
    assert all(c[:2] != ["tmux", "send-keys"] for c in calls), \
        "quiet row must receive no typed wake"


# (d) status shows `quiet` for a quiet row and not for a plain row.
def test_status_shows_quiet_only_for_quiet_row(project, monkeypatch):
    _write_seats(project, [_quiet_row(settings="quiet")])
    _fake_tmux(monkeypatch, ["@246", "director"])
    out = send_mod.status(project, "director")
    assert "quiet" in out
    _write_seats(project, [_quiet_row()])  # non-quiet row, same seat
    out2 = send_mod.status(project, "director")
    assert out2.startswith("status director:")
    assert "quiet" not in out2


# (e) a NON-quiet row keeps every nudge behavior (existing behavior intact).
def test_non_quiet_row_still_nudges(project, monkeypatch):
    _write_seats(project, [_quiet_row()])  # no settings at all
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "secret body", "kid")
    assert _typed(calls), "a non-quiet row must still nudge"
    assert _enters(calls), "a non-quiet row must still press Enter"


# (f) the parent probe as a regression test: a DM (send_dm) to a quiet row
# writes the dm but types NO send-keys and NO Enter — the _nudge_window
# choke point that every nudge entry funnels through must skip quiet.
def test_send_dm_to_quiet_row_types_no_nudge(project, monkeypatch):
    # send_dm resolves its nudge root via find_project_root -> the .agi
    # graph root; the seats row must live where THAT reader looks.
    (project / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (project / ".agi" / "nodes" / ".geometry" / "seats.md").write_text(
        _seats_md([_quiet_row(settings="quiet")]))
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send_dm(project, "mee", "director", "quiet dm body", "mee")
    dm = project / "dm" / "director--mee.md"
    assert dm.is_file() and "quiet dm body" in dm.read_text(), \
        "the dm must still be WRITTEN for a quiet row"
    assert _typed(calls) == [], \
        "send_dm to a quiet row must type NO nudge token"
    assert _enters(calls) == [], \
        "send_dm to a quiet row must type NO Enter"


# rotate normalization: `quiet` composes with `ultracode`, token list and
# JSON object forms both read, and a bare `ultracode` stays intact.
def test_normalize_settings_composes_quiet_with_ultracode():
    assert rotate._normalize_settings("ultracode quiet") == \
        {"ultracode": True, "quiet": True}
    assert rotate._normalize_settings("quiet") == {"quiet": True}
    assert rotate._normalize_settings('{"quiet": true}') == {"quiet": True}
    assert rotate._normalize_settings("ultracode") == {"ultracode": True}
    assert rotate._normalize_settings({}) is None
    assert rotate._normalize_settings(None) is None