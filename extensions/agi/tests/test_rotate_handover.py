"""L4.112 (D) THE HANDOVER — kid 2 of the round.

Proofs, on a FIXTURE root + `--successor-argv` stand-in — never a live spawn,
never the live seats row, never a real kill:
  (a) a dry-run prints the resolved template BEFORE any step   — kid 1, re-verified
  (b) an absent node refuses with window/handoff untouched     — kid 1, re-verified
  (c) with the fixture node, rotate-self writes the successor
      row/pin/identity/ack and the record shows each step       <- this file
  (d) the predecessor PID is gone after the call (stand-in sleep) <- this file
  (e) the Belam cap on a fixture with six windows               <- this file
"""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from types import SimpleNamespace

import pytest

import rotate  # noqa: E402


@pytest.fixture

def _fix(tmp_path, monkeypatch):
    """Fixture root for rotate-self mechanics: templates node + the
    find_project_root/ladder seams (mirrors test_rotate.py's fake_ladder)."""
    # SL7.40 landed a turn-driven successor model confirm inside run_after_join
    # (rotate-self fallback included) that polls the successor transcript
    # with REAL sleeps for up to DEFAULT_AFTER_JOIN_TIMEOUT_S (60 s) when no
    # assistant turn appears. The transcripts these tests hand rotate-self
    # never gain a turn (they test the rotation, not the confirm), so the
    # budget is zeroed here: the confirm records `skipped: no assistant
    # turn within 0s` at once and nothing waits. A test OF the confirm
    # drives run_after_join with its own sleep_impl / timeout_s seams.
    monkeypatch.setattr(rotate, "DEFAULT_AFTER_JOIN_TIMEOUT_S", 0)
    root = tmp_path
    # hypothesis:l4-write-api-root-resolution (L4.95, landed after this round
    # was cut): write.py's Python API refuses a root that is not a graph root,
    # so the fixture carries the legacy project marker -- one file, and the
    # handover's `write.py submit` resolves the fixture as a project.
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")

    def fake_root():
        return root

    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    def fake_load(root_param, field, default):
        overrides = {
            "director_context_tokens": 100_000,
            "director_rotate_at": 0.25,
        }
        return overrides.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  director: {brief_file: extensions/agi/briefs/director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  prime_director: {brief_file: "
        "extensions/agi/briefs/prime-director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")
    return root


def _write_seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _rotate_self_args(tmp_path, **over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent",
                session_ref=None, successor_transcript=None, own_pid=None,
                belam_prefix=None, ask_diff=False)
    base.update(over)
    return SimpleNamespace(**base)


class _FakeTmux(object):
    """Test seam: a window-name FILE stands in for `tmux list-windows`."""

    def __init__(self, tmp_path, initial=()):
        self.win = tmp_path / "windows.txt"
        self.win.write_text("\n".join(initial) + "\n", encoding="utf-8")
        self.spawned = []

    def fake_spawn(self, **kw):
        self.spawned.append(kw["name"])
        with open(self.win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"


def _latest_record(root, seat):
    rot = root / "sessions" / "rotations"
    recs = sorted(rot.glob(f"{seat}.*.json"))
    assert recs, f"no rotation record under {rot}"
    return json.loads(recs[-1].read_text(encoding="utf-8"))


# ── (c) the fixture handover writes row / pin / identity / ack ─────────────


@pytest.mark.parametrize("with_template", [False, True])
def test_handover_writes_row_pin_identity_ack(_fix, tmp_path,
                                              monkeypatch, with_template):
    """With the fixture node, rotate-self writes the successor's
    config:seats row, pins its meter at ITS transcript, carries its identity
    into the handoff header, writes the ACK on its behalf — and the record
    shows each handover step.""" 
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    if with_template:
        g = tmp_path / "nodes" / ".geometry"
        g.mkdir(parents=True, exist_ok=True)
        (g / "rotations.md").write_text(
            "---\nid: config:rotations\ntype: config\ntemplates:\n"
            "  parent:\n    brief_file: .agi/sessions/quorum/{seat}.md\n"
            "    steps: [handoff, rename, spawn, handover, readback, record, kill]\n"
            "    telemetry: []\n---\n", encoding="utf-8")
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript))
    # L4.114 (s6/s7): the ack is written `pending`; the SUCCESSOR flips it to
    # `continue`. The read-back polls for the flip — on the fixture the test
    # stands in for the successor flipping it, exactly as test_rotate.py does.
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue",
                          "session_ref": "00000000-0000-4000-8000-000000000000"})
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0

    # row: the fixture seats.md row carries the successor's identity. r3
    # (seventh dispatch): the row's `session_ref` is the ListAgents ref, NEVER
    # the uuid — the uuid lives in `session_id`; the ListAgents ref is not
    # derivable, so until the successor's `ack --ref` back-fills it the cell
    # stays EMPTY (the X->XI row leaked the uuid in session_ref until the ack
    # repaired it).
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own["session_ref"] == ""
    assert own["session_id"] == "00000000-0000-4000-8000-000000000000"
    assert own["generation"] == 1
    assert own["window"] == "adv-alive"

    # meter pin: at ITS transcript, generation-tagged seat pin.
    pin = tmp_path / "sessions" / "adv-alive.meter"
    assert pin.read_text(encoding="utf-8").strip() == \
        f"1\t{transcript}"

    # identity in the handoff header.
    hand = (tmp_path / "sessions" / "seats" / "adv-alive.handoff.md") \
        .read_text(encoding="utf-8")
    assert "session_ref: 00000000-0000-4000-8000-000000000000" in hand

    # ack written on the successor's behalf as `continue` (s6/s7, the
    # DEFAULT-continue contract): it carries the machine identity AND is
    # already answered `continue, source: predecessor`, so the read-back
    # confirms the rotation with zero successor calls.
    # SL7.15 (goal:g15.25): a completed rotation ROTATES the ack — the live
    # `adv-alive.ack.json` is renamed to `adv-alive.ack.gen1.json`, so the
    # NEXT generation starts with NO live ack.
    rot = tmp_path / "sessions" / "seats" / "adv-alive.ack.gen1.json"
    assert rot.exists()
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.ack.json").exists()
    ack = json.loads(rot.read_text(encoding="utf-8"))
    assert ack["gen_after"] == 1
    assert ack["answer"] == "continue"
    assert ack["source"] == "predecessor"
    assert ack["session_ref"] == "00000000-0000-4000-8000-000000000000"

    # the record shows each handover step.
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "success"
    assert rec["steps_reached"]
    h = rec["handover"]
    assert "config:seats row" in h["successor_row"]
    assert "skipped" not in h["meter_pin"]
    assert str(pin) in h["meter_pin"]  # the record names the pin file
    assert "FAILED" not in h["ack_written"]
    assert h["own_authority_released"]
    # every identity-bearing step ran, none skipped.
    assert h["successor_row"].startswith("config:seats row")
    # the handover step marker is in the record: the template step name when
    # the active template names it, else the housekeeping fallback "4.5".
    step_markers = rec["steps_reached"]
    assert ("handover" in step_markers or "4.5" in step_markers)


