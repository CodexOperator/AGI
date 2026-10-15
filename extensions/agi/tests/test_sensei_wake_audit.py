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


def _cats(counts: dict):
    """The wake category counts only (a/b/c/d + service-owed s) — `counts` also carries
    the machine-readable `window_reason` (hypothesis:l4-wake-window-ends-at-
    the-ack), so exact-equality on the whole dict would bind the audit to a
    specific window ending."""
    return {k: counts.get(k, 0) for k in ("a", "b", "c", "d", "s")}


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
        cmd = "git -C /srv/agi status -sb | head -3"
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
        cmd = "ls -la /srv/agi/.agi/sessions/rotations | tail -5"
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

    def test_session_keyed_ack_cat_is_a_by_hand_read(self):
        # clause (3) of hypothesis:l4-sensei-audits-agree-on-session-keyed-
        # acks-and-top-level-session-records: `seats/<seat>.ack.<sid8>.json`
        # (the name rotate._ack_path writes for a non-prime seat) carries no
        # `sessions` segment, so the legacy `.ack.json` alternative never sees
        # it. Both spellings must be (b); an unrelated `.json` stays (d).
        assert sensei.classify_call(
            f"cat sessions/seats/{SEAT}.ack.deadbeef.json", "Bash",
            SEAT, [])[0] == "b"
        assert sensei.classify_call(
            f"cat seats/{SEAT}.ack.deadbeef.json", "Bash", SEAT, [])[0] == "b"
        assert sensei.classify_call(
            f"cat seats/{SEAT}.ack.json", "Bash", SEAT, [])[0] == "b"
        # not over-matched: a bare unrelated `.json` read, and a `.ack.` name
        # whose middle token is not an 8-char session prefix
        assert sensei.classify_call(
            "cat reports/summary.json", "Bash", SEAT, [])[0] == "d"
        assert sensei.classify_call(
            f"cat seats/{SEAT}.ack.dead.json", "Bash", SEAT, [])[0] == "d"

    def test_absent_first_turn_list_means_everything_is_hand_read_or_work(self):
        # no template for the role → caller refuses BEFORE classifying, but the
        # pure function must not silently use another role's template; [] means
        # no labels match, so reruns fall through to b/d, never bogus category a.
        cmd = "python3 extensions/agi/bin/rotate.py status --seat X --record latest"
        cat, label = sensei.classify_call(cmd, "Bash", "X", [])
        assert cat in ("b", "d")  # not "a" without a template
        assert label is None


def _write_root(tmp_path: Path, tools_and_cmds, *, posts: bool = False):
    """Write a synthetic graph root with config:seats (or, when `posts`,
    a post-first config:posts) + config:rotations + a synthetic CC transcript
    of the given `(tool, cmd)` calls."""
    graph = tmp_path / ".agi"
    nodes = graph / "nodes"
    (nodes / ".geometry").mkdir(parents=True, exist_ok=True)
    (nodes / "config").mkdir(parents=True, exist_ok=True)
    # the one-season geometry config: seats.md / config:seats (`seats:`)
    # by default; posts.md / config:posts (`posts:`) on a post-first tree.
    # ONLY the chosen file is written -- no fallback present -- so the audit
    # proves it resolves the row through geometry_config.resolve either way.
    cfg_name = "posts" if posts else "seats"
    cfg = (nodes / ".geometry" / f"{cfg_name}.md")
    cfg.write_text(
        "---\n"
        f"id: config:{cfg_name}\n"
        "type: config\n"
        f"{cfg_name}:\n"
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
        f'`grep "name": "<seat>" .agi/nodes/.geometry/{cfg_name}.md`\n'
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


def _set_seat_row(graph: Path, row: dict, *, posts: bool = False) -> None:
    """Rewrite the geometry seat config with ONE synthetic row (used by the
    session-key tests, which need `session_id` / `role` on the row)."""
    cfg_name = "posts" if posts else "seats"
    cfg = graph / "nodes" / ".geometry" / f"{cfg_name}.md"
    cfg.write_text(
        "---\n"
        f"id: config:{cfg_name}\n"
        "type: config\n"
        f"{cfg_name}:\n"
        f"  - {json.dumps(row)}\n"
        "edited_by: test\n---\n<!-- BODY:BEGIN -->\n", encoding="utf-8")


def _write_rotation_record(graph: Path, seed: str, *, session_log: Path | None = None,
                           gen: int | None = None, ts: str = "20260911T120000Z",
                           join_transcript: Path | None = None,
                           session_id: str | None = None,
                           top_session_id: str | None = None):
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
    if top_session_id is not None:
        # clause (2): rotate.py ALSO writes the session id at the record TOP
        # level (rotate.py:4702-4703), which is how a FIRST-SEATING record
        # carries it -- never under handover.join on that shape.
        rec["session_id"] = top_session_id
    if join_transcript is not None or session_id is not None:
        # the shape every LIVE rotation record carries
        # (handover.join.transcript + handover.join.session_id)
        ho = rec.setdefault("handover", {})
        join = ho.setdefault("join", {})
        if join_transcript is not None:
            join["transcript"] = str(join_transcript)
        if session_id is not None:
            join["session_id"] = session_id
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
    assert _cats(counts) == {"a": 1, "b": 1, "c": 1, "d": 1, "s": 0}
    assert counts["window_reason"] == "first (d) at 4"
    assert calls[0]["label"] == "rotation-record"
    assert calls[2]["label"] == "write-verbs"  # -h matched the label but is c
    assert calls[3]["tool"] == "Bash"


# ── SL3.03 window items (hypothesis:l4-the-wake-window-ends-at-the-ack-and-
# ── both-audits-share-one-tool-wrapper): the wake window ends at the ack call
# ── INCLUSIVE (+ the row commit right after it), not at the first
# ── classifier-(d); a transcript with NO ack keeps the first-(d) rule ──────

def _ack_window_blocks(seed: str = "20260911T120000Z"):
    """[git status (d), 20 covered Read tool_use, rotate.py ack, git commit
    naming seats.md, then REAL work] — the ack-window fixture."""
    blocks = [{"type": "tool_use", "name": "Bash",
               "input": {"command": "git status -sb"}}]
    for i in range(20):
        blocks.append({"type": "tool_use", "name": "Read",
                       "input": {"path": f"sessions/rotations/"
                                  f"{SEAT}.20260911T{i:06d}Z.json"}})
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": f"python3 extensions/agi/bin/"
                              f"rotate.py ack --seat {SEAT} --ref abc123 "
                              "continue"}})
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": "git add HANDOFF.md seats.md "
                              "&& git commit -q -m 'seat row'"}})
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": "python3 -m pytest "
                              "extensions/agi/tests/test_sensei.py -q"}})
    return blocks


