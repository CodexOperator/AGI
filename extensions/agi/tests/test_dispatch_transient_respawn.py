"""Tests for hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-
backoff-logged-by-name-never-a-real-failure, conjunct (2): the DISPATCHER.

A kid that dies at its FIRST call, leaving ONLY pi's local catalogue warning
and a 5xx signature line in `output.log`, is a dead round nobody re-runs
(measured: iter-TM.07/a00-1fec07a8/output.log = two lines, no commit, no
node). The claim under test: dispatch polls a bounded startup grace after
Popen and re-spawns exactly that class of death under the SAME lease, agent
id, worktree and log, bounded at 3 attempts, naming each attempt in the log.

No live spawn, no network, no real sleep: `subprocess.Popen` is faked and the
grace/backoff seam `dispatch._GRACE_SLEEP` is a no-op.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

CATALOGUE = (b'Model "deepseek-v4" not found for provider "openrouter". '
             b'Using custom model id.\n')
DEAD_520 = b"error code: 520\n"


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()
_FX = _load_dispatch.__module__


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"kid": "deepseek-v4"}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: deepseek-v4}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        os.environ.pop(k, None)
    return tmp_path


class _StubProc:
    """A fake child: `poll()` returns None `left` times, then `rc` forever."""

    def __init__(self, pid, rc, left):
        self.pid = pid
        self._rc = rc
        self._left = left
        self.returncode = None

    def poll(self):
        if self._left <= 0:
            if self._rc is not None:
                self.returncode = self._rc
            return self.returncode
        self._left -= 1
        return None


def _fake_spawn(monkeypatch, plans):
    """Patch ONLY the spawn Popen (the one with `start_new_session=True`).

    `plans` is one dict per expected spawn, in order:
      bytes -> written to that spawn's log handle before the child is judged
      rc    -> the exit code the child eventually reports (None = never)
      left  -> number of `poll()` calls that see it alive first
    Returns the list of (argv, proc) actually spawned."""
    spawned = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        plan = plans[len(spawned)] if len(spawned) < len(plans) else plans[-1]
        f = kwargs.get("stdout")
        if f is not None and plan.get("bytes"):
            f.write(plan["bytes"])
            f.flush()
        proc = _StubProc(1000 + len(spawned), plan.get("rc"), plan.get("left", 0))
        spawned.append((argv, proc))
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    return spawned


def _argv(tmp_path: Path, *extra):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", *extra]


def _logs(root: Path):
    return sorted(root.glob(".agi/sessions/**/output.log"))


def test_transient_startup_death_is_respawned_and_named(
        project, monkeypatch, capsys):
    """(a) A child that dies rc 1 inside the grace leaving ONLY the catalogue
    warning + `error code: 520` is re-spawned under the SAME lease, agent id,
    worktree and log, with an `attempt 2` line appended; the second child is
    the one that ends up registered."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 1, "left": 0},
        {"bytes": b"", "rc": None, "left": 99},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 0, f"a rescued round must register and exit 0, got {code}"
    assert len(spawned) == 2, f"expected ONE re-spawn, got {len(spawned)}"
    # the SAME argv: same agent id, same worktree, same env, same lease
    assert spawned[0][0] == spawned[1][0], "re-spawn changed the command"

    logs = _logs(project)
    assert len(logs) == 1, f"re-spawn must reuse the SAME log: {logs}"
    text = logs[0].read_text()
    assert "attempt 2" in text, f"no by-name re-spawn line in the log:\n{text}"
    assert "error code: 520" in text or "520" in text, text

    agents = json.loads(
        (sorted(project.glob(".agi/sessions/**/manifest.json"))[0]).read_text()
    )["agents"]
    assert len(agents) == 1, f"exactly one round registered, got {agents}"
    assert agents[0]["pid"] == spawned[1][1].pid, \
        "the registered pid must be the RE-SPAWNED child"


def test_clean_exit_zero_inside_the_grace_is_never_respawned(
        project, monkeypatch, capsys):
    """(b) A child that exits 0 inside the grace takes today's path: exactly
    one Popen, no `attempt` line."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 0, "left": 1},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "rc 0 must never be re-spawned"
    assert "attempt 2" not in _logs(project)[0].read_text()


def test_a_child_alive_past_the_grace_is_never_touched(
        project, monkeypatch, capsys):
    """(c) A healthy child outliving the grace: exactly one Popen, no
    `attempt` line, dispatch returns as today."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": None, "left": 999},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "a live child must never be re-spawned"
    assert "attempt 2" not in _logs(project)[0].read_text()


def test_a_non_transient_startup_death_is_not_respawned(
        project, monkeypatch, capsys):
    """The falsifier guard on the bytes: a child that died with anything else
    in its log (here a real thought) is never re-spawned."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520 + b"# kid: writing node\n", "rc": 1,
         "left": 0},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "a death after real output must not be retried"


def test_the_classifier_reads_only_whole_signature_logs(tmp_path):
    """The decision itself: ONLY non-empty signature lines => transient."""
    cat = tmp_path / "a.log"
    cat.write_bytes(CATALOGUE + DEAD_520)
    assert dispatch._startup_death_is_transient(cat)
    mixed = tmp_path / "b.log"
    mixed.write_bytes(CATALOGUE + b'{"stage": "x"}\n')
    assert dispatch._startup_death_is_transient(mixed) is None
    empty = tmp_path / "c.log"
    empty.write_bytes(b"\n\n")
    assert dispatch._startup_death_is_transient(empty) is None
    missing = tmp_path / "d.log"
    assert dispatch._startup_death_is_transient(missing) is None
