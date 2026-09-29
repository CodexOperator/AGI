"""Falsifiers for goal:g7.32.6.1 (post-branch address resolution)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_address  # noqa: E402


def test_remote_head_cell_wins():
    row = {"name": "director-helper", "town": "core", "remote_head": "core/season2/main"}
    assert dm_address.resolve_address(row) == "core/season2/main"


def test_nearest_prefers_town_season_main_over_town_main():
    row = {"name": "director-helper", "town": "core", "town_season": 2}
    assert dm_address.nearest_remote_branch(row) == "core/season2/main"
    assert dm_address.resolve_address(row) == "core/season2/main"


def test_nearest_falls_back_to_town_main():
    row = {"name": "director-helper", "town": "core"}
    assert dm_address.resolve_address(row) == "core/main"


def test_nearest_falls_back_to_season_main_when_no_town():
    row = {"name": "director-helper", "town": "all", "season": 2}
    assert dm_address.resolve_address(row) == "season2/main"


def test_empty_town_uses_graph_season_main():
    row = {"name": "ghost", "town": ""}
    assert dm_address.resolve_address(row, season=2) == "season2/main"


def test_refuse_none_row():
    with pytest.raises(ValueError, match="row is required"):
        dm_address.nearest_remote_branch(None)


def test_empty_remote_head_does_not_block_fallback():
    row = {"name": "x", "town": "local", "remote_head": "  "}
    assert dm_address.resolve_address(row) == "local/main"