def _cfg_window_blocks(cfg_name: str):
    """The ack-window fixture bound to ONE config spelling (`seats` or
    `posts`): the closing Read touches the config file at that spelling and
    the sealing `git commit` names it at that spelling. Proves the audit
    resolves the row AND seals the seating on either a seats-only or a
    posts-only tree (hypothesis:l4-a-seat-is-a-post-everywhere)."""
    blocks = [{"type": "tool_use", "name": "Bash",
               "input": {"command": "git status -sb"}}]
    # a Read/Grep of the live config at THIS spelling is a by-hand read (b)
    blocks.append({"type": "tool_use", "name": "Read",
                   "input": {"path": f".agi/nodes/.geometry/{cfg_name}.md"}})
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": f"python3 extensions/agi/bin/"
                              f"rotate.py ack --seat {SEAT} --ref abc123 "
                              "continue"}})
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": f"git add HANDOFF.md {cfg_name}.md "
                              "&& git commit -q -m 'seat row'"}})
    return blocks


@pytest.mark.parametrize("posts", [True, False])
def test_wake_audit_finds_rows_and_seals_on_either_config_spelling(tmp_path, posts):
    """Only ONE geometry config file exists (posts.md on a post-first tree,
    seats.md on a one-season tree). The audit must resolve the seat row through
    `geometry_config.resolve`, classify the config Read as a by-hand read, and
    extend the wake window to the `git commit` that names that spelling — on
    BOTH spellings."""
    cfg_name = "posts" if posts else "seats"
    graph, _ = _write_root(tmp_path, [("Bash", "true")], posts=posts)
    # only the chosen file exists; the other spelling must be ABSENT
    other = "seats" if posts else "posts"
    assert not (graph / "nodes" / ".geometry" / f"{other}.md").exists()
    tr = graph / "ack.jsonl"
    tr.write_text(_events(_cfg_window_blocks(cfg_name)), encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0                       # the row resolved through resolve()
    # git status(d) + cfg Read(b) + ack(b) + row commit = 4 calls, window
    # ends at the commit that names THIS spelling
    assert len(calls) == 4
    assert counts["window_reason"] == "ack call 3 + row commit 4"
    assert calls[1]["cat"] == "b"          # the config Read is a by-hand read
    assert calls[3]["cat"] == "d"          # the gap: sealing commit is real (d)


def test_wake_ack_ends_window_inclusive_and_extends_to_the_row_commit(tmp_path):
    # git status (d) 1 + 20 reads (b) 20 + ack (b) + row commit (b) = 23;
    # the real work AFTER the commit is beyond the window and NOT listed.
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    tr = graph / "ack.jsonl"
    tr.write_text(_events(_ack_window_blocks()), encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert len(calls) == 23                      # ack(idx22) + row commit(idx23)
    assert counts["window_reason"] == "ack call 22 + row commit 23"
    # git status(d) + 20 reads(b) + ack(b) + row commit(d, git add/commit is
    # not a by-hand read) — 23 calls, the pytest run beyond the commit excluded.
    # the ack is service-owed (s) since L4.251 — 20 reads (b), ack (s),
    # git status + row commit (d)
    assert _cats(counts) == {"a": 0, "b": 20, "c": 0, "d": 2, "s": 1}
    # the row commit is the sealed end; the pytest run is excluded
    assert "commit" in calls[-1]["cmd"]
    assert "pytest" not in calls[-1]["cmd"]


def test_wake_ack_ends_at_ack_with_reason_when_no_row_commit_follows(tmp_path):
    # ack present but no `git commit` naming seats.md right after -> window
    # stops INCLUSIVE at the ack call, reason names just the ack.
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    blocks = [{"type": "tool_use", "name": "Bash",
               "input": {"command": "git status -sb"}}]
    blocks.append({"type": "tool_use", "name": "Bash",
                   "input": {"command": f"python3 extensions/agi/bin/"
                              f"rotate.py ack --seat {SEAT} --ref abc123 "
                              "// continue"}})
    tr = graph / "ack_only.jsonl"
    tr.write_text(_events(blocks), encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert len(calls) == 2
    assert counts["window_reason"] == "ack call 2"


def test_wake_no_ack_keeps_first_d_rule_with_reason(tmp_path):
    # no ack call anywhere -> the OLD first-(d) cut, reason names the boundary.
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    blocks = [{"type": "tool_use", "name": "Read",
               "input": {"path": f"sessions/rotations/{SEAT}.json"}},
              {"type": "tool_use", "name": "Bash",
               "input": {"command": "git status -sb"}},
              {"type": "tool_use", "name": "Bash",
               "input": {"command": "python3 -m pytest x.py -q"}},
              {"type": "tool_use", "name": "Bash",
               "input": {"command": "rotate.py ack --help"}}]  # help, not the act
    tr = graph / "noack.jsonl"
    tr.write_text(_events(blocks), encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert len(calls) == 2
    assert counts["window_reason"] == "first (d) at 2"
    assert _cats(counts) == {"a": 0, "b": 1, "c": 0, "d": 1, "s": 0}


def test_wake_ack_help_probe_is_not_treated_as_the_ack_call(tmp_path):
    # `rotate.py ack --help` is protocol learning (c); the WINDOW must not
    # treat it as the ack (it would cut the wake at a usage read).
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    blocks = [{"type": "tool_use", "name": "Bash",
               "input": {"command": "python3 extensions/agi/bin/rotate.py "
                          "ack --help"}},
              {"type": "tool_use", "name": "Bash",
               "input": {"command": "git status -sb"}}]
    tr = graph / "help.jsonl"
    tr.write_text(_events(blocks), encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert len(calls) == 2
    assert counts["window_reason"] == "first (d) at 2"



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


def _live_rotations_facts():
    """The LIVE `config:rotations` `## facts` section from this worktree's
    graph (never a copied list — a test of live config reads the live node).
    Returns None when the node is not resolvable, so the caller can skip."""
    root = Path(__file__).resolve().parents[3]  # the worktree root
    rot = root / ".agi" / "nodes" / ".geometry" / "rotations.md"
    if not rot.exists():
        return None
    text = rot.read_text(encoding="utf-8")
    return text.split("## facts", 1)[1] if "## facts" in text else text


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
        assert _cats(counts) == {"a": 0, "b": 1, "c": 0, "d": 0, "s": 0}

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
        assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert counts["window_reason"] == "transcript end"
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
        assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert counts["window_reason"] == "transcript end"
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
        assert _cats(counts) == {"a": 0, "b": 0, "c": 0, "d": 1, "s": 0}
        assert counts["window_reason"] == "first (d) at 1"
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
        assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert counts["window_reason"] == "transcript end"
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
        assert _cats(counts) == {"a": 0, "b": 0, "c": 0, "d": 1, "s": 0}
        assert counts["window_reason"] == "first (d) at 1"
        assert calls[0]["cmd"] == "true"
        assert calls[0]["source"].endswith("20260911T100000Z.json")

# ── SL1.08 build-order items (hypothesis:l4-the-audit-classifier-is-derived-
# ── and-the-window-is-bounded-by-the-record): eight RED-FIRST fixes pinned by
# ── name here — prescribed facts, whois prefix, docstring, dead copy, greedy
# ── sed regex, derived hand-read paths, and grep-target protocol learning ────

def _out_record(graph, ts="20260911T150000Z"):
    """A synthetic OUT rotation record (for _latest_record items)."""
    rec = {"rotation": "rotate-self", "seat": SEAT,
           "recorded_at": ts + "Z", "result": "success",
           "observations": {"b_generation": {"before": 13, "after": 14}}}
    path = graph / "sessions" / "rotations" / f"{SEAT}.{ts}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return path


class TestSLO8PrescribedFacts:
    def test_item1_prescribed_fact_ack_call_is_never_category_a(self):
        # F8 PRESCRIBES the required wake act (the ack); a call PERFORMING it
        # is work (b via the covered after_join ack / d), never (a, F8).
        facts = sensei._parse_facts(
            "- F8 (your ONE required wake act): `python3 extensions/agi/bin/"
            "rotate.py ack --seat <seat> --gen <N> --ref <ref> continue`\n")
        assert facts == [("F8", [])]  # the prescribed shape is dropped
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py ack --seat sanctuary-director "
            "--gen 14 --ref fbb88c continue", "Bash", SEAT, [], facts)
        # pin the actual landing: (s, "ack") — L4.251 (master-sensei proposal
        # (e), hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-
        # record) made a hand-redone after_join step SERVICE-OWED, checked
        # before the by-hand-read clause ever runs. Re-pinned at the L4.251
        # harvest (sanctuary-helper, 2026-09-11): SL1.08 pinned (b, None), the
        # landing before that round. The invariant this test guards is
        # unchanged: the prescribed fact's shapes are dropped so no (a) is
        # reachable. Never (a).
        assert cat != "a"
        assert cat == "s" and label == "ack"

    def test_item2b_prescribe_re_all_alternatives_fire_without_reserved_words(self):
        # the escaped `\\s`/`\\w` branches (`your one ... act`,
        # `one ... decision`) used to be dead regex; each must now mark a fact
        # prescribed with a sentence that contains NO required/mandatory word.
        prescribed = [
            "your one big act is to ack the rotation",  # your one \w+ act
            "make one final decision here",             # one \w+ decision
            "you must perform the handoff",             # must perform
            "minimum wake is a single call",            # minimum wake
        ]
        for prose in prescribed:
            facts = sensei._parse_facts(f"- F8 ({prose}): `python3 x.py run`\n")
            assert facts == [("F8", [])], prose
        # a plain measured fact is NOT prescribed: its shape is kept
        facts = sensei._parse_facts("- F1 (one call proves it): `ps`\n")
        assert facts == [("F1", ["ps"])]


    def test_item1_prescribed_fact_flag_keeps_re_derivable_facts(self):
        # a MEASURED fact (F1) is still re-derivable (a); only prescribed acts drop
        facts = sensei._parse_facts(
            "- F1 (ONE call proves it): `python3 extensions/agi/bin/rotate.py "
            "status --seat <seat> --record latest`\n"
            "- F8 (required wake act): `python3 extensions/agi/bin/rotate.py "
            "ack --seat <seat> --gen <N> --ref <ref> continue`\n")
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/rotate.py status --seat "
            "sanctuary-director --record latest", "Bash", SEAT, [], facts)
        assert cat == "a"
        assert label == "F1"


class TestSLO8WhosPrefix:
    def test_item2_live_f2_whois_rederive_is_category_a_with_live_facts(self):
        # a test of LIVE config reads the live node, never a copied list: ONE
        # live fact cites the multi-token shape `send.py whois <token>` WITHOUT
        # the invocation prefix (F2 until the 2026-09-13 compaction folded it
        # into F3 — the NUMBER is incidental, the shape is the contract), and a
        # fact whose PROSE says `whois` ("`whois` matches by prefix on it") must
        # not shadow it — so the live whois re-derive lands on (a, <the fact
        # carrying the shape>), never on the prose one (goal:g15.13 / item 2).
        live = _live_rotations_facts()
        if live is None:
            pytest.skip("live config:rotations not resolvable from this test")
        facts = sensei._parse_facts(live)
        carriers = sorted({lab for lab, shapes in facts
                           if any(sh.startswith("send.py whois") for sh in shapes)})
        assert len(carriers) == 1, (
            f"exactly one live fact must cite `send.py whois <token>`: {carriers}")
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/send.py whois 8.8.8.8",
            "Bash", SEAT, [], facts)
        assert cat == "a"
        assert label == carriers[0]

    def test_item2_bare_verb_fact_shape_matches_a_live_call_carrying_launch_prefix(self):
        # a fact whose cited shape is the BARE verb (`whois`) must match a live
        # re-derive that carries the invocation prefix (`python3 …/send.py whois`)
        facts = sensei._parse_facts("- F2 (by hand): `whois`\n")
        cat, label = sensei.classify_call(
            "python3 extensions/agi/bin/send.py whois 8.8.8.8",
            "Bash", SEAT, [], facts)
        assert cat == "a"
        assert label == "F2"

    def test_item2_bare_verb_is_not_a_filter_arg(self):
        # `grep whois file` is a search OVER output, not a re-derive of the
        # whois fact — the bare verb must not match as another verb's argument.
        facts = sensei._parse_facts("- F2: `whois`\n")
        cat, _ = sensei.classify_call("grep whois /tmp/x", "Bash", SEAT, [], facts)
        assert cat != "a"


class TestSLO8MiscFixes:
    def test_item3_read_rotations_docstring_matches_behaviour(self):
        doc = sensei._read_rotations.__doc__ or ""
        # the stale claim (facts body "used for text mentions only") is gone
        assert "text mentions only" not in doc
        # and the docstring now describes the re-derive + prescribed skip
        assert "prescribed" in doc and "re-derive" in doc

    def test_item4_latest_record_has_no_dead_list_copy(self, tmp_path):
        # behavioural pin of `_latest_record`: resolves the latest record and
        # a given gen — the dead `matches = [f for f in files]` copy is gone
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        _write_rotation_record(graph, "20260911T100000Z", gen=13)
        _write_rotation_record(graph, "20260911T110000Z", gen=14)
        latest = sensei._latest_record(graph, SEAT)
        assert latest is not None and latest[0].name.endswith("20260911T110000Z.json")
        g14 = sensei._latest_record(graph, SEAT, gen=14)
        assert g14 is not None and g14[0].name.endswith("20260911T110000Z.json")
        assert sensei._latest_record(graph, SEAT, gen=12) is None

    def test_item5_sed_read_piped_grep_i_is_learning_not_an_inplace_edit(self):
        # `-i` after the pipe belongs to grep, NOT sed; the read-only sed of a
        # source file keeps its protocol-learning verdict (c).
        assert sensei._is_protocol_learning(
            "sed -n 1,40p extensions/agi/bin/write.py | grep -i '^def '",
            "Bash") is True

    def test_item5_minus_i_after_pipe_is_not_seds_inplace_flag(self):
        # sed's OWN -i stays split off: `sed 's/x/y/' f && grep -i foo` has NO
        # sed in-place flag (sed writes stdout; grep owns the -i), so the
        # in-place exemption must not swallow it / mislabel it a source edit.
        assert sensei._is_protocol_learning(
            "sed 's/x/y/' f && grep -i foo", "Bash") is False
        # and a genuine sed -i IS a source edit (real work, not learning)
        assert sensei._is_protocol_learning(
            "sed -i 's/a/b/' extensions/agi/bin/sensei.py", "Bash") is False

    def test_item8_grep_on_pipeline_output_is_not_protocol_learning(self):
        # grep feeding on a piped OUTPUT (its own quoted pattern mentions
        # nothing source-like here; the `.py` is a filter verb, not a path) is
        # a hand read of the seat's inbox (b), not a source/log grep (c): the
        # `send.py read` is the inbox first_turn a template already covers.
        cmd = ("date -u; python3 extensions/agi/bin/send.py read "
               "sanctuary-director | grep -vE '\\.py$'")
        cat, _ = sensei.classify_call(cmd, "Bash", SEAT, _ft_entries())
        assert cat == "b"



class TestSLO8DerivedHandReadPaths:
    def test_item6_hand_read_paths_are_derived_not_literal(self, tmp_path):
        entries = _ft_entries()
        facts = sensei._parse_facts(
            "- F2: the seat registry; `grep \"name\": \"<seat>\" "
            ".agi/nodes/.geometry/seats.md`\n")
        signals = sensei._hand_read_paths(entries, facts, SEAT)
        # a path the CONFIG derives (the registry read cited by F2) is hand-read
        assert sensei._path_is_hand_read(
            ".agi/nodes/.geometry/seats.md", signals) is True
        # a path nothing configures is real work
        assert sensei._path_is_hand_read("docs/architecture.md", signals) is False
        # the old literal file list is NOT hard-coded on the function
        assert not hasattr(sensei, "_PATH_IS_HAND_READ_LIST")
        # the seat's OWN record / ack / pin / bootstrap paths are DERIVED from
        # the seat identity + sessions layout — the bare generic substrings are
        # gone, and a path NOT derivable from this seat/config is real work (d)
        assert sensei._path_is_hand_read(
            f"sessions/rotations/{SEAT}.20260911T120000Z.json", signals) is True
        assert sensei._path_is_hand_read(
            f"sessions/seats/{SEAT}.ack.json", signals) is True
        assert sensei._path_is_hand_read(
            f"sessions/seats/{SEAT}.bootstrap.json", signals) is True
        assert sensei._path_is_hand_read(
            f"sessions/{SEAT}.meter", signals) is True
        # …and another seat's (or a bare, seat-less) file is NOT a by-hand read
        assert sensei._path_is_hand_read(
            "sessions/rotations/other-seat.json", signals) is False
        assert sensei._path_is_hand_read(
            "sessions/other-seat.meter", signals) is False
        assert sensei._path_is_hand_read(
            "seats/other-seat.ack.json", signals) is False

    def test_item6_wake_audit_derives_hand_read_for_nonbash(self, tmp_path):
        # end-to-end: a Read of the derived registry path is (b); a custom file
        # that no first_turn/fact/seat path covers is real work (d)
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        block = {"type": "tool_use", "name": "Read",
                 "input": {"path": ".agi/nodes/.geometry/seats.md"}}
        tr = graph / "d.jsonl"
        tr.write_text(_events([block]) + _events(
            [{"type": "tool_use", "name": "Read",
              "input": {"path": "docs/architecture.md"}}]), encoding="utf-8")
        code, calls, _ = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert [c["cat"] for c in calls] == ["b", "d"]
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
            "ls -la /srv/agi/.agi/sessions/rotations | tail -5",
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
            ("Bash", "ls -la /srv/agi/.agi/sessions/rotations "
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
        # counts also carries window_reason (SL3.03) — compare the buckets
        assert _cats(counts) == {"a": 0, "b": 2, "c": 0, "d": 1, "s": 2}
        assert counts["window_reason"] == "ack call 1, first (d) at 5"
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


class TestSessionKeyedWakeAudit:
    """hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-
    prime-ack-name: a non-prime post's record and ack are keyed on the
    `session_id` its row carries (rotate._ack_session_id / rotate._ack_path,
    landed 1c7072101), never on a generation and never on the Prime
    `.ack.json` name."""

    def test_record_selected_by_row_session_not_latest(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid_a = "aaaaaaaa-1111-2222-3333-444444444444"
        sid_b = "bbbbbbbb-1111-2222-3333-444444444444"
        tr_a = graph / "sess_a.jsonl"
        tr_a.write_text(_events([{"type": "tool_use", "name": "Bash",
                                 "input": {"command": "whois 8.8.8.8"}}]),
                        encoding="utf-8")
        tr_b = graph / "sess_b.jsonl"
        tr_b.write_text(_events([{"type": "tool_use", "name": "Bash",
                                 "input": {"command": "true"}}]),
                        encoding="utf-8")
        # the row names session A, and A's record is the OLDER one -- so a
        # "latest record" rule and a "session" rule disagree by construction.
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid_a})
        _write_rotation_record(graph, "20260911T100000Z", join_transcript=tr_a,
                               session_id=sid_a, ts="20260911T100000Z")
        _write_rotation_record(graph, "20260911T110000Z", join_transcript=tr_b,
                               session_id=sid_b, ts="20260911T110000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        # session A's transcript (a whois -> F2 re-derive), NOT B's (`true`)
        assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
        assert calls[0]["label"] == "F2"
        assert calls[0]["source"].endswith("20260911T100000Z.json")

    def test_two_session_keyed_acks_selects_the_matching_session(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid_a = "aaaaaaaa-1111-2222-3333-444444444444"
        sid_b = "bbbbbbbb-1111-2222-3333-444444444444"
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid_a})
        seats = graph / "sessions" / "seats"
        seats.mkdir(parents=True, exist_ok=True)
        own_ack = seats / f"{SEAT}.ack.{sid_a[:8]}.json"
        other_ack = seats / f"{SEAT}.ack.{sid_b[:8]}.json"
        own_ack.write_text("{}\n", encoding="utf-8")
        other_ack.write_text("{}\n", encoding="utf-8")
        tr = graph / "ack_reads.jsonl"
        tr.write_text(_events([
            {"type": "tool_use", "name": "Read",
             "input": {"path": str(own_ack)}},
            {"type": "tool_use", "name": "Read",
             "input": {"path": str(other_ack)}},
        ]), encoding="utf-8")
        # explicit transcript: this conjunct is exactly the ack SIGNAL set.
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
        assert code == 0
        assert calls[0]["cat"] == "b"      # the row's OWN session-keyed ack
        assert calls[1]["cat"] == "d"      # the OTHER session's ack is not

    def test_prime_legacy_ack_and_latest_record_unchanged(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        _set_seat_row(graph, {"name": SEAT, "role": "prime_director",
                              "tier": 0})
        legacy = graph / "sessions" / "seats" / f"{SEAT}.ack.json"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text("{}\n", encoding="utf-8")
        tr = graph / "prime.jsonl"
        tr.write_text(_events([{"type": "tool_use", "name": "Read",
                                "input": {"path": str(legacy)}}]),
                      encoding="utf-8")
        older = graph / "prime_old.jsonl"
        older.write_text(_events([{"type": "tool_use", "name": "Bash",
                                   "input": {"command": "true"}}]),
                         encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", join_transcript=older,
                               gen=12, ts="20260911T100000Z")
        _write_rotation_record(graph, "20260911T110000Z", join_transcript=tr,
                               gen=13, ts="20260911T110000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert calls[0]["cat"] == "b"      # the legacy Prime `.ack.json`
        assert calls[0]["source"].endswith("20260911T110000Z.json")  # latest
        paths = sensei._hand_read_paths([], [], SEAT, "")
        assert f"seats/{SEAT}.ack.json" in paths

    def test_nonprime_row_without_session_id_falls_back(self, tmp_path):
        graph, _ = _write_root(tmp_path, [("Bash", "true")])  # row: no session_id
        old_tr = graph / "nb_old.jsonl"
        old_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                    "input": {"command": "true"}}]),
                          encoding="utf-8")
        new_tr = graph / "nb_new.jsonl"
        new_tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                    "input": {"command": "whois 1.1.1.1"}}]),
                          encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", join_transcript=old_tr,
                               gen=12, ts="20260911T100000Z")
        _write_rotation_record(graph, "20260911T110000Z", join_transcript=new_tr,
                               gen=13, ts="20260911T110000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert calls[0]["label"] == "F2"     # the LATEST record, as before
        assert calls[0]["source"].endswith("20260911T110000Z.json")
        # the documented fallback is the legacy name, never a silent re-key
        paths = sensei._hand_read_paths([], [], SEAT, "")
        assert f"seats/{SEAT}.ack.json" in paths
        assert len([p for p in paths if p.startswith(f"seats/{SEAT}.ack.")]) == 1

    def test_record_selected_by_top_level_session_id(self, tmp_path):
        # clause (2): rotate.py writes the session id in TWO places -- the
        # record TOP level (rotate.py:4702-4703) for a first-seating record,
        # and handover.join for a rotate-self record. The matcher must read
        # BOTH, mirroring rotate._record_join, or a first-seating record is
        # invisible and the audit refuses the very session it was given.
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid = "aaaa1111-2222-3333-4444-555566667777"
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid})
        tr = graph / "top_only.jsonl"
        tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                "input": {"command": "whois 9.9.9.9"}}]),
                      encoding="utf-8")
        rec_path = _write_rotation_record(graph, "20260911T100000Z",
                                          join_transcript=tr,
                                          ts="20260911T100000Z",
                                          top_session_id=sid)
        # the fixture really is top-level-only: handover.join carries no id
        doc = json.loads(rec_path.read_text(encoding="utf-8"))
        assert doc["session_id"] == sid
        assert "session_id" not in doc["handover"]["join"]
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        assert calls[0]["label"] == "F2"
        assert calls[0]["source"].endswith("20260911T100000Z.json")

    def test_only_another_sessions_record_refuses_by_name(self, tmp_path,
                                                         capsys):
        # P1 (auth, committed from /tmp/probe_sl7124_parent.py): the row names
        # session A; the ONLY record on disk belongs to session B. The audit
        # must refuse BY NAME (listing the session), never silently fall back
        # to "latest" -- which is exactly what a half-fix does.
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid_a = "aaaaaaaa-1111-2222-3333-444444444444"
        sid_b = "bbbbbbbb-1111-2222-3333-444444444444"
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid_a})
        tr_b = graph / "only_b.jsonl"
        tr_b.write_text(_events([{"type": "tool_use", "name": "Bash",
                                  "input": {"command": "true"}}]),
                        encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z",
                               join_transcript=tr_b, session_id=sid_b,
                               ts="20260911T100000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        err = capsys.readouterr().err
        assert code == 2
        assert calls == []
        assert sid_a[:8] in err and "session" in err

    def test_prime_row_with_session_id_stays_on_latest_and_legacy_ack(
            self, tmp_path):
        # P3 (auth, committed from /tmp/probe_sl7124_parent.py): a PRIME row
        # carrying a session_id ANYWAY stays on the latest-record /
        # legacy `.ack.json` arm. rotate._ack_session_id is "" for a prime
        # seat, so the legacy read is (b), the session-keyed read is (d), and
        # _hand_read_paths("") carries no session-keyed signal.
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid = "cccccccc-1111-2222-3333-444444444444"
        _set_seat_row(graph, {"name": SEAT, "role": "prime_director",
                              "tier": 0, "session_id": sid})
        seats = graph / "sessions" / "seats"
        seats.mkdir(parents=True, exist_ok=True)
        legacy = seats / f"{SEAT}.ack.json"
        legacy.write_text("{}\n", encoding="utf-8")
        keyed = seats / f"{SEAT}.ack.{sid[:8]}.json"
        keyed.write_text("{}\n", encoding="utf-8")
        assert rotate._ack_session_id(graph, SEAT) == ""
        old = graph / "prime_old.jsonl"
        old.write_text(_events([{"type": "tool_use", "name": "Bash",
                                 "input": {"command": "true"}}]),
                       encoding="utf-8")
        new = graph / "prime_new.jsonl"
        new.write_text(_events([
            {"type": "tool_use", "name": "Read",
             "input": {"path": str(legacy)}},
            {"type": "tool_use", "name": "Read",
             "input": {"path": str(keyed)}},
        ]), encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", join_transcript=old,
                               gen=12, ts="20260911T100000Z")
        _write_rotation_record(graph, "20260911T110000Z", join_transcript=new,
                               gen=13, ts="20260911T110000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
        assert code == 0
        # the LATEST record (no session selection for a prime)
        assert calls[0]["source"].endswith("20260911T110000Z.json")
        # legacy `.ack.json` by hand -> (b); the session-keyed name -> (d)
        assert [c["cat"] for c in calls] == ["b", "d"]
        paths = sensei._hand_read_paths([], [], SEAT, "")
        assert f"seats/{SEAT}.ack.json" in paths
        assert f"seats/{SEAT}.ack.{sid[:8]}.json" not in paths

    def test_hand_read_paths_adds_session_keyed_ack_only_when_given(self):
        plain = sensei._hand_read_paths([], [], SEAT, "")
        assert f"seats/{SEAT}.ack.json" in plain
        keyed = sensei._hand_read_paths([], [], SEAT, "abcdef1234567890")
        assert f"seats/{SEAT}.ack.abcdef12.json" in keyed
        assert f"seats/{SEAT}.ack.json" in keyed


# ── direct unit tests for the two record readers (hypothesis:l4-record-
# ── transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-
# ── level-session-id): the top-level `transcript_path` a FIRST-SEATING
# ── record carries must resolve, with `handover.join.transcript` still
# ── winning when present, and `_record_matches_session` must mirror
# ── `rotate._record_join`'s top-level-then-join-overwrites precedence.

class TestRecordTranscriptDirect:
    def test_top_level_transcript_path_alone_resolves(self):
        # the first-seating shape (rotate.py _seating_record): the ONLY
        # spelling such a record carries.
        assert sensei._record_transcript(
            {"transcript_path": "/tmp/seat.jsonl"}) == Path("/tmp/seat.jsonl")

    def test_join_transcript_wins_over_top_level_transcript_path(self):
        # both spellings present -> the join spelling, exactly as
        # rotate._record_join lets handover.join.* overwrite the top level.
        assert sensei._record_transcript({
            "transcript_path": "/tmp/top.jsonl",
            "handover": {"join": {"transcript": "/tmp/join.jsonl"}},
        }) == Path("/tmp/join.jsonl")

    def test_join_transcript_alone_still_resolves(self):
        assert sensei._record_transcript({
            "handover": {"join": {"transcript": "/tmp/join.jsonl"}},
        }) == Path("/tmp/join.jsonl")

    def test_session_log_still_wins_over_top_level_transcript_path(self):
        # no regression: the pre-existing reads keep their order.
        assert sensei._record_transcript({
            "session_log": "/tmp/log.jsonl",
            "transcript_path": "/tmp/top.jsonl",
        }) == Path("/tmp/log.jsonl")

    def test_c_readback_log_path_is_jsonl_only(self):
        assert sensei._record_transcript(
            {"observations": {"c_readback_log_path": "/tmp/dbg.log"}}) is None
        assert sensei._record_transcript(
            {"observations": {"c_readback_log_path": "/tmp/dbg.jsonl"}}) \
            == Path("/tmp/dbg.jsonl")

    def test_record_with_none_of_the_keys_returns_none(self):
        assert sensei._record_transcript({}) is None
        assert sensei._record_transcript({"transcript_path": ""}) is None


class TestRecordMatchesSessionDirect:
    A = "aaaaaaaa-1111-2222-3333-444444444444"
    B = "bbbbbbbb-1111-2222-3333-444444444444"

    def test_join_session_id_wins_over_top_level_session_id(self):
        # rotate._record_join's rule: top level first, handover.join wins.
        rec = {"session_id": self.A,
               "handover": {"join": {"session_id": self.B}}}
        assert sensei._record_matches_session(rec, self.B) is True
        assert sensei._record_matches_session(rec, self.A) is False

    def test_top_level_session_id_alone_still_matches(self):
        # the first-seating shape; no regression.
        assert sensei._record_matches_session(
            {"session_id": self.A}, self.A) is True

    def test_empty_caller_id_matches_nothing(self):
        assert sensei._record_matches_session({"session_id": self.A}, "") \
            is False

    def test_record_with_neither_spelling_matches_nothing(self):
        assert sensei._record_matches_session({}, self.A) is False
        assert sensei._record_matches_session(
            {"handover": {"join": {}}}, self.A) is False

    def test_full_id_matches_its_eight_char_prefix_and_not_seven(self):
        rec = {"session_id": self.A}
        assert sensei._record_matches_session(rec, self.A[:8]) is True
        assert sensei._record_matches_session(rec, self.A[:7]) is False


def test_wake_audit_reads_a_seating_only_records_top_level_transcript(
        tmp_path):
    # wire probe for the changed bytes: a FIRST-SEATING record carries ONLY
    # the top-level `transcript_path` (no session_log, no handover.join), and
    # the audit must audit it rather than refuse "names no transcript".
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    tr = graph / "seating.jsonl"
    tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                            "input": {"command": "whois 1.1.1.1"}}]),
                  encoding="utf-8")
    d = graph / "sessions" / "rotations"
    d.mkdir(parents=True, exist_ok=True)
    sid = "dddddddd-1111-2222-3333-444444444444"
    (d / f"{SEAT}.20260911T160000Z.seating.json").write_text(json.dumps({
        "rotation": "first-seating", "seat": SEAT, "session_id": sid,
        "transcript_path": str(tr),
        "recorded_at": "20260911T160000Z",
    }, indent=2) + "\n", encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, None)
    assert code == 0, counts
    assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
    assert calls[0]["label"] == "F2"
    assert calls[0]["source"].endswith(".seating.json")


