"""Tests for hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
(kid 2 of 2: RESPAWN + ROW + DM + LOCK RELEASE + the once-guard defect).

Detection (kid 1) is already merged; THIS half makes detection heal. A dead
seat (pid gone + window @id gone + no window named + no rotation in flight) is
RESPAWNED through its existing spawn path via the launcher seam (a fake
launcher — never a real model), its config:seats row's generation/window/pid
are rewritten (session_ref stays empty for the successor's ack), one dm each
goes to the `rotated_by` holder and to the Sensei, and ONE crash-recovery
record carries the probable_cause AND the respawn outcome.

THE DEFECT PIN (the reason kid 2 exists): the once-guard is keyed on a RESPAWN
OUTCOME, never on mere detection. kid 1's detection wrote `result: detected`
BEFORE any spawn; if the guard treated that record as done, pass N+1 would
never respawn the still-dead seat. So: a `result: detected`-only record must
NOT suppress the respawn on the next pass; only a `result: respawned` record
suppresses.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
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
    """A fixture graph root whose seats row + sessions dir are all ours
    (basename `.agi`, so write.py's descend-only root resolution accepts it)."""
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (g / "sessions").mkdir(parents=True, exist_ok=True)
    return g


# (SL7.03) leak detector: AGI_REAPER_LOG must never survive a test -- a raw
# `os.environ[...] = ...` write would bleed a reaper-log path into later
# tests' watch-loop logging. All writes go through monkeypatch.setenv.
@pytest.fixture(scope="module", autouse=True)
def _no_reaper_log_leak():
    yield
    assert "AGI_REAPER_LOG" not in os.environ, \
        "AGI_REAPER_LOG leaked out of a test -- use monkeypatch.setenv"


def _write_seats(graph: Path, rows: list[dict]) -> None:
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _rows(graph: Path) -> list[dict]:
    try:
        import rotate as _r
        return _r._load_seats(graph)
    except Exception:  # noqa: BLE001
        return []


def _row(graph: Path, name: str) -> dict:
    for r in _rows(graph):
        if r.get("name") == name:
            return r
    return {}


def _rotations(graph: Path) -> Path:
    r = graph / "sessions" / "rotations"
    r.mkdir(parents=True, exist_ok=True)
    return r


def _crash_records(graph: Path, seat: str) -> list[Path]:
    return (sorted(_rotations(graph).glob(f"{seat}.*.json"))
            if _rotations(graph).exists() else [])


def _write_record(graph: Path, seat: str, rec: dict, stamp: str) -> Path:
    p = _rotations(graph) / f"{seat}.{stamp}.json"
    p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return p



def _scan(graph: Path, *, launcher, dead: bool = True,
          window_names=("", ""), windows_file: str | None = None) -> list[dict]:
    """One seat-dead scan with a poked process table, a fake window list and an
    EXPLICIT launcher seam (a fake launcher that returns 0 == spawn failed, or
    a working fake launcher)."""
    wf = Path(windows_file) if windows_file else graph / "windows.arg"
    wf.write_text("\n".join(window_names) + "\n", encoding="utf-8")
    return heal._watch_seats(graph, pid_alive=(lambda pid: not dead),
                             window_path=str(wf), launcher=launcher)


def _working_launcher(records: list, pid: int = 515151, window: str = "@777"):
    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        records.append({"name": name, "pid": pid, "window": window,
                        "cwd": str(cwd)})
        return pid, window
    return launch


def _failing_launcher(records: list):
    def launch(root, name, shell_cmd, window_path=None):
        records.append({"name": name, "ok": False})
        return 0, ""
    return launch


def _inbox(graph: Path, to: str) -> str:
    p = graph / "sessions" / "inbox" / f"{to}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _crash_record(graph: Path, seat: str) -> dict:
    recs = _crash_records(graph, seat)
    assert len(recs) == 1, f"expected exactly one record for {seat}, got {recs}"
    return json.loads(recs[0].read_text())


# --- THE DEFECT PIN ---------------------------------------------------------

def test_detection_only_record_still_respawns_next_pass(graph):
    """The once-guard must key on the RESPAWN OUTCOME: pass 1's spawn fails and
    writes `result: detected` (kid 1's legacy shape); pass 2 must STILL respawn
    the still-dead seat — a detected-only record never suppresses the retry."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director", "generation": 1}])
    fail_recs: list = []
    pass1 = _scan(graph, launcher=_failing_launcher(fail_recs),
                  window_names=("", "@1 other"))
    assert len(pass1) == 1 and pass1[0]["respawned"] is False
    assert len(fail_recs) == 1, "spawn attempted once even though it failed"
    rec = _crash_record(graph, "seat-a")
    assert rec["result"] == "detected", "a failed spawn records detected-only"

    # the seat is STILL dead -> pass 2 MUST try again.
    ok_recs: list = []
    pass2 = _scan(graph, launcher=_working_launcher(ok_recs),
                  window_names=("", "@1 other"))
    assert len(pass2) == 1, "a detected-only record must not stop the retry"
    assert pass2[0]["respawned"] is True
    assert len(ok_recs) == 1, "pass 2 respawned the still-dead seat"
    # A `respawned` write is ALWAYS a fresh `<seat>.<stamp>.json` (heal.py
    # _write_crash_recovery: only a `detected` re-write dedupes in place), so
    # after detected -> respawned the seat legitimately carries TWO records
    # whenever the two passes straddle a whole-second stamp boundary — and
    # ONE only when they land in the same second and the fresh file happens
    # to overwrite pass 1's. The claim is about the NEWEST record, never the
    # count (an exactly-one assertion here flaked 1/996 under suite load).
    newest = json.loads(_crash_records(graph, "seat-a")[-1].read_text())
    assert newest["result"] == "respawned", \
        "pass 2 recorded the respawn outcome as the newest record"


# --- RACE-2 COMMITTED STAMPS (hypothesis:l4-the-cross-second-boundary-) -----
# The writer seam: `_rotate._write_rotation_record` (rotate.py:_write_rotation_record)
# names a fresh file from `datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')` where
# `datetime` is rotate's own import. Patching `rotate.datetime.utcnow` is the
# narrowest seam the writer offers -- heal keeps its OWN `import datetime` for
# `recorded_at`, so the patch never touches the detection timestamp. No test
# sleeps: the two-file / one-file shapes are owned by the clock, not by wall
# time.


def _advancing_clock(first_second: int = 1):
    """A fake `rotate.datetime` whose `utcnow()` advances one second per call,
    so two writes land on two distinct `<seat>.<stamp>.json` files."""
    state = {"n": first_second - 1}

    class _Stamp:
        def __init__(self, n):
            self.n = n

        def strftime(self, _fmt):
            return f"20260912T00000{self.n:02d}Z"

    class _FakeDT:
        @staticmethod
        def utcnow():
            state["n"] += 1
            return _Stamp(state["n"])
    return _FakeDT


def _frozen_clock(stamp: str = "20260912T000001Z"):
    """A fake `rotate.datetime` locked to ONE stamp, so two writes land on the
    SAME filename and the second overwrites the first."""
    class _Stamp:
        def strftime(self, _fmt):
            return stamp

    class _FakeDT:
        @staticmethod
        def utcnow():
            return _Stamp()
    return _FakeDT


def test_two_distinct_stamp_records_detected_then_respawned(graph, monkeypatch):
    """RACE-2 (SL7.53): force pass 1 and pass 2 to straddle a whole-second
    boundary through the record writer's clock -- NEVER a real sleep. Pass 1
    detects (writes `result: detected`), pass 2 respawns (writes a fresh
    file); two distinct forced stamps give TWO files. The older reads
    `detected`, the newest reads `respawned`. A regression to 'assert exactly
    one record' would FAIL here precisely because the two stamps are forced --
    this is the committed test that owns the two-file shape a same-second
    coalescing test never exercises."""
    import rotate
    monkeypatch.setattr(rotate, "datetime", _advancing_clock())
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director", "generation": 1}])
    fail_recs: list = []
    pass1 = _scan(graph, launcher=_failing_launcher(fail_recs),
                  window_names=("", "@1 other"))
    assert len(pass1) == 1 and pass1[0]["respawned"] is False
    ok_recs: list = []
    pass2 = _scan(graph, launcher=_working_launcher(ok_recs),
                  window_names=("", "@1 other"))
    assert len(pass2) == 1 and pass2[0]["respawned"] is True
    recs = _crash_records(graph, "seat-a")
    assert len(recs) == 2, \
        "two forced distinct second-stamps -> TWO files; hiding pass 1's " \
        "detected record behind an exactly-one assertion is the regression " \
        "this test exists to catch"
    assert recs[0].name != recs[-1].name, "two files carry two stamps"
    older = json.loads(recs[0].read_text())
    newest = json.loads(recs[-1].read_text())
    assert older["result"] == "detected", "the older record still reads detected"
    assert newest["result"] == "respawned", "the newest record carries respawned"


def test_equal_stamp_records_newest_still_respawned(graph, monkeypatch):
    """RACE-2, frozen-clock side (SL7.53): when both passes land in the SAME
    second, pass 2's fresh respawned write OVERWRITES pass 1's detected file
    (same stamp -> same filename), so ONE record remains and it reads
    `respawned`. The claim is the NEWEST record, never the count -- an
    exactly-one assertion is only valid here BECAUSE the clock is frozen, and
    this test proves the respawned outcome is still the newest (the only)
    record."""
    import rotate
    monkeypatch.setattr(rotate, "datetime", _frozen_clock())
    _write_seats(graph, [{"name": "seat-b", "pid": 424242, "window": "@50",
                          "role": "director", "generation": 1}])
    fail_recs: list = []
    _scan(graph, launcher=_failing_launcher(fail_recs),
          window_names=("", "@1 other"))
    ok_recs: list = []
    pass2 = _scan(graph, launcher=_working_launcher(ok_recs),
                  window_names=("", "@1 other"))
    assert pass2 and pass2[0]["respawned"] is True
    recs = _crash_records(graph, "seat-b")
    assert len(recs) == 1, \
        "same stamp -> same filename -> one coalesced record under a frozen " \
        "clock"
    newest = json.loads(recs[0].read_text())
    assert newest["result"] == "respawned", \
        "the equal-stamp coalesced record still reads respawned (the newest)"


def test_respawned_record_suppresses_next_pass(graph):
    """Once the respawn landed, its `result: respawned` record IS the guard:
    a second pass does nothing — two passes never spawn twice."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director"}])
    recs: list = []
    pass1 = _scan(graph, launcher=_working_launcher(recs),
                  window_names=("", "@1 other"))
    assert pass1[0]["respawned"] is True
    assert len(recs) == 1
    assert _crash_record(graph, "seat-a")["result"] == "respawned"

    pass2 = _scan(graph, launcher=_working_launcher(recs),
                  window_names=("", "@1 other"))
    assert pass2 == [], "a second pass over an already-respawned seat is idle"
    assert len(recs) == 1, "no second spawn"
    assert len(_crash_records(graph, "seat-a")) == 1, "no second record"


