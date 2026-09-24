"""Named-pane restart holder; direct Popen is the explicit fallback."""
from __future__ import annotations
import hashlib, os, subprocess

def _socket(pane_name):
    return "agi-hold-" + hashlib.sha256(pane_name.encode()).hexdigest()[:16]

def start_held(args, env, *, cwd, pane_name, log_file):
    """Return a live deterministic pane pid, recreating its private server if needed."""
    socket = _socket(pane_name)
    def tmux(*cmd, **kw):
        return subprocess.run(["tmux", "-L", socket, *cmd], env=env,
            capture_output=True, text=True, check=False, **kw)
    try:
        found = tmux("display-message", "-p", "-t", pane_name, "#{pane_pid} #{pane_dead}")
        if found.returncode == 0 and found.stdout.strip():
            pid, dead = found.stdout.split()[:2]
            if dead == "0":
                return int(pid)
        # A private server is replaced wholesale: its inherited environment is
        # the only secret-safe way to give the new pane its exact child_env.
        tmux("kill-server")
        # Popen supplies a file object, but tmux's shell command needs a path.
        # Keep the object alive for the direct fallback and hand only its name
        # to tmux; str(file) leaks a repr like <_io.BufferedWriter ...>.
        log_path = getattr(log_file, "name", log_file)
        launched = tmux("new-session", "-d", "-P", "-F", "#{pane_pid}",
            "-s", pane_name, "-n", pane_name, "-c", cwd, "--",
            "sh", "-c", 'log=$1; shift; exec "$@" >>"$log" 2>&1',
            "hold", os.fspath(log_path), *args)
        if launched.returncode == 0 and launched.stdout.strip():
            return int(launched.stdout.strip())
    except (OSError, ValueError):
        pass
    return subprocess.Popen(args, env=env, cwd=cwd, stdout=log_file,
        stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
        start_new_session=True).pid

def enabled():
    return os.environ.get("HOLD_PANE", "").lower() in {"1", "true", "yes", "on"}
