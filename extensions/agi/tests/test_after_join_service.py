"""The captive after_join first turn, performed by THE SERVICE
(hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-
fires-at-turn-one, owed item (i)).

Implements `run_after_join` in rotate.py: after a rotation has happened, the
SERVICE (the heal.py watch loop when `agent_dispatch.inline_reaper` is false,
else the rotate-self post-spawn tail as the fallback when no service runs)
waits `startup.after_join_delay_s` (default 20), runs the template's
`startup.after_join` list as ONE ordered flow, writes every command's output
into the rotation record, and sends ONE dm — the successor's SECOND input —
whose decision is CAPTIVE (it prints the exact copy-paste `diff` line, so the
successor runs NOTHING).

Hermetic: no real wait (injectable sleep), no real tmux/spawn (echo commands),
no real dm (injectable send). Tests for rotate-self's dry-run-run-nothing are
in test_rotate_startup.py's sibling path; here the one-function + two-caller
contract is the claim.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
from agi.bin import heal  # noqa: E402  (after_join service caller)

# Fully-filled canonical placeholder values (mirrors test_rotate_startup).
VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "worktree": "/wt",
    "repo": "/repo",
    "tmux_session": "agi-rc",
    "pred_pids": "123 456",
}


def _startup(after_join=None, delay_s=None):
    s = {}
    if after_join is not None:
        s["after_join"] = after_join
    if delay_s is not None:
        s["after_join_delay_s"] = delay_s
    return s


class _Rec:
    """subprocess.run stand-in that answers every command with a fixed
    output so the no-shell executor returns deterministic rc/output."""

    def __init__(self, rc=0, out="", err=""):
        self.returncode = rc
        self.stdout = out
        self.stderr = err


def _fake_run(monkeypatch, proc=None):
    if proc is None:
        proc = _Rec(out="echoed")
    def _run(cmd, **kwargs):
        return proc
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    return proc


def test_delay_is_honoured_injectable_no_real_wait():
    """(a) the `startup.after_join_delay_s` delay is honoured — sleep_impl is
    called with it once before any command, and a missing key defaults to 20.
    No real waiting: sleep_impl is a recorder."""
    slept = []
    startup = _startup(after_join=[{"label": "join", "cmd": "echo {seat}"}],
                       delay_s=5)
    out = rotate.run_after_join(
        Path("."), seat="sanctuary-director", gen=11, startup=startup,
        values=VALUES, dry_run=False, sleep_impl=lambda s: slept.append(s),
        send_dm=lambda to, text: None)
    assert slept == [5], "sleep_impl must be called once with after_join_delay_s"
    assert out["delay_s"] == 5
    # default when absent
    slept2 = []
    rotate.run_after_join(
        Path("."), seat="s", gen=1, startup=_startup(
            after_join=[{"label": "x", "cmd": "echo x"}]),
        values=VALUES, sleep_impl=lambda s: slept2.append(s),
        send_dm=lambda to, text: None)
    assert slept2 == [20], "default after_join_delay_s is 20"


def test_one_flow_order_join_pin_ack_model_confirm_reap_proof():
    """(b) the after_join list runs in EXACTLY the declared order — join, pin,
    ack, model_confirm, reap-proof — one flow, every command's label present in
    the same sequence as the template declares it."""
    startup = _startup(after_join=[
        {"label": "join", "cmd": "echo join-done"},
        {"label": "pin", "cmd": "echo pin-done"},
        {"label": "ack", "cmd": "echo ack-done"},
        {"label": "model_confirm", "cmd": "echo model-done"},
        {"label": "reap-proof", "cmd": "echo reap-done"},
    ])
    import agi.bin.rotate as rot
    calls = []
    real_run = rot.subprocess.run
    def _capture(cmd, **kwargs):
        calls.append(cmd)
        return _Rec(out=f"{cmd[1]}-out")
    rot.subprocess.run = _capture
    try:
        out = rotate.run_after_join(
            Path("."), seat="s", gen=11, startup=startup, values=VALUES,
            delay_override=0, sleep_impl=lambda s: None,
            send_dm=lambda to, text: None)
    finally:
        rot.subprocess.run = real_run
    labels = [r["label"] for r in out["results"]]
    assert labels == ["join", "pin", "ack", "model_confirm", "reap-proof"], labels
    assert out["results"][0]["rc"] == 0
    assert "join-done-out" in out["results"][0]["output"]


def test_dm_carries_captive_copy_paste_line():
    """(c) the captive dm text carries the literal copy-paste `diff` line the
    successor would emit — including the resolved seat and gen."""
    startup = _startup(after_join=[{"label": "ack", "cmd": "echo {seat}"}])
    import agi.bin.rotate as rot
    real_run = rot.subprocess.run
    rot.subprocess.run = lambda cmd, **kw: _Rec(out="ack")
    try:
        out = rotate.run_after_join(
            Path("."), seat="sanctuary-director", gen=9, startup=startup,
            values=VALUES, delay_override=0, sleep_impl=lambda s: None,
            send_dm=lambda to, text: None)
    finally:
        rot.subprocess.run = real_run
    dm = out["dm"]
    assert "## AFTER_JOIN OUTPUT" in dm
    line = ("python3 extensions/agi/bin/rotate.py "
            "ack --seat sanctuary-director --gen 9 "
            "--ref abc123 diff --text -")
    assert line in dm, "captive copy-paste line must appear verbatim"


def test_record_receives_every_command_output():
    """(d) every after_join command's output lands in the rotation record's
    `after_join.results`, and the marker makes a second pass skip it."""
    rec_path = Path(".") / "seat.20260911T000000Z.json"
    rec_path.write_text(json.dumps({"rotation": "rotate-self", "seat": "s",
                                    "result": "success", "gen_after": 7}))
    startup = _startup(after_join=[
        {"label": "pin", "cmd": "echo pin-op"},
        {"label": "ack", "cmd": "echo ack-op"},
    ])
    import agi.bin.rotate as rot
    real_run = rot.subprocess.run
    rot.subprocess.run = lambda cmd, **kw: _Rec(out=cmd[1])
    sent = []
    try:
        out = rotate.run_after_join(
            Path("."), seat="s", gen=7, startup=startup, values=VALUES,
            record_path=str(rec_path), delay_override=0,
            sleep_impl=lambda s: None,
            send_dm=lambda to, text: (sent.append(text), None)[1])
        assert out["appended"] is True
        saved = json.loads(rec_path.read_text())
        aj = saved["after_join"]
        assert aj["performed_by"] == "service"
        assert [r["label"] for r in aj["results"]] == ["pin", "ack"]
        assert all("pin-op" in r["output"] or "ack-op" in r["output"]
                   for r in aj["results"])
        assert sent == [out["dm"]], "exactly ONE dm, the composed text"
    finally:
        rec_path.unlink(missing_ok=True)
        rot.subprocess.run = real_run


def test_heal_service_calls_the_same_rotate_function():
    """(e) caller 1 — the heal.py watch loop (the service when inline_reaper
    is false) reaches the SAME rotate.run_after_join_for_seat, and is a silent
    no-op when inline_reaper is truthy (rotate-self owns after_join).

    heal.py imports `rotate` through its own bin-path (module name `rotate`),
    a DIFFERENT name than `agi.bin.rotate`; patch the module heal binds so the
    mock reaches the code under test."""
    import rotate as hrot
    called = []
    orig_reaper = hrot._inline_reaper_enabled
    orig_seats = hrot._load_seats
    orig_aj = hrot.run_after_join_for_seat
    orig_log = heal._watch_log
    try:
        hrot._inline_reaper_enabled = lambda root: False
        hrot._load_seats = lambda root: [{"name": "seat-a"}, {"seat": "seat-b"}]
        hrot.run_after_join_for_seat = lambda root, seat: (
            called.append(seat) or {})
        heal._watch_log = lambda line: None
        heal._run_pending_after_joins(Path("."))
        assert sorted(called) == ["seat-a", "seat-b"], called
        # inline_reaper truthy -> no-op
        hrot._inline_reaper_enabled = lambda root: True
        heal._run_pending_after_joins(Path("."))
        assert sorted(called) == ["seat-a", "seat-b"], \
            "a truthy inline_reaper must leave after_join to rotate-self"
    finally:
        hrot._inline_reaper_enabled = orig_reaper
        hrot._load_seats = orig_seats
        hrot.run_after_join_for_seat = orig_aj
        heal._watch_log = orig_log


def test_rotate_self_fallback_reaches_the_same_function():
    """(e) caller 2 — rotate.run_after_join_for_seat (the rotate-self fallback
    path's discovery) invokes the SAME run_after_join with the seat's template
    `after_join` list, the matched rotation record as record_path, and the
    succ_ref/succ_transcript resolved through the record's join window @id
    (never a session id in the ref slot)."""
    import agi.bin.rotate as rot
    rec_path = Path(".") / "x.20260911T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "seat-a", "result": "success",
        "gen_after": 7,
        "recorded_at": "2026-09-11T00:00:00.000000Z",
        "handover": {"join": {
            "window_id": "@42", "transcript": "/tmp/fallback.jsonl"}},
    }))
    orig_latest = rot._latest_rotate_record
    orig_find = rot._find_seat
    orig_tmpl = rot._resolve_template
    orig_ftv = rot._first_turn_values
    orig_join = rot._join_successor
    orig_aj = rot.run_after_join
    record = []
    ftv_calls = []
    tmpl = {"startup": _startup(
        after_join=[{"label": "join", "cmd": "echo {seat}"}], delay_s=20)}
    try:
        rot._latest_rotate_record = lambda root, seat: (
            json.loads(rec_path.read_text()), rec_path
        )
        rot._find_seat = lambda root, name: {
            "role": "director", "session_ref": "row-ref-a"}
        rot._resolve_template = lambda root, role: (tmpl, "director", "test")
        rot._join_successor = lambda *a, **k: {
            "found": True, "window_id": "@42", "pid": 99,
            "session_id": "sess-live", "transcript": "/tmp/live.jsonl",
            "name": "seat-a", "path": "/tmp/reg/99.json", "note": "live"}
        rot._first_turn_values = lambda *a, **k: (
            ftv_calls.append(k) or {
                "succ_ref": k.get("succ_ref", ""),
                "succ_transcript": k.get("succ_transcript", ""),
                "seat": "seat-a", "succ_name": k.get("succ_name", "")})
        rot.run_after_join = lambda *a, **kw: (
            record.append((a, kw)) or {
                "delay_s": 20, "results": [], "dm": "",
                "appended": True, "sent": True,
                "record_path": kw.get("record_path")})
        out = rot.run_after_join_for_seat(Path("."), "seat-a")
        assert out is not None
        (_a, kw) = record[0]
        assert kw["startup"]["after_join"][0]["label"] == "join"
        assert str(kw["record_path"]) == str(rec_path)
        assert kw["values"]["succ_ref"] == "row-ref-a", \
            "succ_ref is the seat row's OWN session_ref cell, never a session id"
        assert kw["values"]["succ_transcript"] == "/tmp/live.jsonl", \
            "succ_transcript fills from the live join"
        assert ftv_calls and ftv_calls[-1]["succ_name"] == "seat-a"
    finally:
        rec_path.unlink(missing_ok=True)
        rot._latest_rotate_record = orig_latest
        rot._find_seat = orig_find
        rot._resolve_template = orig_tmpl
        rot._first_turn_values = orig_ftv
        rot._join_successor = orig_join
        rot.run_after_join = orig_aj


def test_after_join_seat_no_join_key_falls_back_to_record_transcript():
    """(1) — a record with NO handover.join.window_id does NO registry join;
    succ_ref still comes ONLY from the row's session_ref; succ_transcript
    falls back to the record's own handover.join.transcript."""
    import agi.bin.rotate as rot
    rec_path = Path(".") / "y.20260911T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "seat-b", "result": "success",
        "gen_after": 2,
        "recorded_at": "2026-09-11T00:00:00.000000Z",
        "handover": {"join": {"transcript": "/tmp/rec-fallback.jsonl"}},
    }))
    orig_latest = rot._latest_rotate_record
    orig_find = rot._find_seat
    orig_tmpl = rot._resolve_template
    orig_join = rot._join_successor
    orig_aj = rot.run_after_join
    joins = []
    record = []
    tmpl = {"startup": _startup(
        after_join=[{"label": "j", "cmd": "echo {seat}"}], delay_s=20)}
    try:
        rot._latest_rotate_record = lambda root, seat: (
            json.loads(rec_path.read_text()), rec_path)
        rot._find_seat = lambda root, name: {"role": "director"}
        rot._resolve_template = lambda root, role: (tmpl, "director", "test")
        rot._join_successor = lambda *a, **k: (joins.append(k) or {"found": True})
        rot.run_after_join = lambda *a, **kw: (
            record.append((a, kw)) or {"record_path": kw.get("record_path")})
        rot.run_after_join_for_seat(Path("."), "seat-b")
        assert joins == [], \
            "no window_id in the record => no registry join attempted"
        (_a, kw) = record[0]
        assert kw["values"]["succ_ref"] == "", \
            "no row session_ref => succ_ref stays empty"
        assert kw["values"]["succ_transcript"] == "/tmp/rec-fallback.jsonl", \
            "succ_transcript falls back to the record's join transcript"
    finally:
        rec_path.unlink(missing_ok=True)
        rot._latest_rotate_record = orig_latest
        rot._find_seat = orig_find
        rot._resolve_template = orig_tmpl
        rot._join_successor = orig_join
        rot.run_after_join = orig_aj


