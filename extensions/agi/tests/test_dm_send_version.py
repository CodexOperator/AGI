"""Falsifiers for goal:g7.32.6.2 (send = dm node version, read=false)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_send_version  # noqa: E402


def test_pairwise_slug_sorted():
    assert dm_send_version.pairwise_slug("b", "a") == "a--b"
    assert dm_send_version.dm_relpath("b", "a") == "comms/dm/a--b.md"


def test_build_send_version_read_false_and_destination():
    v = dm_send_version.build_send_version(
        sender="belam",
        addressee="director-helper",
        body="hello",
        address="core/season2/main",
    )
    assert v["read"] is False
    assert v["destination"] == "core/season2/main"
    assert v["route"] == "post-branch"
    assert "inbox" not in v["path"]
    assert v["path"].endswith("belam--director-helper.md")


def test_refuse_missing_address_no_hub():
    with pytest.raises(ValueError, match="address"):
        dm_send_version.build_send_version(
            sender="a", addressee="b", body="x", address=""
        )


def test_refuse_self_pair():
    with pytest.raises(ValueError, match="self-pair"):
        dm_send_version.pairwise_slug("x", "x")
