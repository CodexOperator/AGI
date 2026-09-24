"""Named-pane restart holder; direct Popen is the explicit fallback."""
from __future__ import annotations
import os, subprocess

def start_held(args, env, *, cwd, pane_name, log_file):
    """Attach to a deterministic pane, else create it; return its pid."""
    try:
        found = subprocess.run(["tmux", "display-message", "-p", "-t", pane_name,
            "#{pane_pid}"], env=env, capture_output=True, text=True, check=False)
        if found.returncode == 0 and found.stdout.strip():
            return int(found.stdout.strip())
        launched = subprocess.run(["tmux", "new-window", "-d", "-n", pane_name,
            "--", *args], env=env, cwd=cwd, stdout=log_file,
            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, check=False)
        if launched.returncode == 0:
            pid = subprocess.run(["tmux", "display-message", "-p", "-t", pane_name,
                "#{pane_pid}"], env=env, capture_output=True, text=True, check=False)
            if pid.returncode == 0 and pid.stdout.strip():
                return int(pid.stdout.strip())
    except (OSError, ValueError):
        pass
    return subprocess.Popen(args, env=env, cwd=cwd, stdout=log_file,
        stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
        start_new_session=True).pid

def enabled():
    return os.environ.get("HOLD_PANE", "").lower() in {"1", "true", "yes", "on"}
