"""hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-
record-and-name-a-finding-only-over-the-floor.

The two sensei audit verbs (`wake-audit`, `rotate-out-audit`) now write their
result INTO the audited rotation record under ONE top-level key `audit` =
`{"wake"|"out": {calls, a, b, c, d, floor, excess, transcript,
window_start, window_end, audited_at, audited_by}}`, and print ONE line that
names the finding only when the window is over the floor:

    green  <post> <side> --record <stamp> <calls> (floor N)      excess == 0
    FINDING <post> <side> --record <stamp> excess <n> over floor <N>

FALSIFIERS held here, one per conjunct (fixtures synthetic; the ONE
live-corpus conjunct at the bottom reads the real `sessions/rotations` and
says so in its own docstring -- it never touches a live seat, transcript or
record):

  - a record byte differs outside `audit` after a run: compared BOTH parsed
    (JSON with `audit` popped) and RAW (the `audit` block textually removed
    from the rewritten bytes equals the original bytes);
  - a re-run grows the record / duplicates its side;
  - a wake with excess 0 prints anything but `green`;
  - `--no-record` writes nothing;
  - every printed identity line names the record STAMP, never a generation;
  - the verb never sends a dm (the dm to the Prime stays a Sensei act);
  - a STARTED record is REFUSED by name (`record still STARTED; audit after
    the outcome`), no write, non-zero exit;
  - a non-canonical record is REFUSED by name rather than reflowed whole;
  - an `audit` block survives the rotate.py outcome rewrite of its own file;
  - the floor in the record equals the config:rotations CELL it was read
    from;
  - the audited record is committed by exact path (temp repo, never this
    one) and a merge in progress / an untracked record refuses by name.

The write path's byte-preservation rests on the record being in the canonical
form `rotate.py` writes (`json.dumps(record, indent=2) + "\n"`,
rotate.py:4566,5304); every fixture here writes records that way.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import sensei  # noqa: E402
import rotate  # noqa: E402

SEAT = "sanctuary-director"
STAMP = "20260911T120000Z"

# A synthetic director first_turn mirroring the LIVE config:rotations shape,
# identical to test_sensei_wake_audit.py so the shared classifier is the same.
FT = [
    {"label": "rotation-record",
     "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} "
            "--record latest"},
    {"label": "facts",
     "cmd": "python3 extensions/agi/bin/write.py config:rotations "
            "'read body 37:46'"},
    {"label": "write-verbs",
     "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p"},
]


def _canonical(rec: dict) -> str:
    """The ONE byte form rotate.py writes a rotation record in."""
    return json.dumps(rec, indent=2) + "\n"


def _strip_audit_block(raw: str) -> str:
    """Remove the `audit` block from a rewritten record's RAW text, leaving
    the bytes exactly as they were before the write. `audit` is assigned last,
    so the block is the final `,\\n  "audit": {…}\\n  }` before the closing
    brace; the substitution must actually match (a no-op would hide a
    reformat)."""
    out = re.sub(r',\n  "audit": \{.*\n  \}\n\}\n$', "\n}\n", raw,
                 flags=re.S)
    assert out != raw, "the audit block was not found at the record's tail"
    return out


def _seats_md() -> str:
    return ("---\nid: config:seats\ntype: config\nseats:\n"
            f'  - {{"name": "{SEAT}", "role": "director", "tier": 1}}\n'
            "edited_by: test\n---\n<!-- BODY:BEGIN -->\n")


def _rotations_md() -> str:
    ft_lines = "\n".join(f"        - {json.dumps(e)}" for e in FT)
    return ("---\nid: config:rotations\ntype: config\n"
            "templates:\n  director:\n    startup:\n      first_turn:\n"
            f"{ft_lines}\n"
            "floor_out: 1\nfloor_wake: 0\n"
            "edited_by: test\n---\n"
            "<!-- BODY:BEGIN -->\n# config:rotations\n\n## facts\n"
            "- F1 (by hand): a worktree seat's record; one call proves it\n")


def _graph_skeleton(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    geo = graph / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "seats.md").write_text(_seats_md(), encoding="utf-8")
    (geo / "rotations.md").write_text(_rotations_md(), encoding="utf-8")
    (graph / "sessions" / "rotations").mkdir(parents=True, exist_ok=True)
    return graph


def _write_wake_project(tmp_path: Path, calls):
    """A tmp project whose single rotation record resolves the wake window.

    Returns `(graph, record_path, transcript_path)`. The record is written in
    rotate.py's canonical byte form so the write-back's byte-preservation can
    be measured against it."""
    graph = _graph_skeleton(tmp_path)
    tr = graph / "wake.jsonl"
    events = []
    for tool, cmd in calls:
        events.append(json.dumps(
            {"type": "assistant",
             "message": {"role": "assistant",
                         "content": [{"type": "tool_use", "name": tool,
                                      "input": {"command": cmd}}]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")
    rec = {"rotation": "rotate-self", "seat": SEAT,
           "recorded_at": "2026-09-11T12:00:00Z", "result": "success",
           "session_log": str(tr)}
    rec_path = graph / "sessions" / "rotations" / f"{SEAT}.{STAMP}.json"
    rec_path.write_text(_canonical(rec), encoding="utf-8")
    return graph, rec_path, tr


def _wake_args(**kw):
    base = dict(seat=SEAT, gen=None, transcript=None, record=None,
                redact=True, no_record=False)
    base.update(kw)
    return SimpleNamespace(**base)


# ── wake side ────────────────────────────────────────────────────────────

def test_wake_writes_audit_key_and_preserves_every_other_byte(tmp_path, capsys):
    graph, rec_path, tr = _write_wake_project(tmp_path, [
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20"),
        ("Bash", "ps -o pid,ppid -p 1234 2>/dev/null"),
        ("Bash", "python3 -m pytest extensions/agi/tests/test_sensei.py -q"),
    ])
    before = rec_path.read_text(encoding="utf-8")
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    after = rec_path.read_text(encoding="utf-8")
    capsys.readouterr()

    # (1) the audit key exists with every field the claim names
    rec = json.loads(after)
    audit = rec["audit"]["wake"]
    assert audit["calls"] == 3
    assert (audit["a"], audit["b"], audit["c"], audit["d"]) == (0, 2, 0, 1)
    assert audit["floor"] == 0
    assert audit["excess"] == 3
    assert audit["transcript"] == str(tr)
    # ONE shape on both sides: named keys, present-or-null
    assert audit["window_start"] == {"call_index": 1, "line": None,
                                    "ts": None}
    assert audit["window_end"] == {"call_index": 3, "line": None,
                                  "ts": None}
    assert audit["audited_by"] == sensei.SENSEI
    assert audit["audited_at"].endswith("Z")

    # (2) FALSIFIER: parsed comparison — JSON with `audit` popped is identical
    assert {k: v for k, v in rec.items() if k != "audit"} == \
        json.loads(before)

    # (3) FALSIFIER: RAW comparison — the original bytes are recoverable from
    # the rewritten bytes by removing the audit block textually.
    assert _strip_audit_block(after) == before


def test_wake_audit_rerun_replaces_its_side_and_never_grows(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20"),
    ])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    first = rec_path.read_text(encoding="utf-8")
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    second = rec_path.read_text(encoding="utf-8")
    capsys.readouterr()

    # idempotent: a re-run replaces `audit.wake`, byte-identically (only
    # `audited_at` may differ, so compare the record with timestamps dropped)
    a = json.loads(first)
    b = json.loads(second)
    assert set(b["audit"]) == {"wake"}
    a["audit"]["wake"].pop("audited_at")
    b["audit"]["wake"].pop("audited_at")
    assert a == b
    # FALSIFIER: no duplication / growth: `audit.wake` is an OBJECT, never a
    # list, and the record's byte length is EXACTLY the first run's (only
    # `audited_at`'s digits may differ, and that is the same width every run).
    assert isinstance(b["audit"]["wake"], dict)
    assert len(second) == len(first)


def test_wake_zero_calls_prints_green_and_excess_zero(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    out = capsys.readouterr().out
    line = f"green {SEAT} wake --record {STAMP} 0 (floor 0)"
    assert line in out
    assert "FINDING" not in out
    audit = json.loads(rec_path.read_text(encoding="utf-8"))["audit"]["wake"]
    assert audit["calls"] == 0 and audit["excess"] == 0 and audit["floor"] == 0


def test_wake_over_floor_prints_finding_naming_stamp_never_gen(
        tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20"),
    ])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    out = capsys.readouterr().out
    line = f"FINDING {SEAT} wake --record {STAMP} excess 1 over floor 0"
    assert line in out
    assert "green" not in out
    # FALSIFIER: the identity is the record STAMP, never a generation
    assert STAMP in line and "gen" not in line.split("FINDING")[1].split("\n")[0]


def test_wake_no_record_writes_nothing_but_still_prints(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    before = rec_path.read_text(encoding="utf-8")
    assert sensei.cmd_wake_audit(graph, _wake_args(no_record=True)) == 0
    out = capsys.readouterr().out
    assert f"green {SEAT} wake --record {STAMP} 0 (floor 0)" in out
    # FALSIFIER: --no-record is a dry read — not one byte changed
    assert rec_path.read_text(encoding="utf-8") == before


def test_wake_audit_never_sends_a_dm(tmp_path, capsys, monkeypatch):
    """The verb NAMES the finding; the dm to the Prime stays a Sensei act."""
    def _boom(*a, **kw):  # pragma: no cover - must never run
        raise AssertionError("the audit verb must not send anything")

    monkeypatch.setattr(sensei._send, "send_dm", _boom)
    monkeypatch.setattr(sensei._send, "send_room", _boom)
    graph, _rec, _tr = _write_wake_project(tmp_path, [
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20"),
    ])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    assert "FINDING" in capsys.readouterr().out


# ── rotate-out side ──────────────────────────────────────────────────────

GEN = 14
OUT_STAMP = "20260911T150000Z"
PREV_STAMP = "20260911T100000Z"
RECORDED_OUT = "2026-09-11T15:00:00Z"


def _write_out_project(tmp_path: Path, cmds=None):
    """Two canonical rotation records + the predecessor's transcript: PREV
    (gen 14 joined, names the transcript) and OUT (gen 14 left, bounds the
    window). Returns `(graph, out_record_path, transcript_path)`.

    `cmds` overrides the five default assistant calls, so a caller can build
    a window whose call count sits AT/below the floor for a VERB-level
    green."""
    graph = _graph_skeleton(tmp_path)
    tr = graph / "gen14.jsonl"
    events = [json.dumps(
        {"type": "user",
         "message": {"role": "user", "content": [
             {"type": "text", "text": "merge-up 14: go"}]}})]
    for cmd in (cmds if cmds is not None else (
        f"python3 extensions/agi/bin/rotate.py status --seat {SEAT} "
        f"--record latest",
        "tmux capture-pane -t sanctuary-director -p | tail -20",
        "python3 extensions/agi/bin/rotate.py -h | sed -n 1,30p",
        "python3 extensions/agi/bin/write.py .agi/nodes/handoff.md "
        "'replace body 5:9 -'",
        f"python3 extensions/agi/bin/rotate.py rotate-self --seat {SEAT} "
        f"--gen 15",
    )):
        events.append(json.dumps(
            {"type": "assistant",
             "message": {"role": "assistant",
                         "content": [{"type": "tool_use", "name": "Bash",
                                      "input": {"command": cmd}}]}}))
        events.append(json.dumps(
            {"type": "user",
             "message": {"role": "user", "content": [
                 {"type": "tool_result", "content": "ok",
                  "tool_use_id": "t"}]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")
    rot_dir = graph / "sessions" / "rotations"
    prev = {"seat": SEAT, "recorded_at": "2026-09-11T10:00:00Z",
            "observations": {"b_generation": {"before": 13, "after": 14}},
            "handover": {"join": {"transcript": str(tr)}}}
    (rot_dir / f"{SEAT}.{PREV_STAMP}.json").write_text(_canonical(prev),
                                                       encoding="utf-8")
    out = {"seat": SEAT, "recorded_at": RECORDED_OUT,
           "observations": {"b_generation": {"before": 14, "after": 15}},
           "s12_self_reap": {"chain": [999999]}}
    out_path = rot_dir / f"{SEAT}.{OUT_STAMP}.json"
    out_path.write_text(_canonical(out), encoding="utf-8")
    return graph, out_path, tr


def _out_args(**kw):
    base = dict(seat=SEAT, gen=None, transcript=None, record=None,
                registry_dir=None, redact=True, no_record=False)
    base.update(kw)
    return SimpleNamespace(**base)


def test_rotate_out_writes_audit_out_with_floor_one(tmp_path, capsys):
    graph, out_path, _tr = _write_out_project(tmp_path)
    before = out_path.read_text(encoding="utf-8")
    assert sensei.cmd_rotate_out_audit(graph, _out_args()) == 0
    after = out_path.read_text(encoding="utf-8")
    capsys.readouterr()

    audit = json.loads(after)["audit"]["out"]
    assert audit["calls"] == 5
    assert (audit["a"], audit["b"], audit["c"], audit["d"]) == (1, 1, 1, 2)
    assert audit["floor"] == 1
    assert audit["excess"] == 4
    assert audit["window_start"] == {"call_index": None, "line": 0,
                                    "ts": None}
    assert audit["window_end"] == {"call_index": None, "line": None,
                                  "ts": RECORDED_OUT}
    assert audit["audited_by"] == sensei.SENSEI

    # FALSIFIER: no byte outside `audit` changed (parsed AND raw)
    assert {k: v for k, v in json.loads(after).items() if k != "audit"} == \
        json.loads(before)
    assert _strip_audit_block(after) == before


def test_rotate_out_line_names_the_stamp_and_the_floor(tmp_path, capsys):
    graph, _out_path, _tr = _write_out_project(tmp_path)
    assert sensei.cmd_rotate_out_audit(graph, _out_args()) == 0
    out = capsys.readouterr().out
    line = (f"FINDING {SEAT} out --record {OUT_STAMP} excess 4 over floor 1")
    assert line in out
    assert "gen" not in line


def test_rotate_out_no_record_writes_nothing(tmp_path, capsys):
    graph, out_path, _tr = _write_out_project(tmp_path)
    before = out_path.read_text(encoding="utf-8")
    assert sensei.cmd_rotate_out_audit(graph, _out_args(no_record=True)) == 0
    assert "FINDING" in capsys.readouterr().out
    assert out_path.read_text(encoding="utf-8") == before


def test_explicit_transcript_writes_no_record(tmp_path, capsys):
    """The write is keyed on the record the audit ITSELF resolved: an
    explicit `--transcript` resolves no record, so nothing is written (and
    the existing `audit.out` survives untouched)."""
    graph, out_path, tr = _write_out_project(tmp_path)
    assert sensei.cmd_rotate_out_audit(graph, _out_args()) == 0
    capsys.readouterr()
    mid = out_path.read_text(encoding="utf-8")
    assert "out" in json.loads(mid)["audit"]
    assert sensei.cmd_wake_audit(
        graph, _wake_args(transcript=str(tr))) == 0
    out = capsys.readouterr().out
    assert "wake --record ?" in out
    assert out_path.read_text(encoding="utf-8") == mid


# ── conjunct 3: rotate.py status shows the audit key ─────────────────────

def test_rotate_status_prints_the_audit_key_from_the_record(tmp_path, capsys):
    """`rotate.py status --post S --record latest` renders the RAW record text
    (rotate.py:3080-3084), so the audit key falls out with NO rotate.py
    change. This is the owner's read."""
    graph, _rec_path, _tr = _write_wake_project(tmp_path, [])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    capsys.readouterr()
    rc = rotate.cmd_status(
        SimpleNamespace(record="latest", seat=SEAT, wait=0), graph)
    out = capsys.readouterr().out
    assert rc == 0
    assert '"audit"' in out
    assert '"wake"' in out and '"floor": 0' in out
    assert f"# latest rotation record: {SEAT}.{STAMP}.json" in out


