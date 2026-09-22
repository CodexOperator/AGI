"""Regression + integration guard for `adapters/tmux_hold.py` (`goal:g7.31.1.2`).

Everything here runs against `FakeTmux`, a fake of tmux's real semantics. No
committed test starts or kills a real tmux session and none signals a real
pane process: the conftest `_no_real_tmux` autouse guard is never defeated.
The claims a real server used to prove (first-spawn founds the pane;
`remain-on-exit` is set before the process could exit; restart re-enters the
SAME `#{pane_id}` with `created: False`; a killed window recreates once with
`created: True`; the child env survives restart) are re-expressed here as
fake-driven tests, because a faithful fake is the proof and shelling out is
the defect.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
from adapters import tmux_hold  # noqa: E402

grok = adapters.load("grok_bot")

AGENT = "a00-test-seat"
SEAT = tmux_hold.pane_name(AGENT)


# --------------------------------------------------------------- fake tmux


class FakeTmux:
    """Minimal tmux: sessions hold windows; one window is current per session.

    `-s` on `list-panes` is what makes a non-current window visible. A
    `respawn-pane` advances the pane's pid, so a caller can tell a re-entered
    pane from a fabricated one by its immutable `#{pane_id}`.
    """

    def __init__(self):
        self.sessions: dict[str, dict] = {}
        self.calls: list[list[str]] = []
        self._next_pane = 10

    def _pane(self, sess, name, pid):
        self._next_pane += 1
        return {"name": name, "pane": f"%{self._next_pane}", "pid": pid,
                "dead": 0, "window": f"@{self._next_pane}"}

    def _find_pane(self, target):
        for sess in self.sessions.values():
            for w in sess["windows"]:
                if target in (w["pane"], w["window"]):
                    return w
        return None

    def run(self, cmd, *a, **k):
        self.calls.append(list(cmd))
        s = self.sessions
        rc, out = 0, ""
        if cmd[1] == "list-panes":
            name = cmd[cmd.index("-t") + 1]
            if name not in s:
                rc = 1
            else:
                wins = s[name]["windows"]
                rows = wins if "-s" in cmd else [wins[s[name]["current"]]]
                out = "".join(f"{w['name']} {w['pane']} {w['pid']}\n"
                              for w in rows)
        elif cmd[1] == "new-session":
            name = cmd[cmd.index("-s") + 1]
            w = self._pane(name, cmd[cmd.index("-n") + 1], 1000)
            s[name] = {"windows": [w], "current": 0}
        elif cmd[1] == "new-window":
            name = cmd[cmd.index("-t") + 1]
            w = self._pane(name, cmd[cmd.index("-n") + 1], 2000)
            s[name]["windows"].append(w)
            s[name]["current"] = len(s[name]["windows"]) - 1
        elif cmd[1] == "respawn-pane":
            w = self._find_pane(cmd[cmd.index("-t") + 1].split(":")[-1])
            if w is None:
                rc = 1
            else:
                w["pid"] += 1
                w["dead"] = 0
        return subprocess.CompletedProcess(cmd, rc, out, "")

    def seat_windows(self):
        return [w for w in self.sessions["S"]["windows"] if w["name"] == SEAT]


@pytest.fixture
def fake(monkeypatch):
    f = FakeTmux()
    monkeypatch.setattr(subprocess, "run", f.run)
    return f


HARNESS = {"tmux": True, "tmux_session": "S"}
ARGV = ["/bin/true"]


def _session_with_seat_and_foreign_current(fake):
    """Seat's own window exists but a FOREIGN window is current."""
    fake.run(["tmux", "new-session", "-d", "-s", "S", "-n", SEAT])
    fake.run(["tmux", "new-window", "-t", "S", "-n", "other"])
    s = fake.sessions["S"]
    s["current"] = 1  # `other` is current; the seat window is not
    return s


def test_panes_enumerates_session_wide(fake):
    """`panes()` must pass `-s` or it cannot see a non-current window."""
    _session_with_seat_and_foreign_current(fake)
    rows = tmux_hold.panes(HARNESS)
    assert [r[0] for r in rows] == [SEAT, "other"]
    list_calls = [c for c in fake.calls if c[1] == "list-panes"]
    assert list_calls, "panes() issued no list-panes call"
    assert "-s" in list_calls[0]


def test_reattach_addresses_by_pane_id_not_current_window(fake):
    s = _session_with_seat_and_foreign_current(fake)
    held = s["windows"][0]["pane"]
    before = len(fake.calls)
    pid = tmux_hold.reattach(HARNESS, AGENT, ARGV, cwd="/tmp")
    verbs = [c[1] for c in fake.calls[before:]]
    assert "new-window" not in verbs  # no fabricated second seat window
    assert "new-session" not in verbs
    assert any(c[1] == "respawn-pane" and c[c.index("-t") + 1] == held
               for c in fake.calls)  # immutable pane id, not `S:seat-...`
    assert len(fake.seat_windows()) == 1
    assert pid == fake.seat_windows()[0]["pid"]
    assert s["current"] == 1  # foreign window untouched


def test_start_reuses_non_current_named_pane(fake):
    s = _session_with_seat_and_foreign_current(fake)
    pid = tmux_hold.start(HARNESS, AGENT, ARGV, cwd="/tmp")
    assert [c[1] for c in fake.calls].count("new-window") == 1  # `other` only
    assert len(fake.seat_windows()) == 1
    assert pid == s["windows"][0]["pid"]


