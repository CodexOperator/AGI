"""Tests for hypothesis:l4-the-pin-is-the-lease, KID 1 of 2 — the TABLES +
the JUDGEMENT (pure functions in heal.py).

KID 1 scope only, per the serial build order:
  * `_pin_table(root, rows)`        — (1a) pins -> {session_id: (seat, pin, gen)}
  * `_seat_sessions(registry_dir, windows)` — (1b) seat sessions from registry
                                        files whose @id resolves via the window
                                        list
  * `_judge_leases(pins, sessions, rows, root, now)` — (1c) one verdict per
                                        session (KEEP/PROTECTED/IN-FLIGHT/
                                        BELAM-UNPINNED/REAP)

KID 2 owns the pass, the arm, the dm, and the live dry-run proof — nothing
here, and nothing here may read `~/.claude/sessions`, kill a real process, or
touch `.agi/config.json`. Everything is FIXTURE tree / fixture registry dir /
fixture window list (the existing `window_path` seam) / fake pid table.
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


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    """A fixture graph root whose seats row + sessions dir are all ours."""
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (g / "sessions").mkdir(parents=True, exist_ok=True)
    return g


@pytest.fixture
def registry(graph: Path) -> Path:
    """A fixture registry dir (stands in for `~/.claude/sessions`)."""
    r = graph / "registry"
    r.mkdir(parents=True, exist_ok=True)
    return r


def _write_seats(graph: Path, rows: list[dict]) -> None:
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _windows(names: list[str]) -> list[(str, str)]:
    """A fixture window list `[(@<N>, <name>), ...]` with deterministic ids
    (`@101 + i`) over a window-path file (the existing `_all_windows` seam).
    The ids are the SAME base every registry test uses, so an @id written for
    a name resolves here."""
    import tempfile
    wp = Path(tempfile.mkdtemp()) / "windows.txt"
    lines = [f"@{101 + i} {nm}" for i, nm in enumerate(names)]
    wp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return heal._all_windows(str(wp))


_OWNER = object()  # sentinel: writes `tmux: None` (owner/stub, clause 4)


def _write_registry(registry: Path, pid: int, sid: str, window_id: str,
                    session: str = "agi-rc", tmux=_OWNER) -> None:
    """Write a `<registry>/<pid>.json` carrying `sessionId` + `tmux:
    <session>:@<id>.%<id>`. `tmux=_OWNER` (the default) derives the @id cell
    from `window_id`; pass `tmux=None` to model the owner's remote-control
    sessions / streamer stub (clause 4: never a seat session). `window_id`
    must be one of the ids `_windows` produced for the same seat name."""
    if tmux is None:
        cell = None
    else:
        cell = f"{session}:@{window_id.lstrip('@')}.%{window_id.lstrip('@')}"
    (registry / f"{pid}.json").write_text(
        json.dumps({"sessionId": sid, "session_id": sid, "tmux": cell}),
        encoding="utf-8")


def _id_for(names: list[str], name: str) -> str:
    """The fixture window id `_windows(names)` assigns to `name`."""
    return f"@{101 + names.index(name)}"


def _mk_transcript(graph: Path, sid: str) -> str:
    """Create a transcript file under the fixture graph and return its path
    (the thing a meter pin names). Stem == session_id."""
    d = graph / "transcripts"
    d.mkdir(parents=True, exist_ok=True)
    tp = d / f"{sid}.jsonl"
    tp.write_text("{}", encoding="utf-8")
    return str(tp)


def _mk_pin(graph: Path, seat: str, transcript: str | None,
            gen: int | None = None, pin_name: str | None = None) -> Path:
    """Write `<graph>/sessions/<seat>.meter` (or a custom pin_name) naming a
    transcript. `transcript=None` writes a stale pin naming a path that does
    not exist (-> transcript missing)."""
    d = graph / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    p = d / (pin_name or f"{seat}.meter")
    if transcript is None:
        p.write_text(f"{gen or 0}\t{graph}/sessions/nonexistent-{seat}"
                     f".jsonl\n", encoding="utf-8")
    else:
        line = (f"{gen}\t{transcript}\n" if gen is not None
                else f"{transcript}\n")
        p.write_text(line, encoding="utf-8")
    return p


def _rotation(graph: Path, seat: str, age_s: int) -> None:
    """A `started` rotation record for `seat`, `age_s` old."""
    d = graph / "sessions" / "rotations"
    d.mkdir(parents=True, exist_ok=True)
    rec = {"rotation": "rotate-self", "seat": seat, "result": "started",
           "recorded_at": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s)),
           "steps_reached": ["spawn"]}
    stamp = time.strftime("%Y%m%dT%H%M%SZ",
                          time.gmtime(time.time() - age_s))
    (d / f"{seat}.{stamp}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def _seats(graph: Path) -> list[dict]:
    import rotate as _rotate  # noqa: PLC0415
    return _rotate._load_seats(graph)


def _judge(*, graph: Path, registry: Path, names: list[str], rows: list[dict],
           now: float | None = None) -> list[dict]:
    """Wire the whole KID-1 pipeline for a set of window names: build the
    window list, read rows, build pins, list seat sessions, judge."""
    windows = _windows(names)
    rows = rows or _seats(graph)
    pins, _skipped = heal._pin_table(graph, rows)
    sess = heal._seat_sessions(str(registry), windows)
    return heal._judge_leases(pins, sess, rows, graph,
                              now=now or time.time())


# --------------------------------------------------------------------------
# (1a) _pin_table
# --------------------------------------------------------------------------

def test_pin_table_maps_session_to_lease(graph):
    """A row's own pin names a transcript whose stem is a session_id ->
    `{session_id: (seat, pin_path, generation)}`."""
    sid_a = "aaaa-1111"
    ta = _mk_transcript(graph, sid_a)
    _mk_pin(graph, "seat-a", ta, gen=3)
    pins, skipped = heal._pin_table(graph, [{"name": "seat-a"}])
    assert skipped == []
    seat, pin_path, gen = pins[sid_a]
    assert seat == "seat-a"
    assert gen == 3
    assert pin_path.endswith("sessions/seat-a.meter")


def test_pin_table_pred_pins_and_missing_pin_is_skip(graph):
    """`predecessor_pins` read from the cell (absent = 0); a pred pin whose
    transcript file is gone is SKIPPED with a reason (clause 3) and never a
    lease; a pred pin whose transcript exists IS a lease."""
    sid_v = "vvvv-2222"
    tv = _mk_transcript(graph, sid_v)
    _mk_pin(graph, "belam", None, gen=1)                       # own pin stale
    _mk_pin(graph, "belam", tv, pin_name="belam.pred-1.meter")  # pred-1 -> VI
    _mk_pin(graph, "belam", None, pin_name="belam.pred-2.meter")  # pred-2 stale
    rows = [{"name": "belam", "predecessor_pins": 2}]
    pins, skipped = heal._pin_table(graph, rows)
    assert sid_v in pins
    seat, pinp, _g = pins[sid_v]
    assert seat == "belam"
    assert pinp.endswith("belam.pred-1.meter")
    reasons = [s["reason"] for s in skipped]
    assert sum("transcript missing" in r for r in reasons) >= 2, reasons


def test_pin_table_absent_row_pin_not_a_lease(graph):
    """A row whose own pin is stale (transcript missing), or whose pin file
    is absent, leases nothing."""
    _mk_pin(graph, "seat-a", None)  # transcript missing
    pins, skipped = heal._pin_table(graph, [{"name": "seat-a"},
                                            {"name": "seat-none"}])
    assert pins == {}
    assert any("transcript missing" in s["reason"] for s in skipped)


# --------------------------------------------------------------------------
# (1b) _seat_sessions
# --------------------------------------------------------------------------

def test_seat_sessions_resolves_id_through_window_list(graph, registry):
    """A registry file whose tmux @id resolves via the window list is a seat
    session; an owner session (`tmux: None`) and an @id resolving to no
    window are NOT (clause 4)."""
    _write_registry(registry, 1001, "sida", "@50", session="view-a")
    _write_registry(registry, 1002, "sidb", "@51", session="view-b")
    _write_registry(registry, 1003, "sid-owner", "@52", tmux=None)  # owner/stub
    _write_registry(registry, 1004, "sid-orphan", "@99")  # @id not in windows
    windows = [("@50", "seat-a"), ("@51", "seat-b"), ("@52", "owner-w")]
    sess = heal._seat_sessions(str(registry), windows)
    sids = sorted(s["session_id"] for s in sess)
    assert sids == ["sida", "sidb"]           # owner + orphan excluded
    by = {s["session_id"]: s for s in sess}
    assert by["sida"]["window_name"] == "seat-a"
    assert by["sida"]["window_id"] == "@50"
    assert by["sida"]["pid"] == 1001


def test_seat_sessions_empty_registry(graph, registry):
    assert heal._seat_sessions(str(registry), []) == []
    assert heal._seat_sessions(str(graph / "nope"), []) == []
    # never a default-dir read: passing nothing touches no ~/.claude file
    assert isinstance(heal._seat_sessions(windows=[]), list)


# --------------------------------------------------------------------------
# (1c) _judge_leases
# --------------------------------------------------------------------------

def test_pinned_seat_session_keep(graph, registry):
    """A pinned seat session -> KEEP (its sessionId is a live lease)."""
    names = ["seat-a"]
    sid_a = "aaaa-keep"
    _mk_transcript(graph, sid_a)
    _mk_pin(graph, "seat-a", str(graph / "transcripts" / f"{sid_a}.jsonl"),
            gen=1)
    _write_registry(registry, 1001, sid_a, _id_for(names, "seat-a"))
    _write_seats(graph, [{"name": "seat-a"}])
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert [(s["session_id"], s["verdict"], s["reason"]) for s in out] == [
        (sid_a, "KEEP", "")]


def test_unpinned_plain_seat_would_reap(graph, registry):
    """An unpinned plain-seat session -> REAP (KID 2's pass turns this into
    would-reap under dry-run / reaped under armed)."""
    names = ["seat-b"]
    sid_b = "bbbb-reap"
    _write_registry(registry, 2001, sid_b, _id_for(names, "seat-b"))
    _write_seats(graph, [{"name": "seat-b"}])
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert out and out[0]["verdict"] == "REAP" and out[0]["seat"] == "seat-b"


def test_protected_row_protected(graph, registry):
    """`protected: true` (absent = not) -> PROTECTED even when unpinned."""
    names = ["seat-c"]
    sid_c = "cccc-prot"
    _write_registry(registry, 3001, sid_c, _id_for(names, "seat-c"))
    _write_seats(graph, [{"name": "seat-c", "protected": True}])
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert out and out[0]["verdict"] == "PROTECTED"


def test_rotation_in_flight_not_reaped(graph, registry):
    """A seat with a `started` rotation 3 min old -> IN-FLIGHT, never REAP
    (the guard is CALLED, not copied)."""
    names = ["seat-d"]
    sid_d = "dddd-flight"
    _write_registry(registry, 4001, sid_d, _id_for(names, "seat-d"))
    _write_seats(graph, [{"name": "seat-d"}])
    _rotation(graph, "seat-d", 180)
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert out and out[0]["verdict"] == "IN-FLIGHT"


def test_old_started_rotation_is_reap(graph, registry):
    """A `started` rotation OLDER than the window is not in flight -> the
    unpinned session is REAP."""
    names = ["seat-d2"]
    sid_d = "dddd-old"
    _write_registry(registry, 4002, sid_d, _id_for(names, "seat-d2"))
    _write_seats(graph, [{"name": "seat-d2"}])
    _rotation(graph, "seat-d2", 3600)
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert out and out[0]["verdict"] == "REAP"


def test_owner_session_absent_from_judgement(graph, registry):
    """An owner remote-control session (`tmux: None`) is absent from the seat
    session table and so never appears in a judgement at all."""
    _write_registry(registry, 5001, "sid-owner", "@90", tmux=None)
    _write_seats(graph, [{"name": "seat-e"}])
    windows = _windows(["seat-e"])
    rows = _seats(graph)
    sess = heal._seat_sessions(str(registry), windows)
    assert sess == []           # owner never listed
    out = heal._judge_leases({}, sess, rows, graph, now=time.time())
    assert out == []


def test_outside_seat_window_not_judged(graph, registry):
    """A session whose window name is NOT a seat/belam name is never listed
    (clause 4 falsifier: 'a session outside the seat/belam window names
    listed at all')."""
    names_seat = ["seat-f", "agi-06"]
    _write_registry(registry, 6001, "sid-agi", _id_for(names_seat, "agi-06"))
    _write_seats(graph, [{"name": "seat-f"}])
    windows = _windows(names_seat)
    rows = _seats(graph)
    sess = heal._seat_sessions(str(registry), windows)
    assert sess                      # candidate resolves (avi window exists)
    out = heal._judge_leases({}, sess, rows, graph, now=time.time())
    assert out == []                 # but never judged (not a seat name)


def test_belam_no_pred_table_unpinned_predecessors_held(graph, registry):
    """With NO predecessor-pin table (row has no `predecessor_pins` cell),
    the pinned prime -> KEEP and every idle belam predecessor -> BELAM-UNPINNED
    (reason 'no predecessor-pin table yet'); NOTHING reaped."""
    names = ["belam-S1-L4-XI", "belam-S1-L4-V", "belam-S1-L4-VI",
             "belam-S1-L4-VIII", "belam-S1-L4-IX"]
    sids = {nm: f"{nm.lower()}-s" for nm in names}
    _mk_transcript(graph, sids[names[0]])
    _mk_pin(graph, "belam", str(graph / "transcripts" / "belam-s1-l4-xi-s.jsonl"),
            gen=11)                                      # belam.meter -> XI
    for i, nm in enumerate(names):
        _write_registry(registry, 100 + i, sids[nm],
                        _id_for(names, nm))
    _write_seats(graph, [{"name": "belam"}])
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    judged = {s["window_name"]: s["verdict"] for s in out}
    assert judged == {
        "belam-S1-L4-XI": "KEEP",
        "belam-S1-L4-V": "BELAM-UNPINNED",
        "belam-S1-L4-VI": "BELAM-UNPINNED",
        "belam-S1-L4-VIII": "BELAM-UNPINNED",
        "belam-S1-L4-IX": "BELAM-UNPINNED",
    }
    assert "REAP" not in judged.values()
    assert all(s["reason"] == "no predecessor-pin table yet"
               for s in out if s["verdict"] == "BELAM-UNPINNED")


def test_belam_pred_pin_keeps_predecessor(graph, registry):
    """With `predecessor_pins: 5` and `belam.pred-1.meter` naming VI, VI is
    KEEP (its session is pinned); a still-incomplete pred table never reaps
    the other idle predecessors (BELAM-UNPINNED, not REAP)."""
    names = ["belam-S1-L4-XI", "belam-S1-L4-V", "belam-S1-L4-VI",
             "belam-S1-L4-VIII", "belam-S1-L4-IX"]
    sid_xi = f"{names[0].lower()}-xi2"
    sid_vi = f"{names[2].lower()}-vi2"
    _mk_transcript(graph, sid_xi)
    _mk_transcript(graph, sid_vi)
    _mk_pin(graph, "belam", str(graph / "transcripts" / f"{sid_xi}.jsonl"),
            gen=11)                                      # prime pinned
    _mk_pin(graph, "belam",
            str(graph / "transcripts" / f"{sid_vi}.jsonl"),
            pin_name="belam.pred-1.meter")               # pred-1 -> VI
    sids = {nm: (sid_xi if nm == names[0] else
                 (sid_vi if nm == names[2] else f"{nm.lower()}-x"))
            for nm in names}
    for i, nm in enumerate(names):
        _write_registry(registry, 200 + i, sids[nm], _id_for(names, nm))
    _write_seats(graph, [{"name": "belam", "predecessor_pins": 5}])
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    judged = {s["window_name"]: s["verdict"] for s in out}
    assert judged["belam-S1-L4-VI"] == "KEEP"     # pred-1 leases VI
    assert judged["belam-S1-L4-XI"] == "KEEP"     # prime still pinned
    assert judged["belam-S1-L4-V"] == "BELAM-UNPINNED"
    assert judged["belam-S1-L4-VIII"] == "BELAM-UNPINNED"
    assert judged["belam-S1-L4-IX"] == "BELAM-UNPINNED"
    assert "REAP" not in judged.values()


def test_skipped_transcript_judged_unpinned(graph, registry):
    """A pin whose transcript is gone -> SKIPPED with a reason; its session
    is judged unpinned (plain-seat -> REAP)."""
    names = ["seat-x"]
    sid_x = "xx-stale"
    _mk_pin(graph, "seat-x", None)              # stale pin (transcript missing)
    _write_registry(registry, 7001, sid_x, _id_for(names, "seat-x"))
    _write_seats(graph, [{"name": "seat-x"}])
    pins, skipped = heal._pin_table(graph, _seats(graph))
    assert pins == {}
    assert any("transcript missing" in s["reason"] for s in skipped)
    out = _judge(graph=graph, registry=registry, names=names, rows=None)
    assert out and out[0]["verdict"] == "REAP"

# --------------------------------------------------------------------------
# KID 2 — the PASS + the ARM (_pin_reap_pass, mode from config).
# Append, never rewrite the KID-1 tests above. FIXTURES ONLY: fixture root,
# fixture registry dir, fixture window file via the `window_path` seam, a fake
# pid table, a fake reaper. Never reads `~/.claude/sessions`, never kills a
# real process, never edits `.agi/config.json` (tests WRITE a fixture config
# dir, never the live one).
# --------------------------------------------------------------------------

import os as _os
import tempfile as _tempfile


def _window_file(names: list[str]) -> str:
    """A fixture window-path file (one `@<N> <name>` line per name). Returns
    the path; `_pin_reap_pass` feeds it to `_all_windows` via `window_path`."""
    wp = Path(_tempfile.mkdtemp()) / "windows.txt"
    wp.write_text("\n".join(f"@{101 + i} {nm}"
                            for i, nm in enumerate(names)) + "\n",
                  encoding="utf-8")
    return str(wp)


def _set_pin_reap_mode(graph: Path, mode: str) -> None:
    """Write the fixture config's `reaper.pin_reap` (never the live config)."""
    cfg = {"metric_primary": "x"}
    if mode:
        cfg["reaper"] = {"pin_reap": mode}
    (graph / "config.json").write_text(json.dumps(cfg), encoding="utf-8")


def _run_pass(*, graph: Path, registry: Path, names: list[str], rows: list,
              mode: str | None = "dry-run", pid_alive=None, reaper=None,
              now: float | None = None):
    """Wire `_pin_reap_pass` over a fixture: rows, pins are built from the
    fixture graph and sessions dir; sessions from the fixture registry and the
    fixture window file. `mode` passed explicitly (None = read config)."""
    wp = _window_file(names)
    if reaper is None:
        reaper = lambda root, j, rt: {"fake": True, "seat": j["seat"]}  # noqa: E731
    return heal._pin_reap_pass(
        graph, registry_dir=str(registry), window_path=wp,
        pid_alive=pid_alive, reaper=reaper, now=now or time.time(), mode=mode)


def test_pass_dry_run_lists_never_arms(graph, registry):
    """Dry-run (config absent / `dry-run`) lists a REAP session as would-reap
    and NEVER arms: the fake reaper must not be called, nothing returned."""
    names = ["seat-r"]
    sid = "rrrr-dry"
    _write_registry(registry, 9001, sid, _id_for(names, "seat-r"))
    _write_seats(graph, [{"name": "seat-r"}])
    called = []
    def reaper(root, j, rt):
        called.append(j)
        raise AssertionError("reaper must not run under dry-run")
    acted = _run_pass(graph=graph, registry=registry, names=names, rows=None,
                      mode="dry-run", reaper=reaper)
    assert acted == []
    assert called == []


def test_pass_armed_reaps_and_dms(graph, registry, monkeypatch):
    """`reaper.pin_reap: armed` arms a REAP session: the reaper runs once and
    ONE dm goes to the row's `rotated_by` holder (send patched, nothing sent).
    Owner `tmux: None` session is still absent (never judged, never reaped)."""
    names = ["seat-arm"]
    sid = "aaaa-arm"
    _write_registry(registry, 9002, sid, _id_for(names, "seat-arm"))
    _write_registry(registry, 9003, "owner-s", "@77", tmux=None)  # owner
    _write_seats(graph, [{"name": "seat-arm", "rotated_by": "boss-1"}])
    _set_pin_reap_mode(graph, "armed")
    seen = []
    def reaper(root, j, rt):
        seen.append(j["session_id"])
        return {"pids": [42], "reaped": True}
    dms = []
    import importlib as _il
    sendmod = _il.import_module("send")   # the canonical module heal imports
    monkeypatch.setattr(sendmod, "send",
                        lambda root, to, text, sender: dms.append((to, text)))
    acted = _run_pass(graph=graph, registry=registry, names=names, rows=None,
                      mode="armed", reaper=reaper, pid_alive=lambda p: True)
    assert seen == [sid]
    assert len(acted) == 1
    assert acted[0]["seat"] == "seat-arm"
    assert acted[0]["session_id"] == sid
    assert acted[0]["reap"]["reaped"] is True
    assert len(dms) == 1 and dms[0][0] == "boss-1"
    assert "pin-reap" in dms[0][1]


def test_pass_armed_never_reaps_protected_or_in_flight(graph, registry):
    """Armed mode reaps ONLY `REAP`: a PROTECTED session and an IN-FLIGHT seat
    are never handed to the reaper (kid-1 verdicts hold BY CONSTRUCTION)."""
    names = ["seat-prot", "seat-flight"]
    _write_registry(registry, 9101, "pp-1", _id_for(names, "seat-prot"))
    _write_registry(registry, 9102, "ff-1", _id_for(names, "seat-flight"))
    _write_seats(graph, [{"name": "seat-prot", "protected": True},
                         {"name": "seat-flight"}])
    _rotation(graph, "seat-flight", 180)
    called = []
    def reaper(root, j, rt):
        called.append(j["seat"])
        return {"reaped": True}
    _run_pass(graph=graph, registry=registry, names=names, rows=None,
              mode="armed", reaper=reaper)
    assert called == []  # neither PROTECTED nor IN-FLIGHT reaches the reaper


def test_pass_armed_skips_dead_pid_idempotent(graph, registry, monkeypatch):
    """A REAP session whose pid is already dead is SKIPPED (idempotent: the
    reaper is not called, nothing re-killed), recorded as an action with the
    'pid already gone' note, and the dm still fires."""
    names = ["seat-dead"]
    sid = "dddd-dead"
    _write_registry(registry, 9201, sid, _id_for(names, "seat-dead"))
    _write_seats(graph, [{"name": "seat-dead", "rotated_by": "boss-2"}])
    _set_pin_reap_mode(graph, "armed")
    called = []
    def reaper(root, j, rt):
        called.append(j)
        raise AssertionError("reaper must not run for an already-dead pid")
    dms = []
    import importlib as _il
    sendmod = _il.import_module("send")   # the canonical module heal imports
    monkeypatch.setattr(sendmod, "send",
                        lambda root, to, text, sender: dms.append(to))
    acted = _run_pass(graph=graph, registry=registry, names=names, rows=None,
                      mode="armed", reaper=reaper, pid_alive=lambda p: False)
    assert called == []
    assert len(acted) == 1
    assert acted[0]["reaped"] is False
    assert "pid already gone" in acted[0]["note"]
    assert dms == ["boss-2"]


def test_pass_mode_override_is_list_only(graph, registry):
    """`mode="dry-run"` forces LIST ONLY even when the config says armed — the
    `pin-reap` subcommand contract (armed only through config, never a flag)."""
    names = ["seat-cli"]
    sid = "cccc-cli"
    _write_registry(registry, 9301, sid, _id_for(names, "seat-cli"))
    _write_seats(graph, [{"name": "seat-cli"}])
    _set_pin_reap_mode(graph, "armed")   # config says armed...
    called = []
    def reaper(root, j, rt):
        called.append(j)
        raise AssertionError("CLI pin-reap must be list-only")
    acted = _run_pass(graph=graph, registry=registry, names=names, rows=None,
                      mode="dry-run", reaper=reaper)   # ...override -> list
    assert acted == [] and called == []


def test_pass_mode_reads_config_default_dry_run(graph, registry):
    """Untouched config (`no reaper.pin_reap cell`) -> dry-run by reading the
    config itself (mode=None), proving the fail-closed default is read, not
    assumed."""
    names = ["seat-cfg"]
    sid = "eeee-cfg"
    _write_registry(registry, 9401, sid, _id_for(names, "seat-cfg"))
    _write_seats(graph, [{"name": "seat-cfg"}])
    (graph / "config.json").write_text(
        json.dumps({"metric_primary": "x"}), encoding="utf-8")
    called = []
    def reaper(root, j, rt):
        called.append(j)
        raise AssertionError("no-mode config must stay list-only")
    acted = _run_pass(graph=graph, registry=registry, names=names, rows=None,
                      mode=None, reaper=reaper)
    assert acted == [] and called == []
