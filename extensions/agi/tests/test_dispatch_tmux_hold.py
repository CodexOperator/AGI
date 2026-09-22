"""Dispatch seam tests for the durable named tmux pane hold (`goal:g7.31.1.2`).

Two demoted defects, proven on the built bytes with NO real tmux server:

* `HeldProc.poll` used to report rc 0 for a dead pane, so dispatch's
  `_await_startup(proc) or proc.returncode == 0` read a dead held seat as a
  clean startup and registered it `status: running`. Here the FIRST-spawn seam
  (`dispatch._open_round`'s hold branch) is driven end to end through
  `dispatch.main` with the adapter's real `hold_harness` resolution, and a
  dead seat is asserted NOT to become a healthy running record.
* the hold branch itself was only wire-read (grep); the same tests exercise it
  through the one seam dispatch uses -- `tmux_hold.spawn(hold, agent_id, ...,
  env=spawn_env)` -- with tmux faked.

`subprocess.run` is faked for tmux calls and passed through for everything
else, exactly as the conftest `_no_real_tmux` guard does.
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

from adapters import tmux_hold  # noqa: E402


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()

CATALOGUE = (b'Model "grok-4" not found for provider "openrouter". '
             b'Using custom model id.\n')
DEAD_520 = b"error code: 520\n"

AGENT = "a00-test-seat"
LOG_REDIRECT = re.compile(r"exec >>(.+?) 2>&1")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A config whose harness declares NO tmux cell: the hold must come from
    the adapter's own `HOLD_PANE`/`hold_harness`."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "box": {"tmux_session": "S"},
        "harnesses": {"grok-bot": {"adapter": "grok_bot",
                                   "models": {"kid": "grok-4"},
                                   "env": {"DT_SEAM_PROBE": "held"}}},
        "spawn": {"harness": "grok-bot", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n"
        "  - {tier: 0, role: kid, harness: grok-bot, model: grok-4}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR", "AGI_SEAT"):
        os.environ.pop(k, None)
    return tmp_path


class SeatTmux:
    """Fake tmux that also models pane-process life and the seat's log.

    `dying_respawns` respawns Seats die (their pid is never marked alive);
    every further respawn stays alive. `log_bytes` is appended to the seat's
    `output.log` on each respawn, emulating the shell redirect `_cmd` builds.
    """

    def __init__(self, dying_respawns: int = 0, log_bytes: bytes = b""):
        self.sessions: dict[str, dict] = {}
        self.calls: list[list[str]] = []
        self.alive_pids: set[int] = set()
        self.dying_respawns = dying_respawns
        self.log_bytes = log_bytes
        self._next = 10

    def _pane(self, name):
        self._next += 1
        return {"name": name, "pane": f"%{self._next}", "pid": 1000,
                "window": f"@{self._next}"}

    def _find(self, target):
        for sess in self.sessions.values():
            for w in sess["windows"]:
                if target in (w["pane"], w["window"]):
                    return w
        return None

    def _seat_log(self, cmd):
        if not self.log_bytes or "--" not in cmd:
            return
        payload = cmd[cmd.index("--") + 3]
        m = LOG_REDIRECT.search(payload)
        if not m:
            return
        path = Path(m.group(1).strip("'\""))
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "ab") as fh:
            fh.write(self.log_bytes)

    def run(self, cmd, *a, **k):
        self.calls.append(list(cmd))
        s = self.sessions
        rc, out = 0, ""
        if cmd[1] == "list-panes":
            name = cmd[cmd.index("-t") + 1]
            if name not in s:
                rc = 1
            else:
                out = "".join(f"{w['name']} {w['pane']} {w['pid']}\n"
                              for w in s[name]["windows"])
        elif cmd[1] == "new-session":
            s.setdefault(cmd[cmd.index("-s") + 1], {
                "windows": [self._pane(cmd[cmd.index("-n") + 1])],
                "current": 0})
        elif cmd[1] == "respawn-pane":
            w = self._find(cmd[cmd.index("-t") + 1].split(":")[-1])
            if w is None:
                rc = 1
            else:
                w["pid"] += 1
                if self.dying_respawns > 0:
                    self.dying_respawns -= 1
                else:
                    self.alive_pids.add(w["pid"])
                self._seat_log(cmd)
        return subprocess.CompletedProcess(cmd, rc, out, "")

    def respawns(self):
        return [c for c in self.calls if c[1] == "respawn-pane"]

    def seat_windows(self):
        return [w for w in self.sessions["S"]["windows"]]


@pytest.fixture()
def fake_tmux(monkeypatch):
    real_run = subprocess.run
    f = SeatTmux()

    def _run(cmd, *a, **k):
        if isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "tmux":
            return f.run(cmd, *a, **k)
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _run)
    monkeypatch.setattr(tmux_hold, "_alive", lambda pid: pid in f.alive_pids)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    return f


def _argv(project: Path):
    return [str(BIN / "dispatch.py"), str(project), "1",
            "--level", "small", "--tier", "kid",
            "--target", "hypothesis:x"]


def _agents(root: Path):
    manifests = sorted(root.glob(".agi/sessions/**/manifest.json"))
    if not manifests:
        return []
    return json.loads(manifests[0].read_text())["agents"]


def test_first_spawn_through_dispatch_founds_the_pane_and_threads_env(
        project, fake_tmux, monkeypatch):
    """The `_open_round` hold branch founds the named pane on the FIRST spawn
    and reaches `tmux_hold.spawn(..., env=spawn_env)` -- resolved from the
    adapter's own `hold_harness`, since the config carries no tmux cell."""
    fake_tmux.dying_respawns = 0  # the seat lives
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert "S" in fake_tmux.sessions, "no session was founded"
    assert [w["name"] for w in fake_tmux.seat_windows()] == [
        tmux_hold.pane_name(_agents(project)[0]["id"])], \
        "the seat's named window was not founded on the first spawn"

    respawns = fake_tmux.respawns()
    assert len(respawns) == 1, f"expected exactly one first spawn, got {respawns}"
    # the child env rides the respawn command (`respawn-pane` inherits the
    # SERVER's env, never the dispatch child's).
    assert any("DT_SEAM_PROBE=held" in a for a in respawns[0]), respawns[0]


