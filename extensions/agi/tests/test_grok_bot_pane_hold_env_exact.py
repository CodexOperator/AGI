"""goal:g7.31.1.2 -- the pane child's environment EQUALS the passed `env`.

`tmux -e K=V` only ADDS to the tmux SERVER's environment; it can never REMOVE
a variable the server already carries (measured on real tmux 3.4). Kid-2's
suite measured a shim that HONOURED `-e`, so the leak stayed invisible. These
tests use REAL tmux, isolated under a private TMUX_TMPDIR, and read the pane
child's OWN `env` output.

F (gate): a present-but-broken tmux (`PermissionError`) is tmux PRESENT, not
absent -- it must raise `PaneHoldError`, never fall back to an anonymous
`Popen`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")

HARNESS = {"adapter": "grok_bot", "models": {}}


@pytest.fixture(autouse=True)
def _no_real_tmux():
    """Override conftest's project-wide tmux guard so REAL tmux is reachable.

    Isolation is the `real_tmux` fixture's private TMUX_TMPDIR, never the
    shared server: the guard would otherwise answer rc-1 before PATH and no
    real-tmux measurement could exist.
    """
    yield


@pytest.fixture
def real_tmux(tmp_path, monkeypatch):
    """A private tmux server, on its own socket dir, killed at teardown."""
    if shutil.which("tmux") is None:
        pytest.skip("no real tmux on this box")
    sock = tmp_path / "tmux-sock"
    sock.mkdir()
    monkeypatch.setenv("TMUX_TMPDIR", str(sock))
    yield sock
    subprocess.run(["tmux", "kill-server"], capture_output=True)


def _sess(tmp_path) -> Path:
    s = tmp_path / "iter-X" / "a00-seat"
    s.mkdir(parents=True, exist_ok=True)
    return s


def _dump_script(tmp_path, out: Path) -> str:
    p = tmp_path / "dump_env.sh"
    p.write_text(f'#!/bin/bash\nenv > "{out}"\nsleep 120\n')
    p.chmod(0o755)
    return str(p)


def _reap(pid):
    try:
        os.kill(pid, 9)
    except OSError:
        pass


def test_real_tmux_scrubbed_child_env_reaches_the_pane(tmp_path, real_tmux,
                                                       monkeypatch):
    """The integrated restart path on real tmux: the credential-none rule's
    OPENROUTER_API_KEY must not reach the pane child; a marker must."""
    out = tmp_path / "child.txt"
    monkeypatch.setenv("OPENROUTER_API_KEY", "SENTINEL-DO-NOT-LEAK")
    monkeypatch.setenv("GROK_TEST_MARKER", "kept")
    # Seed the tmux SERVER env with the key too: env -i, not -e, must strip it.
    subprocess.run(["tmux", "new-session", "-d", "-s", "seed", "sleep 120"],
                   check=True)
    sess = _sess(tmp_path)
    pid = grok.restart(
        harness={**HARNESS, "bin": _dump_script(tmp_path, out),
                 "env": {"GROK_TEST_MARKER": "kept"}},
        tier="kid", context_file=str(sess / "context.md"),
        agent_id="a00-seat", iter_n=1, sess_dir=sess, hold_pane=True)
    for _ in range(40):
        if out.exists() and out.read_text().strip():
            break
        time.sleep(0.05)
    text = out.read_text()
    assert "GROK_TEST_MARKER=kept" in text, "the scrubbed env must reach the pane"
    assert "OPENROUTER_API_KEY" not in text, (
        "a variable the tmux server carries must be REMOVED, not merely "
        "overridden: " + text)
    _reap(pid)


def test_env_i_removes_a_server_carried_variable(tmp_path, real_tmux):
    """The mechanism, directly: `env=None` (today's inherit) shows the
    sentinel reaching the child; the passed `env` without it does not."""
    sent = "PARENT_SENTINEL_MUST_NOT_REACH_CHILD"
    os.environ[sent] = "leak-me"
    subprocess.run(["tmux", "new-session", "-d", "-s", "seed", "sleep 120"],
                   check=True)
    try:
        inherit = tmp_path / "inherit.txt"
        grok.hold_in_pane(
            name="agi-seat-inherit",
            args=["bash", "-c", f'env > "{inherit}"; sleep 120'],
            cwd=tmp_path, env=None)
        for _ in range(40):
            if inherit.exists() and inherit.read_text().strip():
                break
            time.sleep(0.05)
        assert sent in inherit.read_text(), (
            "non-vacuity: the tmux server DOES carry the sentinel")

        scrubbed = tmp_path / "scrubbed.txt"
        env = {k: v for k, v in os.environ.items() if k != sent}
        grok.hold_in_pane(
            name="agi-seat-scrubbed",
            args=["bash", "-c", f'env > "{scrubbed}"; sleep 120'],
            cwd=tmp_path, env=env)
        for _ in range(40):
            if scrubbed.exists() and scrubbed.read_text().strip():
                break
            time.sleep(0.05)
        text = scrubbed.read_text()
        assert "GROK_TEST_MARKER" not in text  # sanity: this is the other pane
        assert sent not in text, "env -i must remove the server-carried var"
    finally:
        os.environ.pop(sent, None)


def test_present_but_broken_tmux_is_a_named_refusal(tmp_path, monkeypatch):
    """PermissionError = tmux PRESENT, broken. A named PaneHoldError, never an
    anonymous Popen (the goal forbids anonymous persistent seats)."""
    def broken(*a, **k):
        raise PermissionError("tmux: permission denied")

    def no_popen(*a, **k):
        raise AssertionError("a broken tmux must never fall back to Popen")

    monkeypatch.setattr(grok.subprocess, "run", broken)
    monkeypatch.setattr(grok.subprocess, "Popen", no_popen)
    with pytest.raises(grok.PaneHoldError):
        grok.restart(
            harness={**HARNESS, "bin": "/bin/true"}, tier="kid",
            context_file=str(_sess(tmp_path) / "context.md"),
            agent_id="a00-seat", iter_n=1, sess_dir=_sess(tmp_path),
            hold_pane=True)
    assert not (_sess(tmp_path) / "output.log").exists(), (
        "the anonymous Popen fallback opens output.log before spawning")