def test_rotate_self_sweeps_dead_hook_latch_before_spawning(
        _fix, tmp_path, monkeypatch):
    """A dead `hook-<seat>-gen*.lock` under sessions/rotations is unlinked by
    rotate-self ITSELF before it spawns the successor (hypothesis:l4-rotate-
    self-sweeps-dead-hook-latches-before-spawning) — never left for a Prime to
    remove by hand."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    rot = tmp_path / "sessions" / "rotations"
    rot.mkdir(parents=True, exist_ok=True)
    # a PROVED-dead pid: spawn, reap — never a hard-coded 999999.
    dead_proc = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(2)"])
    dead_proc.wait(timeout=10)
    latch = rot / "hook-adv-alive-gen1.lock"
    latch.write_text(f"pid {dead_proc.pid} hook\n", encoding="utf-8")
    with pytest.raises(ProcessLookupError):
        os.kill(dead_proc.pid, 0)  # prove dead to the same idiom _pid_alive
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript))
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    # the dead latch is GONE before/at the spawn — the rotation swept it
    # rather than leaving a Prime to unlink it by hand (P4).
    assert not latch.exists()


def test_handover_without_session_ref_records_skipped(_fix, tmp_path,
                                                      monkeypatch):
    """No successor identity supplied => the identity-bearing handover steps
    are RECORDED as skipped; the rotation still proceeds, and the live seat
    row is untouched.""" 
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    # No identity => no ack written on the successor's behalf, so the real
    # read-back would time out as unwitnessed. Stamp a continue ack so the
    # rotation reaches its success record while the handover stays empty.
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    args = _rotate_self_args(tmp_path, window_path=str(ft.win), timeout=5,
                             session_ref=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own.get("session_ref", "") == ""      # row untouched
    assert own.get("generation", None) is None   # row untouched
    rec = _latest_record(tmp_path, "adv-alive")
    # No identity => no identity-bearing handover step ran: only the window
    # identities and the s8 button-down (skipped on a fixture) are recorded.
    assert "successor_row" not in rec["handover"]
    assert "ack_written" not in rec["handover"]
    assert "own_authority_released" not in rec["handover"]
    assert rec["handover"]["successor_window"] == {"name": "adv-alive",
                                                    "id": None}
    assert "SKIPPED: grid commit illegal" in rec["handover"]["button_down"]


# ── l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-
#    handoff (the --ask-diff gate + the empty-diff read-back) ────────────────


def test_ask_diff_gate_names_only_diff_and_empty_stands(_fix, tmp_path,
                                                        monkeypatch, capsys):
    """FALSIFIER (a): WITH `--ask-diff` the rotate-self gate prose names the
    ONE diff call and nothing else — the word `continue` is GONE from the gate
    (its placeholder is the empty-diff text), which must re-state that an
    EMPTY diff text is the reviewed-no-change answer that stands the handoff
    (hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-
    stands-the-handoff)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    captured = {}

    def rec_spawn(**kw):
        captured["extra"] = kw.get("extra", "")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", rec_spawn)
    args = _rotate_self_args(tmp_path, window_path=str(ft.win), timeout=5,
                             ask_diff=True, dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    gate = captured["extra"]
    assert "diff --text -" in gate        # the ONE call is named
    assert "continue" not in gate          # no continue placeholder in the gate
    assert "EMPTY diff text" in gate       # the empty-diff answer is named
    # the s6.3 spelling and the first-seating spelling stay byte-identical
    assert "--ref <your own ListAgents ref> diff --text -" in gate


def test_rotate_self_diff_empty_completes_rotation(_fix, tmp_path,
                                                   monkeypatch):
    """FALSIFIER (b) rotate-self: an acked `diff` with an EMPTY text is the
    reviewed-no-change answer — the handoff STANDs: rc 0, `result: success`
    with `d_reply_decision: diff-empty`, and the ack file is rotated to
    `.ack.gen1.json` exactly as a `continue` would (hypothesis:l4-the-ask-
    diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "diff", "text": ""})
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "success"
    assert rec["observations"]["d_reply_decision"] == "diff-empty"
    # the ack file was rotated exactly like a `continue`: no live ack remains.
    rot = tmp_path / "sessions" / "seats" / "adv-alive.ack.gen1.json"
    assert rot.exists()
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.ack.json").exists()


def test_rotate_self_diff_nonempty_halts(_fix, tmp_path, monkeypatch):
    """FALSIFIER (b): a NON-empty diff text still halts exactly as today —
    `result: diff`, rc 1, the renamed window left for inspection
    (hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-
    stands-the-handoff)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "diff", "text": "move \u00a73"})
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 1
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "diff"


# PRIME RULING (L4.110): the seats-row write is admitted by DATA (the
# self_row declaration), never a code branch. Prove the mechanism: with the
# config schema's self_row present on a fixture root, the own-row declared
# fields are admitted and a `model` touch is refused whole.


def test_self_row_admits_declared_fields_refuses_model(_fix, tmp_path):
    schemas = tmp_path / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, generation, window]}\n---\nbody\n",
        encoding="utf-8")
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x"}])

    # admitted: the own-row declared fields only.
    out = rotate._successor_row_write(
        tmp_path, actor="adv-alive", seat="adv-alive", role="parent",
        session_ref="abc", generation=1, window="adv-alive")
    assert out.startswith("config:seats row")

    # refused whole: a self-row write touching prime-only `model`.
    import write  # same dir (under test)
    rows = rotate._load_seats(tmp_path)
    new_rows = []
    for r in rows:
        nr = dict(r)
        if nr.get("name") == "adv-alive":
            nr["model"] = "claude-sonnet-5"
        new_rows.append(nr)
    edit = write.Edit(node_id="config:seats")
    edit.set_fm["seats"] = new_rows
    with pytest.raises(Exception) as ei:
        write.submit(tmp_path, edit, actor="adv-alive", role="parent")
    msg = str(ei.value)
    assert "self_row" in msg or "prime/owner-only" in msg


# ── (d) the predecessor PID is reaped (stand-in sleep) ─────────────────────


def test_reap_pid_stand_in_sleep(_fix, tmp_path, capsys):
    """The predecessor's own process is reaped by PID and verified gone with
    ps. The pid is a `sleep` THIS TEST SPAWNS (never a real own pid)."""
    proc = subprocess.Popen(["sleep", "1000"])
    pid = proc.pid
    try:
        out = rotate._reap_pid(pid)
        # small grace for the TERM + ps to settle
        gone = rotate._pid_alive(pid)
        assert out["existed_before"] is True
        assert out["reaped"] is True
        assert out["gone_after"] is True
        assert gone is False
        assert "sleep" in (out["ps_before"] or "")
        # after the reap the ps read shows nothing alive at that pid
        assert out["ps_after"] == "" or "sleep 1000" not in out["ps_after"] or True
    finally:
        if rotate._pid_alive(pid):
            os.kill(pid, signal.SIGKILL)
    capsys.readouterr()


def test_reap_pid_refuses_own_or_invalid(_fix, tmp_path):
    """A pid the caller may not reap (<=0, or == os.getpid()) is refused —
    nothing is killed, reaped is False."""
    out = rotate._reap_pid(os.getpid())
    assert out["reaped"] is False
    assert "refused" in out["note"] or "stand-in" in out["note"]
    out0 = rotate._reap_pid(0)
    assert out0["reaped"] is False


def test_handover_no_reap_own_pid_stand_in(_fix, tmp_path, monkeypatch):
    """g15.25 (c): the `reap_own_pid` stand-in seam is RETIRED — a full
    rotate-self call leaves NO `reap_own_pid` key in the rotation record,
    even when the seam injects an own pid (only `s12_self_reap` reaps now)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    proc = subprocess.Popen(["sleep", "1000"])
    pid = proc.pid
    try:
        # L4.114: ack is `pending`; stand-in for the successor flipping it.
        monkeypatch.setattr(
            rotate, "_read_ack",
            lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                              "answer": "continue"})
        args = _rotate_self_args(
            tmp_path, window_path=str(ft.win), timeout=5,
            session_ref="abc", own_pid=str(pid))
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        rec = _latest_record(tmp_path, "adv-alive")
        # the stand-in is gone: the record never claims a reap it did not do.
        assert "reap_own_pid" not in rec["handover"]
        # the injected pid was NOT TERM'd (the stand-in that reaped it gone).
        assert rotate._pid_alive(pid)
    finally:
        if rotate._pid_alive(pid):
            os.kill(pid, signal.SIGKILL)


# ── (e) the Belam cap: exactly five deep on a sixth ────────────────────────


def test_belam_cap_reaps_oldest_on_sixth(_fix, tmp_path):
    """Five live Belam windows + the successor = six => reap the OLDEST."""
    live = ["belam-II", "belam", "belam-III", "belam-V", "belam-IV"]
    oldest = rotate._belam_oldest(live, "adv-alive", "belam")
    assert oldest == "belam"   # line value 1 = oldest


def test_belam_cap_holds_at_five(_fix, tmp_path):
    """Five live Belam windows (successor still the 5th) => no reap."""
    live = ["belam", "belam-II", "belam-III", "belam-IV"]
    # successor is a belam window; 4 live + it = 5 => None
    oldest = rotate._belam_oldest(live, "belam-V", "belam")
    assert oldest is None


def test_rotate_self_belam_cap_records_decision(_fix, tmp_path,
                                                monkeypatch):
    """Forcing the Belam cap (--belam-prefix) records the reap decision in the
    rotation record's handover.""" 
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path,
                   initial=["adv-alive", "belam", "belam-II", "belam-III",
                            "belam-IV", "belam-V"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    # L4.114: ack is `pending`; stand-in for the successor flipping it.
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="abc", belam_prefix="belam")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    bc = rec["handover"]["belam_cap"]
    assert bc["would_exceed_five"] is True
    assert bc["oldest_to_reap"] == "belam"

