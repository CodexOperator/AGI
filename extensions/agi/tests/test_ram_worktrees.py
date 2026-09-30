"""goal:g7.16.1.5.4 -- round worktrees check out on the RAM disk.

The config:guard cell `GUARD_RAM_WORKTREES_<box>` names the tmpfs dir; a
round worktree is added there and `.agi/worktrees/<agent>` is a symlink to
it (readers that glob .agi/worktrees are unchanged). `GUARD_RAM_WT_HOLD_PCT`
is the line at or over which dispatch HOLDS a launch. A real temp git repo;
the "tmpfs" is a plain temp dir.
"""
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import dispatch  # noqa: E402
import locations  # noqa: E402


def _git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], check=True,
                          capture_output=True, text=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setenv("GUARD_BOX", "test-box")
    r = tmp_path / "repo"
    (r / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    _git(r, "init", "-q", "-b", "main")
    (r / "f.txt").write_text("x\n")
    _git(r, "add", "f.txt")
    _git(r, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    return r


def _guard(repo, cells: str):
    (repo / ".agi" / "nodes" / ".geometry" / "guard.md").write_text(
        "---\nid: config:guard\n---\n# config:guard\n\n```sh guard.env\n"
        "GUARD_RAM_DIR_other_box=/nope\n" + cells + "```\n")


def _paths(repo):
    return [ln.split(" ", 1)[1] for ln in _git(repo, "worktree", "list", "--porcelain").splitlines()
            if ln.startswith("worktree ")]


def test_guard_cell_reads_this_boxs_key(repo):
    _guard(repo, "GUARD_RAM_DIR_test_box='/mnt/x'\n")
    assert locations.guard_box_key() == "test_box"
    assert locations.guard_cell(repo / ".agi", "RAM_DIR") == "/mnt/x"
    assert locations.guard_cell(repo / ".agi", "RAM_MAIN", "d") == "d"


def test_a_round_worktree_checks_out_on_the_ram_dir(repo, tmp_path):
    ram = tmp_path / "ram" / "worktrees"
    ram.parent.mkdir()
    _guard(repo, f"GUARD_RAM_WORKTREES_test_box={ram}\n")
    link = dispatch.branch_worktree_for_spawn(repo / ".agi", "loop/a1", "a1", "main")
    assert link == repo / ".agi" / "worktrees" / "a1" and link.is_symlink()
    assert (link / "f.txt").read_text() == "x\n"
    paths = _paths(repo)
    assert str(ram / "a1") in paths
    assert not [p for p in paths if "/.agi/worktrees/" in p]  # falsifier 2
    dispatch.drop_branch_worktree(repo / ".agi", link)
    assert not link.exists() and not link.is_symlink()
    assert str(ram / "a1") not in _paths(repo)


def test_the_cell_off_keeps_todays_disk_path(repo):
    _guard(repo, "")
    wt = dispatch.branch_worktree_for_spawn(repo / ".agi", "loop/a2", "a2", "main")
    assert wt == repo / ".agi" / "worktrees" / "a2" and not wt.is_symlink()
    assert dispatch.ram_worktree_hold(repo / ".agi") is None


def test_the_hold_line(repo, tmp_path):
    ram = tmp_path / "ram" / "worktrees"
    ram.parent.mkdir()
    _guard(repo, f"GUARD_RAM_WORKTREES_test_box={ram}\nGUARD_RAM_WT_HOLD_PCT_test_box=0\n")
    assert "hold line 0%" in dispatch.ram_worktree_hold(repo / ".agi")
    _guard(repo, f"GUARD_RAM_WORKTREES_test_box={ram}\nGUARD_RAM_WT_HOLD_PCT_test_box=100.1\n")
    assert dispatch.ram_worktree_hold(repo / ".agi") is None


def test_a_reboot_emptied_ram_worktree_is_enumerated_dead(repo, tmp_path):
    """A reboot empties the tmpfs: the kid's registration is stale and
    cli's dead-kid enumeration finds it under the RAM dir (then prune)."""
    import shutil
    import cli
    ram = tmp_path / "ram" / "worktrees"
    ram.parent.mkdir()
    _guard(repo, f"GUARD_RAM_WORKTREES_test_box={ram}\n")
    dispatch.branch_worktree_for_spawn(repo / ".agi", "loop/k", "a00-k1", "main")
    assert cli._dead_kid_worktrees(repo) == []
    shutil.rmtree(ram)
    assert cli._dead_kid_worktrees(repo) == [(ram / "a00-k1").resolve()]
