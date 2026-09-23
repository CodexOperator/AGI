"""goal:g7.31.1.2 -- durable named tmux pane seam.

The falsifier: kill the seat process, restart reattaches to the SAME named
tmux pane; no second `new-window` for a name that already exists. These tests
drive `tmux_seat.ensure_pane` with an injected recording runner (never live
tmux; the conftest guard would answer rc-1 anyway), and prove the real call
site -- `rotate._launch_window` -- reaches the seam.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import tmux_seat  # noqa: E402
import rotate  # noqa: E402


class _Proc:
    def __init__(self, argv, rc, stdout="", stderr=""):
        self.args = argv
        self.returncode = rc
        self.stdout = stdout
        self.stderr = stderr


class FakeTmux:
    """Records argv; `windows` is the set of names a `list-windows` would show."""

    def __init__(self, windows=()):
        self.windows = set(windows)
        self.calls = []

    def __call__(self, argv):
        self.calls.append(list(argv))
        verb = argv[1]
        if verb == "list-windows":
            return _Proc(argv, 0, stdout="\n".join(sorted(self.windows)))
        if verb == "new-window":
            self.windows.add(argv[argv.index("-n") + 1])
            return _Proc(argv, 0, stdout="@7\n")
        return _Proc(argv, 0)

    def argv_for(self, verb):
        return [c for c in self.calls if c[1] == verb]


def test_first_launch_creates_named_window_and_makes_it_durable():
    fake = FakeTmux()
    op, _proc = tmux_seat.ensure_pane("agi-rc", "seat-a", "cmd", runner=fake)

    assert op == "new", "no window of this name existed; this is a first launch"
    new = fake.argv_for("new-window")
    assert len(new) == 1
    assert new[0][new[0].index("-n") + 1] == "seat-a"
    opt = fake.argv_for("set-option")
    assert len(opt) == 1, "durability must be set at first launch"
    assert opt[0][-2:] == ["remain-on-exit", "on"]
    assert "agi-rc:seat-a" in opt[0]
    # guard on the guard: a genuine call IS recorded (not a vacuous fake)
    assert fake.calls, "the runner recorded nothing"


def test_reattach_after_process_death_issues_no_second_new_window():
    # The pane survived the process: `remain-on-exit on` left a dead pane
    # behind, so list-windows still reports the name.
    fake = FakeTmux(windows={"seat-a"})
    op, _proc = tmux_seat.ensure_pane("agi-rc", "seat-a", "cmd2", runner=fake)

    assert op == "respawn"
    assert fake.argv_for("new-window") == [], "must NOT open a second window"
    respawn = fake.argv_for("respawn-window")
    assert len(respawn) == 1, "the SAME pane must be addressed by name"
    assert "agi-rc:seat-a" in respawn[0]
    assert respawn[0][-1] == "cmd2"


def test_launch_window_call_site_reaches_the_seam(monkeypatch):
    """Wire probe: the real seat launch path calls the seam (file:line named
    in the node). The seam is not exercised only by these tests."""
    seen = {}

    def fake_ensure(session, name, shell_cmd, *, runner=None):
        seen["args"] = (session, name, shell_cmd)
        return "new", _Proc([], 0)

    monkeypatch.setattr(rotate.tmux_seat, "ensure_pane", fake_ensure)
    rc = rotate._launch_window("agi-rc", "wire-seat", "echo hi")

    assert rc == 0
    assert seen["args"][0] == "agi-rc"
    assert seen["args"][1] == "wire-seat"
    assert seen["args"][2].endswith("echo hi")


def test_recovery_call_site_reattaches_the_same_pane(monkeypatch, tmp_path):
    """The second real call site -- `heal._launch_recovered`, the dead-seat
    restart path -- reattaches through the seam: the pane survived the process
    (`remain-on-exit`), so no second `new-window` is issued for the name."""
    import heal  # noqa: PLC0415

    fake = FakeTmux(windows={"seat-wt"})
    monkeypatch.setattr(tmux_seat, "_default_runner", fake)
    _pid, _wid = heal._launch_recovered(
        tmp_path, "seat-wt", "echo back", cwd=tmp_path)

    assert fake.argv_for("new-window") == [], "recovery must reattach"
    respawn = fake.argv_for("respawn-window")
    assert len(respawn) == 1
    assert "agi-rc:seat-wt" in respawn[0]
