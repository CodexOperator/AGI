"""Predecessor autopsy pre-fill (hypothesis:l4-a-recovery-seating-gets-its-
predecessor-autopsy-pre-filled-from-files).

Proves, on FIXTURE files only (registry json + transcript + rotation record +
a reaper-log stand-in) — never a live spawn, never a real tmux, never real
git writes:
  (a) `_run_autopsy` prints every labelled line with the fixture's values
      FROM FILES ONLY, heartbeats excluded from the last-10, entries after the
      death timestamp excluded;
  (b) a live pid prints `alive: yes` and the autopsy still prints;
  (c) no record -> `launch: not recorded (record: none)`, never an exit 2;
  (d) a reaper log naming SIGTERM for the pid -> the probable-cause line;
  (e) `cmd_autopsy` exits 0 and prints the block;
  (f) the commands the autopsy runs are ALL read-only (git rev-list /
      rev-parse / status --porcelain — never merge/kill/tmux);
  (g) `cmd_spawn` with a dead pid in the seat row ends its `[seating]` block
      with the autopsy; `--no-autopsy` omits it and leaves the base block.

SL2.02 residue (same hypothesis's region, Prime XI line (7)):
  (h) a successful `cmd_spawn --seat S` ALSO writes rotate-self step 2's two
      writes — the meter pin at gen 1 (`sessions/<S>.meter`, the SAME writer)
      and `seats/<S>.ack.json` with `answer: pending`, and the `[seating]`
      block carries all three worktree facts;
  (i) a FAILED spawn removes the pre-window first-seating bootstrap record
      (`_first_seating_run` wrote it before the window came up) — no 'started'
      record behind;
  (j) a POST-join bootstrap with a no-op join writes `unresolved: join found
      nothing within <N>s`, never the pre-join `pending: resolved after join`.
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

import rotate  # noqa: E402


class _Proc:
    def __init__(self, rc=0, out="", err=""):
        self.returncode = rc
        self.stdout = out
        self.stderr = err


DEAD_PID = 3526521  # a "gone" pid that must not exist on this box


def _mk_seats(root, seat, pid):
    """A config:seats node with one row carrying a (dead) pid."""
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    row = {"name": seat, "role": "parent", "tier": 3, "model": "claude-opus-5",
           "pid": pid, "generation": 11}
    (nodes / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n  - "
        + json.dumps(row) + "\n---\n", encoding="utf-8")


def _mk_registry(root, pid, transcript, death_ms):
    """A `--registry-dir` `<pid>.json` carrying the measured shape."""
    reg = root / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / f"{pid}.json").write_text(json.dumps(
        {"pid": pid, "sessionId": "dead-sess", "cwd": "/tmp/wt",
         "status": "idle", "updatedAt": death_ms, "statusUpdatedAt": death_ms,
         "tmux": "agi-rc:@9.%9", "name": "dead-seat",
         "transcript": str(transcript)}), encoding="utf-8")
    return reg


def _mk_transcript(root, death_ts_iso, n_entries=14, heartbeats=4):
    """A CC JSONL transcript: `n_entries` assistant text/tool_use entries at
    1s intervals ending at `death_ts_iso`, interleaved with `heartbeats`
    content-less assistant lines that MUST be excluded from the last-10, plus
    two entries strictly AFTER the death ts that MUST be excluded."""
    path = root / "transcript.jsonl"
    _fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    end = datetime.strptime(death_ts_iso, _fmt)
    lines = []
    # two post-death entries first (file order) — must be bounded out
    for k in (1, 2):
        ts = _fmt_stamp(_add_s(end, k * 5))
        lines.append(assistant_text(ts, f"after-death-{k}"))
    for i in range(n_entries):
        ts = _fmt_stamp(_add_s(end, -(n_entries - i)))
        if i % 5 == 0:
            # a heartbeat: assistant with NO text/tool_use content — skipped
            lines.append(heartbeat(ts))
        elif i % 2 == 0:
            lines.append(assistant_text(ts, f"entry-{i}"))
        else:
            lines.append(assistant_tool(ts, "Bash", {"command": f"echo {i}"}))
    heart = _fmt_stamp(_add_s(end, -1))
    lines.append(assistant_text(heart, "last-before-death"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _fmt_stamp(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _add_s(dt, secs):
    import datetime as _d
    return dt + _d.timedelta(seconds=secs)


def heartbeat(ts):
    return json.dumps({"type": "assistant", "timestamp": ts,
                       "message": {"content": []}})


def assistant_text(ts, text):
    return json.dumps({"type": "assistant", "timestamp": ts,
                       "message": {"content": [{"type": "text", "text": text}]}})


def assistant_tool(ts, name, inp):
    return json.dumps({"type": "assistant", "timestamp": ts,
                       "message": {"content": [{"type": "tool_use",
                                                "name": name, "input": inp}]}})


def _mk_record(root, seat):
    """A rotation record for `seat` carrying handover/result (no launch field)."""
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True, exist_ok=True)
    (rot / f"{seat}.20260911T000000Z.json").write_text(json.dumps(
        {"seat": seat, "rotation": "rotate-self", "trigger": "rotate-self",
         "result": "success", "handover": {
             "own_window": {"name": f"{seat}-old", "id": "@1"},
             "successor_window": {"name": f"{seat}-new", "id": "@2"}}}),
        encoding="utf-8")
    return rot


def _run_fake_git(monkeypatch, captured=None):
    """A subprocess-run seam: read-only git answers; everything else recorded."""
    def _run(cmd, **kwargs):
        if captured is not None:
            captured.append(cmd)
        if isinstance(cmd, str):
            return _Proc(0, "")
        if cmd and cmd[0] == "git":
            if cmd[1:3] == ["rev-list", "--count"]:
                return _Proc(0, "3\n")
            if "--verify" in cmd and "MERGE_HEAD" in cmd:
                return _Proc(1, "")
            if cmd[1:5] == ["status", "--porcelain"]:
                return _Proc(0, " M .agi/nodes/x.md\n?? .agi/comms/foo.md\n")
        return _Proc(0, "")
    monkeypatch.setattr(rotate.subprocess, "run", _run)


def _fixture(tmp_path, seat="deadseat", transcript_override=None):
    root = tmp_path
    death_iso = "2026-09-11T15:19:56.528Z"
    # ms epoch that MUST round-trip to death_iso under the autopsy's own
    # `datetime.utcfromtimestamp(ms/1000)` — computed in UTC, never local.
    _dt = datetime.strptime(death_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
    import calendar
    death_ms = int(calendar.timegm(_dt.utctimetuple()) * 1000)
    _mk_seats(root, seat, DEAD_PID)
    tp = transcript_override or _mk_transcript(root, death_iso)
    reg = _mk_registry(root, DEAD_PID, tp, death_ms)
    _mk_record(root, seat)
    return root, reg, tp


def test_autopsy_full_block_from_fixture(tmp_path):
    """Every labelled line present with the fixture's value; heartbeats and
    post-death entries excluded from the last-10; `unresolved merge` degrades
    to `no` on the bare fixture tmp dir (no MERGE_HEAD)."""
    root, reg, tp = _fixture(tmp_path)
    lines = rotate._run_autopsy(seat="deadseat", pid=DEAD_PID,
                                registry_dir=str(reg), root=root)
    txt = "\n".join(lines)
    assert "[autopsy] predecessor pid: 3526521 alive: no (gone)" in txt
    assert "[autopsy] death time: 2026-09-11T15:19:56Z (source: registry updatedAt)" in txt
    assert f"[autopsy] transcript: {tp}" in txt
    # the last-10 section excludes heartbeats (5 seen above) and the two
    # after-death entries, and includes `last-before-death`
    assert "[autopsy] last 10 non-heartbeat entries before death:" in txt
    assert "entry-" in txt and "last-before-death" in txt
    assert "after-death-" not in txt
    # exactly 10 entry lines follow the header (reaper/section lines indent
    # the same way, so match only text/tool_use entry lines)
    body = txt.split("[autopsy] last 10 non-heartbeat entries before death:", 1)[1]
    entry_lines = [l for l in body.splitlines()
                   if l.startswith("[autopsy]   ")
                   and (" tool_use " in l or " text: " in l)]
    assert len(entry_lines) == 10, entry_lines
    # record launch (no launch script field -> named from the record)
    assert "launch: record <deadseat>" in txt
    assert "result success" in txt
    # worktree lines; behind degrades to n/a on the bare tmp dir
    assert "[autopsy] worktree: behind origin/season/s2 n/a" in txt


def test_autopsy_live_pid_still_prints(tmp_path):
    """A live pid (the test's own) prints `alive: yes` and the autopsy still
    prints instead of refusing — a live predecessor is a fact, not a refusal."""
    root = tmp_path
    _mk_seats(root, "live", os.getpid())
    # no registry, no record, no transcript for the live pid
    lines = rotate._run_autopsy(seat="live", pid=os.getpid(),
                                registry_dir=None, root=root)
    txt = "\n".join(lines)
    assert "alive: yes" in txt
    assert "[autopsy] last 10 non-heartbeat entries before death:" in txt
    assert "(no transcript on disk)" in txt


def test_autopsy_no_record_launch_is_none_not_fail(tmp_path):
    """No rotation record -> `launch: not recorded (record: none)`, and the
    autopsy still exits 0 — never a hard failure."""
    root = tmp_path
    _mk_seats(root, "fresh", DEAD_PID)
    lines = rotate._run_autopsy(seat="fresh", pid=DEAD_PID,
                                registry_dir=None, root=root)
    assert "launch: not recorded (record: none)" in "\n".join(lines)


def test_autopsy_read_only_commands(tmp_path, monkeypatch):
    """The subprocess-list the autopsy runs is ALL read-only git: no merge, no
    kill, no tmux, no writes."""
    root, reg, tp = _fixture(tmp_path)
    captured = []
    _run_fake_git(monkeypatch, captured=captured)
    rotate._run_autopsy(seat="deadseat", pid=DEAD_PID,
                        registry_dir=str(reg), root=root)
    assert captured, "expected the worktree/git reads to run"
    readonly_git_head = {"rev-list", "rev-parse", "status", "log", "show"}
    for cmd in captured:
        assert cmd[0] == "git", cmd
        # git -C <root> <verb> ... — the -C prefix is itself read-only
        idx = 1
        if cmd[1] == "-C":
            idx = 3
        assert cmd[idx] in readonly_git_head, cmd
        joined = " ".join(cmd[1:])
        # never a merge, kill, checkout, or any non-read verb
        for bad in (" merge", "kill", "checkout", "add -A", " reset", "commit"):
            assert bad not in joined, cmd


def test_autopsy_cmd_exits_zero(tmp_path, capsys):
    """`cmd_autopsy` prints the same block and exits 0."""
    root, reg, tp = _fixture(tmp_path)
    args = SimpleNamespace(seat="deadseat", pid=DEAD_PID,
                           registry_dir=str(reg))
    rc = rotate.cmd_autopsy(args, root)
    out = capsys.readouterr().out
    assert rc == 0
    assert "[autopsy] predecessor pid: 3526521 alive: no (gone)" in out


def test_spawn_recovery_appends_autopsy_and_no_autopsy_omits(
        tmp_path, monkeypatch, capsys):
    """`cmd_spawn` with a dead pid in the seat row ends its `[seating]` block
    with the autopsy; `--no-autopsy` omits only the autopsy and keeps the base
    `[seating]` lines."""
    root, reg, _tp = _fixture(tmp_path, seat="spawnseat")
    _run_fake_git(monkeypatch)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **k: (0, "x"))
    monkeypatch.setattr(rotate, "_first_seating_announce",
                        lambda *a, **k: [])
    monkeypatch.setattr(rotate, "_current_sequence", lambda root: 7)

    base = dict(name="spawnseat", tier="parent", prompt_file=None, model=None,
                effort=None, settings=None, successor_argv=None, seat="spawnseat",
                tmux_session="t", window_path=None, dry_run=False,
                registry_dir=str(reg), no_autopsy=False, pid=DEAD_PID)
    rc = rotate.cmd_spawn(SimpleNamespace(**base), root)
    out = capsys.readouterr().out
    assert rc == 0
    assert "[seating] spawned-by: cmd_spawn" in out
    assert "[seating] worktree:" in out
    assert "[seating] previous seat died — predecessor autopsy:" in out
    assert "[autopsy] predecessor pid: 3526521 alive: no (gone)" in out
    # the autopsy is the LAST block: no `[seating]` line after the last autopsy
    last_autopsy = out.rfind("[autopsy]")
    assert out.rfind("[seating]") < last_autopsy

    # --no-autopsy keeps the base block but drops the autopsy
    base["no_autopsy"] = True
    capsys.readouterr()
    rc2 = rotate.cmd_spawn(SimpleNamespace(**base), root)
    out2 = capsys.readouterr().out
    assert rc2 == 0
    assert "[seating] spawned-by: cmd_spawn" in out2
    assert "[autopsy]" not in out2
    assert "[seating] previous seat died" not in out2


def test_spawn_pins_meter_gen1_ack_pending_and_three_worktree_facts(
        tmp_path, monkeypatch, capsys):
    """(h) SL2.02 residue: a successful spawn ALSO does rotate-self step 2's
    two writes — pins the seat's meter at gen 1 (the SAME `_pin_successor_
    meter`, never a second format) and writes seats/<S>.ack.json with `answer:
    pending`; and the `[seating]` block carries all three worktree facts (the
    `behind N` / `unresolved merge` / `dirty` line from `_seating_worktree_
    lines`)."""
    root, reg, _tp = _fixture(tmp_path, seat="pinseat")
    _run_fake_git(monkeypatch)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **k: (0, "x"))
    monkeypatch.setattr(rotate, "_first_seating_announce",
                        lambda *a, **k: [])
    monkeypatch.setattr(rotate, "_current_sequence", lambda root: 3)

    base = dict(name="pinseat", tier="parent", prompt_file=None, model=None,
                effort=None, settings=None, successor_argv=None, seat="pinseat",
                tmux_session="t", window_path=None, dry_run=False,
                registry_dir=str(reg), no_autopsy=False, pid=DEAD_PID)
    rc = rotate.cmd_spawn(SimpleNamespace(**base), root)
    out = capsys.readouterr().out
    assert rc == 0

    # the meter pin: `sessions/<seat>.meter` = `1\t<transcript>` (gen 1)
    pin = root / "sessions" / "pinseat.meter"
    assert pin.is_file(), out
    assert pin.read_text(encoding="utf-8").startswith("1\t")
    # the ack: `sessions/seats/<seat>.ack.json` with `answer: pending`
    ack = root / "sessions" / "seats" / "pinseat.ack.json"
    assert ack.is_file(), out
    ack_doc = json.loads(ack.read_text(encoding="utf-8"))
    assert ack_doc["answer"] == "pending"
    assert ack_doc["seat"] == "pinseat" and ack_doc["gen_after"] == 1
    # the [seating] base block carries all three worktree facts
    assert "[seating] worktree: behind" in out
    assert "unresolved merge:" in out
    assert "dirty:" in out
    # observation (a): the record line names the next write, never a hard `none`
    assert "record: none yet (this seating writes one)" in out


def test_spawn_failed_leaves_no_started_record(tmp_path, monkeypatch):
    """(i) Prime XI line (7) second half: a FAILED spawn removes the
    pre-window first-seating bootstrap record `_first_seating_run` wrote, so
    no 'started' record survives a seat that never came up."""
    root, reg, _tp = _fixture(tmp_path, seat="failseat")
    _run_fake_git(monkeypatch)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **k: (1, "boom"))
    monkeypatch.setattr(rotate, "_current_sequence", lambda root: 0)

    # _first_seating_run writes the gen-1 bootstrap record BEFORE the window
    # spawn — mirror the real pre-window write (Prime's 'the record it wrote')
    def fake_first_run(root, **kw):
        rotate._write_bootstrap(root, seat=kw["seat"], generation=1,
                                telemetry=None, verification=None)
        return "BLOCK", []
    monkeypatch.setattr(rotate, "_first_seating_run", fake_first_run)

    base = dict(name="failseat", tier="parent", prompt_file=None, model=None,
                effort=None, settings=None, successor_argv=None, seat="failseat",
                tmux_session="t", window_path=None, dry_run=False,
                registry_dir=str(reg), no_autopsy=False, pid=DEAD_PID)
    rc = rotate.cmd_spawn(SimpleNamespace(**base), root)
    assert rc == 1
    rec = root / "sessions" / "seats" / "failseat.bootstrap.json"
    assert not rec.exists(), "failed spawn left a pre-window 'started' record"


def test_noop_join_bootstrap_prints_unresolved_not_pending(tmp_path):
    """(j) Prime XI line (7) second half: a POST-join bootstrap whose join
    resolved nothing writes `unresolved: join found nothing within <N>s` for
    the join-pending facts — never the pre-join `pending: resolved after
    join`. The pre-join write (join_poll_secs None) still promises the future
    join as before."""
    root = tmp_path
    out = rotate._write_bootstrap(
        root, seat="nopjoin", generation=1,
        telemetry=["successor_address", "successor_live_model",
                   "model_refusal_fallback"],
        verification=None,
        join_pending={"successor_address", "successor_live_model",
                      "model_refusal_fallback"},
        join_poll_secs=rotate.REGISTRY_JOIN_TIMEOUT_S)
    doc = json.loads(Path(out).read_text(encoding="utf-8"))
    for key in ("successor_address", "successor_live_model",
                "model_refusal_fallback"):
        assert doc["telemetry"][key] == (
            f"unresolved: join found nothing within "
            f"{rotate.REGISTRY_JOIN_TIMEOUT_S}s"), key
    # pre-join (join not yet attempted) keeps the old promise
    out2 = rotate._write_bootstrap(
        root, seat="prejoin", generation=1,
        telemetry=["successor_address"], verification=None,
        join_pending={"successor_address"}, join_poll_secs=None)
    doc2 = json.loads(Path(out2).read_text(encoding="utf-8"))
    assert doc2["telemetry"]["successor_address"] == "pending: resolved after join"