def test_dry_run_resolves_runs_nothing():
    """The dry-run variant resolves every after_join entry and writes NOTHING —
    neither a record append nor a send; and it never sleeps."""
    rec_path = Path(".") / "dry.20260911T000000Z.json"
    rec_path.write_text(json.dumps({"result": "success"}))
    startup = _startup(after_join=[{"label": "ack", "cmd": "echo {seat}"}])
    slept = []
    sent = []
    try:
        out = rotate.run_after_join(
            Path("."), seat="s", gen=3, startup=startup, values=VALUES,
            record_path=str(rec_path), dry_run=True,
            sleep_impl=lambda s: slept.append(s), send_dm=lambda *a: sent.append(a))
        assert out["results"][0]["dry"] is True
        assert out["dm"], "the captive dm is still composed for the plan"
        assert slept == [], "dry-run must never sleep"
        assert sent == [], "dry-run must never send a dm"
        assert json.loads(rec_path.read_text()) == {"result": "success"}, \
            "dry-run must never append to the record"
    finally:
        rec_path.unlink(missing_ok=True)

# ── goal:g15.25 (SL7.40 (a)) — the after_join successor MODEL CONFIRM ──────
# run_after_join performs _confirm_successor_model ONCE, after the successor
# transcript carries its first assistant turn (polled, never a bare fixed
# sleep), and writes the result into the SAME rotation record's
# handover.model_confirm in place.