# ── the floor constants ──────────────────────────────────────────────────

def test_every_live_rotation_record_is_in_the_canonical_byte_form():
    """The write-back's byte-preservation rests on the record being exactly
    `json.dumps(record, indent=2) + "\n"`, which is how rotate.py writes it.

    THIS test is the one conjunct in this file that reads the LIVE corpus
    (`<repo>/.agi/sessions/rotations`, reached through the checkout this test
    file sits in) rather than a `tmp_path` fixture: a live record whose bytes
    do not round-trip would be refused by the verb's canonical precondition,
    and the refusal is exactly the behaviour this file must see exercised on
    real bytes. Skipped when no live records are reachable."""
    live = Path(__file__).resolve().parents[3] / ".agi" / "sessions" / \
        "rotations"
    if not live.is_dir():
        pytest.skip(f"no live rotations dir at {live}")
    records = [p for p in sorted(live.glob("*.json"))
               if p.name != "sequence.json"]
    if not records:
        pytest.skip("no live rotation records")
    for p in records:
        raw = p.read_text(encoding="utf-8")
        try:
            obj = json.loads(raw)
        except ValueError:
            continue  # a record that does not parse is skipped, not fatal
        assert json.dumps(obj, indent=2) + "\n" == raw, (
            f"{p.name} is not in rotate.py's canonical byte form")


