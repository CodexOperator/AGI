"""Tests for hypothesis:a00-d89b6c11-b6e73f -- a healer is a LAUNCHED AGENT,
so it rides the SAME memory cap as the kid it repairs.

`heal._heal`'s `subprocess.Popen` ran the raw `pi` argv: it was the one live
agent spawn in the engine outside `mem_cap.wrap_argv` (dispatch's kid at
dispatch.py:2851 and workflow's stage at workflow.py:1803 were already
wrapped). A healer is spawned precisely when a round has already gone wrong --
the moment a runaway is most likely -- so the uncapped spawn was the worst
possible place to leave the gap.

These tests pin the WRAP, not a live cgroup kill: the box's fork bound forbids
a real fan-out here (see the hypothesis), so the claim is proven on the argv
the seam hands to Popen, which is the same list the live spawn runs.
"""
from __future__ import annotations

import importlib.util
import json
import shlex
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    """A project graph root with a config that names the cap explicitly."""
    g = tmp_path / "repo" / ".agi"
    (g / "nodes").mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage", "spawn": {"memory_max": "1G"}}))
    return g


class _FakeProc:
    pid = 4242


def _heal_once(graph: Path, monkeypatch) -> list:
    """Run `_heal` for one hung agent; return the argv Popen was handed."""
    it = graph / "sessions" / "iter-L1.07"
    (it / "agent-h").mkdir(parents=True, exist_ok=True)
    log = it / "agent-h" / "output.log"
    log.write_text("stuck\n")
    rec = {"id": "agent-h", "status": "running", "pid": 0,
           "log_file": str(log), "iter_n": "C"}
    (it / "agent-h" / "agent.json").write_text(json.dumps(rec))
    seen: list = []

    def _fake_popen(argv, **kwargs):
        seen.append(list(argv))
        return _FakeProc()

    monkeypatch.setattr(heal.subprocess, "Popen", _fake_popen)
    monkeypatch.setattr(heal.time, "sleep", lambda *_a, **_k: None)
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "1")
    heal._heal(graph, "L1.07", "agent-h", rec)
    assert len(seen) == 1, seen
    return seen[0]


def test_healer_argv_carries_the_configured_cap(graph, monkeypatch):
    """The ONE conjunct: a healer spawn is wrapped by `mem_cap.wrap_argv` with
    the cap the config names -- the same wrapper dispatch and workflow use."""
    argv = _heal_once(graph, monkeypatch)
    assert argv[0] == "systemd-run", argv
    assert "--property=MemoryMax=1G" in argv, argv
    assert argv[-1].startswith("You are healer heal-"), argv


def test_healer_record_names_the_command_actually_launched(graph, monkeypatch):
    """`agent.json`'s healer.command is the LAUNCHED argv, so an operator
    reading the record sees the cap that bound -- not the bare pi line."""
    argv = _heal_once(graph, monkeypatch)
    rec = json.loads((graph / "sessions" / "iter-L1.07" / "agent-h"
                      / "agent.json").read_text())
    assert rec["healer"]["command"] == " ".join(shlex.quote(a) for a in argv)
    assert "MemoryMax=1G" in rec["healer"]["command"]


def test_a_capped_off_cell_leaves_the_healer_unwrapped(tmp_path, monkeypatch):
    """`spawn.memory_max: null` means the operator asked for NO cap. The
    healer then spawns the raw pi argv -- the escape hatch stays an escape
    hatch, and the wrap is not a hard-coded bound."""
    g = tmp_path / "repo" / ".agi"
    (g / "nodes").mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps(
        {"spawn": {"memory_max": None}}))
    argv = _heal_once(g, monkeypatch)
    assert "systemd-run" not in argv, argv
    assert "-p" in argv and "--append-system-prompt" in argv, argv
    assert not any(a.startswith("--property=MemoryMax") for a in argv), argv


def test_an_absent_cell_still_caps_the_healer(tmp_path, monkeypatch):
    """No `spawn` cell at all -> `resolve_memory_cap`'s shipped '4G'. A
    missing config must not be the one case where a healer runs uncapped."""
    g = tmp_path / "repo" / ".agi"
    (g / "nodes").mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    argv = _heal_once(g, monkeypatch)
    assert "--property=MemoryMax=4G" in argv, argv