def test_after_join_confirms_model_once_after_turn_lands_mid_wait(tmp_path):
    """The successor's first assistant turn appears MID-poll: the transcript
    goes from no-model to model between ticks. run_after_join confirms exactly
    ONCE (not before the turn, not repeatedly), writes the result into the
    SAME record's handover.model_confirm, and returns it."""
    import agi.bin.rotate as rot
    tr = tmp_path / "succ.jsonl"
    tr.write_text('{"type":"user","message":{"content":[{"type":"text",'
                  '"text":"hello"}]}}\n', encoding="utf-8")
    rec_path = tmp_path / "seat.20260912T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "s", "result": "success",
        "gen_after": 5,
        "handover": {"successor_window": {"name": "s", "id": "@7"}},
    }), encoding="utf-8")
    startup = {"after_join_delay_s": 5,
               "after_join": [{"label": "ack", "cmd": "echo {seat}"}]}
    val = dict(VALUES)
    val["succ_transcript"] = str(tr)
    real_run = rotate.subprocess.run
    rotate.subprocess.run = lambda cmd, **kw: _Rec(out=cmd[1])

    def _sleep(secs):
        # the successor's FIRST assistant turn lands while the poll waits
        tr.write_text(
            tr.read_text(encoding="utf-8")
            + '{"type":"assistant","message":{"role":"assistant",'
              '"content":[{"tool_use":{"name":"bash","input":{'
              '"command":"echo hi"}}}]},"model":"claude-sonnet-5"}\n',
            encoding="utf-8")
    try:
        out = rotate.run_after_join(
            tmp_path, seat="s", gen=5, startup=startup, values=val,
            record_path=str(rec_path), delay_override=0,
            sleep_impl=_sleep, poll_interval=1.0,
            send_dm=lambda to, text: None)
    finally:
        rotate.subprocess.run = real_run
    mc = out["model_confirm"]
    assert isinstance(mc, dict), mc
    assert mc.get("live") == {"model": "claude-sonnet-5"}, mc
    assert mc.get("confirm_at") == "after_join", mc
    saved = json.loads(rec_path.read_text())
    assert saved["handover"]["model_confirm"] == mc, \
        "the SAME record's handover.model_confirm is filled in place"
    assert saved["handover"]["model_confirm"]["confirm_at"] == "after_join"