def test_wake_audit_help_exits_zero():
    # `sensei.py wake-audit -h` must exit 0 (argparse -h); the --redact flag
    # is part of that surface.
    try:
        sensei.main(["wake-audit", "-h"])
    except SystemExit as e:
        assert e.code == 0
    else:
        raise AssertionError("argparse -h should have raised SystemExit(0)")


# ── clause (3): `--record latest` passes the session gate ──────────────────
# hypothesis:l4-the-sensei-record-selector-refuses-ambiguous-stamps-by-name-
# and-latest-passes-the-session-gate: `--record latest` used to return BEFORE
# `_select_rotation_record`'s session gate, so a wake audit on a post whose
# newest on-disk record belonged to ANOTHER session audited it and exited 0.
# `latest` is the default spelled out loud, so it must take the SAME gate the
# no-flag default does.

class TestRecordLatestPassesTheSessionGate:
    def test_record_latest_refuses_when_latest_is_another_session(
            self, tmp_path, capsys):
        """FALSIFIER F2: the only record on disk carries session B while the
        row names session A; `--record latest` must refuse BY NAME like the
        no-flag default, never audit B's wake."""
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid_a = "aaaaaaaa-1111-2222-3333-444444444444"
        sid_b = "bbbbbbbb-1111-2222-3333-444444444444"
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid_a})
        tr_b = graph / "latest_b.jsonl"
        tr_b.write_text(_events([{"type": "tool_use", "name": "Bash",
                                  "input": {"command": "true"}}]),
                        encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z",
                               join_transcript=tr_b, session_id=sid_b,
                               ts="20260911T100000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None,
                                                record="latest")
        assert code == 2
        assert calls == [] and counts == {}
        assert sid_a[:8] in capsys.readouterr().err

    def test_record_latest_still_resolves_when_the_session_matches(
            self, tmp_path):
        """The gate is an identity gate, not a refusal of `latest`: a record
        carrying the row's own session still resolves."""
        graph, _ = _write_root(tmp_path, [("Bash", "true")])
        sid = "aaaaaaaa-1111-2222-3333-444444444444"
        _set_seat_row(graph, {"name": SEAT, "role": "director", "tier": 1,
                              "session_id": sid})
        tr = graph / "latest_ok.jsonl"
        tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                                "input": {"command": "whois 1.1.1.1"}}]),
                      encoding="utf-8")
        _write_rotation_record(graph, "20260911T100000Z", join_transcript=tr,
                               session_id=sid, ts="20260911T100000Z")
        code, calls, counts = sensei.wake_audit(graph, SEAT, None, None,
                                                record="latest")
        assert code == 0
        assert calls[0]["label"] == "F2"