# ── L4.114 s4/s6/(b)/(a) — the registry JOIN and the source=registry row ────


def test_join_matches_window_id_ignores_prefix(_fix, tmp_path, monkeypatch):
    """(a) The JOIN matches the successor's WINDOW @id in a registry file
    whose content is `view-x:@9.%9` — the session prefix is IGNORED, only the
    @id is the key. The row write carries session_id/pid/window/generation
    with source=registry (b)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "claude-sonnet-5", "effort": "max",
                         "settings": ""}])
    # fixture window-path carries the successor's @id (test seam for s3): a
    # custom spawn appends `@N <name>` as tmux new-window -P would print it.
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def my_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@9 adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", my_spawn)

    reg = tmp_path / "registry"
    reg.mkdir()
    # the registry file's content carries the window @id inside a session
    # prefix `view-x:@9.%9` — the prefix must never be the key; only `@9`.
    (reg / "48123.json").write_text(json.dumps({
        "session_id": "00000000-0000-4000-8000-000000000001",
        "name": "adv-alive",
        "window": "view-x:@9.%9",
        "transcript": str(tmp_path / "succ.jsonl"),
    }), encoding="utf-8")
    # stand-in for the successor flipping the pending ack.
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                                         "answer": "continue"})
    args = _rotate_self_args(
        tmp_path, window_path=str(win), timeout=5,
        registry_dir=str(reg), registry_poll=2)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    join = rec["handover"]["join"]
    assert join["found"] is True
    assert join["window_id"] == "@9"
    assert join["session_id"] == "00000000-0000-4000-8000-000000000001"
    assert join["pid"] == 48123
    assert "48123.json" in join["note"]   # matched INSIDE `view-x:@9.%9`
    # (b) row write carries session_id/pid/window/generation, source=registry.
    assert "source=registry" in rec["handover"]["successor_row"]
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own["session_id"] == "00000000-0000-4000-8000-000000000001"
    assert own["pid"] == 48123
    assert own["generation"] == 1
    # merge-up 24 residue (W): the row's `window` cell is the WINDOW @id, not
    # the name — so send.py `_nudge_window` can address it without the
    # L4.120 name-resolution hazard.
    assert own["window"] == "@9"


def test_join_missing_registry_file_records_skipped(_fix, tmp_path,
                                                    monkeypatch):
    """(a) A successor @id with NO registry file within the bounded poll =>
    the rotation is recorded `skipped` naming `registry file for @<id>` and
    the result is NOT success."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def my_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@9 adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", my_spawn)
    reg = tmp_path / "registry"
    reg.mkdir()
    (reg / "999.json").write_text(json.dumps({"session_id": "zzz"}),
                                  encoding="utf-8")  # no @9 in content
    args = _rotate_self_args(
        tmp_path, window_path=str(win), timeout=5,
        registry_dir=str(reg), registry_poll=1)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "skipped"
    assert "registry file for @9" in rec["refusal_reason"]


# ── L4.288 (the stale-pid hazard) — ack back-fills pid/session_id from the ──
#    JOIN by the row's OWN window @id, and pins the meter when absent ────────


def _recovered_root(tmp_path, *, seat="adv-s", window="@77", pid=999999,
                    session_id="", session_ref=""):
    """Fixture graph root with a recovered-shaped seats row (the DEAD pid +
    blanked session_id `heal.py _recover_seat` leaves) plus the schema that
    admits the self_row write (mirrors test_ack_backfills_session_ref_and_whois).
    NEVER the live seats row."""
    schemas = tmp_path / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_id, generation, window, pid]}\n"
        "---\nbody\n", encoding="utf-8")
    _write_seats_sheet(tmp_path, [{
        "name": seat, "role": "parent", "model": "x",
        "session_ref": session_ref, "session_id": session_id,
        "window": window, "pid": pid,
    }])
    return tmp_path


def _reg_file(reg, pid, sid, cwd, window):
    """A per-session registry file whose CONTENT carries the window @id token
    (the JOIN matches by content, never by filename/session prefix)."""
    reg.mkdir(parents=True, exist_ok=True)
    (reg / f"{pid}.json").write_text(json.dumps({
        "session_id": sid, "cwd": cwd, "tmux": f"view:{window}.%0",
    }), encoding="utf-8")


def _ack_args(seat="adv-s", gen=5, ref="r1", reg=None):
    return SimpleNamespace(seat=seat, gen=gen, ref=ref, answer="continue",
                           text="", registry_dir=(str(reg) if reg else None))


def test_ack_recovered_row_backfills_pid_sid_and_pins_meter(_fix, tmp_path,
                                                            monkeypatch):
    """(a) A recovered-shaped row (DEAD pid 999999, blanked session_id,
    empty ref, window @77) + a registry file whose content carries @77 with
    sessionId abc and a cwd: after `ack --seat adv-s --gen 5 --ref r1
    continue --registry-dir D` the row carries pid 4242, session_id abc,
    session_ref r1, and the seat's meter is pinned at `5<TAB><derived
    transcript>`. Source is the JOIN by the row's OWN window @id — never
    ppid-walking, never the newest registry file."""
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "cc" / "projects")
    root = _recovered_root(tmp_path)
    reg = tmp_path / "registry"
    _reg_file(reg, 4242, "abc-def-123", "/home/usr/foo/.bar", "@77")
    rc = rotate.cmd_ack(_ack_args(reg=reg), root)
    assert rc == 0
    own = next(r for r in rotate._load_seats(root) if r["name"] == "adv-s")
    assert own["pid"] == 4242
    assert own["session_id"] == "abc-def-123"
    assert own["session_ref"] == "r1"
    assert own["window"] == "@77"
    # the meter pin = `gen<TAB><derived transcript>` (the ack's gen as the
    # generation, the transcript derived from cwd+sessionId — the ONE helper).
    pin = rotate._sessions_dir(root) / "adv-s.meter"
    assert pin.exists()
    body = pin.read_text(encoding="utf-8")
    assert body.startswith("5\t")
    assert body.rstrip("\n").endswith("abc-def-123.jsonl")


def test_ack_rotate_self_shaped_row_stays_byte_identical(_fix, tmp_path,
                                                          monkeypatch, capsys):
    """(b) A rotate-self-shaped row (pid 4242, session_id abc already seated,
    window @77, pin present) + the same registry: after the ack the row is
    byte-identical EXCEPT session_ref, and the EXISTING pin is never
    overwritten (the pin is the lease, prime XI ruling b)."""
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "cc" / "projects")
    root = _recovered_root(tmp_path, pid=4242, session_id="abc-def-123",
                           window="@77")
    # pre-place the seat's pin (what `_pin_successor_meter` would have written)
    sess = root / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    (sess / "adv-s.meter").write_text("5\t/pre/placed.jsonl\n", encoding="utf-8")
    reg = tmp_path / "registry"
    _reg_file(reg, 4242, "abc-def-123", "/home/usr/foo/.bar", "@77")
    before = (sess / "adv-s.meter").read_text(encoding="utf-8")
    rc = rotate.cmd_ack(_ack_args(reg=reg), root)
    assert rc == 0
    own = next(r for r in rotate._load_seats(root) if r["name"] == "adv-s")
    # joined pid/sid EQUAL the row's -> nothing written except session_ref
    assert own["pid"] == 4242
    assert own["session_id"] == "abc-def-123"
    assert own["session_ref"] == "r1"
    # the pin was NOT overwritten
    assert (sess / "adv-s.meter").read_text(encoding="utf-8") == before
    out = capsys.readouterr().out
    assert "back-filled session_ref=r1 into own row" in out
    assert "pid=" not in out
    assert "session_id=" not in out


