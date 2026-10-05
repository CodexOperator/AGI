"""Falsifiers for dm_engine production façade (g7.32.6.7–.9)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import dm_engine  # noqa: E402


def test_plan_send_uses_remote_head_and_refuses_inbox():
    row = {"name": "alice", "remote_head": "town/core/main", "town": "core"}
    p = dm_engine.plan_send(sender="bob", addressee_row=row, body="hi")
    assert p["destination"] == "town/core/main"
    assert p["read"] is False
    assert p["route"] == "post-branch"
    assert "inbox" not in p["path"]
    assert p["path"] == "comms/dm/alice--bob.md"


def test_plan_send_falls_back_to_nearest_remote_visible():
    row = {"name": "alice", "town": "core", "town_season": 2, "season": 2}
    p = dm_engine.plan_send(sender="bob", addressee_row=row, body="hi")
    assert p["destination"] == "core/season2/main"
    assert p["read"] is False


def test_plan_send_refuses_missing_name():
    with pytest.raises(ValueError, match="addressee_row.name"):
        dm_engine.plan_send(sender="bob", addressee_row={}, body="hi")


def test_plan_read_aims_at_sender_remote():
    sender_row = {"name": "bob", "remote_head": "season2/main"}
    p = dm_engine.plan_read(sender_row=sender_row, addressee="alice", body="ok")
    assert p["read"] is True
    assert p["destination"] == "season2/main"
    assert p["read_target"] == "sender"
    assert "inbox" not in p["path"]


def test_gate_nudge_requires_from_sync(tmp_path):
    row = {"name": "alice", "box": "local-town"}
    dm = {"body": "hi", "read": False}
    # without from_sync → False regardless of locality stubs
    assert dm_engine.gate_nudge(tmp_path, row, dm, from_sync=False) is False


def test_gate_nudge_quiet_blocks_without_red(tmp_path, monkeypatch):
    import boxes

    monkeypatch.setattr(boxes, "row_is_local", lambda root, row: True)
    row = {"name": "alice", "box": "local-town", "quiet": True}
    dm = {"body": "hi", "read": False}
    assert dm_engine.gate_nudge(tmp_path, row, dm, from_sync=True) is False
    dm_red = {"body": "alert [red]", "read": False}
    assert dm_engine.gate_nudge(tmp_path, row, dm_red, from_sync=True) is True


def test_sync_interval_and_schedule_honor_config_cell():
    assert dm_engine.sync_interval_min(None) == 3
    assert dm_engine.sync_schedule_expr(None) == "*/3 * * * *"
    cfg = {"values": {"dm": {"sync_interval_min": 2}}}
    assert dm_engine.sync_interval_min(cfg) == 2
    assert dm_engine.sync_schedule_expr(cfg) == "*/2 * * * *"
    with pytest.raises(ValueError):
        dm_engine.sync_interval_min({"values": {"dm": {"sync_interval_min": 9}}})


def test_plan_sync_tick_only_emits_gated(tmp_path, monkeypatch):
    import boxes

    monkeypatch.setattr(boxes, "row_is_local", lambda root, row: True)
    row = {"name": "alice", "box": "local-town"}
    unread = [
        (row, {"body": "one", "read": False}),
        (row, {"body": "two", "read": True}),  # read → skip
    ]
    plans = dm_engine.plan_sync_tick(tmp_path, [row], unread, from_sync=True)
    assert len(plans) == 1
    assert plans[0]["post"] == "alice"
    assert plans[0]["body"] == "one"
    assert plans[0]["from_sync"] is True

@pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green')
def test_crons_known_jobs_includes_dm_sync():
    """g7.32.6.8 — production crons.py knows dm_sync by name."""
    path = Path(__file__).resolve().parents[1] / "bin" / "crons.py"
    src = path.read_text()
    assert "dm_sync" in src
    assert "dm_engine" in src
    assert "dm-sync" in src
    assert "KNOWN_JOBS" in src

