"""Tests for the meter hook's IMPERATIVE block + FORCE capture (conjuncts 1/2).

hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself

Red-first, build-order:
  (1) a payload at f >= line prints the imperative block (exact string);
  (2) an unread `rotate now` from the holder prints it BELOW the line;
  (3) a stale card N minutes after the first imperative -> handoff + rotate-self
      --force invoked, argv recorded, NOTHING spawned under AGI_HOOK_NO_SPAWN;
  (4) the captured card carries AUTO-CAPTURED and a non-empty stops line.
"""
import importlib.util
import io
import json
import os
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_cap", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

#: every argv the capture WOULD run through the ONE `_Popen` seam.
_SPAWNS: list[list[str]] = []


@pytest.fixture(autouse=True)
def _no_inherited_seat(monkeypatch):
    monkeypatch.delenv("AGI_SEAT", raising=False)


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)
    _SPAWNS.clear()
    hook._CAPTURE_LOGGED.clear()

    class _FakeProc:
        pid = 2 ** 24

    monkeypatch.setattr(hook, "_Popen",
                        lambda argv, **_kw: (_SPAWNS.append(argv), _FakeProc())[1])


@pytest.fixture
def run_hook():
    def _run(payload, state_dir, monkeypatch, capsys):
        monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        code = hook.main([])
        cap = capsys.readouterr()
        return code, cap.out, cap.err
    return _run


def _graph(tmp_path, extra=""):
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        + extra + "---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotate_at\": 0.4}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return graph, cwd


def _transcript(path, tokens):
    path.write_text(json.dumps({"message": {"role": "assistant", "usage": {
        "input_tokens": tokens, "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0}}}) + "\n")


def _payload(graph, tp, session, cwd):
    return {"hook_event_name": "UserPromptSubmit", "session_id": session,
            "transcript_path": str(tp), "cwd": str(cwd)}


EXPECTED = ("ROTATE NOW: (a) write the card wholesale now, (b) run python3 "
            "extensions/agi/bin/rotate.py rotate; nothing else this turn")


def test_imperative_at_or_over_the_line(tmp_path, run_hook, monkeypatch, capsys):
    """Conjunct 1: f >= line prints the imperative block verbatim, and the
    [meter] line stays the LAST stdout line."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    tp = tmp_path / "over.jsonl"
    _transcript(tp, 45_000)                     # 0.45 >= 0.4 -> over the line
    state_dir = tmp_path / "state-over"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-over", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out


def test_imperative_on_unread_rotate_now_below_the_line(tmp_path, run_hook,
                                                        monkeypatch, capsys):
    """Conjunct 1: an UNREAD `rotate now` in the seat's inbox prints the
    imperative block even below the line (0.10 < 0.25)."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    inbox = graph / "sessions" / "inbox" / "probe-director.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("---\nfrom: sanctuary-director\nrotate now\n")
    tp = tmp_path / "below.jsonl"
    _transcript(tp, 10_000)                     # 0.10 < 0.25
    state_dir = tmp_path / "state-below"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-below", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out


def _stale_state(tmp_path, graph, state_dir, minutes_ago=600):
    card = graph / "sessions" / "quorum" / "probe-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# probe-director card\n")
    os.utime(card, (1, 1))
    state_dir.mkdir(exist_ok=True)
    (state_dir / "capture-probe-director.json").write_text(
        json.dumps({"first": int(__import__("time").time()) - minutes_ago}))
    return card


def test_force_capture_after_n_minutes_records_argv(tmp_path, run_hook,
                                                    monkeypatch, capsys):
    """Conjunct 2: card stale 10 min after the first imperative -> the driven
    handoff AND rotate-self --force --stops are invoked; under
    AGI_HOOK_NO_SPAWN nothing is spawned, the argv is RECORDED."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-cap"
    _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "cap.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, "s-cap", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert [a for a in _SPAWNS if "rotate-self" in a or "handoff" in a] == []
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    handoff, rot = hook._CAPTURE_LOGGED
    assert handoff[2:5] == ["handoff", "--driven", "--seat"], handoff
    assert handoff[handoff.index("--seat") + 1] == "probe-director"
    assert "s3" in handoff and "s6" in handoff
    assert "rotate-self" in rot and "--force" in rot
    stops = rot[rot.index("--stops") + 1]
    assert "auto-captured at f=" in stops, stops
    assert "10 min without a self-rotate" in stops, stops


def test_captured_card_carries_auto_captured_marker(tmp_path, run_hook,
                                                    monkeypatch, capsys):
    """Conjunct 2 (4): the card the hook captures carries AUTO-CAPTURED and the
    generated stops line is non-empty (the successor knows it was not authored)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-marker"
    card = _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "marker.jsonl"
    _transcript(tp, 45_000)
    code, out, err = run_hook(_payload(graph, tp, "s-marker", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    text = card.read_text()
    assert text.startswith(hook.AUTO_CAPTURED), text
    rots = [a for a in _SPAWNS if "rotate-self" in a]
    assert len(rots) == 1, _SPAWNS
    assert len([a for a in _SPAWNS if "handoff" in a]) == 1, _SPAWNS
    stops = rots[0][rots[0].index("--stops") + 1]
    assert stops.strip(), "stops line must never be empty"
    assert "auto-captured at f=" in stops, stops
