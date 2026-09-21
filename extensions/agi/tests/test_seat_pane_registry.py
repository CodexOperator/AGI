"""goal:g7.31.2.1 — seat-start registry pin matches live tmux.

hypothesis:a00-aa592d9a-c374ea.

Falsifier, verbatim: after seat start, posts/seat registry shows occupied
with the live pane/session pin matching `tmux`.

Two halves, both asserted on the WIRE bytes / the returned value:

  WRITE (cmd_spawn, no live tmux): the seat row written into the graph's
  seats.md carries `window == "@7"` — the @id the tmux READER
  (`tmux list-windows`, stubbed here by a `window_path` seam file) would
  return — plus `generation`/`session_ref`/`pid` cells. A JOIN miss must
  commit pid 0 and an empty session_ref, never the predecessor's stale pid.

  NEGATIVE CONTROL: with the seat absent from the window list, the row must
  NOT claim a window tmux does not have.

  READ (seat_status.pane_coherent): a row whose `window` @id does not match
  live tmux is reported as drift BY SEAT NAME, and with tmux absent the
  helper FAILS OPEN (None, no crash), matching seat_status's contract.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402
import seat_status as SS  # noqa: E402

# Deliberately the LIVE pytest process: the positive occupation tests run the
# REAL rotate._pid_alive against an actually-alive pid, so the alive branch
# these tests exist to cover is never stubbed away. The dead-pid negative test
# keeps its literal 999999999.
_LIVE_PID = os.getpid()


def _graph(tmp_path, rows):
    """A real `.agi` graph root (the write API resolves descend-only) whose
    config:seats registry carries `rows`."""
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "x"}',
                                       encoding="utf-8")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_name, session_id, generation, window, "
        "pid, pubkey, sig_scheme, enc_scheme, key_history, session_label]}\n"
        "---\nbody\n", encoding="utf-8")
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (graph / "nodes" / ".geometry" / "seats.md").write_text(body,
                                                            encoding="utf-8")
    return graph


def _spawn_args(seat="director-seat", wins=None, reg=None):
    return SimpleNamespace(
        name=seat, tier="kid", prompt_file=None, model=None, effort=None,
        settings=None, tmux_session="agi-rc", window_path=wins,
        dry_run=False, successor_argv=None, seat=seat, pid=None,
        no_autopsy=True, registry_dir=reg, harness=None,
    )


@pytest.fixture
def spawned(monkeypatch):
    """Capture spawn_window; model the real sequence — the seat's window is
    ABSENT at the pre-spawn gate and PRESENT after the launch. `box['after']`
    is what the launch leaves in the tmux window list."""
    calls = []
    box = {"after": ""}

    def fake_spawn_window(**kw):
        calls.append(kw)
        wp = kw.get("window_path")
        if wp:
            Path(wp).write_text(box["after"], encoding="utf-8")
        return 0, "echo ok"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn_window)
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    monkeypatch.setattr(rotate, "_first_seating_run",
                        lambda *a, **k: ("", []))
    return calls, box


def _row(graph, name):
    """The seat row exactly as it lives on the wire in seats.md."""
    fm = yaml.safe_load((graph / "nodes" / ".geometry" / "seats.md")
                        .read_text(encoding="utf-8").split("---")[1])
    return next(r for r in fm["seats"] if r.get("name") == name)


def _run(tmp_path, spawned, rows, after, seat="director-seat"):
    calls, box = spawned
    wins = tmp_path / "winlist"
    wins.write_text("", encoding="utf-8")           # absent at the gate
    box["after"] = after                            # the launch brings it up
    graph = _graph(tmp_path, rows)
    rc = rotate.cmd_spawn(
        _spawn_args(seat=seat, wins=str(wins), reg=str(tmp_path / "noreg")),
        graph)
    assert rc == 0, rc
    return _row(graph, seat)


# ---- WRITE side: the row the seat start commits ------------------------- #

def test_seat_start_registers_the_live_tmux_pin(tmp_path, spawned):
    """Positive: the row's `window` cell == the @id tmux would report."""
    r = _run(tmp_path, spawned,
             [{"name": "director-seat", "role": "director",
               "session_kind": "remote-control"}],
             "@7 director-seat\n")
    assert r.get("window") == "@7", r
    # identity cells present and coherent; the JOIN missed (empty registry),
    # so pid is the EMPTY sentinel 0 and session_ref is empty.
    assert "generation" in r, r
    assert r.get("pid") == 0, r
    assert r.get("session_ref") in ("", None), r


def test_seat_start_join_miss_never_keeps_the_stale_row_pid(
        tmp_path, spawned):
    """A join MISS commits EMPTY pid/session_ref, never the stale row pid."""
    r = _run(tmp_path, spawned,
             [{"name": "director-seat", "role": "director",
               "pid": 999999, "session_ref": "stale-ref"}],
             "@7 director-seat\n")
    assert r.get("pid") == 0, r
    assert r.get("session_ref") in ("", None), r


def test_seat_start_without_a_live_window_claims_no_occupation(
        tmp_path, spawned):
    """Negative control: no live pane -> no window claim in the registry."""
    r = _run(tmp_path, spawned,
             [{"name": "director-seat", "role": "director"}],
             "@9 somebody-else\n")
    assert not r.get("window"), r


