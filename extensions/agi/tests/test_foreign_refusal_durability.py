"""The foreign-row refusal is said ONCE per (row, cause) ACROSS PROCESSES.

hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused,
clause (3) — the `nudge_sweep` cron is a NEW PROCESS every tick (crons.py
`nudge_sweep`), so a process-local memo is empty on every tick and the same
refusal is re-printed forever. Two tests here drive the REAL boundary:

  * the durable memo, across SEPARATE `python3` invocations (not two calls in
    one process, which would prove nothing about a process-local set);
  * the box stamp, through the real seating call site
    `rotate._successor_row_write` (not a direct `_stamp_row_box` call, which
    would pass even if the call site were dead).

Temp graphs only; the live .agi, the live posts.md and every live pane are
untouched.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
BIN = HERE.parent / "bin"
sys.path.insert(0, str(BIN))

import rotate  # noqa: E402
import write  # noqa: E402

LIVE_SCHEMA = (HERE.parents[2] / ".agi" / "context" / "schemas" / "[config].md")

FOREIGN = {"name": "far-seat", "role": "director", "model": "m",
           "session_ref": "", "generation": 1, "window": "@9", "pid": 4242,
           "box": "sanctuary"}


def _graph(tmp_path: Path, rows: list[dict]) -> Path:
    """A temp project root whose config carries the memo cell, repo-relative."""
    agi = tmp_path / ".agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (agi / "context" / "schemas").mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text(json.dumps(
        {"paths": {"core": {"foreign_refusal_memo":
                            ".agi/sessions/foreign_refusals.tsv"}}}))
    (agi / "context" / "schemas" / "[config].md").write_text(
        LIVE_SCHEMA.read_text(encoding="utf-8"))
    head = ("---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
            "type: config\nparents:\n  - goal:g17\n")
    body = "\n".join("  - " + json.dumps(r) for r in rows)
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        head + "posts:\n" + body + "\n---\n\n# config:posts\n\nfixture\n")
    return agi


def _write_rows(root: Path, rows: list[dict]) -> None:
    posts = root / "nodes" / ".geometry" / "posts.md"
    head = posts.read_text(encoding="utf-8").rsplit("posts:\n", 1)[0]
    body = "\n".join("  - " + json.dumps(r) for r in rows)
    posts.write_text(head + "posts:\n" + body + "\n---\n\n# config:posts\n\nf\n",
                     encoding="utf-8")


# A real, separate interpreter: fresh import of send.py, fresh _FOREIGN_REFUSALS.
# Fake tmux SCREAMS on any send-keys, and a resolved (local) row exits non-zero.
_DRIVER = r'''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import send


class _R:
    returncode = 0
    stdout = "\n".join(("@1", "@9", "far-seat"))
    stderr = ""


def _run(argv, **kw):
    if "send-keys" in list(argv):
        raise SystemExit("SEND-KEYS into a foreign row")
    return _R()


send.subprocess.run = _run
got = send._nudge_target(Path(sys.argv[2]), sys.argv[3], None)
print("REFUSED" if got is None else "RESOLVED")
'''


def _sweep(root: Path, name: str = "far-seat",
           box: str = "local-town") -> subprocess.CompletedProcess:
    env = dict(os.environ, AGI_BOX=box)
    return subprocess.run(
        [sys.executable, "-c", _DRIVER, str(BIN), str(root), name],
        capture_output=True, text=True, timeout=120, cwd=str(root.parent),
        env=env)


# Two MORE real interpreters for the RACE: `_STALL` holds the rewrite open
# inside its swap window and drops a gate FILE (an observable signal -- no
# shared memory, no in-process event); `_NAMER` is the ordinary once-only
# naming path, exactly as `nudge_sweep` calls it.
_STALL = r'''
import os, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import send
root, gate, real = Path(sys.argv[2]), Path(sys.argv[3]), os.replace
send._OS_REPLACE = lambda s, d: (gate.write_text("held"),
                                 time.sleep(float(sys.argv[4])
                                            if len(sys.argv) > 4 else 2.0),
                                 real(s, d))[2]
send._forget_refusals("far-seat", root)
print("SWAPPED")
'''

_NAMER = r'''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import send
root = Path(sys.argv[2])
if len(sys.argv) > 3:        # an UNLOCKED pre-1f19e160c writer: bare append
    with send._foreign_memo_path(root).open("a", encoding="utf-8") as fh:
        fh.write("old-seat\tcore-town\n")
    print("APPENDED")
    sys.exit(0)
print("SAID" if send._foreign_refusal_said(
    root, "late-seat", "core-town") else "QUIET")
'''


def _raced_swap(tmp_path: Path, root: Path, sleep_s: str = "2.0"):
    """A real rewrite process, held open inside its swap window."""
    gate = tmp_path / "held"
    w = subprocess.Popen(
        [sys.executable, "-c", _STALL, str(BIN), str(root), str(gate),
         sleep_s],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(tmp_path))
    for _ in range(200):                      # 20s, then fail loudly
        if gate.exists():
            break
        time.sleep(0.1)
    assert gate.exists(), "the rewrite never reached its swap window"
    return w


def _said(res: subprocess.CompletedProcess) -> list[str]:
    return [ln for ln in res.stderr.splitlines() if "FOREIGN box row" in ln]


def test_falsifier_refusal_is_silent_in_the_NEXT_process(tmp_path):
    """FALSIFIER: two ticks of the same sweep, two PROCESSES, ONE line."""
    root = _graph(tmp_path, [FOREIGN])
    first = _sweep(root)
    assert "REFUSED" in first.stdout, first
    assert len(_said(first)) == 1 and "sanctuary" in _said(first)[0]
    second = _sweep(root)
    assert "REFUSED" in second.stdout
    assert _said(second) == [], second.stderr  # the tick that used to shout
    memo = tmp_path / ".agi" / "sessions" / "foreign_refusals.tsv"
    assert memo.read_text(encoding="utf-8").splitlines() == ["far-seat\tsanctuary"]


def test_falsifier_a_clean_sweep_in_a_later_process_re_names_the_cause(
        tmp_path):
    """A row that becomes addressable and foreign again under a NEW cause must
    be NAMED again — in a process that never held the old memo in memory."""
    root = _graph(tmp_path, [FOREIGN])
    assert len(_said(_sweep(root))) == 1
    _write_rows(root, [dict(FOREIGN, box="local-town")])
    clean = _sweep(root)                        # swept clean: memo must forget
    assert "RESOLVED" in clean.stdout, clean.stderr
    assert _said(clean) == []
    _write_rows(root, [dict(FOREIGN, box="core-town")])   # a DIFFERENT cause
    again = _sweep(root)
    assert len(_said(again)) == 1, again.stderr
    assert "core-town" in _said(again)[0]


# ------------------------------------------------- the stamp, through the CALLER


def test_seating_call_site_stamps_the_box(tmp_path, monkeypatch):
    """The stamp must be reached FROM the real seating writer. Calling
    `_stamp_row_box` directly would pass even if the call site were dead."""
    monkeypatch.setenv("AGI_BOX", "local-town")
    seen: list[dict] = []
    real = rotate._write_identity_cells

    def _spy(root, *, seat, actor, role, cells):  # noqa: ANN001
        seen.append(dict(cells))
        return real(root, seat=seat, actor=actor, role=role, cells=cells)

    monkeypatch.setattr(rotate, "_write_identity_cells", _spy)
    root = _graph(tmp_path, [{"name": "sanctuary-master",
                              "role": "prime_director", "model": "m",
                              "session_ref": "", "generation": 0, "window": ""},
                             {"name": "director-belam", "role": "director",
                              "model": "m", "session_ref": "", "generation": 0,
                              "window": ""}])
    out = rotate._successor_row_write(
        root, actor="director-belam", seat="director-belam", role="director",
        session_ref="agi-test", generation=1, window="@2", pid=7,
        session_id="sid-1", session_name="agi-test")
    assert "box=local-town" in out, out
    assert {"box": "local-town"} in seen, seen
    row = next(r for r in write._load_seats(root)
               if r["name"] == "director-belam")
    assert row["box"] == "local-town"


def test_a_reader_never_sees_a_torn_memo_while_a_rewrite_is_in_flight(
        tmp_path, monkeypatch):
    """The durable memo is rewritten by `_forget_refusals` while
    `_foreign_refusal_said` READS the same file (nudge_sweep every 2 min, and
    `wake --all-local` fanning out). A truncating `write_text` leaves a window
    in which a reader sees a partial/empty file and re-names an already-named
    refusal. The rewrite must go through a temp sibling + `os.replace`.

    FALSIFIER: with the old `path.write_text(...)` the hook below never fires
    (there is no replace to intercept), so `assert fired` fails."""
    import threading
    import send

    root = _graph(tmp_path, [FOREIGN])
    memo = tmp_path / ".agi" / "sessions" / "foreign_refusals.tsv"
    memo.parent.mkdir(parents=True, exist_ok=True)
    memo.write_text("far-seat\tsanctuary\nother\tcore-town\n", encoding="utf-8")

    gate = threading.Event()
    released = threading.Event()
    fired: list[bool] = []

    def _blocking_replace(src, dst):  # noqa: ANN001
        fired.append(True)
        gate.set()
        released.wait(30)          # hold the rewrite open, pre-swap
        return real_replace(src, dst)

    real_replace = os.replace
    # patch send._OS_REPLACE, NOT `os.replace`: `send.os IS os`, so patching the
    # module attribute would block EVERY thread in the interpreter for 30s.
    monkeypatch.setattr(send, "_OS_REPLACE", _blocking_replace)
    t = threading.Thread(target=send._forget_refusals, args=("far-seat", root))
    t.start()
    assert gate.wait(30), "no os.replace: the rewrite is not atomic"
    mid = memo.read_text(encoding="utf-8").splitlines()   # a reader lands here
    released.set()
    t.join(30)
    assert fired and mid == ["far-seat\tsanctuary", "other\tcore-town"], mid
    assert memo.read_text(encoding="utf-8").splitlines() == ["other\tcore-town"]


def test_a_naming_racing_the_rewrite_is_merged_not_discarded(tmp_path):
    """A naming landing between the rewrite's READ and its SWAP used to be
    DISCARDED (the swap carries the pre-race content), so that refusal was
    never named again -- and re-named on every later tick, forever. The
    read-filter-swap and the append must hold the SAME lock. TWO REAL
    PROCESSES: the writer stalls in the swap window, a second interpreter
    names. FALSIFIER: unlocked, the append lands in the window, the swap
    overwrites it, and `late-seat` is gone from the memo."""
    root = _graph(tmp_path, [FOREIGN])
    memo = tmp_path / ".agi" / "sessions" / "foreign_refusals.tsv"
    memo.parent.mkdir(parents=True, exist_ok=True)
    memo.write_text("far-seat\tsanctuary\nother\tcore-town\n", encoding="utf-8")
    writer = _raced_swap(tmp_path, root)
    try:
        namer = subprocess.run(
            [sys.executable, "-c", _NAMER, str(BIN), str(root)],
            capture_output=True, text=True, timeout=120, cwd=str(tmp_path))
        assert "SAID" in namer.stdout, namer.stderr
    finally:
        out, err = writer.communicate(timeout=60)
    assert "SWAPPED" in out, err
    assert memo.read_text(encoding="utf-8").splitlines() == [
        "other\tcore-town", "late-seat\tcore-town"]


def test_both_writer_classes_in_the_swap_window_merge_and_lose(tmp_path):
    """The writer-class comment (`_foreign_memo_lock`): inside the swap window a
    LOCK-TAKING naming is MERGED and an UNLOCKED one is LOST (it appended to
    the inode the swap discards). FALSIFIER: drop the flock, `old-seat` too."""
    root = _graph(tmp_path, [FOREIGN])
    memo = tmp_path / ".agi" / "sessions" / "foreign_refusals.tsv"
    memo.parent.mkdir(parents=True, exist_ok=True)
    memo.write_text("far-seat\tsanctuary\nother\tcore-town\n", encoding="utf-8")
    writer = _raced_swap(tmp_path, root, "8.0")
    try:
        for extra, want in ((["unlocked"], "APPENDED"), ([], "SAID")):
            r = subprocess.run([sys.executable, "-c", _NAMER, str(BIN),
                                str(root)] + extra, capture_output=True,
                               text=True, timeout=120, cwd=str(tmp_path))
            assert want in r.stdout, r
    finally:
        out, err = writer.communicate(timeout=60)
    assert "SWAPPED" in out, err
    assert memo.read_text(encoding="utf-8").splitlines() == [
        "other\tcore-town", "late-seat\tcore-town"]


def test_a_swapped_tmp_is_a_consumed_distinct_name(tmp_path, monkeypatch):
    """The `if not swapped` guard is cosmetic: after `_OS_REPLACE` the tmp ENTRY
    IS CONSUMED, the names are distinct, and a stale unlink of the tmp name
    leaves the memo INTACT. FALSIFIER: swap INTO the tmp name."""
    import send
    root = _graph(tmp_path, [FOREIGN])
    memo = tmp_path / ".agi" / "sessions" / "foreign_refusals.tsv"
    memo.parent.mkdir(parents=True, exist_ok=True)
    memo.write_text("far-seat\tsanctuary\nother\tcore-town\n", encoding="utf-8")
    seen: list[tuple[Path, Path]] = []
    real = send._OS_REPLACE
    monkeypatch.setattr(send, "_OS_REPLACE", lambda s, d: (
        real(s, d), seen.append((Path(s), Path(d))))[0])
    send._forget_refusals("far-seat", root)
    assert seen, "no swap: the rewrite is not atomic"
    src, dst = seen[0]
    assert not src.exists() and src != dst, (src, dst)
    src.unlink(missing_ok=True)               # the stale unlink, in full
    assert memo.read_text(encoding="utf-8").splitlines() == ["other\tcore-town"]
