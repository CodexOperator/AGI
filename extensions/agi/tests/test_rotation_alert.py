"""Tests for the rotation-alert UserPromptSubmit hook.

hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip

Proof criteria (a)–(e) of the brief:
  (a) a synthetic payload on stdin with a KNOWN transcript emits text naming
      THAT path in a `--session-log` argument — assert on the literal path;
  (b) a payload MISSING the transcript field fails closed with a named error
      and emits no fraction;
  (c) escalation: rising usage across several invocations of ONE session emits
      once per band below threshold and on EVERY invocation at/above it —
      assert the COUNTS per band;
  (d) two DIFFERENT session ids do not share escalation state;
  (e) the hook is SILENT and exits 0 outside an agi project and on an
      unreadable transcript.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"

spec = importlib.util.spec_from_file_location("rotation_alert", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


@pytest.fixture(autouse=True)
def _no_inherited_seat(monkeypatch):
    """Tests never inherit the RUNNER's AGI_SEAT.

    A seat exports AGI_SEAT in its own pane, so a test run from inside a seat
    worktree measures WHATEVER seat the runner exports unless it is cleared. A
    seat identification exercised by any test would then silently depend on the
    pane it happens to run in. ONE autouse fixture clears it for every test in
    the module (the three former per-test `monkeypatch.delenv` lines fold in
    here); a test that NEEDS a particular seat sets AGI_SEAT explicitly.
    """
    monkeypatch.delenv("AGI_SEAT", raising=False)


#: EVERY test records (and does NOT really run) the hook's background rotate-
#: self calls. goal:g15.25 line (4) made an over-line identifiable seat trigger
#: `_spawn_rotate_self`, so any over-line seat fixture would otherwise launch a
#: REAL detached rotate-self against the tmp fixture (a gitless root — a real
#: subprocess that does real writes and exits 3). That must never happen in a
#: test that is not about rotating. This recorder replaces the spawn for every
#: test; the rotation tests read `_SPAWNS` back as the proof.
_SPAWNS: list[list[str]] = []

#: A provably-DEAD sentinel pid the `_no_real_spawn` recorder returns (NOT a
#: real-looking 12345 that a latch could read as a live rotate-self). 2**24
#: (16777216) sits beyond OS pid_max, so `hook._pid_alive(_RECORDER_PID)` is
#: False — any latch the recorder path leaves naming it reads stale/never-held
#: and can never hold a generation against a phantom.
_RECORDER_PID = 2 ** 24


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    """Patch the ONE launch seam `hook._Popen` (a module attribute — never the
    whole function) to a recorder for every test, so no test reaches a REAL
    subprocess.Popen with a rotate-self argv.

    `_spawn_rotate_self` builds the argv via `hook._rotate_self_argv` and calls
    `_Popen(argv, ...)`, returning `proc.pid`. The recorder records that argv
    (the exact bytes the production path would spawn) into `_SPAWNS` and
    returns a fake proc whose pid is `_RECORDER_PID` — a provably-DEAD sentinel
    (16777216, beyond OS pid_max, so `hook._pid_alive` reports it dead), never a
    real-looking 12345 that a latch could read as a live rotate-self. A latch
    the recorder path leaves naming `_RECORDER_PID` reads as stale/never-held, so
    the rotation claim is proved on the built bytes without running a real
    rotate-self against a gitless tmp fixture (a real subprocess does real
    writes and exits 3 — that must never happen in a test not about rotating),
    and without ever latching a phantom pid that could hold a generation.
    Patching the SEAM, not the function, is what keeps an out-of-process run
    honest: a fresh interpreter imports this module with the REAL
    subprocess.Popen, so the out-of-process test declines via AGI_HOOK_NO_SPAWN
    instead.
    """
    _SPAWNS.clear()

    class _FakeProc:
        pid = _RECORDER_PID

    def _record(argv, **_kw):
        _SPAWNS.append(argv)
        return _FakeProc()

    monkeypatch.setattr(hook, "_Popen", _record)


@pytest.fixture
def agi_project(tmp_path, monkeypatch):
    """A model graph root: a `.agi` dir with config.json + a ladder node.

    Mirrors the real layout: root IS the `.agi` dir, the graph lives at
    `<root>/nodes/.geometry/ladder.md` (locations.find_project_root).
    """
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n---\n")
    return graph


@pytest.fixture
def run_hook():
    """Run the hook's main() with a given payload; return (code, out, err)."""
    def _run(payload: dict, state_dir: Path, monkeypatch, capsys):
        monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        code = hook.main([])
        cap = capsys.readouterr()
        return code, cap.out, cap.err
    return _run


def _payload(root, transcript, session_id="sess-1", cwd=None):
    return {
        "hook_event_name": "UserPromptSubmit",
        "session_id": session_id,
        "transcript_path": str(transcript),
        "cwd": str(cwd or root),
    }


def _write_transcript(path, tokens):
    """A transcript whose assistant usage sums to `tokens` tokens."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps({
        "message": {"role": "assistant",
                     "usage": {"input_tokens": tokens,
                                "cache_read_input_tokens": 0,
                                "cache_creation_input_tokens": 0}},
    }) for _ in range(1)) + "\n")


# --- (a) names the handed path in --session-log -----------------------------
def test_a_names_handed_transcript_path(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)  # 0.12 → band 0 (0.10)
    state_dir = tmp_path / "state-a"
    code, out, err = run_hook(_payload(agi_project, transcript, "sel-a"), state_dir,
                              monkeypatch, capsys)
    assert code == 0
    # (a): assert the LITERAL path appears in a --session-log argument.
    assert f"--session-log {transcript}" in out
    assert str(transcript) in out


# --- (b) missing transcript field → fail closed, named error, no fraction ----
def test_b_missing_transcript_fails_closed(run_hook, tmp_path, monkeypatch, capsys):
    test_root = tmp_path / "plain" / "graph" / ".agi"
    test_root.mkdir(parents=True)
    (test_root / "config.json").write_text("{}")
    state_dir = tmp_path / "state-b"
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": "s",
               "cwd": str(test_root)}  # NO transcript_path
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 3
    assert "fail-closed" in err or "no \"transcript_path\"" in err
    assert "--session-log" not in out       # no command, no fraction emitted


# --- (c) escalation: once per band below, EVERY call at/over -----------------
def test_c_escalation_counts_per_band(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    transcript = tmp_path / "sess.jsonl"
    state_dir = tmp_path / "state-c"
    # window=100k, threshold=0.25 → bands at 0.10/0.1375/0.175/0.2125/0.25.
    # tokens → fraction: 10k=.10 (b0), 16k=.16 (b1), 20k=.20 (b2), 30k=.30 (over)
    emissions = []
    for tokens in (10_000, 16_000, 20_000, 30_000, 30_000):
        _write_transcript(transcript, tokens)
        code, out, err = run_hook(_payload(agi_project, transcript, "sess-c"),
                                  state_dir, monkeypatch, capsys)
        assert code == 0
        emissions.append(("## ⚠️" in out and "--session-log" in out, out))
    # first three: one emission each (bands 0,1,2), below line
    assert [em[0] for em in emissions] == [True, True, True, True, True]
    # over the line (30k): the FIFTH call ALSO emits — every firing at/over.
    assert emissions[3][0] and emissions[4][0]
    # Band counts: 3 distinct band emissions below line + 2 over-line = 5 total,
    # and NO re-fire of an already-fired band. Static check below.
    assert "approaching rotation" in emissions[0][1].lower()
    assert "ROTATION OWED" in emissions[3][1]


def test_c_no_refire_within_band(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """Staying inside an already-crossed band is SILENT (once per band)."""
    transcript = tmp_path / "sess.jsonl"
    state_dir = tmp_path / "state-c2"
    _write_transcript(transcript, 10_000)  # band0 = 0.10
    code, out, _ = run_hook(_payload(agi_project, transcript, "sess-c2"),
                            state_dir, monkeypatch, capsys)
    assert code == 0 and "--session-log" in out
    # Same session, slightly deeper but still band0 (< 0.1375): SILENT.
    _write_transcript(transcript, 13_000)  # 0.13, still band0
    code, out, _ = run_hook(_payload(agi_project, transcript, "sess-c2"),
                            state_dir, monkeypatch, capsys)
    assert code == 0 and "--session-log" not in out


# --- (d) two session ids do not share escalation state -----------------------
def test_d_sessions_independent(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    transcript_a = tmp_path / "a.jsonl"
    transcript_b = tmp_path / "b.jsonl"
    _write_transcript(transcript_a, 10_000)
    _write_transcript(transcript_b, 10_000)
    state_dir = tmp_path / "state-d"
    # A fires band0.
    code, out, _ = run_hook(_payload(agi_project, transcript_a, "sess-A"),
                            state_dir, monkeypatch, capsys)
    assert code == 0 and "--session-log" in out
    # B, SAME STATE DIR, same depth: must STILL fire — no shared state.
    code, out, _ = run_hook(_payload(agi_project, transcript_b, "sess-B"),
                            state_dir, monkeypatch, capsys)
    assert code == 0 and "--session-log" in out
    # A again at same depth: now silent (its own band0 already fired).
    code, out, _ = run_hook(_payload(agi_project, transcript_a, "sess-A"),
                            state_dir, monkeypatch, capsys)
    assert code == 0 and "--session-log" not in out


# --- (e) silent + exit 0 outside a project and on unreadable transcript ------
def test_e_silent_outside_project(run_hook, tmp_path, monkeypatch, capsys):
    outside = tmp_path / "plain"   # no .agi/config.json anywhere above it
    outside.mkdir(exist_ok=True)
    transcript = tmp_path / "x.jsonl"
    _write_transcript(transcript, 50_000)
    state_dir = tmp_path / "state-e1"
    code, out, err = run_hook(_payload(outside, transcript, "sess-e", cwd=outside),
                              state_dir, monkeypatch, capsys)
    assert code == 0
    assert out == ""          # nothing printed
    assert "--session-log" not in out


def test_e_silent_on_unreadable_transcript(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    missing = tmp_path / "no-such-transcript.jsonl"   # does not exist
    state_dir = tmp_path / "state-e2"
    code, out, err = run_hook(_payload(agi_project, missing, "sess-e2"),
                              state_dir, monkeypatch, capsys)
    assert code == 0
    assert out == ""
    assert "--session-log" not in out


def test_e_no_stdin_is_silent(run_hook, tmp_path, monkeypatch, capsys):
    """No payload on stdin (not a hook invocation): nothing, exit 0."""
    state_dir = tmp_path / "state-e3"
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))   # empty stdin
    assert hook.main([]) == 0
    assert capsys.readouterr().out == ""

# --------------------------------------------------------------------------
# Repair tests — added by sanctuary-director gen V in review of L4.94.
#
# 🔴 THE ROUND'S OWN 8 TESTS PASS IDENTICALLY BEFORE AND AFTER A 141x
# CORRECTION TO THE NUMERATOR. That is the finding, not a footnote: a suite
# that cannot distinguish the defect from the fix is not testing the claim.
# Both fixtures below are built so that the wrong implementation FAILS them.
# --------------------------------------------------------------------------

import json as _json
import subprocess as _subprocess
import sys as _sys
from pathlib import Path as _Path

_HOOK = _Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"


def _many_message_transcript(path, turns, per_turn):
    """A transcript whose SUM and whose LATEST differ by construction.

    Every assistant turn carries the same `usage`, so latest == per_turn while
    the sum == turns * per_turn. With one or two turns these coincide — which
    is exactly why the round's fixtures could not see the defect.
    """
    with open(path, "w", encoding="utf-8") as fh:
        for _ in range(turns):
            fh.write(_json.dumps({"message": {
                "role": "assistant",
                "usage": {"input_tokens": per_turn,
                          "cache_read_input_tokens": 0,
                          "cache_creation_input_tokens": 0}}}) + "\n")


def test_the_numerator_is_the_latest_message_not_a_running_sum(tmp_path):
    """A level, not a total. 200 turns of 1,000 tokens is a 1,000-token
    context, not a 200,000-token one. The summing implementation reports 200x
    this number and would fire on every session from its first few turns."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("ra_repair", _HOOK)
    ra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ra)

    tp = tmp_path / "t.jsonl"
    _many_message_transcript(tp, turns=200, per_turn=1000)
    used, seen = ra._latest_usage(tp)
    assert seen == 200, seen           # it really did read every message
    assert used == 1000, used          # ...and reports the LEVEL, not 200_000