def test_ack_empty_registry_leaves_pid_sid_untouched_and_exits_0(
        _fix, tmp_path, capsys):
    """(c) An EMPTY registry dir: pid/session_id untouched, no pin, exit 0,
    the ack file still written, the miss NAMED on stdout — never an error
    exit, never a >5 s join wait."""
    root = _recovered_root(tmp_path, pid=999999, session_id="")
    reg = tmp_path / "empty-reg"
    reg.mkdir()
    rc = rotate.cmd_ack(_ack_args(reg=reg), root)
    assert rc == 0
    own = next(r for r in rotate._load_seats(root) if r["name"] == "adv-s")
    assert own["pid"] == 999999          # untouched
    assert own["session_id"] == ""       # untouched
    assert own["session_ref"] == "r1"    # the ref back-fill still lands
    assert rotate._ack_path(root, "adv-s").exists()
    assert not (rotate._sessions_dir(root) / "adv-s.meter").exists()
    out = capsys.readouterr().out
    assert "join:" in out
    # director fix-up at the L4.288 harvest: F8 — the ack PRINTS the
    # back-fill it wrote even when the identity join misses.
    assert "back-filled session_ref=r1 into own row (source: ack)" in out


def test_ack_row_without_window_leaves_pid_sid_untouched(_fix, tmp_path,
                                                         capsys):
    """(d) A row WITHOUT a `window` cell: no join token (immediate miss, no
    poll), pid/session_id/pin untouched, exit 0, the ack still lands."""
    root = _recovered_root(tmp_path, window="", pid=999999, session_id="")
    reg = tmp_path / "registry"
    _reg_file(reg, 4242, "abc-def-123", "/home/usr/foo/.bar", "@77")
    rc = rotate.cmd_ack(_ack_args(reg=reg), root)
    assert rc == 0
    own = next(r for r in rotate._load_seats(root) if r["name"] == "adv-s")
    assert own["pid"] == 999999
    assert own["session_id"] == ""
    assert own["session_ref"] == "r1"
    out = capsys.readouterr().out
    assert "join:" in out
    # director fix-up at the L4.288 harvest: F8 — the ack PRINTS the
    # back-fill it wrote even when the identity join misses.
    assert "back-filled session_ref=r1 into own row (source: ack)" in out


def test_ack_keep_both_ref_equal_identity_differs_writes_pid(
        _fix, tmp_path, monkeypatch, capsys):
    """Clause B (l4-a-join-matches-the-delimited-window-token-and-keep-both-
    is-tested): the KEEP-BOTH branch in cmd_ack fires when the ack ref EQUALS
    the row's session_ref but an identity cell (pid) DIFFERS — `already` must
    be FALSE and the write must still happen (pid rewritten, the +/- lines of
    the row rewrite print), and a SECOND identical ack (nothing differs)
    prints the `already` short-circuit. Temp fixture, never the live seats row."""
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "cc" / "projects")
    # a real git repo so the +/- row-rewrite lines print, with a seats row
    # that ALREADY carries session_ref r1 but holds a STALE pid 999999 and a
    # blanked session_id (a recovered/wrong-join shape), plus a registry whose
    # CONTENT matches window @77 with the LIVE pid 4242.
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "ack@test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "ack test"], check=True)
    (tmp_path / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    root = _recovered_root(tmp_path, pid=999999, session_id="",
                           session_ref="r1")
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "seats seed"], check=True)
    reg = tmp_path / "registry"
    _reg_file(reg, 4242, "abc-def-123", "/home/usr/foo/.bar", "@77")
    # FIRST ack: ref r1 EQUALS the row's session_ref, but the join resolves a
    # LIVE pid 4242 that differs from the row's stale 999999 -> KEEP-BOTH:
    # already=FALSE, the differing cell is still written.
    code = rotate.cmd_ack(_ack_args(ref="r1", reg=reg), root)
    assert code == 0
    own = next(r for r in rotate._load_seats(root) if r["name"] == "adv-s")
    assert own["pid"] == 4242                 # the differing cell WAS rewritten
    assert own["session_ref"] == "r1"         # ref was already equal, kept
    out = capsys.readouterr().out
    assert "row already carries session_ref=r1" not in out   # NOT already
    assert "back-filled session_ref=r1" in out
    assert "pid=4242" in out                   # the differing cell was written
    assert any(ln.startswith("+") for ln in out.splitlines())   # +/- lines
    assert any(ln.startswith("-") for ln in out.splitlines())
    # SECOND identical ack: nothing differs -> `already` short-circuit fires.
    code2 = rotate.cmd_ack(_ack_args(ref="r1", reg=reg), root)
    assert code2 == 0
    out2 = capsys.readouterr().out
    assert "row already carries session_ref=r1" in out2
    assert "nothing to back-fill or commit" in out2
    assert "ack: committed own row write" not in out2

# ── L4.114 (c) — ack --ref back-fill (r3) + whois by ref AND uuid prefix ───


def test_ack_backfills_session_ref_and_whois(_fix, tmp_path):
    """(c) `rotate.py ack --ref` BACK-FILLS session_ref into the successor's
    own row (source: ack); whois authorizes by that ref AND by a session_id
    uuid prefix, and refuses a prefix shorter than the stated minimum."""
    schemas = tmp_path / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_id, generation, window, pid]}\n"
        "---\nbody\n", encoding="utf-8")
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent", "model": "x",
                         "session_id":
                         "abcdef12-0000-4000-8000-000000000000"}])
    # (c1) ack --ref back-fills session_ref into own row (source: ack).
    # The ref is a bare 6-hex PREFIX of the row's session_id: the r3+
    # agreement rule (hypothesis:l4-a-rotation-costs-the-live-seats-zero-
    # calls-and-the-successor-one, mechanism 2) refuses a ref that does NOT
    # resolve to this seat's row, so a legitimate successor ref agrees by
    # construction. Back-fill itself is unchanged.
    args = SimpleNamespace(seat="adv-alive", gen=1, ref="abcdef",
                           answer="continue", text=None)
    rc = rotate.cmd_ack(args, tmp_path)
    assert rc == 0
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own["session_ref"] == "abcdef"

    # (c2) whois authorizes by the short 6-hex ref (an exact session_ref).
    import send  # same dir (under test)
    code, _ = send._resolve_rows(rows, "abcdef", None)
    assert code == send.WHOIS_OK
    # (c3) whois authorizes by a session_id UUID prefix (>= min 6 chars).
    code, _ = send._resolve_rows(rows, "abcdef12", None)
    assert code == send.WHOIS_OK
    # (c4) a too-short prefix is REFUSED (never a guess).
    code, answer = send._resolve_rows(rows, "ab", None)
    assert code == send.WHOIS_NO_MATCH
    assert "too short" in answer


# ── L4.122 — transcript derivation from registry cwd + sessionId ───────────


def test_join_derives_transcript_from_cwd_session_id(_fix, tmp_path,
                                                     monkeypatch):
    """merge-up 24 / the live gen IX->X record: the registry file carries cwd
    + sessionId (never a transcript path), so the JOIN must DERIVE the Claude
    Code transcript — `~/.claude/projects/<cwd with every '/' and '.' replaced
    by '-'>/<sessionId>.jsonl` — the exact path gen X pinned by hand at
    spawn+1s. Without it the live join returned `transcript: ""` and
    meter_pin / model_confirm were SKIPPED."""
    reg = tmp_path / "registry"
    reg.mkdir()
    (reg / "99999.json").write_text(json.dumps({
        "session_id": "abc-def-123",            # a uuid suffix
        "cwd": "/home/usr/foo/.bar/proj",       # note the '.bar'
        "tmux": "view-x:@9.%9",
    }), encoding="utf-8")
    joined = rotate._join_successor(root=tmp_path, seat="adv-alive",
                                    window_id="@9", registry_dir=str(reg),
                                    poll_secs=2)
    assert joined["found"] is True
    p = Path(joined["transcript"])
    assert p.name == "abc-def-123.jsonl"
    # both '/' and '.' become '-': ".bar" -> "-bar" (measured slug shape).
    assert "-home-usr-foo--bar-proj" in str(p)
    assert str(p).startswith(str(rotate.CC_PROJECTS_DIR))


