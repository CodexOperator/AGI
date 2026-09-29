"""goal:g7.16.1.2.1 · hypothesis:rotation-records-carry-home-relative-paths-one-resolver.

The writer half, pinned through the existing `_write_rotation_record` (no new
interface): a record whose paths sit under HOME is written `~`-relative, so the
committed record never carries the box user's home path. A tmp graph and a
tmp HOME only; no live pane, seat or record is touched. RED on the trunk at
82d64ffe7 (council bundle 2, director-general-2); green since director-general-3's
build. The reader half is `_resolve_record_path`, pinned below.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import rotate  # noqa: E402


def test_a_rotation_record_is_written_home_relative(tmp_path, monkeypatch):
    home = tmp_path / "home" / "someuser"
    (home / "proj").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    root = tmp_path / ".agi"
    (root / "sessions").mkdir(parents=True)
    record = {"seat": "probe", "handover": {"join": {
        "transcript": str(home / "proj" / "t.jsonl"), "path": str(home / "proj")}},
        "after_join": {"results": [{"cmd": f"python3 x --session-log {home}/proj/t.jsonl"}]}}
    path = rotate._write_rotation_record(root, record)
    text = path.read_text(encoding="utf-8")
    assert str(home) not in text
    assert json.loads(text)["handover"]["join"]["transcript"] == "~/proj/t.jsonl"


def test_another_boxs_home_is_written_placeholder(tmp_path, monkeypatch):
    """Re-homed records carry ANOTHER box's home: it becomes `<home>/`."""
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    root = tmp_path / ".agi"
    (root / "sessions").mkdir(parents=True)
    path = rotate._write_rotation_record(root, {"seat": "probe", "ps": "cwd=/home/abcdef/w x"})
    assert json.loads(path.read_text(encoding="utf-8"))["ps"] == "cwd=<home>/w x"


def test_the_one_resolver_expands_tilde_and_passes_the_absolute_form(tmp_path, monkeypatch):
    home = tmp_path / "home" / "someuser"
    monkeypatch.setenv("HOME", str(home))
    assert rotate._resolve_record_path("~/proj/t.jsonl") == f"{home}/proj/t.jsonl"
    assert rotate._resolve_record_path(f"{home}/proj/t.jsonl") == f"{home}/proj/t.jsonl"
    assert rotate._resolve_record_path(None) == ""
