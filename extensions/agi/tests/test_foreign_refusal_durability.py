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
