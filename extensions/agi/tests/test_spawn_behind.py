"""Tests for the spawn behind-or-refuse gate
(hypothesis:l4-spawn-from-a-worktree-merges-origin-first-or-refuses-when-behind).

RED FIRST, measured PRE-FIX: `cmd_spawn` printed `[seating] worktree: behind N`
via `_seating_worktree_lines` and LAUNCHED anyway -- no merge, no refusal
(rotate.py cmd_spawn body matched `_git_proc(root,"merge"` / `refused: .*behind`
zero times; the behind line printed at the pre-fix :2093-2095). These tests
drive the built gate `_spawn_behind_gate` and the real `cmd_spawn` entry, so on
the pre-fix bytes every one of them fails with AttributeError (the helper does
not exist) or on the missing refusal. Git is faked through `rotate._git_maybe`
(the stdout seam) / `rotate._git_proc` (the returncode seam), never a real
remote.

1. behind + clean  -> the reused `_perform_season_merge` lands it, spawn
   continues (rc 0).
2. behind + conflict -> REFUSE BY NAME, rc 3, NO merge attempted.
3. not behind -> NO fetch, NO merge, rc 0 (byte-identical launch).
4. --dry-run behind -> the would-line only; no fetch, no merge, rc 0.
5. behind + merge refused by git -> rc 3, never a false ok.
6. the real `cmd_spawn` refuses and NEVER reaches `spawn_window`.
7. the gate call site precedes `spawn_window` in `cmd_spawn`'s source.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "extensions"))   # the `agi` package
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))

from agi.bin import rotate  # noqa: E402


def _git_map(lines):
    def fake(cwd, *args):
        return lines.get(args)
    return fake


def _behind_map(n=2):
    return {
        ("rev-list", "--count", "HEAD..origin/season/s2"): [str(n)],
    }


def _ok_proc(rc=0):
    return lambda *a, **k: SimpleNamespace(returncode=rc, stdout="")


def _patch_season(monkeypatch):
    monkeypatch.setattr(rotate, "season_branch", lambda root: "season/s2")


# 1 -------------------------------------------------------------------
def test_gate_merges_when_behind_clean(tmp_path, capsys, monkeypatch):
    _patch_season(monkeypatch)
    gm = _behind_map(2)
    gm[("rev-parse", "--short", "HEAD")] = ["cafe123"]
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    monkeypatch.setattr(rotate, "_git_proc", _ok_proc())
    monkeypatch.setattr(rotate, "_merge_applies_clean", lambda root, sb: True)
    rc = rotate._spawn_behind_gate(tmp_path, dry_run=False)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[spawn] behind origin/season/s2 (2) — merged cafe123" in out


# 2 -------------------------------------------------------------------
def test_gate_refuses_on_conflict_never_merges(tmp_path, capsys, monkeypatch):
    _patch_season(monkeypatch)
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(_behind_map(2)))
    monkeypatch.setattr(rotate, "_git_proc", _ok_proc())
    monkeypatch.setattr(rotate, "_merge_applies_clean", lambda root, sb: False)
    monkeypatch.setattr(rotate, "_merge_conflict_paths",
                        lambda root, sb: "extensions/agi/bin/rotate.py")

    def _no_merge(*a, **k):
        raise AssertionError("merge performed on a conflicting tree")
    monkeypatch.setattr(rotate, "_perform_season_merge", _no_merge)
    rc = rotate._spawn_behind_gate(tmp_path, dry_run=False)
    err = capsys.readouterr().err
    assert rc == 3, err
    assert ("ERR: spawn refused: behind origin/season/s2 2, merge conflict "
            "(extensions/agi/bin/rotate.py)") in err
    assert "git merge --no-edit origin/season/s2" in err


# 3 -------------------------------------------------------------------
def test_gate_not_behind_no_merge(tmp_path, capsys, monkeypatch):
    """Even -> rc 0 and NO merge (the fetch already ran, that is how 'even'
    is learned; rotate-self's perform path fetches the same way)."""
    _patch_season(monkeypatch)
    calls = []

    def _rec(cwd, *args):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout="")
    monkeypatch.setattr(rotate, "_git_proc", _rec)
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(_behind_map(0)))
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda *a, **k: pytest.fail("merged when even"))
    monkeypatch.setattr(rotate, "_perform_season_merge",
                        lambda *a, **k: pytest.fail("merged when even"))
    rc = rotate._spawn_behind_gate(tmp_path, dry_run=False)
    assert rc == 0
    assert ("fetch", "origin", "season/s2") in calls
    assert not [c for c in calls if c and c[0] in ("merge", "merge-tree")]


# 4 -------------------------------------------------------------------
def test_gate_dry_run_no_fetch_no_merge(tmp_path, capsys, monkeypatch):
    _patch_season(monkeypatch)
    calls = []
    monkeypatch.setattr(rotate, "_git_proc",
                        lambda cwd, *a: (calls.append(a) or
                                         SimpleNamespace(returncode=0,
                                                         stdout="")))
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(_behind_map(3)))
    monkeypatch.setattr(rotate, "_perform_season_merge",
                        lambda *a, **k: pytest.fail("merged on a dry-run"))
    rc = rotate._spawn_behind_gate(tmp_path, dry_run=True)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[spawn] would merge origin/season/s2 (3)" in out
    assert calls == []          # no fetch, no merge-tree, no merge


# 5 -------------------------------------------------------------------
def test_gate_refuses_when_git_refuses_the_merge(tmp_path, capsys,
                                                 monkeypatch):
    _patch_season(monkeypatch)
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(_behind_map(2)))
    monkeypatch.setattr(rotate, "_git_proc", _ok_proc())
    monkeypatch.setattr(rotate, "_merge_applies_clean", lambda root, sb: True)
    monkeypatch.setattr(rotate, "_perform_season_merge", lambda root, sb: None)
    rc = rotate._spawn_behind_gate(tmp_path, dry_run=False)
    err = capsys.readouterr().err
    assert rc == 3, err
    assert "refused by git (aborted)" in err
    assert "merged" not in err


# 6 -------------------------------------------------------------------
def test_cmd_spawn_refuses_and_never_launches(tmp_path, capsys, monkeypatch):
    """The real entry: a conflicting spawn returns 3 and `spawn_window` is
    never reached (the refusal sits before the launch, pre-fix it launched
    past the behind line)."""
    _patch_season(monkeypatch)
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(_behind_map(2)))
    monkeypatch.setattr(rotate, "_git_proc", _ok_proc())
    monkeypatch.setattr(rotate, "_merge_applies_clean", lambda root, sb: False)
    monkeypatch.setattr(rotate, "_merge_conflict_paths", lambda root, sb: "x")
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda *a, **k: pytest.fail("launched behind/conflict"))
    (tmp_path / "nodes").mkdir()
    rc = rotate.cmd_spawn(SimpleNamespace(dry_run=False), tmp_path)
    assert rc == 3
    assert "ERR: spawn refused" in capsys.readouterr().err


# 7 -------------------------------------------------------------------
def test_gate_call_precedes_spawn_window():
    src = inspect.getsource(rotate.cmd_spawn)
    gate = src.find("_spawn_behind_gate(")
    spawn = src.find("spawn_window(")
    assert gate >= 0, "cmd_spawn no longer calls the behind gate"
    assert spawn >= 0, "cmd_spawn no longer calls spawn_window"
    assert gate < spawn, (
        "the behind gate must run before the window is built"
    )
