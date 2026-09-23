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
from pathlib import Path


def enabled(harness: dict) -> bool:
    return bool(harness.get("tmux") or harness.get("pane"))


def pane_name(agent_id: str) -> str:
    """Deterministic seat -> pane window name (hashed target-safe)."""
    return "seat-" + hashlib.sha1(str(agent_id).encode()).hexdigest()[:12]


def _box_session() -> str:
    """The box cell `box.tmux_session` -- the ONE source of the session name.

    `adapters.resolve` normally carries it into `harness["tmux_session"]` and
    dispatch records it in `harness_spec`; this reads the live config so a
    restart of an older record still lands in the box's own session instead of
    a second hardcoded literal (`goal:g7.31.1.2`).
    """
    try:
        import locations
        root = locations.find_project_root(Path(__file__).resolve().parent)
        if root is not None:
            cfg = locations.load_config(root) or {}
            return str((cfg.get("box") or {}).get("tmux_session") or "").strip()
    except Exception:  # noqa: BLE001 -- no config: no box session to name
        pass
    return ""


def _session(harness: dict) -> str:
    sess = str(harness.get("tmux_session") or "").strip() or _box_session()
    if not sess:
        raise RuntimeError(
            "tmux_hold: no session name -- harness carries no `tmux_session` "
            "and the box cell is unreadable (`goal:g7.31.1.2`)")
    return sess


def panes(harness: dict) -> list[tuple[str, str, str]]:
    """[(window_name, pane_id, pane_pid)] across the WHOLE session.

    `-s` is load-bearing: without it tmux lists only the session's CURRENT
    window, so a seat whose window is not current is invisible to
    `start()`/`reattach()` -- which then fabricated a second window of the
    same name (`goal:g7.31.1.2`, parent probe 2).
    """
    cp = subprocess.run(
        ["tmux", "list-panes", "-s", "-t", _session(harness), "-F",
         "#{window_name} #{pane_id} #{pane_pid}"], capture_output=True, text=True)
    return [] if cp.returncode else [
        tuple(ln.split()) for ln in cp.stdout.splitlines() if ln.strip()]
def _pane(harness: dict, name: str) -> tuple[str, int] | None:
    """The seat's (pane_id, pane_pid) session-wide -- an immutable id, not a name."""
    return next(((i, int(p)) for w, i, p in panes(harness) if w == name), None)
def _cmd(argv, log_file):
    if not log_file:
        return list(argv)
    return ["sh", "-c", "exec >>" + shlex.quote(str(log_file)) + " 2>&1; exec "
            + " ".join(shlex.quote(a) for a in argv)]
def _run(args):
    return subprocess.run(args, capture_output=True, text=True)
def start(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None):
    """Create the named pane ONLY if the session has none, then run argv in it."""
    name, sess, have = pane_name(agent_id), _session(harness), panes(harness)
    if any(w == name for w, _, _ in have):
        return reattach(harness, agent_id, argv, cwd=cwd, log_file=log_file)
    args = (["tmux", "new-session", "-d", "-s", sess, "-n", name] if not have
            else ["tmux", "new-window", "-t", sess, "-n", name])
    if _run([*args, "-c", str(cwd), "--", *_cmd(argv, log_file)]).returncode != 0:
        return None
    _run(["tmux", "set-option", "-t", sess, "remain-on-exit", "on"])
    hit = _pane(harness, name)
    return hit[1] if hit else None
def reattach(harness: dict, agent_id: str, argv: list[str], *, cwd, log_file=None,
             created: dict | None = None):
    """Re-enter the SAME pane after death: `respawn-pane -k` on its pane_id.

    If the named pane is genuinely GONE (its window was killed, not just its
    process) it is re-created by `start()` exactly once and `created` is
    stamped -- so a caller can tell a held pane from a fabricated one instead
    of being handed a fresh pane as if it were the original.
    """
    name = pane_name(agent_id)
    hit = _pane(harness, name)
    if hit is None:
        pid = start(harness, agent_id, argv, cwd=cwd, log_file=log_file)
        if created is not None:
            again = _pane(harness, name)
            created.update(created=pid is not None,
                           pane_id=again[0] if again else None)
        return pid
    pane_id = hit[0]
    cp = _run(["tmux", "respawn-pane", "-k", "-t", pane_id,
               "-c", str(cwd), "--", *_cmd(argv, log_file)])
    if created is not None:
        created.update(created=False, pane_id=pane_id)
    hit = _pane(harness, name)
    return hit[1] if cp.returncode == 0 and hit else None
