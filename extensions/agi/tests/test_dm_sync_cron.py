"""Falsifiers for goal:g7.32.6.3 (per-box sync cron interval cell)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_sync_cron  # noqa: E402


def test_default_is_three_minutes():
    assert dm_sync_cron.interval_minutes({}) == 3
    assert dm_sync_cron.interval_seconds({}) == 180


def test_values_dm_cell_wins():
    cfg = {"values": {"dm": {"sync_interval_min": 1}}}
    assert dm_sync_cron.interval_minutes(cfg) == 1
    assert dm_sync_cron.interval_seconds(cfg) == 60


def test_comms_cell_accepted():
    cfg = {"comms": {"dm_sync_interval_min": 2}}
    assert dm_sync_cron.interval_minutes(cfg) == 2


def test_out_of_range_refused():
    with pytest.raises(ValueError, match="out of"):
        dm_sync_cron.interval_minutes({"values": {"dm": {"sync_interval_min": 5}}})
    with pytest.raises(ValueError, match="out of"):
        dm_sync_cron.interval_minutes({"values": {"dm": {"sync_interval_min": 0}}})


def test_ensure_config_cell_stamps_default():
    out = dm_sync_cron.ensure_config_cell({})
    assert out["values"]["dm"]["sync_interval_min"] == 3
