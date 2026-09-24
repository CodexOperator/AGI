"""goal:g7.28.1 (hypothesis:a00-c3a24084-4190b2) -- falsifiers 1 and 3.

A `--persistent` dispatch HOLDS its seat and, when the child dies, re-opens
it through the SAME `_open_round` seam -- hence the SAME rendered
`spawn_args`/`spawn_env`, no second argv path, no re-render. And the seat's
record shows the occupation (persistent / live pid / restart_count).

No live model, no network, no real sleep: `subprocess.Popen` is faked for the
spawn path and `dispatch._PERSIST_SLEEP` is a no-op.
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


def _load_dispatch():
    spec = importlib.util.spec_from_file_location(
        "agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


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
              "AGI_ACTOR", dispatch._PERSIST_STOP_ENV):
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


def _fake_spawn(monkeypatch, plans, stop_after=None):
    """Patch the spawn Popen; `stop_after=N` sets the clean-stop env once N
    children have been opened, so a live persistent seat still ends."""
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
        proc = _StubProc(1000 + len(spawned), plan.get("rc"),
                         plan.get("left", 0))
        spawned.append((argv, proc, dict(kwargs.get("env") or {})))
        if stop_after is not None and len(spawned) >= stop_after:
            os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    return spawned


def _argv(tmp_path: Path, *extra):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", *extra]


def _count_build_command(monkeypatch) -> list:
    """Count adapter.build_command calls: a restart that rebuilt argv would
    call it a second time."""
    calls: list = []
    real_load = dispatch.adapters.load
    wrapped: set = set()

    def _load(name):
        mod = real_load(name)
        if id(mod) not in wrapped:
            wrapped.add(id(mod))
            orig = mod.build_command

            def _bc(*a, **k):
                calls.append(1)
                return orig(*a, **k)

            mod.build_command = _bc
        return mod

    monkeypatch.setattr(dispatch.adapters, "load", _load)
    return calls


def _manifest(root: Path) -> list[dict]:
    path = sorted(root.glob(".agi/sessions/**/manifest.json"))[0]
    return json.loads(path.read_text())["agents"]


def test_persistent_restart_reuses_the_very_same_argv(
        project, monkeypatch, capsys):
    """Falsifiers 1+3: the child dies, the supervisor restarts it, and the
    re-opened argv is the IDENTICAL list object the first spawn used -- the
    seam never rebuilt it (`mem_cap.wrap_argv` returns the same list when no
    cap is set, so `is` is the honest proof)."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    builds = _count_build_command(monkeypatch)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    assert len(spawned) == 2, f"expected one restart, got {len(spawned)}"
    # Same rendered argv: byte-identical, and the builder that renders it ran
    # exactly ONCE -- a restart through a second argv path would rebuild it.
    assert spawned[0][0] == spawned[1][0]
    assert len(builds) == 1, f"argv was rebuilt: build_command x{len(builds)}"


@pytest.mark.parametrize("credential", ["none", "openrouter"])
def test_persistent_restart_reuses_the_sanitized_child_env(
        project, monkeypatch, capsys, credential):
    """The held restart reaches the real Popen seam with the same env map.

    This is deliberately boundary-level: spying only child_env would miss a
    second argv/env path.  Credential-off strips the inherited key; the
    credential-on row preserves it, and explicit harness vars survive both.
    """
    config = json.loads((project / ".agi/config.json").read_text())
    config["harnesses"]["pi"] = dict(config["harnesses"]["pi"])
    config["harnesses"]["pi"].update({"credential": credential,
                                        "env": {"HARNESS_ONLY": "yes"}})
    (project / ".agi/config.json").write_text(json.dumps(config))
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-inherited")
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    assert len(spawned) == 2
    first_env, restart_env = spawned[0][2], spawned[1][2]
    if credential == "none":
        assert "OPENROUTER_API_KEY" not in first_env
        assert "OPENROUTER_API_KEY" not in restart_env
    else:
        assert first_env["OPENROUTER_API_KEY"] == "sk-or-v1-inherited"
        assert restart_env == first_env
    assert restart_env == first_env
    assert restart_env["HARNESS_ONLY"] == "yes"


def test_fire_and_forget_default_spawns_no_supervisor(
        project, monkeypatch, capsys):
    """`--persistent` absent: exactly one spawn, no restart bookkeeping, and
    no supervisor in the path (the default must be unchanged)."""
    spawned = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, f"default path must not restart: {len(spawned)}"
    agents = _manifest(project)
    assert agents and "persistent" not in agents[0], agents
    assert "restart_count" not in agents[0], agents


def test_record_carries_persistent_live_pid_and_restart_count(
        project, monkeypatch, capsys):
    """Conjunct (c): the seat's own record shows the occupation -- persistent
    true, the CURRENT (restarted) pid, and the restart count."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    agents = _manifest(project)
    assert len(agents) == 1, agents
    rec = agents[0]
    assert rec["persistent"] is True, rec
    assert rec["restart_count"] == 1, rec
    assert rec["pid"] == spawned[1][1].pid, (
        f"record pid {rec['pid']} is not the live child "
        f"{spawned[1][1].pid}")
