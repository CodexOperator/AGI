"""hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-
branches-go, conjunct (a): NO committed test in test_heal_worktree_refusal.py
reaches the LIVE tmux server.

The refusal tests drive the real `_watch_seats` pass with a fake LAUNCHER, but
the launcher is only one of the ways out of that pass: a nudge goes through
send.py, and send.py:2208-2209 defaults the session to
`rotate.DEFAULT_TMUX_SESSION` (the test root governs rows + inbox only), so a
test that stops stubbing would type into a live pane.

This is the RECORDING SHIM that proves it either way: a `tmux` on PATH that
appends its argv and exits 0. Run the file under it; every invocation aimed at
the default session is a live pane this suite just touched. Zero invocations
is the claim, and it is a MEASUREMENT — not a source grep that a future
refactor would make a lie.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TARGET = TESTS / "test_heal_worktree_refusal.py"


def test_no_refusal_test_touches_the_live_tmux_server(tmp_path):
    shim_dir = tmp_path / "bin"
    shim_dir.mkdir()
    log = tmp_path / "tmux.log"
    (shim_dir / "tmux").write_text(
        '#!/bin/sh\nprintf "%s\\n" "$*" >> "$AGI_TMUX_SHIM_LOG"\nexit 0\n',
        encoding="utf-8")
    (shim_dir / "tmux").chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = f"{shim_dir}{os.pathsep}{env.get('PATH', '')}"
    env["AGI_TMUX_SHIM_LOG"] = str(log)
    env.pop("AGI_TMUX_SESSION", None)

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(TARGET), "-q", "-p", "no:randomly"],
        cwd=TESTS.parent.parent.parent, env=env, capture_output=True,
        text=True, timeout=300, start_new_session=True)
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-2000:]

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "agi_rotate_for_guard", TESTS.parent / "bin" / "rotate.py")
    rotate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rotate)

    calls = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln] \
        if log.exists() else []
    live = [c for c in calls if rotate.DEFAULT_TMUX_SESSION in c]
    assert not live, (
        "a committed test reached the LIVE tmux server: "
        f"{live} (all recorded calls: {calls})")
