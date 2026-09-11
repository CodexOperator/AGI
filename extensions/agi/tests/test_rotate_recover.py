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
    def launch(root, name, shell_cmd, window_path=None):
        records.append({"name": name, "pid": pid, "window": window})
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
    assert _crash_record(graph, "seat-a")["result"] == "respawned", \
        "pass 2 overwrote detection with the respawn outcome"


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

def test_dead_seat_respawns_and_writes_row_and_dms(graph):
    """A dead plain director seat -> EXACTLY one spawn, one row rewrite
    (generation/pid/window; session_ref stays empty), one dm to the
    `rotated_by` holder AND one to the Sensei, and one crash-recovery record
    carrying both the probable_cause and the respawn outcome."""
    logp = graph / "reaper.log"
    os.environ["AGI_REAPER_LOG"] = str(logp)
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


def test_crash_loop_is_named_not_respawned(graph):
    """Three `respawned` recoveries within the hour -> the fourth death is
    NAMED in the watch log and NOT respawned (a seat that dies every few
    minutes is a finding for a human, not a spawn budget)."""
    logp = graph / "reaper.log"
    os.environ["AGI_REAPER_LOG"] = str(logp)
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
    numeral naming rule, never the plain seat name: with no live belam window
    left (the dead prime took it with it), the successor is `belam-II` and its
    generation IS the numeral."""
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@50",
                          "role": "prime_director", "generation": 2}])
    launch_recs: list = []
    acted = _scan(graph, launcher=_working_launcher(launch_recs, window="@777"),
                  window_names=("", "@99 other"))
    assert len(acted) == 1 and acted[0]["respawned"] is True
    assert launch_recs[0]["name"] == "belam-II", \
        "a chain seat is respawned under the numeral chain, not its plain name"
    rec = _crash_record(graph, "belam")
    assert rec["result"] == "respawned"
    assert rec["respawn_outcome"]["name"] == "belam-II"
    assert rec["respawn_outcome"]["generation"] == 2, \
        "the chain seat's generation IS its numeral line value"
    row = _row(graph, "belam")
    assert row["window"] == "@777"


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

def test_stale_verify_suite_lock_removed(graph):
    """A stale verify-suite.lock under the dead seat's tree is removed with a
    log line as part of the recovery."""
    logp = graph / "this.log"
    os.environ["AGI_REAPER_LOG"] = str(logp)
    _write_seats(graph, [{"name": "seat-a", "pid": 424242, "window": "@50",
                          "role": "director"}]
                       )
    lock = graph / "sessions" / "verify-suite.lock"
    lock.write_text("stale", encoding="utf-8")
    _scan(graph, launcher=_working_launcher([]), window_names=("", "@1 other"))
    assert not lock.exists(), "stale lock removed"
    assert "verify-suite.lock" in logp.read_text(), \
        "the lock removal is logged"
    del os.environ["AGI_REAPER_LOG"]


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