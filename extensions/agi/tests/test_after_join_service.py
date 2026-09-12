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
import os
import sys
import time
from datetime import datetime, timezone
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


def _startup(after_join=None, delay_s=None, max_age=None):
    s = {}
    if after_join is not None:
        s["after_join"] = after_join
    if delay_s is not None:
        s["after_join_delay_s"] = delay_s
    if max_age is not None:
        s["after_join_max_age_s"] = max_age
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
        assert aj["performer"] == "watch"  # (SL7.72) default = the watch
        assert aj["performed_by"] == "watch"  # legacy key kept in lockstep
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
        hrot.run_after_join_for_seat = lambda root, seat, **kw: (
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
        rot._resolve_template = lambda root, role, explicit=None, **kw: (tmpl, "director", "test")
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
        rot._resolve_template = lambda root, role, explicit=None, **kw: (tmpl, "director", "test")
        rot._join_successor = lambda *a, **k: (joins.append(k) or {"found": True})
        rot.run_after_join = lambda *a, **kw: (
            record.append((a, kw)) or {"record_path": kw.get("record_path")})
        # (SL7.76) the seat row must be LIVE for the after_join to run at all:
        # a dead row (no pid/session/window, join not attempted) is skipped.
        # A live pid keeps this test on the transcript-fallback path.
        rot._find_seat = lambda root, name: {"role": "director", "pid": os.getpid()}
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
    bootstrap record's TWO join-only facts filled. NOW UNSTUBBED: it drives the
    REAL `_resolve_template(root, role, None)` against a fixture rotation
    template (SL7.54 — the old 2-arg call raised TypeError, so the reach was
    only exercised through a lambda)."""
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
    # (goal:g15.25 SL7.54) the reach test drives run_after_join_for_seat
    # through the REAL `_resolve_template(root, role, None)` against a fixture
    # rotation template — the OLD 2-arg call raised TypeError here. The role
    # default template declares an empty after_join list so no real command
    # runs, but a real resolution + handover.model_confirm + fill occur.
    td = tmp_path / "nodes" / ".geometry"
    td.mkdir(parents=True, exist_ok=True)
    (td / "rotations.md").write_text(
        "---\ntemplates:\n  parent:\n    startup:\n      after_join: []\n---\n",
        encoding="utf-8")
    assert rotate._resolve_template(tmp_path, "parent", None) == (
        {"startup": {"after_join": []}}, "parent", "role default (parent)")
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


# ── goal:g15.25 (SL7.54) — recorded_at is UTC, never naive-local ─────────
def test_after_join_due_check_reads_recorded_at_as_utc(tmp_path):
    """A rotation record's `recorded_at` (isoformat + Z, a UTC instant) is
    parsed as UTC, never as a naive LOCAL wall clock. Force the box into a
    fixed non-UTC zone (EDT) and stamp a record 30 s before `now` in UTC with
    DEFAULT_AFTER_JOIN_DELAY_S=20: it is genuinely DUE, but the OLD naive-local
    parse reads its UTC wall-clock numbers as local time, shifting it 4 h into
    the future so `run_after_join_for_seat` returns None (not due). The UTC
    parse must let it through."""
    import agi.bin.rotate as rot
    # deterministically non-UTC local zone for the OLD naive-local path
    old_tz = os.environ.get("TZ")
    os.environ["TZ"] = "America/New_York"
    has_tzset = hasattr(time, "tzset")
    if has_tzset:
        time.tzset()
    try:
        now = time.time()
        rec_ts = datetime.fromtimestamp(now - 30, timezone.utc) \
            .isoformat().replace("+00:00", "Z")  # 30 s ago, UTC
        rec_path = tmp_path / "due.20260912T000000Z.json"
        rec_path.write_text(json.dumps({
            "rotation": "rotate-self", "seat": "s", "result": "success",
            "gen_after": 2, "recorded_at": rec_ts,
            "handover": {"join": {"window_id": "@1",
                                   "transcript": "/tmp/s.jsonl"}}}))
        orig_latest = rot._latest_rotate_record
        orig_find = rot._find_seat
        orig_tmpl = rot._resolve_template
        orig_join = rot._join_successor
        orig_aj = rot.run_after_join
        record = []
        tmpl = _startup(after_join=[], delay_s=20)
        try:
            rot._latest_rotate_record = lambda root, seat: (
                json.loads(rec_path.read_text()), rec_path)
            rot._find_seat = lambda root, name: {"role": "parent"}
            rot._resolve_template = lambda root, role, explicit=None, **kw: (
                tmpl, "parent", "test")
            rot._join_successor = lambda *a, **k: {"found": True}
            rot.run_after_join = lambda *a, **kw: (
                record.append((a, kw)) or {"record_path": kw.get(
                    "record_path"), "model_confirm": "ran"})
            out = rot.run_after_join_for_seat(Path(tmp_path), "s", now=now)
            assert record, \
                "record stamped 30 s ago in UTC with delay 20 is DUE; the old " \
                "naive-local parse shifted it 4 h into the future (EDT)"
            assert out["model_confirm"] == "ran"
        finally:
            rot._latest_rotate_record = orig_latest
            rot._find_seat = orig_find
            rot._resolve_template = orig_tmpl
            rot._join_successor = orig_join
            rot.run_after_join = orig_aj
    finally:
        if old_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old_tz
        if has_tzset:
            time.tzset()


# ── goal:g15.25 (SL7.54 fix 3) — join-facts rewrite is SURGICAL ──────────
# kid 1 (a00-0f166884) claimed fixes (3)(4)(5) "already landed". NOT TRUE:
# re-measured on HEAD 865b4d15, _fill_bootstrap_join_facts passed NO
# join_poll_secs and its overrides carried ONLY the join facts, so every
# OTHER fact was re-derived through _derive_bootstrap_fact (a measured ack
# fact clobbered) and an unresolved join fact read the PRE-join
# "pending: resolved after join" lie. These three tests prove the fix.

def _seed_bootstrap_record(bpath, telemetry, measured_at):
    bpath.parent.mkdir(parents=True, exist_ok=True)
    bpath.write_text(json.dumps({
        "shape": "v1", "seat": bpath.stem.replace(".bootstrap", ""),
        "generation": 9, "written_by": "rotate-self", "commit": "abc111",
        "measured_at": measured_at, "telemetry": telemetry,
        "verification": {"ok": True},
    }), encoding="utf-8")


def test_fill_bootstrap_join_facts_touches_only_join_facts_byte_identical(
        tmp_path):
    """fix 3 (surgical): the fill rewrites ONLY the join facts — every
    NON-join telemetry fact (incl. a MEASURED ack fact) keeps its
    byte-identical value AND its measured_at stamp; it is never re-derived
    through _derive_bootstrap_fact (which clobbered the ack) and never
    restamped at this write's commit."""
    import agi.bin.rotate as rot
    bpath = tmp_path / "sessions" / "seats" / "seat-x.bootstrap.json"
    tele = {
        "ack": "continue (source predecessor, gen 9)",
        "model": "claude-opus-5", "effort": "max",
        "mail": "SKIPPED: m", "account": "SKIPPED: a",
        "floor": "SKIPPED: f", "registry": "SKIPPED: r", "crons": "SKIPPED: c",
        "successor_live_model": "pending: resolved after join",
        "successor_address": "@7",
        "model_refusal_fallback": "pending: resolved after join",
    }
    measured = {"ack": "acc1111111111", "model": "abcc2222222222",
                "successor_live_model": "old-commit-1"}
    _seed_bootstrap_record(bpath, dict(tele), dict(measured))
    ok = rot._fill_bootstrap_join_facts(
        tmp_path, seat="seat-x",
        live_model='{"model": "claude-sonnet-5"}',
        refusal_fallback="ts=2026-09-12T11:00:00.000Z category=safety "
                          "requestId=req-3",
        join_poll_secs=30)
    assert ok
    b = json.loads(bpath.read_text())
    t = b["telemetry"]
    # join facts (successor_address preserved, never clobbered)
    assert t["successor_live_model"] == '{"model": "claude-sonnet-5"}', t
    assert t["model_refusal_fallback"] == (
        "ts=2026-09-12T11:00:00.000Z category=safety requestId=req-3"), t
    assert t["successor_address"] == "@7", t
    # every NON-join fact: value AND measured_at byte-identical
    for k in ("ack", "model", "effort", "mail", "account",
              "floor", "registry", "crons"):
        assert t[k] == tele[k], (k, t[k])
        assert b["measured_at"].get(k) == measured.get(k), \
            (k, b["measured_at"], measured)
    # the ack fact in particular — the kid-1-clobbered fact
    assert t["ack"] == "continue (source predecessor, gen 9)", t
    assert b["measured_at"]["ack"] == "acc1111111111", b["measured_at"]


def test_fill_bootstrap_join_facts_unresolved_when_join_found_nothing(
        tmp_path):
    """fix 3 (unresolved): when the join RESOLVED NOTHING (no live model),
    the threaded join_poll_secs writes `unresolved: join found nothing within
    <N>s` for the unresolved join fact — never the PRE-join `pending: resolved
    after join` lie that a future join will fix it."""
    import agi.bin.rotate as rot
    bpath = tmp_path / "sessions" / "seats" / "seat-y.bootstrap.json"
    tele = {
        "ack": "continue (source predecessor, gen 9)",
        "model": "claude-opus-5", "effort": "max",
        "successor_live_model": "pending: resolved after join",
        "model_refusal_fallback": "pending: resolved after join",
    }
    _seed_bootstrap_record(bpath, dict(tele), {})
    ok = rot._fill_bootstrap_join_facts(
        tmp_path, seat="seat-y", live_model=None,
        refusal_fallback=None, join_poll_secs=30)
    assert ok
    b = json.loads(bpath.read_text())
    t = b["telemetry"]
    assert t["successor_live_model"] == "unresolved: join found nothing within 30s", t
    assert t["model_refusal_fallback"] == (
        "unresolved: join found nothing within 30s"), t
    for k in ("ack", "model", "effort"):
        assert t[k] == tele[k], (k, t[k])


# ── goal:g15.25 (SL7.54 fix 4) — pre-turn probe defers only when armed ──
def test_after_join_performer_armed_branches(tmp_path, monkeypatch):
    """fix 4: a SERVICE performer is armed exactly when the fixture forces the
    fallback, OR inline_reaper is truthy (rotate-self is the fallback), OR the
    box declares the unit (`reaper.unit_enabled` not false) AND the heal watch
    is demonstrably alive (`_watch_alive` reads its per-pass heartbeat). With a
    dead/absent/stale heartbeat the SERVICE is NOT armed — rotate-self's own
    tail performs at step (6.4) instead."""
    import agi.bin.rotate as rot
    # forced: always armed
    assert rot._after_join_performer_armed(tmp_path, forced=True)
    # inline_reaper truthy -> rotate-self fallback performer
    monkeypatch.setattr(rot, "_inline_reaper_enabled", lambda root: True)
    assert rot._after_join_performer_armed(tmp_path)
    monkeypatch.setattr(rot, "_inline_reaper_enabled", lambda root: False)
    # the box declares the unit armed; only watch LIVENESS decides from here.
    (tmp_path / "agi-tree.config.json").write_text(
        json.dumps({"reaper": {"unit_enabled": True}}), encoding="utf-8")
    # inline_reaper off, NO heartbeat -> watch not alive -> no SERVICE armed
    # (the rotate-self tail performs at (6.4); the pre-turn probe must not
    #  record a deferral-to-service that nobody will honour)
    assert not rot._after_join_performer_armed(tmp_path)
    # a LIVE heartbeat -> unit armed, watch alive -> armed
    _live_heartbeat(tmp_path, monkeypatch)
    assert rot._after_join_performer_armed(tmp_path)
    # unit refused -> no service performer (never reaches the alive check)
    (tmp_path / "agi-tree.config.json").write_text(
        json.dumps({"reaper": {"unit_enabled": False}}), encoding="utf-8")
    assert not rot._after_join_performer_armed(tmp_path)
    # unit re-armed, STALE heartbeat -> watch dead -> not armed
    (tmp_path / "agi-tree.config.json").write_text(
        json.dumps({"reaper": {"unit_enabled": True}}), encoding="utf-8")
    _live_heartbeat(tmp_path, monkeypatch,
                    at=time.time() - rot.WATCH_HEARTBEAT_GRACE_S - 10)
    assert not rot._after_join_performer_armed(tmp_path)
    # unit re-armed, fresh heartbeat from a DEAD pid -> not armed
    _live_heartbeat(tmp_path, monkeypatch, pid=999_999_999)
    assert not rot._after_join_performer_armed(tmp_path)


# ── goal:g15.25 (SL7.54 fix 5) — pushed-seats memo cleared per run ────────
def test_run_after_join_for_seat_clears_pushed_seats_memo(tmp_path, monkeypatch):
    """fix 5: run_after_join_for_seat clears the per-process pushed-seats
    fetch memo (`_prime_rows_fetch_clear`) at the START of EVERY run — a
    long-lived reaper process must not pin the first-fetched prime row across
    Prime rotations. Two runs in one process each clear the memo."""
    import agi.bin.rotate as rot
    cleared = []
    rec_path = tmp_path / "c.20200101T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": "c", "result": "success",
        "gen_after": 3, "recorded_at": "2020-01-01T00:00:00.000000Z",
        "handover": {"join": {"window_id": "@1",
                               "transcript": "/tmp/c.jsonl"}}}),
        encoding="utf-8")
    tmpl = _startup(after_join=[], delay_s=0)
    monkeypatch.setattr(rot, "_prime_rows_fetch_clear",
                        lambda: cleared.append(1))
    monkeypatch.setattr(
        rot, "_latest_rotate_record",
        lambda root, seat: (json.loads(rec_path.read_text()),
                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent",
                                            "pid": os.getpid()})
    monkeypatch.setattr(
        rot, "_resolve_template",
        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": False})
    monkeypatch.setattr(rot, "run_after_join",
                        lambda *a, **kw: {"model_confirm": "ran"})
    # (SL7.76) the row carries a LIVE pid (os.getpid) so this seat is NOT
    # skipped as a dead seat — the memo-clear is what this test measures, and
    # the liveness gate must not turn an old record into a one-shot skip.
    out = rot.run_after_join_for_seat(Path(tmp_path), "c")
    assert out is not None
    assert len(cleared) == 1, cleared
    # a SECOND run in the SAME process (the reaper loop) clears again
    rot.run_after_join_for_seat(Path(tmp_path), "c")
    assert len(cleared) == 2, cleared


# ── goal:g15.25 — the service dm is sent by a DECLARED SENDER, never ────────
# `from: unknown` (hypothesis:l4-the-service-after-join-dm-is-sent-by-a-
# declared-signed-sender-never-from-unknown). The default send_dm passed
# send(root, to, text, None) — sender None → send.py falls to 'unknown' when
# no seat env is exported, and `_sign_line` signed only when a key exists for
# that (unknown) id. Now the default passes ONE declared sender resolved by
# `_after_join_sender`: the custodian/outgoing seat when its key exists, else
# the system sender `heal`. `unknown` can no longer appear; the record names
# dm_sender + dm_signed.
import types as _types


def _stub_send(monkeypatch, module_name="send"):
    """Register a stub `send` module (the name rotate.run_after_join's default
    closure imports) and the table under test."""
    stub = _types.ModuleType(module_name)
    calls = []
    stub.send = lambda root, to, text, sender: calls.append((to, sender))
    monkeypatch.setitem(sys.modules, module_name, stub)
    return calls


def test_default_send_dm_names_heal_without_a_seat_key(tmp_path, monkeypatch):
    """No `<sessions>/seats/<seat>.key` exists: the default send_dm passes the
    SYSTEM sender `heal` (never None → never 'unknown'), the dm still sends,
    and the record names dm_sender=heal + dm_signed=false (unsigned-but-named)."""
    calls = _stub_send(monkeypatch)
    rec_path = tmp_path / "s.json"
    rec_path.write_text(json.dumps({"result": "success", "seat": "s"}),
                        encoding="utf-8")
    startup = _startup(after_join=[{"label": "ack", "cmd": "echo x"}])
    out = rotate.run_after_join(
        tmp_path, seat="s", gen=2, startup=startup, values=VALUES,
        record_path=str(rec_path), delay_override=0,
        sleep_impl=lambda s: None)
    assert calls == [("s", "heal")], \
        "default closure passes ONE declared sender, never None: %r" % calls
    assert out["sent"] is True, "the dm is still delivered, named"
    aj = json.loads(rec_path.read_text())["after_join"]
    assert aj["dm_sender"] == "heal", aj
    assert aj["dm_signed"] is False, aj


def test_default_send_dm_signs_when_the_custodian_seat_key_exists(
        tmp_path, monkeypatch):
    """The outgoing/custodian seat HAS a key under `<sessions>/seats/`: the
    default send_dm passes that SEAT name (resolved by the ONE helper), so
    send.py signs — and the record names dm_sender=<seat> + dm_signed=true."""
    kdir = tmp_path / "sessions" / "seats"
    kdir.mkdir(parents=True, exist_ok=True)
    (kdir / "seat-a.key").write_text(
        json.dumps({"scheme": "ed25519", "priv_hex": "ab" * 32}),
        encoding="utf-8")
    calls = _stub_send(monkeypatch)
    rec_path = tmp_path / "sa.json"
    rec_path.write_text(json.dumps({"result": "success", "seat": "seat-a"}),
                        encoding="utf-8")
    out = rotate.run_after_join(
        tmp_path, seat="seat-a", gen=2,
        startup=_startup(after_join=[{"label": "ack", "cmd": "echo x"}]),
        values=VALUES, record_path=str(rec_path), delay_override=0,
        sleep_impl=lambda s: None)
    assert calls == [("seat-a", "seat-a")], calls
    aj = json.loads(rec_path.read_text())["after_join"]
    assert aj["dm_sender"] == "seat-a", aj
    assert aj["dm_signed"] is True, aj


def test_after_join_sender_resolves_deterministically(tmp_path):
    """ONE helper, deterministic from (root, seat): a keyed seat resolves to
    itself (the custodian that can SIGN); an unkeyed seat resolves to the
    system sender `heal`. No input resolves to 'unknown' — so the watch and the
    tail can never diverge on the same seat (the falsifier)."""
    assert rotate._after_join_sender(tmp_path, "seat-a") == "heal", \
        "unkeyed seat -> system sender heal"
    kdir = tmp_path / "sessions" / "seats"
    kdir.mkdir(parents=True, exist_ok=True)
    (kdir / "seat-a.key").write_text("{}", encoding="utf-8")
    assert rotate._after_join_sender(tmp_path, "seat-a") == "seat-a", \
        "keyed seat -> the custodian seat itself"


def test_after_join_dm_record_carries_sender_in_dry_run_too(tmp_path):
    """The record fields dm_sender/dm_signed are populated by the same
    resolution whether or not a send fires (a caller-injected send_dm still
    records the DECLARED sender); and the dry-run resolves but never sends."""
    rec_path = tmp_path / "dry.json"
    rec_path.write_text(json.dumps({"result": "success"}), encoding="utf-8")
    startup = _startup(after_join=[{"label": "ack", "cmd": "echo x"}])
    sent = []
    out = rotate.run_after_join(
        tmp_path, seat="s", gen=1, startup=startup, values=VALUES,
        record_path=str(rec_path), dry_run=True, send_dm=lambda *a: sent.append(a))
    assert sent == [], "dry-run never sends"
    assert json.loads(rec_path.read_text()) == {"result": "success"}, \
        "dry-run never appends sender fields to the record"
    assert out["dm"], "dry-run still plans the captive dm"

# ── hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-
# ── refused-by-name-and-skipped-never-run-on-the-empty-slot ───────────────
# (g15 build order 2026-09-12) An after_join entry that USES a placeholder
# whose value resolves EMPTY is refused by name and never executed — no rc, no
# output. Generic to every after_join entry (the ack's empty `{succ_ref}`
# refuses the SAME way as the reap-proof's empty `{pred_pids}`), fallback is
# honored with first_turn's precedence, and a first seeding's NAMED value
# (`none: first seating`) is a NON-empty string that still runs.

def _assert_named_refusal(r, key, reason):
    assert "refused" in r and "rc" not in r and "output" not in r, r
    assert f"placeholder {{{key}}} empty" in r["refused"], r["refused"]
    assert reason in r["refused"], r["refused"]
    assert "skipped by name" in r["refused"], r["refused"]


def test_empty_pred_pids_refuses_named_never_runs():
    """The reap-proof repro: empty `{pred_pids}` on a MAIN post with no
    predecessor chain must refuse BY NAME (no predecessor chain) and never
    execute — `grep -E ''` must never match the whole process table."""
    entry = {"label": "reap-proof",
             "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'"}
    vals = dict(VALUES)
    vals["pred_pids"] = ""
    import agi.bin.rotate as rot
    real_run = rot.subprocess.run
    rot.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("refused entry must NEVER run"))
    try:
        r = rot._run_after_join_command(entry, vals, 60, 4000)
    finally:
        rot.subprocess.run = real_run
    _assert_named_refusal(r, "pred_pids", "no predecessor chain")


