"""hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-by-post-and-record-
never-by-b-generation — the two sensei audit verbs resolve their window by
RECORD, never by a generation.

MEASURED pre-fix (2026-09-16, this checkout): `sensei.py rotate-out-audit
--post <seat>` refused for EVERY live post —

    ERR: cannot default --gen: the latest record has no b_generation.before

— because rotate.py writes `b_generation` only for a prime role or role None
(guard e85a1a797), so thought-master / sensei-director / master-sensei
rotate-self records carry no generation at any depth. `wake-audit` ran but
printed `--gen latest`, a generation where the record's own stamp belongs.

These tests pin the built fix on tmp_path COPIES of the two live record shapes
(never the live tree): (1) a CURRENT genless non-prime rotate-self record
shaped like thought-master.20260916T110753Z.json and (2) a record carrying
`observations.b_generation`.

FALSIFIERS named by the claim:
  - `rotate-out-audit --post <seat>` with no flag on the genless record still
    refuses;
  - a generation-carrying record resolves to a DIFFERENT window than the gen
    path did;
  - a printed line names a generation instead of the record stamp.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import sensei  # noqa: E402

SEAT = "thought-master"
R0_STAMP = "20260916T000000Z"
R1_STAMP = "20260916T063950Z"
OUT_STAMP = "20260916T110753Z"
OUT_REC_AT = "2026-09-16T11:08:55.989691Z"
SUCC_SID = "d98fb21a-e5aa-4072-94c8-048ab651fbef"
SID1 = "aaaaaaaa-1111-2222-3333-444444444444"

FT = [
    {"label": "rotation-record",
     "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} "
            "--record latest"},
    {"label": "facts",
     "cmd": "python3 extensions/agi/bin/write.py config:rotations "
            "'read body 37:46'"},
]


def _events(calls, ts_prefix="2026-09-16T10:00:0"):
    """A CC `.jsonl` body: one real user turn, then the given tool_use calls
    each followed by tool_result feedback, timestamped SECOND by second from
    `ts_prefix` so a record's `recorded_at` can bound the window."""
    out = [json.dumps({"type": "user", "timestamp": "2026-09-16T09:59:00Z",
                       "message": {"role": "user", "content": [
                           {"type": "text", "text": "merge-up: go"}]}})]
    for i, (tool, cmd) in enumerate(calls):
        ts = f"{ts_prefix}{i}Z"
        out.append(json.dumps({"type": "assistant", "timestamp": ts,
                               "message": {"role": "assistant", "content": [
                                   {"type": "tool_use", "name": tool,
                                    "input": {"command": cmd}}]}}))
        out.append(json.dumps({"type": "user", "timestamp": ts,
                               "message": {"role": "user", "content": [
                                   {"type": "tool_result",
                                    "content": "ok",
                                    "tool_use_id": "t"}]}}))
    return "\n".join(out) + "\n"


def _transcript(path: Path, calls):
    path.write_text(_events(calls), encoding="utf-8")
    return path


