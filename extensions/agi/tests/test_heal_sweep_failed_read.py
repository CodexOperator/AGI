"""goal:g7.16.1.5.3.2 -- heal.py's worktree sweep never reads a FAILED git read as clean.

`_sweep_finished_worktrees` judged `status_lines, _ = _git(["status", "--porcelain"], wt)`
and `head_lines, _ = _git(["rev-parse", "HEAD"], wt)` WITHOUT the return code, and `_git`
is best-effort (a broken git = ([], nonzero)). A failed status on an UNMERGED tree read as
"no dirty paths": `_sweep_archive` pinned HEAD only and the tree was dropped with
`git worktree remove --force`, the uncommitted bytes gone. A failed rev-parse on a tree
whose gitdir exists read as head "": nothing pinned, then the same remove. The invariant
(belam's [red], 18:27Z 10-07): a worktree with uncommitted state is never removed before
its archive ref exists; a read that FAILED is unknown, never "nothing to archive".

REAL scratch git repos and worktrees; the ONE fault is a wrapper around `heal._git` that
returns ([], 128) for exactly the call under test on exactly one tree; everything else is
real. No live path, no network, no box state (the pressure gate is stubbed like the sibling
sweep tests). A call that kills a child by OOM cannot be forced here: the wrapper stands in
for it (the observable is the same: ([], nonzero)).

Lanes: f1 status fails on an UNMERGED DIRTY tree · f2 status fails on an UNMERGED CLEAN
tree and on a MERGED one · f3 rev-parse HEAD fails (gitdir exists, head not cached) ·
f4 the sweep goes ON past a refusal · f5 the refusal is per pass: the next pass with a
healthy git archives + removes the tree and clears the record · f6 dry-run refuses too ·
c1 control: status ok + merged + clean = removed · c2 control: the DG2.C1 orphan keeps its
orphan refusal, once · c3 control: unmerged dirty, status ok = archived (both refs verify,
the bytes on the -dirty ref) and removed.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
NS = "refs/archive/worktrees/"


@pytest.fixture(autouse=True)
def _no_box_pressure(monkeypatch):
    monkeypatch.setattr(heal, "_sweep_pressure_ok", lambda root: (True, "test"))
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()
    yield
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()


def _sh(*args: str) -> None:
    out = subprocess.run(list(args), capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{args}: {out.stderr}")


@pytest.fixture
def repo(tmp_path: Path, monkeypatch) -> Path:
    r = tmp_path / "repo"
    g = r / ".agi"
    (g / "nodes").mkdir(parents=True)
    (g / "config.json").write_text(json.dumps({"reaper": {"worktree_grace_min": 0}}))
    _sh("git", "init", "-b", "season/s2", str(r))
    _sh("git", "-C", str(r), "config", "user.email", "t@example.com")
    _sh("git", "-C", str(r), "config", "user.name", "t")
    (r / ".gitignore").write_text(".agi/sessions/\n.agi/worktrees/\n")
    (r / "base.txt").write_text("base\n")
    (g / "nodes" / "root.md").write_text("# root\n")
    _sh("git", "-C", str(r), "add", "-A")
    _sh("git", "-C", str(r), "commit", "-q", "-m", "init")
    monkeypatch.setenv("AGI_REAPER_LOG", str(g / "reaper.log"))
    return r


def _graph(r: Path) -> Path:
    return r / ".agi"


def _log(r: Path) -> str:
    p = _graph(r) / "reaper.log"
    return p.read_text() if p.exists() else ""


def _cut(r: Path, agent: str, branch: str) -> Path:
    wt = _graph(r) / "worktrees" / agent
    _sh("git", "-C", str(r), "worktree", "add", "-b", branch, str(wt), "season/s2")
    return wt


def _commit(wt: Path, name: str) -> None:
    (wt / name).write_text(name + "\n")
    _sh("git", "-C", str(wt), "add", "-A")
    _sh("git", "-C", str(wt), "commit", "-q", "-m", name)


def _ref(r: Path, ref: str) -> str:
    o = subprocess.run(["git", "-C", str(r), "rev-parse", "--verify", "-q", ref],
                       capture_output=True, text=True)
    return o.stdout.strip()


def _round(r: Path, wt: Path, agent: str, n: int) -> None:
    """The round's session records, stamped and brought HOME byte-for-byte as session-complete
    leaves them: the sweep's base (`agent.json` base_branch) and its condition (4)."""
    it = wt / ".agi" / "sessions" / f"iter-{n:03d}"
    it.mkdir(parents=True, exist_ok=True)
    (it / "agent.json").write_text(json.dumps(
        {"id": agent, "status": "done", "base_branch": "season/s2"}))
    (it / "manifest.json").write_text(json.dumps({"timeout_seconds": 600, "agents": []}))
    shutil.copytree(it, _graph(r) / "sessions" / it.name)


