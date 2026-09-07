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
