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