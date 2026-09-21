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
import time
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


# --- hypothesis:l3-branch-isolation-partial-break --------------------------
# A healer's cwd decides which tree its source edits touch. For a `--branch`
# spawn the record carries the agent's own worktree; the healer must re-enter
# it, not the main checkout.

def test_healer_cwd_reenters_the_branch_worktree(tmp_path):
    main_graph = tmp_path / "main" / ".agi"
    main_graph.mkdir(parents=True)
    wt = main_graph / "worktrees" / "a00-x"
    wt.mkdir(parents=True)
    rec = {"worktree": str(wt)}
    assert heal._heal_cwd(main_graph, rec).resolve() == wt.resolve()


def test_healer_cwd_falls_back_to_root_without_a_worktree(tmp_path):
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True)
    assert heal._heal_cwd(graph, {}) == graph


def test_healer_cwd_ignores_a_gone_worktree(tmp_path):
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True)
    rec = {"worktree": str(graph / "worktrees" / "a00-gone")}
    # Not on disk (dropped) → healers fall back to the resolved root rather
    # than spawning into a directory that does not exist.
    assert heal._heal_cwd(graph, rec) == graph

def test_healer_spawn_sets_cwd_from_worktree_record(tmp_path):
    """The Popen on the healer path must route cwd through `_heal_cwd`, not
    a re-entry of the caller's root."""
    source = (BIN / "heal.py").read_text()
    assert "cwd=str(heal_root)" in source, (
        "healer Popen must use the worktree-aware heal_root")
    assert "_heal_cwd(root, rec)" in source


# --- ladder is the ONE source (hypothesis:l4-a-model-change-is-one-write) ---

def _make_ladder_project(repo: Path, parent_model: str) -> Path:
    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            "allowed_extra": ["~z-ai/glm-flash-latest"]}},
        "agent_dispatch": {"model": "~z-ai/glm-flash-latest"}}))
    ladder = (graph / "nodes" / ".geometry" / "ladder.md")
    ladder.write_text(f"""---
current_season: 2
roles:
  - {{"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}}
  - {{"tier": 1, "role": "parent", "harness": "pi", "model": "{parent_model}", "effort": "", "settings": ""}}
---

fixture
""")
    return graph


def test_heal_resolves_the_ladder_row_model_for_the_healed_role(tmp_path):
    """A healed parent re-spawns with the LADDER row's model (the one source),
    not the config's allowed/legacy values — so the same one write on the
    ladder that changed the live spawn changes what a re-spawn uses."""
    graph = _make_ladder_project(tmp_path, "deepseek/deepseek-v4.1-flash")
    args = heal._pi_model_args(graph, "parent", "parent")
    assert "--model" in args
    assert args[args.index("--model") + 1] == "deepseek/deepseek-v4.1-flash"


def test_heal_without_a_ladder_still_uses_config(tmp_path):
    """No ladder file -> the historical config path still answers (missing
    ladder never blocks)."""
    graph = make_project(tmp_path, provider="openrouter",
                         model="z-ai/glm-5.3-flash")
    args = heal._pi_model_args(graph, "parent", "parent")
    assert "--model" in args
    assert args[args.index("--model") + 1] == "z-ai/glm-5.3-flash"


# --- hyp:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid- ----
# resolves-like-a-dead-running-record (claim b): the SECOND live admission
# point -- `_main_heal`'s per-agent block, the loop driver.sh runs as
# `heal.py <root> <iter_n>`. Even with the dispatch fix live, a `stalled`
# record found by THIS loop used to die at the `status != "running"` guard
# (L183 pre-fix) and never resolve. These tests drive the REAL `_main_heal`
# path, not a copy of its block.


def _stalled_round(tmp_path: Path, pid: int) -> tuple[Path, Path]:
    """A tmp graph with one round carrying a single `stalled` agent whose
    pid is `pid`. Returns `(root, agent_json_path)`."""
    root = tmp_path
    graph = root / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    iter_dir = graph / "sessions" / "iter-001"
    (iter_dir / "a00-s").mkdir(parents=True, exist_ok=True)
    (iter_dir / "manifest.json").write_text(json.dumps({
        "iter": 1,
        "timeout_seconds": 600,
        "agents": [{"id": "a00-s", "status": "running"}],
    }, indent=2))
    aj = iter_dir / "a00-s" / "agent.json"
    aj.write_text(json.dumps({
        "id": "a00-s",
        "status": "stalled",
        "pid": pid,
        "started_at": int(time.time()) - 100,
        "node_id": "hypothesis:h1",
    }, indent=2))
    return root, aj, iter_dir / "manifest.json"


# the real dispatch module heal's `_reap_one` closes over, so patching on it
# is the ONLY patch that reaches the resolution rule heal actually calls.
import dispatch as real_dispatch  # noqa: E402 -- cached module heal imported


def test_heal_resolves_stalled_dead_pid_to_failed(monkeypatch, tmp_path):
    """A `stalled` record with a PROVABLY dead pid reaches the dead-pid path
    in `_main_heal` and resolves through dispatch._reap_one to `failed` with
    the stall named (no completion, no branch advance -> never restarted),
    and the manifest mirrors it."""
    root, aj, mp = _stalled_round(tmp_path, 999999)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    assert heal.main() == 0  # resolved THIS pass -> all terminal
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "failed"
    assert "stalled" in rec["fail_reason"]
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    assert manifest["agents"][0]["status"] == "failed"


def test_heal_resolves_stalled_dead_to_done_unreported_on_branch_advance(
        monkeypatch, tmp_path):
    """Same admission, but the work landed: when the round branch advanced,
    dispatch._reap_one still resolves the stalled-dead record to
    `done-unreported` (never restarted)."""
    root, aj, mp = _stalled_round(tmp_path, 999999)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(real_dispatch, "_branch_has_done_commit",
                        lambda root, rec, agent_id: True)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    assert heal.main() == 0
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "done-unreported"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    assert manifest["agents"][0]["status"] == "done-unreported"


def test_heal_leaves_a_live_pid_stalled_record_untouched(monkeypatch, tmp_path):
    """A `stalled` record whose pid is LIVE is NOT terminal: one pass leaves
    it untouched (status stalled, no fail_reason, no finished_at), all_terminal
    is False, and `_main_heal` returns the NAMED non-zero `NOT_TERMINAL_YET`
    code instead of sleeping toward the 30-min deadline. Clock and sleep are
    seam-injected, so the pass is bounded and no real sleep happens."""
    root, aj, mp = _stalled_round(tmp_path, 987654)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: True)
    slept: list = []
    monkeypatch.setattr(heal, "_sleep", lambda s: slept.append(s))
    monkeypatch.setattr(heal, "_now", lambda: 0.0)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    t0 = time.monotonic()
    rc = heal.main()
    assert time.monotonic() - t0 < 1.0
    assert rc == heal.NOT_TERMINAL_YET
    assert rc != 0
    assert slept == []  # returned after one pass; never polled
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "stalled"
    assert "fail_reason" not in rec
    assert "finished_at" not in rec
    assert json.loads(mp.read_text(encoding="utf-8"))["agents"][0]["status"] \
        == "stalled"
