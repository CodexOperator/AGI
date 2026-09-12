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
