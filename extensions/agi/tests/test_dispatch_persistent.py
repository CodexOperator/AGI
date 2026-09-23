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


# --- goal:g7.28.1 (DH.168) -- the two holes the parent review named ---------
# (a) exhaustion must never leave `persistent:true` over a corpse;
# (b) a named `--seat` must show its occupation in its OWN posts row and
#     clear it when no live child remains. The row write reuses rotate's ONE
#     identity writer -- never a second writer.

LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
               "context" / "schemas" / "[config].md")


@pytest.fixture()
def project_with_seat(project: Path) -> Path:
    """The dispatch project plus a `posts.md` row for seat-a (stale pid)."""
    import shutil
    sd = project / ".agi" / "context" / "schemas"
    sd.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LIVE_SCHEMA, sd / "[config].md")
    geo = project / ".agi" / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    rows = [
        {"name": "seat-a", "role": "director", "harness": "pi",
         "model": "deepseek-v4", "pid": 999999},
        {"name": "other", "role": "kid", "pid": 123},
    ]
    body = "\n".join("  - " + json.dumps(r) for r in rows)
    (geo / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
        "\n---\n\n# config:posts\n\nfixture\n", encoding="utf-8")
    return project


def _row(project: Path, name: str) -> dict:
    import geometry_config
    rows = geometry_config.load_rows(project / ".agi")
    return next(r for r in rows if r.get("name") == name)


def test_exhaustion_never_leaves_persistent_over_a_corpse(
        project, monkeypatch, capsys):
    """Hole (a): reopen always yields an instantly-dead child; the FINAL
    record must not assert `persistent` over a pid that names nothing live."""
    spawned = _fake_spawn(monkeypatch, [{"left": 0, "rc": 1}])
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    # initial spawn + one restart per max_restarts, then the bound breaks.
    assert len(spawned) == dispatch._PERSIST_MAX_RESTARTS + 1, len(spawned)
    assert spawned[-1][1].poll() is not None, "last child must be a corpse"
    agents = _manifest(project)
    rec = agents[0]
    assert "persistent" not in rec, f"corpse still asserted: {rec}"
    assert rec["pid"] == 0, rec
    assert rec["restart_count"] == dispatch._PERSIST_MAX_RESTARTS, rec
    # the session record the supervisor kept current says the same.
    sess = sorted(project.glob(".agi/sessions/**/agent.json"))[0]
    on_disk = json.loads(sess.read_text())
    assert "persistent" not in on_disk and on_disk["pid"] == 0, on_disk


def test_named_seat_row_shows_occupation_then_clears(
        project_with_seat, monkeypatch, capsys):
    """Hole (b): with `--seat`, the seat's OWN posts row carries the child
    pid at start/each restart and is cleared (pid 0) when the last child is
    dead. A foreign row is never touched (write.py self_row)."""
    spawned = _fake_spawn(monkeypatch, [{"left": 0, "rc": 1}])
    written: list[int] = []
    real = dispatch._persistent_row

    def _rec(root, seat, *, pid, session_id=None):
        written.append(pid)
        return real(root, seat, pid=pid, session_id=session_id)

    monkeypatch.setattr(dispatch, "_persistent_row", _rec)
    monkeypatch.setattr(sys, "argv",
                        _argv(project_with_seat, "--persistent",
                              "--seat", "seat-a"))

    assert dispatch.main() == 0
    # the live child pids were written, then the clear sentinel.
    assert 1000 in written, written
    assert written[-1] == 0, written
    assert _row(project_with_seat, "seat-a")["pid"] == 0, _row(
        project_with_seat, "seat-a")
    assert _row(project_with_seat, "other")["pid"] == 123