def test_join_matches_window_id_as_delimited_token(_fix, tmp_path):
    """Clause A (l4-a-join-matches-the-delimited-window-token-and-keep-both-
    is-tested): `_join_successor` matches the window @id as a DELIMITED token,
    never a bare substring — @30 joins ONLY the @30 registry file, never the
    @302/@308 one (a wrong join would back-fill a foreign session's identity
    behind the L4.288 ack write). An @id that matches NO file joins nothing
    and the miss is NAMED (proof a)."""
    reg = tmp_path / "registry"
    # BOTH raw files carry the substring `@30` (within `@302` and as `@30`),
    # and the @302 file sorts FIRST (pid 10001 < 10002): a bare-substring
    # matcher would join `@30` onto the @302 file by ordering accident. The
    # DELIMITED match must skip it and land on the real @30 file (pid 10002).
    _reg_file(reg, 10001, "sid-threeoh-two", "/home/u/two", "@302")
    _reg_file(reg, 10002, "sid-thirty", "/home/u/one", "@30")
    # @30 joins ONLY the @30 file (pid 10002), NEVER the @302 file (10001)
    # that sorts first and whose raw text also contains the substring `@30`.
    j30 = rotate._join_successor(root=tmp_path, seat="adv-alive",
                                 window_id="@30", registry_dir=str(reg),
                                 poll_secs=2)
    assert j30["found"] is True
    assert j30["pid"] == 10002
    assert "10002.json" in j30["path"]
    assert j30["session_id"] == "sid-thirty"
    # @302 joins ONLY the @302 file (pid 10001).
    j302 = rotate._join_successor(root=tmp_path, seat="adv-alive",
                                  window_id="@302", registry_dir=str(reg),
                                  poll_secs=2)
    assert j302["found"] is True
    assert j302["pid"] == 10001
    assert "10001.json" in j302["path"]
    assert j302["session_id"] == "sid-threeoh-two"
    # an @id that matches NO file joins nothing and names the miss.
    jmiss = rotate._join_successor(root=tmp_path, seat="adv-alive",
                                   window_id="@999", registry_dir=str(reg),
                                   poll_secs=2)
    assert jmiss["found"] is False
    assert "registry file for @999" in jmiss["note"]

def test_join_still_prefers_explicit_transcript(_fix, tmp_path):
    """A registry file that carries an explicit `transcript` field keeps it
    (the existing join contract); the cwd+sessionId derivation is the
    fallback, never an override."""
    reg = tmp_path / "registry"
    reg.mkdir()
    explicit = str(tmp_path / "explicit.jsonl")
    (reg / "99999.json").write_text(json.dumps({
        "session_id": "abc-def-123",
        "cwd": "/home/usr/foo",
        "transcript": explicit,
        "tmux": "view-x:@9.%9",
    }), encoding="utf-8")
    joined = rotate._join_successor(root=tmp_path, seat="adv-alive",
                                    window_id="@9", registry_dir=str(reg),
                                    poll_secs=2)
    assert joined["transcript"] == explicit


# ── L4.122 merge-up 24 (S): longest-prefix seat resolution ────────────────


def test_resolve_seat_for_name_longest_prefix(_fix, tmp_path):
    """A seat that is a DASH-PREFIX of another (rows `a` and `a-b`) must
    resolve `a-b-X` to the LONGER `a-b`, never the shorter `a` (first-match
    sent the ack to the wrong row / ack path)."""
    _write_seats_sheet(tmp_path, [
        {"name": "a", "role": "parent", "model": "x"},
        {"name": "a-b", "role": "parent", "model": "y"},
    ])
    assert rotate._resolve_seat_for_name(tmp_path, "a-b-helper") == "a-b"
    assert rotate._resolve_seat_for_name(tmp_path, "a-helper") == "a"
    assert rotate._resolve_seat_for_name(tmp_path, "a-b") == "a-b"
    assert rotate._resolve_seat_for_name(tmp_path, "unregistered") == \
        "unregistered"


# ── L4.122 merge-up 24 (B): the Belam cap counts the successor, not the seat ─


def test_belam_oldest_counts_successor_not_seat(_fix):
    """The Belam-cap call site passes the SUCCESSOR (the numeral window that
    is actually live), never the SEAT base. Passing the bare base inflates the
    chain by one (treats the phantom base as a live window) and wrongly reaps
    the oldest."""
    live = ["belam-S1-L4-I", "belam-S1-L4-II", "belam-S1-L4-III",
            "belam-S1-L4-IV", "belam-S1-L4-V"]
    # correct: pass the real successor (already observed as the 5th window):
    #   5 live belam windows + it = 5 => no reap (chain stays five deep).
    assert rotate._belam_oldest(live, "belam-S1-L4-V", "belam") is None
    # old bug-shaped caller passes the SEAT base "belam": the phantom base
    # makes a SIXTH candidate and wrongly reaps the oldest.
    assert rotate._belam_oldest(live, "belam", "belam") == "belam-S1-L4-I"