# --- RECOVER: spawn + row + dm + record -------------------------------------

def test_dead_seat_respawns_and_writes_row_and_dms(graph, monkeypatch):
    """A dead plain director seat -> EXACTLY one spawn, one row rewrite
    (generation/pid/window; session_ref stays empty), one dm to the
    `rotated_by` holder AND one to the Sensei, and one crash-recovery record
    carrying both the probable_cause and the respawn outcome."""
    logp = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logp))
    _write_seats(graph, [{"name": "dir-1", "pid": 424242, "window": "@50",
                          "role": "director", "model": "claude-sonnet-5",
                          "generation": 2, "rotated_by": "sanctuary-prime"}])
    (graph / "sessions" / "dir-1.log").write_text("uds shutdown\n", encoding="utf-8")
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs, pid=515151,
                                                    window="@777"),
                  window_names=("", "@1 other"))

    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert len(launch_recs) == 1 and launch_recs[0]["name"] == "dir-1"
    # row rewrite via the seat's own rule: plain seat -> same name, gen 2->3.
    row = _row(graph, "dir-1")
    assert row["generation"] == 3
    assert row["pid"] == 515151
    assert row["window"] == "@777"
    assert row.get("session_ref", "") == "", "session_ref stays empty (ack)"
    assert len([r for r in _rows(graph) if r["name"] == "dir-1"]) == 1, \
        "the seat's own row, not a new seat"
    # one dm each to the holder and to the Sensei.
    holder = _inbox(graph, "sanctuary-prime")
    sensei = _inbox(graph, "master-sensei")
    assert "[crash-recovery]" in holder
    assert "dir-1" in holder and "respawned" in holder
    assert "[crash-recovery]" in sensei
    # one record with cause + outcome.
    rec = _crash_record(graph, "dir-1")
    assert rec["result"] == "respawned"
    assert rec["probable_cause"] == "idle-external-teardown"
    assert rec["respawn_outcome"]["name"] == "dir-1"
    assert rec["respawn_outcome"]["pid"] == 515151
    assert rec["respawn_outcome"]["generation"] == 3
    assert "DEAD seat dir-1" in logp.read_text()


