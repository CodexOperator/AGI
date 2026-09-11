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

    def test_after_join_ack_done_by_hand_is_category_b_not_real_work(self):
        # rotate.py ack is an after_join step the SERVICE performs; the agent
        # doing it by hand is a hand redone of a covered action → b, never d.
        cmd = ("python3 extensions/agi/bin/rotate.py ack --seat "
               "sanctuary-director --gen 14 --ref 7aeee9 continue")
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"

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
    rot.write_text(
        "---\nid: config:rotations\ntype: config\n"
        "templates:\n  director:\n    startup:\n      first_turn:\n"
        f"{ft_lines}\n  prime_director:\n    startup:\n      first_turn:\n"
        '        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify"}\n'
        "edited_by: test\n---\n"
        "<!-- BODY:BEGIN -->\n# config:rotations\n\n## facts\n- F1 (gen: by hand)\n",
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
    assert counts == {"a": 1, "b": 1, "c": 1, "d": 1}
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