def test_non_empty_pred_pids_runs():
    """A non-empty `{pred_pids}` resolves and the entry RUNS (rc present, no
    refusal)."""
    entry = {"label": "reap-proof", "cmd": "echo poll {pred_pids}"}
    r = rotate._run_after_join_command(entry, VALUES, 60, 4000)
    assert "rc" in r and "refused" not in r, r
    assert "123 456" in r.get("output", ""), r


def test_first_seating_named_value_runs_not_refusal():
    """A first seating's NAMED value `none: first seating` is a NON-empty
    string — the entry still runs (its grep matches nothing, exit 1), not a
    refusal."""
    entry = {"label": "reap-proof", "cmd": "echo {pred_pids}"}
    vals = dict(VALUES)
    vals["pred_pids"] = "none: first seating"
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    assert "rc" in r and "refused" not in r, r
    assert "first seating" in r.get("output", ""), r


def test_empty_succ_ref_ack_refuses_named():
    """Generic to every after_join entry: the ack entry's empty `{succ_ref}`
    refuses by name (row session_ref empty), never run."""
    entry = {"label": "ack",
             "cmd": "python3 extensions/agi/bin/rotate.py "
                    "ack --seat {seat} --gen {gen} --ref {succ_ref} "
                    "diff --text -"}
    vals = dict(VALUES)
    vals["succ_ref"] = ""
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    _assert_named_refusal(r, "succ_ref", "row session_ref empty")


