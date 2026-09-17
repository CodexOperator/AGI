"""Conjunct (4) of hypothesis:l4-the-suite-refuses-to-start-when-its-
basetemp-resolves-to-the-live-checkout... -- the throwaway-worktree run.

A throwaway `git worktree add` of the live repo, a pytest basetemp INSIDE
it, and prove the NAMED refusal from claims (1)+(3) fires BEFORE any test,
and that the live shared-state surface -- posts.md, HANDOFF.md, every quorum
card, verify-suite-ts.json, the `.spawn-budget` lease set and `git log -1`
of the checked-out branch -- are byte-identical after the run. The throwaway
is removed in teardown.

IMPORTANT for any human running only this file: it adds a throwaway worktree
under /tmp at the CURRENT HEAD of the branch this test ships from (the code
that carries the conftest gate). The worktree is detached and removed by the
test; nothing is written to any shared tree.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

import locations

#: The live engine checkout this test ships from -- the main checkout a suite
#: may never write (git_common_root of every worktree, this one included).
LIVE = locations.git_common_root(Path(locations.__file__).resolve())

#: The repo this test file lives in (its own worktree), whose HEAD carries the
#: gate -- the commit the throwaway worktree must be checked out at.
REPO = Path(__file__).resolve()
while not (REPO / ".git").exists():
    REPO = REPO.parent

_HEAD = subprocess.run(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"],
    capture_output=True, text=True, check=True).stdout.strip()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _tree_hash(root: Path) -> dict[str, str]:
    """{relpath: sha} for every file under root, sorted by relpath."""
    out: dict[str, str] = {}
    if not root.is_dir():
        return out
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = _sha256(p)
    return out


def _snapshot() -> tuple[dict[str, str], str, str]:
    """The byte-identity surface: individual shared files + the two dirs."""
    files: dict[str, str] = {}
    for rel, p in {
        "posts.md": LIVE / ".agi/nodes/.geometry/posts.md",
        "HANDOFF.md": LIVE / "HANDOFF.md",
        "verify-suite-ts.json": LIVE / ".agi/sessions/verify-suite-ts.json",
    }.items():
        if p.is_file():
            files[rel] = _sha256(p)
    files.update({f"quorum/{k}": v
                  for k, v in _tree_hash(LIVE / ".agi/sessions/quorum").items()})
    files.update({f"spawn-budget/{k}": v for k, v in _tree_hash(
        LIVE / ".agi/sessions/.spawn-budget").items()})
    head = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%H %s"],
                          capture_output=True, text=True, check=True).stdout.strip()
    return files, head, str(subprocess.run(
        ["git", "-C", str(REPO), "status", "--porcelain"],
        capture_output=True, text=True).stdout)


def test_throwaway_worktree_basetemp_refuses_before_any_write(tmp_path):
    """A pytest run whose basetemp sits INSIDE a throwaway worktree of the live
    repo must refuse to start (exit 3, the named line) and must leave every
    shared-state byte where it found it."""
    wt = tmp_path / "throwaway-wt"
    try:
        subprocess.run(
            ["git", "-C", str(REPO), "worktree", "add", "--detach", str(wt),
             _HEAD],
            capture_output=True, text=True, check=True)
        before = _snapshot()

        res = subprocess.run(
            [sys.executable, "-m", "pytest",
             "extensions/agi/tests/test_suite_live_checkout.py", "-q",
             "--basetemp", str(wt / "basetemp"), "-p", "no:cacheprovider"],
            cwd=wt, capture_output=True, text=True)
        after = _snapshot()

        # claim (1)+(3): the NAMED refusal, exit 3, before any test counted.
        assert res.returncode == 3, f"expected exit 3, got {res.returncode}:\n{res.stdout}\n{res.stderr}"
        assert "refused: basetemp" in res.stdout + res.stderr
        assert str(wt) in res.stdout + res.stderr
        assert "passed" not in res.stdout.splitlines()[-1]

        # claim (4): byte-identical shared state after the refused run.
        assert after[0] == before[0], "shared-state files changed by a refused run"
        assert after[1] == before[1], "checked-out branch moved during a refused run"
        assert after[2] == before[2], "worktree became dirty during a refused run"
    finally:
        # Best-effort remove; a never-added worktree fails silently.
        subprocess.run(
            ["git", "-C", str(REPO), "worktree", "remove", "--force", str(wt)],
            capture_output=True, text=True)