def test_dead_held_seat_is_never_registered_running(
        project, fake_tmux, monkeypatch, capsys):
    """A dead held pane process is not a healthy running seat. `HeldProc.poll`
    returns a nonzero death rc, the transient classifier sees nothing
    transient, and dispatch refuses by name instead of writing
    `status: running`."""
    fake_tmux.dying_respawns = 999  # every respawn dies, no transient bytes
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 6, f"a dead held seat must refuse, got rc {code}"
    agents = _agents(project)
    assert all(a.get("status") != "running" for a in agents), agents

    issue = [json.loads(l) for l in capsys.readouterr().out.splitlines()
             if l.lstrip().startswith("{")]
    assert issue and "held pane process died" in issue[0]["detail"], issue


def test_transient_death_of_a_held_seat_triggers_the_bounded_retry(
        project, fake_tmux, monkeypatch):
    """The first held seat dies leaving ONLY the catalogue warning + a 5xx
    signature: dispatch re-spawns under the SAME log, names attempt 2, and
    registers the SECOND (live) seat -- the direct-`Popen` transient path,
    reached because `HeldProc.poll` no longer lies with rc 0."""
    fake_tmux.dying_respawns = 1
    fake_tmux.log_bytes = CATALOGUE + DEAD_520
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(fake_tmux.respawns()) == 2, "the transient death was not retried"
    agents = _agents(project)
    assert len(agents) == 1 and agents[0]["status"] == "running", agents
    assert agents[0]["pid"] in fake_tmux.alive_pids, \
        "the registered pid must be the LIVE re-spawned seat"

    logs = sorted(project.glob(".agi/sessions/**/output.log"))
    assert len(logs) == 1, f"re-spawn must reuse the SAME log: {logs}"
    assert "attempt 2" in logs[0].read_text()