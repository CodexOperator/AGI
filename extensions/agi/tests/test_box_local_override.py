"""goal:g7.33.14 — box-local `config.local.json` overlays committed box cells.

hypothesis:a00-d089cf46-707110: clearing the literal bucket must NOT write
this box into shared config.json; authority moves to an untracked local
override read before the committed cell. Local wins per key; committed
foreign reference box stays intact for other machines / unify seeds.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green: boxes local overlay API is gone')

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import boxes  # noqa: E402

COMMITTED = {
    "root": "/srv/foreign-box/agi",
    "logs_dir": "/home/ubuntu/logs",
    "tmux_session": "agi-rc",
    "user": "ubuntu",
}

LOCAL = {
    "root": "/data/work/agi",
    "logs_dir": "/home/belam/logs",
    "user": "belam",
}

SCHEMA = """---
fields:
  root: {type: str}
  logs_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  logs: logs_dir
  tmux: tmux_session
  user: user
---
"""


def _graph(tmp_path: Path, box: dict | None = None) -> Path:
    graph = tmp_path / "graph"
    graph.mkdir()
    (graph / "config.json").write_text(
        json.dumps({"box": dict(box or COMMITTED)}), encoding="utf-8")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[box].md").write_text(SCHEMA, encoding="utf-8")
    return graph


def test_local_overlay_wins_per_key_committed_untouched(tmp_path):
    graph = _graph(tmp_path)
    (graph / "config.local.json").write_text(
        json.dumps({"box": LOCAL}), encoding="utf-8")
    cells = boxes.box_cells(graph)
    assert cells["root"] == "/data/work/agi"
    assert cells["logs_dir"] == "/home/belam/logs"
    assert cells["user"] == "belam"
    # tmux not in local → committed value kept
    assert cells["tmux_session"] == "agi-rc"
    # shared file bytes unchanged
    committed = json.loads((graph / "config.json").read_text(encoding="utf-8"))
    assert committed["box"] == COMMITTED


def test_absent_local_reads_committed_only(tmp_path):
    graph = _graph(tmp_path)
    assert boxes.box_cells(graph) == {
        k: str(COMMITTED[k]) for k in ("root", "logs_dir", "tmux_session", "user")
    }
    assert boxes.local_config_path(graph) is None


def test_allow_paths_names_local_file(tmp_path):
    graph = _graph(tmp_path)
    assert "config.local.json" in boxes.allow_paths(graph)
    assert "config.json" in boxes.allow_paths(graph)


def test_main_checkout_local_reaches_a_worktree_graph(tmp_path):
    """Worktree graph without its own local file resolves main's via git common-dir."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.check_call(["git", "init", "-q"], cwd=repo)
    subprocess.check_call(
        ["git", "config", "user.email", "t@t"], cwd=repo)
    subprocess.check_call(
        ["git", "config", "user.name", "t"], cwd=repo)
    agi = repo / ".agi"
    agi.mkdir()
    (agi / "config.json").write_text(
        json.dumps({"box": COMMITTED}), encoding="utf-8")
    schemas = agi / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[box].md").write_text(SCHEMA, encoding="utf-8")
    (repo / ".gitignore").write_text(".agi/config.local.json\n", encoding="utf-8")
    (agi / "config.local.json").write_text(
        json.dumps({"box": LOCAL}), encoding="utf-8")
    (repo / "README").write_text("x\n", encoding="utf-8")
    subprocess.check_call(
        ["git", "add", "README", ".gitignore", ".agi/config.json",
         ".agi/context/schemas/[box].md"], cwd=repo)
    subprocess.check_call(
        ["git", "commit", "-qm", "init"], cwd=repo)
    # local file stays on disk and is ignored (never tracked)
    assert (agi / "config.local.json").is_file()
    tracked = subprocess.check_output(
        ["git", "ls-files", ".agi/config.local.json"], cwd=repo, text=True)
    assert tracked.strip() == ""

    wt = tmp_path / "wt"
    subprocess.check_call(
        ["git", "worktree", "add", "-q", str(wt), "HEAD"], cwd=repo)
    wt_agi = wt / ".agi"
    assert wt_agi.is_dir()
    # worktree does not carry main's untracked local file
    assert not (wt_agi / "config.local.json").is_file()
    cells = boxes.box_cells(wt_agi)
    assert cells["root"] == "/data/work/agi"
    assert cells["user"] == "belam"
    got = boxes.local_config_path(wt_agi)
    assert got is not None
    assert got.resolve() == (agi / "config.local.json").resolve()


def test_null_local_value_does_not_clobber(tmp_path):
    graph = _graph(tmp_path)
    (graph / "config.local.json").write_text(
        json.dumps({"box": {"root": "/data/work/agi", "user": None}}),
        encoding="utf-8")
    cells = boxes.box_cells(graph)
    assert cells["root"] == "/data/work/agi"
    assert cells["user"] == "ubuntu"  # null skipped; committed kept
