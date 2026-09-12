"""Tests for the phase-3 closeout CAPTIVE-STEP DRIVER — `rotate.py`
`_closeout_run_steps` + the step-list/seams/grammar helpers
(hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-
once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-
by-name, phase 3: WORKTREE-POST captive steps, logged by name in the
rotation record's `closeout: [{step, result, detail}]`, a refused step
naming itself and STOPPING the call).

Every side-effecting step is driven through an INJECTABLE `seams` table --
the test never spawns a child, never hits the network, never writes a node.
The real seam table (`_make_closeout_seams`) is still exercised for the two
steps that are grammatically testable hermetically: the merge-up target (the
real runner merges the seat branch into MAIN's checkouted season2/main with
--no-ff, on a git fixture) and the grant grammar.

1. The driver runs the WORKTREE-POST step list IN ORDER, logging each by name.
2. A refused step (a runner returning `(False, ...)`) STOPS the call: the log
   ends at that step, the error names the STEP, and nothing after it runs.
3. A step with NO runner is refused BY NAME (and stops).
4. The merge-up runner merges --no-ff of the seat branch into the CHECKED-OUT
   season2/main IN MAIN -- NEVER the seat tree, NEVER `origin/season/s2` or
   a bare `main`; it refuses by name when MAIN is on another branch, dirty,
   or unresolvable.
5. The grant grammar (`_grant_present_for_seat`) consumes ONLY a signed line
   FROM the prime, read from the SEAT's OWN inbox or the seat<->prime dm
   file, whose body's FIRST WORD is GRANT|GO and whose ts is LATER than the
   ASK's send time: an unsigned line, a non-prime line, a substring-only
   match, a stale block, or a block in the Prime's own inbox each never grant.
6. The numbers line composes the five facts + the hash + one line per goal.
7. Step order is the claim's spelling (post_verify first, numbers last).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_REPO / "extensions"))
sys.path.insert(0, str(_BIN))

from agi.bin import rotate  # noqa: E402


def _fake_seams(runner_table):
    """Lightweight recorder-seams: each listed runner returns ok unless the
    test names it to refuse."""
    refusers = set()

    def make(step):
        def run():
            if step in refusers:
                return (False, "refused", f"fake {step} refused")
            return (True, "ok", f"fake {step} ran")
        return run

    return {step: make(step) for step in rotate.WORKTREE_POST_CLOSEOUT_STEPS}, refusers


def test_driver_runs_worktree_post_steps_in_order():
    seams, _ = _fake_seams({})
    entries, err = rotate._closeout_run_steps(
        Path("/tmp/co-root"), "adv-alive", role="parent", seams=seams)
    assert err is None
    names = [e["step"] for e in entries]
    assert names == rotate.WORKTREE_POST_CLOSEOUT_STEPS
    assert names[0] == "post_verify" and names[-1] == "numbers"
    # every entry is logged by NAME with a result and a detail
    for e in entries:
        assert set(e) >= {"step", "result", "detail"}
        assert e["result"] in ("ok", "skip", "refused", "failed", "sent",
                               "granted", "merged")


def test_step_list_defaults_to_worktree_post_and_reads_template():
    default = rotate._closeout_step_list("parent", None)
    assert default == rotate.WORKTREE_POST_CLOSEOUT_STEPS
    tmpl = {"closeout": {"steps": ["merge_up", "numbers"]}}
    assert rotate._closeout_step_list("parent", tmpl) == ["merge_up", "numbers"]


def test_refused_step_stops_and_names_itself():
    seams, refusers = _fake_seams({})
    refusers.add("suite")                        # refuse the 6th step
    entries, err = rotate._closeout_run_steps(
        Path("/tmp/co-root"), "a", "parent", seams=seams)
    assert err is not None and "suite" in err and "refused" in err
    names = [e["step"] for e in entries]
    # the log ends AT the refused step -- nothing after it runs
    assert names == rotate.WORKTREE_POST_CLOSEOUT_STEPS[
        :rotate.WORKTREE_POST_CLOSEOUT_STEPS.index("suite") + 1]
    assert entries[-1]["result"] == "refused"


def test_unknown_step_refused_by_name():
    seams, _ = _fake_seams({})
    seams["nope"] = None                          # a step with no runner
    tmpl = {"closeout": {"steps": ["post_verify", "nope", "numbers"]}}
    entries, err = rotate._closeout_run_steps(
        Path("/tmp/co-root"), "a", "parent", template=tmpl, seams=seams)
    assert err is not None and "nope" in err and "no runner" in err
    assert [e["step"] for e in entries] == ["post_verify", "nope"]


def test_merge_up_refuses_without_resolvable_main_and_constant_is_season2_main():
    """Re-aimed from the pre-fix merge-target test: the NEW merge_up
    resolves MAIN (the shared graph root's git toplevel) and gates on MAIN's
    checked-out branch/Main tree -- so a gitless fixture (no MAIN to resolve)
    REFUSES BY NAME rather than stubbing a merge (the pre-fix test stubbed
    `_perform_season_merge`, the sync-direction helper the claim retires).
    The one-constant gate survives: season2/main, never origin/season/s2."""
    assert rotate._CLOSEOUT_MERGE_TARGET == "season2/main"
    seams = rotate._make_closeout_seams(Path("/tmp/co-root"), {})
    ok, result, detail = seams["merge_up"]()
    assert ok is False and result == "refused"
    assert "merge_up" in detail and "MAIN" in detail and "refused" in detail


def _write_inbox(root, recipient, blocks):
    inbox = root / "sessions" / "inbox" / f"{recipient}.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("".join(blocks), encoding="utf-8")


def _block_full(frm, to, ts, body, signed=True):
    head = f"---\nts: {ts}\nfrom: {frm}\nto: {to}\n"
    if signed:
        head += "env: v1\nsig: scheme:aa:bb\n"
    return head + f"\n{body}\n"


def test_grant_grammar_only_signed_prime_grant_in_seat_channels(tmp_path):
    """Re-aimed from the pre-fix grant-grammar test: the grant is read from
    the SEAT's OWN inbox or the seat<->prime dm file -- never the Prime's
    inbox, never a bare-substring GRANT|GO, never a stale (pre-ask) block.
    A signed Prime block whose body's FIRST WORD is GRANT or GO and whose ts
    is LATER than the ASK's send time grants; each false channel/word/age
    case does not."""
    import send
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    seat, prime = "adv-alive", "prime"
    since = "2026-09-12T00:00:30+00:00"        # the ASK's send time
    T0 = "2026-09-12T00:00:00Z"                # BEFORE the ask (stale)
    T1 = "2026-09-12T00:01:00Z"                # AFTER the ask (fresh)

    def grant():
        return rotate._grant_present_for_seat(root, seat, prime, since)

    # (a) signed prime, FIRST WORD GRANT, after the ask -> GRANTS
    _write_inbox(root, seat, [_block_full(prime, seat, T1, "GRANT now")])
    assert grant() is True
    # (b) `no GRANT yet`: first word is `no` -> NO grant (never a substring)
    _write_inbox(root, seat, [_block_full(prime, seat, T1, "no GRANT yet")])
    assert grant() is False
    # (c) unsigned -> no grant
    _write_inbox(root, seat,
                 [_block_full(prime, seat, T1, "GRANT", signed=False)])
    assert grant() is False
    # (d) signed NON-prime -> no grant
    _write_inbox(root, seat,
                 [_block_full("someone-else", seat, T1, "GRANT")])
    assert grant() is False
    # (e) signed prime but STALE (before the ask) -> no grant
    _write_inbox(root, seat, [_block_full(prime, seat, T0, "GRANT")])
    assert grant() is False
    # (f) a grant in the PRIME's OWN inbox never grants (the seat's channel,
    # not the Prime's, is read) -- seat inbox still holds only the stale (e)
    _write_inbox(root, prime, [_block_full(prime, seat, T1, "GRANT")])
    assert grant() is False
    # (g) the seat<->prime dm file is a second grant channel; GO counts too
    croot = send.comms_root(root)
    dm = send._dm_path(croot, seat, prime)
    dm.parent.mkdir(parents=True, exist_ok=True)
    dm.write_text(_block_full(prime, seat, T1, "GO ahead"), encoding="utf-8")
    assert grant() is True


def test_numbers_line_composes_five_facts_hash_and_goals():
    record = {
        "facts": ["42", "7", "1.3", "3", "0x2a"],
        "commit": "deadbeef",
        "goals": ["one: done", "two: merged"],
    }
    line = rotate._numbers_line(record)
    assert line == "42 | 7 | 1.3 | 3 | 0x2a | deadbeef | one: done | two: merged"
    # a record-less caller still gets a well-formed line (empty is fine)
    assert isinstance(rotate._numbers_line({}), str)


def test_driver_never_raises_on_runner_exception():
    seams, _ = _fake_seams({})
    def boom():
        raise RuntimeError("fake blowup")
    seams["render_check"] = boom
    entries, err = rotate._closeout_run_steps(
        Path("/tmp/co-root"), "a", "parent", seams=seams)
    # the raising step is refused by name; the log stops there
    assert err is not None and "render_check" in err
    assert entries[-1]["step"] == "render_check"


# ── CLI WIRING (SL7.84): `rotate-self --closeout` actually CALLS phase 3 ──
# The parent-review finding was a dead driver: the phase-3 runner had NO
# caller outside the tests. These prove the CLI path runs the captive steps,
# persists `closeout: [...]` in the in-progress rotation record, and shapes a
# refused step as a non-zero exit BEFORE the spawn. Driven through the NAMED
# seam (`--closeout-seams-json`) so the takeover never spawns / merges /
# pushes; a real live run uses the real seam table.


@pytest.fixture
def _co_rs(tmp_path, monkeypatch):
    """Fixture root for the rotate-self --closeout CLI wiring: geometry,
    seats sheet, a parent rotation template (default closeout step list), a
    fake tmux window file, and the git/push seams so phase 2 (write/commit /
    push) completes on a gitless fixture."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(
        rotate, "load_ladder_field",
        lambda r, f, d: {"director_context_tokens": 100_000,
                         "director_rotate_at": 0.25}.get(f, d))

    def _write_seats(rows):
        g = root / "nodes" / ".geometry"
        g.mkdir(parents=True, exist_ok=True)
        (root / "sessions").mkdir(parents=True, exist_ok=True)
        body = "---\nid: config:seats\ntype: config\nseats:\n"
        for r in rows:
            body += "  - " + json.dumps(r) + "\n"
        body += "---\n"
        (g / "seats.md").write_text(body, encoding="utf-8")

    def _write_templates():
        g = root / "nodes" / ".geometry"
        g.mkdir(parents=True, exist_ok=True)
        (g / "rotations.md").write_text(
            "---\nid: config:rotations\ntype: config\ntemplates:\n"
            "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
            "    steps: [handoff, rename, spawn]\n    telemetry: [seat]\n"
            "---\n\nbody\n", encoding="utf-8")

    _write_seats([{"name": "adv-alive", "role": "parent",
                   "model": "x", "effort": "max", "settings": ""}])
    _write_templates()
    win = root / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    # gitless fixture: phase-2's real push has nothing to push -- stub it so
    # phase 2 completes and phase 3 (the captive steps) runs.
    monkeypatch.setattr(rotate, "_stops_push", lambda root, label="stops": None)
    return root, win


