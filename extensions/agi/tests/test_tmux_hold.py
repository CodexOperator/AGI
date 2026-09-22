"""Regression + integration guard for `adapters/tmux_hold.py` (`goal:g7.31.1.2`).

Two tiers, deliberately:

* `FakeTmux` unit tests model tmux's current-window semantics (a `list-panes`
  without `-s` returns ONLY the current window) so a regression that drops `-s`
  reproduces the duplicate window, not a green lie.
* The real-tmux test is the PROOF: it founds a pane on first spawn, captures
  the immutable `#{pane_id}`, kills the process, restarts through the adapter,
  and asserts the SAME pane id comes back with `created is False`. It skips BY
  NAME when `tmux` is absent so the suite is honest about what ran.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
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
    """Minimal tmux: sessions hold windows; one window is current per session."""

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


# --------------------------------------------------- adapter-declared hold


def test_grok_adapter_declares_the_hold_without_a_config_cell():
    """The hold is decided from the adapter's own declaration, not a dispatch
    string branch (`goal:g7.31.1.2` deliverable B)."""
    assert grok.HOLD_PANE is True
    assert grok.hold_harness({"adapter": "grok_bot"}).get("tmux") is True
    # an explicit opt-out wins outright
    assert grok.hold_harness({"adapter": "grok_bot", "tmux": False})["tmux"] is False


# --------------------------------------------------------- REAL tmux proof

needs_tmux = pytest.mark.skipif(
    shutil.which("tmux") is None,
    reason="real-tmux integration test: `tmux` absent on this box")

#: The real stdlib runner, captured at import -- BEFORE the suite's autouse
#: `_no_real_tmux` guard rebinds it. The guard exists to keep ordinary tests
#: away from the LIVE `agi-rc` session; the proof below is the deliberate
#: exception, on a scratch session it creates and kills itself.
_REAL_RUN = subprocess.run


@pytest.fixture
def real_tmux(monkeypatch):
    monkeypatch.setattr(subprocess, "run", _REAL_RUN)


def _probe_session() -> str:
    """A scratch session name -- never the live `agi-rc` box session."""
    return f"agi-dt67-probe-{os.getpid()}"


@needs_tmux
def test_real_tmux_first_spawn_founds_the_named_pane(tmp_path, real_tmux):
    """Acceptance 5: after the FIRST spawn (before any restart) the seat's
    window exists in the session, list-panes says so."""
    sess = _probe_session()
    harness = grok.hold_harness({"adapter": "grok_bot", "tmux_session": sess})
    try:
        held = tmux_hold.spawn(harness, AGENT, ["sh", "-c", "sleep 60"],
                               cwd=str(tmp_path), log_file=tmp_path / "out.log")
        assert held is not None and held.pid
        rows = tmux_hold.panes(harness)
        assert [r[0] for r in rows] == [SEAT]
        out = subprocess.run(
            ["tmux", "list-panes", "-s", "-t", sess, "-F", "#{window_name}"],
            capture_output=True, text=True).stdout
        assert SEAT in out
    finally:
        subprocess.run(["tmux", "kill-session", "-t", sess],
                       capture_output=True)


@needs_tmux
def test_real_tmux_restart_reenters_the_same_pane(tmp_path, real_tmux):
    """Acceptance 1/4: kill the process; restart re-enters the SAME immutable
    pane id and the record says `created: False`."""
    sess = _probe_session()
    harness = grok.hold_harness({"adapter": "grok_bot", "tmux_session": sess})
    seat_dir = tmp_path / "sess"
    seat_dir.mkdir()
    try:
        held = tmux_hold.spawn(harness, AGENT, ["sh", "-c", "sleep 60"],
                               cwd=str(tmp_path), log_file=seat_dir / "output.log")
        assert held is not None
        held_pane = next(i for w, i, _ in tmux_hold.panes(harness) if w == SEAT)

        os.kill(held.pid, signal.SIGKILL)
        for _ in range(50):
            if not tmux_hold._alive(held.pid):
                break
            time.sleep(0.05)
        assert not tmux_hold._alive(held.pid)

        rec = {"worktree": str(tmp_path)}
        pid = grok.restart(
            harness=harness, tier="kid", context_file=str(tmp_path / "context.md"),
            agent_id=AGENT, iter_n=1, sess_dir=seat_dir, agent_record=rec)
        assert pid is not None and pid != held.pid
        assert rec["tmux"] == {"created": False, "pane_id": held_pane}
        rows = tmux_hold.panes(harness)
        assert [(w, i) for w, i, _ in rows if w == SEAT] == [(SEAT, held_pane)]
        assert json.loads((seat_dir / "agent.json").read_text())["tmux"] == rec["tmux"]
    finally:
        subprocess.run(["tmux", "kill-session", "-t", sess],
                       capture_output=True)


@needs_tmux
def test_real_tmux_restart_of_gone_pane_recreates_once(tmp_path, real_tmux):
    """Acceptance 4: a genuinely lost pane reports `created: True` and is
    recreated exactly once."""
    sess = _probe_session()
    harness = grok.hold_harness({"adapter": "grok_bot", "tmux_session": sess})
    seat_dir = tmp_path / "sess"
    seat_dir.mkdir()
    try:
        held = tmux_hold.spawn(harness, AGENT, ["sh", "-c", "sleep 60"],
                               cwd=str(tmp_path), log_file=seat_dir / "output.log")
        assert held is not None
        # Kill the WINDOW, not merely the process: the pane is genuinely gone.
        subprocess.run(["tmux", "kill-window", "-t", SEAT], capture_output=True)
        assert tmux_hold.panes(harness) == []

        rec = {"worktree": str(tmp_path)}
        pid = grok.restart(
            harness=harness, tier="kid", context_file=str(tmp_path / "context.md"),
            agent_id=AGENT, iter_n=1, sess_dir=seat_dir, agent_record=rec)
        assert pid is not None
        assert rec["tmux"]["created"] is True
        seat_windows = [w for w, _, _ in tmux_hold.panes(harness) if w == SEAT]
        assert seat_windows == [SEAT]  # exactly one, not two
    finally:
        subprocess.run(["tmux", "kill-session", "-t", sess],
                       capture_output=True)