def test_recovered_director_resumes_on_its_own_quorum_card(graph):
    """A recovered director/helper is spawned on ITS OWN quorum card
    (`<sessions>/quorum/<seat>.md`, the file rotate-self hands a successor),
    never the assembled generic brief. Found by the L4.283 harvest's live
    proof: with `prompt_file=None` spawn_window assembled the generic director
    brief and the recovered seat would have woken with none of its §0-§3."""
    _write_seats(graph, [{"name": "dir-1", "pid": 424242, "window": "@50",
                          "role": "director", "model": "claude-sonnet-5",
                          "generation": 2, "rotated_by": "sanctuary-prime"}])
    (graph / "sessions" / "dir-1.log").write_text("uds shutdown\n", encoding="utf-8")
    card = graph / "sessions" / "quorum" / "dir-1.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# SESSION HANDOFF dir-1\nSENTINEL-CARD-LINE-7f3a\n",
                    encoding="utf-8")
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None):
        seen.append(shell_cmd)
        return 515151, "@777"

    acted = _scan(graph, launcher=launch, window_names=("", "@1 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert len(seen) == 1
    assert "SENTINEL-CARD-LINE-7f3a" in seen[0], \
        "the recovered director was not spawned on its quorum card"


def _backdate_records(graph: Path, seat: str, seconds: int) -> None:
    """Rewrite every crash-recovery record's `recorded_at` `seconds` into the
    past (the fixture's clock is real time; the guard reads the record)."""
    import datetime as _dt
    for rec_path in _crash_records(graph, seat):
        rec = json.loads(rec_path.read_text())
        # only a FRESH record (this pass's) is backdated; an already-backdated
        # one keeps its stamp, so successive recoveries keep distinct files.
        stamp = heal._parse_record_ts(rec.get("recorded_at", "")) or 0
        # time.time(), never utcnow().timestamp(): a naive utcnow reads as
        # LOCAL on this EST box (the very bug _parse_record_ts guards).
        if (time.time() - stamp) > 120:
            continue
        ts = _dt.datetime.utcnow() - _dt.timedelta(seconds=seconds)
        rec["recorded_at"] = ts.isoformat() + "Z"
        # a real recovery is minutes apart, so its record file carries a
        # distinct stamp; the fixture recovers within one second, so rename
        # the file to its backdated stamp or successive records collide.
        newp = rec_path.with_name(
            f"{seat}.{ts.strftime('%Y%m%dT%H%M%SZ')}.json")
        rec_path.unlink()
        newp.write_text(json.dumps(rec))


def test_respawned_record_is_a_bounded_guard_not_forever(graph):
    """A `respawned` record suppresses a second spawn only inside the 10-minute
    window; a recovered successor that dies AGAIN later is a NEW death and is
    respawned. Found by the L4.283 harvest's live proof (sanctuary-director
    182119Z 19:29Z): on the round's bytes the guard scanned every record ever
    written, so the first recovery of a seat was also its last."""
    _write_seats(graph, [{"name": "seat-b", "pid": 424242, "window": "@50",
                          "role": "director", "generation": 1}])
    recs1: list = []
    pass1 = _scan(graph, launcher=_working_launcher(recs1, window="@60"),
                  window_names=("", "@1 other"))
    assert len(pass1) == 1 and pass1[0]["respawned"] is True
    # inside the window, the successor (@60) gone again -> still suppressed
    recs2: list = []
    pass2 = _scan(graph, launcher=_working_launcher(recs2, window="@61"),
                  window_names=("", "@1 other"))
    assert pass2 == [] and recs2 == [], "inside 10 min the guard holds"
    # 11 minutes later, the successor is dead -> a new death, respawned
    _backdate_records(graph, "seat-b", 11 * 60)
    recs3: list = []
    pass3 = _scan(graph, launcher=_working_launcher(recs3, window="@62"),
                  window_names=("", "@1 other"))
    assert len(pass3) == 1 and pass3[0]["respawned"] is True, \
        "an old respawned record must not suppress a later death"
    assert len(recs3) == 1
    assert _row(graph, "seat-b")["generation"] == 3


def test_crash_loop_is_named_not_respawned(graph, monkeypatch):
    """Three `respawned` recoveries within the hour -> the fourth death is
    NAMED in the watch log and NOT respawned (a seat that dies every few
    minutes is a finding for a human, not a spawn budget)."""
    logp = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logp))
    _write_seats(graph, [{"name": "seat-c", "pid": 424242, "window": "@50",
                          "role": "director", "generation": 1}])
    for i in range(3):
        recs: list = []
        got = _scan(graph, launcher=_working_launcher(recs, window=f"@7{i}"),
                    window_names=("", "@1 other"))
        assert len(got) == 1 and got[0]["respawned"] is True, i
        _backdate_records(graph, "seat-c", 11 * 60 * (i + 1))
    recs4: list = []
    pass4 = _scan(graph, launcher=_working_launcher(recs4, window="@80"),
                  window_names=("", "@1 other"))
    assert pass4 == [] and recs4 == [], "the fourth death is not respawned"
    assert "CRASH LOOP" in logp.read_text()


