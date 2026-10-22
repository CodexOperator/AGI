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


# ---- FF1: fail closed -- "gone" ONLY on FileNotFoundError -------------------
def test_path_gone_is_true_only_for_a_missing_path(tmp_path):
    here = tmp_path / "here"
    here.mkdir()
    assert locations.path_gone(here) is False
    assert locations.path_gone(here / "nope") is True
    closed = tmp_path / "closed"
    closed.mkdir()
    (closed / "x").write_text("x")
    closed.chmod(0o000)
    try:
        assert locations.path_gone(closed / "x") is None, "EACCES is unknown, not gone"
    finally:
        closed.chmod(0o700)


def test_drop_helper_refuses_a_checkout_it_cannot_stat(scratch):
    """The council's FF1 mutant: priv at 0o000, the foreign worktree's `.git`
    cannot be looked at -> NOT gone -> False, 'gate' still registered. RED on
    the lexists-based helper (EACCES read as gone, the entry was removed)."""
    other = scratch["other"]
    assert not locations.drop_dead_worktree_admin(scratch["repo"], other)
    assert "gate" in _registered(scratch["repo"])


# ---- FF2: heal says what happened ------------------------------------------
def _ram_link(scratch, name="a00-ram01"):
    ram = scratch["tmp"] / "ram" / name
    _sh("git", "-C", str(scratch["repo"]), "worktree", "add", "-b", f"loop/{name}",
        str(ram), "season/s2")
    link = scratch["graph"] / "worktrees" / name
    link.symlink_to(ram)
    shutil.rmtree(scratch["tmp"] / "ram")
    return link


def test_sweep_ram_link_logs_registration_dropped(scratch, monkeypatch):
    log = scratch["graph"] / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _ram_link(scratch)
    heal._sweep_finished_worktrees(scratch["graph"])
    assert "[sweep] unlinked a00-ram01: RAM target gone; registration dropped" \
        in log.read_text()


def test_sweep_ram_link_gitdir_mismatch_logs_no_match_and_keeps(scratch, monkeypatch):
    log = scratch["graph"] / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    link = _ram_link(scratch)
    adm = Path(_sh("git", "-C", str(scratch["repo"]), "rev-parse",
                   "--path-format=absolute", "--git-common-dir").strip()) / "worktrees"
    (adm / "a00-ram01" / "gitdir").write_text(str(scratch["tmp"] / "elsewhere" / ".git") + "\n")
    heal._sweep_finished_worktrees(scratch["graph"])
    assert "[sweep] unlinked a00-ram01: RAM target gone; NO MATCH, kept" in log.read_text()
    assert not link.is_symlink()
    assert "a00-ram01" in _registered(scratch["repo"]), "an entry nothing names is kept"


def test_sweep_ram_link_locked_entry_logs_left_locked(scratch, monkeypatch):
    log = scratch["graph"] / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _ram_link(scratch)
    adm = Path(_sh("git", "-C", str(scratch["repo"]), "rev-parse",
                   "--path-format=absolute", "--git-common-dir").strip()) / "worktrees"
    (adm / "a00-ram01" / "locked").write_text("deliberate\n")
    heal._sweep_finished_worktrees(scratch["graph"])
    assert "RAM target gone; left (locked)" in log.read_text()
    assert "a00-ram01" in _registered(scratch["repo"])


# ---- the aio label: a failed drop reads "left (not provably gone, or drop failed)" ----
def test_sweep_ram_link_failed_drop_logs_not_provably_gone_or_drop_failed(
        scratch, monkeypatch):
    """A matching, unlocked entry whose rmtree left it behind: the entry is
    kept and the line says "left (not provably gone, or drop failed)" -- not
    "NO MATCH" (the entry IS matched). The same word covers a checkout that
    cannot be PROVEN gone (EACCES). RED on the old label."""
    log = scratch["graph"] / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _ram_link(scratch, "a00-ram02")
    monkeypatch.setattr(shutil, "rmtree", lambda *a, **k: None)  # the drop leaves it behind
    heal._sweep_finished_worktrees(scratch["graph"])
    assert "[sweep] unlinked a00-ram02: RAM target gone; left (not provably gone, or drop failed)" \
        in log.read_text()
    assert "a00-ram02" in _registered(scratch["repo"]), "the entry is kept"


# ---- goal:g7.16.1.11.45.4: the sweep survives a RAM link behind an UNREADABLE parent ----
def test_sweep_survives_an_eacces_ram_link_and_still_sweeps_the_next(scratch, monkeypatch):
    """Two RAM links in ONE pass: the first's target is under a 0o000 parent
    (Path.is_dir/exists raised PermissionError and killed the pass), the second's
    target is gone. The pass COMPLETES, logs "left (not provably gone, or drop
    failed)" for the first (link and registration kept) and the SECOND is still
    swept (unlinked, registration dropped)."""
    log = scratch["graph"] / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    closed = scratch["tmp"] / "closed"
    first = closed / "a00-eacc1"
    second = scratch["tmp"] / "ram" / "a00-gone2"
    for name, target in (("a00-eacc1", first), ("a00-gone2", second)):
        _sh("git", "-C", str(scratch["repo"]), "worktree", "add", "-b", f"loop/{name}",
            str(target), "season/s2")
        (scratch["graph"] / "worktrees" / name).symlink_to(target)
    shutil.rmtree(scratch["tmp"] / "ram")           # the second target is gone for good
    closed.chmod(0o000)                              # the first is unreadable, not gone
    try:
        heal._sweep_finished_worktrees(scratch["graph"])
    finally:
        closed.chmod(0o700)
    text = log.read_text()
    assert "[sweep] left a00-eacc1: RAM target not provably gone; left (not provably gone, or drop failed)" in text
    assert (scratch["graph"] / "worktrees" / "a00-eacc1").is_symlink(), "the link stays"
    assert "a00-eacc1" in _registered(scratch["repo"]), "its registration stays"
    assert not (scratch["graph"] / "worktrees" / "a00-gone2").is_symlink(), "the NEXT link is still swept"
    assert "a00-gone2" not in _registered(scratch["repo"])
    assert "[sweep] unlinked a00-gone2: RAM target gone; registration dropped" in text