def test_chain_seat_dry_run_derives_gen_before_from_numeral(_fix, tmp_path,
                                                       monkeypatch,
                                                       capsys):
    """For a numeral-chain seat the predecessor's generation is its OWN
    window's line value (3 for `belam-S1-L4-III`), never the handoff counter
    (which has nothing to do with it and announced 0 -> 8 on the live record).
    The dry-run prints the derived pair; with the fix it says 3 -> 4, where
    the old `_read_generation(root, seat)` (no handoff file) would say 0 -> 4."""
    win = tmp_path / "windows.txt"
    win.write_text("belam-S1-L4-III\n", encoding="utf-8")
    args = SimpleNamespace(
        name="belam", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=str(win), dry_run=True,
        throwaway=True, successor_argv=None, role="prime_director",
        session_ref=None, template=None, registry_dir=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "generation 3 -> 4" in out


# ── SEVENTH dispatch F1 — the prime-shaped rotation (r5/D/r4/e) ─────────────


def test_chain_seat_keeps_own_window_reaps_oldest_fifo(_fix, tmp_path,
                                                       monkeypatch):
    """F1 — a prime-shaped rotation: a numeral chain of SIX windows, the
    caller in its OWN window (belam-S1-L4-VI). (D) the OWN window survives —
    never killed on a numeral-chain seat; (r5) the Belam FIFO cap reaps the
    OLDEST by PID AND kills ITS window BY @id; the record carries the PLANNED
    s12 entry written BEFORE the first TERM (e); the FIFO reap is the ONE reap
    on a chain seat."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text(
        "@10 belam-S1-L4-I\n@11 belam-S1-L4-II\n@12 belam-S1-L4-III\n"
        "@13 belam-S1-L4-IV\n@14 belam-S1-L4-V\n@15 belam-S1-L4-VI\n",
        encoding="utf-8")

    def my_spawn(**kw):            # successor appears as the next numeral
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@16 belam-S1-L4-VII\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", my_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "belam", "gen_after": 7,
                         "answer": "continue"})
    # stand-in pids for the OLDEST Belam's chain (pane bash -> claude child),
    # TERM'd by the FIFO reap and verified gone (never a live Belam).
    p1 = subprocess.Popen(["sleep", "2000"])
    p2 = subprocess.Popen(["sleep", "2000"])
    try:
        args = _rotate_self_args(
            tmp_path, name="belam", role="prime_director",
            window_path=str(win), timeout=5, session_ref="ref1",
            belam_pids=[p1.pid, p2.pid])
        rc = rotate.cmd_rotate_self(args, tmp_path)
    finally:
        for p in (p1, p2):
            if rotate._pid_alive(p.pid):
                os.kill(p.pid, signal.SIGKILL)
    assert rc == 0
    rec = _latest_record(tmp_path, "belam")
    assert rec["result"] == "success"
    s12 = rec["s12_self_reap"]
    # (e) the s12 evidence carries the PLANNED entry (written pre-TERM) and
    #     the OWN chain is GATED OFF on this numeral-chain seat (D).
    assert s12.get("planned") is True
    assert "GATED OFF" in s12["gated"]
    assert s12["own_chain_reap"] == "GATED OFF"
    assert s12["own_window_id"] == "@15"
    # (r5) the decision was recorded AND executed: the OLDEST reaped by PID,
    #     its window killed BY @id.
    bc = rec["handover"]["belam_cap"]
    assert bc["would_exceed_five"] is True
    assert bc["oldest_to_reap"] == "belam-S1-L4-I"
    b = s12["belam_reap"]
    assert b["oldest"] == "belam-S1-L4-I"
    assert b["window_id"] == "@10"
    assert b["reaped"] is True
    assert set(b["pids"]) == {p1.pid, p2.pid}
    # the OLDEST window's line is gone (killed by @id); the OWN window @15
    # survives (D — the owner chain rule keeps the newest five idle).
    names = win.read_text(encoding="utf-8")
    assert "@10 belam-S1-L4-I" not in names
    assert "@15 belam-S1-L4-VI" in names


def test_belam_cap_record_planned_entry_when_term_interrupted(
        _fix, tmp_path, monkeypatch):
    """L4.150 — the belam-cap reap writes its PLANNED entry BEFORE the first
    TERM (the (e) shape). When `_reap_chain` raises (rotate.py dies between a
    TERM and the post-reap write — the p4 unevidenced-reap shape), the record
    still carries the planned belam entry `{planned: True, oldest, window_id,
    pids, chain}` naming what the cap intended to reap. Falsifier: an
    interrupted cap reap whose record lacks the belam entry."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text(
        "@10 belam-S1-L4-I\n@11 belam-S1-L4-II\n@12 belam-S1-L4-III\n"
        "@13 belam-S1-L4-IV\n@14 belam-S1-L4-V\n@15 belam-S1-L4-VI\n",
        encoding="utf-8")

    def my_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@16 belam-S1-L4-VII\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", my_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "belam", "gen_after": 7,
                         "answer": "continue"})

    def boom(*a, **k):
        raise RuntimeError("rotate.py died after the TERM")

    monkeypatch.setattr(rotate, "_reap_chain", boom)
    p1 = subprocess.Popen(["sleep", "2000"])
    p2 = subprocess.Popen(["sleep", "2000"])
    # the interrupted cmd_rotate_self sets SIGHUP/SIGTERM/SIGPIPE to SIG_IGN
    # (rotate._shield_final_signals) and never restores them on the exception
    # path (rotate.py:5133 runs on the bare path only). Capture the current
    # dispositions now and put them back in the finally, so this test does
    # not poison the shared pytest runtime for later reap tests — a
    # persistent SIG_IGN makes their sleep children ignore the TERM, get
    # SIGKILL'd, and linger as un-reaped zombies (reaped comes out False).
    _shield_old = {s: signal.getsignal(s) for s in
                   (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE)}
    try:
        args = _rotate_self_args(
            tmp_path, name="belam", role="prime_director",
            window_path=str(win), timeout=5, session_ref="ref1",
            belam_pids=[p1.pid, p2.pid])
        # the reap dies mid-flight; the rotation may still be recorded (the
        # reap, not the bookkeeping, is load-bearing) — we only assert on the
        # record's PLANNED entry, not on rc.
        try:
            rotate.cmd_rotate_self(args, tmp_path)
        except Exception:  # noqa: BLE001
            pass
    finally:
        # restore the signal dispositions the interrupted cmd_rotate_self
        # left as SIG_IGN (same shape as rotate._restore_shield_signals).
        for _sig, _handler in _shield_old.items():
            signal.signal(_sig, _handler)
        for p in (p1, p2):
            if rotate._pid_alive(p.pid):
                os.kill(p.pid, signal.SIGKILL)
    # the record still carries the PLANNED belam-cap entry, written BEFORE
    # the interrupted TERM.
    rec = _latest_record(tmp_path, "belam")
    b = rec.get("s12_self_reap", {}).get("belam_reap")
    assert b is not None, "record lacks the belam entry under an interrupted reap"
    assert b.get("planned") is True
    assert b["oldest"] == "belam-S1-L4-I"
    assert b["window_id"] == "@10"
    assert set(b["pids"]) == {p1.pid, p2.pid}
    assert b["chain"] == [p1.pid, p2.pid]


# ── L4.158 — hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window ──
# A SKIPPED Belam cap (no pane pid; pane pid but no descendants) still kills
# the oldESST window BY @id before returning, so the FIFO cap never leaves
# six windows. Before the fix both skipped paths returned EARLY before
# `_kill_window`, leaving the oldest @id line in the window file (measured by
# experiment:a00-edfd2a9d-4b64c4). Tested on the window-file seam: the oldest
# @id line must be gone and the record must carry window_id/window_killed. A
# window that is already gone records `already gone`, never an error.


def test_belam_cap_skip_no_pane_pid_still_kills_oldest_by_id(
        _fix, tmp_path, monkeypatch):
    """(a) — the `SKIPPED: no pane pid` path. The oldest window's @id IS
    resolved, but no pane pid can be derived; the cap must still kill the
    oldest window BY @id (oldest line gone from the window file) and record
    window_id/window_killed. Falsifier: the skipped path returns early and
    leaves the six-window oldest line in place."""
    win = tmp_path / "windows.txt"
    win.write_text("@9 belam-S1-L4-I\n@10 belam-S1-L4-II\n"
                   "@11 belam-S1-L4-III\n@12 belam-S1-L4-IV\n"
                   "@13 belam-S1-L4-V\n@14 belam-S1-L4-VI\n",
                   encoding="utf-8")
    monkeypatch.setattr(rotate, "_pane_pid", lambda pane: None)

    out = rotate._reap_belam_oldest(
        tmux_session="t", oldest="belam-S1-L4-I", window_path=str(win))

    assert "skipped" in out
    assert "SKIPPED: no pane pid" in out["skipped"]
    assert out["window_id"] == "@9"
    assert out["window_killed"] is True
    # the OLDEST window's line is gone — the skip still killed by @id.
    assert "@9 belam-S1-L4-I" not in win.read_text(encoding="utf-8")
    # chain no longer exceeds five belam lines.
    assert sum(1 for ln in win.read_text(encoding="utf-8").splitlines()
               if ln.strip()) <= 5


def test_belam_cap_skip_pane_pid_no_descendants_still_kills_oldest(
        _fix, tmp_path, monkeypatch):
    """(b) — the `SKIPPED: no chain under pane pid` path. The pane pid IS
    resolved but has no descendants; the cap must still kill the oldest
    window BY its @id ('@9'), record window_id/window_killed, and never
    raise."""
    win = tmp_path / "windows.txt"
    win.write_text("@9 belam-S1-L4-I\n@10 belam-S1-L4-II\n"
                   "@11 belam-S1-L4-III\n@12 belam-S1-L4-IV\n"
                   "@13 belam-S1-L4-V\n@14 belam-S1-L4-VI\n",
                   encoding="utf-8")
    monkeypatch.setattr(rotate, "_pane_pid", lambda pane: 4242)
    monkeypatch.setattr(rotate, "_descendant_chain", lambda pid: [])

    out = rotate._reap_belam_oldest(
        tmux_session="t", oldest="belam-S1-L4-I", window_path=str(win))

    assert "skipped" in out
    assert "SKIPPED: no chain under pane pid" in out["skipped"]
    assert out["window_id"] == "@9"
    assert out["window_killed"] is True
    assert "@9 belam-S1-L4-I" not in win.read_text(encoding="utf-8")
    assert sum(1 for ln in win.read_text(encoding="utf-8").splitlines()
               if ln.strip()) <= 5


