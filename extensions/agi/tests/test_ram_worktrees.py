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


class _Repo(type(Path())):
    """A Path that can carry the fixture's recorded RAM writes."""


def _git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], check=True,
                          capture_output=True, text=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setenv("GUARD_BOX", "test-box")
    r = _Repo(tmp_path / "repo")
    (r / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    _git(r, "init", "-q", "-b", "main")
    (r / "f.txt").write_text("x\n")
    _git(r, "add", "f.txt")
    _git(r, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    # goal:g7.16.1.5.5.1: never a real systemd-run unit from a test -- the
    # wrap is recorded and the argv runs as-is.
    r.ram_writes = []
    monkeypatch.setattr(locations, "ram_write_argv",
                        lambda argv: r.ram_writes.append(list(argv)) or list(argv))
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


# ---------- goal:g7.16.1.5.5.1: the RAM disk's pages on their own slice ------

def test_a_ram_checkout_is_written_from_the_ram_slice(repo, tmp_path):
    ram = tmp_path / "ram" / "worktrees"
    ram.parent.mkdir()
    _guard(repo, f"GUARD_RAM_WORKTREES_test_box={ram}\n")
    dispatch.branch_worktree_for_spawn(repo / ".agi", "loop/a2", "a2", "main")
    assert [a[3:5] for a in repo.ram_writes] == [["worktree", "add"]]
    assert str(ram / "a2") in repo.ram_writes[0]


def test_a_disk_checkout_is_not_wrapped(repo):
    dispatch.branch_worktree_for_spawn(repo / ".agi", "loop/a3", "a3", "main")
    assert repo.ram_writes == []


def test_ram_write_argv_runs_under_the_ram_slice(monkeypatch):
    """Through THE one scope-argv builder (goal:g7.16.1.7.1.1): a scope under
    ramdisk.slice, never a second systemd-run argv of its own."""
    import importlib
    import mem_cap
    real = importlib.reload(locations).ram_write_argv  # the fixture-free one
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    argv = real(["cp", "a", "b"])
    assert argv == mem_cap.scope_argv(["cp", "a", "b"], "ramdisk.slice")
    assert "--scope" in argv and "--slice=ramdisk.slice" in argv
    assert locations.RAM_SLICE == "ramdisk.slice"  # never agi-*: no dash nesting
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    assert real(["cp", "a", "b"]) == ["cp", "a", "b"]


def test_guard_init_writes_the_ram_slice_without_an_oomd_kill():
    src = (Path(dispatch.__file__).resolve().parents[1] / "guard" /
           "guard-init.sh").read_text(encoding="utf-8")
    block = src[src.index("the RAM disk's OWN budget line"):
                src.index('put "$UGUARD/ramdisk.slice"')]
    assert "MemoryMax=${RAM_BUDGET_M}M" in block
    assert not [ln for ln in block.splitlines() if ln.startswith("ManagedOOM")]
    assert 'size_cell RAM_BUDGET_M RAM_BUDGET' in src  # read + validated as a size cell (goal:g7.16.1.5.5.5)
    # one slice name in two languages, pinned equal (review R3 note)
    assert f'put "$UGUARD/{locations.RAM_SLICE}"' in src
    # R2: --uninstall removes it, --status reads it
    assert src.count('"$UGUARD/ramdisk.slice"') >= 2
    assert "show -p MemoryMax --value ramdisk.slice" in src
