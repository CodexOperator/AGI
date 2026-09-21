"""Durable named tmux pane hold — adapter seam (`goal:g7.31.1.2`).
One pane per seat; its `#{pane_id}` and window name survive the seat process
dying, so `restart` re-enters the SAME pane, not a fresh anonymous one. Opt-in
via `harness["tmux"]`; unset keeps direct-`Popen`. A pane has no name of its
own, so the window carries the seat name and holds exactly one pane.
"""
from __future__ import annotations

import hashlib
import shlex
import subprocess

DEFAULT_SESSION = "agi-hold"


def enabled(harness: dict) -> bool:
    return bool(harness.get("tmux") or harness.get("pane"))


def pane_name(agent_id: str) -> str:
    """Deterministic seat -> pane window name (hashed target-safe)."""
    return "seat-" + hashlib.sha1(str(agent_id).encode()).hexdigest()[:12]


def _session(harness: dict) -> str:
    return str(harness.get("tmux_session") or DEFAULT_SESSION)


def panes(harness: dict) -> list[tuple[str, str, str]]:
    """[(window_name, pane_id, pane_pid)]; empty if the session is absent."""
    cp = subprocess.run(
        ["tmux", "list-panes", "-t", _session(harness), "-F",
         "#{window_name} #{pane_id} #{pane_pid}"], capture_output=True, text=True)
    return [] if cp.returncode else [
        tuple(ln.split()) for ln in cp.stdout.splitlines() if ln.strip()]
def _pid(harness: dict, name: str) -> int | None:
    return next((int(p) for w, _i, p in panes(harness) if w == name), None)
def _cmd(argv, log_file):
    if not log_file:
        return list(argv)
    return ["sh", "-c", "exec >>" + shlex.quote(str(log_file)) + " 2>&1; exec "
            + " ".join(shlex.quote(a) for a in argv)]
def _run(args):
    return subprocess.run(args, capture_output=True, text=True)
def start(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None):
    """Create the named pane ONLY if absent, then run argv inside it."""
    name, sess, have = pane_name(agent_id), _session(harness), panes(harness)
    if not have:
        args = ["tmux", "new-session", "-d", "-s", sess, "-n", name,
                "-c", str(cwd), "--", *_cmd(argv, log_file)]
    elif not any(w == name for w, _, _ in have):
        args = ["tmux", "new-window", "-t", sess, "-n", name,
                "-c", str(cwd), "--", *_cmd(argv, log_file)]
    else:
        return reattach(harness, agent_id, argv, cwd=cwd, log_file=log_file)
    if _run(args).returncode != 0:
        return None
    _run(["tmux", "set-option", "-t", sess, "remain-on-exit", "on"])
    return _pid(harness, name)
def reattach(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None):
    """Re-enter the SAME pane after death — respawn-pane -k, no second window."""
    name, sess, have = pane_name(agent_id), _session(harness), panes(harness)
    if not any(w == name for w, _, _ in have):
        return start(harness, agent_id, argv, cwd=cwd, log_file=log_file)
    cp = _run(["tmux", "respawn-pane", "-k", "-t", f"{sess}:{name}",
               "-c", str(cwd), "--", *_cmd(argv, log_file)])
    return _pid(harness, name) if cp.returncode == 0 else None