def unmerged_dirty(r: Path, agent="a00-dirty1") -> Path:
    """HEAD never landed AND an uncommitted file + an uncommitted edit."""
    wt = _cut(r, agent, f"loop/{agent}@2")
    _commit(wt, "round.md")
    (wt / "uncommitted.txt").write_text("precious bytes\n")
    (wt / "base.txt").write_text("base\nedited\n")
    _round(r, wt, agent, 1)
    return wt


def unmerged_clean(r: Path, agent="a00-uncln1") -> Path:
    wt = _cut(r, agent, f"loop/{agent}@2")
    _commit(wt, "round.md")
    _round(r, wt, agent, 2)
    return wt


def merged_clean(r: Path, agent="a00-mrgcl1") -> Path:
    wt = _cut(r, agent, f"loop/{agent}@2")   # HEAD == the base tip: an ancestor
    _round(r, wt, agent, 3)
    return wt


class Fault:
    """A wrapper around heal._git: ([], 128) for ONE call on ONE tree, every call recorded."""

    def __init__(self, monkeypatch, tree: str | None, call: str):
        self.tree, self.call, self.on, self.calls = tree, call, True, []
        real = heal._git

        def wrapped(args, cwd, err=None):
            self.calls.append((list(args), Path(cwd).name))
            hit = {"status": list(args)[:2] == ["status", "--porcelain"],
                   "head": list(args) == ["rev-parse", "HEAD"]}[self.call]
            if self.on and hit and Path(cwd).name == self.tree:
                return [], 128
            return real(args, cwd, err)

        monkeypatch.setattr(heal, "_git", wrapped)
        if call == "head":   # the head is not cached by the one `worktree list` call
            real_heads = heal._sweep_worktree_heads
            monkeypatch.setattr(heal, "_sweep_worktree_heads",
                                lambda mc: {k: (b, "") for k, (b, _h) in real_heads(mc).items()})

    def removes(self):
        return [c for c in self.calls if c[0][:2] == ["worktree", "remove"]]


def sweep(r: Path, **kw):
    return heal._sweep_finished_worktrees(_graph(r), **kw)


def _refusal(r: Path, agent: str) -> list[str]:
    return [l for l in _log(r).splitlines() if f"refused {agent}" in l]


# -- f1
def test_f1_failed_status_on_an_unmerged_dirty_tree_is_refused(repo, monkeypatch):
    wt = unmerged_dirty(repo)
    f = Fault(monkeypatch, "a00-dirty1", "status")
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (0, 1)
    assert wt.is_dir() and (wt / "uncommitted.txt").read_text() == "precious bytes\n"
    assert (wt / "base.txt").read_text() == "base\nedited\n"
    line = _refusal(repo, "a00-dirty1")
    assert len(line) == 1 and "git status failed (rc 128)" in line[0], _log(repo)
    assert "[sweep] refused a00-dirty1: git status failed (rc 128)" in line[0]
    assert not _ref(repo, NS + "a00-dirty1"), "nothing is archived on a failed read"
    assert not _ref(repo, NS + "a00-dirty1-dirty")
    assert f.removes() == [], "no `worktree remove` call"
    assert "a00-dirty1" in heal._SWEEP_SKIP
    assert "archived a00-dirty1" not in _log(repo) and "removed a00-dirty1" not in _log(repo)


# -- f2
@pytest.mark.parametrize("make,agent", [(unmerged_clean, "a00-uncln1"),
                                        (merged_clean, "a00-mrgcl1")])
def test_f2_failed_status_is_unknown_never_clean(repo, monkeypatch, make, agent):
    wt = make(repo)
    f = Fault(monkeypatch, agent, "status")
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (0, 1)
    assert wt.is_dir()
    line = _refusal(repo, agent)
    assert len(line) == 1 and "git status failed (rc 128)" in line[0], _log(repo)
    assert not _ref(repo, NS + agent) and f.removes() == []
    assert agent in heal._SWEEP_SKIP and f"removed {agent}" not in _log(repo)


