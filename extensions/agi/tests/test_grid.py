"""Tests for bin/grid.py — the per-node git grid (TODO H10 MVP)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin" / "grid.py"
spec = importlib.util.spec_from_file_location("grid", BIN)
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "autoresearch-tree.config.json").write_text("{}")
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "x.md").write_text(
        '---\nid: "idea:x"\ntype: idea\n---\n\nfirst thought\n'
    )
    grid.cmd_init(tmp_path)
    return tmp_path


def versions(root, node_id):
    tip = grid.branch_tip(root, grid.node_branch(node_id))
    return int(grid.git(root, "rev-list", "--count", tip)) if tip else 0


def test_init_is_bare_and_idempotent(project):
    assert (project / ".grid" / "repo" / "HEAD").exists()
    grid.cmd_init(project)  # second call must not blow up


def test_commit_creates_version_and_skips_unchanged(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1
    # unchanged content -> no new version (change, not time, makes versions)
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1


def test_edit_makes_v2_and_diff_shows_it(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text().replace("first thought", "second thought"))
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 2
    branch = grid.node_branch("idea:x")
    diff = grid.git(project, "diff", f"{branch}~1", branch, "--", "node.md")
    assert "-first thought" in diff and "+second thought" in diff


def test_session_branch_is_separate_dimension(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text() + "\ndraft addition\n")
    grid.cmd_commit(project, [str(f)], do_all=False, session=("3", "a01-kid"))
    # D3 recorded, D2 untouched:
    assert grid.branch_tip(project, "session/3/a01-kid/idea/x") is not None
    assert versions(project, "idea:x") == 1


def test_node_without_id_is_skipped(project, capsys):
    (project / "nodes" / "idea" / "noid.md").write_text("no frontmatter here\n")
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert grid.branch_tip(project, "node/noid") is None


def test_sanitize_refuses_ref_hostile_chars():
    assert grid.sanitize("hyp:weird id~^?.") == "hyp/weird-id---"
    assert ".." not in grid.sanitize("a:..b")


def test_sync_pushes_all_branches(project, tmp_path):
    grid.cmd_commit(project, [], do_all=True, session=None)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    grid.cmd_sync(project, str(remote))
    out = subprocess.run(
        ["git", "-C", str(remote), "branch", "--list", "--format=%(refname:short)"],
        capture_output=True, text=True, check=True,
    ).stdout
    assert "node/idea/x" in out
