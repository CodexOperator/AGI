"""Tests for `dispatch.py --dry-run` (hypothesis:l3-dispatch-dry-run).

The claim under test: `--dry-run` resolves EVERYTHING the live spawn path
resolves (target, tier, role, ladder tier, brief tier, model and effort rows,
env exports), assembles the brief, prints a compact report (quoted command,
env, brief tier, brief line count + first 20 lines) and exits 0 — WITHOUT
spawning, taking a spawn-budget slot, writing a manifest or a session dir, or
calling Popen.

These tests run dispatch.py as a real subprocess against a scratch project, so
exit codes and stdout are the ground truth, and the no-side-effect clauses are
checked on disk (`no sessions/ dir`) which is exactly the guarantee the
hypothesis names.

Run with `--harness claude-code` (the verify's advisor case: model + effort
routing, the advisor brief swap, the ultracode env gate) and `--harness pi`
(the other harness, prompt-segment spelling).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

LADDER = """---
current_season: 2
roles:
  - {"tier": 3, "role": "parent", "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "ultracode"}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""}
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
"""

CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "deepseek-v4", "parent": "glm-flash"},
        },
        "claude-code": {
            "adapter": "claude_code",
            "models": {"kid": "claude-sonnet-5", "parent": "claude-opus-5",
                       "director": "claude-fable-5-1"},
            "effort": {"director": "max"},
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A scratch agi project: `.agi/` with a config and a ladder roles table."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    return tmp_path


def _run(project: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(project), "1", *args],
        capture_output=True, text=True,
    )


def test_pi_dry_run_resolves_the_spawn_and_exits_zero(project):
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=pi" in out
    # the ladder tier-1 parent row resolves the pi model
    assert "--model" in out and "glm-flash" in out
    assert "brief_tier=parent" in out
    assert "no budget slot taken" in out


def test_pi_dry_run_creates_no_session_dir(project):
    _run(project, "--harness", "pi", "--tier", "parent",
         "--target", "hypothesis:x", "--dry-run")
    assert not (project / ".agi" / "sessions").exists(), (
        "a dry run must not create a session dir")


def test_claude_advisor_dry_run_resolves_model_effort_and_env(project):
    """The verify's advisor case: a tier-3 parent aimed at a vision node gets
    the advisor brief and the full ultracode spawn, resolved without
    spawning."""
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--ladder-tier", "3", "--target", "vision:alive", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out
    # the tier-3 parent ladder row -> claude-opus-5 / effort max / ultracode
    assert "--model claude-opus-5" in out
    assert "--effort max" in out
    # the ladder settings row is shell-quoted in the printed command (JSON
    # carries spaces, so shlex adds single-quote marks) — match the printed
    # spelling.
    assert "--settings '{\"ultracode\": true}'" in out
    # the advisor brief swap
    assert "brief_tier=advisor" in out
    # the ultracode env gate, shown in the exported env
    assert "CLAUDE_CODE_WORKFLOWS=1" in out
    assert "AGI_LADDER_TIER=3" in out
    assert "AGI_MODEL=claude-opus-5" in out
    # the brief is summarized, not printed in full
    assert "first 20:" in out


def test_claude_advisor_dry_run_creates_no_session_dir(project):
    _run(project, "--harness", "claude-code", "--tier", "parent",
         "--ladder-tier", "3", "--target", "vision:alive", "--dry-run")
    assert not (project / ".agi" / "sessions").exists(), (
        "a dry run must not create a session dir")
    assert not list((project / ".agi" / "nodes").rglob("experiment/*.md")), (
        "a dry run must not scaffold a node")


def test_dry_run_takes_no_budget_slot(project):
    """The budget is checked on disk: a dry run registers nothing live."""
    _run(project, "--harness", "pi", "--tier", "parent",
         "--target", "hypothesis:x", "--dry-run")
    budget_dir = project / ".agi" / "sessions" / ".spawn-budget"
    assert not budget_dir.exists(), (
        f"a dry run must not register a spawn-budget slot, but {budget_dir} exists")


def test_explicit_harness_flag_wins_over_ladder_row(project):
    """hypothesis:l3-dispatch-harness-flag-overridden — an explicit
    --harness claude-code must beat a ladder row that names pi (the tier-1
    parent row), and take claude-code's OWN parent model/effort, not the pi
    row's glm-flash model. One notice line names both harnesses."""
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out, out
    # the command line is a claude command with claude-code's own parent
    # model, NOT the pi row's glm-flash
    cmd_line = next(l.strip() for l in out.splitlines()
                    if l.strip().startswith("command:"))
    assert "claude -p" in cmd_line, out
    assert "--model claude-opus-5" in cmd_line, out
    assert "glm-flash" not in cmd_line, out
    # a notice names both the explicit and the ladder-row harness
    assert "overrides" in out and "claude-code" in out and "pi" in out, out


def test_ladder_row_wins_without_harness_flag(project):
    """Without --harness the ladder row still wins: a tier-3 parent row that
    names claude-code beats the config default harness (pi)."""
    r = _run(project, "--tier", "parent", "--ladder-tier", "3",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out, out
    assert "--model claude-opus-5" in out, out


def test_seat_row_wins_over_both_harness_and_ladder(project):
    """A --seat row keeps winning over BOTH an explicit --harness and the
    ladder row: the seat names pi while the explicit flag names claude-code,
    so the seat's pi harness must win."""
    seats = (project / ".agi" / "nodes" / ".geometry" / "seats.md")
    seats.write_text("---\nseats:\n"
                     "  - {name: liaison, tier: 1, role: parent, "
                     "harness: pi, model: ~z-ai/glm-flash-latest, "
                     "effort: \"\", settings: \"\"}\n---\n")
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--seat", "liaison", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=pi" in out, out
    assert "glm-flash" in out, out


def test_dry_run_exports_identity_and_readers_agree(project, monkeypatch):
    """hypothesis:l3-agent-id-never-exported — the JOINED contract.

    dispatch --dry-run resolves the real child env, so it must export the id
    it minted as both AGI_AGENT_ID and AGI_ACTOR. This test reads the
    PRODUCER's own output (not a value the test invented), then feeds exactly
    that env to the two READERS, send._detect_sender and write._default_actor,
    and asserts all three surfaces resolve to the one id. Green here means the
    suite is no longer testing a contract half by hand-constructing the other
    half's input — the shape test_send.py used to mask with
    monkeypatch.setenv.
    """
    import importlib.util
    import re as _re

    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    m_id = _re.search(r"\bAGI_AGENT_ID=(\S+)", out)
    m_actor = _re.search(r"\bAGI_ACTOR=(\S+)", out)
    assert m_id, f"dry-run env must export AGI_AGENT_ID:\n{out}"
    assert m_actor, f"dry-run env must export AGI_ACTOR:\n{out}"
    aid, actor = m_id.group(1), m_actor.group(1)
    assert aid.startswith("dry") and len(aid) >= 10, f"not an agent id: {aid}"
    assert actor == aid, "AGI_ACTOR must equal the minted agent id"

    # Feed the producer's OWN exported values to the readers — no invented id.
    monkeypatch.setenv("AGI_AGENT_ID", aid)
    monkeypatch.setenv("AGI_ACTOR", aid)
    monkeypatch.delenv("AGI_TMUX_WINDOW_NAME", raising=False)
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("USER", raising=False)

    sys.path.insert(0, str(BIN))
    loaded = {}
    for name in ("send", "write"):
        spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod  # dataclasses needs the module registered
        spec.loader.exec_module(mod)
        loaded[name] = mod
    assert loaded["send"]._detect_sender(None) == aid
    assert loaded["write"]._default_actor() == aid
