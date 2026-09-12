"""hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning —
rotate-self's `_sweep_dead_hook_latches` sweep of the seat's dead
`hook-<seat>-gen*.lock` latches before it spawns the successor (P4).

A latch left by a rotate-self that DIED (or whose pid was reused) holds a
dead pid: it blocks nothing (the hook's own release fires only on the hook's
NEXT run), but it sits in sessions/rotations until the hook fires again, and
a Prime that notices it spends a WAKE call removing it by hand. rotate-self
therefore unlinks every latch for ITS seat whose holder pid is not alive
(`os.kill(pid,0)` fails, or the pid is unparseable/absent), printing ONE
stderr line naming each swept file, BEFORE spawning the successor. A latch
whose holder pid is alive is left alone; the sweep is best-effort and NEVER
refuses the rotation.

Three tests + the never-refuses / scoped-by-seat falsifier:
  (a) dead-pid latch is swept and NAMED          — the claim
  (b) live-pid latch is kept                     — falsifier 2
  (c) unparseable-pid latch is swept             — the claim's `unparseable`
  (d) other-seat latches + a missing dir survive — never-refuses, scoped
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

import rotate  # noqa: E402


def _dead_pid() -> int:
    """A pid PROVED dead: spawn a short-lived child, reap it, return its pid.
    A reaped child's pid cannot be killed with signal 0 (ProcessLookupError),
    so `_pid_alive` reads it dead — deterministic, unlike a hard-coded
    999999, which can be a live process on a box whose pid space reaches it."""
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
    proc.wait(timeout=10)
    pid = proc.pid
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    return pid


def _rot(tmp_path: Path) -> Path:
    p = tmp_path / "sessions" / "rotations"
    p.mkdir(parents=True, exist_ok=True)
    return p


def test_sweep_removes_dead_latch_and_names_it(tmp_path, capsys):
    """A dead-pid latch is unlinked and named on its one stderr line."""
    rot = _rot(tmp_path)
    latch = rot / "hook-adv-alive-gen1.lock"
    latch.write_text(f"pid {_dead_pid()} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert n == 1
    assert not latch.exists()
    err = capsys.readouterr().err
    assert "hook-adv-alive-gen1.lock" in err


def test_sweep_keeps_live_pid_latch(tmp_path, capsys):
    """A latch whose holder pid is alive is left alone (its rotate-self is
    still mid-flight)."""
    rot = _rot(tmp_path)
    latch = rot / "hook-adv-alive-gen2.lock"
    latch.write_text(f"pid {os.getpid()} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert n == 0
    assert latch.exists()
    assert capsys.readouterr().err == ""


def test_sweep_removes_unparseable_pid_latch(tmp_path, capsys):
    """A latch whose holder pid is unparseable/absent is dead: swept and
    named."""
    rot = _rot(tmp_path)
    names = ("hook-adv-alive-gen1.lock", "hook-adv-alive-gen3.lock")
    for name, content in ((names[0], "garbage\n"), (names[1], "")):
        (rot / name).write_text(content, encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert n == 2
    assert not list(rot.glob("hook-adv-alive-gen*.lock"))


def test_sweep_never_refuses_and_scopes_by_seat(tmp_path, capsys):
    """Other seats' latches are untouched; a missing latch dir is a
    best-effort no-op (both can never fail the rotation)."""
    rot = _rot(tmp_path)
    dead = _dead_pid()
    other = rot / "hook-other-seat-gen1.lock"
    other.write_text(f"pid {dead} hook\n", encoding="utf-8")
    own = rot / "hook-adv-alive-gen9.lock"
    own.write_text(f"pid {dead} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert n == 1
    assert other.exists()      # a different seat's latch survives
    assert not own.exists()
    # a root with no sessions/rotations dir at all: glob yields nothing.
    bare = tmp_path / "graphsolo"
    bare.mkdir(parents=True, exist_ok=True)
    assert rotate._sweep_dead_hook_latches(bare, "adv-alive") == 0


def test_sweep_reaches_own_tree_dir_when_split_from_shared(tmp_path, monkeypatch,
                                                           capsys):
    """REGRESSION (measuring a build-order gap, not a new claim): a
    linked-worktree seat's hook writes its latch to the seat's OWN tree
    (`root/sessions/rotations`) while `_rotations_dir` routes to the SHARED
    MAIN-sessions dir; a dead latch in the OWN tree must still be swept.

    Splits the two with a monkeypatched `_rotations_dir` (the pre-fix code
    globbed ONLY `_rotations_dir`, so the own-tree dead latch was left
    behind), plants a dead latch in the own-tree dir, and asserts it is
    swept and named."""
    own = tmp_path / "sessions" / "rotations"
    own.mkdir(parents=True, exist_ok=True)

    def _split_shared(root: Path) -> Path:
        return root / "sharedroom" / "rotations"

    monkeypatch.setattr(rotate, "_rotations_dir", _split_shared)

    latch = own / "hook-adv-split-gen1.lock"
    latch.write_text(f"pid {_dead_pid()} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-split")

    assert n == 1
    assert not latch.exists()
    assert "hook-adv-split-gen1.lock" in capsys.readouterr().err


def test_sweep_no_double_count_when_own_eq_shared(tmp_path, monkeypatch):
    """When the own-tree dir and `_rotations_dir` are the SAME physical dir
    (the main-checkout identity, and the plain-fixture shape the earlier
    tests already rely on), a dead latch is swept exactly once, never
    double-counted or double-printed. Forces the dirs to coincide by pointing
    `_rotations_dir` back at the own-tree dir."""
    own = tmp_path / "sessions" / rotate.ROTATIONS_DIR_NAME
    own.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(rotate, "_rotations_dir", lambda root: own)

    latch = own / "hook-adv-one-gen1.lock"
    latch.write_text(f"pid {_dead_pid()} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-one")

    assert n == 1            # swept once, not twice
    assert not latch.exists()