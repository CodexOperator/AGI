"""CAPTURE SAFETY: the AUTO-CAPTURED marker never lands on a live card, the
capture latches once per seating, and the forced chain's output lands in a
DECLARED log instead of DEVNULL.

hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-
forced-rotation-is-logged-and-latched

RED-FIRST on the pre-fix bytes: `_force_capture` did
`card.write_text("AUTO-CAPTURED\\n" + card.read_text())` on the LIVE card path,
so a symlinked card (a quorum card symlinked into nodes/doc/<card>.md, restored
by director-engine gen 22) got the marker written THROUGH the link, above the
node's `---` -> FrontmatterError on the next read. The chain's stdout+stderr
went to DEVNULL, and nothing latched: every further prompt past the ratio in the
same seating captured again.
"""
import importlib.util
import io
import json
import os
import sys
import time
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_safety", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

_SPAWNS: list[list[str]] = []
_KWARGS: list[dict] = []


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    monkeypatch.delenv("AGI_SEAT", raising=False)
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)
    _SPAWNS.clear()
    _KWARGS.clear()
    hook._CAPTURE_LOGGED.clear()

    class _FakeProc:
        pid = 2 ** 24

    def _fake(argv, **kw):
        _SPAWNS.append(argv)
        _KWARGS.append(kw)
        return _FakeProc()

    monkeypatch.setattr(hook, "_Popen", _fake)


def _graph(tmp_path, extra=""):
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "capture_chain_log: capture-chain.log\n" + extra + "---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotated_by\": \"sanctuary-director\", "
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


def _symlinked_card(graph, state_dir, minutes_ago=600):
    """A quorum card that is a SYMLINK into a graph node (the live shape) and
    a capture stamp old enough to force."""
    node = graph / "nodes" / "doc" / "card-probe-director.md"
    node.parent.mkdir(parents=True, exist_ok=True)
    node.write_text("---\nid: doc:card-probe-director\ntype: doc\n---\n"
                    "# probe-director card\n\n## \u00a73 where it stops\n"
                    "old stop\n\n## \u00a76 banked\n")
    card = graph / "sessions" / "quorum" / "probe-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.symlink_to(node)
    os.utime(node, (1, 1))
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "capture-probe-director.json").write_text(json.dumps({
        "first": int(time.time()) - minutes_ago * 60, "session": "s-a"}))
    return card, node


def _run(tmp_path, monkeypatch, capsys, session, state_dir, graph, cwd,
         name="x"):
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    tp = tmp_path / f"{name}.jsonl"
    _transcript(tp, 45_000)                     # 0.45 >= 0.4, over the line
    monkeypatch.setattr(sys, "stdin", io.StringIO(
        json.dumps(_payload(graph, tp, session, cwd))))
    code = hook.main([])
    return code, capsys.readouterr()


def test_capture_never_writes_into_the_symlinked_card_node(
        tmp_path, monkeypatch, capsys):
    """Falsifier 1: capture once against a symlinked card — the NODE's first
    line is still `---` and the node still parses. Pre-fix the marker was
    written THROUGH the link, above the frontmatter."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    state_dir = tmp_path / "state-sym"
    card, node = _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "sym")
    assert code == 0, cap.err
    assert card.is_symlink(), "the card link itself is never touched"
    text = node.read_text()
    assert text.startswith("---\n"), text[:120]
    assert hook.AUTO_CAPTURED not in text, text[:200]


def test_the_capture_marker_rides_the_state_dir_not_the_card(
        tmp_path, monkeypatch, capsys):
    """Conjunct 1: the AUTO-CAPTURED record is a SIBLING state file, so the
    capture is still observable after the card is untouched."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    state_dir = tmp_path / "state-sib"
    _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "sib")
    assert code == 0, cap.err
    marker = state_dir / "capture-probe-director.captured"
    assert marker.is_file(), sorted(p.name for p in state_dir.iterdir())
    assert "auto-captured at f=" in marker.read_text()


def test_capture_latches_once_per_seating(tmp_path, monkeypatch, capsys):
    """Falsifier 2: a second prompt past the ratio in the SAME seating
    captures nothing. Pre-fix every prompt re-captured (3 captures, no
    rotation)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    state_dir = tmp_path / "state-latch"
    _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "latch1")
    assert code == 0, cap.err
    assert len(_SPAWNS) == 1, _SPAWNS
    spawned = len(_SPAWNS)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "latch2")

    assert code == 0, cap.err
    assert len(_SPAWNS) == spawned, "latched: a second prompt must not spawn"
    assert "latched" in cap.out, cap.out


def test_the_forced_chain_output_lands_in_a_declared_log(
        tmp_path, monkeypatch, capsys):
    """Conjunct 2: the ONE backgrounded chain's stdout+stderr go to a DECLARED
    log file under the hook's state dir, never to DEVNULL — a failed
    handoff -> rotate-self chain must leave a trace."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    state_dir = tmp_path / "state-log"
    _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "log")
    assert code == 0, cap.err
    assert len(_KWARGS) == 1, _KWARGS
    kw = _KWARGS[0]
    out = kw.get("stdout")
    assert out is not subprocess_devnull(), kw
    assert getattr(out, "name", out) == str(
        state_dir / "capture-chain.log"), kw
    assert kw.get("stderr") == out, kw


def test_the_chain_log_name_comes_from_the_ladder_cell_not_a_literal(
        tmp_path, monkeypatch, capsys):
    """config-max: the chain log NAME is the ladder cell `capture_chain_log`;
    a different cell value lands the chain output on a different file."""
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "card_capture_minutes: 10\ncapture_chain_log: chain-run-2.out\n---\n")
    cwd = str(graph.parent)
    state_dir = tmp_path / "state-cell"
    _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "cell")
    assert code == 0, cap.err
    assert len(_KWARGS) == 1, _KWARGS
    out = _KWARGS[0].get("stdout")
    assert getattr(out, "name", out) == str(state_dir / "chain-run-2.out"), _KWARGS


def test_capture_fails_closed_when_the_ladder_declares_no_log_cell(
        tmp_path, monkeypatch, capsys):
    """Absent is NOT a silent default: with no `capture_chain_log` cell the
    capture refuses rather than write the chain output to an unnamed file."""
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "card_capture_minutes: 10\n---\n")
    cwd = str(graph.parent)
    state_dir = tmp_path / "state-nocell"
    _symlinked_card(graph, state_dir)
    code, cap = _run(tmp_path, monkeypatch, capsys, "s-a", state_dir, graph,
                     cwd, "nocell")
    assert code == 0, cap.err
    assert _SPAWNS == [], "no chain may run with no declared log"
    assert "fail-closed" in cap.out and "capture_chain_log" in cap.out, cap.out


def subprocess_devnull():
    import subprocess
    return subprocess.DEVNULL