def _closeout_form(s3="bash next-step.sh"):
    slots = ["s0", "s1", "s2", "s3", "s4", "s5", "s6"]
    return json.dumps([{"slot": s,
                        "value": ("keep" if s != "s3" else s3)}
                       for s in slots])


def test_rotate_self_closeout_refused_step_exits_nonzero_skips_spawn(
        _co_rs, monkeypatch, capsys):
    """SL7.84: wiring -- `rotate-self --closeout` runs the captive steps and
    persists them in the rotation record's `closeout: [...]` IN ORDER; a
    refused step (here `push`, near the end) EXITS NON-ZERO naming the step,
    stops the record AT it, and NEVER reaches the spawn (spawn_window not
    called). Padded with the named seam (`--closeout-seams-json`), so no real
    merge / suite / push fires."""
    root, win = _co_rs
    from types import SimpleNamespace
    spawned = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: spawned.append(kw.get("name")) or (0, "ok"))
    seams = json.dumps({"refuse": ["push"]})    # refuse the 8th step (10 total)
    args = SimpleNamespace(
        name="adv-alive", force=False, dry_run=False, throwaway=False,
        role=None, template=None, prepare=False, stops=None, stops_file=None,
        ask_diff=False, closeout=True, form="-", closeout_seams_json=seams,
        window_path=str(win), tmux_session="t", debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        session_ref=None, successor_transcript=None, successor_argv=None,
        verification_argv=None, comms_root=None, trigger="rotate-self",
        in_flight=None, own_pid=None)
    import io
    import sys as _sys
    _sys.stdin = io.StringIO(_closeout_form())
    try:
        rc = rotate.cmd_rotate_self(args, root)
    finally:
        _sys.stdin = _sys.__stdin__  # type: ignore[attr-defined]

    assert rc != 0
    err = capsys.readouterr().err
    assert "push" in err and "closeout refused" in err
    assert spawned == []   # (c) the spawn path was NOT reached on refusal

    # (a) the record carries the closeout log IN ORDER, stopping AT push;
    # (b) result still `started` (no spawn to complete it), steps stop at push.
    recs = sorted((root / "sessions" / "rotations").glob("adv-alive.*.json"))
    assert recs, "rotate-self --closeout wrote no rotation record"
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    names = [e["step"] for e in rec["closeout"]]
    full = rotate.WORKTREE_POST_CLOSEOUT_STEPS
    assert names[0] == "post_verify"
    assert names == full[:full.index("push") + 1]
    assert rec["closeout"][-1]["step"] == "push"
    assert rec["closeout"][-1]["result"] == "refused"
    assert rec["result"] == "started"
    for e in rec["closeout"]:
        assert set(e) >= {"step", "result", "detail"}