def test_empty_gen_refuses_named():
    """`gen` also carries a named reason (no generation resolved)."""
    entry = {"label": "ack", "cmd": "echo gen {gen}"}
    vals = dict(VALUES)
    vals["gen"] = ""
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    _assert_named_refusal(r, "gen", "no generation resolved")


def test_unmapped_empty_placeholder_still_refuses_named():
    """A placeholder with no mapped reason still refuses, NAMING the
    placeholder — never an invented silent pass."""
    entry = {"label": "x", "cmd": "echo {seat}"}
    vals = dict(VALUES)
    vals["seat"] = ""
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    assert "refused" in r and "rc" not in r, r
    assert "placeholder {seat} empty" in r["refused"], r["refused"]
    assert "skipped by name" in r["refused"], r["refused"]


def test_usable_per_entry_fallback_resolves_instead_of_refusing():
    """An entry whose placeholder has a usable per-entry `fallback:` resolves
    through the fallback instead of refusing."""
    entry = {"label": "ack", "cmd": "echo {succ_ref}",
             "fallback": "none-provided"}
    vals = dict(VALUES)
    vals["succ_ref"] = ""
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    assert "rc" in r and "refused" not in r, r
    assert "none-provided" in r.get("output", ""), r


def test_usable_code_fallback_prime_ref_resolves():
    """The code map _STARTUP_FALLBACKS resolves an emptied `{prime_ref}` to the
    by-key whois form (`--key {prime_key}`) instead of refusing — same
    precedence first_turn uses."""
    entry = {"label": "whois", "cmd": "echo {prime_ref}"}
    vals = dict(VALUES)
    vals["prime_ref"] = ""
    vals["prime_key"] = "pubKEY123"
    r = rotate._run_after_join_command(entry, vals, 60, 4000)
    assert "rc" in r and "refused" not in r, r
    assert "--key pubKEY123" in r.get("cmd", ""), r
    assert "pubKEY123" in r.get("output", ""), r