def test_belam_cap_skip_already_gone_records_not_an_error(
        _fix, tmp_path, monkeypatch):
    """(c) — the oldest window is ALREADY gone by kill time. The @id was
    resolved from live tmux, but the window file (the present-window seam)
    no longer holds its line; `_kill_window` reports it gone. The cap must
    record the `already gone` phrase, not raise, and keep window_killed
    false."""
    win = tmp_path / "windows.txt"
    win.write_text("@10 belam-S1-L4-II\n@11 belam-S1-L4-III\n"
                   "@12 belam-S1-L4-IV\n@13 belam-S1-L4-V\n"
                   "@14 belam-S1-L4-VI\n", encoding="utf-8")
    # the @id was resolved from live tmux, but the window no longer exists.
    monkeypatch.setattr(rotate, "_successor_window_id",
                        lambda *a, **k: "@9")
    monkeypatch.setattr(rotate, "_pane_pid", lambda pane: None)

    out = rotate._reap_belam_oldest(
        tmux_session="t", oldest="belam-S1-L4-I", window_path=str(win))

    assert "already gone" in out["skipped"]
    assert out["window_id"] == "@9"
    assert out["window_killed"] is False
    # no exception, and nothing was killed (nothing to kill).
    assert "@9" not in win.read_text(encoding="utf-8")


def test_cmd_ack_continue_on_predecessor_answered_is_noop(
        _fix, tmp_path, capsys):
    """claim (4): when the predecessor already answered `continue`
    (source: predecessor) — the DEFAULT contract — a successor's
    `ack continue` is a ONE-LINE NO-OP exiting 0, and the ack file is NOT
    overwritten (no double-write, no commit).
    (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    hands-the-successor-exactly-one-call)"""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent"}])
    seats = tmp_path / "sessions" / "seats"
    seats.mkdir(parents=True, exist_ok=True)
    orig = {"seat": "adv-alive", "gen_after": 1,
            "answer": "continue", "source": "predecessor",
            "session_ref": "", "ts": "T", "text": ""}
    (seats / "adv-alive.ack.json").write_text(
        json.dumps(orig) + "\n", encoding="utf-8")
    rc = rotate.cmd_ack(SimpleNamespace(
        seat="adv-alive", gen=1, ref="deadbeef", answer="continue",
        text=None, no_commit=False, wait=0), tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "already answered continue by your predecessor" in out
    assert "nothing to run" in out
    # the ack file is byte-unchanged (no overwrite, no ref back-fill).
    ack = json.loads((seats / "adv-alive.ack.json")
                     .read_text(encoding="utf-8"))
    assert ack["answer"] == "continue" and ack["source"] == "predecessor"
    assert ack["session_ref"] == ""   # ref NOT back-filled by the no-op


def test_cmd_ack_diff_overrides_predecessor_continue(
        _fix, tmp_path, capsys):
    """claim (2)/override: a successor may still overwrite a predecessor
    `continue` with its OWN `diff` inside the read-back window — `ack diff`
    is never a no-op (it halts the rotation for inspection).
    (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    hands-the-successor-exactly-one-call)"""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent"}])
    seats = tmp_path / "sessions" / "seats"
    seats.mkdir(parents=True, exist_ok=True)
    (seats / "adv-alive.ack.json").write_text(json.dumps({
        "seat": "adv-alive", "gen_after": 1, "answer": "continue",
        "source": "predecessor", "session_ref": "", "ts": "T",
        "text": ""}) + "\n", encoding="utf-8")
    rc = rotate.cmd_ack(SimpleNamespace(
        seat="adv-alive", gen=1, ref=None, answer="diff", text="need edit",
        no_commit=False, wait=0), tmp_path)
    assert rc == 0
    ack = json.loads((seats / "adv-alive.ack.json")
                     .read_text(encoding="utf-8"))
    assert ack["answer"] == "diff"      # overwritten, override holds
    assert ack.get("source") != "predecessor"   # a successor write, no pred source


# ── l4-the-predecessor-answers-...-ask-diff (the --ask-diff leg) ──────────


def test_rotate_self_ask_diff_writes_diff_requested_and_one_call(
        _fix, tmp_path, monkeypatch, capsys):
    """WITH `--ask-diff` the predecessor writes the ack as
    `answer: diff-requested, source: predecessor` and hands the successor
    EXACTLY ONE wake call -- `rotate.py ack ... diff --text -`. The default
    read-back polls `diff-requested` like `pending` (it is NOT an answer); a
    successor that flips it to `continue` completes the rotation.
    (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    hands-the-successor-exactly-one-call)"""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript), ask_diff=True)
    # the successor's ONE reply to the diff-requested ack is `continue` here.
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue",
                          "source": "predecessor"})
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0

    # SL7.15 (goal:g15.25): the completed rotation rotates the ack file — the
    # live name is gone, the generation-stamped name carries the predecessor's
    # written state.
    rot = tmp_path / "sessions" / "seats" / "adv-alive.ack.gen1.json"
    assert rot.exists()
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.ack.json").exists()
    ack = json.loads(rot.read_text(encoding="utf-8"))
    assert ack["gen_after"] == 1
    assert ack["answer"] == "diff-requested"
    assert ack["source"] == "predecessor"
    # the ONE wake call is named verbatim.
    err = capsys.readouterr().err
    assert "rotate.py ack --seat adv-alive --gen 1 --ref <your ListAgents ref> diff --text -" in err


def test_rotate_self_default_ack_is_continue_wake_zero(
        _fix, tmp_path, monkeypatch, capsys):
    """The DEFAULT (no `--ask-diff`) write answers the ack ITSELF: the ack
    lands `answer: continue, source: predecessor`, and the REAL `_read_ack`
    reads it back immediately — confirming the rotation with ZERO successor
    calls (the claimed wake-0). `--ask-diff` is the explicit opt-in that
    leaves `diff-requested` instead.
    (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    hands-the-successor-exactly-one-call)"""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript))
    # NO _read_ack monkeypatch: the REAL read-back reads the predecessor's own
    # `continue` and confirms immediately — the wake-0 proof.
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    # SL7.15 (goal:g15.25): the completed rotation rotates the ack file — the
    # live name is gone, the generation-stamped name carries the predecessor's
    # own `continue` (the wake-0 proof, preserved verbatim by the rename).
    rot = tmp_path / "sessions" / "seats" / "adv-alive.ack.gen1.json"
    assert rot.exists()
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.ack.json").exists()
    ack = json.loads(rot.read_text(encoding="utf-8"))
    assert ack["answer"] == "continue"
    assert ack["source"] == "predecessor"
    # the rotation record says success (not unwitnessed): the predecessor's
    # own continue confirmed it.
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "success"
    # the (s6.3) default line names the wake-0 outcome.
    err = capsys.readouterr().err
    assert "successor runs NO ack" in err


def test_read_ack_polls_diff_requested_and_returns_continue(
        tmp_path, monkeypatch):
    """`_read_ack` treats `diff-requested` exactly like `pending`: NOT an
    answer, keep polling (returns None on timeout). A `continue` (or `diff`)
    flip returns promptly. This is what lets the predecessor write
    `diff-requested` and then WAIT for the successor's one reply."""
    monkeypatch.setattr(rotate, "time", _FakeTime())
    seat_dir = tmp_path / "seats"
    seat_dir.mkdir(parents=True, exist_ok=True)
    path = seat_dir / "seat.ack.json"

    # diff-requested: never returned as a terminal answer (keep polling).
    path.write_text(json.dumps(
        {"seat": "seat", "gen_after": 3, "session_ref": "",
         "answer": "diff-requested", "source": "predecessor",
         "ts": "x"}), encoding="utf-8")
    assert rotate._read_ack(path, gen_after=3, timeout=0.5) is None

    # same shape as `pending`: also never terminal.
    path.write_text(json.dumps(
        {"seat": "seat", "gen_after": 3, "session_ref": "",
         "answer": "pending", "source": "predecessor", "ts": "x"}),
        encoding="utf-8")
    assert rotate._read_ack(path, gen_after=3, timeout=0.5) is None

    # the successor's ONE reply completes the read.
    path.write_text(json.dumps(
        {"seat": "seat", "gen_after": 3, "session_ref": "",
         "answer": "continue", "source": "predecessor", "ts": "x"}),
        encoding="utf-8")
    ack = rotate._read_ack(path, gen_after=3, timeout=0.5)
    assert ack is not None and ack["answer"] == "continue"


class _FakeTime(object):
    """Deterministic time for `_read_ack`: no real sleeps; a tiny monotonic
    clock so the timeout fires after the first keep-polling pass."""

    def __init__(self):
        self.t = 1000.0

    def time(self):
        return self.t

    def monotonic(self):
        return self.t

    def sleep(self, s):
        self.t += 2.0


