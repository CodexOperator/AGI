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
import json
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

    swept = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert swept == ["hook-adv-alive-gen1.lock"]
    assert not latch.exists()
    err = capsys.readouterr().err
    assert "hook-adv-alive-gen1.lock" in err


def test_sweep_writes_line_to_log_sink_in_addition_to_stderr(tmp_path, capsys):
    """SL7.83 (a): each swept line is appended to the production launch
    path's log (`log_path`) IN ADDITION to stderr — the launch path discards
    the spawn's stderr, so without the log sink a sweep leaves no trace."""
    rot = _rot(tmp_path)
    latch = rot / "hook-adv-log-gen1.lock"
    latch.write_text(f"pid {_dead_pid()} hook\n", encoding="utf-8")
    log = tmp_path / "seats" / "adv-log.wrapper.log"
    log.parent.mkdir(parents=True, exist_ok=True)

    swept = rotate._sweep_dead_hook_latches(tmp_path, "adv-log", log_path=log)

    assert swept == ["hook-adv-log-gen1.lock"]
    body = log.read_text(encoding="utf-8")
    assert "swept dead hook latch hook-adv-log-gen1.lock" in body
    assert "[sweep:adv-log]" in body
    # the SINK line is in addition to the stderr line, not replacing it
    assert "hook-adv-log-gen1.lock" in capsys.readouterr().err


def test_sweep_empty_writes_nothing_to_log(tmp_path, capsys):
    """SL7.83 (c): a sweep with nothing to sweep adds NO noise line to the
    log and no key content beyond the empty list the record carries."""
    rot = _rot(tmp_path)
    latch = rot / "hook-adv-clean-gen1.lock"
    latch.write_text(f"pid {os.getpid()} hook\n", encoding="utf-8")
    log = tmp_path / "adv-clean.wrapper.log"

    swept = rotate._sweep_dead_hook_latches(tmp_path, "adv-clean", log_path=log)

    assert swept == []
    assert latch.exists()
    assert not log.exists()      # nothing swept -> no log file even created
    assert capsys.readouterr().err == ""


def test_record_swept_latches_writes_key_and_empty_list(tmp_path):
    """SL7.83 (b): the rotation record carries `swept_latches` — the names
    when something was swept, an EMPTY list when none — never absent."""
    rec = tmp_path / "adv-record.20260912T000000Z.json"
    rec.write_text(json.dumps({"rotation": "rotate-self", "seat": "r1"})
                   + "\n", encoding="utf-8")

    rotate._record_swept_latches(rec, ["hook-r1-gen1.lock", "hook-r1-gen3.lock"])
    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert doc["swept_latches"] == ["hook-r1-gen1.lock", "hook-r1-gen3.lock"]

    rotate._record_swept_latches(rec, [])
    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert doc["swept_latches"] == []   # empty list, never absent


def test_swept_latches_survives_real_record_rewrite_order(tmp_path):
    """SL7.83 (b) REAL ORDERING: the key those helpers write must survive
    every subsequent in-place rewrite on the live `cmd_rotate_self` path.
    `_write_rotate_self_started` builds a FRESH dict each call and would
    clobber `swept_latches` written just earlier by `_record_swept_latches`;
    this drives the exact ordering (record writers interleaved) and asserts
    the fact is still present with its value at the end — the record the
    successor's STARTUP reads. Fails on the pre-SL7.83 code."""
    rec = tmp_path / "adv-order.20260912T120000Z.json"
    seat = "adv-order"

    # (2) an earlier in-progress write exists first (reaches `started`), as
    #     on the live path where the sweep happens AFTER a first started write.
    rotate._write_rotate_self_started(rec, seat=seat, steps=["handoff"],
                                      gen_before=1, gen_after=2)
    # the pre-spawn sweep lands its key into that same file.
    rotate._record_swept_latches(rec, ["hook-adv-order-gen1.lock"])
    # then the LATER step rewrites clobber it — exactly the live ordering at
    # ~12893, ~13284, ~13306 before the outcome.
    rotate._write_rotate_self_started(rec, seat=seat,
                                      steps=["handoff", "spawn"],
                                      gen_before=1, gen_after=2)
    rotate._write_rotate_self_started(rec, seat=seat,
                                      steps=["handoff", "spawn", "join"],
                                      gen_before=1, gen_after=2)

    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert doc["swept_latches"] == ["hook-adv-order-gen1.lock"]
    assert doc["steps_reached"] == ["handoff", "join", "spawn"]

    # the final in-place OUTCOME write (`_write_rotation_record`) must too.
    rotate._write_rotation_record(
        tmp_path, rotate._rotate_self_record(
            seat=seat, result="success", gen_before=1, gen_after=2),
        path=rec)
    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert doc["swept_latches"] == ["hook-adv-order-gen1.lock"]


