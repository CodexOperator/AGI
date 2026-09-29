"""Falsifiers for goal:g7.32.6.5 (read = read-flag to sender remote)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_read_version  # noqa: E402


def test_read_true_destination_is_sender_remote():
    sender = {"name": "belam", "town": "core", "town_season": 2, "remote_head": "core/season2/main"}
    v = dm_read_version.build_read_version(
        sender_row=sender,
        addressee="director-helper",
        body="ack",
    )
    assert v["read"] is True
    assert v["destination"] == "core/season2/main"
    assert v["read_target"] == "sender"
    assert v["to"] == "belam"
    assert "inbox" not in v["path"]


def test_falls_back_to_nearest_when_no_remote_head_cell():
    sender = {"name": "belam", "town": "core"}
    v = dm_read_version.build_read_version(
        sender_row=sender, addressee="director-helper"
    )
    assert v["destination"] == "core/main"
    assert v["read"] is True


def test_refuse_nameless_sender():
    with pytest.raises(ValueError, match="sender_row.name"):
        dm_read_version.build_read_version(
            sender_row={"town": "core"}, addressee="x"
        )