def test_the_emitted_command_is_actually_runnable(tmp_path, monkeypatch, run_hook, capsys):
    """P5 is the hook's whole reason for existing, so an unrunnable command is
    the deliverable failing, not a typo.

    The original emitted `--seat <s> --pin --session-log <path>`, in which
    `--pin` (which TAKES A PATH) swallowed the `--session-log` flag as its
    value. This asserts the emitted argv PARSES against rotate.py's own
    parser — the arithmetic-not-the-string standard.

    mur-SL2.17 / goal:g15.24 (ii): drives the hook's ENTRY FUNCTION IN
    PROCESS — `hook.main([])` with `sys.stdin` monkeypatched to a StringIO
    carrying the JSON payload, `capsys` capturing stdout (via `run_hook`),
    and the autouse `_no_real_spawn` fixture patching the ONE launch seam
    `hook._Popen` to a recorder. An in-process run proves the spawn argv was
    BUILT without firing a real rotate-self — no subprocess is spawned, so
    the `AGI_HOOK_NO_SPAWN` guard is not needed here (its OWN out-of-process
    coverage lives at test_the_no_spawn_guard... below).
    """
    import shlex

    # A seat worktree shape, so the seat is derivable and --pin is emitted.
    root = tmp_path / "repo" / ".agi" / "worktrees" / "seat-demo" / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    (root / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 1000\ndirector_rotate_at: 0.47\n---\n",
        encoding="utf-8")
    tp = tmp_path / "own.jsonl"
    _many_message_transcript(tp, turns=3, per_turn=900)   # 0.90 -> over the line

    code, out, err = run_hook(_payload(root.parent, tp), tmp_path / "state",
                              monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED NOW" in out, out

    cmd = [ln for ln in out.splitlines() if "rotate.py meter" in ln]
    assert cmd, out
    argv = shlex.split(cmd[0])
    # The defect, stated directly: no flag may be another flag's value.
    for i, tok in enumerate(argv):
        if tok == "--pin":
            assert not argv[i + 1].startswith("--"), \
                f"--pin swallowed a flag: {argv[i:i + 2]}"
    assert "--session-log" in argv, argv
    assert str(tp) in argv, argv          # it names the HANDED transcript

    # And it must parse against rotate.py's real parser, not merely look right.
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "bin"))
    import rotate
    parser = rotate.build_parser() if hasattr(rotate, "build_parser") else None
    if parser is not None:
        ns = parser.parse_args(argv[2:])      # drop "python3 <path>"
        assert ns.session_log == str(tp)
        assert ns.pin and not str(ns.pin).startswith("--")

# --------------------------------------------------------------------------
# Round SL1.05 — the hook SAYS WHAT IT MEASURES (hypothesis:l4-the-rotation-
# alert-hook-says-what-it-measures). Build order, not measurement: the
# fixtures (a)-(d) FAIL against the pre-fix bytes and pass on the built ones.
# --------------------------------------------------------------------------

# --- (a) registration text names UserPromptSubmit, never SessionStart -------
def test_a_registration_names_userpromptsubmit():
    src = _HOOK.read_text(encoding="utf-8")
    # The Prime INSTALLED the hook under UserPromptSubmit (16:21Z). The
    # registration comment and docstring must name the hook point that is
    # actually wired, not the SessionStart it was drafted for.
    assert "UserPromptSubmit" in src
    assert "SessionStart" not in src


# --- (b) the printed band pct is the band's OWN fraction of threshold -------
def _fraction_test(graph, transcript, session, state_dir, run_hook, monkeypatch, capsys):
    # AGI_SEAT is cleared by the module's autouse fixture (_no_inherited_seat).
    state_dir.mkdir(exist_ok=True)
    return run_hook(_payload(graph, transcript, session), state_dir, monkeypatch, capsys)