def test_first_spawn_founds_the_named_pane(fake):
    """The FIRST spawn (`spawn`, what dispatch's `_open_round` calls) creates
    the seat's pane before any restart could attach to it."""
    held = tmux_hold.spawn(HARNESS, AGENT, ARGV, cwd="/tmp")
    assert "S" in fake.sessions
    assert len(fake.seat_windows()) == 1
    assert held is not None and held.pid == fake.seat_windows()[0]["pid"]


def test_pane_founded_with_remain_on_exit_before_the_process_runs(fake):
    """`remain-on-exit` is set on the pane BEFORE `respawn-pane`, so a
    fast-failing process cannot close the window and take the hold with it."""
    tmux_hold.spawn(HARNESS, AGENT, ARGV, cwd="/tmp")
    verbs = [c[1] for c in fake.calls]
    setopt = [c for c in fake.calls if c[1] == "set-option"]
    assert setopt and "remain-on-exit" in setopt[0] and "on" in setopt[0]
    assert verbs.index("set-option") < verbs.index("respawn-pane")


def test_reattach_of_genuinely_gone_pane_creates_once_and_says_so(fake):
    """Window killed (not just the process): recreate ONCE, record `created`."""
    fake.run(["tmux", "new-session", "-d", "-s", "S", "-n", "other"])
    created: dict = {}
    pid = tmux_hold.reattach(HARNESS, AGENT, ARGV, cwd="/tmp", created=created)
    assert created == {"created": True, "pane_id": fake.seat_windows()[0]["pane"]}
    assert len(fake.seat_windows()) == 1
    assert pid == fake.seat_windows()[0]["pid"]


def test_reattach_of_held_pane_records_not_created(fake):
    s = _session_with_seat_and_foreign_current(fake)
    created: dict = {}
    tmux_hold.reattach(HARNESS, AGENT, ARGV, cwd="/tmp", created=created)
    assert created == {"created": False, "pane_id": s["windows"][0]["pane"]}


def test_restart_carries_the_child_env_into_the_respawn_command(fake):
    """`respawn-pane` inherits the tmux SERVER's environment, so the child env
    must ride the command itself; an `env`-less reattach strips the seat.
    Both a `harness["env"]` cell and the base environ are asserted, because
    `child_env` merges both (`goal:g7.31.1.2`)."""
    _session_with_seat_and_foreign_current(fake)
    harness = grok.hold_harness({"adapter": "grok_bot", "tmux_session": "S",
                                 "env": {"DT67_PROBE": "hello"}})
    env = grok.child_env(harness=harness,
                         base={**os.environ, "DT67_BASE_PROBE": "base-hello"},
                         tier="kid")
    before = len(fake.calls)
    tmux_hold.reattach(HARNESS, AGENT, ARGV, cwd="/tmp", env=env)
    respawn = [c for c in fake.calls[before:] if c[1] == "respawn-pane"]
    assert respawn, "reattach issued no respawn-pane"
    assert "DT67_PROBE=hello" in respawn[0]
    assert "DT67_BASE_PROBE=base-hello" in respawn[0]


def test_restart_hold_branch_passes_child_env(fake, monkeypatch, tmp_path):
    """Supporting (fixtures) guard: `restart`'s hold branch hands `reattach`
    the SAME child env the non-hold `Popen` branch passes."""
    _session_with_seat_and_foreign_current(fake)
    monkeypatch.setenv("DT67_BASE_PROBE", "base-hello")
    harness = grok.hold_harness({"adapter": "grok_bot", "tmux_session": "S"})
    harness = {**harness, "env": {"DT67_PROBE": "hello"}}
    seen: dict = {}
    real = tmux_hold.reattach
    monkeypatch.setattr(
        tmux_hold, "reattach",
        lambda *a, **k: (seen.update(k), real(*a, **k))[1])
    seat_dir = tmp_path / "sess"
    seat_dir.mkdir()
    grok.restart(harness=harness, tier="kid", context_file="c.md",
                 agent_id=AGENT, iter_n=1, sess_dir=seat_dir,
                 agent_record={})
    assert seen.get("env", {}).get("DT67_PROBE") == "hello"
    assert seen["env"].get("DT67_BASE_PROBE") == "base-hello"


# ------------------------------------------------------- held death semantics


def test_heldproc_reports_a_dead_pane_as_a_nonzero_death(monkeypatch):
    """A dead pane process is a DEATH, not a clean rc 0. dispatch reads rc 0
    as a clean startup (`_await_startup(proc) or proc.returncode == 0`) and
    would register a dead held seat `status: running` (`goal:g7.31.1.2`)."""
    monkeypatch.setattr(tmux_hold, "_alive", lambda pid: False)
    assert tmux_hold.HeldProc(4242).poll() == 1
    monkeypatch.setattr(tmux_hold, "_alive", lambda pid: True)
    assert tmux_hold.HeldProc(4243).poll() is None


def test_heldproc_keeps_its_first_death_rc(monkeypatch):
    monkeypatch.setattr(tmux_hold, "_alive", lambda pid: False)
    p = tmux_hold.HeldProc(4244)
    assert p.poll() == 1 and p.returncode == 1
    monkeypatch.setattr(tmux_hold, "_alive", lambda pid: True)
    assert p.poll() == 1  # once dead, never resurrected by a later poll


# --------------------------------------------------- adapter-declared hold


def test_grok_adapter_declares_the_hold_without_a_config_cell():
    """The hold is decided from the adapter's own declaration, not a dispatch
    string branch (`goal:g7.31.1.2` deliverable B)."""
    assert grok.HOLD_PANE is True
    assert grok.hold_harness({"adapter": "grok_bot"}).get("tmux") is True
    # an explicit opt-out wins outright
    assert grok.hold_harness({"adapter": "grok_bot", "tmux": False})["tmux"] is False