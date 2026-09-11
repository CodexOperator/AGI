"""goal:g15.17 residue — spawn/ack/rotate-self fixes (hypothesis:l4-spawn-
seats-without-a-root-with-the-rows-role-and-pins-at-the-rows-generation-and-
a-first-rotation-is-not-a-first-seating).

Covers the falsifiers, each as a behavior-to-build test:
  (a) `spawn --seat S` with root None seats the window and prints
      `[seating] no project root: template + bootstrap skipped` — no
      TypeError, exit 0.
  (b) a first seating's role is the SEAT ROW's role when a row exists,
      `--tier` only as the fallback (a director-seat first-seating record
      never homogenizes to a prime just because --tier defaulted).
  (e) a RE-spawn of an existing seat pins at the row's generation (row gen
      11 -> pin reads 11), never back at FIRST_SEATING_GEN.
  (c) `ack --gen 1` is a first seating ONLY when no rotation record AND no
      pending ack exist for the seat — a first ROTATION acked at gen 1 after
      a rotate-self emits nothing extra and writes no seating.json.
  (d)(ii) a join-only rotate-self (a role template that declares `startup`
      but strips first_turn) is refused BY NAME.
"""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate


def _seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _director_turn_rotations(root):
    """A config:rotations node whose director template declares a
    `startup.first_turn` probe — the block a first seating composes."""
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (root / "bin").mkdir(parents=True, exist_ok=True)
    (root / "bin" / "probe_g15.py").write_text(
        "import sys\nprint(','.join(sys.argv[1:]))\n", encoding="utf-8")
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  director: {brief_file: x.md, steps: [spawn], telemetry: [seat],\n"
        "    startup: {first_turn: [{label: probe, "
        "cmd: \"python3 {repo}/bin/probe_g15.py {seat} gen={gen}\"}]}}\n"
        "---\n\nbody\n", encoding="utf-8")


def _registry(root, raw="@42"):
    reg = root / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "999.json").write_text(json.dumps({
        "window_id": raw, "session_id": "2717-aaaa",
        "transcript": "t.jsonl", "cwd": str(root)}), encoding="utf-8")
    return reg


# ---- (a) spawn --seat with root None: seat the window, skip template ---- #

def test_spawn_seat_no_project_root_skips_template(tmp_path, monkeypatch,
                                                   capsys):
    """`spawn --seat S` OUTSIDE any project root (root None) must NOT crash
    on Path(None) -> _rotations_node_path; it seats the window and prints the
    named skip (SL2.02 refuter's reproduction becomes a test)."""
    calls = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: calls.append(kw) or (0, "echo ok"))
    args = SimpleNamespace(name="dir-x", tier="kid", prompt_file=None,
                           model=None, effort=None, settings=None,
                           tmux_session="agi-rc", window_path=None,
                           dry_run=True, successor_argv=None, seat="dir-x",
                           pid=None, no_autopsy=True)
    rc = rotate.cmd_spawn(args, None)          # root = None
    assert rc == 0, f"root-less spawn --seat must exit 0, got {rc}"
    assert calls, "the window must still be spawned (seated) without a root"
    out = capsys.readouterr().out
    assert "[seating] no project root: template + bootstrap skipped" in out
    # the generic seat-less branch is untouched when root is None too
    args2 = SimpleNamespace(name="gen-x", tier="kid", prompt_file=None,
                            model=None, effort=None, settings=None,
                            tmux_session="agi-rc", window_path=None,
                            dry_run=True, successor_argv=None, seat=None,
                            pid=None, no_autopsy=True)
    rc2 = rotate.cmd_spawn(args2, None)
    assert rc2 == 0


# ---- (b)+(e) spawn uses row role; re-spawn pins at the row's generation - #