def test_chain_seat_successor_is_next_numeral(graph):
    """A prime_director (belam) chain seat is respawned through the Nth-
    numeral naming rule, never the plain seat name. The NUMERAL is driven by
    the registry row's `generation` (max with the latest record's `gen_after`,
    +1) -- NEVER inferred from open window names (prime XI 19:38Z: a name is
    not an address). Row generation 2 with no window and no record left -> the
    successor is `belam-III` at generation 3 (the dead prime took its own
    `belam-II` window with it, so the row is the only oracle).

    ``_derive_successor_name``'s OLD window inference, seeing NO open belam
    window, guessed `belam-II`/gen 2 regardless of the row and would have
    respawned the successor at gen 2 -- the same generation the row says the
    seat already died at. That collision is the bug this fixes."""
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 2}])
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs, window="@777"),
                  window_names=("", "@99 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert launch_recs[0]["name"] == "belam-III", \
        "the successor numeral is max(row generation)+1, never window-inferred"
    rec = _crash_record(graph, "belam")
    assert rec["result"] == "respawned"
    assert rec["respawn_outcome"]["name"] == "belam-III"
    assert rec["respawn_outcome"]["generation"] == 3, \
        "the chain seat's generation IS its numeral line value"
    row = _row(graph, "belam")
    assert row["window"] == "@777"


def test_chain_successor_base_and_numeral_from_latest_record(graph):
    """A chain seat's successor BASE and NUMERAL both come from the latest
    rotation/crash-recovery record, not from open windows: a crash-recovery
    record that already respawned the seat at `belam-S1-L4-V` (gen_after 5)
    flexes the NEXT successor to `belam-S1-L4-VI` at generation 6 -- the base
    (`belam-S1-L4`) is carried by the record's successor name so a reaped
    window name can never corrupt the chain label."""
    _write_record(graph, "belam", {
        "rotation": "crash-recovery", "result": "respawned",
        "succ_name": "belam-S1-L4-V", "gen_after": 5,
        "recorded_at": "2026-09-11T00:00:00.000000Z"},
        stamp="20260911T000000Z")
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 5}])
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs, window="@778"),
                  window_names=("", "@99 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert launch_recs[0]["name"] == "belam-S1-L4-VI"
    rec = json.loads(_crash_records(graph, "belam")[-1].read_text())
    assert rec["respawn_outcome"]["generation"] == 6


def test_chain_successor_base_from_rotate_self_record_handover(graph):
    """The chain base can also come from a rotate-self `success` record's
    `handover.successor_window.name` (no crash-recovery record yet): the
    generator of the base is the same `_latest_rotate_record` both read.
    With the row still at gen 1 (a fresh prime that later crashed), the
    successor is the next numeral on the recorded line base."""
    _write_record(graph, "belam", {
        "rotation": "rotate-self", "result": "success", "gen_after": 1,
        "handover": {"successor_window": {"name": "belam-S1-L4-I",
                                            "id": "@300"}},
        "recorded_at": "2026-09-11T00:00:00.000000Z"},
        stamp="20260911T000100Z")
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 1}])
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs, window="@779"),
                  window_names=("", "@99 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert launch_recs[0]["name"] == "belam-S1-L4-II"


def test_chain_successor_collision_still_refuses_an_open_window(graph):
    """Open window names are consulted ONLY for the collision refusal: if the
    (row/record-derived) successor window already exists, the recovery is
    refused and the seat stays dead rather than double-spawning."""
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 2}])
    acted = _scan(graph, launcher=_working_launcher([], window="@777"),
                  window_names=("belam-III", "@99 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is False
    assert "already exists" in acted[0]["outcome"]["reason"]


def test_chain_corpse_behind_predecessor_window_is_respawned(graph):
    """(1c) DELETED (prime XI ruling 2026-09-11 19:38Z): an idle predecessor
    window (`belam-S1-L4-II`, the owner's capped chain) is NOT a live
    successor — the dead prime (@50 gone) IS respawned, into the NEXT numeral,
    with the predecessor window still open. Before the ruling this read
    `nothing` and prime crash-recovery was structurally dead."""
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 2}])
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs),
                  window_names=("", "@2 belam-S1-L4-II"))
    assert len(acted) == 1 and acted[0]["respawned"] is True, \
        "a corpse behind an open predecessor window is DEAD"
    assert len(launch_recs) == 1
    assert launch_recs[0]["name"].endswith("-III"), launch_recs[0]["name"]


