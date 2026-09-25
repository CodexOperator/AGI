#!/usr/bin/env python3
"""Launch an agent in a reusable tmux pane, with a direct-Popen fallback."""
from __future__ import annotations
import json, os, shlex, subprocess, sys, time
from pathlib import Path
class HeldProcess:
    def __init__(self, pid: int, pane_id: str, marker: Path):
        self.pid, self.pane_id, self._marker = pid, pane_id, marker
    def poll(self):
        try:
            return int(self._marker.read_text().strip())
        except (OSError, ValueError):
            return None

    @property
    def returncode(self):
        """Match subprocess.Popen's post-poll return-code contract."""
        return self.poll()
def _tmux(*args):
    result = subprocess.run(list(args), check=True, capture_output=True, text=True)
    output = getattr(result, "stdout", None)
    if result is None or output is None:
        raise OSError("tmux unavailable")
    return output.strip()
def start(argv, *, env, cwd, log, mode, seat, agent_id, state_dir, pane_id=None):
    state_dir.mkdir(parents=True, exist_ok=True)
    spec, marker = state_dir / "hold.json", state_dir / "hold.done"
    pid_file = state_dir / "hold.pid"
    marker.unlink(missing_ok=True); pid_file.unlink(missing_ok=True)
    spec.write_text(json.dumps({"argv": argv, "env": env, "cwd": str(cwd),
                                "log": str(log), "mode": mode}))
    spec.chmod(0o600)
    session = "agi-hold-" + "".join(c for c in f"{seat}-{agent_id}"
                                    if c.isalnum() or c in "-_")[:60]
    runner = f"{shlex.quote(sys.executable)} {shlex.quote(__file__)} _run {shlex.quote(str(spec))}"
    try:
        if not pane_id:
            _tmux("tmux", "new-session", "-d", "-s", session)
            pane_id = _tmux("tmux", "display-message", "-p", "-t", session,
                            "#{pane_id}")
        _tmux("tmux", "send-keys", "-t", pane_id, "-l", runner)
        _tmux("tmux", "send-keys", "-t", pane_id, "Enter")
        for _ in range(100):
            try:
                pid = int(pid_file.read_text().strip()); break
            except (OSError, ValueError):
                time.sleep(0.01)
        else:
            raise OSError("held pane did not publish a pid")
        return HeldProcess(pid, pane_id, marker)
    except (OSError, ValueError, subprocess.CalledProcessError):
        return None
def _popen(argv, *, env, cwd, log, mode):
    with open(log, mode) as logf:
        return subprocess.Popen(argv, stdout=logf, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True,
                                cwd=str(cwd), env=env)
def start_or_popen(*args, **kwargs):
    held = start(*args, **kwargs)
    return held if held is not None else _popen(
        args[0], env=kwargs["env"], cwd=kwargs["cwd"], log=kwargs["log"],
        mode=kwargs["mode"])
def _run(spec_path):
    path = Path(spec_path); spec = json.loads(path.read_text())
    with open(spec["log"], spec["mode"]) as logf:
        proc = subprocess.Popen(spec["argv"], cwd=spec["cwd"], env=spec["env"],
            stdin=subprocess.DEVNULL, stdout=logf, stderr=subprocess.STDOUT)
        path.with_name("hold.pid").write_text(str(proc.pid)); rc = proc.wait()
    path.with_name("hold.done").write_text(str(rc)); return rc