def test_after_join_records_named_skip_when_no_turn_within_budget(tmp_path):
    """No assistant turn ever lands within the poll budget: the confirm is
    recorded as a NAMED `skipped: no assistant turn within <N>s`, never a
    bare `skipped`, and the record carries it. The poll is turn-driven — it
    sleeps exactly budget/poll_interval ticks and never a fixed once.""" 
    import agi.bin.rotate as rot
    tr = tmp_path / "succ.jsonl"
    tr.write_text('{"type":"user","message":{"content":[{"type":"text",'
                  '"text":"hello"}]}}\n', encoding="utf-8")
    rec_path = tmp_path / "seat.20260912T000001Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "s", "result": "success",
        "gen_after": 3, "handover": {}}), encoding="utf-8")
    startup = {"after_join_delay_s": 5,
               "after_join": [{"label": "ack", "cmd": "echo x"}]}
    val = dict(VALUES)
    val["succ_transcript"] = str(tr)
    real_run = rotate.subprocess.run
    rotate.subprocess.run = lambda cmd, **kw: _Rec(out=cmd[1])
    sleeps = []
    try:
        out = rotate.run_after_join(
            tmp_path, seat="s", gen=3, startup=startup, values=val,
            record_path=str(rec_path), delay_override=0,
            sleep_impl=lambda s: sleeps.append(s),
            poll_interval=2.0, timeout_s=4,
            send_dm=lambda to, text: None)
    finally:
        rotate.subprocess.run = real_run
    mc = out["model_confirm"]
    assert isinstance(mc, str) and "skipped: no assistant turn within 4s" in mc, mc
    assert sleeps == [2.0, 2.0], \
        "poll sleeps N=budget/interval ticks, never one fixed sleep"
    saved = json.loads(rec_path.read_text())
    assert saved["handover"]["model_confirm"] == mc