def _write_graph(tmp_path: Path, genless=True):
    """A tmp_path graph copying the two LIVE record shapes.

    `genless=True` (the CURRENT producer): three records shaped like
    thought-master's — a seating record naming PRED_A's transcript, a genless
    rotate-self record naming PRED_B's, and the genless OUT record naming the
    successor's. `genless=False`: the same graph with `observations.b_generation`
    on the two rotate-self records (the shape a PRIME role still writes).

    Returns `(graph, a, b, succ)`."""
    graph = tmp_path / ".agi"
    nodes = graph / "nodes"
    (nodes / ".geometry").mkdir(parents=True, exist_ok=True)
    (nodes / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        f'  - {{"name": "{SEAT}", "role": "director", "tier": 1, '
        f'"session_id": "{SUCC_SID}"}}\n'
        "edited_by: test\n---\n<!-- BODY:BEGIN -->\n", encoding="utf-8")
    ft_lines = "\n".join(f"        - {json.dumps(e)}" for e in FT)
    (nodes / ".geometry" / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\n"
        "templates:\n  director:\n    startup:\n      first_turn:\n"
        f"{ft_lines}\n"
        "edited_by: test\n---\n"
        "<!-- BODY:BEGIN -->\n# config:rotations\n\n## facts\n"
        "- F1 (gen: by hand)\n", encoding="utf-8")

    a = _transcript(graph / "pred_a.jsonl",
                    [("Bash", "python3 extensions/agi/bin/write.py "
                              ".agi/nodes/handoff.md 'replace body 5:9 -'")])
    b = _transcript(graph / "pred_b.jsonl",
                    [("Bash", "tmux capture-pane -t thought-master -p "
                              "| tail -20"),
                     ("Bash", "python3 extensions/agi/bin/rotate.py "
                              "rotate-self --seat thought-master")])
    succ = _transcript(graph / "succ.jsonl",
                       [("Bash", "python3 extensions/agi/bin/sender.py "
                                 "read thought-master")])

    rot = graph / "sessions" / "rotations"
    rot.mkdir(parents=True, exist_ok=True)

    # R0: the seating record — a first seating carries the incoming seat's own
    # transcript at the TOP level `transcript_path` (rotate._seating_record).
    r0 = {"rotation": "seating", "trigger": "first-seating", "seat": SEAT,
          "recorded_at": "2026-09-16T00:00:00.000000Z",
          "gen_before": 0, "gen_after": 1, "transcript_path": str(a)}
    (rot / f"{SEAT}.{R0_STAMP}.seating.json").write_text(
        json.dumps(r0), encoding="utf-8")

    # R1: a genless non-prime rotate-self record (the shape measured on
    # thought-master.20260916T063950Z.json / sensei-director).
    r1 = {"rotation": "rotate-self", "seat": SEAT, "result": "success",
          "recorded_at": "2026-09-16T06:39:50.379216Z",
          "handover": {"join": {"found": True, "weight": "@1",
                                "session_id": SID1,
                                "transcript": str(b)}},
          "s12_self_reap": {"chain": [{"pid": 111111}]}}
    # R2: the OUT record — genless, recorded_at bounds the rotate-out window,
    # its join names the SUCCESSOR's transcript (never the predecessor's).
    r2 = {"rotation": "rotate-self", "seat": SEAT, "result": "success",
          "recorded_at": OUT_REC_AT,
          "handover": {"join": {"found": True, "window_id": "@394",
                                "pid": 691554, "session_id": SUCC_SID,
                                "transcript": str(succ)}},
          "s12_self_reap": {"chain": [{"pid": 999999}]}}
    if not genless:
        r1["observations"] = {"b_generation": {"before": 13, "after": 14}}
        r2["observations"] = {"b_generation": {"before": 14, "after": 15}}
    (rot / f"{SEAT}.{R1_STAMP}.json").write_text(json.dumps(r1),
                                                 encoding="utf-8")
    (rot / f"{SEAT}.{OUT_STAMP}.json").write_text(json.dumps(r2),
                                                  encoding="utf-8")
    return graph, a, b, succ


# ── (1) the genless shape: BOTH verbs resolve with NO flags ────────────────

def test_genless_copy_carries_no_generation_at_any_depth(tmp_path):
    """The fixture really is the measured shape: the OUT record has no
    `b_generation`, no `gen_before`/`gen_after`, and no `observations` — the
    record the old default read. This is the fixture's own falsifier."""
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=True)
    rec = json.loads((graph / "sessions" / "rotations" /
                      f"{SEAT}.{OUT_STAMP}.json").read_text(encoding="utf-8"))
    assert "b_generation" not in rec
    assert "observations" not in rec
    assert "gen_before" not in rec and "gen_after" not in rec
    assert sensei._gen_bounds(rec) == (None, None)


def test_rotate_out_no_flag_resolves_the_genless_record(tmp_path):
    """FALSIFIER 1: `rotate-out-audit --post <seat>` with NO flag used to exit
    2 with `cannot default --gen`. It now defaults to the post's LATEST
    rotation record and resolves the predecessor's transcript from the record
    before it — naming the record stamp, never a generation."""
    graph, _a, b, _succ = _write_graph(tmp_path, genless=True)
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, None,
                                                          None)
    assert code == 0
    assert str(window["log_path"]) == str(b)
    assert window["record"] == OUT_STAMP
    assert window["gen"] is None          # no generation was needed or invented
    assert window["source"] == f"previous record {R1_STAMP} handover.join.transcript"
    assert "gen" not in window["source"]
    assert len(calls) == 2
    assert counts == {"a": 0, "b": 1, "c": 0, "d": 1, "s": 0}


def test_wake_audit_no_flag_resolves_the_genless_record(tmp_path):
    """The wake verb's default is the same record, resolved by the identity the
    seat row carries, and the printed source names the record stamp."""
    graph, _a, _b, succ = _write_graph(tmp_path, genless=True)
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
    assert code == 0
    assert calls[0]["source"] == f"record:{SEAT}.{OUT_STAMP}.json"
    assert OUT_STAMP in calls[0]["source"]
    assert len(calls) == 1


def test_genless_gen_alias_refuses_by_name_and_is_never_the_default(tmp_path):
    """`--gen` is a DEPRECATED alias: on a record with no generation it refuses
    BY NAME (naming `--record`) and never silently substitutes the record."""
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=True)
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, 7, None)
    assert code == 2
    assert calls == [] and counts == {} and window == {}
    code, calls, counts = sensei.wake_audit(graph, SEAT, 7, None)
    assert code == 2


