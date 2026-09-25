"""Named tmux launch adapter for persistent dispatch seats."""
from __future__ import annotations

import subprocess
from pathlib import Path


class PaneProcess:
    """The minimum process protocol dispatch needs for a tmux-hosted pane."""

    def __init__(self, pid: int):
        self.pid = pid
        self.returncode = None

    def poll(self):
        import os
        try:
            os.kill(self.pid, 0)
        except OSError:
            self.returncode = -1
        return self.returncode


def start(*, argv, log_file: Path, cwd: Path, env: dict[str, str],
          pane_name: str) -> dict:
    """Start one named pane and return dispatch's launch-result fields."""
    with open(log_file, "ab") as log:
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", pane_name, "-c", str(cwd),
             "--", *argv], env=env, stdout=log, stderr=subprocess.STDOUT,
            check=True)
    pane = subprocess.run(
        ["tmux", "list-panes", "-t", pane_name, "-F", "#{pane_id}\t#{pane_pid}"],
        capture_output=True, text=True, check=True).stdout.strip()
    pane_id, pid = pane.split("\t", 1)
    return {"process": PaneProcess(int(pid)), "pane_id": pane_id,
            "created": True, "adapter": "tmux_hold"}
