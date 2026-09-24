"""Named tmux pane seam used by dispatch and restart."""
from __future__ import annotations
import os, shlex, subprocess

def _run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)

def _pane(name):
    r = _run(["tmux", "list-panes", "-a", "-F", "#{pane_id}\t#{pane_current_path}\t#{pane_pid}", "-t", name])
    for line in r.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and (parts[1] == name or name in parts[1]):
            return {"pane_id": parts[0], "pid": int(parts[2]), "created": False}
    return None

def start(name, argv, cwd=None, env=None):
    """Start once, or return the existing named pane; never claim fallback."""
    old = _pane(name)
    if old: return old
    cmd = ["tmux", "new-session", "-d", "-s", name]
    if cwd: cmd += ["-c", str(cwd)]
    if env:
        prefix = " ".join(f"{k}={shlex.quote(str(v))}" for k, v in env.items())
        argv = ["/bin/sh", "-lc", f"{prefix} exec {shlex.join(argv)}"]
    r = _run(cmd + [shlex.join(argv)])
    if r.returncode: return None
    return _pane(name)

def reattach(name, argv, cwd=None, env=None):
    """Respawn the named pane in place, preserving its tmux pane identity."""
    pane = _pane(name)
    if not pane: return start(name, argv, cwd, env)
    cmd = ["tmux", "respawn-pane", "-k", "-t", pane["pane_id"]]
    if cwd: cmd += ["-c", str(cwd)]
    if env: cmd[1:1] = ["-e", ",".join(f"{k}={v}" for k,v in env.items())]
    r = _run(cmd + [shlex.join(argv)])
    return pane if r.returncode == 0 else None