# -- f3
def test_f3_failed_rev_parse_on_a_live_gitdir_is_refused(repo, monkeypatch):
    wt = unmerged_dirty(repo)
    assert (repo / ".git" / "worktrees" / "a00-dirty1").is_dir(), "the gitdir exists"
    f = Fault(monkeypatch, "a00-dirty1", "head")
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (0, 1)
    assert wt.is_dir() and (wt / "uncommitted.txt").read_text() == "precious bytes\n"
    line = _refusal(repo, "a00-dirty1")
    assert len(line) == 1 and "rev-parse" in line[0], _log(repo)
    assert "orphan" not in line[0], "a live gitdir is not the DG2.C1 orphan"
    assert not _ref(repo, NS + "a00-dirty1") and not _ref(repo, NS + "a00-dirty1-dirty")
    assert f.removes() == []
    assert "a00-dirty1" in heal._SWEEP_SKIP
    assert "archived a00-dirty1" not in _log(repo) and "removed a00-dirty1" not in _log(repo)


# -- f4
def test_f4_the_sweep_goes_on_past_a_refusal(repo, monkeypatch):
    bad = unmerged_dirty(repo, "a00-aaaa11")          # sorts first, its status fails
    good = merged_clean(repo, "a00-bbbb22")           # sorts second, healthy
    Fault(monkeypatch, "a00-aaaa11", "status")
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (1, 1)
    assert bad.is_dir() and (bad / "uncommitted.txt").exists()
    assert not good.exists(), "the clean+merged tree is removed in the same pass"
    assert len(_refusal(repo, "a00-aaaa11")) == 1 and "removed a00-bbbb22" in _log(repo)


# -- f5
def test_f5_the_refusal_is_per_pass_and_the_next_healthy_pass_archives_then_removes(repo, monkeypatch):
    wt = unmerged_dirty(repo, "a00-retry1")
    f = Fault(monkeypatch, "a00-retry1", "status")
    sweep(repo)
    assert wt.is_dir() and "a00-retry1" in heal._SWEEP_SKIP
    f.on = False                                       # git is healthy again
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (1, 0)
    assert not wt.exists()
    assert _ref(repo, NS + "a00-retry1") and _ref(repo, NS + "a00-retry1-dirty")
    shown = subprocess.run(["git", "-C", str(repo), "show", NS + "a00-retry1-dirty:uncommitted.txt"],
                           capture_output=True, text=True)
    assert shown.stdout == "precious bytes\n", "the uncommitted bytes are on the -dirty ref"
    assert "a00-retry1" not in heal._SWEEP_SKIP, "a tree that passed is no longer recorded as refused"


# -- f6
def test_f6_dry_run_refuses_too(repo, monkeypatch):
    wt = unmerged_dirty(repo, "a00-dry111")
    Fault(monkeypatch, "a00-dry111", "status")
    removed, refused, _ = sweep(repo, dry_run=True)
    assert (removed, refused) == (0, 1) and wt.is_dir()
    text = _log(repo)
    assert "git status failed (rc 128)" in text
    assert "(dry-run)" not in text, text


# -- controls
def test_c1_status_ok_merged_clean_is_removed_as_today(repo):
    wt = merged_clean(repo)
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (1, 0) and not wt.exists()
    assert "removed a00-mrgcl1" in _log(repo) and not _ref(repo, NS + "a00-mrgcl1")


def test_c2_the_orphan_keeps_its_refusal_once(repo):
    wt = _cut(repo, "a00-orph99", "loop/o-O@2")
    (wt / "stray.txt").write_text("bytes\n")
    shutil.rmtree(repo / ".git" / "worktrees" / "a00-orph99")
    sweep(repo)
    sweep(repo)
    line = _refusal(repo, "a00-orph99")
    assert len(line) == 1 and "orphan" in line[0] and "gitdir gone" in line[0], _log(repo)
    assert (wt / "stray.txt").exists() and not _ref(repo, NS + "a00-orph99")


def test_c3_unmerged_dirty_with_status_ok_is_archived_then_removed(repo):
    wt = unmerged_dirty(repo)
    head = _ref(wt, "HEAD")
    removed, refused, _ = sweep(repo)
    assert (removed, refused) == (1, 0) and not wt.exists()
    assert _ref(repo, NS + "a00-dirty1") == head and _ref(repo, NS + "a00-dirty1-dirty")
    shown = subprocess.run(["git", "-C", str(repo), "show", NS + "a00-dirty1-dirty:uncommitted.txt"],
                           capture_output=True, text=True)
    assert shown.stdout == "precious bytes\n"
    assert "archived a00-dirty1" in _log(repo) and "removed a00-dirty1" in _log(repo)