def test_floors_are_the_owners_numbers_and_have_one_reader(tmp_path):
    """The floor is the config:rotations CELL, not a constant in sensei.py.

    FALSIFIER: a floor value in the record differs from the config cell. The
    fixture carries the live cells (`floor_wake: 0`, `floor_out: 1`); the
    fallback dict exists only for a cell-less node and is not a second live
    copy."""
    fm, _facts = sensei._read_rotations(_graph_skeleton(tmp_path))
    assert sensei._audit_floors(fm) == {"wake": 0, "out": 1}
    # a node whose cells are absent falls back to the recorded owner numbers
    assert sensei._audit_floors("") == sensei.FALLBACK_AUDIT_FLOOR
    # a CHANGED cell moves the floor the payload records (ONE reader)
    changed = fm.replace("floor_out: 1", "floor_out: 7")
    assert sensei._audit_floors(changed)["out"] == 7
    p = sensei.audit_payload("out", 3, {}, "t", 1, 1, 7)
    assert p["floor"] == 7 and p["excess"] == 0
    assert sensei.audit_finding_line(SEAT, "wake", "S", 0, 0) == \
        f"green {SEAT} wake --record S 0 (floor 0)"
    assert sensei.audit_finding_line(SEAT, "out", "S", 3, 1) == \
        f"FINDING {SEAT} out --record S excess 2 over floor 1"
    # AUDIT_SIDES is deleted, not tombstoned
    assert not hasattr(sensei, "AUDIT_SIDES")


