"""A capture latch prints as a MEMORY, never as a HOLD, and the stamp write
merges onto a fresh read instead of clobbering a concurrent writer.

RED-FIRST on the pre-fix bytes (hypothesis:a-capture-latch-is-a-memory-never-
a-hold):
  (1) an over-line seating whose gate defers with `capture-latched` must NOT
      print the generic "while that holds" HOLD text;
  (2) every OTHER deferral keeps that text verbatim (the latch line is its
      own, not a rewrite of the shared suffix);
  (3) the latch's own line still names the latch and re-checks next prompt;
  (4) `_captive_rotate` still returns True for "captured"/"capture-no-spawn"
      and False for "capture-latched" (the quiet half stays pinned);
  (5) `_force_capture`'s stamp write RE-READS before writing, so a field a
      concurrent writer lands during the capture chain survives.
"""
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_latch_mem", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

HOLD_TEXT = "the hook is not rotating this seat while that holds"
LATCH_LINE = "not a hold"


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    hook._CAPTURE_LOGGED.clear()
    monkeypatch.setattr(hook, "_Popen", lambda argv, **_kw: None)


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


def _over_line(monkeypatch, tmp_path, session_id, which):
    """Run main() over the line with the gate deferring `which`."""
    _, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_POST", "probe-director")
    state = tmp_path / "state"
    state.mkdir(exist_ok=True)
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state))
    monkeypatch.setattr(hook, "_gated_rotate",
                        lambda *_a, **_kw: which)
    # trigger (a) runs BEFORE the over-line branch; neutralise it so the
    # branch under test is the one that prints.
    monkeypatch.setattr(hook, "_captive_rotate", lambda *_a, **_kw: False)
    tp = tmp_path / "t.jsonl"
    tp.write_text(json.dumps({"message": {"role": "assistant", "usage": {
        "input_tokens": 45_000, "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0}}}) + "\n")
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({
        "hook_event_name": "UserPromptSubmit", "session_id": session_id,
        "transcript_path": str(tp), "cwd": str(cwd)})))
    assert hook.main([]) == 0


def test_latched_over_line_seat_prints_no_hold_claim(tmp_path, monkeypatch,
                                                    capsys):
    """Falsifier 1: the latch is a memory of a capture that already ran, not a
    blocker — the pre-fix bytes printed the generic HOLD suffix here."""
    _over_line(monkeypatch, tmp_path, "s-1", "capture-latched")
    out = capsys.readouterr().out
    assert HOLD_TEXT not in out, out
    assert LATCH_LINE in out, out
    assert "capture-latched" in out, out


def test_every_other_deferral_keeps_the_hold_text(tmp_path, monkeypatch,
                                                  capsys):
    """Falsifier 2 (negative probe): only the latch got a new line; every
    other deferral's suffix is untouched."""
    _over_line(monkeypatch, tmp_path, "s-1", "merge-in-flight")
    out = capsys.readouterr().out
    assert HOLD_TEXT in out, out
    assert LATCH_LINE not in out, out


def test_captured_no_spawn_pins_true_latched_pins_false(tmp_path, monkeypatch):
    """Falsifier 4: the QUIET half of the predicate is pinned — only a capture
    that actually captured (or recorded under NO_SPAWN) may go quiet."""
    graph, _cwd = _graph(tmp_path)
    state = tmp_path / "state"
    state.mkdir()
    card = tmp_path / "card.md"
    card.write_text("card")
    ladder = {"captive_rotate_ratio": 0.5}
    calls = {"which": "captured"}

    def _fake_force(*_a, **_kw):
        return calls["which"]

    monkeypatch.setattr(hook, "_force_capture", _fake_force)
    monkeypatch.setattr(hook, "_merge_in_flight", lambda _r: "")
    monkeypatch.setattr(hook, "_suite_lock_held", lambda _r: False)
    monkeypatch.setattr(hook, "_captive_rotate_eligible", lambda *_a: True)
    for which, expected in (("captured", True),
                            ("capture-no-spawn", True),
                            ("capture-latched", False),
                            ("capture-no-log", False),
                            ("capture-failed", False)):
        calls["which"] = which
        got = hook._captive_rotate(graph, "probe-director", 0.9, 0.4, ladder,
                                   10, state, session_id="s-1")
        assert got is expected, (which, got)


def test_stamp_write_rereads_and_merges(tmp_path, monkeypatch):
    """Falsifier 5: a writer that lands DURING the capture chain must not have
    its field clobbered by the latch write."""
    state = tmp_path / "state"
    state.mkdir()
    stamp = state / "capture-seat.json"
    stamp.write_text(json.dumps({"first": 1, "other": "keep"}))
    card = tmp_path / "card.md"
    card.write_text("card")
    root = tmp_path / "proj" / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}")
    (root / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncapture_chain_log: capture-chain.log\n---\n")

    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)

    def _racy_spawn(*_a, **_kw):
        """The concurrent writer: a field lands after the top-of-call read."""
        blob = json.loads(stamp.read_text())
        blob["concurrent"] = "survivor"
        stamp.write_text(json.dumps(blob))
        return None

    monkeypatch.setattr(hook, "_spawn_capture_chain", _racy_spawn)
    which = hook._force_capture(root, "seat", card, 0.9, 10, state,
                                session_id="s-9")
    assert which == "captured", which
    blob = json.loads(stamp.read_text())
    assert blob.get("concurrent") == "survivor", blob
    assert blob.get("first") == 1, blob
    assert blob.get("session") == "s-9", blob
    assert isinstance(blob.get("captured"), int), blob


def test_session_field_is_written_only_when_session_given(tmp_path, monkeypatch):
    """Negative probe: the merge did not start writing `session` on its own."""
    state = tmp_path / "state"
    state.mkdir()
    stamp = state / "capture-seat.json"
    stamp.write_text(json.dumps({"first": 1}))
    card = tmp_path / "card.md"
    card.write_text("card")
    root = tmp_path / "proj" / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}")
    (root / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncapture_chain_log: capture-chain.log\n---\n")
    monkeypatch.setattr(hook, "_spawn_capture_chain", lambda *_a, **_kw: None)
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)
    which = hook._force_capture(root, "seat", card, 0.9, 10, state)
    assert which == "captured", which
    blob = json.loads(stamp.read_text())
    assert "session" not in blob, blob
    assert blob.get("first") == 1, blob
    assert blob.get("captured") <= time.time(), blob