# ── the record is resolved ONCE, by the audit, not again by the CLI ───────

def test_wake_audit_resolves_the_rotation_record_once(tmp_path, monkeypatch,
                                                      capsys):
    """`cmd_wake_audit` used to re-run `_select_wake_record` just to print the
    header (a SECOND resolution that could drift from the window's). The
    audit resolves the record once and hands the CLI the stamp."""
    from types import SimpleNamespace
    graph, _ = _write_root(tmp_path, [("Bash", "true")])
    tr = graph / "once.jsonl"
    tr.write_text(_events([{"type": "tool_use", "name": "Bash",
                            "input": {"command": "whois 1.1.1.1"}}]),
                  encoding="utf-8")
    _write_rotation_record(graph, "20260911T120000Z", join_transcript=tr)
    real = sensei._select_wake_record
    seen = []

    def counting(*a, **k):
        seen.append(a)
        return real(*a, **k)

    monkeypatch.setattr(sensei, "_select_wake_record", counting)
    args = SimpleNamespace(seat=SEAT, gen=None, transcript=None, record=None,
                           redact=True)
    assert sensei.cmd_wake_audit(graph, args) == 0
    out = capsys.readouterr().out
    assert "--record 20260911T120000Z (role director)" in out
    assert len(seen) == 1, f"record resolved {len(seen)} times, want 1"