def test_main_accepts_no_record_beside_record(tmp_path, capsys, monkeypatch):
    """`--no-record` is a REAL CLI flag, not an abbreviation: the parser
    accepts it alongside `--record` and routes it to the dry read."""
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    before = rec_path.read_text(encoding="utf-8")
    monkeypatch.setattr(sensei.locations, "find_project_root",
                        lambda _p: graph)
    rc = sensei.main(["--root", str(graph), "wake-audit", "--seat", SEAT,
                      "--no-record", "--record", STAMP])
    assert rc == 0
    out = capsys.readouterr().out
    assert f"green {SEAT} wake --record {STAMP} 0 (floor 0)" in out
    assert rec_path.read_text(encoding="utf-8") == before


# ── (a) the STARTED refusal, the outcome-rewrite preserve ────────────────

def test_started_record_audit_refuses_by_name_and_writes_nothing(
        tmp_path, capsys):
    """A started record has no outcome to audit: the verb refuses BY NAME
    instead of sleeping for the outcome, and not one byte changes."""
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    rec["result"] = "started"
    rec_path.write_text(_canonical(rec), encoding="utf-8")
    before = rec_path.read_text(encoding="utf-8")

    assert sensei.cmd_wake_audit(graph, _wake_args()) == 3
    err = capsys.readouterr().err
    assert sensei.STARTED_REFUSAL in err
    assert "audit" not in json.loads(rec_path.read_text(encoding="utf-8"))
    assert rec_path.read_text(encoding="utf-8") == before