def test_b_band_pct_is_own_fraction(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    # threshold 0.25, window 100k. band 0.55 -> 0.1375; band 0.40 -> 0.10.
    t40 = tmp_path / "b40.jsonl"
    _write_transcript(t40, 10_000)          # fraction 0.10 -> crossed band 0.40
    code, out, err = _fraction_test(agi_project, t40, "sess-b40",
                                    tmp_path / "state-b40", run_hook,
                                    monkeypatch, capsys)
    assert code == 0
    # int(0.40*threshold*100)=18 on the old bytes; int(0.40*100)=40 on the fix.
    assert "Crossed band 40% of threshold" in out, out

    t55 = tmp_path / "b55.jsonl"
    _write_transcript(t55, 16_000)          # fraction 0.16 -> crossed band 0.55
    code, out, err = _fraction_test(agi_project, t55, "sess-b55",
                                    tmp_path / "state-b55", run_hook,
                                    monkeypatch, capsys)
    assert code == 0
    assert "Crossed band 55% of threshold" in out, out
    assert "Crossed band 18" not in out


def test_b2_band_message_says_keep_working_not_stop(agi_project, run_hook, tmp_path,
                                                     monkeypatch, capsys):
    """A below-the-line band is not a stop: the owner measured a director
    idling at 0.85x the line instead of working to it (2026-09-24). The band
    message must say so explicitly, not just report the fraction."""
    t = tmp_path / "b2.jsonl"
    _write_transcript(t, 10_000)  # threshold 0.25, window 100k -> band 0.40
    code, out, err = _fraction_test(agi_project, t, "sess-b2",
                                    tmp_path / "state-b2", run_hook,
                                    monkeypatch, capsys)
    assert code == 0
    assert "keep working" in out.lower(), out
    assert "rotate.py rotate" in out, out


# --- (c) the fraction line names BOTH the window and the line ---------------
def test_c_fraction_line_names_window_and_line(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    tp = tmp_path / "c.jsonl"
    _write_transcript(tp, 10_000)          # fraction 0.10 at threshold 0.25
    code, out, err = _fraction_test(agi_project, tp, "sess-c", tmp_path / "state-c",
                                    run_hook, monkeypatch, capsys)
    assert code == 0
    assert "of the line" in out, out
    # SM.14a shape: <frac> of <thr> window (<pct>% of the line)
    assert "0.1000 of 0.250 window" in out, out
    assert "40.00% of the line" in out, out


# --- (c2) SM.14a: the gen-27 misread pair renders BOTH referents -----------
def test_c2_meter_phrase_names_window_and_line_referents(
        tmp_path, run_hook, monkeypatch, capsys):
    """SM.14a — the measured disease: window fraction 0.3183 at a 0.470
    threshold printed only `0.6772 of the line`, read by the Prime as past
    the line. The fix prints `<frac> of <thr> window (N% of the line)` so
    each number is labelled with what it is a fraction of."""
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    tp = tmp_path / "c2.jsonl"
    _write_transcript(tp, 31_830)          # 0.3183 of the window
    code, out, err = _fraction_test(graph, tp, "sess-c2",
                                    tmp_path / "state-c2", run_hook,
                                    monkeypatch, capsys)
    assert code == 0
    assert "0.3183 of 0.470 window (67.72% of the line)" in out, out


# --- (d) a fixture worktree seat is measured against its OWN rotate_at ------
def test_d_seat_measured_at_own_rotate_at(tmp_path, run_hook, monkeypatch, capsys):
    """A seat whose config:seats row declares rotate_at 0.4 is measured at 0.4,
    not at the ladder's director_rotate_at 0.47 — and the emitted message names
    the row that won."""
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"sensei-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-sensei-director\", "
        "\"rotate_at\": 0.4}\n---\n")

    # cwd sits under the seat's worktree -> the seat is identifiable by path.
    seat_cwd = graph / "worktrees" / "seat-sensei-director"
    seat_cwd.mkdir(parents=True, exist_ok=True)

    tp = tmp_path / "d.jsonl"
    _write_transcript(tp, 45_000)          # fraction 0.45: >= 0.4, < 0.47
    state_dir = tmp_path / "state-d"
    state_dir.mkdir(exist_ok=True)
    # AGI_SEAT is cleared by the module's autouse fixture; the seat is
    # identified from the cwd sitting under the `seat-<name>` worktree.
    code, out, err = run_hook(_payload(graph, tp, "sess-d", cwd=str(seat_cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    # 0.45 >= 0.4 => ROTATION OWED proves it fired against the SEAT's 0.4,
    # not the ladder's 0.47 (0.45 < 0.47 would only be "approaching").
    assert "ROTATION OWED" in out, out
    # the emitted message NAMES the row that supplied the threshold.
    assert "config:seats" in out and "sensei-director" in out, out
    assert "ladder.director_rotate_at" not in out, out


# --- (kid 2) config:posts / post-<name> worktree / AGI_POST (hypothesis:
# --- l4-a-seat-is-a-post-everywhere) ----------------------------------------
def test_posts_md_is_resolved_post_first(tmp_path, run_hook, monkeypatch, capsys):
    """A posts.md-ONLY fixture (no seats.md on disk — the post-rename live
    shape) still resolves the post's OWN rotate_at. The measured fraction 0.45
    is >= the posts row line 0.4 but < the ladder 0.47, so ROTATION OWED fires
    only if the `posts:` row was read; a residual literal `seats.md` stat would
    return [] and fall to the ladder ("approaching", not OWED) — and fail."""
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    # only posts.md exists — the renamed live file
    (graph / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nposts:\n"
        "  - {\"name\": \"sensei-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/post-sensei-director\", "
        "\"rotate_at\": 0.4}\n---\n")

    # cwd sits under the RENAMED `post-<name>` worktree spelling
    post_cwd = graph / "worktrees" / "post-sensei-director"
    post_cwd.mkdir(parents=True, exist_ok=True)

    tp = tmp_path / "posts.jsonl"
    _write_transcript(tp, 45_000)          # fraction 0.45: >= 0.4, < 0.47
    state_dir = tmp_path / "state-posts"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-posts", cwd=str(post_cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out, out
    # the message names the POSTS row that won — never {} / ladder
    assert "config:posts" in out and "sensei-director" in out, out
    assert "ladder.director_rotate_at" not in out, out


def test_agi_post_wins_over_agi_seat_in_hook(tmp_path, run_hook, monkeypatch, capsys):
    """Both AGI_POST and AGI_SEAT set: AGI_POST identifies the post, so the
    threshold comes from the POST row (rotate_at 0.4) not the legacy row
    (rotate_at 0.99). 0.45 fires ROTATION OWED only against the post row."""
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nposts:\n"
        "  - {\"name\": \"new-post\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/post-new-post\", "
        "\"rotate_at\": 0.4}\n"
        "  - {\"name\": \"legacy-seat\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-legacy-seat\", "
        "\"rotate_at\": 0.99}\n---\n")
    monkeypatch.setenv("AGI_POST", "new-post")
    monkeypatch.setenv("AGI_SEAT", "legacy-seat")

    tp = tmp_path / "env.jsonl"
    _write_transcript(tp, 45_000)          # >= 0.4 (new-post), < 0.99 and 0.47
    state_dir = tmp_path / "state-env"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-env", cwd=str(graph)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out, out
    assert "new-post" in out, out
    assert "legacy-seat" not in out, out


# --- (e) a seat rotate_at of 0 is treated as MISSING, not as threshold 0 ----
def test_e_nonpositive_seat_rotate_at_falls_back_to_ladder(tmp_path, run_hook, monkeypatch, capsys):
    """RED-FIRST guard for the ZeroDivisionError. A config:seats row whose
    `rotate_at` is 0 (or negative) must NOT become threshold 0.0.

    On the pre-fix bytes `_seat_line()` returns float(0) unconditionally;
    `over_line = fraction >= 0.0` is True and `_emit` computes
    `fraction / threshold` -> **ZeroDivisionError**, a traceback on every
    prompt for that seat. The seat's own row must lose to the ladder default
    exactly the way a MISSING row does, and the message must say the ladder
    won.
    """
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    # The seat's row declares rotate_at 0 — a real value that must be treated
    # as missing, never as a 0.0 threshold.
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"sensei-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-sensei-director\", "
        "\"rotate_at\": 0}\n---\n")

    seat_cwd = graph / "worktrees" / "seat-sensei-director"
    seat_cwd.mkdir(parents=True, exist_ok=True)

    tp = tmp_path / "e.jsonl"
    _write_transcript(tp, 25_000)          # fraction 0.25: >=0.188 (band 0.40)
                                             # yet < 0.47, so it must fire as
                                             # "approaching" against the LADDER line
    state_dir = tmp_path / "state-e"
    state_dir.mkdir(exist_ok=True)

    # (i)+(ii) must NOT raise / crash, and (iii) must not collapse to a
    # 0.0 threshold that forces `over_line` true and divides by zero.
    code, out, err = run_hook(_payload(graph, tp, "sess-e", cwd=str(seat_cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, (err, out)           # (i) exit 0, not a traceback
    assert "ZeroDivisionError" not in err
    assert "Traceback" not in err
    assert "ROTATION OWED" not in out     # 0.10 < 0.47 -> approaching, not over
    # the row's 0 was rejected -> the message names the LADDER as the source.
    assert "ladder.director_rotate_at" in out, out
    assert "config:seats" not in out, out

# --------------------------------------------------------------------------
# Round SL3.04 — the seat's rotate_at is read MAIN-CHECKOUT-first and the
# tests never inherit the runner's AGI_SEAT (hypothesis:l4-the-rotation-
# alert-reads-the-main-checkout-row-and-its-tests-do-not-inherit-the-runners-
# seat). Build order, not measurement: the fixtures fail against the pre-fix
# bytes and pass on the built ones. Each test also asserts on the emitted
# SOURCE STRING that names which tree won.
# --------------------------------------------------------------------------

def _linked_worktree(tmp_path, main_seats, wt_seats, wt_name):
    """A (main checkout, linked worktree) graph-root PAIR with per-tree
    `config:seats` rows and a ladder on the worktree. Returns (wt_graph,
    main_graph). `git_common_root` is stubbed in the CALLER to bounce the
    worktree root onto `main_graph` (a tmp tree has no real git worktree, so
    the resolver cannot discover the integration tree itself)."""
    outer = tmp_path / "outer"
    main_graph = outer / "repo" / ".agi"
    (main_graph / "nodes" / ".geometry").mkdir(parents=True)
    (main_graph / "config.json").write_text("{}")
    if main_seats is not None:
        (main_graph / "nodes" / ".geometry" / "seats.md").write_text(main_seats)
    wt_graph = main_graph / "worktrees" / wt_name / ".agi"
    (wt_graph / "nodes" / ".geometry").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    (wt_graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (wt_graph / "nodes" / ".geometry" / "seats.md").write_text(wt_seats)
    return wt_graph, main_graph


def _stub_git_common_root(monkeypatch, main_graph):
    """Wire `locations.git_common_root` to bounce any WORKTREE path onto the
    main checkout, and leave a main-checkout path alone."""
    import sys as _s
    _s.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
    import locations
    monkeypatch.setattr(locations, "git_common_root",
                        lambda root: main_graph if "worktrees" in str(root) else root)


# --- (f) MAIN-CHECKOUT ROW WINS over the worktree's stale row ---------------
def test_f_main_checkout_row_wins(tmp_path, run_hook, monkeypatch, capsys):
    """A fixture main checkout whose seats row says rotate_at 0.4 and a linked
    worktree whose stale row says 0.47 -> threshold 0.4 and the source string
    says `(main checkout)`. The Prime edits the line on MAIN; a seat must not
    keep rotating at a stale merged value for a whole generation."""
    main_seats = ("---\nseats:\n"
                  "  - {\"name\": \"test-seat\", \"role\": \"director\", "
                  "\"worktree\": \".agi/worktrees/seat-test-seat\", "
                  "\"rotate_at\": 0.4}\n---\n")
    wt_seats = ("---\nseats:\n"
                "  - {\"name\": \"test-seat\", \"role\": \"director\", "
                "\"worktree\": \".agi/worktrees/seat-test-seat\", "
                "\"rotate_at\": 0.47}\n---\n")
    wt_graph, main_graph = _linked_worktree(tmp_path, main_seats, wt_seats,
                                            "seat-test-seat")
    _stub_git_common_root(monkeypatch, main_graph)

    tp = tmp_path / "f.jsonl"
    _write_transcript(tp, 45_000)     # fraction 0.45: >= main 0.4, < worktree 0.47
    state_dir = tmp_path / "state-f"
    state_dir.mkdir(exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "test-seat")   # explicit — may NOT rely on env
    code, out, err = run_hook(_payload(wt_graph, tp, "sess-f",
                                       cwd=str(wt_graph.parent)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    # 0.45 >= 0.4 => ROTATION OWED: measured at the MAIN row's 0.4, not the
    # worktree's 0.47 (0.45 < 0.47 would only be "approaching").
    assert "ROTATION OWED" in out, out
    # the source string NAMES the main checkout as the winner.
    assert "config:seats test-seat.rotate_at (main checkout)" in out, out
    assert "ladder.director_rotate_at" not in out, out


# --- (g) a seat present ONLY in the worktree row ----------------------------
def test_g_seat_only_in_worktree_row(tmp_path, run_hook, monkeypatch, capsys):
    """When the MAIN checkout has no row for the seat, the worktree row wins —
    and the source string says `(worktree)`."""
    wt_seats = ("---\nseats:\n"
                "  - {\"name\": \"only-wt\", \"role\": \"director\", "
                "\"worktree\": \".agi/worktrees/seat-only-wt\", "
                "\"rotate_at\": 0.47}\n---\n")
    wt_graph, main_graph = _linked_worktree(tmp_path, None, wt_seats, "seat-only-wt")
    _stub_git_common_root(monkeypatch, main_graph)   # main has NO seats.md

    tp = tmp_path / "g.jsonl"
    _write_transcript(tp, 45_000)     # 0.45 < 0.47 -> approaching, not over
    state_dir = tmp_path / "state-g"
    state_dir.mkdir(exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "only-wt")
    code, out, err = run_hook(_payload(wt_graph, tp, "sess-g",
                                       cwd=str(wt_graph.parent)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" not in out   # 0.45 < 0.47
    assert "config:seats only-wt.rotate_at (worktree)" in out, out
    assert "main checkout" not in out, out
    assert "ladder.director_rotate_at" not in out, out


# --- (h) the cwd-`worktree` fallback is KEPT (reached by a non-convention row)-
def test_h_dead_fallback_reached_by_nonconvention_worktree(tmp_path, run_hook, monkeypatch, capsys):
    """DECISION (ii): the row-`worktree` path-match fallback is KEPT, on
    evidence. The seats schema allows a row whose `worktree` does NOT follow
    the `seat-<name>` convention (`.agi/context/schemas/[config].md` types
    `worktree` as an unconstrained string relative to graph_root). From inside
    such a worktree `_seat_from_cwd` returns None, so the fallback is the ONLY
    thing that identifies the seat — this fixture reaches it (seat `weird`). A
    fallback capable of this is not dead code; it is a safety net the real
    registry merely never exercises (every perpetual seat uses `seat-<name>`)."""
    outer = tmp_path / "outer"
    graph = outer / "repo" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n  - {\"name\": \"weird\", \"role\": \"director\", "
        "\"worktree\": \"custom-ish\", \"rotate_at\": 0.5}\n---\n")
    cwd = graph / "custom-ish"      # worktree that does NOT follow seat-<name>
    cwd.mkdir(parents=True, exist_ok=True)

    tp = tmp_path / "h.jsonl"
    _write_transcript(tp, 45_000)   # 0.45 < weird's 0.5 -> approaching, not over
    state_dir = tmp_path / "state-h"
    state_dir.mkdir(exist_ok=True)
    # AGI_SEAT deliberately NOT set: the autouse fixture cleared any inherited
    # value and the cwd fallback must identify the seat on its own.
    code, out, err = run_hook(_payload(graph, tp, "sess-h", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    # the fallback identified `weird` and its 0.5 line won (0.45 -> approaching).
    assert "config:seats weird.rotate_at" in out, out
    assert "ROTATION OWED" not in out, out


def _unresolved_worktree(tmp_path, seats):
    """A single worktree graph root holding `seats` in its config:seats row and
    a ladder, for the P7 fallback cases where main cannot be resolved."""
    outer = tmp_path / "outer"
    graph = outer / "repo" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(seats)
    return graph


def _stub_git_common_root_raise(monkeypatch):
    """locations.git_common_root RAISES — the main-checkout resolver is down
    (git unavailable). The hook must not crash and must not label main."""
    import sys as _s
    _s.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
    import locations
    def _boom(_root):
        raise RuntimeError("git unavailable")
    monkeypatch.setattr(locations, "git_common_root", _boom)


def _stub_git_common_root_no_graph(monkeypatch, tmp_path):
    """git_common_root returns a repo root that find_project_root cannot map to
    any graph (no `.agi`/config.json under it) → `unresolved:no-graph-root`."""
    import sys as _s
    _s.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
    import locations
    bare = tmp_path / "bare-repo-root"
    bare.mkdir(exist_ok=True)
    monkeypatch.setattr(locations, "git_common_root", lambda _root: bare)


# --- (j) main UNRESOLVED via exception → worktree row, named reason ---------
def test_j_main_unresolved_exception_labels_worktree(tmp_path, run_hook,
                                                     monkeypatch, capsys):
    """When locations.git_common_root RAISES (git unavailable, any Exception),
    the hook must NOT crash (P7) and must NOT label the worktree's row
    `(main checkout)` — the exact lie this round removes. It emits the worktree
    threshold with a source string that NAMES why main was unresolved."""
    seats = ("---\nseats:\n  - {\"name\": \"booms\", \"role\": \"director\", "
             "\"worktree\": \".agi/worktrees/seat-booms\", "
             "\"rotate_at\": 0.4}\n---\n")
    graph = _unresolved_worktree(tmp_path, seats)
    _stub_git_common_root_raise(monkeypatch)

    tp = tmp_path / "j.jsonl"
    _write_transcript(tp, 30_000)   # 0.30 < 0.4 -> approaching, not over
    state_dir = tmp_path / "state-j"
    state_dir.mkdir(exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "booms")
    code, out, err = run_hook(_payload(graph, tp, "sess-j",
                                       cwd=str(graph.parent)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, (err, out)      # P7: an exception path must not crash/hang
    assert "Traceback" not in err
    # threshold from the WORKTREE row, labelled with the unresolved reason.
    assert "config:seats booms.rotate_at (worktree; main unresolved:" in out, out
    assert "main checkout" not in out, out


# --- (k) main UNRESOLVED via no graph root → named reason -------------------
def test_k_main_unresolved_no_graph_root_labels_worktree(tmp_path, run_hook,
                                                         monkeypatch, capsys):
    """When git_common_root resolves a repo root but find_project_root finds no
    graph under it (case (ii) of the round), main is unresolved with reason
    `no-graph-root`; the worktree row is labelled with that reason, never
    `(main checkout)`."""
    seats = ("---\nseats:\n  - {\"name\": \"ngr\", \"role\": \"director\", "
             "\"worktree\": \".agi/worktrees/seat-ngr\", "
             "\"rotate_at\": 0.47}\n---\n")
    graph = _unresolved_worktree(tmp_path, seats)
    _stub_git_common_root_no_graph(monkeypatch, tmp_path)

    tp = tmp_path / "k.jsonl"
    _write_transcript(tp, 45_000)   # 0.45 < 0.47 -> approaching, not over
    state_dir = tmp_path / "state-k"
    state_dir.mkdir(exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "ngr")
    code, out, err = run_hook(_payload(graph, tp, "sess-k",
                                       cwd=str(graph.parent)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, (err, out)
    assert ("config:seats ngr.rotate_at "
            "(worktree; main unresolved: unresolved:no-graph-root)") in out, out
    assert "main checkout" not in out, out


# --- (i) the autouse fixture clears an inherited AGI_SEAT -------------------
def test_module_agiseat_is_cleared_at_entry():
    """The module's autouse fixture must clear the RUNNER's AGI_SEAT at every
    test entry, even when a seat exports it (`env AGI_SEAT=x python3 -m pytest
    ... -q` is green). This assertion is trivially true in a clean shell; its
    PROOF is the whole module going green under `env AGI_SEAT=x`."""
    assert "AGI_SEAT" not in os.environ

# --------------------------------------------------------------------------
# Round SL7.23 — the meter hook ROTATES at threshold (goal:g15.25 line (4)),
# hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up.
# Build order, not measurement: each gate that HOLDS (card age / merge-up in
# flight / prepare captives / once-per-generation latch) makes the hook do
# NOTHING and print its reason; every gate clean makes the hook background
# `rotate.py rotate-self --stops` ONCE (rotate-out ZERO calls — the hook IS
# the rotate-out). The spawn is the `_no_real_spawn` recorder; `_SPAWNS` is
# read back as the proof. The merge-up gate is THE point of the node — its
# test comes first.
# --------------------------------------------------------------------------

def _over_line_seat_fixture(tmp_path):
    """A single-tree graph fixture whose seat `probe-director` (AGI_SEAT) has
    rotate_at 0.4, with a worktree cwd. Transcript 45_000 / window 100_000 =
    0.45 >= 0.4 → over the line. Gitless: every gate's measurement degrades to
    clean, so gates (b)(c)(d) pass and gate (a) passes unless a card is made
    stale — the fixture for the CLEAN state that must rotate."""
    outer = tmp_path / "outer"
    graph = outer / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotate_at\": 0.4}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return graph, cwd


# --- gate (b) FIRST — the merge-up-in-flight gate is THE point of the node ---
def test_live_suite_lock_defers_rotation(tmp_path, run_hook, monkeypatch, capsys):
    """A LIVE verify-suite lock holds gate (b): the hook prints the deferral
    and does NOT rotate. A rotation landing mid-merge is worse than one extra
    tool call — this is the FALSIFIER that must hold."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    lock = graph / "sessions" / "verify-suite.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text(str(os.getpid()))   # THIS test's own LIVE pid
    tp = tmp_path / "lock.jsonl"
    _write_transcript(tp, 45_000)       # 0.45 >= 0.4 -> over the line
    state_dir = tmp_path / "state-lock"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-lock", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out          # the over-line banner still shows
    assert ("rotation deferred: merge-up in flight "
            "(verify-suite lock live)") in out, out
    assert _SPAWNS == []                   # the hook does NOT rotate
    assert "rotation: spawned" not in out


# --- gate (a) card-age captive ----------------------------------------------
def test_stale_card_delays_and_prints_card_line(tmp_path, run_hook, monkeypatch, capsys):
    """A card OLDER than the last WORK commit holds gate (a): the hook prints
    the card line to write and does NOT rotate (the hook never rotates a seat
    whose card is stale)."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    # fake a WORK commit far in the FUTURE so the freshly-past card is stale.
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    card = graph / "sessions" / "quorum" / "probe-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# probe-director card (stale)\n")
    os.utime(card, (1, 1))                # mtime far in the PAST
    tp = tmp_path / "stale.jsonl"
    _write_transcript(tp, 45_000)
    state_dir = tmp_path / "state-stale"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-stale", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    assert "card-age captive" in out, out
    assert "rotate.py handoff --driven --seat probe-director" in out, out
    # conjunct (4): the ONE-LINE EXIT prints FIRST, never buried under prose.
    assert (out.index("rotate.py handoff --driven --seat probe-director")
            < out.index("card-age captive")), out
    assert _SPAWNS == []                   # the hook does NOT rotate a stale card


# --- ALL GATES CLEAN -> the hook IS the rotate-out (ZERO calls) -------------
def test_over_line_clean_state_rotates_from_hook(tmp_path, run_hook, monkeypatch, capsys):
    """A fake seat over its line with a CLEAN state rotates from the hook with
    ZERO rotate-out calls: exactly one background `rotate.py rotate-self
    --stops` snapshot, the spawn + card printed, and the once-per-generation
    latch written so a slow spawn is never doubled."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    tp = tmp_path / "clean.jsonl"
    _write_transcript(tp, 45_000)
    state_dir = tmp_path / "state-clean"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-clean", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    # rotate-out ZERO calls: the hook runs rotate-self ITSELF, exactly once.
    assert len(_SPAWNS) == 1, _SPAWNS
    argv = _SPAWNS[0]
    assert "rotate-self" in argv, argv
    assert argv[argv.index("--name") + 1] == "probe-director"
    assert argv[argv.index("--role") + 1] == "director"
    assert argv[argv.index("--timeout") + 1] == "900"
    assert "--force" in argv
    stops = argv[argv.index("--stops") + 1]
    assert stops.startswith("stops: "), stops   # NEVER empty (line (4) FALSIFIER)
    # what the hook did is PRINTED -- the operator sees the spawn + the card.
    assert "rotation: spawned rotate-self" in out, out
    assert "probe-director" in out
    # once-per-generation latch under the shared sessions dir.
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-cle.lock"
    assert latch.exists(), "once-per-seating latch not written"
    assert "session sess-clean" in latch.read_text()
    assert "rotation deferred" not in out


# --- gate (d) once-per-generation latch -------------------------------------
def test_latch_prevents_double_rotation(tmp_path, run_hook, monkeypatch, capsys):
    """Gate (d): once a spawn for seat + generation has happened (latch present),
    a next prompt does NOT re-spawn — a slow spawn is never doubled."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-onc.lock"
    latch.parent.mkdir(parents=True, exist_ok=True)
    latch.write_text("pid 1\n")          # as if a spawn had just started
    tp = tmp_path / "once.jsonl"
    _write_transcript(tp, 45_000)
    state_dir = tmp_path / "state-once"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-once", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "already rotating probe-director session sess-onc" in out, out
    assert _SPAWNS == []                  # a slow spawn is NEVER doubled


def test_latch_keys_session_for_nonprime_and_gen_for_prime(tmp_path):
    """Clause (3) LATCH: a NON-prime post keys its once-per-seating latch on
    the row's session id (`hook-<seat>-<sid8>.lock`, body `session <id>`); the
    PRIME post keeps the gen key BYTE-IDENTICAL (`hook-<seat>-gen<N>.lock`,
    body `gen <N>`). FALSIFIERS: a non-prime latch still keyed on gen; a prime
    latch path changed in any byte."""
    graph = tmp_path / "g" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"session_id\": \"a1b2c3d4-1111-2222-3333-444455556666\"}\n"
        "  - {\"name\": \"belam\", \"role\": \"prime_director\", "
        "\"session_id\": \"ffffffff-0000-0000-0000-000000000000\"}\n---\n")
    # non-prime: the row's session id keys the latch (row wins the fallback).
    prime, sid = hook._seat_latch_identity(graph, "probe-director", "fallback")
    assert prime is False and sid == "a1b2c3d4-1111-2222-3333-444455556666"
    lp = hook._latch_path(graph, "probe-director", 7, session_id=sid, prime=prime)
    assert lp.name == "hook-probe-director-a1b2c3d4.lock", lp
    # prime: the gen key is unchanged, byte for byte.
    prime, sid = hook._seat_latch_identity(graph, "belam", "")
    assert prime is True
    lp = hook._latch_path(graph, "belam", 20, session_id=sid, prime=prime)
    assert lp.name == "hook-belam-gen20.lock", lp


# --------------------------------------------------------------------------
# SL7.23 continuation — gate (b) is THE point: prove ALL THREE merge-up
# signals HOLD (not just the suite lock), and choose+prove the latch-stale-
# on-failure behaviour. gate (b)'s MERGE_HEAD and unpushed-commit signals
# require a REAL git repo (a gitless fixture degrades only to "clean", which
# proves gates do not FALSELY hold but not that a real blocker Holds).
# --------------------------------------------------------------------------

def _git_run(repo: Path, *args: str):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


def _dead_pid() -> int:
    """A pid PROVED dead: spawn a short-lived child, reap it, return its pid.
    A reaped child's pid cannot be killed with signal 0 (ProcessLookupError),
    so `_pid_alive` reads it dead — deterministic, unlike a hard-coded
    999999, which can be a live process on a box whose pid space reaches it
    (this one's /proc/sys/kernel/pid_max is 4194304)."""
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
    proc.wait(timeout=10)
    pid = proc.pid
    # prove the reap: the pid must read dead to the same idiom `_pid_alive`.
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    return pid


def _real_repo_with_seat(tmp_path):
    """A REAL git repo at `<tmp>/outer/repo` whose graph root is `<repo>/.agi`
    and which carries the over-line `probe-director` seat — git measurements
    no longer degrade to clean, so gate (b)'s git-backed signals can HOLD."""
    outer = tmp_path / "outer"
    repo = outer / "repo"
    repo.mkdir(parents=True)
    _git_run(repo, "init", "-q", "-b", "master")
    _git_run(repo, "config", "user.email", "t@example.com")
    _git_run(repo, "config", "user.name", "t")
    (repo / "seed").write_text("x\n")
    _git_run(repo, "add", "seed")
    _git_run(repo, "commit", "-q", "-m", "seed")

    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.47\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotate_at\": 0.4}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return repo, graph, cwd


def _over_line_run(graph, cwd, tp, state_dir, tmp_path, run_hook, monkeypatch, capsys):
    """Write an over-line transcript and run the hook (seat from AGI_SEAT)."""
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    _write_transcript(tp, 45_000)          # 0.45 >= 0.4 -> over the line
    state_dir.mkdir(exist_ok=True)
    return run_hook(_payload(graph, tp, "sess-gb", cwd=str(cwd)),
                    state_dir, monkeypatch, capsys)


def test_merge_head_present_holds_rotation(tmp_path, run_hook, monkeypatch, capsys):
    """Signal (1) of gate (b): a REAL `.git/MERGE_HEAD` on the main checkout
    (a merge-up being performed RIGHT NOW) defers the rotation — the hook
    prints the deferral and does NOT rotate (_SPAWNS == [])."""
    repo, graph, cwd = _real_repo_with_seat(tmp_path)
    # a real merge state: MERGE_HEAD names a valid commit (HEAD).
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    (repo / ".git" / "MERGE_HEAD").write_text(head + "\n")
    tp = tmp_path / "mh.jsonl"
    code, out, err = _over_line_run(graph, cwd, tp, tmp_path / "state-mh",
                                    tmp_path, run_hook, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out          # the over-line banner still shows
    assert ("rotation deferred: merge-up in flight "
            "(merge in progress on MAIN)") in out, out
    assert _SPAWNS == []                   # the hook does NOT rotate mid-merge


def test_ahead_of_origin_is_info_not_a_captive(tmp_path, run_hook, monkeypatch, capsys):
    """Being AHEAD of origin on the season branch is NOT a merge in flight: the
    hook prints it as an INFO line and gate (b) does not hold. Under the old
    gate (b) this was labelled `unpushed merge commit on the season branch`, the
    normal state between pushes in a shared checkout, usually another seat's
    commit (hypothesis:...-merge-up-in-flight-means-a-real-merge, conjunct 3)."""
    repo, graph, cwd = _real_repo_with_seat(tmp_path)
    # the season branch, with a remote origin pushed and then one commit AHEAD.
    _git_run(repo, "checkout", "-q", "-b", "season/s2")
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    _git_run(repo, "remote", "add", "origin", str(bare))
    _git_run(repo, "push", "-q", "-u", "origin", "season/s2")
    (repo / "season-note").write_text("ahead\n")
    _git_run(repo, "add", "season-note")
    _git_run(repo, "commit", "-q", "-m", "unpushed commit")
    # sanity: origin/season/s2..season/s2 really is non-zero
    n = subprocess.run(["git", "-C", str(repo), "rev-list", "--count",
                        "origin/season/s2..season/s2"],
                       capture_output=True, text=True, check=True).stdout.strip()
    assert n == "1", n
    # THE FALSIFIER: ahead-only is NOT a merge in flight.
    assert hook._merge_in_flight(graph) is None
    assert hook._season_unpushed_count(graph) == 1   # ...but it IS measured
    tp = tmp_path / "up.jsonl"
    code, out, err = _over_line_run(graph, cwd, tp, tmp_path / "state-up",
                                    tmp_path, run_hook, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    assert ("info: 1 unpushed commit(s) on season/s2 "
            "(not a merge in flight)") in out, out
    # the old label is GONE: no captivation, no deferral, on the ahead-only
    # signal. (prepare's own unpushed check may still hold the rotation — a
    # different captive, named as prepare's, never as a merge in flight.)
    assert "merge-up in flight (unpushed merge commit" not in out, out
    assert "(merge in progress on MAIN)" not in out, out


def test_clean_real_git_repo_rotates(tmp_path, run_hook, monkeypatch, capsys):
    """A REAL git repo with NO merge-up signal (no MERGE_HEAD, no suite lock,
    nothing ahead of origin) and a genuinely CLEAN tree + fresh card: every
    gate honestly passes, and the hook DOES rotate — proving the deferrals
    above were the signals HOLDING, not an always-git-deferral."""
    repo, graph, cwd = _real_repo_with_seat(tmp_path)
    # the graph + a fresh card, COMMITTED so the tree is genuinely clean, and
    # master pushed to origin so gate (c)'s `no upstream` captive is cleared.
    card = graph / "sessions" / "quorum" / "probe-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# probe-director card (fresh)\n")
    _git_run(repo, "add", "-A")
    _git_run(repo, "commit", "-q", "-m", "graph + card")
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    _git_run(repo, "remote", "add", "origin", str(bare))
    _git_run(repo, "push", "-q", "-u", "origin", "master")
    # card mtime bumped past the last WORK commit -> gate (a) reads it fresh.
    os.utime(card, (2_000_000_000, 2_000_000_000))
    # sanity: the same gates the hook runs are clean
    assert hook._merge_head_present(graph) is False
    assert hook._suite_lock_held(graph) is False
    assert hook._season_unpushed(graph) is False
    assert hook._prepare_other_captives(graph, "probe-director") == []
    tp = tmp_path / "cl.jsonl"
    code, out, err = _over_line_run(graph, cwd, tp, tmp_path / "state-cl",
                                    tmp_path, run_hook, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    assert len(_SPAWNS) == 1, _SPAWNS     # clean real repo rotates exactly once
    assert "rotation: spawned rotate-self" in out, out
    assert "rotation deferred" not in out


# --- latch-stale-on-failure: a DEAD holder releases, a LIVE one holds --------
def test_dead_latch_is_released_and_rerotates(tmp_path, run_hook, monkeypatch, capsys):
    """The latch records the ROTATE-SELF pid. A latch whose holder pid is DEAD
    (a rotate-self that FAILED mid-flight — the exact hole the parent named)
    is released as stale, and a clean-state seat re-rotates on the NEXT prompt
    instead of being latched out of auto-retry for the whole generation."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    tp = tmp_path / "dead.jsonl"
    _write_transcript(tp, 45_000)            # 0.45 >= 0.4 -> over the line
    # FIRST prompt: clean -> rotates, leaves a latch naming the rotate-self pid.
    state_dir = tmp_path / "state-dead"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-dead", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out, out
    assert len(_SPAWNS) == 1, (out, _SPAWNS)
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-dea.lock"
    assert latch.exists()
    assert hook._latch_holder_pid(latch) == _RECORDER_PID  # the ROTATE-SELF pid

    # SIMULATE the mid-flight failure: its holder dies.
    monkeypatch.setattr(hook, "_pid_alive", lambda pid: False)
    # _SPAWNS is read back by the run; clear for the second prompt's proof.
    _SPAWNS.clear()
    code, out, err = run_hook(_payload(graph, tp, "sess-dead", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    # NOT deferred by a stale latch — the seat retries.
    assert "already rotating" not in out, out
    assert len(_SPAWNS) == 1, _SPAWNS     # the failed generation is NOT latched
    assert "rotation: spawned rotate-self" in out, out

# --------------------------------------------------------------------------
# SL7.32 — the meter hook's latch never lands as tracked churn in MAIN, the
# stale-latch release runs BEFORE gate (c), a worktree seat never writes its
# latch into MAIN's tree, and the rotate-self launch goes through ONE seam no
# test can fire live (hypothesis:l4-the-meter-hook-latch-is-ignored-...).
# FIX-ONLY build round: each test FAILS the pre-fix bytes and passes the built
# ones. Fixtures name a THROWAWAY seat (probe-director), never a registered
# one (the c1f01e920 incident: a live rotate-self --stops for the
# sensei-director seat fired from a kid's pytest).
# --------------------------------------------------------------------------


def test_latch_path_resolves_to_seats_own_tree_not_main(tmp_path):
    """Fix #3 — a worktree seat's hook latch resolves OUTSIDE MAIN's tree (its
    OWN `<root>/sessions`), so a hook run in a worktree never writes its
    `hook-*.lock` into MAIN's checkout. The shared MAIN-sessions dir is what
    the pre-fix `_latch_path` used, so every worktree hook run left untracked
    churn under MAIN.

    Built on a REAL two-tree git fixture — a main repo and a checked-out
    worktree with its own `.agi/sessions` — so both trees genuinely resolve
    and the discriminator is real, not two fabricated paths on a gitless tmp
    tree (where `_shared_sessions_dir` degrades to the identity and the
    assertion cannot tell the seat's tree from main). FALSIFIER-proof: this
    FAILS if `_latch_path` is pointed back at the shared MAIN sessions dir."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("ra_latch", _HOOK)
    ra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ra)

    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _git_run(repo, "init", "-q", "-b", "master")
    _git_run(repo, "config", "user.email", "t@example.com")
    _git_run(repo, "config", "user.name", "t")
    (repo / "seed").write_text("x\n")
    _git_run(repo, "add", "seed")
    _git_run(repo, "commit", "-q", "-m", "seed")

    main_root = repo / ".agi"
    (main_root / "nodes" / ".geometry").mkdir(parents=True)
    (main_root / "config.json").write_text("{}")

    # a REAL worktree on its own branch, with its OWN `.agi/sessions` dir.
    wt_dir = repo / "worktrees" / "seat-demo"
    _git_run(repo, "worktree", "add", "-q", "-b", "wt-seat-demo",
             str(wt_dir))
    worktree = wt_dir / ".agi"
    (worktree / "nodes" / ".geometry").mkdir(parents=True)
    (worktree / "config.json").write_text("{}")
    (worktree / "sessions").mkdir(parents=True, exist_ok=True)

    latch = ra._latch_path(worktree, "demo", 3)
    assert latch.name == "hook-demo-gen3.lock", latch
    # the latch lives in the SEAT's OWN sessions dir ...
    assert str(latch).startswith(str((worktree / "sessions").resolve())), latch
    # ... and NEVER under MAIN's sessions dir (the pre-fix shared-sessions
    # target that made every worktree hook run leave untracked churn in MAIN).
    assert not str(latch).startswith(str((main_root / "sessions").resolve())), latch


def test_dead_latch_released_before_gate_c_captive(tmp_path, run_hook, monkeypatch, capsys):
    """Fix #2 — the stale-latch release (dead holder pid) runs BEFORE gate (c),
    so a dead-pid latch is released even on a prompt where a prepare captive
    HOLDS the rotation. Pre-fix the unlink sat inside gate (d), AFTER gate (c)
    returned, so a dead latch stranded behind a captive blocked every later
    rotation until a human removed it by hand."""
    repo, graph, cwd = _real_repo_with_seat(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    # a DIRTY tree makes gate (c) prepare's 'dirty' captive HOLD (listed,
    # never performed) while gate (b) stays clean.
    (repo / "dirty-marker").write_text("uncommitted\n")
    # a DEAD-pid latch (a REAPED child's pid, PROVED dead — never a hard-coded
    # 999999, which can be a live process on this box) for this seat + gen 0.
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-gc.lock"
    latch.parent.mkdir(parents=True, exist_ok=True)
    latch.write_text(f"pid {_dead_pid()}\n")
    tp = tmp_path / "gc.jsonl"
    _write_transcript(tp, 45_000)                 # 0.45 >= 0.4 → over the line
    state_dir = tmp_path / "state-gc"
    state_dir.mkdir(exist_ok=True)
    code, out, err = run_hook(_payload(graph, tp, "sess-gc", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "ROTATION OWED" in out
    # gate (c) held → no rotation, no spawn.
    assert _SPAWNS == [], (out, _SPAWNS)
    # ... BUT the dead latch is GONE: the stale release ran even though a
    # captive held below it (pre-fix it would still be sitting there).
    assert not latch.exists(), "dead latch was NOT released before gate (c)"


def test_spawn_launch_goes_through_the_popen_seam_and_no_spawn_honoured(
        tmp_path, run_hook, monkeypatch, capsys):
    """Fix #4 — `_spawn_rotate_self` launches through the ONE `_Popen` seam,
    and AGI_HOOK_NO_SPAWN short-circuits BEFORE the seam so no test (in- or
    out-of-process) can fire a REAL rotate-self. Pre-fix the production path
    called subprocess.Popen directly (c1f01e920: a live rotate-self --stops
    for the sensei-director seat fired from a kid's pytest)."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    calls = []

    class _Fake:
        pid = 424242

    def _record(argv, **kw):
        calls.append((argv, kw))
        return _Fake()

    monkeypatch.setattr(hook, "_Popen", _record)
    tp = tmp_path / "ns.jsonl"
    _write_transcript(tp, 45_000)
    state_dir = tmp_path / "state-ns"
    state_dir.mkdir(exist_ok=True)

    # With NO_SPAWN set, the hook DECLINES: it never claims the latch (no
    # fake pid 12345 ever latched), prints 'declined', and does not reach
    # the seam — an out-of-process run can never fire a real rotate-self.
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, out, err = run_hook(_payload(graph, tp, "sess-ns", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "declined: AGI_HOOK_NO_SPAWN" in out, out
    assert "rotation: spawned" not in out, out    # declined, NOT spawned
    assert calls == [], "AGI_HOOK_NO_SPAWN must short-circuit BEFORE _Popen"
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-ns.lock"
    assert not latch.exists(), "NO_SPAWN must write NO latch (ibid. phantom 12345)"
    # the argv stays provable via the builder even under NO_SPAWN (the
    # suppression never routes around the seam that carries the argv).
    bin_dir = Path(hook.__file__).resolve().parents[1] / "bin"
    argv_b = hook._rotate_self_argv(bin_dir, "probe-director", "stops: x")
    assert argv_b[0] == "python3" and "rotate-self" in argv_b

    # Without it, the SEAM (not a raw subprocess.Popen) is the launch point,
    # carrying the exact argv + detach flags the production path needs.
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN")
    code, out, err = run_hook(_payload(graph, tp, "sess-ns", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert calls, "production spawn did not go through the _Popen seam"
    argv, kw = calls[-1]
    assert "rotate-self" in argv, argv
    assert kw.get("start_new_session") is True, kw
    assert kw.get("stdout") is subprocess.DEVNULL, kw


def test_one_no_spawn_check_lives_in_gate_e_not_the_helper(
        tmp_path, monkeypatch):
    """Goal:g15.25 one-check claim — AGI_HOOK_NO_SPAWN is guarded by the ONE
    check, gate (e) in `_gated_rotate`, NOT by a second short-circuit inside
    `_spawn_rotate_self` (dead code that used to read as the fix). Two proofs:

    (1) a DIRECT call to the helper under NO_SPAWN now REACHES the seam: the
    recorder is called (the helper has no stealth env-var branch of its own),
    so the sole suppression lives in the caller — reached end to end through
    the production path covered by `test_spawn_launch_goes_through_the_popen_
    seam_and_no_spawn_honoured` / `test_out_of_process_no_spawn_declines_...`.
    (2) the recorder's sentinel pid is provably DEAD, so a latch left through
    the recorder path can never hold a generation against a phantom pid."""
    calls = []

    class _Fake:
        pid = _RECORDER_PID

    def _record(argv, **kw):
        calls.append((argv, kw))
        return _Fake()

    monkeypatch.setattr(hook, "_Popen", _record)
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    root = tmp_path / "g"
    root.mkdir(exist_ok=True)
    bin_dir = Path(hook.__file__).resolve().parents[1] / "bin"
    pid = hook._spawn_rotate_self(root, "probe-director", "stops: x")
    # (1) the helper reaches the seam even under NO_SPAWN — NO second check.
    assert calls, ("helper must reach the _Popen seam under NO_SPAWN; "
                   "the one NO_SPAWN check is gate (e) in the caller")
    assert calls[0][0][1].endswith("rotate.py"), calls[0][0]
    assert pid == _RECORDER_PID, pid
    # (2) the sentinel is provably dead — a recorder-path latch can't hold.
    assert hook._pid_alive(_RECORDER_PID) is False
    assert _RECORDER_PID != 12345


def test_out_of_process_no_spawn_declines_and_writes_no_latch(tmp_path):
    """Claim (d) — ONE OUT-OF-PROCESS test: run the hook as a real subprocess
    with AGI_HOOK_NO_SPAWN=1 against an over-line seat and assert NO latch,
    NO spawn, exit 0. A fresh interpreter imports this module with the REAL
    subprocess.Popen (the `_no_real_spawn` recorder is invisible here), so the
    only thing stopping a real rotate-self is the NO_SPAWN path itself — the
    exact production-pane hazard (an operator export leaking into the hook's
    env) the fix is for."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    tp = tmp_path / "oop.jsonl"
    _write_transcript(tp, 45_000)
    state_dir = tmp_path / "state-oop"
    state_dir.mkdir(exist_ok=True)
    driver = dedent(f'''\
        import importlib.util, json, sys
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("rotation_alert", {str(HOOK)!r})
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        payload = {{"hook_event_name":"UserPromptSubmit", "session_id":"sess-oop",
                    "transcript_path": {str(tp)!r}, "cwd": {str(cwd)!r}}}
        sys.stdin = __import__("io").StringIO(json.dumps(payload))
        raise SystemExit(m.main([]))
    ''')
    script = tmp_path / "oop_driver.py"
    script.write_text(driver)
    env = dict(os.environ)
    env["AGI_HOOK_NO_SPAWN"] = "1"
    env["AGI_ROTATION_STATE_DIR"] = str(state_dir)
    env.pop("AGI_POST", None)   # the runner's own post must not leak in
    env.pop("AGI_SEAT", None)
    env["AGI_SEAT"] = "probe-director"
    # The hook resolves seats rows through `graph_core.persistence.frontmatter`
    # (geometry_config.load_rows), which lives under src/ — on sys.path under
    # pytest (conftest), but a bare `python3` subprocess does NOT carry it, so
    # without this the seats row is unread and the seat falls to the ladder
    # default, never reaching over-line. Replicate the engine import surface.
    engine_src = Path(hook.__file__).resolve().parents[1] / "src"
    old_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(engine_src) + (os.pathsep + old_pp if old_pp else "")
    proc = subprocess.run([sys.executable, str(script)], capture_output=True,
                          text=True, env=env, timeout=60)
    # exit 0, the decline printed, and NO spawn message.
    assert proc.returncode == 0, proc.stdout[-600:] + proc.stderr[-600:]
    assert "declined: AGI_HOOK_NO_SPAWN" in proc.stdout, proc.stdout[-600:]
    assert "rotation: spawned" not in proc.stdout, proc.stdout[-600:]
    # NO latch written (the phantom 12345 must never land in a latch).
    latch = graph / "sessions" / "rotations" / "hook-probe-director-sess-oop.lock"
    assert not latch.exists(), "out-of-process NO_SPAWN still wrote a latch"
    # the manual rotate advice is still offered (suppression disables the
    # SPAWN, not the guidance) — and the decline only ever prints from the
    # over-line branch, proving the seat DID resolve and would have spawned.
    assert "ROTATION OWED" in proc.stdout
    assert "rotate.py" in proc.stdout

# --------------------------------------------------------------------------
# Round SL7.70 — the hook prints ONE compact [meter] line on EVERY prompt
# (hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-
# every-prompt). Fix-only build: the pre-fix bytes are SILENT below the first
# band and inside an already-fired band, so D1's "prints on every prompt"
# fails them and passes the built ones. D1 = unconditional meter line (last
# stdout line); D2 = band block unchanged ABOVE it; D3 = turn 1 estimated and
# labelled; D4 = P6 refusal reason in place of the fraction.
# --------------------------------------------------------------------------

def test_meter_line_prints_below_first_band(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """D1 — a prompt below the first band (currently silent in the body)
    prints the [meter] line as its WHOLE stdout. The meter is unconditional;
    the band escalation is what stays quiet below the line. The fixture seat
    is resolved (AGI_SEAT + computable pin) because claim (2) of
    experiment:a00-deae9b09-fb6c31 makes a seat-None prompt print `no-post`
    with NO fraction — the D1 fraction-line only belongs to a RESOLVED post."""
    monkeypatch.setenv("AGI_SEAT", "meter-director")
    transcript = tmp_path / "below.jsonl"
    _write_transcript(transcript, 5_000)          # 0.05 < band 0 (0.10)
    state_dir = tmp_path / "state-below"
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-below"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines, out
    assert lines[-1].startswith("[meter]"), out
    assert "post=meter-director" in lines[-1], lines[-1]
    assert "0.0500" in lines[-1], lines[-1]        # a real fraction, not est.
    assert "approaching rotation" not in out, out  # no band block below band
    assert "--session-log" not in lines[-1], lines[-1]  # meter never the command


def test_meter_line_last_stdout_line_after_band_crossing(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """D2 — a band-crossing prompt prints the band block AND the [meter] line,
    and the [meter] line is the LAST stdout line (asserted on the last
    non-empty line, not an `in`). Resolved seat: claim (2) makes a seat-None
    prompt print `no-post` with NO fraction."""
    monkeypatch.setenv("AGI_SEAT", "meter-director")
    transcript = tmp_path / "band.jsonl"
    _write_transcript(transcript, 20_000)         # 0.20 -> crosses band 0.70
    state_dir = tmp_path / "state-band"
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-band"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "approaching rotation" in out, out      # band block still prints
    assert "--session-log" in out
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines[-1].startswith("[meter]"), out    # meter is the LAST line
    assert "post=meter-director" in lines[-1], lines[-1]
    assert "0.2000" in lines[-1], lines[-1]


def test_turn_one_estimates_and_labels_meter(agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """D3 — turn 1 (no assistant usage yet) prints a labelled `est.` fraction
    as the [meter] line, never a blank, never a bare unlabelled 0.0000. The
    estimate is informational: NO band block fires from an estimate. Resolved
    seat (AGI_SEAT): claim (2) makes a seat-None prompt print `no-post` with
    NO fraction, so the estimate-fraction belongs to a RESOLVED post."""
    monkeypatch.setenv("AGI_SEAT", "meter-director")
    transcript = tmp_path / "turn1.jsonl"
    transcript.parent.mkdir(parents=True, exist_ok=True)
    # a transcript with ONLY a user message — no assistant usage to measure.
    transcript.write_text(json.dumps({"message": {"role": "user",
                                                  "content": "hi"}}) + "\n")
    state_dir = tmp_path / "state-turn1"
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-turn1"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines, out
    assert lines[-1].startswith("[meter]"), out
    assert "post=meter-director" in lines[-1], lines[-1]
    assert "est." in lines[-1], lines[-1]          # labelled estimate
    assert "0.0000" not in out, out                # never a bare unlabelled zero
    assert "approaching rotation" not in out, out  # no band block from estimate
    assert "--session-log" not in out, out


def test_missing_pin_prints_refusal_reason_not_fraction(tmp_path, run_hook, monkeypatch, capsys):
    """D4 — a RESOLVED seat whose pin cannot be computed refuses the number:
    the [meter] line reads `post=<post> no-pin`, with NO digit where the
    fraction would go (P6 stays fail-closed). FALSIFIER: a missing pin that
    still prints a fraction."""
    graph, cwd = _over_line_seat_fixture(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setattr(hook, "_canonical_pin", lambda *a, **k: None)
    tp = tmp_path / "nopin.jsonl"
    _write_transcript(tp, 5_000)          # 0.05 < band0 (0.16) -> silent body
    state_dir = tmp_path / "state-nopin"
    code, out, err = run_hook(_payload(graph, tp, "sess-nopin", cwd=str(cwd)),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines, out
    assert lines[-1].startswith("[meter]"), out
    assert len(lines) == 1, out           # silent body: meter is the whole stdout
    after = lines[-1].split("post=probe-director ", 1)[1]
    assert after.startswith("no-pin"), lines[-1]    # reason, owned by the seat
    assert not after[:1].isdigit(), lines[-1]       # no confident number

# --------------------------------------------------------------------------
# T1 + T2 of experiment:a00-83d5d0e0-bcf35b (SL7.70 kid 2) — PIN THE P7
# CARVE-OUT so no later kid 'fixes' the silent paths into a meter line, and
# SETTLE the mid-read OSError path by measuring it.
#
# The claim's word 'unconditionally' is FALSE on exactly the paths the hook's
# own P7 ("SILENT and exit 0 outside an agi project and on an unreadable
# transcript — this runs on every session on the box and must never break
# one", rotation_alert.py:36) requires to be silent. MEASURED on the real
# hook bytes by this round's parent (three live payloads) and re-measured on
# this base (experiment:a00-83d5d0e0-bcf35b):
#   * no transcript_path                -> rc 3, `[meter] post=n/a
#     no-transcript-path`  (fail-closed, P2)
#   * transcript_path does not exist    -> rc 0, stdout '' (no [meter])
#   * cwd outside an agi project        -> rc 0, stdout '' (no [meter])
#   * transcript exists but unreadable  -> rc 0, stdout '' (no [meter]), a
#     fail-closed reason on STDERR (measured: chmod-000, PermissionError)
# These tests make the silence DELIBERATE and NAMED (P7 + hypothesis id), so
# a later kid who reads 'unconditionally' cannot 'fix' it into a meter line
# emitted into every non-agi session on this box. hypothesis:
# l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt
# --------------------------------------------------------------------------

def test_p7_no_meter_outside_agi_project(run_hook, tmp_path, monkeypatch, capsys):
    """P7 — a payload whose cwd has no enclosing .agi holding a config prints
    NO [meter] at all (measurement, not inference):
    `cwd outside an agi project -> rc 0, stdout ''`. The claim's meter line is
    scoped INSIDE AN AGI PROJECT WITH A READABLE TRANSCRIPT; outside a project
    the hook is silent and exits 0 (P7) so it never breaks a session.
    hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-
    every-prompt. FALSIFIER: any [meter] token on stdout outside a project."""
    outside = tmp_path / "plain-no-agi"      # no .agi/config.json above it
    outside.mkdir(exist_ok=True)
    transcript = tmp_path / "x.jsonl"
    _write_transcript(transcript, 50_000)
    state_dir = tmp_path / "state-p7out"
    code, out, err = run_hook(_payload(outside, transcript, "sess-p7out",
                                       cwd=outside),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert out == ""                          # deliberate P7 silence
    assert "[meter]" not in out
    assert "--session-log" not in out


def test_p7_no_meter_transcript_does_not_exist(agi_project, run_hook, tmp_path,
                                               monkeypatch, capsys):
    """P7 — a transcript_path that does not exist on disk (so the hook cannot
    read it) prints NO [meter] at all (measurement, not inference):
    `transcript_path does not exist -> rc 0, stdout ''`. The claim's meter
    line needs a readable transcript; a missing one is P7 silence (if the
    hook were to emit a meter line it would have to print for a measurement it
    never made). hypothesis:l4-the-rotation-alert-hook-prints-one-compact-
    meter-line-on-every-prompt. FALSIFIER: any [meter] token on stdout for a
    missing transcript."""
    missing = tmp_path / "no-such-transcript.jsonl"  # does not exist on disk
    state_dir = tmp_path / "state-p7miss"
    code, out, err = run_hook(_payload(agi_project, missing, "sess-p7miss"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert out == ""                          # deliberate P7 silence
    assert "[meter]" not in out
    assert "--session-log" not in out


def test_mid_read_oserror_is_p7_silence_not_claim(agi_project, run_hook,
                                                  tmp_path, monkeypatch,
                                                  capsys):
    """T2 — a transcript that EXISTS but whose mid-read open() raises OSError
    (permission lost between is_file() and open(); measured for real with a
    chmod-000 file -> rc 0, stdout '', 'cannot read transcript' on stderr) is
    P7 SILENCE, not the claim: the claim is scoped to 'INSIDE AN AGI PROJECT
    WITH A READABLE TRANSCRIPT', and an unreadable transcript is explicitly
    outside it. The hook must NOT print a [meter] line on stdout for a number
    it could not read; the fail-closed reason goes to stderr (P6 never a
    confident fraction, P7 never a broken session). Deterministic via the
    `_latest_usage` seam (an unreadable real file is environment-dependent:
    root bypasses 000). FALSIFIER: a [meter] line on stdout when
    _latest_usage raises. hypothesis:l4-the-rotation-alert-hook-prints-one-
    compact-meter-line-on-every-prompt."""
    transcript = tmp_path / "readable-once.jsonl"
    _write_transcript(transcript, 5_000)     # would read fine if not broken

    def _raise(_tp):
        raise OSError("simulated mid-read failure")

    monkeypatch.setattr(hook, "_latest_usage", _raise)
    state_dir = tmp_path / "state-oserr"
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-oserr"),
                              state_dir, monkeypatch, capsys)
    assert code == 0                    # P7: never break the session
    assert "[meter]" not in out         # a number we could not read: never
    assert out == ""
    assert "cannot read transcript" in err      # fail-closed reason, on stderr

# --------------------------------------------------------------------------
# Round SL7.94 — experiment:a00-deae9b09-fb6c31 (hypothesis:l4-the-rotation-
# alert-hook-checks-the-project-first-prints-no-fraction-without-a-post-
# estimates-from-the-prompt-field-and-imports-rotate-lazily). Four FIX-ONLY
# edits to pointer the hook at claim (1)-(4):
#   (1) P7 outside-project check runs BEFORE the rc-3 no-transcript refusal —
#       outside a project the hook exits 0 and prints NOTHING whatever the
#       payload (tests a1/a2 below);
#   (2) no post resolved = NO fraction — the [meter] reads `post=n/a no-post`
#       (test c2);
#   (3) the turn-1 estimate counts len(payload['prompt']) + transcript bytes,
#       never the whole JSON envelope (test d2);
#   (4) `import rotate` is deferred to the over-line paths that need it — a
#       pin-only prompt must not execute it (test e2 poisons the import).
# Existing test (b) `test_b_missing_transcript_fails_closed` (rc 3 inside a
# project, kept) and test (f) `test_missing_pin_prints_refusal_reason_not_
# fraction` (known seat, pin absent -> `no-pin`, kept) already cover claims
# (1)-inside and (2)-pin-missing; they are unchanged.
# --------------------------------------------------------------------------

def test_a1_outside_project_no_transcript_is_silent(run_hook, tmp_path,
                                                    monkeypatch, capsys):
    """claim (1) / P7 — outside an agi project the hook exits 0 and prints
    NOTHING whatever the payload, even ONE with no transcript_path. Pre-fix
    this returned rc 3 with a `[meter] no-transcript-path` refusal; the fix
    runs the P7 project check FIRST so a non-project session is never
    bothered. FALSIFIER: any stdout (a refusal or a [meter]) outside a
    project."""
    outside = tmp_path / "plain-no-agi"
    outside.mkdir(exist_ok=True)
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": "s-a1",
               "cwd": str(outside)}            # NO transcript_path
    state_dir = tmp_path / "state-a1"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert out == ""                            # P7 silence, whatever payload
    assert "no-transcript-path" not in out


def test_a2_inside_project_no_transcript_refuses(run_hook, tmp_path,
                                                 monkeypatch, capsys):
    """claim (1) — the rc-3 no-transcript refusal is KEPT, but only INSIDE an
    agi project. Same payload as test_a1 with a project root."""
    inside = tmp_path / "proj" / "graph" / ".agi"
    inside.mkdir(parents=True)
    (inside / "config.json").write_text("{}")
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": "s-a2",
               "cwd": str(inside)}             # NO transcript_path
    state_dir = tmp_path / "state-a2"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 3, err
    assert "no \"transcript_path\"" in err or "fail-closed" in err
    assert "--session-log" not in out           # no command, no fraction


def test_c2_no_post_prints_unresolved_label_no_fraction(agi_project, run_hook,
                                                       tmp_path, monkeypatch,
                                                       capsys):
    """claim (2) FALSIFIER — with NO post resolved the [meter] reads the
    unresolved label (`post=n/a`) and the refusal `no-post`, with NO decimal
    where a fraction would go. Pre-fix, seat None (bool(seat) False) made
    pin_missing False, so a FRACTION was printed for an unresolved seat."""
    transcript = tmp_path / "nopost.jsonl"
    _write_transcript(transcript, 5_000)        # 0.05 -> below first band
    state_dir = tmp_path / "state-nopost"
    # AGI_SEAT is cleared by the autouse fixture: the agi_project cwd is not
    # a seat-/post-* worktree, so NO seat resolves.
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-nopost"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines and lines[-1].startswith("[meter]"), out
    assert "post=n/a" in lines[-1], lines[-1]     # the unresolved label
    after = lines[-1].split("post=n/a ", 1)[1]
    assert after.startswith("no-post"), lines[-1]  # the refusal reason
    assert not after[7:8].isdigit(), lines[-1]     # no digit in the fraction slot


def test_d2_est_counts_prompt_field_not_envelope(agi_project, tmp_path,
                                                 monkeypatch, capsys):
    """claim (3) — the turn-1 estimate counts len(payload['prompt']) + the
    transcript BYTES, NEVER len(raw) (the whole JSON envelope). Assert the
    exact `<est>/<window>` from a KNOWN prompt length and a KNOWN transcript
    size. Pre-fix est = int((len(raw) + bytes)/4) included the ~200-byte
    envelope, so a 10-char prompt overestimated by the envelope each turn."""
    monkeypatch.setenv("AGI_SEAT", "meter-director")
    tp = tmp_path / "turn1-est.jsonl"
    content = json.dumps({"message": {"role": "user", "content": "hi"}}) + "\n"
    tp.write_text(content, encoding="utf-8")
    size = len(content.encode("utf-8"))           # KNOWN transcript bytes
    prompt = "p" * 37                             # KNOWN prompt length
    state_dir = tmp_path / "state-est"
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": "s-est",
               "transcript_path": str(tp), "cwd": str(agi_project),
               "prompt": prompt}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    code = hook.main([])
    cap = capsys.readouterr()
    assert code == 0, cap.err
    lines = [ln for ln in cap.out.splitlines() if ln.strip()]
    assert lines and lines[-1].startswith("[meter]"), cap.out
    est = int((len(prompt) + size) / 4)           # the PROMPT, not the envelope
    assert f"({est}/100000)" in lines[-1], lines[-1]
    assert "est." in lines[-1], lines[-1]


def test_e2_poisoned_rotate_import_still_prints_pin_only(agi_project, run_hook,
                                                         tmp_path, monkeypatch,
                                                         capsys):
    """claim (4) FALSIFIER — `import rotate` must NOT be reachable from the
    pin-only prompt. Poison sys.modules['rotate'] = None so the next
    `import rotate` raises ImportError: a below-band prompt with a resolved
    post and a computable pin must STILL print the [meter] fraction. Pre-fix,
    `_canonical_pin` imported rotate on every prompt, so the poison broke it
    into a `no-pin` refusal."""
    monkeypatch.setenv("AGI_SEAT", "meter-director")
    monkeypatch.setitem(sys.modules, "rotate", None)   # any `import rotate` raises
    transcript = tmp_path / "pinonly.jsonl"
    _write_transcript(transcript, 5_000)               # 0.05 -> pin-only path
    state_dir = tmp_path / "state-pinonly"
    code, out, err = run_hook(_payload(agi_project, transcript, "sess-pinonly"),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines and lines[-1].startswith("[meter]"), out
    after = lines[-1].split("post=meter-director ", 1)[1]
    assert after[:1].isdigit(), lines[-1]              # a real fraction, from the pin
    assert "no-pin" not in lines[-1], lines[-1]        # the pin was computable
    assert "no-post" not in lines[-1], lines[-1]


# ═══════════════════════════════════════════════════════════════════════════
# hypothesis:l5 conjunct 2+3 — the [meter] hook auto-posts a nudge's verified
# bodies into the chat IN THIS TURN when the prompt is the machine wake head
# for `<self>`; an owner-typed prompt never consumes (the gate).
# ═══════════════════════════════════════════════════════════════════════════


def test_l5_nudge_prompt_auto_posts_delivered_in_this_turn(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct 2+3 — a prompt beginning with the machine wake
    head for `<self>` (seat 'a' from cwd) runs the ONE `send.py read <self>`
    (the `_run_send_read` seam, so no real subprocess) and appends the VERIFIED
    body NAMED as delivered-in-this-turn, plus a do-not-read-again line (F25);
    the [meter] line still prints last."""
    calls = []
    def _fake(bin_dir, seat):
        calls.append(seat)
        return "VERIFIED seat-a (ed25519)\n  hello from sender\n"
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)              # 0.12 -> below band
    state_dir = tmp_path / "state-l5"
    payload = _payload(agi_project, transcript, "sess-l5", cwd=str(cwd))
    payload["prompt"] = "[agi-nudge] unread for a: send.py read a"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert calls == ["a"], f"the ONE read must run for self: {calls}"
    assert "DELIVERED IN THIS TURN" in out, out
    assert "VERIFIED seat-a (ed25519)" in out, out
    assert "Do NOT read again this turn (F25)." in out
    assert "[meter]" in out, "the meter must still print"
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines[-1].startswith("[meter]"), "the meter must stay the LAST line"


def test_l5_owner_typed_prompt_never_consumes(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct 2 GATE — a prompt that does NOT begin with the
    machine wake head for `<self>` (an owner-typed message) must NOT run the
    auto-read nor emit any delivery context (the inbox is never touched)."""
    calls = []
    def _fake(bin_dir, seat):
        calls.append(seat)
        return "VERIFIED seat-a (ed25519)\n"
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)
    state_dir = tmp_path / "state-gate"
    payload = _payload(agi_project, transcript, "sess-gate", cwd=str(cwd))
    payload["prompt"] = "What is the current status of the rotation?"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert calls == [], "owner-typed prompt must never run the auto-read"
    assert "DELIVERED IN THIS TURN" not in out


# ═══════════════════════════════════════════════════════════════════════════
# hypothesis:l5 conjunct 1+3 — the auto-post never consumes what it cannot
# deliver. (a) an empty body (timeout or a mail-less inbox) is NOT claimed as
# delivered — no DELIVERED banner, no F25 suppression, ONE undelivered line, and
# no consume; (b) a turn missing transcript_path never touches the inbox;
# (c) committed fixtures for the byte-cap truncate branch and the NO_SPAWN
# decline branch.
# ═══════════════════════════════════════════════════════════════════════════


def test_l5_empty_body_is_not_delivered(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct (a) — `_run_send_read` returning an EMPTY body
    (a timeout and a genuinely mail-less inbox both read back as '' from the
    seam) must NOT be claimed as delivered: no DELIVERED banner, no F25
    do-not-read-again suppression, exactly the ONE undelivered line, and the
    inbox left unconsumed (nothing suppressed). Never raises (exit 0)."""
    calls = []
    def _fake(bin_dir, seat):
        calls.append(seat)
        return ""                       # timeout / mail-less inbox
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)
    state_dir = tmp_path / "state-empty"
    payload = _payload(agi_project, transcript, "sess-empty", cwd=str(cwd))
    payload["prompt"] = "[agi-nudge] unread for a: send.py read a"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert calls == ["a"], "the ONE read must still run for self"
    assert "DELIVERED IN THIS TURN" not in out, out
    assert "Do NOT read again this turn (F25)." not in out, out
    assert out.count("NOT delivered") == 1, f"exactly ONE undelivered line: {out}"
    assert "[meter]" in out, "the meter must still print"


def test_l5_missing_transcript_never_consumes(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct (b) — a turn MISSING transcript_path refuses at
    rc-3 WITHOUT ever running the auto-post (the call now sits AFTER the
    fail-closed required-field gate, so the inbox is untouched on a refusal)."""
    calls = []
    def _fake(bin_dir, seat):
        calls.append(seat)
        return "VERIFIED seat-a (ed25519)\n"
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    state_dir = tmp_path / "state-missing"
    payload = _payload(agi_project, tmp_path / "sess.jsonl",
                       "sess-missing", cwd=str(cwd))
    del payload["transcript_path"]     # the fail-closed field is absent
    payload["prompt"] = "[agi-nudge] unread for a: send.py read a"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 3, f"must refuse with rc-3: {err}"
    assert calls == [], "a refusing turn must never run the auto-read"
    assert "DELIVERED IN THIS TURN" not in out, out


def test_l5_byte_cap_truncate_fixture(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct (c) committed fixture — a body big enough that
    the assembled text exceeds `_AUTOPOST_BYTE_CAP` takes the truncate branch:
    the delivered banner prints once plus a named 'exceeds byte cap' tail line."""
    def _fake(bin_dir, seat):
        return "VERIFIED seat-a (ed25519)\n" + "x" * (hook._AUTOPOST_BYTE_CAP + 5000)
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)
    state_dir = tmp_path / "state-cap"
    payload = _payload(agi_project, transcript, "sess-cap", cwd=str(cwd))
    payload["prompt"] = "[agi-nudge] unread for a: send.py read a"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert "exceeds byte cap" in out, out
    assert "DELIVERED IN THIS TURN" in out, out


def test_l5_no_spawn_declines_never_reads(
        agi_project, run_hook, tmp_path, monkeypatch, capsys):
    """hypothesis:l5 conjunct (c) committed fixture — AGI_HOOK_NO_SPAWN set
    makes a nudge print the 'NOT auto-read' decline and return without EVER
    running the read (no subprocess path)."""
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    calls = []
    def _fake(bin_dir, seat):
        calls.append(seat)
        return "VERIFIED seat-a (ed25519)\n"
    monkeypatch.setattr(hook, "_run_send_read", _fake)
    cwd = agi_project.parent / "worktrees" / "seat-a"
    cwd.mkdir(parents=True)
    transcript = tmp_path / "sess.jsonl"
    _write_transcript(transcript, 12_000)
    state_dir = tmp_path / "state-nospawn"
    payload = _payload(agi_project, transcript, "sess-nospawn", cwd=str(cwd))
    payload["prompt"] = "[agi-nudge] unread for a: send.py read a"
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert calls == [], "NO_SPAWN must decline BEFORE the read ever runs"
    assert "NOT auto-read (AGI_HOOK_NO_SPAWN)" in out, out
    assert "DELIVERED IN THIS TURN" not in out, out


def test_capture_cluster_templates_preserve_exact_output():
    """The capture-declined, captured, and captive-deferred templates keep
    the original f-string bytes while routing all three through render()."""
    assert hook.render("rotation_alert", "capture_declined", seat="a") == \
        "rotation: capture for a declined (AGI_HOOK_NO_SPAWN)."
    assert hook.render("rotation_alert", "captured", seat="a", minutes=7,
                       line="stop: threshold") == \
        "rotation: CAPTURED a's final card (7 min stale): stop: threshold"
    assert hook.render("rotation_alert", "captive_deferred_body",
                       prefix=hook.DEFER_PREFIX, which="suite-lock-held") == \
        f"{hook.DEFER_PREFIX} (suite-lock-held) — the captive auto-rotate does not fire while that holds."
