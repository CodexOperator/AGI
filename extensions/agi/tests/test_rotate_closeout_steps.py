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
steps that are grammatically testable hermetically: the merge target and the
grant grammar.

1. The driver runs the WORKTREE-POST step list IN ORDER, logging each by name.
2. A refused step (a runner returning `(False, ...)`) STOPS the call: the log
   ends at that step, the error names the STEP, and nothing after it runs.
3. A step with NO runner is refused BY NAME (and stops).
4. The merge-up runner targets `season2/main` -- NEVER `origin/season/s2` or
   a bare `main`: it derives the season branch off the one constant and
   refuses any other target.
5. The grant grammar (`_prime_grant_present`) consumes ONLY a signed line
   FROM the prime whose body matches GRANT|GO: an unsigned line, a non-prime
   line, and a signed-prime line without GRANT/GO each never grant.
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


def test_merge_target_is_season2_main_never_origin_season_s2(monkeypatch):
    assert rotate._CLOSEOUT_MERGE_TARGET == "season2/main"
    calls = []
    monkeypatch.setattr(rotate, "_perform_season_merge",
                        lambda root, sb: calls.append(sb) or "abc1234")
    seams = rotate._make_closeout_seams(Path("/tmp/co-root"), {})
    ok, result, detail = seams["merge_up"]()
    assert ok is True and result == "merged"
    assert calls == ["main"]                       # the season2/main branch
    assert "season2/main" in detail and "merge --no-ff" in detail
    # the runner is gated on the ONE constant: a tampered target is refused
    rotate._CLOSEOUT_MERGE_TARGET = "origin/season/s2"
    try:
        ok, result, detail = seams["merge_up"]()
        assert ok is False and result == "refused"
        assert "season2/main" in detail
    finally:
        rotate._CLOSEOUT_MERGE_TARGET = "season2/main"


def _write_inbox(root, prime, blocks):
    inbox = root / "sessions" / "inbox" / f"{prime}.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("".join(blocks), encoding="utf-8")


_MSG = "---\nts: 2026-09-12T00:00:00Z\nfrom: {frm}\nto: {to}\n"
_SIGNED = _MSG + "env: v1\nsig: scheme:aa:bb\n"


def test_grant_grammar_only_signed_prime_grant_consumed():
    prime = "prime"
    # (a) unsigned prime line with GRANT -> no grant
    _write_inbox(Path("/tmp/co-root"), prime, [
        _MSG.format(frm=prime, to="x") + "\nGRANT\n"])
    assert rotate._prime_grant_present(Path("/tmp/co-root"), prime) is False
    # (b) signed NON-prime line with GRANT -> no grant
    _write_inbox(Path("/tmp/co-root"), prime, [
        _SIGNED.format(frm="someone-else", to="x") + "\nGRANT\n"])
    assert rotate._prime_grant_present(Path("/tmp/co-root"), prime) is False
    # (c) signed prime line WITHOUT GRANT|GO -> no grant
    _write_inbox(Path("/tmp/co-root"), prime, [
        _SIGNED.format(frm=prime, to="x") + "\nhold tight\n"])
    assert rotate._prime_grant_present(Path("/tmp/co-root"), prime) is False
    # (d) signed prime line with GRANT -> GRANTS
    _write_inbox(Path("/tmp/co-root"), prime, [
        _SIGNED.format(frm=prime, to="x") + "\npending PR is GO\n"])
    assert rotate._prime_grant_present(Path("/tmp/co-root"), prime) is True
    # (e) no inbox at all -> no grant
    empty = Path("/tmp/co-root-none")
    assert rotate._prime_grant_present(empty, prime) is False


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