def test_dm_prints_refused_and_refusal_line_for_empty_pred_pids():
    """The dm goes through the EXISTING refused branch of
    `_compose_after_join_dm` — it prints REFUSED plus the refusal line, with no
    new dm branch."""
    startup = _startup(after_join=[
        {"label": "reap-proof",
         "cmd": "ps -e | grep -E '{pred_pids}'"},
    ])
    vals = dict(VALUES)
    vals["pred_pids"] = ""
    import agi.bin.rotate as rot
    # (SL7.73 harvest) the thrower guards the ONE executor of an after_join
    # command, `_run_units_no_shell` — not `subprocess.run` wholesale, which
    # SL7.75's `_after_join_sender` -> `_sessions_dir` -> git also reaches for
    # the sender resolution (a merge interaction, not a defect of either).
    real_run = rot._run_units_no_shell
    rot._run_units_no_shell = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("refused entry must NEVER run"))
    sent = []
    try:
        out = rot.run_after_join(
            Path("."), seat="s", gen=11, startup=startup, values=vals,
            delay_override=0, sleep_impl=lambda s: None,
            send_dm=lambda to, text: sent.append(text))
    finally:
        rot._run_units_no_shell = real_run
    r = out["results"][0]
    assert "refused" in r and "rc" not in r and "output" not in r, r
    assert "REFUSED" in out["dm"], out["dm"]
    assert "no predecessor chain" in out["dm"], out["dm"]
    assert "skipped by name" in out["dm"], out["dm"]
    assert sent == [out["dm"]], "exactly ONE dm, the composed text"