# ---- READ side: seat_status.pane_coherent ------------------------------- #

def test_pane_coherent_true_when_pin_matches_live(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    assert SS.pane_coherent({"name": "director-seat", "window": "@7"},
                            "agi-rc", str(wins)) is True


def test_pane_coherent_names_drift_by_seat(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    out = SS.pane_coherent({"name": "director-seat", "window": "@9"},
                           "agi-rc", str(wins))
    assert isinstance(out, str) and "director-seat" in out and "@9" in out, out


def test_pane_coherent_names_a_missing_live_window(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 somebody-else\n", encoding="utf-8")
    out = SS.pane_coherent({"name": "director-seat", "window": "@7"},
                           "agi-rc", str(wins))
    assert isinstance(out, str) and "director-seat" in out, out


def test_pane_coherent_fails_open_without_tmux(tmp_path, monkeypatch):
    monkeypatch.setattr(SS.shutil, "which", lambda _n: None)
    assert SS.pane_coherent({"name": "director-seat", "window": "@7"},
                            "agi-rc", None) is None


def test_pane_coherent_fails_open_when_the_seam_is_absent(tmp_path):
    assert SS.pane_coherent({"name": "director-seat", "window": "@7"},
                            "agi-rc", str(tmp_path / "missing")) is None

# ---- READ side: seat_status.seat_occupation (pane + pid) ----------------- #

def test_seat_occupation_occupied_when_window_and_pid_agree(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    occ = SS.seat_occupation(
        {"name": "director-seat", "window": "@7", "pid": _LIVE_PID},
        "agi-rc", str(wins))
    assert occ is not None, occ
    assert occ["state"] == "occupied", occ
    assert occ["window"] == "@7" and occ["live"] == "@7", occ
    assert occ["pid_alive"] is True, occ


def test_seat_occupation_pane_drift_when_row_window_is_stale(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    occ = SS.seat_occupation(
        {"name": "director-seat", "window": "@9", "pid": _LIVE_PID},
        "agi-rc", str(wins))
    assert occ["state"] == "pane-drift", occ
    assert occ["window"] == "@9" and occ["live"] == "@7", occ


def test_seat_occupation_pane_drift_when_dead_pid_owns_a_matching_window(
        tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    occ = SS.seat_occupation(
        {"name": "director-seat", "window": "@7", "pid": 999999999},
        "agi-rc", str(wins))
    assert occ["state"] == "pane-drift", occ
    assert occ["pid_alive"] is False, occ


def test_seat_occupation_unoccupied_when_no_window_answers_the_name(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 somebody-else\n", encoding="utf-8")
    occ = SS.seat_occupation(
        {"name": "director-seat", "window": "@7"}, "agi-rc", str(wins))
    assert occ["state"] == "unoccupied", occ
    assert occ["live"] is None, occ


def test_seat_occupation_fails_open_without_tmux(tmp_path, monkeypatch):
    monkeypatch.setattr(SS.shutil, "which", lambda _n: None)
    assert SS.seat_occupation(
        {"name": "director-seat", "window": "@7"}, "agi-rc", None) is None


def test_seat_occupation_fails_open_when_the_seam_is_absent(tmp_path):
    assert SS.seat_occupation(
        {"name": "director-seat", "window": "@7"},
        "agi-rc", str(tmp_path / "missing")) is None


# ---- the INJECTED view: occupation reaches to_markdown/to_compact --------- #

def test_collect_without_a_seam_computes_no_occupation(tmp_path):
    """Byte-identical contract: no seam -> no occupation cell anywhere."""
    graph = _graph(tmp_path, [{"name": "director-seat", "role": "director"}])
    v = SS.collect(graph, {})
    assert all(s.get("occupation") is None for s in v.seats), v.seats
    text = "\n".join(SS.to_markdown(v)) + "\n".join(SS.to_compact(v))
    assert "pane=" not in text, text


def test_collect_with_a_window_seam_renders_occupation_both_views(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    graph = _graph(tmp_path, [{"name": "director-seat", "role": "director",
                               "window": "@7", "pid": _LIVE_PID}])
    v = SS.collect(graph, {}, tmux_session="agi-rc", window_path=str(wins))
    occ = v.seats[0]["occupation"]
    assert occ and occ["state"] == "occupied", occ
    assert "pane=occupied(@7)" in "\n".join(SS.to_compact(v))
    assert "pane=occupied(@7)" in "\n".join(SS.to_markdown(v))


def test_collect_with_the_seam_renders_drift(tmp_path):
    wins = tmp_path / "winlist"
    wins.write_text("@7 director-seat\n", encoding="utf-8")
    graph = _graph(tmp_path, [{"name": "director-seat", "role": "director",
                               "window": "@9"}])
    v = SS.collect(graph, {}, tmux_session="agi-rc", window_path=str(wins))
    assert v.seats[0]["occupation"]["state"] == "pane-drift", v.seats
    assert "pane=pane-drift(row @9 live @7)" in "\n".join(SS.to_compact(v))
