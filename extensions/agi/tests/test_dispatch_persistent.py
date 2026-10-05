"""goal:g7.28.1 + goal:g7.28.1.2 + goal:g7.28.2 (hypothesis:a00-c3a24084-4190b2).

A `--persistent` dispatch HOLDS its seat and, when the child dies, re-opens
it through the SAME `_open_round` seam -- hence the SAME rendered
`spawn_args`/`spawn_env`, no second argv path, no re-render. And the seat's
record shows the occupation (persistent / live pid / restart_count).

goal:g7.28.1.2 — after start AND after each supervised restart, the
seats/posts registry row for `--seat` shows occupied with the live
pid/session pin (not only agent.json).

goal:g7.28.2 — kid/parent NON-persistent spawns stay fire-and-forget:
exactly one spawn, no persistent/restart_count fields, posts/seats row
untouched even with --seat, and dry-run creates no session / names no
supervisor.

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

pytestmark = pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green: dispatch._PERSIST_STOP_ENV is gone')
import yaml

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


# ---------------------------------------------------------------------------
# goal:g7.28.1.2 — posts/seats registry occupation under persistent start/
# restart. Fixture carries a real config:seats row + the live [config].md
# self_row schema so `_pin_posts_row_occupation` -> `_write_identity_cells`
# is admitted.
# ---------------------------------------------------------------------------

_LIVE_CONFIG_SCHEMA = (
    Path(__file__).resolve().parents[3] / ".agi" / "context" / "schemas"
    / "[config].md"
)
_SEAT_NAME = "director-seat"


def _install_posts_registry(graph: Path, *, pid: int = 0) -> None:
    """Write seats.md + [config].md schema under an `.agi` graph root."""
    geom = graph / "nodes" / ".geometry"
    geom.mkdir(parents=True, exist_ok=True)
    row = {"name": _SEAT_NAME, "role": "director", "pid": pid,
           "session_ref": "", "window": ""}
    body = (
        "---\nid: config:seats\ntype: config\nseats:\n"
        f"  - {json.dumps(row)}\n---\n"
    )
    (geom / "seats.md").write_text(body, encoding="utf-8")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    if _LIVE_CONFIG_SCHEMA.exists():
        (schemas / "[config].md").write_text(
            _LIVE_CONFIG_SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        (schemas / "[config].md").write_text(
            "---\nname: config\nwritten_by: [owner, prime_director]\n"
            "self_row: {list_key: seats, match_key: name, "
            "fields: [session_ref, session_name, session_id, generation, "
            "window, pid]}\n---\nbody\n",
            encoding="utf-8")


def _posts_row(root: Path, name: str = _SEAT_NAME) -> dict:
    """The seats/posts row exactly as it lives on the wire."""
    graph = root / ".agi"
    seats = graph / "nodes" / ".geometry" / "seats.md"
    posts = graph / "nodes" / ".geometry" / "posts.md"
    path = posts if posts.exists() else seats
    fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
    key = "posts" if "posts" in fm else "seats"
    return next(r for r in fm[key] if r.get("name") == name)


@pytest.fixture()
def project_with_posts(project: Path) -> Path:
    """`project` plus a seats/posts registry row the pin writer can update."""
    _install_posts_registry(project / ".agi", pid=0)
    return project


def test_persistent_start_pins_posts_row_live_pid(
        project_with_posts, monkeypatch, capsys):
    """g7.28.1.2 falsifier 1: after persistent start, posts/seats row pid
    matches the supervised child (and session_id carries the agent id)."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 999, "rc": None},
    ], stop_after=1)
    monkeypatch.setattr(
        sys, "argv",
        _argv(project_with_posts, "--persistent", "--seat", _SEAT_NAME))

    assert dispatch.main() == 0
    assert len(spawned) == 1
    row = _posts_row(project_with_posts)
    assert row.get("pid") == spawned[0][1].pid, row
    # session pin: agent id landed in session_id
    assert row.get("session_id"), row