# ── goal:g15.25 (SL7.72) — after_join performed live vs by rotate-self tail ──
def _live_heartbeat(root, monkeypatch, *, pid=None, at=None):
    """Write a fresh heal-watch heartbeat (`<sessions>/reaper.watch.json`) with
    a live pid (default: the test process) so `_watch_alive` reads it alive."""
    import agi.bin.rotate as rot
    sess = root / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    (sess / rot.WATCH_HEARTBEAT_FILE).write_text(json.dumps({
        "pid": pid if pid is not None else os.getpid(),
        "at": at if at is not None else time.time(),
    }), encoding="utf-8")


def _rotation_record(tmp_path, seat, *, recorded_at="2020-01-01T00:00:00.000000Z"):
    """A due rotation record for `seat` under `<tmp>/sessions/rotations/`."""
    rec_path = tmp_path / "sessions" / "rotations" / f"{seat}.20200101T000000Z.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": seat, "result": "success",
        "gen_after": 1, "recorded_at": recorded_at,
        "handover": {"join": {"window_id": "@1", "transcript": "/tmp/j.jsonl"}}}),
        encoding="utf-8")
    return rec_path


def test_no_watcher_tail_performs(tmp_path, monkeypatch):
    """(a) inline_reaper FALSE + no heartbeat file => `_after_join_performer_armed`
    is False (no SERVICE armed) yet `_after_join_tail_should_perform` is True —
    rotate-self's own post-spawn tail performs the captive after_join itself, so
    a rotation never depends on a watcher that is not running. The record ends
    with `after_join.performer == "tail"` (never absent, never {})."""
    import agi.bin.rotate as rot
    monkeypatch.setattr(rot, "_inline_reaper_enabled", lambda root: False)
    assert not rot._after_join_performer_armed(tmp_path)
    assert rot._after_join_tail_should_perform(tmp_path)
    rec_path = _rotation_record(tmp_path, "tail-seat")
    tmpl = _startup(after_join=[{"label": "join", "cmd": "echo tail-ran"}],
                    delay_s=0)
    _fake_run(monkeypatch)
    # the TAIL path performs with performer="tail" (step (6.4) passes this).
    out = rot.run_after_join(
        Path(tmp_path), seat="tail-seat", gen=1, startup=tmpl, values=VALUES,
        record_path=str(rec_path), sleep_impl=lambda s: None,
        send_dm=lambda to, text: None, performer="tail")
    rec = json.loads(rec_path.read_text())
    aj = rec.get("after_join")
    assert isinstance(aj, dict) and aj, "after_join must never be absent/{} on a tail-performed record"
    assert aj.get("performer") == "tail", aj
    assert aj.get("performed_by") == "tail", aj
    assert aj.get("results"), "the tail's single command must be recorded"
    assert out["appended"] is True


