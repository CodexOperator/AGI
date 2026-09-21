"""Regression guard for `adapters/tmux_hold.py` (`goal:g7.31.1.2`).

The parent's probe 2 refuted the first version: `panes()` ran
`tmux list-panes -t <session>` WITHOUT `-s`, so it saw only the session's
CURRENT window. With a foreign window current and the seat's process dead,
`reattach()` could not find the seat by name, fell through to `start()`, and
issued a SECOND `new-window -n seat-<hash>` -- two panes for one seat.

The fake below models tmux's current-window semantics deliberately: a
`list-panes` without `-s` returns ONLY the current window. A regression that
drops `-s` therefore reproduces the duplicate, not a green lie.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

from adapters import tmux_hold  # noqa: E402

AGENT = "a00-test-seat"
SEAT = tmux_hold.pane_name(AGENT)


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
    assert "-s" in fake.calls[0]


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