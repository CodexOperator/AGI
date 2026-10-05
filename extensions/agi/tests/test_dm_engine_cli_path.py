"""Production-importer falsifier: send.py dm-plan / dm-sync CLI path (g7.32.6.7).

Mirrors test_magic_pane_cli_path.py — deleting the dm_engine call in send.py
makes every case here go RED.
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green: send.py dm-plan verbs are gone')

import json
import os
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
SEND = BIN / "send.py"


def _run(tmp_path: Path, *argv: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True, exist_ok=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"box": {"name": "t"}, "values": {"dm": {"sync_interval_min": 3}}})
    )
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("AGI_") and k not in ("PI_MODEL",)}
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(SEND), *argv],
        cwd=root, env=env, capture_output=True, text=True,
    )


def test_dm_plan_verb_on_help(tmp_path):
    r = _run(tmp_path, "--help")
    assert "dm-plan" in r.stdout, r.stdout + r.stderr
    assert "dm-sync" in r.stdout, r.stdout + r.stderr
    assert "dm-read-plan" in r.stdout, r.stdout + r.stderr


def test_dm_plan_prints_post_branch_payload(tmp_path):
    # --addressee-json supplies the post row (no live seats registry needed)
    row = json.dumps({"name": "alice", "remote_head": "core/main", "town": "core"})
    r = _run(tmp_path, "dm-plan", "--to", "alice", "--row-json", row,
             "hello", "world", "--from", "bob")
    assert r.returncode == 0, r.stdout + r.stderr
    payload = json.loads(r.stdout.strip().splitlines()[-1])
    assert payload["kind"] == "dm_send"
    assert payload["destination"] == "core/main"
    assert payload["read"] is False
    assert payload["body"] == "hello world"
    assert "inbox" not in payload["path"]


def test_dm_plan_writes_no_inbox_and_refuses_to_row_mismatch(tmp_path):
    row = json.dumps({"name": "alice", "remote_head": "core/main"})
    r = _run(tmp_path, "dm-plan", "--to", "alice", "--row-json", row,
             "hi", "--from", "bob")
    assert r.returncode == 0, r.stdout + r.stderr
    # production plan never creates sessions/inbox
    assert not list((tmp_path / "proj").rglob("sessions/inbox/**")), r.stdout + r.stderr
    bad = _run(tmp_path, "dm-plan", "--to", "eve", "--row-json", row,
               "hi", "--from", "bob")
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "!= row.name" in bad.stderr


def test_dm_read_plan_sets_read_true(tmp_path):
    row = json.dumps({"name": "bob", "remote_head": "season2/main"})
    r = _run(tmp_path, "dm-read-plan", "--sender-json", row,
             "--addressee", "alice", "--from", "alice")
    assert r.returncode == 0, r.stdout + r.stderr
    payload = json.loads(r.stdout.strip().splitlines()[-1])
    assert payload["read"] is True
    assert payload["destination"] == "season2/main"
    assert payload["read_target"] == "sender"


def test_dm_sync_prints_interval_and_plans(tmp_path):
    r = _run(tmp_path, "dm-sync", "--dry-plan")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "interval_min=3" in r.stdout
    assert "schedule=*/3" in r.stdout