def test_watch_alive_tail_skips(tmp_path, monkeypatch):
    """(b) a FRESH heartbeat with a live pid => `_watch_alive` True and the
    SERVICE is armed, so `_after_join_tail_should_perform` is False — the tail
    does NOT run after_join (deferral to an alive watch is real, no double-
    perform). The watch's own run_after_join_for_seat writes
    `after_join.performer == "watch"` exactly once; a second call returns None."""
    import agi.bin.rotate as rot
    _live_heartbeat(tmp_path, monkeypatch)
    monkeypatch.setattr(rot, "_inline_reaper_enabled", lambda root: False)
    (tmp_path / "agi-tree.config.json").write_text(
        json.dumps({"reaper": {"unit_enabled": True}}), encoding="utf-8")
    assert rot._watch_alive(tmp_path)
    assert rot._after_join_performer_armed(tmp_path)
    assert not rot._after_join_tail_should_perform(tmp_path)

    # the watch performs once on a real record; the tail/skip decision above
    # already proved the tail would not run when the watch is alive.
    rec_path = _rotation_record(tmp_path, "watch-seat")
    tmpl = _startup(after_join=[], delay_s=0)  # empty list -> results []
    def _lat(root, seat):
        return json.loads(rec_path.read_text()), str(rec_path)
    monkeypatch.setattr(rot, "_latest_rotate_record", _lat)
    monkeypatch.setattr(rot, "_find_seat", lambda root, name: {"role": "parent"})
    monkeypatch.setattr(
        rot, "_resolve_template",
        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor", lambda *a, **k: {"found": False})
    monkeypatch.setattr(rot, "_after_join_model_confirm", lambda *a, **k: None)
    _fake_run(monkeypatch)
    out1 = rot.run_after_join_for_seat(Path(tmp_path), "watch-seat",                                       now=1 << 60, performer="watch",
                                       send_dm=lambda to, text: None)
    assert out1 is not None
    r1 = json.loads(rec_path.read_text())
    assert r1.get("after_join") and r1["after_join"].get("performer") == "watch"
    # a second call re-reads the file, sees after_join already present -> None
    out2 = rot.run_after_join_for_seat(Path(tmp_path), "watch-seat",
                                       now=1 << 60, performer="watch",
                                       send_dm=lambda to, text: None)
    assert out2 is None, "already performed: the second watch run must return None"


def test_after_join_key_never_empty(tmp_path, monkeypatch):
    """(c) a rotation with a ZERO-length after_join list still records
    `after_join` with `performer` and `results == []` — never {}; and a record
    that ALREADY carries `after_join` makes the tail skip (double-perform guard,
    via the real production guard `_after_join_already_performed`)."""
    import agi.bin.rotate as rot
    # zero-length list -> after_join present, results []
    rec_path = _rotation_record(tmp_path, "empty-seat")
    tmpl = _startup(after_join=[], delay_s=0)
    _fake_run(monkeypatch)
    rot.run_after_join(
        Path(tmp_path), seat="empty-seat", gen=1, startup=tmpl, values=VALUES,
        record_path=str(rec_path), sleep_impl=lambda s: None,
        send_dm=lambda to, text: None, performer="tail")
    aj = json.loads(rec_path.read_text()).get("after_join")
    assert isinstance(aj, dict) and aj, "after_join must never be {}"
    assert aj.get("performer") == "tail"
    assert aj.get("results") == []

    # already-performed record -> the tail's double-perform guard skips
    done_path = _rotation_record(tmp_path, "done-seat")
    done_rec = json.loads(done_path.read_text())
    done_rec["after_join"] = {"performer": "watch", "results": []}
    done_path.write_text(json.dumps(done_rec), encoding="utf-8")
    assert rot._after_join_already_performed(str(done_path)) is True
    hit = []
    monkeypatch.setattr(
        rot, "_after_join_tail_should_perform", lambda *a, **k: True)
    monkeypatch.setattr(
        rot, "run_after_join",
        lambda *a, **kw: hit.append(1) or {})
    # the (6.4)-shared sequence: decide, then guard, then (only if free) run
    if rot._after_join_tail_should_perform(tmp_path):
        if not rot._after_join_already_performed(str(done_path)):
            rot.run_after_join(Path(tmp_path), seat="done-seat", gen=1,
                               startup={}, values=VALUES,
                               record_path=str(done_path), performer="tail")
    assert not hit, "the tail must NOT call run_after_join on an already-\n            performed record"


# ── goal:g15.25 (SL7.76) — liveness skip + age budget + honest delay ──────
# Parent claim: the after_join catch-up SKIPS a seat with no live session and
# MARKS a late run past its age budget. Four claims: (a) skip a dead seat with
# one log line, record nothing; (b) age budget `startup.after_join_max_age_s`
# (default 300) — a late LIVE seat runs once tagged late, a late DEAD seat is
# marked skipped once; (c) recorded `delay_s` is the TEMPLATE's promise and
# `performed_after_s` is the measured age; (d) the tail path inherits (a)-(c)
# through the SAME run_after_join_for_seat (no second gate — covered by (a)).
def _seed_rotation(tmp_path, name="seat-d", recorded_at="2020-01-01T00:00:00Z",
                   window_id="@42"):
    rec_path = tmp_path / f"{name}.20200101T000000Z.json"
    rec_path.write_text(json.dumps({
        "rotation": "rotate-self", "seat": name, "result": "success",
        "gen_after": 7, "recorded_at": recorded_at,
        "handover": {"join": {"window_id": window_id,
                               "transcript": "/tmp/x.jsonl"}}}),
        encoding="utf-8")
    return rec_path


def test_dead_seat_skipped_no_record_no_dm_one_log(tmp_path, monkeypatch):
    """(a)+(1) a seat row with NO pid, NO session_id, NO window_id, and no
    registry join result, is a DEAD seat: run_after_join_for_seat returns a
    skip, writes NO after_join and NO dm into the record (a fresh-age record
    gets no skip marker either), and heal's loop logs exactly ONE line
    `after_join skipped for <seat>: no live session`."""
    import agi.bin.rotate as rot
    # a FRESH dead seat (age within budget) proves test-1's "record nothing"
    now = time.time()
    fresh = datetime.fromtimestamp(now - 30, timezone.utc)\
        .isoformat().replace("+00:00", "Z")
    rec_path = _seed_rotation(tmp_path, name="dead", window_id="@42",
                              recorded_at=fresh)
    tmpl = {"startup": _startup(after_join=[{"label": "ack", "cmd": "echo x"}],
                                delay_s=5)}
    calls = {"aj": 0, "dm": 0}
    monkeypatch.setattr(rot, "_latest_rotate_record",
                        lambda root, seat: (json.loads(rec_path.read_text()),
                                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent"})  # dead row
    monkeypatch.setattr(rot, "_resolve_template",
                        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": False})
    monkeypatch.setattr(rot, "run_after_join",
                        lambda *a, **kw: (calls.__setitem__("aj",
                                                            calls["aj"] + 1)
                                          or {"results": [], "appended": True,
                                              "sent": True}))
    out = rot.run_after_join_for_seat(
        tmp_path, "dead", send_dm=lambda to, text: calls.__setitem__(
            "dm", calls["dm"] + 1))
    assert out is not None and out.get("skipped") == "no live session", out
    assert calls["aj"] == 0, "dead seat must never reach run_after_join"
    assert calls["dm"] == 0, "dead seat must never send a dm"
    saved = json.loads(rec_path.read_text())
    assert "after_join" not in saved, \
        "a fresh-age dead seat records nothing at all"
    # heal's loop emits exactly ONE skip line for this seat
    logged = []
    import rotate as hrot
    monkeypatch.setattr(hrot, "_inline_reaper_enabled", lambda root: False)
    monkeypatch.setattr(hrot, "_load_seats",
                        lambda root: [{"name": "dead"}])
    monkeypatch.setattr(heal, "_watch_log", lambda line: logged.append(line))
    monkeypatch.setattr(hrot, "run_after_join_for_seat",
                        lambda root, seat: out)
    heal._run_pending_after_joins(tmp_path)
    assert logged == [f"after_join skipped for 'dead': no live session"], logged


def test_second_run_dead_late_seat_is_noop_once_marker_holds(tmp_path,
                                                             monkeypatch):
    """(b)+(2) a DEAD seat whose record is long past its age budget is marked
    `after_join: {skipped: 'no live session', age_s: N}` ONCE; a SECOND run
    over that same dead seat returns None (no-op) because the already-
    performed guard now holds."""
    import agi.bin.rotate as rot
    rec_path = _seed_rotation(tmp_path, name="dead-late")  # 2020 -> very old
    tmpl = {"startup": _startup(after_join=[], delay_s=5)}
    monkeypatch.setattr(rot, "_latest_rotate_record",
                        lambda root, seat: (json.loads(rec_path.read_text()),
                                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent"})
    monkeypatch.setattr(rot, "_resolve_template",
                        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": False})
    monkeypatch.setattr(rot, "run_after_join",
                        lambda *a, **kw: {"results": []})
    out = rot.run_after_join_for_seat(tmp_path, "dead-late")
    assert out is not None and out["skipped"] == "no live session", out
    assert out.get("late") is True, "2020 record is far past the age budget"
    saved = json.loads(rec_path.read_text())
    assert saved["after_join"]["skipped"] == "no live session", saved
    assert isinstance(saved["after_join"]["age_s"], (int, float)), saved
    # second run: the skip marker holds -> no-op
    out2 = rot.run_after_join_for_seat(tmp_path, "dead-late")
    assert out2 is None, "after the once-marked skip, a re-run is a no-op"


def test_live_late_seat_performed_once_tagged_late(tmp_path, monkeypatch):
    """(b)+(3) a LIVE seat whose record is past its age budget is performed
    EXACTLY once, its record's after_join carrying `late: true` and a numeric
    `age_s` — never performed as-if-fresh."""
    import agi.bin.rotate as rot
    rec_path = _seed_rotation(tmp_path, name="seat-live")  # 2020 -> old
    tmpl = {"startup": _startup(after_join=[], delay_s=5,
                                max_age=10)}
    calls = {"n": 0}
    monkeypatch.setattr(rot, "_latest_rotate_record",
                        lambda root, seat: (json.loads(rec_path.read_text()),
                                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent",
                                            "pid": os.getpid()})  # LIVE row
    monkeypatch.setattr(rot, "_resolve_template",
                        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": True, "pid": os.getpid(),
                                         "session_id": "live"})
    real_aj = rot.run_after_join

    def _aj(*a, **kw):
        calls["n"] += 1
        return real_aj(*a, **kw)
    monkeypatch.setattr(rot, "run_after_join", _aj)
    real_run = rot.subprocess.run
    rot.subprocess.run = lambda cmd, **kw: _Rec(out=cmd[1])
    try:
        out = rot.run_after_join_for_seat(tmp_path, "seat-live",
                                          sleep_impl=lambda s: None,
                                          send_dm=lambda to, text: None)
    finally:
        rot.subprocess.run = real_run
    assert calls["n"] == 1, "a live late seat is performed EXACTLY once"
    assert out is not None
    saved = json.loads(rec_path.read_text())
    aj = saved["after_join"]
    assert aj.get("late") is True, aj
    assert isinstance(aj.get("age_s"), (int, float)), aj
    assert aj["age_s"] > 10, aj
    # a SECOND run is a no-op (already performed)
    calls["n"] = 0
    out2 = rot.run_after_join_for_seat(tmp_path, "seat-live")
    assert out2 is None and calls["n"] == 0


def test_fresh_live_seat_unchanged_no_late(tmp_path, monkeypatch):
    """(b)+(4) a FRESH live seat (age within budget) is unchanged: recorded no
    later than its budget so NO `late` key is written, and the record is
    performed normally with the promised template delay."""
    import agi.bin.rotate as rot
    now = time.time()
    rec_ts = datetime.fromtimestamp(now - 30, timezone.utc)\
        .isoformat().replace("+00:00", "Z")  # 30 s ago
    rec_path = _seed_rotation(tmp_path, name="seat-fresh",
                              recorded_at=rec_ts)
    tmpl = {"startup": _startup(after_join=[], delay_s=5)}
    monkeypatch.setattr(rot, "_latest_rotate_record",
                        lambda root, seat: (json.loads(rec_path.read_text()),
                                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent",
                                            "pid": os.getpid()})
    monkeypatch.setattr(rot, "_resolve_template",
                        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": True})
    rot.run_after_join_for_seat(tmp_path, "seat-fresh",
                                sleep_impl=lambda s: None,
                                send_dm=lambda to, text: None)
    saved = json.loads(rec_path.read_text())
    aj = saved["after_join"]
    assert "late" not in aj, f"fresh seat must not be tagged late: {aj}"
    assert aj.get("delay_s") == 5, aj


def test_delay_s_is_template_promise_performed_after_s_is_measured(
        tmp_path, monkeypatch):
    """(c)+(5) the record's `delay_s` equals the TEMPLATE's after_join_delay_s
    (the promised run), never `delay_s: 0` as a claim of promptness; and
    `performed_after_s` is the MEASURED now-recorded_at age (>= 0), a separate
    key."""
    import agi.bin.rotate as rot
    now = time.time()
    rec_ts = datetime.fromtimestamp(now - 120, timezone.utc)\
        .isoformat().replace("+00:00", "Z")  # 120 s ago
    rec_path = _seed_rotation(tmp_path, name="seat-delay", recorded_at=rec_ts)
    tmpl = {"startup": _startup(after_join=[], delay_s=37)}
    monkeypatch.setattr(rot, "_latest_rotate_record",
                        lambda root, seat: (json.loads(rec_path.read_text()),
                                            str(rec_path)))
    monkeypatch.setattr(rot, "_find_seat",
                        lambda root, name: {"role": "parent",
                                            "pid": os.getpid()})
    monkeypatch.setattr(rot, "_resolve_template",
                        lambda root, role, explicit=None, **kw: (tmpl, "parent", "test"))
    monkeypatch.setattr(rot, "_join_successor",
                        lambda *a, **k: {"found": True})
    rot.run_after_join_for_seat(tmp_path, "seat-delay",
                                sleep_impl=lambda s: None,
                                send_dm=lambda to, text: None)
    saved = json.loads(rec_path.read_text())
    aj = saved["after_join"]
    assert aj["delay_s"] == 37, \
        f"delay_s must be the TEMPLATE promise, got {aj['delay_s']}"
    assert aj["delay_s"] != 0, "delay_s 0 must never be written as promptness"
    assert aj.get("performed_after_s") is not None, \
        "the measured performed_after_s key must be present"
    assert aj["performed_after_s"] >= 0, aj
    assert abs(aj["performed_after_s"] - 120) < 5, \
        f"performed_after_s should be ~120 s measured: {aj}"
