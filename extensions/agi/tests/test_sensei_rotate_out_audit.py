"""Tests for sensei.py rotate-out-audit (goal:g15.13 / hypothesis
:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window).

Mirror of test_sensei_wake_audit.py, over the OUTGOING predecessor instead
of the incoming successor: the classifier (classify_call) is reused as-is;
what differs is the WINDOW — every assistant tool_use after the predecessor's
LAST real user input to the end of its OWN transcript — and the way the
predecessor transcript is resolved (through the rotation records, never the
newest slug-dir transcript). All fixtures synthetic; no real seat, transcript
or write is touched.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import sensei  # noqa: E402
import rotate  # noqa: E402


def _git(cwd: Path, *args: str):
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)

# A synthetic director first_turn mirroring the LIVE config:rotations shape,
# identical to the wake-audit fixture so the two audits share one classifier.
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

# --gen 14 rotates OUT. The previous record (after == 14) is gen 14 joining
# its seat, and carries gen 14's OWN transcript in handover.join.transcript.
GEN = 14
OUT_STAMP = "20260911T150000Z"   # the rotation that took gen 14 out (before=14)
PREV_STAMP = "20260911T100000Z"  # the rotation that brought gen 14 in (after=14)
RECORDED_OUT = "2026-09-11T15:00:00Z"


def _write_root(tmp_path: Path, gen14_calls):
    """Synthetic graph root: config:seats + config:rotations + two rotation
    records + the predecessor's (gen 14's) transcript."""
    graph = tmp_path / ".agi"
    nodes = graph / "nodes"
    (nodes / ".geometry").mkdir(parents=True, exist_ok=True)
    (nodes / "config").mkdir(parents=True, exist_ok=True)
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

    # the predecessor's (gen 14's) transcript: a real user input first, then
    # a few tool_use calls separated by tool_result feedback, then the calls
    # we want in the window up to the record's recorded_at.
    tr = graph / "gen14.jsonl"
    events = []
    events.append(json.dumps({"type": "user",
                              "message": {"role": "user", "content": [
                                  {"type": "text", "text": "merge-up 14: go"}]}}))
    IN_WINDOW = [
        # (a) re-reads a record rotate-self already handles → names the field
        ("Bash", "python3 extensions/agi/bin/rotate.py status --seat "
                 f"{SEAT} --record latest"),
        # (b) a hand poll of a pane / record (b)
        ("Bash", "tmux capture-pane -t sanctuary-director -p | tail -20"),
        # (c) protocol learning (c)
        ("Bash", "python3 extensions/agi/bin/rotate.py -h | sed -n 1,30p"),
        # (d) the genuine decision: the card edit
        ("Bash", "python3 extensions/agi/bin/write.py .agi/nodes/handoff.md "
                 "'replace body 5:9 -'"),
        # (d) the genuine decision: the rotate-self invocation
        ("Bash", f"python3 extensions/agi/bin/rotate.py rotate-self "
                 f"--seat {SEAT} --gen 15"),
    ]
    payload = IN_WINDOW if gen14_calls is None else gen14_calls
    for tool, cmd in payload:
        events.append(json.dumps({"type": "assistant",
                                  "message": {"role": "assistant", "content": [
                                      {"type": "tool_use", "name": tool,
                                       "input": {"command": cmd}}]}}))
        events.append(json.dumps({"type": "user",
                                  "message": {"role": "user", "content": [
                                      {"type": "tool_result",
                                       "content": "ok", "tool_use_id": "t"}]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")

    # rotation records: PREV (gen 14 joined, after==14, carries gen14's
    # transcript) and OUT (gen 14 left, before==14, recorded_at = window end).
    rot_dir = graph / "sessions" / "rotations"
    rot_dir.mkdir(parents=True, exist_ok=True)
    prev = {"seat": SEAT, "recorded_at": "2026-09-11T10:00:00Z",
            "observations": {"b_generation": {"before": 13, "after": 14}},
            "handover": {"join": {"transcript": str(tr)}}}
    (rot_dir / f"{SEAT}.{PREV_STAMP}.json").write_text(
        json.dumps(prev), encoding="utf-8")
    out = {"seat": SEAT, "recorded_at": RECORDED_OUT,
           "observations": {"b_generation": {"before": 14, "after": 15}},
           "handover": {"join": {"transcript": "should-not-be-used"}},
           "s12_self_reap": {"chain": [999999]}}
    (rot_dir / f"{SEAT}.{OUT_STAMP}.json").write_text(
        json.dumps(out), encoding="utf-8")
    return graph, tr


def test_rotate_out_audit_resolves_through_previous_record_and_classifies(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    # gen 14's transcript came from the PREVIOUS record (after == 14), not the
    # newest slug-dir file, and not the OUT record's own join.transcript.
    assert str(window["log_path"]) == str(tr)
    assert "previous record" in window["source"]
    assert window["gen"] == 14
    assert window["recorded_at"] == RECORDED_OUT
    # five calls in the window: a, b, c, d, d
    assert len(calls) == 5
    cats = [c["cat"] for c in calls]
    assert cats == ["a", "b", "c", "d", "d"]
    assert counts == {"a": 1, "b": 1, "c": 1, "d": 2, "s": 0}
    assert calls[0]["label"] == "rotation-record"  # (a) names the record field
    assert calls[2]["cat"] == "c" and calls[2]["label"] is None


def test_rotate_out_audit_default_gen_is_latest_record_before(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    # no --gen → defaults to the latest record's b_generation.before == 14
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, None, None)
    assert code == 0
    assert window["gen"] == 14


def test_rotate_out_audit_window_starts_after_last_real_input(tmp_path):
    # a second real user input half-way down: everything before it is OUT of
    # the window, everything after is IN.
    graph, tr = _write_root(tmp_path, None)
    lines = tr.read_text(encoding="utf-8").splitlines()
    # splice a real user turn before the last two tool_use calls
    lines.insert(-4, json.dumps(
        {"type": "user", "timestamp": "2026-09-11T14:55:00Z",
         "message": {"role": "user", "content": [
             {"type": "text", "text": "owner: check the handoff"}]}}))
    tr.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert window["start_ts"] == "2026-09-11T14:55:00Z"
    # only the last two calls (the two genuine decisions) are in the window
    assert [c["cat"] for c in calls] == ["d", "d"]
    assert counts == {"a": 0, "b": 0, "c": 0, "d": 2, "s": 0}


def test_rotate_out_audit_plain_string_content_is_a_real_input(tmp_path):
    # RED-FIRST for the falsifier: a LATER real user turn whose message.
    # content is a plain STRING (not a list of blocks) must start the window
    # and exclude the tool_uses that came before it. Previously the string
    # content was skipped by `if not isinstance(content, list): continue`,
    # so the window started at the transcript head instead.
    graph, tr = _write_root(tmp_path, None)
    lines = tr.read_text(encoding="utf-8").splitlines()
    # splice a plain-string real user turn before the last two tool_use calls,
    # with tool_use calls on BOTH sides (the earlier ones must be excluded)
    lines.insert(-4, json.dumps(
        {"type": "user",
         "timestamp": "2026-09-11T14:56:00Z",
         "message": {"role": "user",
                      "content": "[agi-nudge] unread for sanctuary-director: "
                                  "rotate out now"}}))
    tr.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    # the window starts at the string-content turn, with its timestamp
    assert window["start_ts"] == "2026-09-11T14:56:00Z"
    assert window["start_line"] > 0
    # only the two calls AFTER the string turn are in the window
    assert [c["cat"] for c in calls] == ["d", "d"]
    assert counts == {"a": 0, "b": 0, "c": 0, "d": 2, "s": 0}


def test_rotate_out_audit_whitespace_string_content_is_not_a_real_input(tmp_path):
    # an all-whitespace plain-string user turn must NOT be treated as a real
    # input: it is ignored, so the head text-block turn stays the window start.
    graph, tr = _write_root(tmp_path, None)
    lines = tr.read_text(encoding="utf-8").splitlines()
    lines.insert(1, json.dumps(
        {"type": "user", "timestamp": "2026-09-11T14:50:00Z",
         "message": {"role": "user", "content": "   \n  "}}))
    tr.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    # the whitespace string turn must NOT advance the last real input past the
    # head text-block turn (line 0); it is ignored
    assert window["start_line"] == 0
    assert len(calls) == 5


def test_rotate_out_audit_no_real_user_turn_whole_transcript_is_window(tmp_path):
    # a transcript with only tool_result feedback (no real user input) after
    # the head — the whole transcript becomes the window.
    graph, tr = _write_root(tmp_path, None)
    lines = tr.read_text(encoding="utf-8").splitlines()
    # rebuild = drop the first line (the only real user input)
    no_head = lines[1:]
    tr.write_text("\n".join(no_head) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert window["start_line"] == -1
    assert len(calls) == 5  # no real input → every tool_use is in the window


def test_rotate_out_audit_explicit_transcript_overrides_records(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    if tr.is_file():
        pass
    code, calls, counts, window = sensei.rotate_out_audit(
        graph, SEAT, GEN, tr)
    assert code == 0
    assert str(window["log_path"]) == str(tr)
    assert window["source"] == "explicit --transcript"


def test_rotate_out_audit_missing_predecessor_refuses_named(tmp_path):
    # --gen for a seat with NO previous record carrying the transcript and no
    # fallback pid → named refusal (exit 2), never the newest slug-dir file.
    graph, tr = _write_root(tmp_path, None)
    # remove the PREV record so nothing resolves gen 14's own transcript
    (graph / "sessions" / "rotations" / f"{SEAT}.{PREV_STAMP}.json").unlink()
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 2
    assert calls == [] and counts == {}


def test_rotate_out_audit_unknown_seat_refuses(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    code, _, _, _ = sensei.rotate_out_audit(graph, "no-such-seat", GEN, tr)
    assert code == 2


def test_rotate_out_audit_no_matching_out_record_refuses(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    # no record with b_generation.before == 99
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, 99, tr)
    assert code == 2


def test_rotate_out_audit_role_without_template_refuses_named(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    seats = graph / "nodes" / ".geometry" / "seats.md"
    text = seats.read_text(encoding="utf-8")
    text = text.replace("edited_by: test\n---",
                        f'  - {{"name": "policy-master", "role": "farmer", "tier": 1}}\n'
                        "edited_by: test\n---")
    seats.write_text(text, encoding="utf-8")
    code, _, _, _ = sensei.rotate_out_audit(graph, "policy-master", GEN, tr)
    assert code == 2

# ── SL1.08 build-order item 7 (hypothesis:l4-the-audit-classifier-is-derived-
# ── and-the-window-is-bounded-by-the-record): the rotate-out window is bounded
# ── by the record's `recorded_at`, not the transcript end. A farewell turn
# ── AFTER the record (belam gen-IX shape: a 15:15Z farewell after a 14:05Z
# ── record) must not invert the window to zero calls. ──────────────────────

def test_rotate_out_audit_window_bounded_by_recorded_at_excludes_post_record_farewell(tmp_path):
    # belam gen-IX row: after the record's recorded_at (15:00Z) a real farewell
    # turn + one tool call arrive. The window must pick the LAST real input AT
    # OR BEFORE recorded_at (the head), stop at recorded_at, and exclude the
    # post-record call — not invert to zero calls by starting at the farewell.
    graph, tr = _write_root(tmp_path, None)
    lines = tr.read_text(encoding="utf-8").splitlines()
    farewell = json.dumps({"type": "user",
        "timestamp": "2026-09-11T15:15:00Z",
        "message": {"role": "user",
                    "content": [{"type": "text", "text": "farewell go"}]}})
    post = json.dumps({"type": "assistant", "timestamp": "2026-09-11T15:16:00Z",
        "message": {"role": "assistant", "content": [
            {"type": "tool_use", "name": "Bash", "input": {"command": "true"}}]}})
    lines.append(farewell)
    lines.append(post)
    tr.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    # window starts at the head turn (the last real input <= recorded_at), NOT
    # the farewell — so it is NOT inverted to zero calls
    assert window["start_line"] == 0
    assert window["recorded_at"] == RECORDED_OUT
    assert len(calls) == 5
    # the post-record call (cmd `true`) is OUT of the window
    assert all(c["cat"] != "b" or c["cmd"] != "true" for c in calls)
    assert all(c["cmd"] != "true" for c in calls)
    assert counts == {"a": 1, "b": 1, "c": 1, "d": 2, "s": 0}


# ── SL3.03 one-tool-wrapper parity (hypothesis:l4-the-wake-window-ends-at-
# ── the-ack-and-both-audits-share-one-tool-wrapper): the SAME tool_use must
# ── classify identically on the wake side and the rotate-out side — a covered
# ── Read/Grep is (b), an Edit/Write of the card is (d). rotate_out_audit now
# ── builds hand_paths + parsed facts and routes through classify_tool_use,
# ── exactly as wake_audit does. ────────────────────────────────────────────

def _parity_graph(tmp_path):
    """A graph readable by BOTH audits, plus a transcript carrying a Read of
    a record (b) and an Edit of the card (d) — one graph, one wrapper."""
    graph, _ = _write_root(tmp_path, None)   # seats + rotations + prev/out recs
    rec_tr = graph / "parity.jsonl"
    events = [json.dumps({"type": "user",
                          "message": {"role": "user", "content": [
                              {"type": "text",
                               "text": "merge-up 14: go"}]}}),
              json.dumps({"type": "assistant", "message": {"role":
                          "assistant", "content": [{"type": "tool_use",
                          "name": "Read", "input": {"path": "sessions/"
                          f"rotations/{SEAT}.{PREV_STAMP}.json"}}]}}),
              json.dumps({"type": "user", "message": {"role": "user",
                          "content": [{"type": "tool_result", "content":
                          "ok", "tool_use_id": "r"}]}}),
              json.dumps({"type": "assistant", "message": {"role":
                          "assistant", "content": [{"type": "tool_use",
                          "name": "Edit", "input": {"path": "HANDOFF.md",
                          "old_string": "x", "new_string": "y"}}]}})]
    rec_tr.write_text("\n".join(events) + "\n", encoding="utf-8")
    return graph, rec_tr


def test_rotate_out_read_of_record_is_b_and_edit_of_card_is_d(tmp_path):
    # E landed: rotate_out_audit now passes hand_paths + parsed facts, so a
    # covered Read of a record is (b) — it WAS (d) before (empty cmd, no facts)
    # — and the card Edit/Write stays (d).
    graph, tr = _parity_graph(tmp_path)
    code, calls, counts, window = sensei.rotate_out_audit(
        graph, SEAT, GEN, tr)
    assert code == 0
    assert [c["cat"] for c in calls] == ["b", "d"]
    assert calls[0]["tool"] == "Read" and calls[0]["label"] is None
    assert calls[1]["tool"] == "Edit"
    assert counts == {"a": 0, "b": 1, "c": 0, "d": 1, "s": 0}


def test_rotate_out_threads_the_session_id_like_wake_audit(tmp_path,
                                                           monkeypatch):
    # clause (1): rotate_out_audit must derive its hand-read paths with the
    # seat's OWN session id, exactly as wake_audit does, so a session-keyed
    # ack Read classifies the SAME (b) in both audits. A helper tested
    # directly but never threaded from this call site fails the second half.
    sid = "deadbeef-1111-2222-3333-444444444444"
    graph, _ = _write_root(tmp_path, None)
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        f'  - {{"name": "{SEAT}", "role": "director", "tier": 1, '
        f'"session_id": "{sid}"}}\n'
        "edited_by: test\n---\n<!-- BODY:BEGIN -->\n", encoding="utf-8")
    ack = graph / "sessions" / "seats" / f"{SEAT}.ack.{sid[:8]}.json"
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text("{}\n", encoding="utf-8")
    tr = graph / "keyed_ack.jsonl"
    tr.write_text("\n".join([
        json.dumps({"type": "user", "message": {"role": "user",
                    "content": [{"type": "text",
                                 "text": "merge-up 14: go"}]}}),
        json.dumps({"type": "assistant", "message": {"role": "assistant",
                    "content": [{"type": "tool_use", "name": "Read",
                                 "input": {"path": str(ack)}}]}}),
    ]) + "\n", encoding="utf-8")
    assert rotate._ack_session_id(graph, SEAT) == sid
    _, r_calls, _, _ = sensei.rotate_out_audit(graph, SEAT, GEN, tr)
    _, w_calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
    assert [c["cat"] for c in r_calls] == ["b"]
    assert [c["cat"] for c in w_calls] == ["b"]
    assert r_calls[0]["tool"] == "Read" and w_calls[0]["tool"] == "Read"
    assert [(c["cat"], c["label"]) for c in r_calls] == \
           [(c["cat"], c["label"]) for c in w_calls]
    # the signal is the THREADED identity, never a physical path: stub the
    # identity to "" and the SAME read must fall to (d) in both audits.
    monkeypatch.setattr(rotate, "_ack_session_id", lambda root, seat: "")
    _, r_calls2, _, _ = sensei.rotate_out_audit(graph, SEAT, GEN, tr)
    _, w_calls2, _ = sensei.wake_audit(graph, SEAT, None, tr)
    assert [c["cat"] for c in r_calls2] == ["d"]
    assert [c["cat"] for c in w_calls2] == ["d"]


def test_rotate_out_and_wake_classify_the_same_tool_use_identically(tmp_path):
    # the SAME Read-of-a-record and Edit-of-a-card fed to BOTH audits yield
    # identical (cat, label) — the shared-wrapper parity guarantee.
    graph, tr = _parity_graph(tmp_path)
    _, r_calls, _, _ = sensei.rotate_out_audit(graph, SEAT, GEN, tr)
    _, w_calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
    r_cats = [(c["cat"], c["label"], c["tool"]) for c in r_calls]
    w_cats = [(c["cat"], c["label"], c["tool"]) for c in w_calls]
    # both audits see the Read then the Edit, in the same order
    assert r_cats == [("b", None, "Read"), ("d", None, "Edit")]
    assert r_cats == w_cats
    # and classify_tool_use is the ONE function both route through
    hand = sensei._hand_read_paths(sensei._extract_first_turn(
        sensei._read_rotations(graph)[0], "director"), [], SEAT)
    read_cat, read_lbl, _ = sensei.classify_tool_use(
        "Read", {"path": f"sessions/rotations/{SEAT}.{PREV_STAMP}.json"},
        SEAT, [], [], hand)
    edit_cat, edit_lbl, _ = sensei.classify_tool_use(
        "Edit", {"path": "HANDOFF.md", "old_string": "x",
                  "new_string": "y"}, SEAT, [], [], hand)
    assert (read_cat, read_lbl) == ("b", None)
    assert (edit_cat, edit_lbl) == ("d", None)


# ── SL3.03 items (B) (C) (D): the registry-json fallback resolves a REAL
# ── transcript or refuses by name; the registry-dir seam; ONE records path.
# ── FALSIFIER = an audit that exits 0 with 0 calls on a registry fallback.
# ──────────────────────────────────────────────────────────────────────────

def _write_out_only(tmp_path, monkeypatch):
    """_write_root with the PREV record deleted (so resolution skips step 2
    and reaches the registry fallback) and rotate.CC_PROJECTS_DIR redirected
    to a fixture, so the DERIVED transcript path is controllable. Returns
    (graph, reg_dir, proj_dir, pid)."""
    graph, _ = _write_root(tmp_path, None)
    (graph / "sessions" / "rotations" / f"{SEAT}.{PREV_STAMP}.json").unlink()
    reg = tmp_path / "fixture-registry"; reg.mkdir()
    proj = tmp_path / "fixture-projects"
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", proj)
    return graph, reg, proj, 999999, "aaaa-bbbb"


def test_rotate_out_registry_fallback_resolves_derived_transcript(tmp_path, monkeypatch):
    # item (B): a registry `<pid>.json` {pid, sessionId, cwd} whose DERIVED
    # transcript exists -> the audit resolves IT (not the registry file) and
    # classifies its calls (non-zero).
    graph, reg, proj, pid, sess = _write_out_only(tmp_path, monkeypatch)
    (reg / f"{pid}.json").write_text(
        json.dumps({"pid": pid, "sessionId": sess, "cwd": "/a/b.c"}),
        encoding="utf-8")
    derived = proj / "-a-b-c" / f"{sess}.jsonl"
    derived.parent.mkdir(parents=True, exist_ok=True)
    events = [json.dumps({"type": "user", "message": {"role": "user",
              "content": [{"type": "text", "text": "merge-up: go"}]}}),
              json.dumps({"type": "assistant", "message": {"role":
              "assistant", "content": [{"type": "tool_use", "name": "Bash",
              "input": {"command": "echo hi"}}]}})]
    derived.write_text("\n".join(events) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(
        graph, SEAT, GEN, None, registry_dir=str(reg))
    assert code == 0
    # the transcript resolved is the DERIVED path, never the registry file
    assert str(window["log_path"]) == str(derived)
    assert window["source"] == f"{pid}.json / s12_self_reap.chain"
    assert len(calls) == 1
    assert counts == {"a": 0, "b": 0, "c": 0, "d": 1, "s": 0}


def test_rotate_out_registry_named_refusal_when_derived_absent(tmp_path, monkeypatch, capsys):
    # item (B): a registry file that PARSES and NAMES a transcript that is
    # ABSENT is a NAMED REFUSAL (exit 2, message naming both paths) — never
    # exit 0 with `0 calls` (the falsifier).
    graph, reg, proj, pid, sess = _write_out_only(tmp_path, monkeypatch)
    (reg / f"{pid}.json").write_text(
        json.dumps({"pid": pid, "sessionId": sess, "cwd": "/a/b.c"}),
        encoding="utf-8")
    derived = proj / "-a-b-c" / f"{sess}.jsonl"
    code, calls, counts, window = sensei.rotate_out_audit(
        graph, SEAT, GEN, None, registry_dir=str(reg))
    assert code == 2
    assert calls == [] and counts == {}
    err = capsys.readouterr().err
    assert f"{pid}.json" in err and str(derived) in err
    assert ", absent" in err
    assert "0 calls" not in err


def test_rotate_out_registry_dir_is_honoured(tmp_path, monkeypatch):
    # item (C): a registry file in a FIXTURE dir is found only when
    # --registry-dir points at it; the real ~/.claude/sessions is NOT
    # consulted for the fallback.
    graph, reg, proj, pid, sess = _write_out_only(tmp_path, monkeypatch)
    (reg / f"{pid}.json").write_text(
        json.dumps({"pid": pid, "sessionId": sess, "cwd": "/a/b.c"}),
        encoding="utf-8")
    # default registry dir: the fixture reg file is invisible -> no resolution.
    # Route the default through a DIFFERENT temp dir (never $HOME - a test
    # must not stat ~/.claude): the fixture `reg` file is invisible under it.
    monkeypatch.setattr(rotate, "REGISTRY_DEFAULT_DIR",
                        str(tmp_path / "not-the-registry"))
    code, _, _, _ = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 2
    # --registry-dir points at the fixture: the SAME file is found (and here
    # parses with an absent derived transcript -> named refusal, exit 2, not
    # exit 0 with 0 calls).
    code2, calls, counts, _ = sensei.rotate_out_audit(
        graph, SEAT, GEN, None, registry_dir=str(reg))
    assert code2 == 2
    assert calls == [] and counts == {}


def test_rotate_out_transcript_from_registry_derivation(tmp_path, monkeypatch):
    # the lifted helper (rotate.transcript_from_registry): cwd /a/b.c + sess s
    # -> CC_PROJECTS_DIR/-a-b-c/s.jsonl; missing cwd or sessionId -> None.
    proj = tmp_path / "proj"
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", proj)
    reg = tmp_path / "x.json"
    reg.write_text(json.dumps({"cwd": "/a/b.c", "sessionId": "s"}),
                   encoding="utf-8")
    assert rotate.transcript_from_registry(reg) == proj / "-a-b-c" / "s.jsonl"
    for bad in ({"cwd": "/a/b.c"}, {"sessionId": "s"}, {"cwd": "",
                 "sessionId": ""}, "not a dict", "{bad json"):
        reg.write_text(json.dumps(bad) if not isinstance(bad, str) else bad,
                       encoding="utf-8")
        assert rotate.transcript_from_registry(reg) is None


def test_rotate_out_records_read_shared_sessions_from_worktree(tmp_path):
    # item (D): _seat_rotation_records reads the SHARED sessions dir, so a
    # rotation record in the MAIN checkout's sessions is seen from a linked
    # worktree root (the old per-root `sessions/rotations` refused with
    # "no rotation records").
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text("{}", encoding="utf-8")
    rot_dir = graph / "sessions" / "rotations"
    rot_dir.mkdir(parents=True)
    rec = {"seat": SEAT, "recorded_at": "2026-09-11T15:00:00Z"}
    (rot_dir / f"{SEAT}.wt.json").write_text(json.dumps(rec), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init")
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/wt", str(wt), "master")
    wt_graph = wt / ".agi"
    # the fork is real: the worktree has its OWN graph dir, but the record
    # lives in the MAIN checkout's shared sessions
    assert wt_graph.resolve() != graph.resolve()
    seen = sensei._seat_rotation_records(wt_graph, SEAT)
    assert len(seen) == 1
    assert seen[0][1]["seat"] == SEAT



def test_fallback_pids_reads_dict_chain_and_bare_ints():
    """goal:g15.25 (c) — `_fallback_pids` reads `entry['pid']` from the DICT
    entries `_reap_chain` actually returns and STILL accepts a bare int (a
    record written before this cut). Before the fix it filtered bare ints
    only, so the one reap section's chain of {pid, was_alive, termd, ...}
    dicts yielded [] on every recorded rotation."""
    rec = {"s12_self_reap": {"chain": [
        {"pid": 111, "was_alive": True, "termd": True, "gone_after": True},
        {"pid": 222, "was_alive": False, "termd": False, "gone_after": False},
        333,
        {"pid": 0},            # refused: pid <= 0
        {"pid": -5, "termd": True},
        {"pid": "444"},        # non-int ignored
    ]}}
    assert sensei._fallback_pids(rec) == [111, 222, 333]
    # a record written before the dict cut still resolves
    assert sensei._fallback_pids({"s12_self_reap": {"chain": [999]}}) == [999]
    # no s12 / no chain -> []
    assert sensei._fallback_pids({}) == []
    assert sensei._fallback_pids({"s12_self_reap": {"chain": []}}) == []


# ── hypothesis:l4-predecessor-transcript-shares-the-record-precedence-chain-
# ── and-the-join-absent-shape-resolves: the PREDECESSOR side resolves through
# ── the SAME precedence chain `_record_transcript` applies, and the two
# ── producer shapes rotate._seating_record_merge_handover leaves behind
# ── (handover PRESENT / join ABSENT / top-level transcript_path set; and a
# ── first-SEATING record whose generation rides top-level `gen_after`) are
# ── no longer silent misses. FALSIFIER before the fix: `_resolve_predecessor_
# ── transcript` reads only `handover.join.transcript`, so both shapes returned
# ── `(None, "no predecessor transcript resolved")` and the audit exited 2.

def _write_root_join_absent(tmp_path: Path, shape: str):
    """`_write_root` with the PREV (gen 14 joining) record written in a shape
    that carries NO `handover.join.transcript`:
      - "near_miss": a HYBRID — `observations.b_generation` (the rotate-self
        gen spelling) PLUS a `handover.seating_row_commit` and the top-level
        `transcript_path`. Kept because it is what the pre-fix producer left
        behind and it exercises the top-level fallback under the OLD gen
        spelling.
      - "first_seating": the prime first-SEATING record shape
        (`rotate._seating_record`): top-level `gen_after` (NO
        `observations.b_generation`) + top-level `transcript_path`, and NO
        `handover`.
      - "seating_merged": the LITERAL product of BOTH producers on disk —
        `rotate._write_seating_record` writes `rotate._seating_record`'s
        prime first-seating record, `rotate._seating_record_merge_handover`
        merges `handover.seating_row_commit` into it, and the merged file is
        renamed onto PREV_STAMP's slot and read back from disk. It carries
        NO `observations.b_generation` anywhere (the seating producer never
        writes it — that absence is the point) and NO `join` under
        `handover`.
    Returns `(graph, tr, prev_path)`."""
    graph, tr = _write_root(tmp_path, None)
    prev_path = graph / "sessions" / "rotations" / f"{SEAT}.{PREV_STAMP}.json"
    if shape == "near_miss":
        prev = {"seat": SEAT, "recorded_at": "2026-09-11T10:00:00Z",
                "observations": {"b_generation": {"before": 13, "after": 14}},
                "handover": {"seating_row_commit": "abc123"},
                "transcript_path": str(tr)}
    elif shape == "first_seating":
        prev = {"rotation": "seating", "seat": SEAT,
                "recorded_at": "2026-09-11T10:00:00Z", "trigger":
                "first-seating", "gen_before": 0, "gen_after": GEN,
                "transcript_path": str(tr)}
    elif shape == "seating_merged":
        # Built by BOTH PRODUCERS, never by an inlined copy of the merger body:
        # (1) `rotate._seating_record` + `rotate._write_seating_record` write
        # the record to disk; (2) `rotate._seating_record_merge_handover`
        # merges `handover.seating_row_commit` into THAT file and must name
        # it. A drift in either producer (a renamed key, a dropped merge, a
        # filename suffix the merger's glob no longer sees) fails HERE. The
        # writer names the file by `utcnow`, so the merged file is renamed
        # onto PREV_STAMP's slot — leaving the fixture-planted record beside
        # it would let the resolver read that older record first (filename
        # sort) and the test go green through the WRONG record.
        rec = rotate._seating_record(
            seat=SEAT, role="prime_director", source="rotate",
            window_id=None, ref="", pid=None, session_id="",
            transcript_path=str(tr), first_turn=None, generation=GEN)
        rec["recorded_at"] = "2026-09-11T10:00:00Z"
        written = rotate._write_seating_record(graph, rec)
        merged_path = rotate._seating_record_merge_handover(
            graph, {"seat": SEAT, "recorded_at": rec["recorded_at"],
                    "handover": {"seating_row_commit": "abc123"}})
        assert merged_path == str(written), (merged_path, str(written))
        written.replace(prev_path)
        # (3) read the producers' merged output back from disk as `prev`
        prev = json.loads(prev_path.read_text(encoding="utf-8"))
        assert prev["handover"]["seating_row_commit"] == "abc123", prev
        assert "observations" not in prev, prev
        assert "join" not in prev["handover"], prev
    else:
        raise AssertionError(f"unknown shape {shape!r}")
    if shape != "seating_merged":
        # seating_merged is already on disk as the producers wrote it; the
        # other two shapes are fixture-built dicts and are serialized here.
        prev_path.write_text(json.dumps(prev), encoding="utf-8")
    return graph, tr, prev_path


def _out_records(graph):
    """`(records, idx)` — the seat's rotation records and the index of the
    OUT record (`b_generation.before == GEN`), the record the audit now keys
    the window on (hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-
    by-post-and-record-never-by-b-generation: record, never generation)."""
    records = sensei._seat_rotation_records(graph, SEAT)
    for i, (_p, r) in enumerate(records):
        if sensei._gen_bounds(r)[0] == GEN:
            return records, i
    raise AssertionError("fixture has no OUT record")


@pytest.mark.parametrize("shape",
                         ["near_miss", "first_seating", "seating_merged"])
def test_predecessor_resolves_join_absent_shapes(tmp_path, shape):
    """The near-miss shape (handover present, join absent, top-level path), the
    first-seating shape (top-level `gen_after`) and the merged seating record
    `rotate._seating_record_merge_handover` actually writes ALL resolve to the
    predecessor's transcript, and the printed `source` names BOTH the record
    stamp it came from and the spelling the chain actually took — never a
    `handover.join.transcript` lie, and never a generation."""
    graph, tr, _ = _write_root_join_absent(tmp_path, shape)
    records, idx = _out_records(graph)
    p, source = sensei._resolve_predecessor_transcript(
        graph, SEAT, records, idx, None)
    assert p == tr, f"{shape}: resolved {p}, expected {tr}"
    assert source == f"previous record {PREV_STAMP} transcript_path"
    assert "gen" not in source


@pytest.mark.parametrize("shape",
                         ["near_miss", "first_seating", "seating_merged"])
def test_rotate_out_audit_resolves_near_miss_and_classifies(tmp_path, shape):
    """End-to-end: the audit exits 0 and classifies the predecessor's window
    for EVERY join-absent predecessor shape the producers leave behind — the
    near-miss hybrid, the first-seating record and the merged seating record.
    Before the fix each exited 2 ("no predecessor transcript resolved")."""
    graph, tr, _ = _write_root_join_absent(tmp_path, shape)
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert str(window["log_path"]) == str(tr)
    assert window["source"] == f"previous record {PREV_STAMP} transcript_path"
    assert window["record"] == OUT_STAMP
    assert counts == {"a": 1, "b": 1, "c": 1, "d": 2, "s": 0}


def test_predecessor_precedence_join_wins_over_top_level(tmp_path):
    """The chain is SHARED with `_record_transcript`: when the previous record
    carries BOTH the join spelling and the top-level path, the JOIN wins — the
    fix must not turn the top-level fallback into an override."""
    graph, tr, prev_path = _write_root_join_absent(tmp_path, "near_miss")
    join_tr = tmp_path / "join-wins.jsonl"
    join_tr.write_text(tr.read_text(encoding="utf-8"), encoding="utf-8")
    prev = json.loads(prev_path.read_text(encoding="utf-8"))
    prev["handover"]["join"] = {"transcript": str(join_tr)}
    prev_path.write_text(json.dumps(prev), encoding="utf-8")
    records, idx = _out_records(graph)
    p, source = sensei._resolve_predecessor_transcript(
        graph, SEAT, records, idx, None)
    assert p == join_tr
    assert source == f"previous record {PREV_STAMP} handover.join.transcript"
    assert "gen" not in source


def test_predecessor_never_resolves_the_out_records_own_transcript(tmp_path):
    """The OUT record (b_generation.before==GEN) carries a top-level
    `transcript_path` in the near-miss fixture-adjacent shape; it must NOT be
    the answer — resolution step (2) is the record that brought gen N IN."""
    graph, tr, _ = _write_root_join_absent(tmp_path, "near_miss")
    out_path = graph / "sessions" / "rotations" / f"{SEAT}.{OUT_STAMP}.json"
    out = json.loads(out_path.read_text(encoding="utf-8"))
    decoy = tmp_path / "out-own.jsonl"
    decoy.write_text(tr.read_text(encoding="utf-8"), encoding="utf-8")
    out["transcript_path"] = str(decoy)
    out_path.write_text(json.dumps(out), encoding="utf-8")
    records, idx = _out_records(graph)
    p, _ = sensei._resolve_predecessor_transcript(
        graph, SEAT, records, idx, None)
    assert p == tr, f"resolved the OUT record's own transcript: {p}"


def test_transcript_spelling_names_each_link():
    """`_transcript_spelling` names the link `_record_transcript` took, in the
    same order, and '' when none names a transcript."""
    assert sensei._transcript_spelling({}) == ""
    assert sensei._transcript_spelling(
        {"session_log": "/a.jsonl", "transcript_path": "/b.jsonl"}) == \
        "session_log"
    assert sensei._transcript_spelling(
        {"handover": {"session_log": "/a.jsonl"},
         "transcript_path": "/b.jsonl"}) == "handover.session_log"
    assert sensei._transcript_spelling(
        {"handover": {"join": {"transcript": "/j.jsonl"}},
         "transcript_path": "/b.jsonl"}) == "handover.join.transcript"
    assert sensei._transcript_spelling({"transcript_path": "/b.jsonl"}) == \
        "transcript_path"
    assert sensei._transcript_spelling(
        {"observations": {"c_readback_log_path": "/c.log"}}) == ""
    assert sensei._transcript_spelling(
        {"observations": {"c_readback_log_path": "/c.jsonl"}}) == \
        "observations.c_readback_log_path"


# ── SM.54 (hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-
# ── a-notified-output-file-read-as-its-harvest): the measured gen-8 shape —
# ── (cat <task output-file>, `send.py send <post> '[tag] ...'`, rotate) — is
# ── 1 out call, not 3. A `send.py send` is the post's OWN report (d,
# ── `send=output`), never a hand read (b); a read of the <output-file> the
# ── immediately preceding task-notification named is that task's HARVEST (d,
# ── `harvest of <task-id>`), never a poll; a read of any OTHER path is
# ── untouched and still counts.

OUT_FILE = "/tmp/claude-1001/root/59ca602d/tasks/bpohvkj78.output"


def _notified_transcript(tr: Path, calls):
    """The measured transcript: one real user turn, a task-notification (a
    plain-string user turn — the CC shape), then `calls`."""
    events = [json.dumps({"type": "user", "message": {"role": "user",
              "content": [{"type": "text", "text": "merge-up 14: go"}]}}),
              json.dumps({"type": "user", "message": {"role": "user",
              "content": "<task-notification>\n<task-id>bpohvkj78</task-id>\n"
              "<tool-use-id>t1</tool-use-id>\n"
              f"<output-file>{OUT_FILE}</output-file>\n"
              "<status>completed</status>\n</task-notification>"}})]
    for tool, cmd in calls:
        events.append(json.dumps({"type": "assistant",
            "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": tool,
                 "input": {"command": cmd}}]}}))
        events.append(json.dumps({"type": "user", "message": {"role": "user",
            "content": [{"type": "tool_result", "content": "ok",
                         "tool_use_id": "t"}]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")


SEND = ("python3 extensions/agi/bin/send.py send belam '[complete] stamped "
        "suite; rotate now' && cat .agi/sessions/quorum/belam.md")
ROTATE = "python3 extensions/agi/bin/rotate.py rotate"


def test_rotate_out_the_measured_shape_is_one_out_call_not_three(tmp_path):
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", f"cat {OUT_FILE} | cut -c1-200 && cat "
                 ".agi/sessions/verify-count.json"),
        ("Bash", SEND),
        ("Bash", ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert len(calls) == 3            # all three still PRINTED
    assert window["counted"] == 1     # only the rotate is an out call
    assert counts == {"a": 0, "b": 0, "c": 0, "d": 3, "s": 0}
    # the two excluded calls carry `pre`; window['counted'] is the floor set
    assert [c["pre"] for c in calls] == [True, True, False]
    assert calls[0]["label"] == "harvest of bpohvkj78"
    assert calls[1]["label"] == "send=output"
    assert [c["cat"] for c in calls] == ["d", "d", "d"]
    assert calls[2]["label"] is None


def test_rotate_out_a_read_of_an_unnotified_file_still_counts(tmp_path):
    # FALSIFIER: a read of a path no notification named stays a hand read (b)
    # and is COUNTED — the harvest rule must not un-count unrelated reads.
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", "cat .agi/sessions/master-sensei.log | tail -20"),
        ("Bash", ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["cat"] == "b" and calls[0]["label"] is None
    assert window["counted"] == 2


def test_rotate_out_a_send_does_not_hide_the_calls_after_it(tmp_path):
    # a send BEFORE other calls: only the send itself is un-counted; every
    # call after it is an out call.
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", SEND),
        ("Bash", "python3 -m pytest extensions/agi/tests/test_sensei.py -q"),
        ("Bash", ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert window["counted"] == 2
    assert [c["cat"] for c in calls] == ["d", "d", "d"]


def test_rotate_out_audit_writes_the_window_number_and_prints_green(
        tmp_path, capsys):
    """SM.51-56 item 8: ONE count per side. The line's count and the
    record's `calls` are the SAME read -- the payload's reconciling total
    `a+b+c+d+pre` -- while the excess keeps measuring ONLY the floor set
    `a+b+c+d` (`window['counted']`). The named `pre` bucket explains the two
    excluded calls (`send=output` report + harvest read)."""
    from types import SimpleNamespace
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", f"cat {OUT_FILE}"),
        ("Bash", SEND),
        ("Bash", ROTATE),
    ])
    rot_dir = graph / "sessions" / "rotations"
    for p in rot_dir.glob("*.json"):
        rec = json.loads(p.read_text(encoding="utf-8"))
        p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    args = SimpleNamespace(seat=SEAT, gen=GEN, transcript=None, record=None,
                           registry_dir=None, redact=True, no_record=False)
    assert sensei.cmd_rotate_out_audit(graph, args) == 0
    out = capsys.readouterr().out
    # printed count == payload['calls'] == 3 (1 floor-set call + 2 pre)
    assert (f"green {SEAT} out --record {OUT_STAMP} 3 (floor 1") in out
    audit = json.loads((rot_dir / f"{SEAT}.{OUT_STAMP}.json")
                       .read_text(encoding="utf-8"))["audit"]["out"]
    assert audit["calls"] == 3 and audit["excess"] == 0
    assert audit["pre"] == 2          # the named, additive excluded bucket
    assert audit["d"] == 1 and audit["b"] == 0
    # reconciliation by construction: calls == every bucket it reports
    assert audit["calls"] == (audit["a"] + audit["b"] + audit["c"]
                              + audit["d"] + audit["pre"])


def test_rotate_out_printed_buckets_equal_the_recorded_buckets(
        tmp_path, capsys):
    """SM.51-56 item 8, the falsifying case the suite missed: the PRINTED
    bucket line must report the SAME buckets the record holds -- the
    non-pre `a/b/c/d` plus the named `pre`. Pre-fix the line printed the
    ALL-CALLS classification (`counts`, d=3) while the record held the
    reconciling payload (d=1), so the same audit disagreed with itself and
    `a+b+c+d` over-counted against `len(calls)`."""
    import re
    from types import SimpleNamespace
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", f"cat {OUT_FILE} | cut -c1-200"),
        ("Bash", SEND),
        ("Bash", ROTATE),
    ])
    rot_dir = graph / "sessions" / "rotations"
    for p in rot_dir.glob("*.json"):
        rec = json.loads(p.read_text(encoding="utf-8"))
        p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    args = SimpleNamespace(seat=SEAT, gen=GEN, transcript=None, record=None,
                           registry_dir=None, redact=True, no_record=False)
    assert sensei.cmd_rotate_out_audit(graph, args) == 0
    out = capsys.readouterr().out
    m = re.search(r"counts: a=(\d+) b=(\d+) c=(\d+) d=(\d+) pre=(\d+)", out)
    assert m is not None
    pa, pb, pc, pd, ppre = (int(g) for g in m.groups())
    audit = json.loads((rot_dir / f"{SEAT}.{OUT_STAMP}.json")
                       .read_text(encoding="utf-8"))["audit"]["out"]
    assert (pa, pb, pc, pd, ppre) == (audit["a"], audit["b"], audit["c"],
                                      audit["d"], audit["pre"])
    assert pd == 1 and ppre == 2
    floor = pa + pb + pc + pd
    assert floor == 1 == pd + pb          # the floor set, not all calls
    assert floor + ppre == audit["calls"] == 3
    assert "(a+b+c+d is the floor set; pre is excluded from the floor)" in out


def _notification(tid: str, path: str) -> str:
    return ("<task-notification>\n<task-id>" + tid + "</task-id>\n"
            "<tool-use-id>t1</tool-use-id>\n"
            f"<output-file>{path}</output-file>\n"
            "<status>completed</status>\n</task-notification>")


def _plain_transcript(tr: Path, notices, calls):
    """A real user turn, then `notices` raw user-turn strings, then `calls`."""
    events = [json.dumps({"type": "user", "message": {"role": "user",
              "content": [{"type": "text", "text": "merge-up 14: go"}]}})]
    events += [json.dumps({"type": "user", "message": {"role": "user",
                "content": n}}) for n in notices]
    for tool, cmd in calls:
        events.append(json.dumps({"type": "assistant",
            "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": tool,
                 "input": {"command": cmd}}]}}))
        events.append(json.dumps({"type": "user", "message": {"role": "user",
            "content": [{"type": "tool_result", "content": "ok",
                         "tool_use_id": "t"}]}}))
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")


def test_rotate_out_a_stale_notified_path_is_not_the_harvest(tmp_path):
    # PROBE P2: a SECOND notification (another output file) follows the first;
    # a read of the FIRST, now stale, path is no task's harvest — it is a bare
    # read (b) and IS counted. The whole-file scan un-counted it forever.
    graph, tr = _write_root(tmp_path, None)
    other = "/tmp/claude-1001/root/59ca602d/tasks/aaa111.output"
    _plain_transcript(tr,
                      [_notification("bpohvkj78", OUT_FILE),
                       _notification("othertask", other)],
                      [("Bash", f"cat {OUT_FILE}"), ("Bash", ROTATE)])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["cat"] == "b" and calls[0]["label"] is None
    assert window["counted"] == 2          # the stale read and the rotate
    assert counts == {"a": 0, "b": 1, "c": 0, "d": 1, "s": 0}


def test_rotate_out_a_non_read_mention_of_the_path_is_not_the_harvest(tmp_path):
    """SM.51-56 item 9: the harvest is a READ of the notified <output-file>,
    never any command that merely MENTIONS it. `rm <path> && <rotate>` names
    the path but is not a harvest -- it is classified by the normal rules and
    is COUNTED (the falsifier the pre-fix substring test failed)."""
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", f"rm {OUT_FILE} && " + ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["label"] is None            # not `harvest of bpohvkj78`
    assert calls[0]["pre"] is False             # never excluded from the floor
    assert window["counted"] == 1


def test_rotate_out_a_send_without_a_tag_is_counted_not_the_report(tmp_path):
    """SM.51-56 item 10: `send=output` is the REPORT SHAPE (`[tag]`), never
    the verb. An untagged mid-window dm to a peer is real work and IS counted;
    a tagged send is the post's own report and is excluded."""
    graph, tr = _write_root(tmp_path, None)
    untagged = ("python3 extensions/agi/bin/send.py send belam 'progress: "
                "half done, still working'")
    _notified_transcript(tr, [
        ("Bash", untagged),
        ("Bash", SEND),
        ("Bash", ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["label"] is None and calls[0]["pre"] is False
    assert calls[1]["label"] == "send=output" and calls[1]["pre"] is True
    assert window["counted"] == 2   # the untagged send + the rotate


def test_rotate_out_a_read_tool_of_the_notified_path_is_the_harvest(tmp_path):
    """item 9: a `Read` tool_use whose own path IS the notified <output-file>
    is the harvest too, not only a Bash read verb."""
    graph, tr = _write_root(tmp_path, None)
    events = [json.dumps({"type": "user", "message": {
        "role": "user", "content": "go"}}),
        json.dumps({"type": "user", "message": {"role": "user",
            "content": _notification("bpohvkj78", OUT_FILE)}}),
        json.dumps({"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "tool_use", "name": "Read",
                         "input": {"file_path": OUT_FILE}}]}}),
        json.dumps({"type": "user", "message": {"role": "user",
            "content": [{"type": "tool_result", "content": "ok",
                         "tool_use_id": "t"}]}}),
        json.dumps({"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "tool_use", "name": "Bash",
                         "input": {"command": ROTATE}}]}})]
    tr.write_text("\n".join(events) + "\n", encoding="utf-8")
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["label"] == "harvest of bpohvkj78"
    assert calls[0]["pre"] is True
    assert window["counted"] == 1