def test_started_record_rotate_out_audit_refuses_by_name_too(
        tmp_path, capsys):
    graph, out_path, _tr = _write_out_project(tmp_path)
    rec = json.loads(out_path.read_text(encoding="utf-8"))
    rec["result"] = "started"
    out_path.write_text(_canonical(rec), encoding="utf-8")
    before = out_path.read_text(encoding="utf-8")

    assert sensei.cmd_rotate_out_audit(graph, _out_args()) == 3
    assert sensei.STARTED_REFUSAL in capsys.readouterr().err
    assert out_path.read_text(encoding="utf-8") == before


def test_outcome_rewrite_preserves_the_audit_block(tmp_path):
    """FALSIFIER: an `audit` written on the file before the outcome rewrite
    survives it, byte for byte; and an `audit` THIS run supplies wins."""
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    rec["result"] = "started"
    rec["audit"] = {"wake": {"calls": 1, "floor": 0, "excess": 1}}
    rec_path.write_text(_canonical(rec), encoding="utf-8")
    audit_before = json.loads(rec_path.read_text(encoding="utf-8"))["audit"]

    rotate._write_rotation_record(
        graph, {"rotation": "rotate-self", "seat": SEAT,
                "recorded_at": "2026-09-11T12:05:00Z", "result": "success"},
        path=rec_path)
    after = json.loads(rec_path.read_text(encoding="utf-8"))
    assert after["result"] == "success"
    assert after["audit"] == audit_before

    # a fresh audit this run always wins over the on-disk one
    rotate._write_rotation_record(
        graph, {"rotation": "rotate-self", "seat": SEAT,
                "recorded_at": "2026-09-11T12:06:00Z", "result": "success",
                "audit": {"out": {"calls": 9}}},
        path=rec_path)
    assert json.loads(rec_path.read_text(encoding="utf-8"))["audit"] == \
        {"out": {"calls": 9}}