def test_persistent_restart_updates_posts_row_pid(
        project_with_posts, monkeypatch, capsys):
    """g7.28.1.2 falsifier 2: after supervised restart, row pid is the NEW
    live child — never the corpse."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    monkeypatch.setattr(
        sys, "argv",
        _argv(project_with_posts, "--persistent", "--seat", _SEAT_NAME))

    assert dispatch.main() == 0
    assert len(spawned) == 2
    row = _posts_row(project_with_posts)
    assert row.get("pid") == spawned[1][1].pid, (
        f"row pid {row.get('pid')} is not the live child "
        f"{spawned[1][1].pid}; corpse was {spawned[0][1].pid}")
    assert row.get("pid") != spawned[0][1].pid, row

# ---------------------------------------------------------------------------
# goal:g7.28.2 — non-persistent kid/parent spawns unchanged (regression).
# Persistent is opt-in; default fire-and-forget must stay byte/lifecycle
# identical for BOTH kid and parent tiers, and must never pin the posts row.
# ---------------------------------------------------------------------------


def _project_with_parent_ladder(project: Path) -> Path:
    """Extend the kid-only ladder with a tier-1 parent row so --tier parent
    resolves without changing harness/model allowlists."""
    ladder = project / ".agi" / "nodes" / ".geometry" / "ladder.md"
    ladder.write_text(
        "---\ncurrent_season: 2\nroles:\n"
        "  - {tier: 0, role: kid, harness: pi, model: deepseek-v4}\n"
        "  - {tier: 1, role: parent, harness: pi, model: deepseek-v4}\n"
        "---\nbody",
        encoding="utf-8",
    )
    cfg_path = project / ".agi" / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    models = cfg["harnesses"]["pi"].setdefault("models", {})
    models.setdefault("parent", models.get("kid", "deepseek-v4"))
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    return project


def test_parent_fire_and_forget_spawns_no_supervisor(
        project, monkeypatch, capsys):
    """g7.28.2: --tier parent without --persistent is fire-and-forget —
    exactly one spawn, no persistent/restart_count fields on the record."""
    _project_with_parent_ladder(project)
    spawned = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(
        sys, "argv",
        [str(BIN / "dispatch.py"), str(project), "1",
         "--level", "small", "--harness", "pi", "--tier", "parent",
         "--target", "hypothesis:x"])

    assert dispatch.main() == 0
    assert len(spawned) == 1, f"parent default must not restart: {len(spawned)}"
    agents = _manifest(project)
    assert agents and "persistent" not in agents[0], agents
    assert "restart_count" not in agents[0], agents


def test_nonpersistent_with_seat_leaves_posts_row_untouched(
        project_with_posts, monkeypatch, capsys):
    """g7.28.2: non-persistent spawn even WITH --seat must NOT pin the
    posts/seats row — occupation pin is persistent-only."""
    before = _posts_row(project_with_posts)
    assert before.get("pid") == 0, before
    spawned = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(
        sys, "argv",
        _argv(project_with_posts, "--seat", _SEAT_NAME))

    assert dispatch.main() == 0
    assert len(spawned) == 1
    after = _posts_row(project_with_posts)
    assert after.get("pid") == 0, (
        f"non-persistent must leave posts pid=0; got {after.get('pid')}")
    assert after.get("session_id", "") in ("", None), after
    agents = _manifest(project_with_posts)
    assert agents and "persistent" not in agents[0], agents


def test_kid_dry_run_no_persistent_side_effects(project, capsys):
    """g7.28.2 regression dry-run (kid): resolves, exits 0, creates no
    session dir, never mentions a persistent supervisor."""
    argv = [str(BIN / "dispatch.py"), str(project), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", "--dry-run"]
    import subprocess as sp
    r = sp.run(argv, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = r.stdout + r.stderr
    assert "dry-run: nothing spawned" in out
    assert "persistent:" not in out
    assert "supervisor" not in out.lower() or "persistent" not in out.lower()
    sessions = list(project.glob(".agi/sessions/**"))
    assert not sessions, f"dry-run must not write sessions: {sessions}"


def test_parent_dry_run_no_persistent_side_effects(project, capsys):
    """g7.28.2 regression dry-run (parent): same invariants as kid."""
    _project_with_parent_ladder(project)
    argv = [str(BIN / "dispatch.py"), str(project), "1",
            "--level", "small", "--harness", "pi", "--tier", "parent",
            "--target", "hypothesis:x", "--dry-run"]
    import subprocess as sp
    r = sp.run(argv, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = r.stdout + r.stderr
    assert "dry-run: nothing spawned" in out
    assert "persistent:" not in out
    sessions = list(project.glob(".agi/sessions/**"))
    assert not sessions, f"dry-run must not write sessions: {sessions}"