def test_swept_latches_empty_survives_real_ordering(tmp_path):
    """SL7.83 (b) EMPTY-LIST case of the real ordering: when nothing was
    swept the key is still written (as `[]`) and still survives every later
    rewrite — never absent, exactly the contract the successor's STARTUP
    reads."""
    rec = tmp_path / "adv-empty.20260912T120000Z.json"
    seat = "adv-empty"

    rotate._write_rotate_self_started(rec, seat=seat, steps=["handoff"],
                                      gen_before=1, gen_after=2)
    rotate._record_swept_latches(rec, [])     # nothing swept -> empty list
    rotate._write_rotate_self_started(rec, seat=seat,
                                      steps=["handoff", "spawn"],
                                      gen_before=1, gen_after=2)

    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert doc["swept_latches"] == []        # present, empty, never absent


def test_swept_latches_absent_from_a_record_with_no_sweep(tmp_path):
    """SL7.83 (b) negative: a record that was NEVER given the sweep key does
    not gain one from the preserve-helper's read-back (the pre-spawn refusal
    paths at ~13058/~13086 write a record without running the sweep, so
    they must stay sweep-free — a successor is never spawned for them)."""
    rec = tmp_path / "adv-none.20260912T120000Z.json"
    rec.write_text(json.dumps({"rotation": "rotate-self", "seat": "s9"})
                   + "\n", encoding="utf-8")

    rotate._write_rotate_self_started(rec, seat="s9", steps=["handoff"])

    doc = json.loads(rec.read_text(encoding="utf-8"))
    assert "swept_latches" not in doc



def test_sweep_keeps_live_pid_latch(tmp_path, capsys):
    """A latch whose holder pid is alive is left alone (its rotate-self is
    still mid-flight)."""
    rot = _rot(tmp_path)
    latch = rot / "hook-adv-alive-gen2.lock"
    latch.write_text(f"pid {os.getpid()} hook\n", encoding="utf-8")

    n = rotate._sweep_dead_hook_latches(tmp_path, "adv-alive")

    assert n == []
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

    assert n == list(names)
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

    assert n == ["hook-adv-alive-gen9.lock"]
    assert other.exists()      # a different seat's latch survives
    assert not own.exists()
    # a root with no sessions/rotations dir at all: glob yields nothing.
    bare = tmp_path / "graphsolo"
    bare.mkdir(parents=True, exist_ok=True)
    assert rotate._sweep_dead_hook_latches(bare, "adv-alive") == []


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

    assert n == ["hook-adv-split-gen1.lock"]
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

    assert n == ["hook-adv-one-gen1.lock"]   # swept once, not twice
    assert not latch.exists()

def test_preserve_never_overwrites_a_fresh_sweep(tmp_path):
    """(i) the preserve helper must NOT clobber a sweep THIS run already
    measured: when `rec` carries its own `swept_latches`, the on-disk record's
    STALE list (a re-run on an old record path) is left alone and the rec is
    not marked inherited. Fails on the pre-fix code, which copied the on-disk
    list unconditionally."""
    stale = tmp_path / "adv-stale.20260912T120000Z.json"
    stale.write_text(json.dumps(
        {"swept_latches": ["hook-adv-old-gen1.lock"]})
        + "\n", encoding="utf-8")
    rec = {"rotation": "rotate-self", "seat": "adv-stale",
           "swept_latches": ["hook-adv-new-gen1.lock"]}

    rotate._preserve_swept_latches(rec, stale)

    assert rec["swept_latches"] == ["hook-adv-new-gen1.lock"]   # fresh wins
    assert "inherited" not in rec


def test_preserve_inherits_stale_list_and_marks_it(tmp_path):
    """(i) a rec with NO sweep of its own carries the on-disk list forward and
    is marked `inherited: true`, so a reader can tell a MEASURED sweep from a
    CARRIED one. Fails on the pre-fix code (no inherited marker)."""
    stale = tmp_path / "adv-carried.20260912T120000Z.json"
    stale.write_text(json.dumps(
        {"swept_latches": ["hook-adv-old-gen1.lock"]})
        + "\n", encoding="utf-8")
    rec = {"rotation": "rotate-self", "seat": "adv-carried"}

    rotate._preserve_swept_latches(rec, stale)

    assert rec["swept_latches"] == ["hook-adv-old-gen1.lock"]
    assert rec.get("inherited") is True
