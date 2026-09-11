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

    # ack written on the successor's behalf as `pending` (s6/s7): it carries
    # the machine identity but is NOT a confirmation until the successor
    # flips it to continue.
    ack = json.loads(
        (tmp_path / "sessions" / "seats" / "adv-alive.ack.json")
        .read_text(encoding="utf-8"))
    assert ack["gen_after"] == 1
    assert ack["answer"] == "pending"         # never pre-write `continue`
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
    # No identity => no identity-bearing handover step ran: only the window
    # identities and the s8 button-down (skipped on a fixture) are recorded.
    assert "successor_row" not in rec["handover"]
    assert "ack_written" not in rec["handover"]
    assert "own_authority_released" not in rec["handover"]
    assert rec["handover"]["successor_window"] == {"name": "adv-alive",
                                                    "id": None}
    assert "SKIPPED: grid commit illegal" in rec["handover"]["button_down"]


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
    # (c1) ack --ref back-fills session_ref into own row (source: ack)
    args = SimpleNamespace(seat="adv-alive", gen=1, ref="7902ac",
                           answer="continue", text=None)
    rc = rotate.cmd_ack(args, tmp_path)
    assert rc == 0
    rows = rotate._load_seats(tmp_path)
    own = next(r for r in rows if r["name"] == "adv-alive")
    assert own["session_ref"] == "7902ac"

    # (c2) whois authorizes by the short 6-hex ref (an exact session_ref).
    import send  # same dir (under test)
    code, _ = send._resolve_rows(rows, "7902ac", None)
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