# ── goal:g15.25 (SL7.40) — the after_join fills BOTH join-only facts ───────
# The confirm result writes only `successor_live_model` in the prior cut;
# `model_refusal_fallback` (the SECOND join-only fact the hypothesis names)
# is filled from the successor transcript's last model_refusal_fallback
# system event, BOTH through the existing `_write_bootstrap` overrides seam.

def test_after_join_fills_both_join_facts_through_seam_preserves_resolved(
        tmp_path):
    """run_after_join fills `successor_live_model` AND `model_refusal_fallback`
    in the pre-spawn bootstrap record through the existing overrides seam, and
    preserves a join-only fact ANOTHER path already resolved (successor_address
    set by rotate-self) instead of clobbering it back to `pending:`."""
    tr = tmp_path / "succ.jsonl"
    tr.write_text(
        '{"type":"assistant","message":{"role":"assistant",'
        '"content":[]},"model":"claude-sonnet-5"}\n'
        '{"type":"system","subtype":"model_refusal_fallback",'
        '"timestamp":"2026-09-12T00:00:00.000Z",'
        '"apiRefusalCategory":"safety","requestId":"req-1"}\n',
        encoding="utf-8")
    bdir = tmp_path / "sessions" / "seats"
    bdir.mkdir(parents=True)
    (bdir / "s.bootstrap.json").write_text(json.dumps({
        "shape": "v1", "seat": "s", "generation": 5,
        "written_by": "rotate-self", "commit": None, "measured_at": {},
        "telemetry": {
            "commit": "abc", "seat_row": "{}", "model": "x",
            "effort": "max", "ack": "none", "prev_gen": "4",
            "successor_live_model": "pending: resolved after join",
            "successor_address": "@7",
            "model_refusal_fallback": "pending: resolved after join",
            "mail": "SKIPPED: m", "account": "SKIPPED: a",
            "floor": "SKIPPED: f", "registry": "SKIPPED: r",
            "crons": "SKIPPED: c"},
        "verification": {"ok": True},
    }), encoding="utf-8")
    rec_path = tmp_path / "s.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "s", "result": "success",
        "gen_after": 5, "handover": {}}), encoding="utf-8")
    val = dict(VALUES)
    val["seat"] = "s"
    val["succ_transcript"] = str(tr)
    out = rotate.run_after_join(
        tmp_path, seat="s", gen=5, startup={"after_join_delay_s": 5,
                                              "after_join": []},
        values=val, record_path=str(rec_path), delay_override=0,
        poll_interval=1.0, sleep_impl=lambda s: None,
        send_dm=lambda to, text: None)
    mc = out["model_confirm"]
    assert isinstance(mc, dict) and mc.get("confirm_at") == "after_join", mc
    tele = json.loads((bdir / "s.bootstrap.json").read_text())["telemetry"]
    assert tele["successor_live_model"] == str({"model": "claude-sonnet-5"}), \
        tele
    assert tele["model_refusal_fallback"] == (
        "ts=2026-09-12T00:00:00.000Z category=safety requestId=req-1"), \
        tele
    assert tele["successor_address"] == "@7", \
        "a join fact already resolved (rotate-self) is preserved, never clobbered"
    for k in ("successor_live_model", "model_refusal_fallback"):
        assert not str(tele[k]).startswith("pending:"), (k, tele[k])


