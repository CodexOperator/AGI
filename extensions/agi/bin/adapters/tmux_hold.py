"""Durable named tmux pane hold — adapter seam (`goal:g7.31.1.2`).

One pane per seat; its immutable `#{pane_id}` survives the seat process dying,
so `restart` re-enters the SAME pane instead of fabricating a fresh anonymous
one. Opt-in via `harness["tmux"]`/`harness["pane"]`; unset keeps direct
`Popen`. The window carries the seat name and holds exactly one pane; the
session is the box cell `box.tmux_session`, on the harness or read back from
the live config so an older record still lands in the box's own session.
"""
from __future__ import annotations

import hashlib
import shlex
import subprocess
from pathlib import Path


def enabled(harness: dict) -> bool:
    return bool(harness.get("tmux") or harness.get("pane"))


def pane_name(agent_id: str) -> str:
    """Deterministic seat -> pane window name (hashed target-safe)."""
    return "seat-" + hashlib.sha1(str(agent_id).encode()).hexdigest()[:12]


def _session(harness: dict) -> str:
    sess = str(harness.get("tmux_session") or "").strip()
    if not sess:
        try:
            import locations
            root = locations.find_project_root(Path(__file__).resolve().parent)
            cfg = locations.load_config(root) if root else {}
            sess = str(((cfg or {}).get("box") or {}).get("tmux_session") or "").strip()
        except Exception:  # noqa: BLE001 -- no config: no box session to name
            sess = ""
    if not sess:
        raise RuntimeError("tmux_hold: no session name (`goal:g7.31.1.2`)")
    return sess


def panes(harness: dict) -> list[tuple[str, str, str]]:
    """[(window_name, pane_id, pane_pid)] session-wide. `-s` is load-bearing:
    without it tmux lists only the CURRENT window, so a seat whose window is
    not current is invisible to `spawn`/`reattach` and gets duplicated."""
    cp = subprocess.run(
        ["tmux", "list-panes", "-s", "-t", _session(harness), "-F",
         "#{window_name} #{pane_id} #{pane_pid}"], capture_output=True, text=True)
    return [] if cp.returncode else [
        tuple(ln.split()) for ln in cp.stdout.splitlines() if ln.strip()]


def _pane(harness: dict, name: str) -> tuple[str, int] | None:
    return next(((i, int(p)) for w, i, p in panes(harness) if w == name), None)


def _env_prefix(env):
    """`env -i K=V ...` -- REPLACE the pane environment, never merge into it.

    A `respawn-pane` injects the tmux SERVER's frozen environment, so a
    variable `child_env` adds is missing and one it DROPS (the credential-none
    key `adapters.drop_unneeded_credential` removes) comes back. tmux's own
    `-e` can only add, so a drop would survive it; `env -i` is the shape that
    makes the pane's env exactly `child_env()` (`goal:g7.31.1.2.1`).
    """
    if env is None:
        return []
    return ["env", "-i", *(f"{k}={v}" for k, v in env.items())]


def _cmd(argv, log_file, env=None):
    argv = [*_env_prefix(env), *argv]
    if not log_file:
        return list(argv)
    return ["sh", "-c", "exec >>" + shlex.quote(str(log_file))
            + " 2>&1; exec " + " ".join(shlex.quote(a) for a in argv)]


def _run(args):
    return subprocess.run(args, capture_output=True, text=True)


class HeldProc:
    """A seat process running inside its named pane (`goal:g7.31.1.2.2`).

    Duck-types the bit of `subprocess.Popen` dispatch reads (`pid`, `poll()`,
    `returncode`) so the first-spawn call site does not need a second path.
    Truth is read back from tmux on every call -- never cached -- so a pid
    from a previous respawn is not mistaken for the live one.
    """

    def __init__(self, harness: dict, agent_id: str):
        self._harness = dict(harness)
        self._name = pane_name(agent_id)

    def _row(self):
        return _pane(self._harness, self._name)

    @property
    def pane_id(self):
        row = self._row()
        return row[0] if row else None

    @property
    def pid(self):
        row = self._row()
        return row[1] if row else None

    def poll(self):
        """None while the pane process lives, else its exit status."""
        cp = _run(["tmux", "list-panes", "-s", "-t", _session(self._harness),
                   "-F", "#{window_name}|#{pane_id}|#{pane_pid}|"
                   "#{pane_dead}|#{pane_dead_status}"])
        if cp.returncode:
            return 1
        for ln in cp.stdout.splitlines():
            f = ln.split("|")
            if len(f) >= 4 and f[0] == self._name:
                if f[3] != "1":
                    return None
                return int(f[4]) if len(f) > 4 and f[4].strip() else 1
        return 1

    @property
    def returncode(self):
        return self.poll()


def spawn(harness: dict, agent_id: str, argv: list[str], *, cwd,
          log_file=None, env: dict | None = None) -> "HeldProc | None":
    """Found (or re-enter) the named pane and run argv in it on FIRST spawn.

    `start` when the seat has no pane yet, `reattach` when it has one -- so
    the pane exists before any restart and the same `#{pane_id}` is used for
    the whole seat life. Returns None when no pane could be founded, never a
    fabricated handle.
    """
    have = _pane(harness, pane_name(agent_id))
    pid = (reattach if have else start)(
        harness, agent_id, argv, cwd=cwd, log_file=log_file, env=env)
    return HeldProc(harness, agent_id) if pid is not None else None


def start(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None,
          env: dict | None = None):
    """Create the named pane only if the session has none, then run argv in it.

    The pane is founded with a throwaway shell, `remain-on-exit` set on THAT
    pane, and only then is the real argv respawned in — setting the option
    after the command had run raced a fast-failing process and lost the pane.
    """
    name, sess, have = pane_name(agent_id), _session(harness), panes(harness)
    if any(w == name for w, _, _ in have):
        return reattach(harness, agent_id, argv, cwd=cwd, log_file=log_file,
                        env=env)
    args = (["tmux", "new-session", "-d", "-s", sess, "-n", name] if not have
            else ["tmux", "new-window", "-t", sess, "-n", name])
    if _run([*args, "-c", str(cwd)]).returncode != 0:
        return None
    hit = _pane(harness, name)
    if hit is None:
        return None
    _run(["tmux", "set-option", "-w", "-t", hit[0], "remain-on-exit", "on"])
    cp = _run(["tmux", "respawn-pane", "-k", "-t", hit[0], "-c", str(cwd),
               "--", *_cmd(argv, log_file, env)])
    hit = _pane(harness, name)
    return hit[1] if cp.returncode == 0 and hit else None


def reattach(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None,
             created: dict | None = None, env: dict | None = None):
    """Re-enter the SAME pane after death: `respawn-pane -k` on its `pane_id`.

    A genuinely GONE pane (its window killed, not just its process) is
    re-created by `start()` once and `created` is stamped, so a caller can tell
    a held pane from a fabricated one instead of being handed a fresh pane.
    """
    name, hit = pane_name(agent_id), _pane(harness, pane_name(agent_id))
    if hit is None:
        pid = start(harness, agent_id, argv, cwd=cwd, log_file=log_file, env=env)
        if created is not None:
            again = _pane(harness, name)
            created.update(created=pid is not None,
                           pane_id=again[0] if again else None)
        return pid
    cp = _run(["tmux", "respawn-pane", "-k", "-t", hit[0], "-c", str(cwd),
               "--", *_cmd(argv, log_file, env)])
    if created is not None:
        created.update(created=False, pane_id=hit[0])
    hit = _pane(harness, name)
    return hit[1] if cp.returncode == 0 and hit else None
