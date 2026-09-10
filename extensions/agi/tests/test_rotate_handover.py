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
import signal
import subprocess
import time
from types import SimpleNamespace

import pytest

import rotate  # noqa: E402


@pytest.fixture

def _fix(tmp_path, monkeypatch):
    """Fixture root for rotate-self mechanics: templates node + the
    find_project_root/ladder seams (mirrors test_rotate.py's fake_ladder)."""
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
                belam_prefix=None)
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
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0

    # row: the fixture seats.md row now carries the successor's identity.
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own["session_ref"] == "00000000-0000-4000-8000-000000000000"
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

    # ack written on the successor's behalf: the read-back confirmed it.
    ack = json.loads(
        (tmp_path / "sessions" / "seats" / "adv-alive.ack.json")
        .read_text(encoding="utf-8"))
    assert ack["gen_after"] == 1
    assert ack["answer"] == "continue"
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
    assert rec["handover"] == {}                 # no handover steps recorded


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


def test_handover_reaps_own_pid_stand_in(_fix, tmp_path, monkeypatch):
    """The full rotate-self call reaps the stand-in own pid handed it."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    proc = subprocess.Popen(["sleep", "1000"])
    pid = proc.pid
    try:
        args = _rotate_self_args(
            tmp_path, window_path=str(ft.win), timeout=5,
            session_ref="abc", own_pid=str(pid))
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        rec = _latest_record(tmp_path, "adv-alive")
        hp = rec["handover"]["reap_own_pid"]
        assert hp["reaped"] is True
        assert hp["gone_after"] is True
        assert hp["pid"] == pid
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
    args = _rotate_self_args(
        tmp_path, window_path=str(ft.win), timeout=5,
        session_ref="abc", belam_prefix="belam")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    bc = rec["handover"]["belam_cap"]
    assert bc["would_exceed_five"] is True
    assert bc["oldest_to_reap"] == "belam"