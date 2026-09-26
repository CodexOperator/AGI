"""The capture latch is keyed by the SESSION that captured, and a latched
capture never swallows the over-line IMPERATIVE.

RED-FIRST on the pre-fix bytes (hypothesis:a-capture-latch-is-keyed-by-
session-and-never-swallows-the-imperative):
  (1) a stamp naming ANOTHER session does not latch the caller;
  (2) a LEGACY stamp (no `session`) does not latch a named session;
  (3) a latched SAME-session capture over the line still prints the
      imperative block (the pre-fix `_captive_rotate` returned True on
      `capture-latched`, so main() returned before the imperative).
"""
import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_latch", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

EXPECTED = "ROTATE NOW: (a) write the card wholesale now"


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    hook._CAPTURE_LOGGED.clear()
    monkeypatch.setattr(hook, "_Popen", lambda argv, **_kw: None)


def _stamp(state_dir, seat, blob):
    (state_dir / f"capture-{seat}.json").write_text(json.dumps(blob))


@pytest.mark.parametrize("blob", [{"captured": 1, "session": "old"},
                                  {"captured": 1}])
def test_latch_is_keyed_by_the_session_that_captured(tmp_path, blob):
    """Falsifiers 1+2: a stamp naming another session (or none) reads as
    ABSENT for a named caller, so a successor is never latched from birth."""
    state = tmp_path / "state"
    state.mkdir()
    card = tmp_path / "card.md"
    card.write_text("card")
    _stamp(state, "seat", blob)
    which = hook._force_capture(tmp_path, "seat", card, 0.9, 10, state,
                               session_id="new")
    assert which != "capture-latched", which


def test_same_session_still_latches_once_per_session(tmp_path):
    """P7 holds: the session that captured is not captured twice."""
    state = tmp_path / "state"
    state.mkdir()
    card = tmp_path / "card.md"
    card.write_text("card")
    _stamp(state, "seat", {"captured": 1, "session": "me"})
    assert hook._force_capture(tmp_path, "seat", card, 0.9, 10, state,
                               session_id="me") == "capture-latched"


def _graph(tmp_path):
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "capture_chain_log: capture-chain.log\ncaptive_rotate_ratio: 0.5\n---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotate_at\": 0.4}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return graph, cwd


def test_latched_capture_still_prints_the_imperative(tmp_path, monkeypatch,
                                                     capsys):
    """Falsifier 3: a LATCHED seat above the line still gets the imperative."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_POST", "probe-director")
    tp = tmp_path / "t.jsonl"
    tp.write_text(json.dumps({"message": {"role": "assistant", "usage": {
        "input_tokens": 45_000, "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0}}}) + "\n")
    state = tmp_path / "state"
    state.mkdir()
    _stamp(state, "probe-director", {"captured": 1, "session": "s-1"})
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state))
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({
        "hook_event_name": "UserPromptSubmit", "session_id": "s-1",
        "transcript_path": str(tp), "cwd": str(cwd)})))
    assert hook.main([]) == 0
    out = capsys.readouterr().out
    assert EXPECTED in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out