def test_spawn_failure_leaves_no_row_and_no_dm(graph):
    """A spawn that does not land (launcher returns 0) writes a `detected`
    record and NO row rewrite and NO dm — the seat stays dead and the next
    pass retries (the defect pin)."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director", "rotated_by": "p"}])
    acted = _scan(graph, launcher=_failing_launcher([]),
                  window_names=("", "@1 other"))
    assert acted[0]["respawned"] is False
    rec = _crash_record(graph, "seat-a")
    assert rec["result"] == "detected"
    assert rec["respawn_outcome"]["reason"] != "", "the record names why"
    assert _row(graph, "seat-a").get("pid") == 424242, "row left untouched"
    assert _inbox(graph, "p") == "" and _inbox(graph, "master-sensei") == "", \
        "no dm for a spawn that never landed"


# --- GRACEFUL: lock + rounds + inbox ----------------------------------------

def test_stale_verify_suite_lock_removed(graph, monkeypatch):
    """A stale verify-suite.lock under the dead seat's tree is removed with a
    log line as part of the recovery."""
    logp = graph / "this.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logp))
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director"}]
                       )
    lock = graph / "sessions" / "verify-suite.lock"
    lock.write_text("stale", encoding="utf-8")
    _scan(graph, launcher=_working_launcher([]), window_names=("", "@1 other"))
    assert not lock.exists(), "stale lock removed"
    assert "verify-suite.lock" in logp.read_text(), \
        "the lock removal is logged"


def test_alive_seat_untouched_no_row_no_dm(graph):
    """A live pid is never touched: no spawn, no record, no dm, no row
    change."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director", "rotated_by": "p",
                          "generation": 5}])
    acted = _scan(graph, launcher=_working_launcher([]), dead=False,
                  window_names=("", "@777"))
    assert acted == []
    assert _crash_records(graph, "seat-a") == []
    assert _inbox(graph, "p") == "" and _inbox(graph, "master-sensei") == ""
    assert _row(graph, "seat-a").get("generation") == 5, "row untouched"

