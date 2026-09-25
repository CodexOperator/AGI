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
import re
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


# role -> (ladder tier, model). Both seats are the ones goal:g7.28.2 names.
_ROLES = {"kid": (0, "deepseek-v4"), "parent": (1, "fake-parent")}


def _write_project(root: Path, role: str = "kid") -> Path:
    """A minimal one-node project whose ladder knows `role`."""
    tier_n, model = _ROLES[role]
    graph = root / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {role: model}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: %d, role: %s, "
        "harness: pi, model: %s}\n---\nbody" % (tier_n, role, model))
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
    return root


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    return _write_project(tmp_path, "kid")


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
        spawned.append((argv, proc))
        if stop_after is not None and len(spawned) >= stop_after:
            os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    return spawned


def _argv(tmp_path: Path, *extra, role: str = "kid"):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", role,
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


# ---------------------------------------------------------------------------
# goal:g7.28.2 -- falsifier 1: the `--persistent` branch must not move the
# DEFAULT spawn for EITHER seat. The comparison is the rendered argv and the
# exported environment of the one child each run opens, so a flag that only
# changes lifecycle (and not the wire) is invisible here by construction.
# ---------------------------------------------------------------------------

class _IdleProc:
    """A child that never exits: `poll()` is None forever, so a persistent
    seat has nothing to restart even if the supervisor is left alone."""

    def __init__(self, pid):
        self.pid = pid
        self.returncode = None

    def poll(self):
        return None


def _capture(root: Path, role: str, extra, monkeypatch):
    """One dispatch, Popen faked ONLY on the start_new_session spawn path so
    the internal zoom subprocess.run calls still go to the real thing.
    Returns (spawns, supervisor_calls, manifest_agents)."""
    spawns: list = []
    supervised: list = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        spawns.append((list(argv), dict(kwargs.get("env") or {})))
        return _IdleProc(4000 + len(spawns))

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_supervise_persistent",
                        lambda *a, **k: supervised.append(1))
    monkeypatch.setattr(sys, "argv", _argv(root, *extra, role=role))
    assert dispatch.main() == 0
    return spawns, supervised, _manifest(root)


# a minted agent id, and the scaffolded node id that carries its hash as a
# suffix (`a00-8079f434-9398bd`) -- both are per-run coin flips.
_ID_RE = re.compile(r"a00-[0-9a-f]{6,10}(?:-[0-9a-f]{4,10})?")


def _norm(value, root: Path) -> str:
    """Normalize ONLY the per-run identity: this run's project root and its
    minted ids. Everything else must match byte-wise."""
    return _ID_RE.sub("<ID>", value.replace(str(root), "<ROOT>"))


@pytest.mark.parametrize("role", ["kid", "parent"])
def test_default_spawn_is_identical_with_and_without_persistent(
        tmp_path: Path, monkeypatch, role):
    got = {}
    for label, extra in (("default", []),
                         ("persistent", ["--persistent", "--detach"])):
        root = _write_project(tmp_path / label, role)
        spawns, supervised, agents = _capture(root, role, extra, monkeypatch)
        assert len(spawns) == 1, f"{role}/{label}: {len(spawns)} spawns, want 1"
        argv, env = spawns[0]
        got[label] = (
            [_norm(a, root) for a in argv],
            {k: _norm(v, root) for k, v in env.items()},
            supervised,
            agents[0],
        )

    d_argv, d_env, d_sup, d_rec = got["default"]
    p_argv, p_env, p_sup, p_rec = got["persistent"]
    assert d_argv == p_argv, f"{role}: --persistent changed the rendered argv"
    assert d_env == p_env, f"{role}: --persistent changed the child env"
    # Without the flag the supervisor is never even entered, and the seat
    # record carries neither occupation key.
    assert d_sup == [], f"{role}: supervisor ran on the default path: {d_sup}"
    assert "persistent" not in d_rec, d_rec
    assert "restart_count" not in d_rec, d_rec
    # The two runs really are the same seat on the same loop, so the
    # comparison above was between like and like.
    assert d_rec["tier"] == role == p_rec["tier"], (d_rec, p_rec)
    assert p_sup, f"{role}: --persistent never opened the supervisor"
