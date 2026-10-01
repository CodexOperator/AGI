"""hypothesis:heal-crash-respawn-writes-the-new-pid-into-the-row.

The real recover launcher (`rotate.stand_up_launch`) reports `(None, @id)`: the
pid is not known from tmux. heal then wrote NO pid, the row kept the DEAD one,
and the next sweep re-judged the same corpse (measured: all-is-one pid 2871680
dead twice, 18:46Z and 19:00Z). The respawn now reads the new window's pane pid
(the `AGI_WINDOW_PATH` seam's third field) and writes it into the row, so one
dead process is one respawn. FAKES ONLY: fake launcher, fake process table,
fake window seam file; no tmux, claude or pi is ever touched.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
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
OLD, NEW = 999999, 5555


@pytest.fixture
def graph(tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.setenv("AGI_REAPER_LOG", str(tmp_path / "reaper.log"))
    g = tmp_path / "repo" / ".agi"
    (g / "sessions").mkdir(parents=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    p = g / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True)
    row = {"name": "seat-a", "role": "director", "model": "claude-opus-5",
           "pid": OLD, "window": "@50", "generation": 3}
    p.write_text("---\nid: config:seats\nseats:\n  - " + json.dumps(row)
                 + "\n---\n", encoding="utf-8")
    return g


def _row_pid(graph: Path) -> int:
    row = next(r for r in _load("rotate")._load_seats(graph)
               if r["name"] == "seat-a")
    return int(row.get("pid") or 0)


def _passes(graph: Path, tmp_path: Path, *, pane: str):
    """Pass 1 (OLD dead, launch lands as `(None, @77)`, pane pid `pane` on the
    seam), then pass 2 ten-plus minutes on (past the 600 s once-guard) with the
    window gone and ONLY the new pid alive. Returns (launches, pass1, pass2)."""
    launches: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        launches.append(name)
        return None, "@77"

    wf = tmp_path / "w.txt"
    wf.write_text(f"@1 other\n@77 fresh{pane}\n")
    t0 = time.time()
    one = heal._watch_seats(graph, now=t0, pid_alive=lambda p: p == NEW,
                            window_path=str(wf), launcher=launch)
    wf.write_text("@1 other\n")
    two = heal._watch_seats(graph, now=t0 + 700, pid_alive=lambda p: p == NEW,
                            window_path=str(wf), launcher=launch)
    return launches, one, two


def test_one_dead_process_is_one_respawn_and_the_row_carries_the_new_pid(
        graph, tmp_path):
    launches, one, two = _passes(graph, tmp_path, pane=f" {NEW}")
    assert len(one) == 1 and one[0]["respawned"] is True, one
    assert _row_pid(graph) == NEW, "the row still carries the dead pid"
    assert two == [] and launches == ["seat-a"], (two, launches)


def test_an_unknown_pane_pid_leaves_the_row_pid_alone(graph, tmp_path):
    """No third seam field = UNKNOWN: never a guessed pid (the ack resolves it)."""
    _l, one, _t = _passes(graph, tmp_path, pane="")
    assert one[0]["respawned"] is True, one
    assert _row_pid(graph) == OLD