# ── conjuncts 2, 3, 5 (hypothesis:l4-the-sensei-classifier-…): a nudge read
# ── is service-owed (s); an audit/commit verb ANYWHERE is real work (d),
# ── never a by-hand read; and the wake window ends at the first real input.


def _wake_blocks(*blocks):
    """Serialize tool_use + user-turn blocks into a CC JSONL transcript
    string (an assistant tool_use or a plain-string user turn)."""
    out = []
    for b in blocks:
        if isinstance(b, str):          # a plain-string user turn (nudge)
            out.append(json.dumps({"type": "user",
                                   "message": {"role": "user", "content": b}}))
        else:
            out.append(json.dumps({"type": "assistant",
                                   "message": {"role": "assistant",
                                               "content": [b]}}))
    return "\n".join(out) + "\n"


def test_wake_nudge_read_is_service_owed(tmp_path):
    # conjunct 2: a `send.py read <post>` whose immediately preceding user
    # turn is an `[agi-nudge]` is service-owed (s), never an inbox (a) act.
    # The nudge is embedded after a prefix so it ISN'T the window-ending
    # real input (conjunct 5) — isolating conjunct 2's classification rule
    # from the window boundary so the s-read stays visible inside the window.
    graph, tr = _write_root(tmp_path, [])
    tr.write_text(_wake_blocks(
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "python3 extensions/agi/bin/rotate.py status "
                  f"--seat {SEAT} --record latest"}},
        f"rotated-out [agi-nudge] unread for {SEAT}: send.py read {SEAT}",
        {"type": "tool_use", "name": "Bash",
         "input": {"command": f"python3 extensions/agi/bin/send.py read {SEAT}"}},
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "python3 -m pytest "
                  "extensions/agi/tests/test_sensei.py -q"}}),
        encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert calls[1]["cat"] == "s" and calls[1]["label"] == "nudge"


