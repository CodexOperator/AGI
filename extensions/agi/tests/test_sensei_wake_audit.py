"""Tests for sensei.py wake-audit (hypothesis:sensei-wake-audit-subcommand).

The classifier (classify_call) is pure and tested directly against SYNTHETIC
first_turn entries; wake_audit is tested end-to-end against a SYNTHETIC CC
JSONL fixture written into a tmp graph root with a synthetic config:rotations
node and config:seats node. No real seat, transcript, or write is touched.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import sensei  # noqa: E402
import rotate  # noqa: E402

# A synthetic director first_turn mirroring the LIVE config:rotations shape
# (the director role's startup.first_turn: rotation-record, facts, git-state,
# write-verbs, ...). The classifier must read this fresh, never hardcode it.
FT = [
    {"label": "rotation-record",
     "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest"},
    {"label": "facts",
     "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:46'"},
    {"label": "git-state",
     "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3"},
    {"label": "write-verbs",
     "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p"},
]
SEAT = "sanctuary-director"

# A synthetic director after_join mirroring the LIVE template's
# `startup.after_join` (the steps the SERVICE performs after the join, which a
# hand wake must not redo as "real work"). ack/pin(meter) are also hardcoded
# in classify_call; `register` exists ONLY to prove the live-list path is real.
AJ = [
    {"label": "ack",
     "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue"},
    {"label": "register",
     "cmd": "python3 extensions/agi/bin/rotate.py register --seat {seat}"},
]


def _aj_entries():
    return [dict(e) for e in AJ]


def _ft_entries():
    # we don't substitute {seat} at construction; classify_call binds it.
    return [dict(e) for e in FT]


class TestClassifyCall:
    def test_rerun_of_first_turn_cmd_is_category_a_with_label(self):
        cmd = ("python3 extensions/agi/bin/rotate.py status --seat "
               "sanctuary-director --record latest 2>&1 | tail -20")
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "a"
        assert label == "rotation-record"

    def test_rerun_of_facts_read_is_category_a(self):
        cmd = "python3 extensions/agi/bin/write.py config:rotations 'read body 37:46'"
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "a"
        assert label == "facts"

    def test_git_status_matches_first_turn_git_state(self):
        cmd = "git -C /home/ubuntu/work/agi status -sb | head -3"
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "a"
        assert label == "git-state"

    def test_dash_h_is_protocol_learning_even_when_it_matches_a_label(self):
        # write.py -h is the write-verbs first_turn, but learning the tool is
        # category c (protocol), not a re-derive.
        cmd = "python3 extensions/agi/bin/write.py -h | sed -n 1,40p"
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "c"
        assert label == "write-verbs"

    def test_source_grep_is_protocol_learning(self):
        cmd = ("grep -n '^def verb_note\\\\|^class Edit\\\\|^def verb_' "
               "extensions/agi/bin/write.py")
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "c"
        assert label is None

    def test_hand_read_of_a_record_a_startup_entry_covers_is_category_b(self):
        cmd = ("ps -o pid,ppid,etimes,stat,comm -p 2151405,2151413 "
               "2>/dev/null; echo")
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"

    def test_ls_sessions_rotations_by_hand_is_category_b(self):
        cmd = "ls -la /home/ubuntu/work/agi/.agi/sessions/rotations | tail -5"
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"

    def test_real_work_is_category_d(self):
        cmd = "python3 -m pytest extensions/agi/tests/test_sensei.py -q"
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "d"
        # send a real dm → real work
        cat2, _ = sensei.classify_call(
            "python3 extensions/agi/bin/send.py send belam 'merge-up 20: go'",
            "Bash", SEAT, _ft_entries())
        assert cat2 == "d"

    def test_after_join_ack_done_by_hand_is_service_owed(self):
        # rotate.py ack is an after_join step the SERVICE performs; the agent
        # doing it by hand is category s (service-owed) with the step's label,
        # never b and never d (amended g15 build order, proposal (e) second
        # half).
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py ack --seat "
            "sanctuary-director --gen 14 --ref 7aeee9 continue", "Bash", SEAT,
            _ft_entries())
        assert cat == "s"
        assert label == "ack"

    def test_grepping_the_seat_registry_by_hand_is_category_b_not_c(self):
        cmd = ("grep -o '\"name\": \"sanctuary-director\"[^}]*' "
               ".agi/nodes/.geometry/seats.md")
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"

    def test_absent_first_turn_list_means_everything_is_hand_read_or_work(self):
        # no template for the role → caller refuses BEFORE classifying, but the
        # pure function must not silently use another role's template; [] means
        # no labels match, so reruns fall through to b/d, never bogus category a.
        cmd = "python3 extensions/agi/bin/rotate.py status --seat X --record latest"
        cat, label = sensei.classify_call(cmd, "Bash", "X", [])
        assert cat in ("b", "d")  # not "a" without a template
        assert label is None


def _write_root(tmp_path: Path, tools_and_cmds):
    """Write a synthetic graph root with config:seats + config:rotations +
    a synthetic CC transcript of the given `(tool, cmd)` calls."""
    graph = tmp_path / ".agi"
    nodes = graph / "nodes"
    (nodes / ".geometry").mkdir(parents=True, exist_ok=True)
    (nodes / "config").mkdir(parents=True, exist_ok=True)
    # config:seats — the seat + its role (mirrors the real frontmatter shape)
    seats = (nodes / ".geometry" / "seats.md")
    seats.write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        f'  - {{"name": "{SEAT}", "role": "director", "tier": 1}}\n'
        "edited_by: test\n---\n<!-- BODY:BEGIN -->\n", encoding="utf-8")
    rot = (nodes / ".geometry" / "rotations.md")
    ft_lines = "\n".join(f'        - {json.dumps(e)}' for e in FT)
    aj_lines = "\n".join(f'        - {json.dumps(e)}' for e in AJ)
    rot.write_text(
        "---\nid: config:rotations\ntype: config\n"
        "templates:\n  director:\n    startup:\n      first_turn:\n"
        f"{ft_lines}\n      after_join:\n{aj_lines}\n"
        "  prime_director:\n    startup:\n      first_turn:\n"
        '        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify"}\n'
        "edited_by: test\n---\n"
        "<!-- BODY:BEGIN -->\n# config:rotations\n\n"
        "## facts\n"
        "- F1 (by hand): a worktree seat's record; one call proves it -- "
        "`python3 extensions/agi/bin/rotate.py status --seat <seat> --record latest`\n"
        "- F2 (by hand): the seat registry; `whois` or "
        "`grep \"name\": \"<seat>\" .agi/nodes/.geometry/seats.md`\n"
        "- F3 (note verb): `write.py <node-id> \"note <text>\"`\n",
        encoding="utf-8")
    # people who pass --transcript explicitly skip the pin/slug resolution,
    # so the transcript can live anywhere; put it next to the graph.
    tr = graph / "wake.jsonl"
    events = []
    for tool, cmd in tools_and_cmds:
        block = {"type": "tool_use", "name": tool,
                 "input": {"command": cmd}}
        events.append(json.dumps(
            {"type": "assistant",
             "message": {"role": "assistant", "content": [block]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")
    return graph, tr


def _write_rotation_record(graph: Path, seed: str, *, session_log: Path | None = None,
                           gen: int | None = None, ts: str = "20260911T120000Z",
                           join_transcript: Path | None = None):
    """A synthetic durable rotation record for a seat, matching the shape
    `rotate.py` writes under `sessions/rotations/<seat>.<ts>.json`."""
    sessions = graph / "sessions" / "rotations"
    sessions.mkdir(parents=True, exist_ok=True)
    rec = {
        "rotation": "rotate-self",
        "seat": SEAT,
        "recorded_at": ts + "Z",
        "result": "success",
        "observations": {},
    }
    if gen is not None:
        rec["observations"]["b_generation"] = {"before": gen - 1,
                                                "after": gen}
    if session_log is not None:
        rec["session_log"] = str(session_log)
    if join_transcript is not None:
        # the name every LIVE rotation record carries (handover.join.transcript)
        ho = rec.setdefault("handover", {})
        ho["join"] = {"transcript": str(join_transcript)}
    path = sessions / f"{SEAT}.{seed}.json"
    path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return path


def _events(blocks):
    """Serialize tool_use blocks into a CC JSONL transcript string."""
    out = []
    for block in blocks:
        out.append(json.dumps(
            {"type": "assistant",
             "message": {"role": "assistant", "content": [block]}}))
    return "\n".join(out) + "\n"


def test_wake_audit_end_to_end_cuts_window_and_counts_on_synthetic(tmp_path):
    # a first_turn rerun (a), a by-hand read (b), a -h (c), then real work (d)
    tools_and_cmds = [
        ("Bash", "python3 extensions/agi/bin/rotate.py status --seat "
                 "sanctuary-director --record latest"),
        ("Bash", "ps -o pid,ppid -p 1234 2>/dev/null"),
        ("Bash", "python3 extensions/agi/bin/write.py -h | sed -n 1,40p"),
        ("Bash", "python3 -m pytest extensions/agi/tests/test_sensei.py -q"),
        ("Bash", "sed -i 's/A/B/' extensions/agi/bin/sensei.py"),  # past window
    ]
    graph, tr = _write_root(tmp_path, tools_and_cmds)
    code, calls, counts = sensei.wake_audit(graph, SEAT, 14, tr)
    assert code == 0
    # window = a,b,c then cut at the first d (the pytest run); the trailing
    # sed call is beyond the window and must NOT be listed.
    assert len(calls) == 4
    cats = [c["cat"] for c in calls]
    assert cats == ["a", "b", "c", "d"]
    assert counts == {"a": 1, "b": 1, "c": 1, "d": 1, "s": 0}
    assert calls[0]["label"] == "rotation-record"
    assert calls[2]["label"] == "write-verbs"  # -h matched the label but is c
    assert calls[3]["tool"] == "Bash"


def test_wake_audit_no_transcript_is_a_named_error(tmp_path, monkeypatch):
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    monkeypatch.setattr(rotate, "resolve_transcript",
                        lambda *a, **kw: (None, "no-transcript"))
    code, calls, counts = sensei.wake_audit(graph, SEAT, 14, None)
    assert code == 2
    assert calls == [] and counts == {}


def test_wake_audit_unknown_seat_refuses(tmp_path):
    graph, tr = _write_root(tmp_path, [("Bash", "true")])
    code, _, _ = sensei.wake_audit(graph, "no-such-seat", 1, tr)
    assert code == 2


def test_wake_audit_role_without_template_refuses_named(tmp_path):
    graph, tr = _write_root(tmp_path, [("Bash", "true")])
    # add a seat whose role has NO template in the fixture rotations node;
    # wake-audit must name-refuse rather than fall back to the director's.
    seats = graph / "nodes" / ".geometry" / "seats.md"
    text = seats.read_text(encoding="utf-8")
    text = text.replace("edited_by: test\n---",
                        f'  - {{"name": "policy-master", "role": "farmer", "tier": 1}}\n'
                        "edited_by: test\n---")
    seats.write_text(text, encoding="utf-8")
    code, _, _ = sensei.wake_audit(graph, "policy-master", 3, tr)
    assert code == 2


# ── g15 claim tests (hypothesis:l4-wake-audit-reads-facts-and-defaults-to-
# ── the-latest-record): facts re-derive detection, non-Bash calls, sed -i,
# ── and the optional --gen defaulting to the latest rotation record ─────────

def _fixture_facts():
    # mirror the fixture's `## facts` body (F1/F2/F3 with cited command shapes)
    return sensei._parse_facts(
        "- F1 (by hand): `python3 extensions/agi/bin/rotate.py status "
        "--seat <seat> --record latest`\n"
        "- F2 (by hand): `whois` or "
        "`grep \"name\": \"<seat>\" .agi/nodes/.geometry/seats.md`\n"
        "- F3 (note verb): `write.py <node-id> \"note <text>\"`\n")


class TestFactRederive:
    def test_f1_cited_shape_is_category_a_with_fact_label(self):
        # facts-only (no first_turn entries) so the FACT wins, proving the
        # category-(a) rule is no longer first_turn-only.
        cmd = ("python3 extensions/agi/bin/rotate.py status --seat "
               "sanctuary-director --record latest 2>&1 | tail -5")
        cat, label = sensei.classify_call(cmd, "Bash", SEAT, [],
                                          _fixture_facts())
        assert cat == "a"
        assert label == "F1"

    def test_f2_whois_is_category_a_with_fact_label(self):
        cat, label = sensei.classify_call(
            "whois 8.8.8.8", "Bash", SEAT, [], _fixture_facts())
        assert cat == "a"
        assert label == "F2"

    def test_f2_grep_of_seats_md_is_category_a_with_fact_label(self):
        cat, label = sensei.classify_call(
            'grep \"name\": \"sanctuary-director\" '
            '.agi/nodes/.geometry/seats.md',
            "Bash", SEAT, [], _fixture_facts())
        assert cat == "a"
        assert label == "F2"

    def test_first_turn_label_beats_fact_label_when_both_match(self):
        # rotate.py status is ALSO the rotation-record first_turn entry; the
        # configured entry is the more specific label and must win.
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py status --seat "
            "sanctuary-director --record latest", "Bash", SEAT, _ft_entries(),
            _fixture_facts())
        assert cat == "a"
        assert label == "rotation-record"

    def test_sed_inplace_edit_is_real_work_not_learning(self):
        cat, _ = sensei.classify_call(
            "sed -i 's/a/b/' extensions/agi/bin/sensei.py",
            "Bash", SEAT, _ft_entries(), _fixture_facts())
        assert cat == "d"

    def test_sed_inplace_edit_with_eq_flag_is_work_not_learning(self):
        cat, _ = sensei.classify_call(
            "sed --in-place 's/x/y/' extensions/agi/bin/rotate.py",
            "Bash", SEAT, _ft_entries(), _fixture_facts())
        assert cat == "d"

    def test_plain_source_sed_grep_still_protocol_learning(self):
        # only the IN-PLACE edit is real work; a read-only grep stays (c)
        cat, _ = sensei.classify_call(
            "sed -n 1,40p extensions/agi/bin/write.py",
            "Bash", SEAT, _ft_entries(), _fixture_facts())
        assert cat == "c"


class TestNonBashCalls:
    def test_read_of_seats_md_is_category_b(self, tmp_path):
        block = {"type": "tool_use", "name": "Read",
                 "input": {"path": ".agi/nodes/.geometry/seats.md"}}
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        tr = graph / "nonbash.jsonl"
        tr.write_text(_events([block]), encoding="utf-8")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert calls[0]["cat"] == "b"
        assert counts == {"a": 0, "b": 1, "c": 0, "d": 0, "s": 0}

    def test_read_of_uncovered_path_is_category_d(self, tmp_path):
        block = {"type": "tool_use", "name": "Read",
                 "input": {"path": "docs/architecture.md"}}
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        tr = graph / "nonbash.jsonl"
        tr.write_text(_events([block]), encoding="utf-8")
        code, calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert calls[0]["cat"] == "d"

    def test_edit_tool_of_a_covered_path_is_still_real_work(self, tmp_path):
        # Edit/Write are WRITES: even onto a first_turn-covered path they are
        # real work (d), never a by-hand read (b).
        block = {"type": "tool_use", "name": "Edit",
                 "input": {"path": ".agi/nodes/.geometry/seats.md",
                            "old_string": "x", "new_string": "y"}}
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        tr = graph / "edit.jsonl"
        tr.write_text(_events([block]), encoding="utf-8")
        code, calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert calls[0]["cat"] == "d"

    def test_grep_nonbash_tool_by_path_is_category_b(self, tmp_path):
        block = {"type": "tool_use", "name": "Grep",
                 "input": {"pattern": "sanctuary-director",
                            "path": [".agi/nodes/.geometry/seats.md"]}}
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        tr = graph / "grep.jsonl"
        tr.write_text(_events([block]), encoding="utf-8")
        code, calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert calls[0]["cat"] == "b"


class TestOptionalGenDefaultsToLatestRecord:
    def test_no_gen_audits_latest_record_and_its_transcript(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        # an OLD transcript "123" / an OLD record ..., and the LATEST record
        # naming the NEW transcript (a whois → F2 fact re-derive).
        old = graph / "old.jsonl"
        old.write_text(_events([{"type": "tool_use", "name": "Bash",
                                 "input": {"command": "true"}}]),
                       encoding="utf-8")
        new = graph / "new.jsonl"
        new.write_text(_events([{"type": "tool_use", "name": "Bash",
                                 "input": {"command": "whois 8.8.8.8"}}]),
                       encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", session_log=old,
                               gen=13)
        _write_rotation_record(graph, "20260911T110000Z", session_log=new,
                               gen=14)
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert counts == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert calls[0]["cat"] == "a"
        assert calls[0]["label"] == "F2"
        # source pins WHICH record the transcript came from (never a slug)
        assert calls[0]["source"].startswith("record:")
        assert calls[0]["source"].endswith("20260911T110000Z.json")

    def test_latest_record_wins_over_newest_transcript_monkeypatched_off(self,
                                                                        tmp_path,
                                                                        monkeypatch):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        rec_tr = graph / "rec_tr.jsonl"
        rec_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                    "input": {"command": "whois 1.1.1.1"}}]),
                          encoding="utf-8")
        _write_rotation_record(graph, "20260911T090000Z", session_log=rec_tr,
                               gen=12)
        # rotate.resolve_transcript must NEVER be consulted (its env / pin /
        # newest-.jsonl fallbacks are unreachable for the wake audit).
        def boom(*a, **kw):
            raise AssertionError("resolve_transcript must not be called")
        monkeypatch.setattr(rotate, "resolve_transcript", boom)
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert counts == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert calls[0]["label"] == "F2"

    def test_record_naming_no_transcript_refuses_naming_the_record(self,
                                                                   tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        _write_rotation_record(graph, "20260911T120000Z", gen=14)  # no session_log
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 2
        assert calls == [] and counts == {}

    def test_gen_selects_that_generation_record(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        old_tr = graph / "gen12.jsonl"
        old_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                    "input": {"command": "true"}}]),
                          encoding="utf-8")
        new_tr = graph / "gen13.jsonl"
        new_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                    "input": {"command": "whois 1.1.1.1"}}]),
                          encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", session_log=old_tr,
                               gen=12)
        _write_rotation_record(graph, "20260911T110000Z", session_log=new_tr,
                               gen=13)
        # --gen 12 must audit GEN 12's transcript (old_tr: `true`, empty wake
        # with no tool windows before the first d) — NOT the latest record.
        code, calls, counts = sensei.wake_audit(graph, SEAT, 12, None)
        assert code == 0
        assert counts == {"a": 0, "b": 0, "c": 0, "d": 1, "s": 0}
        assert calls[0]["cmd"] == "true"

    def test_real_record_shape_names_transcript_only_at_handover_join(self,
                                                                     tmp_path):
        # a LIVE rotation record does NOT carry `session_log`; it names its
        # transcript at `handover.join.transcript` (an absolute .jsonl path)
        # together with `handover.join.session_id`. The audit must read THAT
        # transcript, never refuse because `session_log` is absent.
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        join_tr = graph / "live.jsonl"
        join_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                     "input": {"command": "whois 1.1.1.1"}}]),
                          encoding="utf-8")
        rec = _write_rotation_record(
            graph, "20260911T135144Z", gen=15,
            join_transcript=join_tr,
            ts="20260911T135144Z")
        # the record carries the join block but NO session_log at any level
        doc = json.loads(rec.read_text(encoding="utf-8"))
        assert "session_log" not in doc
        assert doc["handover"]["join"]["transcript"] == str(join_tr)
        # --gen-less wake-audit defaults to this latest record and audits it
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert counts == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert calls[0]["label"] == "F2"
        assert calls[0]["source"].endswith("20260911T135144Z.json")

    def test_real_record_shape_join_transcript_respects_gen_selection(self,
                                                                     tmp_path):
        # --gen N selects the N-generation record by observations.b_generation
        # .after even when that record carries its transcript at
        # handover.join.transcript (the live shape).
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        gen12_tr = graph / "g12.jsonl"
        gen12_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                      "input": {"command": "true"}}]),
                            encoding="utf-8")
        gen13_tr = graph / "g13.jsonl"
        gen13_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                      "input": {"command": "whois 8.8.8.8"}}]),
                            encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", gen=12,
                               join_transcript=gen12_tr,
                               ts="20260911T100000Z")
        _write_rotation_record(graph, "20260911T110000Z", gen=13,
                               join_transcript=gen13_tr,
                               ts="20260911T110000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, 12, None)
        assert code == 0
        assert counts == {"a": 0, "b": 0, "c": 0, "d": 1, "s": 0}
        assert calls[0]["cmd"] == "true"
        assert calls[0]["source"].endswith("20260911T100000Z.json")

# ── amended g15 build order (L4.251 fix-only follow-up): piped own-row grep
# ── of seats.md -> (b); hand ack / meter --pin -> service-owed (s); template
# ── after_join steps -> (s); and --redact secret/email/message masking ─────

class TestServiceOwedClassification:
    def test_piped_own_row_grep_of_seats_md_is_byhand_read_not_work(self):
        # the rule `(ls|cat|sed|grep)\b.*seats\.md` needs the file AFTER the
        # verb, so `git show ...seats.md | grep` (file BEFORE the pipe) used to
        # fall to (d). A command naming seats.md with a read-ish verb ANYWHERE
        # is a by-hand read (b), never real work.
        cmd = ('git show origin/season/s2:.agi/nodes/.geometry/seats.md '
               "| grep '\"name\": \"sanctuary-director\"'")
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"

    def test_grep_seats_md_is_byhand_read_unchanged(self):
        cat, _ = sensei.classify_call(
            "grep -o '\"name\": \"sanctuary-director\"' "
            ".agi/nodes/.geometry/seats.md", "Bash", SEAT, _ft_entries())
        assert cat == "b"

    def test_hand_ack_is_service_owed_with_label(self):
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py ack --seat sanctuary-director "
            "--gen 3 --ref abc123 continue", "Bash", SEAT, _ft_entries())
        assert cat == "s"
        assert label == "ack"

    def test_hand_meter_pin_is_service_owed_with_label(self):
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py meter --pin 5f2 --session-log "
            "/tmp/s.json", "Bash", SEAT, _ft_entries())
        assert cat == "s"
        assert label == "meter"

    def test_template_after_join_step_is_service_owed(self):
        # a step the LIVE after_join list declares (but not one of the two
        # hardcoded) is still (s) with the template's own label.
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py register --seat "
            "sanctuary-director", "Bash", SEAT, _ft_entries(), after_join=_aj_entries())
        assert cat == "s"
        assert label == "register"

    def test_plain_read_not_matching_after_join_stays_byhand_or_work(self):
        # a hand read that matches NO after_join step is (b), unchanged — the
        # s rule must not swallow general reads.
        cat, _ = sensei.classify_call(
            "ls -la /home/ubuntu/work/agi/.agi/sessions/rotations | tail -5",
            "Bash", SEAT, _ft_entries(), after_join=_aj_entries())
        assert cat == "b"
        cat2, _ = sensei.classify_call(
            "python3 -m pytest extensions/agi/tests/test_sensei.py -q",
            "Bash", SEAT, _ft_entries(), after_join=_aj_entries())
        assert cat2 == "d"


class TestServiceOwedEndToEnd:
    def test_ack_pin_reads_reports_and_window_cut_by_d_not_s(self, tmp_path,
                                                              capsys):
        # one hand ack (s), one hand pin (s), two reads (b), then real work
        # (d). The s calls are OUTSIDE the a/b/c/d counts and NEVER cut the
        # window — only the d call does.
        from types import SimpleNamespace
        tools_and_cmds = [
            ("Bash", "python3 extensions/agi/bin/rotate.py ack --seat "
                     "sanctuary-director --gen 14 --ref 7aeee9 continue"),
            ("Bash", "python3 extensions/agi/bin/rotate.py meter --pin 5f2 "
                     "--session-log /tmp/s.json"),
            ("Bash", "ls -la /home/ubuntu/work/agi/.agi/sessions/rotations "
                     "| tail -5"),
            ("Bash", "ps -o pid,ppid -p 1234 2>/dev/null"),
            ("Bash", "python3 -m pytest extensions/agi/tests/test_sensei.py "
                     "-q"),
        ]
        graph, tr = _write_root(tmp_path, tools_and_cmds)
        code, calls, counts = sensei.wake_audit(graph, SEAT, 14, tr)
        assert code == 0
        # s calls do not cut the window; the d call cuts it at position 5
        assert len(calls) == 5
        assert [c["cat"] for c in calls] == ["s", "s", "b", "b", "d"]
        assert counts == {"a": 0, "b": 2, "c": 0, "d": 1, "s": 2}
        args = SimpleNamespace(seat=SEAT, gen=14, transcript=str(tr),
                               redact=True)
        rc = sensei.cmd_wake_audit(graph, args)
        assert rc == 0
        out = capsys.readouterr().out
        assert "counts: a=0 b=2 c=0 d=1" in out
        assert "service-owed: s=2 (ack, meter)" in out


class TestRedact:
    def test_redact_key_and_email(self):
        out = sensei.redact_text(
            "echo Bearer sk-or-v1-0123456789abcdef0123456789abcdef "
            "someone@example.com")
        assert "<redacted:key>" in out
        assert "<redacted:email>" in out
        assert "sk-or-v1-0123456789abcdef0123456789abcdef" not in out
        assert "someone@example.com" not in out

    def test_redact_message_body_keeps_verb_and_recipient(self):
        out = sensei.redact_text("send.py send belam 'secret body'")
        assert out == "send.py send belam <redacted:message>"

    def test_redact_default_on_and_no_redact_raw(self, tmp_path, capsys):
        from types import SimpleNamespace
        cmd = ("echo Bearer sk-or-v1-0123456789abcdef0123456789abcdef "
               "someone@example.com")
        graph, tr = _write_root(tmp_path, [("Bash", cmd)])
        # default (--redact ON): the report carries no raw token or email
        args = SimpleNamespace(seat=SEAT, gen=14, transcript=str(tr),
                               redact=True)
        assert sensei.cmd_wake_audit(graph, args) == 0
        out = capsys.readouterr().out
        assert "<redacted:key>" in out and "<redacted:email>" in out
        assert "sk-or-v1-0123456789abcdef0123456789abcdef" not in out
        # --no-redact: a local raw view keeps them
        args2 = SimpleNamespace(seat=SEAT, gen=14, transcript=str(tr),
                                redact=False)
        assert sensei.cmd_wake_audit(graph, args2) == 0
        out2 = capsys.readouterr().out
        assert "sk-or-v1-0123456789abcdef0123456789abcdef" in out2
        assert "someone@example.com" in out2


def test_wake_audit_help_exits_zero():
    # `sensei.py wake-audit -h` must exit 0 (argparse -h); the --redact flag
    # is part of that surface.
    try:
        sensei.main(["wake-audit", "-h"])
    except SystemExit as e:
        assert e.code == 0
    else:
        raise AssertionError("argparse -h should have raised SystemExit(0)")