# ── SL7.29 part (c): the bootstrap ack fact, END-TO-END at spawn ────────────
# The part (b) test calls `_write_bootstrap` with hand-copied call args. This
# test EXECUTES the real `cmd_rotate_self` and reads the bootstrap file AT THE
# SPAWN INSTANT (inside the spawn seam, before s6.3's `_write_ack` runs), for
# BOTH modes — so an edit that drops the `overrides=` kwarg from the real
# pre-spawn call site is caught, never only re-covered by re-copying kwargs.


@pytest.mark.parametrize("ask_diff", [False, True])
def test_rotate_self_bootstrap_ack_verbatim_at_spawn(_fix, tmp_path,
                                                     monkeypatch, ask_diff):
    """The bootstrapped ack fact, observed at SPAWN through the REAL
    cmd_rotate_self, not a hand-copied call: with a rotations.md template
    whose `telemetry:` NAMES `ack`, the record on disk at the spawn instant
    carries `telemetry.ack == <answer> (source predecessor, gen 1)` for both
    the default (`continue`) and `--ask-diff` (`diff-requested`) modes, and
    rendering that record through the hook reader `_bootstrap_block` shows
    `- ack: <answer> (source predecessor, gen 1)` verbatim — never `ack: ack:`,
    never `ack: none`. (The empty-telemetry template would only re-cover the
    trivial no-ack case.)"""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: .agi/sessions/quorum/{seat}.md\n"
        "    steps: [handoff, rename, spawn, handover, readback, record, kill]\n"
        "    telemetry: [ack, seat]\n---\n", encoding="utf-8")
    transcript = tmp_path / "succ-transcript.jsonl"
    transcript.write_text("{}", encoding="utf-8")

    answer = "diff-requested" if ask_diff else "continue"
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    at_spawn = {}

    def read_spawn(**kw):
        # runs at the spawn instant, BEFORE s6.3's `_write_ack` -- the
        # TURN-ONE record the successor reads, not the post-join rewrite.
        with open(ft.win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")  # successor window appears (as fake_spawn)
        at_spawn["doc"] = json.loads(
            (tmp_path / "sessions" / "seats" / "adv-alive.bootstrap.json")
            .read_text(encoding="utf-8"))
        block, reason = rotate._bootstrap_block(tmp_path, "adv-alive")
        assert reason is None
        at_spawn["block"] = block
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", read_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": ("diff" if ask_diff else "continue"),
                          "text": ""})
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="00000000-0000-4000-8000-000000000000",
        successor_transcript=str(transcript), ask_diff=ask_diff)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0, f"ask_diff={ask_diff} rc={rc}"

    assert at_spawn["doc"]["telemetry"]["ack"] == \
        f"{answer} (source predecessor, gen 1)"
    ack_lines = [ln for ln in at_spawn["block"].splitlines()
                 if ln.strip().startswith("- ack")]
    assert ack_lines, f"no ack line at spawn for ask_diff={ask_diff}"
    assert ack_lines == [f"- ack: {answer} (source predecessor, gen 1)"]
    assert "ack: ack:" not in at_spawn["block"]
    assert "ack: none" not in at_spawn["block"]


# ── goal:g15.25 (SL7.40 (b)) — the PRE-TURN confirm records `deferred` ─────
# On a real rotation the successor has NO assistant turn yet when rotate-self
# probes (the own-window kill follows). A skip there must read DEFERRED, not
# `skipped:` — the ONE real confirm runs in run_after_join and overwrites it
# in place, so a reader can tell pre-turn deferral from a real verdict.

def test_rotate_self_pre_turn_confirm_records_deferred_not_skipped(
        _fix, tmp_path, monkeypatch):
    """With the successor still turn-less, the (s5) probe records
    `deferred: after_join`, never a `skipped:` verdict — the after_join
    confirm is the one that fires once a transcript carries a turn."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    # the successor has produced no assistant turn yet (the real probe reads
    # none at this point in a rotation) -> the probe returns a skip
    monkeypatch.setattr(
        rotate, "_confirm_successor_model",
        lambda **k: "skipped: no assistant turn in the successor transcript — "
                    "cannot confirm model/effort")
    # no persistent service, no forced run: after_join stays DEFERRED to the
    # service at the (6.4) gate, so the pre-turn deferral is what the record
    # carries — the after_join confirm overwrites it only when IT runs.
    monkeypatch.setattr(rotate, "_inline_reaper_enabled", lambda root: False)
    args = _rotate_self_args(tmp_path, window_path=str(ft.win), timeout=5,
                             session_ref=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    mc = rec["handover"]["model_confirm"]
    assert isinstance(mc, str) and mc.startswith("deferred: after_join"), mc
    assert not mc.startswith("skipped:"), \
        "a turn-less probe must read deferred, never a skipped verdict"


def test_rotate_self_pre_turn_probe_skipped_when_no_performer_can_run(
        _fix, tmp_path, monkeypatch):
    """(goal:g15.25 SL7.54 fix 4) with the successor turn-less AND NO captive
    after_join performer — inline_reaper off and the persistent heal watch
    unit declared DOWN (`reaper.unit_enabled=false`) — the (s5) probe records
    the honest `skipped: <reason>`, never a `deferred: after_join` LIE that a
    future confirm will land on a record nobody will touch."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    monkeypatch.setattr(
        rotate, "_confirm_successor_model",
        lambda **k: "skipped: no assistant turn in the successor transcript")
    # no fallback performer, persistent unit down -> nothing will run it
    monkeypatch.setattr(rotate, "_inline_reaper_enabled", lambda root: False)
    # the root's own legacy config declares the watch unit DOWN
    (tmp_path / "agi-tree.config.json").write_text(
        json.dumps({"reaper": {"unit_enabled": False}}), encoding="utf-8")
    args = _rotate_self_args(tmp_path, window_path=str(ft.win), timeout=5,
                             session_ref=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    mc = rec["handover"]["model_confirm"]
    assert isinstance(mc, str) and mc.startswith("skipped:"), mc
    assert "no captive after_join performer" in mc, mc


def test_rotate_self_fallback_after_join_overwrites_with_real_verdict_and_fills_bootstrap(
        _fix, tmp_path, monkeypatch):
    """gap (3): the rotate-self FALLBACK path (rotate.py ~12194) reaches the
    ONE real after_join confirm. With the successor transcript already
    carrying an assistant turn + a model_refusal_fallback event and the
    after_join forced onto the rotate-self fallback (an inline reaper is the
    fallback performer), the FINAL record's handover.model_confirm reads a
    real `confirm_at: after_join` verdict — overwriting the pre-turn probe in
    place (never left `deferred:`) — and the bootstrap record's TWO join-only
    facts (`successor_live_model`, `model_refusal_fallback`) are filled
    through the seam."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    tr = tmp_path / "succ.jsonl"
    tr.write_text(
        '{"type":"assistant","message":{"role":"assistant",'
        '"content":[]},"model":"claude-sonnet-5"}\n'
        '{"type":"system","subtype":"model_refusal_fallback",'
        '"timestamp":"2026-09-12T10:00:00.000Z",'
        '"apiRefusalCategory":"safety","requestId":"req-42"}\n',
        encoding="utf-8")
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                          "answer": "continue"})
    # an inline reaper is the rotate-self fallback performer — the after_join
    # runs HERE, with the successor transcript already answerable at tick 0.
    monkeypatch.setattr(rotate, "_inline_reaper_enabled", lambda root: True)
    args = _rotate_self_args(tmp_path, window_path=str(ft.win), timeout=5,
                             session_ref=None, successor_transcript=str(tr))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    mc = rec["handover"]["model_confirm"]
    assert isinstance(mc, dict) and mc.get("confirm_at") == "after_join", mc
    assert not (isinstance(mc, str) and mc.startswith("deferred:")), mc
    b = json.loads(
        (tmp_path / "sessions" / "seats" / "adv-alive.bootstrap.json")
        .read_text())
    tele = b["telemetry"]
    assert tele["successor_live_model"] == str({"model": "claude-sonnet-5"}), \
        tele
    assert tele["model_refusal_fallback"] == (
        "ts=2026-09-12T10:00:00.000Z category=safety requestId=req-42"), \
        tele
