"""hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-
while-the-suite-lock-is-held — `grid.py commit --all` on the cron path (no
--session) defers the evidence-gate rewrite of node FILES under MAIN while a
LIVE foreign pid holds the suite lock; a removed or dead-pid lock demotes as
today (tick, never skip).

The required held-lock test runs `grid.py commit --all` as a SUBPROCESS so the
gate process's pid differs from the test process that wrote the lock —
`acquire_suite_lock` treats `holder == os.getpid()` as stale, so the test's
own live pid must read as a LIVE FOREIGN holder, the exact case the gate must
defer. Fixture root throughout; never the live tree.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
GRID = str(BIN / "grid.py")
MINT = "h1h1h1h1h1h1h1h1h1h1h1h1h1h1h1h1"

# Harness env vars would re-resolve the project root away from the fixture or
# install the worktree's agent-git hook onto the fixture repo. Strip them so
# the subprocess resolves the fixture and only the fixture.
STRIP = {
    "AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT",
    "AUTORESEARCH_TREE_PROJECT_ROOT", "PROJECT_ROOT", "AGI_TIER",
    "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0",
}


def _clean_env():
    env = dict(os.environ)
    for k in list(env):
        if k in STRIP:
            env.pop(k, None)
    return env


def _build(root: Path) -> Path:
    """A legacy fixture root: one unevidenced `proved` experiment node."""
    subprocess.run(["git", "init", "-q", str(root)], check=True,
                   capture_output=True)
    (root / "agi-tree.config.json").write_text("{}")
    d = root / "nodes" / "experiment"
    d.mkdir(parents=True)
    node = d / "h.md"
    node.write_text(
        f'---\nid: "experiment:h"\nmint_id: {MINT}\ntype: experiment\n'
        f"verdict: proved\n---\n\nbody\n"
    )
    return node


def _commit_all(root: Path):
    return subprocess.run(["python3", GRID, "commit", "--all"],
                          cwd=str(root), env=_clean_env(),
                          capture_output=True, text=True)


def _lock(root: Path, pid: int) -> Path:
    p = root / "sessions" / "verify-suite.lock"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(pid))
    return p


def _node_ref_versions(root: Path) -> int:
    out = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--count",
         f"refs/grid/node/{MINT}"],
        capture_output=True, text=True).stdout.strip()
    return int(out) if out.isdigit() else 0


def test_held_lock_defers_rewrite_and_refs_still_write(tmp_path):
    node = _build(tmp_path)
    before = node.read_text()
    _lock(tmp_path, os.getpid())  # test's own live pid = live FOREIGN holder

    r = _commit_all(tmp_path)

    assert r.returncode == 0
    # byte-identical: the gate neither demoted nor planted even its own pid
    assert node.read_text() == before
    assert "verdict: proved" in node.read_text()
    # exactly ONE named line
    assert r.stderr.count(
        f"evidence gate deferred: suite lock held by pid {os.getpid()}") == 1
    # refs still written for the already-committed bytes
    assert _node_ref_versions(tmp_path) == 1


def test_deferral_is_a_tick_not_a_skip(tmp_path):
    node = _build(tmp_path)
    lock = _lock(tmp_path, os.getpid())

    first = _commit_all(tmp_path)          # held -> deferred, node stays proved
    assert first.stderr.count(
        f"evidence gate deferred: suite lock held by pid {os.getpid()}") == 1
    assert "verdict: proved" in node.read_text()

    lock.unlink()                           # lock frees
    second = _commit_all(tmp_path)          # next tick demotes what it would have
    assert "deferred" not in second.stdout + second.stderr
    assert node.read_text() != "proved" and node.read_text() \
        .count("verdict: inconclusive_lean_proved:50") == 1


def test_stale_dead_pid_lock_never_defers(tmp_path):
    node = _build(tmp_path)
    dead = os.fork()  # a child that exits immediately -> a real, now-dead pid
    if dead == 0:
        os._exit(0)
    os.waitpid(dead, 0)
    _lock(tmp_path, dead)

    r = _commit_all(tmp_path)               # stale never defers: demote first call
    assert "deferred" not in r.stdout + r.stderr
    assert node.read_text().count("verdict: inconclusive_lean_proved:50") == 1