def test_started_rewrite_preserves_the_audit_block(tmp_path):
    """The progress writer (`_write_rotate_self_started`) rebuilds the dict
    from arguments too; it preserves the key the same way."""
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    rec["result"] = "started"
    rec["audit"] = {"wake": {"calls": 2, "floor": 0}}
    rec_path.write_text(_canonical(rec), encoding="utf-8")

    rotate._write_rotate_self_started(rec_path, seat=SEAT, steps=["a"])
    after = json.loads(rec_path.read_text(encoding="utf-8"))
    assert after["result"] == "started"
    assert after["audit"] == {"wake": {"calls": 2, "floor": 0}}


# ── (d) one window shape, (b) the record floor is the config cell ────────

def test_rotate_out_green_at_verb_level(tmp_path, capsys):
    """out-side green asserted by RUNNING THE VERB and reading the record,
    never by calling a helper directly."""
    graph, out_path, _tr = _write_out_project(
        tmp_path, cmds=("python3 extensions/agi/bin/write.py "
                        ".agi/nodes/handoff.md 'read body 1:2'",))
    assert sensei.cmd_rotate_out_audit(graph, _out_args()) == 0
    out = capsys.readouterr().out
    assert f"green {SEAT} out --record {OUT_STAMP} 1 (floor 1)" in out
    assert "FINDING" not in out
    audit = json.loads(out_path.read_text(encoding="utf-8"))["audit"]["out"]
    assert audit["calls"] == 1
    assert audit["excess"] == 0
    # FALSIFIER: the record's floor EQUALS the config:rotations cell
    fm, _facts = sensei._read_rotations(graph)
    assert audit["floor"] == sensei._audit_floors(fm)["out"] == 1


