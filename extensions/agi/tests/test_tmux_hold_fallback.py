"""The tmux hold must never brick a restart (`goal:g7.31.1.2.3`).

The falsifier has two halves and both are behavioural: with tmux genuinely
unavailable, or with no session name configured, `grok_bot_adapter.restart`
STILL returns a real pid through the untouched Popen path. A hold that logs
and returns None inside the adapter while the adapter ignores it would satisfy
every sentence of the module's prose and lose the mechanism — so these tests
call the real `restart`, not `hold_or_none` in isolation.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
from adapters import tmux_hold  # noqa: E402

grok = adapters.load("grok_bot")

RESTART_HARNESS = {"adapter": "grok_bot", "models": {"kid": "grok-kid"}}
HELD = {"adapter": "grok_bot", "models": {"kid": "grok-kid"},
        "tmux": True, "tmux_session": "agi-rc"}


class _FakeProc:
    pid = 4242


def _restart(grok_mod, tmp_path, harness):
    """A real `restart` call with Popen faked, returning (pid, pops, rec)."""
    pops = []

    def fake_popen(args, **kwargs):
        pops.append((args, kwargs))
        return _FakeProc()

    orig = grok_mod.subprocess.Popen
    grok_mod.subprocess.Popen = fake_popen
    try:
        sess = tmp_path / "sess"
        sess.mkdir(exist_ok=True)
        rec = {"worktree": str(tmp_path)}
        pid = grok_mod.restart(
            harness=harness, tier="kid", context_file=str(tmp_path / "c.md"),
            agent_id="a00-test", iter_n=1, sess_dir=sess, agent_record=rec)
    finally:
        grok_mod.subprocess.Popen = orig
    return pid, pops, rec


# ------------------------------------------------------------- the fallback


def test_no_tmux_binary_still_restarts_via_popen(monkeypatch, tmp_path):
    """`shutil.which("tmux") -> None`: the hold is declined and Popen runs."""
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: None)
    pid, pops, rec = _restart(grok, tmp_path, HELD)
    assert pid == 4242
    assert len(pops) == 1
    assert rec["pid"] == 4242 and rec["status"] == "restarted"


def test_no_session_name_still_restarts_via_popen(monkeypatch, tmp_path):
    """No `tmux_session` on the harness and none in the live config's `box`
    cell: the resolver returns None instead of raising, and Popen runs."""
    monkeypatch.setattr(tmux_hold, "session", lambda harness: None)
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: "/usr/bin/tmux")
    pid, pops, rec = _restart(grok, tmp_path, HELD)
    assert pid == 4242 and len(pops) == 1 and rec["pid"] == 4242


def test_tmux_nonzero_still_restarts_via_popen(monkeypatch, tmp_path):
    """tmux present and named, but every call fails: no pane, no hold, Popen."""
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(tmux_hold, "session", lambda harness: "agi-rc")
    monkeypatch.setattr(tmux_hold, "_run", lambda args: _cp(1))
    pid, pops, _ = _restart(grok, tmp_path, HELD)
    assert pid == 4242 and len(pops) == 1


def test_unconfigured_harness_is_not_held(monkeypatch, tmp_path):
    """Hold is OPT-IN. An ordinary harness row takes Popen even where tmux
    works, so a default-on hold cannot make a box depend on a binary."""
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: "/usr/bin/tmux")
    pid, pops, _ = _restart(grok, tmp_path, RESTART_HARNESS)
    assert pid == 4242 and len(pops) == 1


# ------------------------------------------------------------ the hold path


def test_a_held_pane_is_returned_and_popen_is_never_called(monkeypatch, tmp_path):
    """The wiring is the claim: when the hold succeeds, the seat's pid comes
    from the PANE and `Popen` is not reached at all."""
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(tmux_hold, "start", lambda *a, **k: 777)
    pid, pops, rec = _restart(grok, tmp_path, HELD)
    assert pid == 777
    assert pops == []
    assert rec["pid"] == 777 and rec["status"] == "restarted"


def test_hold_or_none_never_raises(monkeypatch):
    """A raising `start` is swallowed: the fallback is the whole point."""
    monkeypatch.setattr(tmux_hold.shutil, "which", lambda name: "/usr/bin/tmux")

    def boom(*a, **k):
        raise RuntimeError("tmux_hold: no session name")

    monkeypatch.setattr(tmux_hold, "start", boom)
    assert tmux_hold.hold_or_none(HELD, "a00", ["x"], cwd="/tmp") is None


# -------------------------------------------------------------- the shape


def test_pane_name_is_deterministic_and_seat_scoped():
    """The seat's spine: one stable name per agent id, target-safe."""
    assert tmux_hold.pane_name("a00-x") == tmux_hold.pane_name("a00-x")
    assert tmux_hold.pane_name("a00-x") != tmux_hold.pane_name("a00-y")
    assert tmux_hold.pane_name("a00-x").startswith("seat-")


def test_panes_lists_session_wide(monkeypatch):
    """`-s` or a seat in a non-current window is invisible and gets duplicated.
    Also: an unset session yields [] rather than a `tmux list-panes -t None`."""
    seen = {}

    def fake_run(args, **kw):
        seen["args"] = args
        return _cp(0, out="seat-abc %3 4242\n")

    monkeypatch.setattr(tmux_hold, "session", lambda h: "agi-rc")
    monkeypatch.setattr(tmux_hold, "_run", fake_run)
    assert tmux_hold.panes(HELD) == [("seat-abc", "%3", "4242")]
    assert "-s" in seen["args"]
    monkeypatch.setattr(tmux_hold, "session", lambda h: None)
    assert tmux_hold.panes(HELD) == []


def test_remain_on_exit_is_set_before_the_respawn(monkeypatch):
    """Ordering is load-bearing: set after the real command, a fast-failing
    process takes the pane with it and the seat is duplicated on restart."""
    calls = []
    name = tmux_hold.pane_name("a00-x")

    def fake_run(args, **kw):
        calls.append(args[1])
        return _cp(0, out=f"{name} %3 4242\n")

    monkeypatch.setattr(tmux_hold, "session", lambda h: "agi-rc")
    monkeypatch.setattr(tmux_hold, "_run", fake_run)
    assert tmux_hold.start(HELD, "a00-x", ["run"], cwd="/tmp") == 4242
    assert calls.index("set-option") < calls.index("respawn-pane")


def _cp(code, out=""):
    class _R:
        returncode = code
        stdout = out
        stderr = ""
    return _R()