def test_rotate_out_a_bare_read_with_no_notification_is_a_poll(tmp_path):
    # PROBE P3: `cat some.log` with no notification anywhere — the claim's own
    # test list says [b], uncounted. Kid 1 dodged this by using a sessions/
    # path `_is_byhand_read` already matched; this is the bare case.
    graph, tr = _write_root(tmp_path, None)
    _plain_transcript(tr, [], [("Bash", "cat some.log"), ("Bash", ROTATE)])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["cat"] == "b" and calls[0]["label"] is None
    assert window["counted"] == 2
    assert counts == {"a": 0, "b": 1, "c": 0, "d": 1, "s": 0}


def test_rotate_out_a_grep_of_the_notified_output_is_the_harvest(tmp_path):
    """Conjunct 1 (hypothesis:l4-the-sensei-classifier-…): a GREP of the
    notified <output-file> — not only a `cat` read — is that task's harvest
    (pre), never a hand poll (b). A grep pattern carries `|` inside its quotes,
    which must not end the same-pipe segment of the operand scan."""
    graph, tr = _write_root(tmp_path, None)
    _notified_transcript(tr, [
        ("Bash", f"grep -E '^PASS|^FAIL|^RESULT' {OUT_FILE} | cut -c1-120"),
        ("Bash", SEND),
        ("Bash", ROTATE),
    ])
    code, calls, counts, window = sensei.rotate_out_audit(graph, SEAT, GEN, None)
    assert code == 0
    assert calls[0]["label"] == "harvest of bpohvkj78"   # grep == harvest
    assert [c["pre"] for c in calls] == [True, True, False]
    assert window["counted"] == 1