def test_spawn_first_seating_role_from_row_and_pin_at_row_gen(
        tmp_path, monkeypatch):
    """A first seating through a NON-dry `spawn --seat` takes its role from
    the SEAT ROW (a director row never records as a prime even when --tier
    defaults to prime_director) and pins the meter at the row's generation
    (row gen 11 -> pin reads 11), not back at FIRST_SEATING_GEN."""
    import send as _send
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control",
         "generation": 11},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _seats_sheet(tmp_path, rows)
    _director_turn_rotations(tmp_path)
    wins = tmp_path / "windows.txt"
    wins.write_text("@42 director-seat\nsensei-peer\n", encoding="utf-8")
    reg = _registry(tmp_path)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender:
                        sent.append((other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo ok"))
    args = SimpleNamespace(name="director-seat", tier="prime_director",
                           prompt_file=None, model=None, effort=None,
                           settings=None, tmux_session="agi-rc",
                           window_path=str(wins), dry_run=False,
                           successor_argv=None, seat="director-seat",
                           registry_dir=str(reg), pid=None, no_autopsy=True)
    rc = rotate.cmd_spawn(args, tmp_path)
    assert rc == 0

    recs = list(rotate._rotations_dir(tmp_path)
                .glob("director-seat.*.seating.json"))
    assert len(recs) == 1, f"exactly ONE seating record, got {recs}"
    rec = json.loads(recs[0].read_text(encoding="utf-8"))
    # (b): the record carries the ROW role, never the defaulted --tier.
    assert rec["role"] == "director", \
        f"first-seating role must come from the row, got {rec['role']!r}"
    # the announcement payload got the row role through the same record
    assert sent, "a first seating must still alert"
    # (e): the re-spawn pins at the row's generation, never at 1.
    pin = (tmp_path / "sessions" / "director-seat.meter").read_text(
        encoding="utf-8")
    assert pin.startswith("11\t"), f"pin must read the row gen 11, got {pin!r}"
    ack = json.loads((rotate._ack_path(tmp_path, "director-seat")).read_text(
        encoding="utf-8"))
    assert ack["gen_after"] == 11, \
        f"spawn's ack gen_after must follow the row gen, got {ack['gen_after']}"


# ---- (c) a first rotation acked at gen 1 is NOT a first seating ---------- #

def test_ack_gen1_after_rotate_self_emits_nothing(tmp_path, monkeypatch):
    """A first ROTATION acked at --gen 1 (rotate-self already wrote a rotation
    record AND a pending ack before the successor joins) is NOT a first
    seating: cmd_ack announces nothing and writes no seating.json."""
    import send as _send
    rows = [
        {"name": "rotated-seat", "role": "director"},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _seats_sheet(tmp_path, rows)
    # the rotation record rotate-self wrote before the successor joined
    rot = rotate._rotations_dir(tmp_path)
    rot.mkdir(parents=True, exist_ok=True)
    (rot / "rotated-seat.20260911T000000Z.json").write_text(
        json.dumps({"rotation": "rotate-self", "seat": "rotated-seat",
                    "result": "success"}) + "\n", encoding="utf-8")
    # the pending ack rotate-self wrote before the successor joined
    seats = tmp_path / "sessions" / "seats"
    seats.mkdir(parents=True, exist_ok=True)
    (seats / "rotated-seat.ack.json").write_text(json.dumps({
        "seat": "rotated-seat", "gen_after": 1, "answer": "pending",
        "session_ref": "a11", "ts": "t"}) + "\n", encoding="utf-8")
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender:
                        sent.append((other, text)) or tmp_path)
    rc = rotate.cmd_ack(SimpleNamespace(seat="rotated-seat", gen=1, ref=None,
                                        answer="continue", text=None), tmp_path)
    assert rc == 0
    assert sent == [], \
        f"a first ROTATION acked at gen 1 must not announce a seating: {sent}"
    assert not list(rot.glob("rotated-seat.*.seating.json")), \
        "a first ROTATION must write no seating record"


# ---- (d)(ii) join-only rotate-self refused by name ----------------------- #

def test_rotate_self_refuses_join_only_template(tmp_path, monkeypatch,
                                                capsys):
    """A rotate-self whose role template DECLARES a startup but strips
    first_turn is a join-only seat — nothing to hand off — refused BY NAME
    before any side effect."""
    _seats_sheet(tmp_path, [
        {"name": "join-seat", "role": "director", "model": "m",
         "effort": "max", "settings": ""}])
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  director: {brief_file: x.md, steps: [spawn], telemetry: [seat], "
        "startup: {}}\n---\n\nbody\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo"))
    args = SimpleNamespace(name="join-seat", force=False, timeout=5,
                           debug_file=None, model=None, effort=None,
                           settings=None, prompt_file=None, tmux_session="t",
                           window_path=None, dry_run=True, throwaway=False,
                           successor_argv=None, role="director")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 1, f"join-only rotate-self must be REFUSED, got rc {rc}"
    err = capsys.readouterr().err
    assert "join-only" in err and "first_turn" in err, \
        f"refusal must name the reason:\n{err}"


def test_rotate_self_plain_no_startup_still_spawns(tmp_path, monkeypatch,
                                                   capsys):
    """The legacy plain template (NO startup key at all) is untouched by the
    join-only refusal — a historical rotate-self still proceeds (regression:
    the refusal targets templates that DECLARE a startup, not pre-startup
    shapes)."""
    _seats_sheet(tmp_path, [
        {"name": "plain-seat", "role": "parent", "model": "m",
         "effort": "max", "settings": ""}])
    (tmp_path / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (tmp_path / "nodes" / ".geometry" / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: x.md, steps: [spawn], telemetry: [seat]}\n"
        "---\n\nbody\n", encoding="utf-8")
    seen = {}
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: seen.update(name=kw["name"]) or
                        (0, "echo hi"))
    args = SimpleNamespace(name="plain-seat", force=False, timeout=5,
                           debug_file=None, model=None, effort=None,
                           settings=None, prompt_file=None, tmux_session="t",
                           window_path=None, dry_run=True, throwaway=False,
                           successor_argv=None, role="parent")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0, f"a plain no-startup template must still rotate, rc {rc}"