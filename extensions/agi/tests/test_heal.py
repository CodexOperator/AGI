"""Tests for bin/heal.py's healer spawn.

Healing only runs when something has already gone wrong, which is exactly why
its defects survive: nobody watches the path that only fires on a bad day.
Both assertions below cover a bug that was live and silent until 2026-08-31 —
an unknown pi flag that killed every healer at birth (and exited 0 doing it),
and a Popen with no `env=` that billed the Claude Code subscription.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, BIN / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


heal = _load("agi_heal", "heal.py")
dispatch = _load("agi_dispatch_for_heal", "dispatch.py")


def make_project(repo: Path, **agent_dispatch) -> Path:
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage", "agent_dispatch": agent_dispatch}))
    return graph


# --- the flag that killed every healer -------------------------------------

def test_healer_passes_no_unknown_max_turns_flag():
    """pi has no `--max-turns`. It printed `Unknown option: --max-turns` and
    exited 0, so the loop recorded a healer as launched that had never read its
    own context."""
    source = (BIN / "heal.py").read_text()
    spawn = source.split("pi_args = [", 1)[1].split("]", 1)[0]
    assert "--max-turns" not in spawn


def test_healer_spawn_scrubs_the_environment():
    """dispatch.py's scrub exists so pi children cannot bill the interactive
    Claude Code subscription. The healer sat outside it."""
    source = (BIN / "heal.py").read_text()
    assert "env=_scrubbed_env()" in source
    assert "ANTHROPIC_API_KEY" not in heal._scrubbed_env()


def test_scrub_agrees_with_the_one_dispatch_uses():
    """Same rule, not a second copy of it — heal.py imports the function."""
    assert heal._scrubbed_env() == dispatch.scrubbed_env()


# --- model resolution ------------------------------------------------------

def test_healer_uses_the_projects_configured_model(tmp_path):
    graph = make_project(tmp_path, provider="openrouter",
                         model="z-ai/glm-5.3-flash", thinking="medium")
    args = heal._pi_model_args(graph)
    assert args == ["--provider", "openrouter",
                    "--model", "z-ai/glm-5.3-flash",
                    "--thinking", "medium"]


def test_healer_falls_back_to_pi_defaults_when_unconfigured(tmp_path):
    graph = make_project(tmp_path)
    assert heal._pi_model_args(graph) == []


@pytest.mark.parametrize("broken", ["not json at all", '{"agent_dispatch": 3}'])
def test_broken_config_costs_the_preference_not_the_healer(broken, tmp_path):
    """Healing runs when things are already broken. A malformed config must
    lose the healer its model preference, never its existence."""
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(broken)
    assert heal._pi_model_args(graph) == []


def test_missing_project_returns_no_args(tmp_path):
    assert heal._pi_model_args(tmp_path / "nowhere") == []
