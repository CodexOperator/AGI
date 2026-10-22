"""goal:g7.16.1.11.45.1 -- the engine never runs a bare `git worktree prune`.

A bare prune drops EVERY unlocked registration whose checkout the running uid
cannot stat, so one sweep pass could delete another uid's live worktree entry
(SM's gate worktrees, 10-21 21:44Z). The sweep now removes only the entry whose
`gitdir` names the gone path (`locations.drop_dead_worktree_admin`), and the
`worktree remove` that already deleted its admin dir is not followed by a prune.

Falsifier (sp's row): a scratch MAIN with ANOTHER owner's UNLOCKED worktree
behind an unreadable (000) dir + a dead kid worktree; the sweep removes the
kid's entry and leaves the other's (`worktree list` before/after). The MUTANT
restores today's bare prune and must turn the same check RED.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
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
import locations  # noqa: E402

pytestmark = pytest.mark.skipif(
    os.geteuid() == 0, reason="root can stat a 000 dir: the falsifier needs a non-root uid")


@pytest.fixture(autouse=True)
def _no_box_pressure(monkeypatch):
    monkeypatch.setattr(heal, "_sweep_pressure_ok", lambda root: (True, "test"))


def _sh(*args: str) -> str:
    out = subprocess.run(list(args), capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{args}: {out.stderr}")
    return out.stdout


@pytest.fixture
def scratch(tmp_path: Path):
    """A real MAIN, one dead-able kid worktree, and a foreign unlocked
    worktree whose parent dir is closed (000) while the test runs."""
    repo = tmp_path / "repo"
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(
        {"reaper": {"worktree_grace_min": 0}}))
    _sh("git", "init", "-b", "season/s2", str(repo))
    _sh("git", "-C", str(repo), "config", "user.email", "t@example.com")
    _sh("git", "-C", str(repo), "config", "user.name", "t")
    (repo / ".gitignore").write_text(".agi/sessions/\n.agi/worktrees/\n")
    (repo / "base.txt").write_text("base\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-q", "-m", "init")
    kid = graph / "worktrees" / "a00-dead01"
    _sh("git", "-C", str(repo), "worktree", "add", "-b", "loop/n-K@2", str(kid),
        "season/s2")
    priv = tmp_path / "priv"
    priv.mkdir()
    other = priv / "gate"
    _sh("git", "-C", str(repo), "worktree", "add", "-b", "other/g", str(other),
        "season/s2")
    priv.chmod(0o000)
    try:
        yield {"repo": repo, "graph": graph, "kid": kid, "other": other,
               "tmp": tmp_path}
    finally:
        priv.chmod(0o700)


def _registered(repo: Path) -> set[str]:
    adm = Path(_sh("git", "-C", str(repo), "rev-parse", "--path-format=absolute",
                   "--git-common-dir").strip()) / "worktrees"
    return {p.name for p in adm.iterdir()} if adm.is_dir() else set()


def test_sweep_removes_the_dead_kid_and_leaves_the_foreign_entry(scratch):
    before = _registered(scratch["repo"])
    assert before == {"a00-dead01", "gate"}
    removed, refused, kept = heal._sweep_finished_worktrees(scratch["graph"])
    assert (removed, refused) == (1, 0)
    assert _registered(scratch["repo"]) == {"gate"}, "the other owner's entry survives"


def test_sweep_ram_link_drops_only_its_own_registration(scratch):
    ram = scratch["tmp"] / "ram" / "a00-ram01"
    _sh("git", "-C", str(scratch["repo"]), "worktree", "add", "-b", "loop/n-R@2",
        str(ram), "season/s2")
    link = scratch["graph"] / "worktrees" / "a00-ram01"
    link.symlink_to(ram)
    shutil.rmtree(scratch["tmp"] / "ram")  # the tmpfs emptied at a reboot
    assert _registered(scratch["repo"]) == {"a00-dead01", "gate", "a00-ram01"}
    heal._sweep_finished_worktrees(scratch["graph"])
    assert not link.is_symlink(), "the dead link is unlinked"
    assert _registered(scratch["repo"]) == {"gate"}, \
        "the RAM entry and the removed kid go; the foreign entry stays"


def test_mutant_bare_prune_drops_the_foreign_entry(scratch, monkeypatch):
    """The mutant: today's bare prune after a successful remove. The SAME
    check as the falsifier above must turn RED (the foreign entry is gone)."""
    real = heal._git

    def with_prune(args, cwd, err=None):
        out = real(args, cwd, err)
        if args[:2] == ["worktree", "remove"] and out[1] == 0:
            real(["worktree", "prune"], cwd)
        return out

    monkeypatch.setattr(heal, "_git", with_prune)
    heal._sweep_finished_worktrees(scratch["graph"])
    assert "gate" not in _registered(scratch["repo"]), \
        "the bare prune is destructive: the falsifier's premise holds"


def test_drop_helper_refuses_a_locked_entry_and_a_live_checkout(scratch):
    repo = scratch["repo"]
    gone = scratch["tmp"] / "gone"
    _sh("git", "-C", str(repo), "worktree", "add", "-b", "x/y", str(gone), "season/s2")
    assert not locations.drop_dead_worktree_admin(repo, gone), "checkout still there"
    _sh("git", "-C", str(repo), "worktree", "lock", str(gone))
    shutil.rmtree(gone)
    assert not locations.drop_dead_worktree_admin(repo, gone), "locked entry kept"
    assert "gone" in _registered(repo)
    _sh("git", "-C", str(repo), "worktree", "unlock", str(gone))
    assert locations.drop_dead_worktree_admin(repo, gone)
    assert "gone" not in _registered(repo)
    assert "gate" in _registered(repo)


def test_no_bare_worktree_prune_call_in_engine_code():
    """Negative falsifier: no `["worktree", "prune"]` argv anywhere in bin/."""
    pat = re.compile(r"""["']worktree["']\s*,\s*["']prune["']""")
    hits = [f"{p.name}:{n}" for p in sorted(BIN.glob("*.py"))
            for n, ln in enumerate(p.read_text().splitlines(), 1)
            if pat.search(ln) and not ln.lstrip().startswith("#")]
    assert hits == []