def test_record_flag_selects_an_older_record_by_stamp(tmp_path):
    """`--record <stamp>` is the explicit selector: the older rotate-self
    record's predecessor is the SEATING record's own transcript."""
    graph, a, _b, _succ = _write_graph(tmp_path, genless=True)
    code, _calls, _counts, window = sensei.rotate_out_audit(
        graph, SEAT, None, None, record=R1_STAMP)
    assert code == 0
    assert str(window["log_path"]) == str(a)
    assert window["record"] == R1_STAMP
    assert window["source"] == f"previous record {R0_STAMP} transcript_path"
    # a stamp that resolves to no record refuses by NAME, never falls back
    code, calls, counts, window = sensei.rotate_out_audit(
        graph, SEAT, None, None, record="nope")
    assert code == 2 and calls == [] and counts == {}


def test_record_latest_is_the_latest_record(tmp_path):
    graph, _a, b, _succ = _write_graph(tmp_path, genless=True)
    code, _calls, _counts, window = sensei.rotate_out_audit(
        graph, SEAT, None, None, record="latest")
    assert code == 0
    assert window["record"] == OUT_STAMP
    assert str(window["log_path"]) == str(b)


# ── (2) the generation-carrying shape: record and gen agree ───────────────

def test_generation_record_resolves_the_same_window_as_the_gen_path(tmp_path):
    """FALSIFIER 2: when a record DOES carry `observations.b_generation`, the
    deprecated `--gen N` must resolve to exactly the window the record does —
    same transcript, same recorded_at, same record stamp. A difference is the
    regression the claim names."""
    graph, _a, b, _succ = _write_graph(tmp_path, genless=False)
    c_noflag, _, _, w_noflag = sensei.rotate_out_audit(graph, SEAT, None, None)
    c_gen, _, _, w_gen = sensei.rotate_out_audit(graph, SEAT, 14, None)
    assert c_noflag == 0 and c_gen == 0
    assert w_noflag["record"] == OUT_STAMP == w_gen["record"]
    assert w_noflag["log_path"] == w_gen["log_path"] == str(b)
    assert w_noflag["recorded_at"] == w_gen["recorded_at"] == OUT_REC_AT
    assert w_noflag["source"] == w_gen["source"]
    assert "gen" not in w_gen["source"]
    # and the deprecated flag reports itself as the alias it is, by stamp
    assert w_gen["basis"].endswith(f"(deprecated --gen 14)")


def test_generation_record_from_pytest_is_not_the_default(tmp_path):
    """No flag on the generation-carrying shape selects the LATEST record, not
    `--gen`: the basis names a record, never a generation."""
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=False)
    code, _calls, _counts, window = sensei.rotate_out_audit(graph, SEAT, None,
                                                            None)
    assert code == 0
    assert window["basis"] == f"record {OUT_STAMP}"
    assert "--gen" not in window["basis"]


# ── the printed lines name the record stamp, never a generation ───────────

def test_cli_prints_the_record_stamp_not_a_generation(tmp_path, capsys):
    from types import SimpleNamespace
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=True)
    args = SimpleNamespace(seat=SEAT, gen=None, transcript=None, record=None,
                           registry_dir=None, redact=True)
    assert sensei.cmd_rotate_out_audit(graph, args) == 0
    out = capsys.readouterr().out
    assert f"--record {OUT_STAMP} (role director)" in out
    assert "--gen" not in out
    # the wake header names the record too
    args_w = SimpleNamespace(seat=SEAT, gen=None, transcript=None,
                             record=None, redact=True)
    assert sensei.cmd_wake_audit(graph, args_w) == 0
    out_w = capsys.readouterr().out
    assert f"--record {OUT_STAMP} (role director)" in out_w
    assert "--gen" not in out_w


def test_cli_gen_alias_still_prints_the_record_as_the_identity(tmp_path,
                                                              capsys):
    """A deprecated `--gen N` call prints the RECORD stamp as the identity and
    says the flag is an alias — the generation number is a flag, never the
    window's name."""
    from types import SimpleNamespace
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=False)
    args = SimpleNamespace(seat=SEAT, gen=14, transcript=None, record=None,
                           registry_dir=None, redact=True)
    assert sensei.cmd_rotate_out_audit(graph, args) == 0
    out = capsys.readouterr().out
    assert f"--record {OUT_STAMP} (role director)" in out
    assert "deprecated alias: resolved to record " + OUT_STAMP in out
    assert "--gen_after==" not in out


def test_seat_with_only_another_sessions_record_still_refuses(tmp_path):
    """The record-keyed default must not weaken the identity gate: a row naming
    session A with only session B's record on disk refuses BY NAME (P1), never
    falls back to the latest record."""
    graph, _a, _b, _succ = _write_graph(tmp_path, genless=True)
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        f'  - {{"name": "{SEAT}", "role": "director", "tier": 1, '
        f'"session_id": "bbbbbbbb-1111-2222-3333-444444444444"}}\n'
        "edited_by: test\n---\n<!-- BODY:BEGIN -->\n", encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
    assert code == 2 and calls == [] and counts == {}
