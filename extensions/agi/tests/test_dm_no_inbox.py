"""Falsifiers for goal:g7.32.6.6 (no separate inbox)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_no_inbox  # noqa: E402


def test_inbox_path_detected_and_refused():
    p = ".agi/sessions/inbox/director-helper.md"
    assert dm_no_inbox.is_inbox_path(p) is True
    with pytest.raises(PermissionError, match="inbox path refused"):
        dm_no_inbox.assert_allowed_dm_path(p)


def test_post_branch_dm_path_allowed():
    p = "comms/dm/belam--director-helper.md"
    assert dm_no_inbox.is_post_branch_dm_path(p) is True
    assert dm_no_inbox.assert_allowed_dm_path(p) == p


def test_random_path_refused():
    with pytest.raises(PermissionError, match="not a post-branch"):
        dm_no_inbox.assert_allowed_dm_path("sessions/seats/x.md")
