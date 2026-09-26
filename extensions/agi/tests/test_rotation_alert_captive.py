"""CAPTIVE AUTO-ROTATE trigger (a) -- the meter hook rotates the DIRECTOR at
`f >= captive_rotate_ratio x the seat's line`, no consent asked, the card as it
stands (AUTO-CAPTURED), no `card_capture_minutes` wait.

hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
(owner ruling 05:1xZ 09-19, slice 2, trigger (a)).

Red-first, build-order:
  (1) a DIRECTOR row at f >= ratio*threshold -> handoff + rotate-self --force
      argv recorded under AGI_HOOK_NO_SPAWN, stops naming the captive reason;
  (2) under the ratio -> no capture;
  (3) a NON-director row -> no capture;
  (4) a Prime row -> no capture;
  (5) a master seat -> excluded unless `captive_rotate_masters` is true;
  (6) the ratio is READ FROM THE LADDER (0.5 fires, 0.9 does not, at the same
      fraction);
  (7) a merge in flight -> no capture;
  (8) no `captive_rotate_*` cell at all -> the feature is OFF BY NAME.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_captive", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.delenv("AGI_SEAT", raising=False)
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)
    hook._CAPTURE_LOGGED.clear()


def _graph(tmp_path, extra="", row_role="director", row_name="probe-director",
           row_rotate_at=0.4):
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "capture_chain_log: capture-chain.log\n" + extra + "---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        f"  - {{\"name\": \"{row_name}\", \"role\": \"{row_role}\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotated_by\": \"sanctuary-director\", "
        f"\"rotate_at\": {row_rotate_at}}}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return graph, cwd


def _transcript(path, tokens):
    path.write_text(json.dumps({"message": {"role": "assistant", "usage": {
        "input_tokens": tokens, "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0}}}) + "\n")


def _run(capsys, monkeypatch, graph, cwd, tokens, session="s-cap",
         state=None):
    state = state or (graph.parent / "state")
    state.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state))
    tp = graph.parent / f"{session}.jsonl"
    _transcript(tp, tokens)
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": session,
               "transcript_path": str(tp), "cwd": str(cwd)}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    code = hook.main([])
    return code, capsys.readouterr()


def _captures():
    return [a for a in hook._CAPTURE_LOGGED
            if "handoff" in a or "rotate-self" in a]


def test_captive_ratio_fires_for_director_vector(tmp_path, capsys, monkeypatch):
    """(1) probe-director rotate_at 0.4, ratio cell 0.5 -> captive at 0.2;
    f=0.42 fires. NO_SPAWN records handoff THEN rotate-self --force --stops,
    and the stops line names the captive reason (not the 10-min stale one)."""
    graph, cwd = _graph(tmp_path, extra="captive_rotate_ratio: 0.5\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    got = _captures()
    assert len(got) == 2, hook._CAPTURE_LOGGED
    handoff, rot = got
    assert handoff[2:5] == ["handoff", "--driven", "--seat"], handoff
    assert "rotate-self" in rot and "--force" in rot, rot
    stops = rot[rot.index("--stops") + 1]
    assert "captive ratio 0.5 x the line" in stops, stops
    assert "no self-rotate" in stops, stops


def test_captive_below_the_ratio_is_silent(tmp_path, capsys, monkeypatch):
    """(2) f=0.1 < 0.5*0.4 -> no capture at all."""
    graph, cwd = _graph(tmp_path, extra="captive_rotate_ratio: 0.5\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 10_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_captive_never_fires_for_a_non_director(tmp_path, capsys, monkeypatch):
    """(3) role `parent` at f=0.42 >= 0.2 -> no capture."""
    graph, cwd = _graph(tmp_path, extra="captive_rotate_ratio: 0.5\n",
                        row_role="parent")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_captive_never_fires_for_the_prime(tmp_path, capsys, monkeypatch):
    """(4) role `prime_director` at f=0.42 >= 0.2 -> no capture."""
    graph, cwd = _graph(tmp_path, extra="captive_rotate_ratio: 0.5\n",
                        row_role="prime_director")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_master_excluded_but_opt_in_by_the_ladder_cell(tmp_path, capsys,
                                                       monkeypatch):
    """(5) a seat whose name contains `master` is eligible ONLY when
    `captive_rotate_masters` is true (default off)."""
    graph, cwd = _graph(tmp_path,
                        extra="captive_rotate_ratio: 0.5\n",
                        row_name="sanctuary-master")
    monkeypatch.setenv("AGI_SEAT", "sanctuary-master")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED

    graph2, cwd2 = _graph(tmp_path / "on",
                          extra="captive_rotate_ratio: 0.5\n"
                                "captive_rotate_masters: true\n",
                          row_name="sanctuary-master")
    monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(tmp_path / "on" / "state"))
    code, cap = _run(capsys, monkeypatch, graph2, cwd2, 42_000, session="s-on")
    assert code == 0, cap.err
    assert len(_captures()) == 2, hook._CAPTURE_LOGGED


def test_ratio_is_read_from_the_ladder(tmp_path, capsys, monkeypatch):
    """(6) cell 0.5 fires at f=0.5*threshold; cell 0.9 does not."""
    g05, c05 = _graph(tmp_path / "a", extra="captive_rotate_ratio: 0.5\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, g05, c05, 20_000, session="s-05")
    assert code == 0, cap.err
    assert len(_captures()) == 2, hook._CAPTURE_LOGGED

    hook._CAPTURE_LOGGED.clear()
    g09, c09 = _graph(tmp_path / "b", extra="captive_rotate_ratio: 0.9\n")
    _run(capsys, monkeypatch, g09, c09, 20_000, session="s-09")
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_merge_in_flight_blocks_the_captive(tmp_path, capsys, monkeypatch):
    """(7) a merge in flight is a HARD blocker: no capture, deferral named."""
    graph, cwd = _graph(tmp_path, extra="captive_rotate_ratio: 0.5\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setattr(hook, "_merge_in_flight", lambda *a, **k: "merge-up")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED
    assert "merge-up" in cap.out, cap.out


def test_no_captive_cell_is_off_by_name(tmp_path, capsys, monkeypatch):
    """(8) with neither `captive_rotate_ratio` nor `captive_rotate_masters`
    in the ladder the feature is OFF: an over-line director is NOT captured
    (the pre-existing imperative path is byte-identical)."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_masters_only_without_ratio_is_off_by_name(tmp_path, capsys, monkeypatch):
    """EF.22 conjunct 3: `captive_rotate_masters: true` with NO
    `captive_rotate_ratio` is OFF BY NAME -- not the pre-fix silent 0.85
    literal. f=0.42 >= 0.85*0.4 = 0.34, so the 0.85 fallback fired (RED-FIRST).
    """
    graph, cwd = _graph(tmp_path, extra="captive_rotate_masters: true\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_unparseable_ratio_is_off_by_name(tmp_path, capsys, monkeypatch):
    """EF.22 conjunct 3: an UNPARSEABLE `captive_rotate_ratio` is OFF BY NAME
    -- not the pre-fix silent 0.85 literal (RED-FIRST)."""
    graph, cwd = _graph(tmp_path,
                        extra="captive_rotate_ratio: not-a-number\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    code, cap = _run(capsys, monkeypatch, graph, cwd, 42_000)
    assert code == 0, cap.err
    assert _captures() == [], hook._CAPTURE_LOGGED


def test_hook_subprocess_reads_seat_rows_on_its_own_path(tmp_path):
    """Production-dead regression: executed directly (as `~/.claude/settings
    .json` does), the hook must put its own `src/` on sys.path. Without it
    `geometry_config.load_rows` silently returns [] and the captive gate can
    never read a role — the feature is dead in production while green here."""
    graph, _ = _graph(tmp_path)
    code = ("import importlib.util;"
            f"spec=importlib.util.spec_from_file_location('h', r'{HOOK}');"
            "h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);"
            f"print(len(h._seat_rows(r'{graph}')))")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, env=env, cwd="/tmp")
    assert out.stdout.strip() == "1", (out.stdout, out.stderr)