def test_wake_audit_verb_anywhere_is_d_not_b(tmp_path):
    # conjunct 3: a Bash command carrying an audit/commit verb ANYWHERE
    # (sensei.py *-audit, write.py, git commit) is real work (d), never a
    # by-hand read (b) — even behind a sleep/grep wait loop that reads a
    # rotation record.
    cmd = ("for i in $(seq 1 8); do grep -q '\"result\": \"success\"' "
           ".agi/sessions/rotations/master-sensei.json && break; sleep 15; "
           "done\n"
           "python3 extensions/agi/bin/sensei.py wake-audit --post "
           f"{SEAT}\n"
           "git commit -q -m x && python3 extensions/agi/bin/write.py "
           ".agi/nodes/x.md 'set title y'")
    graph, tr = _write_root(tmp_path, [("Bash", cmd)])
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    assert calls[0]["cat"] == "d" and calls[0]["label"] is None


def test_wake_window_ends_at_first_real_input(tmp_path):
    # conjunct 5: the wake window ends at the FIRST real input after seating
    # (an [agi-nudge]); a call ANSWERING that input is work on it, never wake,
    # even though it is only a hand read (b) not (d).
    graph, tr = _write_root(tmp_path, [])
    tr.write_text(_wake_blocks(
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "python3 extensions/agi/bin/rotate.py status "
                  f"--seat {SEAT} --record latest"}},
        f"[agi-nudge] unread for {SEAT}: kid a00-1234 died",
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "grep -H '' .agi/sessions/master-sensei.log | "
                  "tail -20"}},
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "python3 -m pytest "
                  "extensions/agi/tests/test_sensei.py -q"}}),
        encoding="utf-8")
    code, calls, counts = sensei.wake_audit(graph, SEAT, None, tr)
    assert code == 0
    # the window holds ONLY call 1 (a): the answering read (b, but work on the
    # message) is cut at the first real input, never counted as wake.
    assert len(calls) == 1 and calls[0]["cat"] == "a"
    assert counts["window_reason"] == "first real input at 2"
    assert counts["a"] == 1 and counts["b"] == 0
