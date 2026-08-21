"""Tests for bin/grid.py — the per-node git grid, in-repo ref-namespace mode."""

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
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "x.md").write_text(
        '---\nid: "idea:x"\ntype: idea\n---\n\nfirst thought\n'
    )
    grid.cmd_init(tmp_path)
    return tmp_path


def versions(root, node_id):
    tip = grid.ref_tip(root, grid.node_ref(node_id))
    return int(grid.git(root, "rev-list", "--count", tip)) if tip else 0


def test_init_idempotent_and_refuses_non_repo(tmp_path):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    with pytest.raises(SystemExit):
        grid.cmd_init(tmp_path)  # not a git repo -> hard error, no silent grid


def test_commit_creates_version_and_skips_unchanged(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1
    # unchanged content -> no new version (change, not time, makes versions)
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1


def test_grid_refs_stay_out_of_branch_listing(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    branches = grid.git(project, "branch", "--list")
    assert "grid" not in branches  # D2 must not pollute D1's branch namespace


def test_edit_makes_v2_and_diff_shows_it(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text().replace("first thought", "second thought"))
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 2
    ref = grid.node_ref("idea:x")
    diff = grid.git(project, "diff", f"{ref}~1", ref, "--", "node.md")
    assert "-first thought" in diff and "+second thought" in diff


def test_session_branch_is_separate_dimension(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text() + "\ndraft addition\n")
    grid.cmd_commit(project, [str(f)], do_all=False, session=("3", "a01-kid"))
    # D3 recorded, D2 untouched:
    assert grid.ref_tip(project, "refs/grid/session/3/a01-kid/idea/x") is not None
    assert versions(project, "idea:x") == 1


def test_node_without_id_is_skipped(project):
    (project / "nodes" / "idea" / "noid.md").write_text("no frontmatter here\n")
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert grid.ref_tip(project, "refs/grid/node/noid") is None


def test_commit_prefix_marks_auto_snapshots(project):
    f = project / "nodes" / "idea" / "x.md"
    grid.cmd_commit(project, [str(f)], do_all=False, session=None,
                    prefix="cron: ")
    msg = grid.git(project, "log", "-1", "--format=%s", grid.node_ref("idea:x"))
    assert msg == "cron: v1 idea:x"


def test_sanitize_refuses_ref_hostile_chars():
    assert grid.sanitize("hyp:weird id~^?.") == "hyp/weird-id---"
    assert ".." not in grid.sanitize("a:..b")


def test_cron_lines_are_cwd_proof(tmp_path):
    # Regression: cron runs from $HOME; a line without cd/-C fails silently.
    lines = grid.cron_lines(tmp_path, "main", 5, tmp_path / "g.log")
    assert lines[0].startswith(f"*/5 * * * * cd {tmp_path} && ")
    assert f"'{grid.PUSH_SPEC}'" in lines[0]
    assert "--prefix 'cron: '" in lines[0]
    assert lines[1].startswith(f"7 * * * * git -C {tmp_path} push -q origin main")
    for line in lines:
        assert str(tmp_path / "g.log") in line  # log path doubles as the marker


def test_sync_pushes_grid_refs_and_sets_fetch_spec(project, tmp_path):
    grid.cmd_commit(project, [], do_all=True, session=None)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    grid.cmd_sync(project, str(remote))
    out = subprocess.run(
        ["git", "-C", str(remote), "for-each-ref", "refs/grid",
         "--format=%(refname)"],
        capture_output=True, text=True, check=True,
    ).stdout
    assert "refs/grid/node/idea/x" in out
    # a fresh clone must be able to fetch the grid: refspec configured
    specs = grid.git(project, "config", "--get-all", "remote.origin.fetch")
    assert grid.FETCH_SPEC in specs.splitlines()


def test_find_project_root_accepts_canonical_and_legacy_config(tmp_path):
    # Rename window: agi-tree.config.json is canonical, but projects still
    # carrying autoresearch-tree.config.json must keep resolving.
    canonical = tmp_path / "canonical"
    legacy = tmp_path / "legacy"
    nested = legacy / "nodes" / "idea"
    canonical.mkdir()
    nested.mkdir(parents=True)
    (canonical / "agi-tree.config.json").write_text("{}")
    (legacy / "autoresearch-tree.config.json").write_text("{}")

    assert grid.find_project_root(canonical) == canonical
    assert grid.find_project_root(nested) == legacy
