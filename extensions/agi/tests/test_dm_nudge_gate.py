"""Falsifiers for goal:g7.32.6.4 (nudge = sync-only local unread)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dm_nudge_gate  # noqa: E402


@pytest.fixture(autouse=True)
def _no_inherited_box(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)


def _root(tmp_path: Path, box: str = "encryption-town") -> Path:
    root = tmp_path / "proj"
    (root / ".agi" / "sessions").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text("{}\n", encoding="utf-8")
    (root / ".env").write_text(f"AGI_BOX={box}\n", encoding="utf-8")
    return root


def test_requires_from_sync(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _root(tmp_path)
    row = {"name": "director-helper", "box": "encryption-town"}
    dm = {"body": "hi", "read": False}
    assert dm_nudge_gate.may_nudge(root, row, dm, from_sync=False) is False
    assert dm_nudge_gate.may_nudge(root, row, dm, from_sync=True) is True


def test_foreign_box_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _root(tmp_path)
    row = {"name": "director-helper", "box": "local-town"}
    dm = {"body": "hi", "read": False}
    assert dm_nudge_gate.may_nudge(root, row, dm, from_sync=True) is False


def test_already_read_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _root(tmp_path)
    row = {"name": "director-helper", "box": "encryption-town"}
    dm = {"body": "hi", "read": True}
    assert dm_nudge_gate.may_nudge(root, row, dm, from_sync=True) is False


def test_quiet_blocks_unless_red(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _root(tmp_path)
    row = {"name": "director-helper", "box": "encryption-town", "quiet": True}
    dm = {"body": "hi", "read": False}
    assert dm_nudge_gate.may_nudge(root, row, dm, from_sync=True) is False
    red = {"body": "alert [red]", "read": False}
    assert dm_nudge_gate.may_nudge(root, row, red, from_sync=True) is True