# --- L4.292 kid 1: the crash-recovery record drives the service's after_join
#     (1a widening + gen_after/profile keys + dm note)


def test_crash_recovery_record_carries_after_join_profile(graph):
    """The respawned crash-recovery record carries the rotate-self profile
    keys the after_join template's service reads: `gen_after` (the one
    `_latest_rotate_record`/`run_after_join_for_seat` bind the generation
    against), plus the named placeholders `succ_name`, `gen`, `pin_ref`
    (empty: the pin is service-owed), `tmux_session`, `window_id`,
    `pred_pids` = the dead pid, and `recorded_at`."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director"}])
    acted = _scan(graph, launcher=_working_launcher([], pid=515151,
                                                     window="@777"),
                  window_names=("", "@1 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    rec = _crash_record(graph, "seat-a")
    assert rec["gen_after"] == rec["gen"], "gen_after present = the successor gen"
    assert rec["gen_after"] is not None
    assert rec["succ_name"] == "seat-a"
    assert rec["pred_pids"] == [424242], "dead pid is the predecessor pid list"
    assert rec["pin_ref"] == "", "the recovery itself pins nothing (service-owed)"
    assert rec["tmux_session"], "a real tmux session name"
    assert rec["window_id"]
    assert rec["recorded_at"]


def test_latest_rotate_record_picks_up_crash_recovery_respawned(graph):
    """The one-line widening: a `crash-recovery` `result: respawned` record is
    discoverable by `_latest_rotate_record`, so the service performs the
    recovered seat's after_join (join -> pin -> pending ack) exactly as for a
    rotated one. A crash-recovery `result: detected` record is NOT (a spawn
    did not land -> nothing to bind)."""
    import rotate as _rotate
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    # respawned -> found
    p = _rotations(graph) / f"seat-a.{stamp}.json"
    p.write_text(json.dumps({"rotation": "crash-recovery", "seat": "seat-a",
                             "result": "respawned", "gen_after": 4}), encoding="utf-8")
    pair = _rotate._latest_rotate_record(graph, "seat-a")
    assert pair is not None and pair[0]["result"] == "respawned", \
        "the widening accepts crash-recovery respawned"
    # detected -> not found (no spawn landed, nothing to bind)
    p.write_text(json.dumps({"rotation": "crash-recovery", "seat": "seat-a",
                             "result": "detected"}), encoding="utf-8")
    assert _rotate._latest_rotate_record(graph, "seat-a") is None, \
        "a detected-only crash-recovery record binds nothing"


def test_after_join_service_performs_recovered_seats_join_pin_ack(graph):
    """End to end on the fixture root: a respawned crash-recovery record drives
    `run_after_join_for_seat` to perform the seat's `after_join` list with the
    record's `gen_after` as the generation and the record as the #record_path
    (so join -> pin -> pending ack run and land in the record), exactly as a
    rotate-self record would."""
    import rotate as _rotate
    d = _rotations(graph)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    rec_path = d / f"seat-a.{stamp}.json"
    rec_path.write_text(json.dumps({
        "rotation": "crash-recovery", "seat": "seat-a", "result": "respawned",
        "gen_after": 8,
        "recorded_at": "2020-01-01T00:00:00Z",
    }), encoding="utf-8")
    orig_find = _rotate._find_seat
    orig_tmpl = _rotate._resolve_template
    orig_ftv = _rotate._first_turn_values
    orig_run = _rotate.run_after_join
    got = {}
    try:
        _rotate._find_seat = lambda root, name: {"role": "director"}
        _rotate._resolve_template = lambda root, role, explicit=None, **kw: (
            {"startup": {"after_join": [
                {"label": "join", "cmd": "echo join"},
                {"label": "pin", "cmd": "echo pin"},
                {"label": "ack", "cmd": "echo ack"}]}}, "director", "test")
        _rotate._first_turn_values = lambda *a, **k: {
            "seat": "seat-a", "succ_ref": "", "succ_name": "seat-a",
            "succ_transcript": "", "pin_ref": "", "gen": "8",
            "prime_ref": "", "worktree": "", "repo": str(graph),
            "tmux_session": "agi-rc", "pred_pids": "424242"}
        def fake_run(*a, **kw):
            got["startup"] = kw.get("startup")
            got["gen"] = kw.get("gen")
            got["record_path"] = kw.get("record_path")
            got["seat"] = kw.get("seat")
            return {"appended": True}
        _rotate.run_after_join = fake_run
        out = _rotate.run_after_join_for_seat(graph, "seat-a")
        assert out is not None
        assert got.get("gen") == 8, "the recovered seat's generation = gen_after"
        assert str(got["record_path"]) == str(rec_path), \
            "the after_join writes back into the crash-recovery record"
        labels = [e.get("label") for e in
                  (got["startup"].get("after_join") or [])]
        assert labels == ["join", "pin", "ack"]
    finally:
        _rotate._find_seat = orig_find
        _rotate._resolve_template = orig_tmpl
        _rotate._first_turn_values = orig_ftv
        _rotate.run_after_join = orig_run


def test_recovered_top_level_window_id_fills_after_join_identity(graph):
    """mur-SL2.13 part (6), falsifier closed: a crash-recovery respawned
    record carries `window_id` (and the successor pid) at the TOP level, NOT
    under `handover.join` — so `_record_join(rec)` must accept that shape and
    `run_after_join_for_seat` must read the SAME accessor, giving a RECOVERED
    post the identity fill (pid/session_id) exactly as a rotate-self record
    would. A recovered post whose after_join dm lacks the identity fill is the
    falsifier; this proves it is filled from a handover.join-less record."""
    import rotate as _rotate
    d = _rotations(graph)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    rec_path = d / f"seat-a.{stamp}.json"
    # NO `handover.join` — the crash-recovery shape: top-level window_id.
    rec_path.write_text(json.dumps({
        "rotation": "crash-recovery", "seat": "seat-a",
        "result": "respawned", "gen_after": 9,
        "recorded_at": "2020-01-01T00:00:00Z",
        "window_id": "@77",
        "respawn_outcome": {"name": "seat-a", "window": "@77",
                             "pid": 999},
    }), encoding="utf-8")
    orig_find = _rotate._find_seat
    orig_tmpl = _rotate._resolve_template
    orig_join = _rotate._join_successor
    orig_ftv = _rotate._first_turn_values
    orig_run = _rotate.run_after_join
    got = {}
    try:
        _rotate._find_seat = lambda root, name: {"role": "director"}
        _rotate._resolve_template = lambda root, role, explicit=None, **kw: (
            {"startup": {"after_join": [
                {"label": "join", "cmd": "echo join"}]}},
            "director", "test")
        # top-level window_id drives a registry rejoin -> pid/session_id.
        _rotate._join_successor = lambda **k: {
            "found": True, "window_id": "@77", "pid": 999,
            "session_id": "sess-X", "transcript": "joined",
            "name": "seat-a", "note": ""}
        def fake_run(*a, **kw):
            got["values"] = kw.get("values")
            return {"appended": True}
        _rotate.run_after_join = fake_run
        out = _rotate.run_after_join_for_seat(graph, "seat-a")
        assert out is not None
        v = got.get("values") or {}
        assert v.get("pid") == 999, \
            "recovered post pid identity filled (falsifier closed)"
        assert v.get("session_id") == "sess-X", \
            "recovered post session identity filled (falsifier closed)"
    finally:
        _rotate._find_seat = orig_find
        _rotate._resolve_template = orig_tmpl
        _rotate._join_successor = orig_join
        _rotate._first_turn_values = orig_ftv
        _rotate.run_after_join = orig_run


# --- L4.292 kid 2 (3)+(4): the seat tree + ONE writer, verified on a real
#     linked git worktree ------------------------------------------------


def _git(path: Path, *args: str) -> str:
    res = subprocess.run(["git", *args], cwd=path, capture_output=True,
                         text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args}: {res.stderr}")
    return res.stdout.strip()


def _git_init(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", "master")
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "test")
    (path / ".keep").write_text("x")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "init")


def _git_repo_with_worktree(tmp_path: Path) -> tuple[Path, Path]:
    """A real linked git worktree: `main` is the common root, `wt` sits at
    `<main>/.agi/worktrees/seat-wt` — the exact shape a seat worktree takes
    (the launch cwd must resolve there through git_common_root, never the
    graph dir)."""
    main = tmp_path / "main"
    _git_init(main)
    wt_dir = main / ".agi" / "worktrees" / "seat-wt"
    _git(main, "worktree", "add", "-q", str(wt_dir), "-b", "season/s2")
    return main, wt_dir


def test_seat_tree_dir_worktree_resolves_to_linked_worktree(tmp_path):
    """`_seat_tree_dir` for a worktree seat = MAIN's repo root joined with the
    row's `worktree` cell (`.`-prefixed `.agi/worktrees/seat-wt`), resolved
    through `git_common_root` — the linked worktree's repo root, NEVER the
    graph dir. Empty cell -> MAIN's repo root itself."""
    main, wt_dir = _git_repo_with_worktree(tmp_path)
    graph = main / ".agi"
    (graph / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    seat_tree = heal._seat_tree_dir(graph, {"worktree": ".agi/worktrees/seat-wt"})
    assert seat_tree == wt_dir, (f"got {seat_tree}, want the linked worktree "
                                 f"{wt_dir}")
    main_tree = heal._seat_tree_dir(graph, {"worktree": ""})
    assert main_tree == main, "empty worktree cell -> MAIN's repo root"


def test_launch_recovered_cds_into_seat_tree(tmp_path, monkeypatch):
    """The real `_launch_recovered` builds its tmux new-window line with
    `cd <seat tree> && <shell_cmd>` — the seat tree (never the graph dir)."""
    main, wt_dir = _git_repo_with_worktree(tmp_path)
    graph = main / ".agi"
    captured: list = []

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))
        return type("R", (), {"returncode": 0, "stdout": "@123\n",
                              "stderr": ""})()

    monkeypatch.setattr(heal.subprocess, "run", fake_run)
    pid, wid = heal._launch_recovered(
        graph, "seat-wt", "echo successor", cwd=wt_dir)
    assert wid == "@123"
    assert len(captured) == 1, "one tmux new-window launch"
    tmux_rgx = captured[0]
    assert tmux_rgx[-1].startswith(f"cd {wt_dir} && "), tmux_rgx[-1]
    assert "cd " + str(graph) + " " not in tmux_rgx[-1], \
        "the launch never cds into the graph dir"


