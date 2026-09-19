"""Tests for the undelivered-nudge surface (conjuncts 2-4 of
hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once).

A nudge that is NOT typed into the pane prints ONE plain `[undelivered-yet]`
line instead of the coalesce jargon; a typed nudge prints `[delivered]`.
`send.py wake --all-local` sweeps every LOCAL seat with something pending,
types the retry when the pane is idle (printing `[delivered-late]`), and when
a record stays untyped past T minutes it dms its SENDER exactly ONE
`[undelivered]` line -- never a second on the next sweep.

RED-FIRST: these tests were written before the send.py delta and failed on
the built bytes at the time of writing.
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

import send as send_mod  # noqa: E402

from test_send import _fake_tmux, _seats_md  # noqa: E402


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / ".agi" / "sessions" / "inbox").mkdir(parents=True)
    return root


def _write_seats(project: Path, rows):
    (project / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(_seats_md(rows))


def _row(**extra):
    row = {"name": "director", "role": "director",
           "window": "@246", "pid": 424242}
    row.update(extra)
    return row


def test_busy_send_dm_prints_undelivered_yet_and_records_ts(
        project, monkeypatch, capsys):
    """Conjunct (2)+(4): a dm whose nudge was not typed prints the plain
    `[undelivered-yet]` line and leaves a record carrying ts + sender."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: "busy")
    _write_seats(project, [_row()])
    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send_dm(project, "sender-a", "director", "the body", "sender-a")
    err = capsys.readouterr().err
    assert "[undelivered-yet] director" in err, err
    rec = send_mod._read_deferred(project, "director")
    assert rec is not None
    assert rec.get("sender") == "sender-a"
    assert rec.get("ts")


def test_idle_inbox_send_prints_delivered(project, monkeypatch, capsys):
    """Conjunct (2): a nudge actually typed into the pane says `[delivered]`."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(project, [_row()])
    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "an inbox message", "sender-a")
    err = capsys.readouterr().err
    assert "[delivered] director" in err, err


def test_wake_all_local_types_a_stored_record_and_says_delivered_late(
        project, monkeypatch, capsys):
    """Conjunct (3): the sweep delivers a deferred body once the pane is idle
    and prints ONE `[delivered-late] <to> <send ts>` line."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: "busy")
    _write_seats(project, [_row()])
    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send_dm(project, "sender-a", "director", "the body", "sender-a")
    ts = send_mod._read_deferred(project, "director")["ts"]
    capsys.readouterr()

    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _fake_tmux(monkeypatch, ["@246", "director"])
    assert send_mod.wake_all_local(project) is True
    out = capsys.readouterr().out
    assert f"[delivered-late] director {ts}" in out, out
    assert send_mod._read_deferred(project, "director") is None


def test_stale_record_dms_the_sender_exactly_once(project, monkeypatch, capsys):
    """Conjunct (4): a record still untyped past T minutes dms the SENDER one
    `[undelivered]` line -- and never a second on the next sweep."""
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: "busy")
    _write_seats(project, [_row()])
    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send_dm(project, "sender-a", "director", "the body", "sender-a")
    rec = send_mod._read_deferred(project, "director")
    rec["ts"] = "2020-01-01T00:00:00Z"
    send_mod._nudge_deferred_path(project, "director").write_text(
        json.dumps(rec))
    capsys.readouterr()

    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.wake_all_local(project)
    dm = project / "dm" / "sender-a--wake-repair.md"
    assert dm.is_file(), "the sender must receive ONE dm"
    first = dm.read_text()
    assert "[undelivered] director" in first
    assert "pane busy" in first

    _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.wake_all_local(project)
    assert dm.read_text() == first, "no second [undelivered] on the next sweep"


def test_wake_help_mentions_all_local(capsys):
    """Conjunct (6): the sweep is discoverable from `wake --help`."""
    with pytest.raises(SystemExit):
        send_mod.main(["wake", "--help"])
    out = capsys.readouterr().out
    assert "--all-local" in out, out


def test_send_help_smoke(capsys):
    with pytest.raises(SystemExit) as e:
        send_mod.main(["--help"])
    assert e.value.code == 0
