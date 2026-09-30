"""goal:g7.16.1.7.1.1.4 -- ONE stand-up verb.

`rotate.stand_up` (lock -> resolve -> launch -> row write) is the one code
path under all four modes: a seated spawn, a rotate-self successor, a heal
recovery and a hand restart (`rotate.py stand-up --post <p>`). Each mode is
driven for a dummy post and the verb's core is counted. Negative: no
`launch_in_window` / `post_launch_lock` caller outside the verb's core.
Every launch goes to a fake launcher or stops at a sentinel; no tmux.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import heal  # noqa: E402
import rotate  # noqa: E402
from test_rotate_handover import (  # noqa: E402,F401
    _fix, _rotate_self_args, _write_seats_sheet)

BIN = Path(rotate.__file__).resolve().parent
DEAD_PID = 99_999_999  # above any pid_max: never a live process


@pytest.fixture
def calls(monkeypatch):
    seen: list = []
    real = rotate.stand_up

    def counting(root, post, body, *, mode):
        seen.append((post, mode))
        return real(root, post, body, mode=mode)

    monkeypatch.setattr(rotate, "stand_up", counting)
    return seen


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    g = tmp_path / "repo" / ".agi"
    (g / "sessions").mkdir(parents=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    p = g / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True)
    row = {"name": "seat-a", "role": "director", "pid": DEAD_PID,
           "window": "@50", "generation": 2, "model": "m-1"}
    p.write_text("---\nid: config:seats\nseats:\n  - " + json.dumps(row)
                 + "\n---\n", encoding="utf-8")
    (g / "windows.txt").write_text("\n@1 other\n", encoding="utf-8")
    return g


def _launcher(seen: list):
    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append(name)
        return 424243, "@556"
    return launch


def test_spawn_is_a_stand_up(tmp_path, calls, monkeypatch):
    monkeypatch.setattr(rotate, "_cmd_spawn", lambda args, root: 0)
    assert rotate.cmd_spawn(NS(seat="p1", dry_run=False), tmp_path) == 0
    assert calls == [("p1", "spawn")]


def test_recover_is_a_stand_up(graph, calls):
    launched: list = []
    heal._watch_seats(graph, pid_alive=lambda pid: False,
                      window_path=str(graph / "windows.txt"),
                      launcher=_launcher(launched))
    assert calls == [("seat-a", "recover")] and launched, (calls, launched)


def test_hand_restart_is_a_stand_up(graph, calls, capsys):
    launched: list = []
    rc = rotate.cmd_stand_up(
        NS(post="seat-a", window_path=str(graph / "windows.txt")), graph,
        launcher=_launcher(launched))
    assert rc == 0 and calls == [("seat-a", "restart")], capsys.readouterr()
    assert len(launched) == 1, launched
    recs = sorted((graph / "sessions" / "rotations").glob("seat-a.*.json"))
    rec = json.loads(recs[-1].read_text())
    assert rec["result"] == "respawned" and rec["probable_cause"] == "hand-restart"
    assert "stood up seat-a (fresh)" in capsys.readouterr().out


def test_hand_restart_refuses_a_live_post(graph, calls, capsys):
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.write_text(p.read_text().replace(str(DEAD_PID), str(os.getpid())))
    launched: list = []
    rc = rotate.cmd_stand_up(
        NS(post="seat-a", window_path=str(graph / "windows.txt")), graph,
        launcher=_launcher(launched))
    assert rc == 1 and calls == [] and launched == []
    assert "is alive" in capsys.readouterr().err


def test_rotate_self_successor_is_a_stand_up(_fix, tmp_path, monkeypatch):
    class _Stop(Exception):
        pass

    seen: list = []

    def stop(root, post, body, *, mode):
        seen.append((post, mode))
        raise _Stop

    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max",
                                   "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "stand_up", stop)
    with pytest.raises(_Stop):
        rotate.cmd_rotate_self(_rotate_self_args(tmp_path, window_path=str(win)),
                               tmp_path)
    assert seen == [("adv-alive", "rotate")]


def _callers(fn_name: str) -> set:
    out = set()
    for f in sorted(BIN.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    c = node.func
                    name = getattr(c, "attr", None) or getattr(c, "id", None)
                    if name == fn_name:
                        out.add((f.name, fn.name))
    return out


def test_no_launch_or_lock_outside_the_verbs_core():
    assert _callers("launch_in_window") == {
        ("rotate.py", "_launch_window"), ("rotate.py", "stand_up_launch")}
    assert _callers("post_launch_lock") == {("rotate.py", "stand_up")}
