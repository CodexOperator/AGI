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


def _seed_recovery_ack(gdir):
    """config:rotations `recovery_ack`, the cell heal's recover ack reads
    (hypothesis:heal-ack-line-comes-from-config-rotations-by-role)."""
    geo = Path(gdir) / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\nrecovery_ack:\n"
        "  prime_director: {recovered: \"RECOVERED SEAT {seat} --gen {gen}\","
        " resumed: \"RESUMED SEAT {seat} --gen {gen}\"}\n"
        "  default: {recovered: \"RECOVERED SEAT {seat}\","
        " resumed: \"RESUMED SEAT {seat}\"}\n---\n")


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
    _seed_recovery_ack(g)
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


def _launch_returning(graph, tmp_path, monkeypatch, ret, probe):
    """One sweep, OLD dead, the launcher returns `ret`, `_pane_pid_of` = `probe`."""
    monkeypatch.setattr(heal, "_pane_pid_of", probe)
    return heal._watch_seats(
        graph, now=time.time(), pid_alive=lambda p: False,
        window_path=str(tmp_path / "w.txt"),
        launcher=lambda *a, **k: ret)


def test_a_real_launcher_pid_wins_with_no_pane_probe(graph, tmp_path, monkeypatch):
    calls: list = []
    one = _launch_returning(graph, tmp_path, monkeypatch, (4242, "@77"),
                            lambda *a, **k: calls.append(a) or NEW)
    assert one[0]["respawned"] is True, one
    assert _row_pid(graph) == 4242 and calls == [], calls


def test_a_falsy_window_id_makes_no_pane_lookup(graph, tmp_path, monkeypatch):
    calls: list = []
    one = _launch_returning(graph, tmp_path, monkeypatch, (None, ""),
                            lambda *a, **k: calls.append(a) or NEW)
    assert one[0]["respawned"] is True, one
    assert _row_pid(graph) == OLD and calls == [], calls


def test_a_raising_pane_lookup_never_aborts_the_sweep(
        graph, tmp_path, monkeypatch, capsys):
    def boom(*a, **k):
        raise OSError("seam unreadable")
    one = _launch_returning(graph, tmp_path, monkeypatch, (None, "@77"), boom)
    assert one[0]["respawned"] is True, one
    assert _row_pid(graph) == OLD, "None = the row keeps its prior pid"
    assert "pane pid lookup raised: seam unreadable" in capsys.readouterr().err
    assert "pane pid lookup raised" in (tmp_path / "reaper.log").read_text()


def test_the_pane_pid_dies_with_the_agent_on_the_real_launch_line(
        graph, tmp_path):
    """DH.1 item 2(a): tmux runs `cd T && <shell_cmd>` as the pane command. The
    agent (via the launch-wrapper) is the LAST link of a pure `&&` chain, so the
    pane's shell is its parent and exits with it; a dead pane pid is then what the
    next sweep reads and the seat is re-judged (a third pass, pane dead -> respawn)."""
    import shlex
    cmd = _load("rotate")._shell_cmd(["agent", "--x"], None, seat="seat-a")
    lex = shlex.shlex("cd T && " + cmd, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    toks = list(lex)
    assert {t for t in toks if set(t) <= set("();<>|&")} == {"&&"}, toks
    assert toks.index("launch-wrapper") > max(i for i, t in enumerate(toks) if t == "&&")
    launches, one, two = _passes(graph, tmp_path, pane=f" {NEW}")
    assert two == [], two
    heal._watch_seats(graph, now=time.time() + 1500, pid_alive=lambda p: False,
                      window_path=str(tmp_path / "w.txt"),
                      launcher=lambda *a, **k: launches.append("again") or (None, "@78"))
    assert launches == ["seat-a", "again"], launches


def test_a_live_pane_pid_in_the_row_is_no_stale_row_and_no_second_respawn(
        graph, tmp_path, monkeypatch, capsys):
    """DH.2 item 1: the row pid is a PANE pid, the registry names a DIFFERENT live
    pid. The `pid_alive(row pid)` gate (heal.py `_watch_one_seat` 1a) returns {}
    before `_alive_via_pin` / the stale-row arm are ever read."""
    reg = tmp_path / "reg"
    reg.mkdir()
    (reg / "7777.json").write_text(json.dumps(
        {"pid": 7777, "session_id": "s-other", "tmux": "x @1"}))
    spy: list = []
    monkeypatch.setattr(heal, "_alive_via_pin", lambda *a: spy.append(a))
    launches, one, _t = _passes(graph, tmp_path, pane=f" {NEW}")
    assert _row_pid(graph) == NEW
    spy.clear()  # pass 1 judged the dead OLD pid; only the sweep below counts
    capsys.readouterr()
    two = heal._watch_seats(graph, now=time.time() + 700, registry_dir=str(reg),
                            pid_alive=lambda p: p in (NEW, 7777),
                            window_path=str(tmp_path / "w.txt"),
                            launcher=lambda *a, **k: launches.append("2nd") or (None, "@9"))
    assert two == [] and launches == ["seat-a"] and spy == [], (two, launches, spy)
    assert "stale-row" not in capsys.readouterr().err


def test_an_unknown_pane_pid_is_named_and_the_repeat_is_once_per_window(
        graph, tmp_path, capsys):
    """DH.2 item 2: the dead pid stays in the row, so the SEAT_DEAD_WINDOW_S
    once-guard is the bound: no repeat inside the window, one per window after."""
    launches: list = []
    t0 = time.time()
    (tmp_path / "w.txt").write_text("@1 other\n@77 fresh\n")
    heal._watch_seats(graph, now=t0, pid_alive=lambda p: False,
                      window_path=str(tmp_path / "w.txt"),
                      launcher=lambda *a, **k: launches.append("seat-a") or (None, "@77"))
    assert "pane pid unknown for @77" in capsys.readouterr().err
    assert "pane pid unknown for @77" in (tmp_path / "reaper.log").read_text()
    (tmp_path / "w.txt").write_text("@1 other\n")  # the new window died too
    for dt in (60, heal.SEAT_DEAD_WINDOW_S - 60):  # inside the window of pass 1
        heal._watch_seats(graph, now=t0 + dt, pid_alive=lambda p: False,
                          window_path=str(tmp_path / "w.txt"),
                          launcher=lambda *a, **k: launches.append("in") or (None, "@77"))
    assert launches == ["seat-a"], launches
    heal._watch_seats(graph, now=t0 + 2000, pid_alive=lambda p: False,
                      window_path=str(tmp_path / "w.txt"),
                      launcher=lambda *a, **k: launches.append("past") or (None, "@77"))
    assert launches == ["seat-a", "past"], launches