def test_worktree_seat_recovery_launches_in_and_writes_main_only(graph, tmp_path,
                                                                 monkeypatch):
    """A fixture MAIN + linked worktree end-to-end: a dead worktree seat is
    respawned with the fake launcher receiving cwd = the seat's OWN worktree
    repo root, and the row's identity cells land in MAIN's seats.md — the SAME
    file `_live_seat_row` reads them from — while the worktree's copy is never
    written (it still carries the pre-recovery identity)."""
    main, wt_dir = _git_repo_with_worktree(tmp_path)
    gdir = main / ".agi"
    (gdir / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    # MAIN's seats.md: the (dead, superceded) identity.
    _write_seats(gdir, [{"name": "wt", "pid": 424242, "window": "@50",
                         "generation": 2,
                         "worktree": ".agi/worktrees/seat-wt"}])
    # the worktree's OWN copy: a DIFFERENT (dead) pid so detection reads the
    # worktree row live-first, and a STALE generation that must NOT be the one
    # the successor row writes into MAIN.
    (wt_dir / ".agi" / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (wt_dir / ".agi" / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\nseats:\n"
        "  - " + json.dumps({"name": "wt", "pid": 987654, "window": "@50",
                             "generation": 2,
                             "worktree": ".agi/worktrees/seat-wt"}) + "\n"
        "---\n")
    wf = gdir / "windows.txt"
    wf.write_text("", encoding="utf-8")
    launch_recs: list = []
    acted = heal._watch_seats(
        gdir, pid_alive=(lambda pid: False), window_path=str(wf),
        launcher=_working_launcher(launch_recs, window="@777"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert launch_recs[0]["cwd"] == str(wt_dir), \
        "the recovered successor launches inside its own seat worktree"
    main_row = _row(gdir, "wt")
    assert main_row["generation"] == 3, "MAIN row generation advanced to 3"
    assert main_row["window"] == "@777"
    wt_copy = _row(wt_dir / ".agi", "wt")
    assert wt_copy["pid"] == 987654 and wt_copy.get("window") == "@50", \
        "the worktree seats.md copy was never written (still pre-recovery)"