def test_service_entry_run_after_join_for_seat_confirms_and_fills(tmp_path,
                                                                  monkeypatch):
    """gap (3): the PRODUCTION service entry `run_after_join_for_seat` (the
    heal.py watch loop's per-seat action, rotate.py ~9094) reaches the ONE
    after_join confirm — a real record + a real successor transcript carrying
    an assistant turn and a model_refusal_fallback event end with the record's
    handover.model_confirm overwritten by a real `after_join` verdict and the
    bootstrap record's TWO join-only facts filled."""
    tr = tmp_path / "succ.jsonl"
    tr.write_text(
        '{"type":"assistant","message":{"role":"assistant",'
        '"content":[]},"model":"claude-sonnet-5"}\n'
        '{"type":"system","subtype":"model_refusal_fallback",'
        '"timestamp":"2026-09-12T09:00:00.000Z",'
        '"apiRefusalCategory":"safety","requestId":"req-9"}\n',
        encoding="utf-8")
    bdir = tmp_path / "sessions" / "seats"
    bdir.mkdir(parents=True)
    (bdir / "seat-a.bootstrap.json").write_text(json.dumps({
        "shape": "v1", "seat": "seat-a", "generation": 7,
        "written_by": "rotate-self", "commit": None, "measured_at": {},
        "telemetry": {"model": "x", "effort": "max",
                       "successor_live_model": "pending: resolved after join",
                       "model_refusal_fallback": "pending: resolved after join"},
        "verification": {"ok": True},
    }), encoding="utf-8")
    rec_path = tmp_path / "seat-a.20200101T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "seat-a", "result": "success",
        "gen_after": 7,
        "recorded_at": "2020-01-01T00:00:00.000000Z",
        "handover": {"join": {"window_id": "@42",
                                "transcript": str(tr)}}}), encoding="utf-8")
    monkeypatch.setattr(
        rotate, "_latest_rotate_record",
        lambda root, seat: (json.loads(rec_path.read_text()), str(rec_path)))
    monkeypatch.setattr(
        rotate, "_find_seat",
        lambda root, seat: {"name": "seat-a", "model": "x",
                            "effort": "max", "role": "parent"})
    monkeypatch.setattr(
        rotate, "_resolve_template",
        lambda root, role: ({}, "parent", "mem"))
    monkeypatch.setattr(
        rotate, "_join_successor",
        lambda root, seat, window_id, poll_secs: {
            "found": True, "pid": None, "session_id": None,
            "transcript": str(tr)})
    sleeps = []
    out = rotate.run_after_join_for_seat(
        tmp_path, "seat-a", sleep_impl=lambda s: sleeps.append(s),
        send_dm=lambda to, text: None)
    assert out is not None
    mc = out["model_confirm"]
    assert isinstance(mc, dict) and mc.get("confirm_at") == "after_join", mc
    assert sleeps == [], f"turn present at tick 0 -> no real poll sleep: {sleeps}"
    saved = json.loads(rec_path.read_text())
    assert saved["handover"]["model_confirm"] == mc, \
        "the production service entry reaches the confirm and writes the record"
    b = json.loads((bdir / "seat-a.bootstrap.json").read_text())
    assert b["telemetry"]["successor_live_model"] == str(
        {"model": "claude-sonnet-5"})
    assert b["telemetry"]["model_refusal_fallback"].startswith(
        "ts=2026-09-12T09:00:00.000Z"), b["telemetry"]["model_refusal_fallback"]
