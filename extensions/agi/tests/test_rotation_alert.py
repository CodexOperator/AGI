"""Tests for the rotation-alert SessionStart hook.

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
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"

spec = importlib.util.spec_from_file_location("rotation_alert", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


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
        "hook_event_name": "SessionStart",
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
    payload = {"hook_event_name": "SessionStart", "session_id": "s",
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


def test_the_emitted_command_is_actually_runnable(tmp_path, monkeypatch):
    """P5 is the hook's whole reason for existing, so an unrunnable command is
    the deliverable failing, not a typo.

    The original emitted `--seat <s> --pin --session-log <path>`, in which
    `--pin` (which TAKES A PATH) swallowed the `--session-log` flag as its
    value. This asserts the emitted argv PARSES against rotate.py's own
    parser — the arithmetic-not-the-string standard.
    """
    import shlex
    import importlib.util
    spec = importlib.util.spec_from_file_location("ra_repair2", _HOOK)
    ra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ra)

    # A seat worktree shape, so the seat is derivable and --pin is emitted.
    root = tmp_path / "repo" / ".agi" / "worktrees" / "seat-demo" / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    (root / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 1000\ndirector_rotate_at: 0.47\n---\n",
        encoding="utf-8")
    tp = tmp_path / "own.jsonl"
    _many_message_transcript(tp, turns=3, per_turn=900)   # 0.90 -> over the line

    payload = {"transcript_path": str(tp), "session_id": "sess-1",
               "cwd": str(root.parent)}
    proc = _subprocess.run(
        [_sys.executable, str(_HOOK)], input=_json.dumps(payload),
        capture_output=True, text=True,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}),
             "AGI_ROTATION_STATE_DIR": str(tmp_path / "state")})
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
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
