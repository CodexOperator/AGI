"""Tests for NUDGE CLASSES (hypothesis:l4-nudges-have-classes-service-senders-
never-nudge-post-dms-coalesce-into-one-digest-while-busy-and-quiet-system-
silences-only-the-system-class).

A `config:posts` row whose `settings` carries `quiet-system` gets the class
rules: a SERVICE sender (heal / watch / wake-repair / a self-copy) still
WRITES the dm but types NO nudge; a POST dm keeps its inline nudge when the
pane is idle and coalesces to ONE digest while busy. The existing `quiet`
token stays full silence; a row with NO token keeps today's behaviour
byte-for-byte (the regression conjunct).
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import send as send_mod  # noqa: E402
import rotate  # noqa: E402

from test_send import (  # noqa: E402
    _enters,
    _fake_tmux,
    _seats_md,
    _typed,
    _typed_text,
)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    return root


def _row(**extra):
    row = {"name": "director", "role": "director",
           "window": "@246", "pid": 424242}
    row.update(extra)
    return row


def _write_seats(project: Path, rows):
    (project / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(_seats_md(rows))


def _inbox(project: Path) -> Path:
    return project / ".agi" / "sessions" / "inbox" / "director.md"


# ── (a) a service sender never nudges a quiet-system row ──────────────────

def test_service_sender_never_nudges_quiet_system_row(project, monkeypatch):
    _write_seats(project, [_row(settings="quiet-system")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "heal alarm body", "heal")
    assert "heal alarm body" in _inbox(project).read_text(), \
        "the dm is the record and must still be written"
    assert _typed(calls) == [], "a service sender must type NO nudge token"
    assert _enters(calls) == [], "a service sender must type NO Enter"
    assert all(c[:2] != ["tmux", "capture-pane"] for c in calls), \
        "a service sender must not even probe the pane"


def test_after_join_self_copy_is_service_and_never_nudges(project, monkeypatch):
    """The after_join own-inbox copy (sender == recipient) is a self-copy:
    it wakes nobody, so on a quiet-system row it types nothing."""
    _write_seats(project, [_row(settings="quiet-system")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "rotation self copy", "director")
    assert "rotation self copy" in _inbox(project).read_text()
    assert _typed(calls) == []
    assert _enters(calls) == []


def test_wake_repair_sender_is_service(project, monkeypatch):
    _write_seats(project, [_row(settings="quiet-system")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "repair body", "wake-repair")
    assert _typed(calls) == []
    assert _enters(calls) == []


# ── (b) a post dm keeps its inline nudge and coalesces ONE digest ─────────

def test_post_dm_still_nudges_inline_on_quiet_system_row_when_idle(
        project, monkeypatch):
    _write_seats(project, [_row(settings="quiet-system")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "post body", "kid-1")
    assert _typed(calls), "a direct post dm must still nudge an idle pane"
    assert _enters(calls)


def test_two_post_dms_while_busy_coalesce_to_one_digest(project, monkeypatch):
    """Falsifier: two deferred post dms in one window produce two tokens.
    Under busy they store/defer and the retry types ONE line carrying both."""
    _write_seats(project, [_row(settings="quiet-system")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"],
                       capture_text="busy\n\nesc to interrupt\n")
    assert send_mod._nudge_window(project, "director",
                                  sender="kid-1", body="dm one") is False
    assert send_mod._nudge_window(project, "director",
                                  sender="kid-1", body="dm two") is False
    assert _typed(calls) == [], "a busy pane takes no token"
    # the window lapses: the deferred delivery types ONE line naming both
    send_mod._nudge_marker_path(project, "director").write_text(
        "2020-01-01T00:00:00+00:00\n")
    calls = _fake_tmux(monkeypatch, ["@246", "director"])  # idle retry
    send_mod.wake(project, "director")
    typed = _typed_text(calls)
    assert len(typed) == 1, typed
    assert "dm one" in typed[0]


# ── (c) the token selects the class rules; quiet is still full silence ────

def test_quiet_row_is_still_full_silence(project, monkeypatch):
    _write_seats(project, [_row(settings="quiet")])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "quiet body", "kid-1")
    assert "quiet body" in _inbox(project).read_text()
    assert _typed(calls) == [] and _enters(calls) == []


def test_plain_row_keeps_today_behaviour_for_a_service_sender(
        project, monkeypatch):
    """REGRESSION conjunct: no token = today -- a service sender on a plain
    row still nudges, byte-for-byte unchanged."""
    _write_seats(project, [_row()])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    calls = _fake_tmux(monkeypatch, ["@246", "director"])
    send_mod.send(project, "director", "plain body", "heal")
    assert _typed(calls), "a plain row must keep today's nudge behaviour"


# ── the derivation itself, and the token's place in the schema ────────────

def test_sender_class_is_derived_from_the_sender(project):
    _write_seats(project, [_row(settings="quiet-system")])
    assert send_mod._sender_class(project, "heal") == "service"
    assert send_mod._sender_class(project, "watch") == "service"
    assert send_mod._sender_class(project, "wake-repair") == "service"
    assert send_mod._sender_class(project, None) == "service"
    assert send_mod._sender_class(project, "director",
                                  to="director") == "service"
    assert send_mod._sender_class(project, "kid-1", to="director") == "post"


def test_normalize_settings_reads_quiet_system():
    assert rotate._normalize_settings("quiet-system") == \
        {"quiet_system": True}
    assert rotate._normalize_settings("quiet-system ultracode") == \
        {"quiet_system": True, "ultracode": True}
    assert rotate._normalize_settings('{"quiet_system": true}') == \
        {"quiet_system": True}


def test_row_is_quiet_system_reads_the_settings_cell(project):
    _write_seats(project, [_row(settings="quiet-system")])
    assert send_mod._row_is_quiet_system(project, "director") is True
    assert send_mod._row_is_quiet(project, "director") is False, \
        "quiet-system is NOT full silence"
    _write_seats(project, [_row(settings="quiet")])
    assert send_mod._row_is_quiet_system(project, "director") is False
    assert send_mod._row_is_quiet(project, "director") is True