def test_wake_and_out_coexist_in_one_record(tmp_path):
    """Both sides live under ONE `audit` key and neither clobbers the other,
    including across a re-run of one side."""
    graph, rec_path, tr = _write_wake_project(tmp_path, [])
    wake = sensei.audit_payload(
        "wake", 0, {}, str(tr), sensei.audit_window_point(call_index=1),
        sensei.audit_window_point(call_index=0), 0)
    out = sensei.audit_payload(
        "out", 2, {}, str(tr), sensei.audit_window_point(line=3, ts="t0"),
        sensei.audit_window_point(ts=RECORDED_OUT), 1)
    sensei.write_audit_into_record(rec_path, "wake", wake)
    sensei.write_audit_into_record(rec_path, "out", out)
    audit = json.loads(rec_path.read_text(encoding="utf-8"))["audit"]
    assert set(audit) == {"wake", "out"}
    assert audit["wake"]["floor"] == 0 and audit["out"]["floor"] == 1
    assert audit["wake"]["window_end"] == {"call_index": 0, "line": None,
                                           "ts": None}
    assert audit["out"]["window_start"] == {"call_index": None, "line": 3,
                                            "ts": "t0"}

    sensei.write_audit_into_record(rec_path, "wake", wake)
    assert set(json.loads(rec_path.read_text(encoding="utf-8"))["audit"]) == \
        {"wake", "out"}


# ── (e) the canonical byte precondition ──────────────────────────────────

def test_non_canonical_record_refuses_by_name(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    rec_path.write_text(json.dumps(rec), encoding="utf-8")  # compact
    before = rec_path.read_text(encoding="utf-8")

    assert sensei.cmd_wake_audit(graph, _wake_args()) == 3
    assert "not in rotate.py's canonical byte form" in capsys.readouterr().err
    assert rec_path.read_text(encoding="utf-8") == before


# ── (c) the verb commits the record it wrote (temp repo only) ────────────

def _git_init(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "t@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "t"], check=True)


def _git(tmp_path: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(tmp_path), *args],
                          capture_output=True, text=True).stdout


def test_audited_record_is_committed_by_exact_path(tmp_path, capsys):
    """The verb commits ONLY the audited record, as its own one-pathspec
    commit, in the temp repo this test creates (never the real tree)."""
    graph, rec_path, _tr = _write_wake_project(tmp_path, [
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20")])
    _git_init(tmp_path)
    rel = str(rec_path.relative_to(tmp_path))
    _git(tmp_path, "add", "--", rel)
    _git(tmp_path, "commit", "-q", "-m", "seed", "--", rel)

    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    out = capsys.readouterr().out
    assert "audit_record_commit: committed" in out
    # committed: the path is clean, and the commit names side + stamp
    assert _git(tmp_path, "status", "--porcelain", "--", rel).strip() == ""
    msg = _git(tmp_path, "log", "-1", "--format=%s").strip()
    assert "audit record" in msg and SEAT in msg and STAMP in msg
    assert "FINDING" in msg and "wake" in msg
    # ONE commit only: the seed plus the audit commit
    assert len(_git(tmp_path, "rev-list", "--count", "HEAD").split()) == 1
    assert _git(tmp_path, "rev-list", "--count", "HEAD").strip() == "2"


def test_merge_in_progress_refuses_the_commit_by_name(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    _git_init(tmp_path)
    rel = str(rec_path.relative_to(tmp_path))
    _git(tmp_path, "add", "--", rel)
    _git(tmp_path, "commit", "-q", "-m", "seed", "--", rel)
    (tmp_path / ".git" / "MERGE_HEAD").write_text("0" * 40 + "\n",
                                                  encoding="utf-8")

    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    out = capsys.readouterr().out
    assert "merge in progress" in out
    # the audit is still written; only the commit refused
    assert "wake" in json.loads(rec_path.read_text(encoding="utf-8"))["audit"]
    assert _git(tmp_path, "status", "--porcelain", "--", rel).strip() != ""


def test_untracked_record_refuses_the_commit_by_name(tmp_path, capsys):
    graph, rec_path, _tr = _write_wake_project(tmp_path, [])
    _git_init(tmp_path)
    # the record exists but git has never seen it
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    out = capsys.readouterr().out
    assert "not tracked by git" in out
    assert _git(tmp_path, "rev-list", "--count", "HEAD").strip() in ("0", "")


def test_gitless_root_skips_the_commit_without_failing(tmp_path, capsys):
    graph, _rec_path, _tr = _write_wake_project(tmp_path, [])
    assert sensei.cmd_wake_audit(graph, _wake_args()) == 0
    assert "audit_record_commit: SKIPPED" in capsys.readouterr().out