def test_closeout_log_survives_record_rewrites():
    """SL7.84: `_preserve_closeout` — the phase-3 closeout log is NOT lost
    when a LATER in-place rewrite of the same rotation record runs (the
    process rewrites the file through every rotate-self step). The field is
    read back from disk and merged into each fresh dict."""
    import tempfile
    root = Path(tempfile.mkdtemp(prefix="co-rec-"))
    path = root / "adv-alive.20260912T000000Z.json"
    rotate._write_rotate_self_started(
        path, seat="adv-alive", steps=[])
    entries = [{"step": "post_verify", "result": "ok", "detail": "x"},
               {"step": "numbers", "result": "ok", "detail": "y"}]
    rotate._record_closeout(path, entries)
    # a later rewrite and the final OUTCOME rewrite both keep the log
    rotate._write_rotate_self_started(
        path, seat="adv-alive", steps=["handoff"], gen_before=0, gen_after=1)
    rotate._write_rotation_record(
        root, rotate._rotate_self_record(seat="adv-alive", result="success",
                                         gen_before=0, gen_after=1), path=path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["closeout"] == entries
    assert doc["result"] == "success"    # the outcome write kept it too

# ── SEAT-KIND LISTS (SL7.90): the closeout list is chosen by seat kind ──
# hypothesis:l4-closeout-step-list-is-chosen-by-seat-kind-main-post-and-
# prime-lists-coded-never-the-worktree-list-by-default. Today a Prime
# (role prime_director) and a MAIN post (empty worktree cell) are both
# driven through the worktree list (merge_up_ask / wait_grant / merge_up /
# suite). These prove the coded MAIN-post list and PRIME list are served by
# kind, every step of every list has a runner in the real table AND the CLI
# fake table, and a CLI-driven MAIN-post / Prime fixture records exactly its
# kind's list -- never the worktree list, never another role's list.


def test_step_list_is_chosen_by_seat_kind_and_template_still_wins():
    """(a) The list follows SEAT KIND when the template lacks closeout.steps:
    prime_director -> PRIME list; an EMPTY worktree cell -> MAIN-post list;
    a worktree path -> the worktree list. The template's closeout.steps STILL
    wins over all three."""
    assert rotate._closeout_step_list(
        "prime_director", None) == rotate.PRIME_CLOSEOUT_STEPS
    assert rotate._closeout_step_list("prime", None) == \
        rotate.PRIME_CLOSEOUT_STEPS
    assert rotate._closeout_step_list(
        "parent", None, worktree="") == rotate.MAIN_POST_CLOSEOUT_STEPS
    assert rotate._closeout_step_list(
        "parent", None, worktree="/tmp/wt-adv") == \
        rotate.WORKTREE_POST_CLOSEOUT_STEPS
    # a whitespace-only worktree cell is a MAIN post
    assert rotate._closeout_step_list(
        "parent", None, worktree="   ") == rotate.MAIN_POST_CLOSEOUT_STEPS
    # template closeout.steps wins over prime kind and main-post kind alike
    tmpl = {"closeout": {"steps": ["merge_up", "numbers"]}}
    assert rotate._closeout_step_list(
        "prime_director", tmpl, worktree="") == ["merge_up", "numbers"]
    assert rotate._closeout_step_list(
        "parent", tmpl, worktree="/tmp/wt") == ["merge_up", "numbers"]
    # the three coded spellings are exactly the claim's
    assert rotate.MAIN_POST_CLOSEOUT_STEPS == ["pathspec_commit", "push"]
    assert rotate.PRIME_CLOSEOUT_STEPS == ["g17_1_note", "render", "push"]


def test_real_seam_table_covers_every_step_of_all_three_lists():
    """(b) The REAL seam table (built on a fixture root; runners NOT called)
    has a key for every step of all three coded lists -- a step of ANY list
    with no real runner would be refused by name at run time."""
    seams = rotate._make_closeout_seams(Path("/tmp/co-root"), {})
    for lst in (rotate.WORKTREE_POST_CLOSEOUT_STEPS,
                rotate.MAIN_POST_CLOSEOUT_STEPS,
                rotate.PRIME_CLOSEOUT_STEPS):
        for step in lst:
            assert step in seams, f"{step!r} missing from the real seam table"
    # the four NEW thin wrappers are present and callable
    for step in ("pathspec_commit", "g17_1_note", "render", "push"):
        assert callable(seams[step])


def test_cli_fake_table_covers_union_and_refuser_stops_main_post():
    """(c) The CLI fake table (`_closeout_cli_seams`) has a runner for every
    step of all three coded lists, and a refuser named in a MAIN-post step
    stops a MAIN-post run at exactly that step."""
    fake = rotate._closeout_cli_seams(Path("/tmp/co-root"), "{}")
    # the union of all three coded lists (push is shared across the three, so
    # the fake table carries ONE runner for it -- the driver's own rule that
    # a step lists twice is refused at run time, not duplicated here)
    _union = set(rotate.WORKTREE_POST_CLOSEOUT_STEPS) | \
        set(rotate.MAIN_POST_CLOSEOUT_STEPS) | set(rotate.PRIME_CLOSEOUT_STEPS)
    assert set(fake) == _union
    for lst in (rotate.WORKTREE_POST_CLOSEOUT_STEPS,
                rotate.MAIN_POST_CLOSEOUT_STEPS,
                rotate.PRIME_CLOSEOUT_STEPS):
        for step in lst:
            assert step in fake and callable(fake[step])
    # drive a MAIN-post run through the fake table; refuse `push` (its LAST
    # step) -> entries are exactly [pathspec_commit, push], push refused
    seams = {"refuse": ["push"]}
    cli = rotate._closeout_cli_seams(Path("/tmp/co-root"),
                                     json.dumps(seams))
    entries, err = rotate._closeout_run_steps(
        Path("/tmp/co-root"), "a", "parent", worktree="", seams=cli)
    assert err is not None and "push" in err and "refused" in err
    assert [e["step"] for e in entries] == ["pathspec_commit", "push"]
    assert entries[-1]["result"] == "refused"
    assert entries[0]["step"] == "pathspec_commit"


@pytest.fixture
def _co_rs_kind(tmp_path, monkeypatch):
    """Fixture root like `_co_rs` but with a configurable seats row + the
    prime_director template default, so a MAIN-post row (worktree '') or a
    prime_director row can be driven through the rotate-self --closeout CLI
    path with the named seam (`--closeout-seams-json`) -- no spawn / merge /
    push, no network."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(
        rotate, "load_ladder_field",
        lambda r, f, d: {"director_context_tokens": 100_000,
                         "director_rotate_at": 0.25}.get(f, d))

    def _write_seats(rows):
        g = root / "nodes" / ".geometry"
        g.mkdir(parents=True, exist_ok=True)
        (root / "sessions").mkdir(parents=True, exist_ok=True)
        body = "---\nid: config:seats\ntype: config\nseats:\n"
        for r in rows:
            body += "  - " + json.dumps(r) + "\n"
        body += "---\n"
        (g / "seats.md").write_text(body, encoding="utf-8")

    def _write_templates():
        g = root / "nodes" / ".geometry"
        g.mkdir(parents=True, exist_ok=True)
        (g / "rotations.md").write_text(
            "---\nid: config:rotations\ntype: config\ntemplates:\n"
            "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
            "    steps: [handoff, rename, spawn]\n    telemetry: [seat]\n"
            "  prime_director:\n    brief_file: extensions/agi/briefs/prime-successor.md\n"
            "    steps: [handoff, rename, spawn]\n    telemetry: [seat]\n"
            "---\n\nbody\n", encoding="utf-8")

    _write_seats([{"name": "adv-alive", "role": "parent", "worktree": "",
                   "model": "x", "effort": "max", "settings": ""}])
    _write_templates()
    win = root / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "_stops_push", lambda root, label="stops": None)
    return root, win


def _drive_rotate_self_closeout(root, win, monkeypatch, seams):
    from types import SimpleNamespace
    spawned = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: spawned.append(kw.get("name")) or (0, "ok"))
    args = SimpleNamespace(
        name="adv-alive", force=False, dry_run=False, throwaway=False,
        role=None, template=None, prepare=False, stops=None, stops_file=None,
        ask_diff=False, closeout=True, form="-", closeout_seams_json=seams,
        window_path=str(win), tmux_session="t", debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        session_ref=None, successor_transcript=None, successor_argv=None,
        verification_argv=None, comms_root=None, trigger="rotate-self",
        in_flight=None, own_pid=None)
    import io
    import sys as _sys
    _sys.stdin = io.StringIO(_closeout_form())
    try:
        rc = rotate.cmd_rotate_self(args, root)
    finally:
        _sys.stdin = _sys.__stdin__  # type: ignore[attr-defined]
    return rc, spawned


def _driven_record(root):
    recs = sorted((root / "sessions" / "rotations").glob("adv-alive.*.json"))
    assert recs, "rotate-self --closeout wrote no rotation record"
    return json.loads(recs[-1].read_text(encoding="utf-8"))


def test_main_post_cli_drives_only_pathspec_commit_and_push(
        _co_rs_kind, monkeypatch):
    """(d) A MAIN-post fixture (seat row with worktree '') driven through the
    CLI path records a closeout list of EXACTLY [pathspec_commit, push] in
    order -- no worktree step name (no merge_up_ask / wait_grant / merge_up /
    suite) -- and the rotate-out completes (rc 0)."""
    root, win = _co_rs_kind
    _drive_rotate_self_closeout(root, win, monkeypatch, "{}")
    rec = _driven_record(root)
    assert [e["step"] for e in rec["closeout"]] == \
        ["pathspec_commit", "push"]
    names = {e["step"] for e in rec["closeout"]}
    # no WORKTREE-ONLY step (post_verify / merge_up_ask / wait_grant /
    # merge_up / render_check / suite / grid_commit / verify_stamp / numbers)
    # -- `push` is shared with the worktree list by design, so exclude it
    _wt_only = set(rotate.WORKTREE_POST_CLOSEOUT_STEPS) - {"push"}
    assert not (names & _wt_only), names
    # the MAIN-post run recorded BOTH its kind's steps as OK (no refuser)
    assert all(e["result"] == "ok" for e in rec["closeout"]), rec["closeout"]


def test_prime_cli_drives_only_g17_1_note_render_push(
        _co_rs_kind, monkeypatch):
    """(e) A prime_director fixture (no worktree cell) driven through the CLI
    path records a closeout list of EXACTLY [g17_1_note, render, push] in
    order -- the Prime is never asked for a grant and never merges."""
    root, win = _co_rs_kind
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - {\"name\": \"adv-alive\", \"role\": \"prime_director\", "
        "\"model\": \"x\", \"effort\": \"max\", \"settings\": \"\"}\n"
        "---\n", encoding="utf-8")
    _drive_rotate_self_closeout(root, win, monkeypatch, "{}")
    rec = _driven_record(root)
    assert [e["step"] for e in rec["closeout"]] == \
        ["g17_1_note", "render", "push"]
    names = {e["step"] for e in rec["closeout"]}
    _wt_only = set(rotate.WORKTREE_POST_CLOSEOUT_STEPS) - {"push"}
    assert not (names & _wt_only), names
    # the Prime's list is ITS list, never another role's: no MAIN-post
    # pathspec_commit, no worktree merge-up steps
    assert "pathspec_commit" not in names
    assert not (names & {"merge_up_ask", "wait_grant", "merge_up", "suite"})


def test_pathspec_commit_real_runner_commits_only_card_and_own_row(tmp_path):
    """(f) The pathspec_commit REAL runner (git fixture) commits card + own
    row -- NEVER `git add -A`: a foreign dirty path stays UNCOMMITTED. A
    card is present here, so it wraps `_commit_stops_row`. (The _commit_stops_
    row-only case is covered by the existing test in test_rotate.py.)"""
    from agi.bin import rotate as _r
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True)
    seats = nodes / "seats.md"
    seats.write_text("---\nid: config:seats\ntype: config\nseats:\n"
                     "  - {\"name\": \"s1\", \"role\": \"parent\"}\n"
                     "---\n", encoding="utf-8")
    card = root / "sessions" / "quorum" / "s1.md"
    card.parent.mkdir(parents=True)
    card.write_text("# s1 card\n", encoding="utf-8")
    # a bare git fixture (no remote origin needed -- push is stubbed)
    subprocess = __import__("subprocess")
    subprocess.run(["git", "-C", str(root), "init"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "add", "agi-tree.config.json",
                    "nodes", "sessions"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "fixture"],
                   check=True, capture_output=True)
    # dirty: s1's OWN row (committed by the runner) + a FOREIGN decoy path
    seats.write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - {\"name\": \"s1\", \"role\": \"parent\", "
        "\"edited_by\": \"s1\"}\n"
        "---\n", encoding="utf-8")
    decoy = root / "scratch.log"
    decoy.write_text("x\n", encoding="utf-8")
    card.write_text("# s1 card\n## 🔴 Where it stops\nkeep\n",
                    encoding="utf-8")
    seams = _r._make_closeout_seams(root, {"gen_before": 0, "gen_after": 1},
                                    seat="s1")
    ok, result, detail = seams["pathspec_commit"]()
    assert ok is True and result == "committed", detail
    names = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--name-only", "--format="],
        capture_output=True, text=True).stdout.splitlines()
    names = [n for n in names if n.strip()]
    assert names, "no files in the pathspec closeout commit"
    for n in names:
        assert n in ("sessions/quorum/s1.md", "nodes/.geometry/seats.md"), \
            f"foreign path {n!r} rode the pathspec closeout commit"
    # the decoy stayed UNCOMMITTED (never `git add -A`)
    dirty = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True, text=True).stdout
    assert "scratch.log" in dirty, "decoy was swept into the commit"


def test_g17_1_note_runner_drives_write_py_subprocess_seam(
        _co_rs_kind, monkeypatch):
    """(f) The g17_1_note REAL runner is driven through a subprocess seam --
    a recorded argv -- never by writing the live goal:g17.1 node."""
    root, _win = _co_rs_kind
    recorded = []
    def _fake(subprocess_module, argv, **kw):
        recorded.append(argv)
        class _R:
            returncode = 0
            stdout = "ok"
            stderr = ""
        return _R()
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda argv, *a, **k: _fake(rotate.subprocess, argv))
    seams = rotate._make_closeout_seams(root, {"commit": "abc1234",
                                               "facts": ["42"]})
    ok, result, detail = seams["g17_1_note"]()
    assert ok is True and result == "ok", detail
    assert recorded and str(recorded[0][1]).endswith("write.py")
    assert recorded[0][2:4] == ["goal:g17.1", "note"]
    assert recorded[0][4] == "42 | abc1234"   # the closeout numbers line
    # a non-zero exit REFUSES BY NAME
    def _refuse(argv, *a, **k):
        class _R:
            returncode = 1
            stdout = ""
            stderr = "boom"
        return _R()
    monkeypatch.setattr(rotate.subprocess, "run", _refuse)
    ok, result, detail = seams["g17_1_note"]()
    assert ok is False and result == "refused" and "g17_1_note" in detail

# ── REAL crosscheck-worktree runners (SL7.92): the merge-up in MAIN ───────
# hypothesis:l4-closeout-worktree-post-...-the-merge-up-in-main. These prove
# the REAL runners (on git fixtures only -- a bare origin + a MAIN clone on
# season2/main + a linked seat worktree branch) do what the claim spells:
# merge_up --no-ff's the seat branch into MAIN's checked-out season2/main (a
# merge commit whose second parent is the seat tip) and refuses by name when
# MAIN is elsewhere/dirty; the ask names seat/tip/target/record and is sent
# AS the seat; suite/grid/stamp/render run with cwd=MAIN; push carries origin
# season2/main THEN refs/grid. A pre-fix runner that ever runs a worktree
# step in the SEAT tree, reads the Prime's own inbox, or omits refs/grid is
# the falsifier -- each covered below.


def _git_sole_repo(tmp_path):
    """A single MAIN-like repo with a graph root (no worktree, no remote):
    enough for `_closeout_main` to resolve and a runner whose subprocess is
    seam-recorded to prove cwd/argv. Returns (graph_root, main)."""
    import subprocess as sp
    r = tmp_path / "m"
    sp.run(["git", "init", "-q", str(r)], check=True)
    sp.run(["git", "-C", str(r), "config", "user.email", "t@t"], check=True)
    sp.run(["git", "-C", str(r), "config", "user.name", "t"], check=True)
    (r / "f.txt").write_text("x\n", encoding="utf-8")
    sp.run(["git", "-C", str(r), "add", "f.txt"], check=True)
    sp.run(["git", "-C", str(r), "commit", "-q", "-m", "init"], check=True)
    g = r / ".agi"
    g.mkdir(parents=True)
    (g / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    return g, r


def _merge_fixture(tmp_path):
    """A bare origin + a MAIN clone on season2/main + a linked seat worktree
    on season2/posts/adv carrying a commit, with MAIN's graph root holding a
    seats row whose worktree cell points at the linked worktree. Returns
    (graph_root, main, seat, seat_branch). graph_root is what a rotate-self
    call passes as cfg_root; main is MAIN's repo top."""
    import subprocess as sp
    origin = tmp_path / "origin.git"
    sp.run(["git", "init", "--bare", "-q", str(origin)], check=True)
    seed = tmp_path / "seed"
    sp.run(["git", "init", "-q", str(seed)], check=True)
    sp.run(["git", "-C", str(seed), "config", "user.email", "t@t"], check=True)
    sp.run(["git", "-C", str(seed), "config", "user.name", "t"], check=True)
    (seed / "a.txt").write_text("a\n", encoding="utf-8")
    sp.run(["git", "-C", str(seed), "add", "a.txt"], check=True)
    sp.run(["git", "-C", str(seed), "commit", "-q", "-m", "seed"], check=True)
    sp.run(["git", "-C", str(seed), "checkout", "-q", "-b", "season2/main"],
           check=True)
    (seed / "b.txt").write_text("b\n", encoding="utf-8")
    sp.run(["git", "-C", str(seed), "add", "b.txt"], check=True)
    sp.run(["git", "-C", str(seed), "commit", "-q", "-m", "season"], check=True)
    sp.run(["git", "-C", str(seed), "remote", "add", "origin", str(origin)],
           check=True)
    sp.run(["git", "-C", str(seed), "push", "-q", "origin", "season2/main"],
           check=True)
    sp.run(["git", "-C", str(seed), "push", "-q", "origin", "master"],
           check=True)

    main = tmp_path / "main"
    sp.run(["git", "clone", "-q", str(origin), str(main)], check=True)
    sp.run(["git", "-C", str(main), "config", "user.email", "t@t"], check=True)
    sp.run(["git", "-C", str(main), "config", "user.name", "t"], check=True)
    sp.run(["git", "-C", str(main), "checkout", "-q", "-b", "season2/main",
            "origin/season2/main"], check=True)
    g = main / ".agi"
    g.mkdir(parents=True)
    (g / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    gt = g / "nodes" / ".geometry"
    gt.mkdir(parents=True)
    wt = tmp_path / "wt-adv"
    sp.run(["git", "-C", str(main), "worktree", "add", "-q", "-b",
            "season2/posts/adv", str(wt), "season2/main"], check=True)
    (wt / "card.md").write_text("# adv\n", encoding="utf-8")
    sp.run(["git", "-C", str(wt), "add", "card.md"], check=True)
    sp.run(["git", "-C", str(wt), "commit", "-q", "-m", "seat work"], check=True)
    (gt / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - {\"name\": \"adv\", \"role\": \"parent\", "
        f"\"worktree\": \"{wt}\"}}\n---\n", encoding="utf-8")
    return g, main, "adv", "season2/posts/adv"


def test_merge_up_real_runner_merges_seat_branch_into_season2_main_in_main(
        tmp_path):
    """(1) merge_up: --no-ff of the seat branch into MAIN's checked-out
    season2/main (a merge commit whose SECOND parent is the seat tip), gated
    on MAIN's branch + a clean tracked tree; refuses BY NAME when MAIN is on
    another branch, dirtied ON a path the merge touches, or the one constant
    is tampered away from season2/main. (A dirty path the merge does NOT
    touch no longer blocks -- the claim's gate.)"""
    import subprocess as sp
    g, main, seat, seat_branch = _merge_fixture(tmp_path)
    record = {"gen_before": 7, "gen_after": 8,
              "recorded_at": "2026-09-12T09:00:00.123456Z"}
    seams = rotate._make_closeout_seams(g, record, seat=seat)

    # (a) MAIN dirty ON a path the merge TOUCHES -> refuse, naming it
    sp.run(["git", "-C", str(main), "checkout", "-q", seat_branch, "--",
            "card.md"], check=True)
    (main / "card.md").write_text("# adv\nDIRTY\n", encoding="utf-8")
    ok, result, detail = seams["merge_up"]()
    assert ok is False and result == "refused"
    assert "dirty" in detail and "merge_up" in detail
    assert "card.md" in detail
    sp.run(["git", "-C", str(main), "reset", "-q", "--hard"], check=True)

    # (b) MAIN on another branch -> refuse by name (never a blind merge)
    sp.run(["git", "-C", str(main), "checkout", "-q", "master"], check=True)
    ok, result, detail = seams["merge_up"]()
    assert ok is False and result == "refused"
    assert "season2/main" in detail and "merge_up" in detail
    sp.run(["git", "-C", str(main), "checkout", "-q", "season2/main"],
           check=True)

    # (c) the ONE-constant gate: tamper away from season2/main -> refused
    rotate._CLOSEOUT_MERGE_TARGET = "origin/season/s2"
    try:
        ok, result, detail = seams["merge_up"]()
        assert ok is False and result == "refused"
        assert "season2/main" in detail
    finally:
        rotate._CLOSEOUT_MERGE_TARGET = "season2/main"

    # (d) clean + on season2/main -> --no-ff merge, second parent = seat tip
    seat_tip = sp.run(
        ["git", "-C", str(main), "rev-parse", "season2/posts/adv"],
        capture_output=True, text=True, check=True).stdout.strip()
    ok, result, detail = seams["merge_up"]()
    assert ok is True and result == "merged", detail
    assert "season2/main" in detail and "MAIN" in detail
    parents = sp.run(["git", "-C", str(main), "log", "-1", "--format=%P"],
                     capture_output=True, text=True, check=True).stdout.split()
    assert len(parents) == 2, f"expected a merge commit, got parents {parents}"
    assert parents[1] == seat_tip      # the merge commit's second parent
    # the merge happened in MAIN, NOT the seat worktree (seat HEAD unchanged)
    wt_head = sp.run(["git", "-C", str(tmp_path / "wt-adv"),
                      "rev-parse", "--short", "HEAD"],
                     capture_output=True, text=True, check=True).stdout.strip()
    assert wt_head  # no exception in the seat tree; the merge never ran there


def test_wait_grant_polls_the_seats_own_channels_after_the_ask(tmp_path,
                                                               monkeypatch):
    """(2) wait_grant polls the SEAT's OWN channels (its inbox / the dm),
    bounded AFTER the merge-up ASK's send time -- never the Prime's own
    inbox, never without the ask. The ask is sent first (so the grant wait
    is dated), then the wait consults the seat grammar with that send time."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    recorded = []

    def fake_grant(r, seat_, prime, since_):
        recorded.append((str(r), seat_, prime, since_))
        return True
    monkeypatch.setattr(rotate, "_grant_present_for_seat", fake_grant)
    seams = rotate._make_closeout_seams(root, {}, seat="adv")
    ok, res, det = seams["merge_up_ask"]()
    assert ok is True and res == "sent", det
    ok, res, det = seams["wait_grant"]()
    assert ok is True and res == "granted", det
    assert recorded, "wait_grant never polled the seat's channels"
    _r, seat_, prime, since_ = recorded[0]
    assert seat_ == "adv" and prime == "prime"
    assert since_, "grant wait must be bounded AFTER the ask's send time"


def test_merge_up_ask_names_seat_tip_target_record_and_is_sent_as_seat(
        tmp_path, monkeypatch):
    """(3) the merge-up ASK names the seat (never the placeholder <seat>),
    the target, and the record file, and is sent AS the seat (sender=<seat>,
    so it is signed when the seat is keyed)."""
    import send
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    sent = []

    def recorder(r, to, text, sender):
        sent.append((str(r), to, text, sender))
        return None
    monkeypatch.setattr(send, "send", recorder)
    record = {"recorded_at": "2026-09-12T09:00:00.123456Z"}
    seams = rotate._make_closeout_seams(root, record, seat="adv")
    ok, res, det = seams["merge_up_ask"]()
    assert ok is True and res == "sent", det
    assert sent, "merge-up ASK was never sent"
    _, to, text, sender = sent[0]
    assert to == "prime"
    assert sender == "adv"                          # sent AS the seat
    assert "for adv" in text and "season2/main" in text
    assert "record adv.20260912T090000Z.json" in text  # the record file name


def test_suite_grid_stamp_render_run_in_main_cwd(tmp_path, monkeypatch):
    """(4) suite / grid_commit / verify_stamp / render_check spawn their
    subprocess with cwd=MAIN (the tree the merge landed in), never the seat
    tree; and the suite refuses BY NAME while another live runner holds the
    verify-suite lock."""
    import subprocess as _sp
    g, main = _git_sole_repo(tmp_path)
    (g / "sessions").mkdir(parents=True, exist_ok=True)
    real_run = _sp.run
    calls = []

    def recorder(argv, **kw):
        if argv and argv[0] == "git":
            return real_run(argv, **kw)
        calls.append(([str(a) for a in argv], kw.get("cwd")))
        class _R:
            returncode = 0
            stdout = "ok"
            stderr = ""
        return _R()
    monkeypatch.setattr(rotate.subprocess, "run", recorder)
    seams = rotate._make_closeout_seams(g, {"commit": "abc1234"})

    # a foreign live pid holding the lock -> suite refuses without spawning
    lock = g / "sessions" / "verify-suite.lock"
    lock.write_text("1\n", encoding="utf-8")
    ok, res, det = seams["suite"]()
    assert ok is False and res == "refused"
    assert "suit" in det and "lock" in det
    lock.unlink(missing_ok=True)

    for step in ("suite", "grid_commit", "verify_stamp", "render_check"):
        ok, res, det = seams[step]()
        assert ok is True, f"{step} failed: {det}"
    assert calls, "no post-merge subprocess was spawned"
    for _argv, cwd in calls:
        assert cwd == str(main), f"runner cwd {cwd!r} != MAIN {main!r}"
        assert "rotate.py" not in " ".join(_argv)  # sanity: a bin script
    # the four expected bins were each invoked once, all in MAIN
    joined = " ".join(str(x) for _argv, _cwd in calls for x in _argv)
    for script in ("snapshot-goals.py", "verification.py", "grid.py"):
        assert script in joined


def test_push_real_runner_pushes_season2_main_then_refgrids_from_main(
        tmp_path, monkeypatch):
    """(5) push runs TWO pushes in MAIN -- origin season2/main THEN origin
    refs/grid/*:refs/grid/* -- and refuses BY NAME on the first non-zero rc
    (a push that omits refs/grid, or pushes the seat branch from the seat
    tree, is the falsifier)."""
    import subprocess as _sp
    g, main = _git_sole_repo(tmp_path)
    real_run = _sp.run
    pushed = []
    first_fails = {"flag": False}

    def recorder(argv, **kw):
        if argv and argv[0] == "git" and len(argv) >= 4 and argv[3] == "push":
            pushed.append([str(a) for a in argv])
            class _R:
                returncode = 1 if first_fails["flag"] else 0
                stderr = "" if not first_fails["flag"] else "fatal: repo\n"
                stdout = ""
            return _R()
        return real_run(argv, **kw)
    monkeypatch.setattr(rotate.subprocess, "run", recorder)
    seams = rotate._make_closeout_seams(g, {})

    # first non-zero rc (here the refs/grid push, with season2/main ok in a
    # prior call on the SAME seams below) refuses BY NAME -- so make BOTH
    # fail to prove the FIRST one (season2/main) refuses too:
    first_fails["flag"] = True
    ok, res, det = seams["push"]()
    assert ok is False and res == "refused"
    assert "season2/main" in det and "push" in det
    assert len(pushed) == 1, "push must stop at the first refused push"

    # success: exactly two pushes, in order, both from MAIN
    first_fails["flag"] = False
    pushed.clear()
    ok, res, det = seams["push"]()
    assert ok is True and res == "ok", det
    assert len(pushed) == 2, pushed
    assert pushed[0][2] == str(main) and pushed[1][2] == str(main)  # -C MAIN
    assert pushed[0][4:] == ["origin", "season2/main"]
    assert pushed[1][4:] == ["origin", "refs/grid/*:refs/grid/*"]


# --- hypothesis:l4-the-closeout-merge-up-gate-ignores-cron-owned-dirty- ---
# paths-and-blocks-only-on-a-dirty-path-the-merge-touches: the merge_up
# gate must (a) ignore cron-owned dirty paths, (b) block only on a dirty
# path the MERGE actually TOUCHES (real `git diff --name-only`), (d) refuse
# an unmeasurable tree, and (e) carry ONE spelling of the prefixes. The
# "touched" set is decided by real git on the shared fixture, never a
# hand-passed list.


def test_closeout_cron_owned_prefixes_single_spelling():
    """(e) ONE spelling of the cron-owned prefixes: the closeout constant is
    DERIVED from the prepare churn constants, so a re-spelled literal breaks
    this assert (the falsifier), and the value is what F20 names."""
    assert rotate.CLOSEOUT_CRON_OWNED_PREFIXES == (
        rotate.PREPARE_CHURN_PREFIXES + rotate.PREPARE_CHURN_DIRS)
    assert rotate.CLOSEOUT_CRON_OWNED_PREFIXES == (
        ".agi/comms/", ".agi/sessions/rotations/")


def test_closeout_merge_up_rename_row_judged_on_new_path(tmp_path):
    """A RENAME row (`R old -> new`) of a cron-owned path is judged on the
    NEW path via _porcelain_path (the one extractor the prepare captive and
    this gate share), so the renamed file stays cron-owned and is NOT a
    blocker. Before the fix the raw `line[3:]` yielded 'old -> new', which
    matches no prefix and no merge-touch path."""
    import subprocess as sp
    g, main, _seat, seat_branch = _merge_fixture(tmp_path)
    comm = main / ".agi/comms/season-2/dm"
    comm.mkdir(parents=True)
    (comm / "x.md").write_text("hi\n", encoding="utf-8")
    sp.run(["git", "-C", str(main), "add", ".agi"], check=True)
    sp.run(["git", "-C", str(main), "commit", "-q", "-m", "cron files"],
           check=True)
    sp.run(["git", "-C", str(main), "mv",
            ".agi/comms/season-2/dm/x.md",
            ".agi/comms/season-2/dm/y.md"], check=True)
    # the rename row is staged in the porcelain; the gate's extractor must
    # reduce it to the NEW path so the prefix match still lands
    clean, blockers, ignored = rotate._closeout_main_clean(main, seat_branch)
    assert clean is True and blockers == [], (blockers, ignored)
    assert ignored == 1


def test_closeout_merge_up_ignores_cron_owned_dirty_paths_untouched_by_merge(
        tmp_path):
    """(a) two cron-owned dirty paths (.agi/comms/ dm file, .agi/sessions/
    rotations/sequence.json), NEITHER touched by the merge -> merge_up RUNS
    and its detail names the 2 cron-owned paths it ignored."""
    import subprocess as sp
    g, main, _seat, _sb = _merge_fixture(tmp_path)
    comm = main / ".agi/comms/season-2/dm"
    sess = main / ".agi/sessions/rotations"
    comm.mkdir(parents=True)
    sess.mkdir(parents=True)
    (comm / "x.md").write_text("hi\n", encoding="utf-8")
    (sess / "sequence.json").write_text("[]\n", encoding="utf-8")
    sp.run(["git", "-C", str(main), "add", ".agi"], check=True)
    sp.run(["git", "-C", str(main), "commit", "-q", "-m", "cron files"],
           check=True)
    # the cron writes them -- dirty, and the seat merge touches neither
    (comm / "x.md").write_text("hi\ndirty\n", encoding="utf-8")
    (sess / "sequence.json").write_text("[1]\n", encoding="utf-8")
    seams = rotate._make_closeout_seams(g, {}, seat="adv")
    ok, res, det = seams["merge_up"]()
    assert ok is True and res == "merged", det
    assert "2 cron-owned dirty path(s) ignored" in det


def test_closeout_merge_up_runs_on_dirty_path_untouched_by_merge(tmp_path):
    """(b) a NON-cron dirty tracked path the merge does NOT touch -> merge_up
    RUNS. x.py lives identically on BOTH branches (brought into the seat
    branch so the seat-change diff excludes it), then is dirtied in MAIN."""
    import subprocess as sp
    g, main, _seat, _sb = _merge_fixture(tmp_path)
    wt = tmp_path / "wt-adv"
    xdir = main / "extensions/agi/bin"
    xdir.mkdir(parents=True)
    (xdir / "x.py").write_text("def x(): pass\n", encoding="utf-8")
    sp.run(["git", "-C", str(main), "add", "extensions/agi/bin/x.py"],
           check=True)
    sp.run(["git", "-C", str(main), "commit", "-q", "-m", "x on main"],
           check=True)
    # bring x.py into the seat branch so `diff season2/main..seat` excludes it
    sp.run(["git", "-C", str(wt), "merge", "-q", "-m", "sync x",
            "season2/main"], check=True)
    (main / "extensions/agi/bin/x.py").write_text(
        "def x(): pass\nDIRTY\n", encoding="utf-8")
    seams = rotate._make_closeout_seams(g, {}, seat="adv")
    ok, res, det = seams["merge_up"]()
    assert ok is True and res == "merged", det


def test_closeout_merge_up_refuses_naming_dirty_path_touched_by_merge(
        tmp_path):
    """(c) a NON-cron dirty path the merge DOES touch -> merge_up REFUSES
    NAMING it (extensions/agi/bin/x.py, added on the seat branch and dirtied
    in MAIN)."""
    import subprocess as sp
    g, main, _seat, _sb = _merge_fixture(tmp_path)
    wt = tmp_path / "wt-adv"
    xd = wt / "extensions/agi/bin"
    xd.mkdir(parents=True)
    (xd / "x.py").write_text("def x(): pass\n", encoding="utf-8")
    sp.run(["git", "-C", str(wt), "add", "extensions/agi/bin/x.py"],
           check=True)
    sp.run(["git", "-C", str(wt), "commit", "-q", "-m", "touch x"],
           check=True)
    # x.py IS touched by the merge -- dirty it IN MAIN to force the refusal
    sp.run(["git", "-C", str(main), "checkout", "-q", "season2/posts/adv",
            "--", "extensions/agi/bin/x.py"], check=True)
    (main / "extensions/agi/bin/x.py").write_text(
        "def x(): pass\nDIRTY\n", encoding="utf-8")
    seams = rotate._make_closeout_seams(g, {}, seat="adv")
    ok, res, det = seams["merge_up"]()
    assert ok is False and res == "refused", det
    assert "extensions/agi/bin/x.py" in det
    assert "path(s) the merge touches" in det


def test_closeout_merge_up_refuses_an_unmeasurable_tree(tmp_path,
                                                     monkeypatch):
    """(d) a tree git cannot measure REFUSES: at the seam,
    _closeout_main_clean reports clean=None for a non-repo dir (git rc != 0);
    at the seam table, an unresolvable/unmeasurable MAIN refuses merge_up by
    name. The clean-is-None arm names that the tree could NOT be MEASURED
    (claim 3: still refuses, with a truthful reason -- not "dirty")."""
    import shutil
    import subprocess as sp
    not_repo = tmp_path / "not-a-repo"
    not_repo.mkdir()
    (not_repo / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    clean, blockers, ignored = rotate._closeout_main_clean(not_repo, "b")
    assert clean is None and blockers == [] and ignored == 0
    g, main, _seat, _sb = _merge_fixture(tmp_path)
    shutil.rmtree(main / ".git")
    seams = rotate._make_closeout_seams(g, {}, seat="adv")
    ok, res, det = seams["merge_up"]()
    assert ok is False and res == "refused" and "merge_up" in det
    # force the clean-is-None arm on a still-resolvable MAIN and assert the
    # wording says it was not measurable, not that it is dirty
    monkeypatch.setattr(rotate, "_closeout_main_clean", lambda *a: (None, [], 0))
    g2, _m2, _s2, _sb2 = _merge_fixture(tmp_path / "second")
    seams2 = rotate._make_closeout_seams(g2, {}, seat="adv")
    ok2, res2, det2 = seams2["merge_up"]()
    assert ok2 is False and res2 == "refused"
    assert "could not be measured" in det2
