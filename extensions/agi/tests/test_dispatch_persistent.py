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
    (graph / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nposts:\n"
        "  - {name: probe-seat, role: kid, pid: 77, session_ref: old}\n---\n")
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

    def __init__(self, pid, rc, left, *, stubborn=False):
        self.pid = pid
        self._rc = rc
        self._left = left
        self._stubborn = stubborn
        self.returncode = None
        self.calls = []

    def terminate(self):
        self.calls.append("terminate")
        if not self._stubborn:
            self.returncode = -15

    def kill(self):
        self.calls.append("kill")
        self.returncode = -9

    def wait(self, timeout=None):
        self.calls.append("wait")
        if self.poll() is None:
            raise subprocess.TimeoutExpired("fake child", timeout)
        return self.returncode

    def poll(self):
        if self.returncode is not None:
            return self.returncode
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
                         plan.get("left", 0),
                         stubborn=plan.get("stubborn", False))
        spawned.append((argv, proc))
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


def test_terminal_exhaustion_clears_authoritative_record(
        project, monkeypatch, capsys):
    """Exhausted replacement death leaves no corpse pid or live claim."""
    spawned = _fake_spawn(monkeypatch, [{"left": 0, "rc": 1}])
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    assert len(spawned) == 4
    rec = _manifest(project)[0]
    assert rec["persistent"] is False
    assert rec["pid"] is None
    assert rec["persistent_terminal_reason"] == "restart-exhausted"
    session_rec = json.loads(next(project.glob(
        ".agi/sessions/iter-001/*/agent.json")).read_text())
    assert (session_rec["persistent"], session_rec["pid"]) == (False, None)


def test_live_persistent_child_claims_then_clean_stop_releases_post(
        project, monkeypatch, capsys):
    """The real call path publishes the live pid/session pin, then releases."""
    _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    seen = []

    def observe(_seconds):
        row = dispatch.geometry_config.load_rows(project / ".agi")[0]
        seen.append(dict(row))
        os.environ[dispatch._PERSIST_STOP_ENV] = "1"

    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", observe)
    monkeypatch.setattr(
        sys, "argv", _argv(project, "--persistent", "--seat", "probe-seat"))

    assert dispatch.main() == 0
    assert seen[0]["pid"] == 1000
    assert seen[0]["session_ref"].startswith("a00-")
    row = dispatch.geometry_config.load_rows(project / ".agi")[0]
    assert (row["pid"], row["session_ref"]) == (0, "")


def test_inherited_seat_is_claimed_and_forced_stop_precedes_release(
        project, monkeypatch, capsys):
    """Inherited AGI_SEAT follows the live path; a stubborn child is killed and
    reaped before the post can become vacant."""
    os.environ["AGI_SEAT"] = "probe-seat"
    spawned = _fake_spawn(monkeypatch, [
        {"left": 999, "rc": None, "stubborn": True},
    ])
    seen = []
    released_alive = []

    def observe(_seconds):
        seen.append(dict(dispatch.geometry_config.load_rows(project / ".agi")[0]))
        os.environ[dispatch._PERSIST_STOP_ENV] = "1"

    real_post = dispatch._persistent_post

    def observe_post(root, seat, proc, agent_id, record, occupied):
        if not occupied:
            released_alive.append(proc.poll())
        return real_post(root, seat, proc, agent_id, record, occupied)

    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", observe)
    monkeypatch.setattr(dispatch, "_persistent_post", observe_post)
    monkeypatch.setattr(
        sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    assert seen[0]["pid"] == 1000
    assert seen[0]["session_ref"].startswith("a00-")
    assert spawned[0][1].calls == ["terminate", "wait", "kill", "wait"]
    assert released_alive == [-9]
    row = dispatch.geometry_config.load_rows(project / ".agi")[0]
    assert (row["pid"], row["session_ref"]) == (0, "")


def test_non_persistent_dispatch_never_writes_or_claims_post(
        project, monkeypatch, capsys):
    """Opt-in remains opt-in, including the graph/config authority."""
    before = (project / ".agi/nodes/.geometry/posts.md").read_bytes()
    _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(
        sys, "argv", _argv(project, "--seat", "probe-seat"))

    assert dispatch.main() == 0
    assert (project / ".agi/nodes/.geometry/posts.md").read_bytes() == before
    row = dispatch.geometry_config.load_rows(project / ".agi")[0]
    assert (row["pid"], row["session_ref"]) == (77, "old")
