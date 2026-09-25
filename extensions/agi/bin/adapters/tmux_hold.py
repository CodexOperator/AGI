"""Durable named tmux pane hold — the seat's pane outlives the seat process
(`goal:g7.31.1.2`), keyed by a deterministic `seat-<sha1[:12]>` name so a
restart re-enters the SAME pane. Opt-in via `harness["tmux"]`/`["pane"]`.

`hold_or_none` is the whole caller contract and NEVER raises: a pane pid means
the hold happened, None means it did not — for ANY reason — and the caller's
existing `subprocess.Popen` path is then the fallback (`goal:g7.31.1.2.3`).
"""
from __future__ import annotations
import hashlib, shlex, shutil, subprocess  # noqa: E401
from pathlib import Path


def enabled(harness: dict) -> bool:
    """Opt-in: an unconfigured harness keeps the direct Popen path."""
    return bool(harness.get("tmux") or harness.get("pane"))


def pane_name(agent_id: str) -> str:
    """Deterministic seat -> pane window name (target-safe hash)."""
    return "seat-" + hashlib.sha1(str(agent_id).encode()).hexdigest()[:12]


def session(harness: dict) -> str | None:
    """The session name, or None — NEVER raises. An unset name is a fallback
    condition, not an error (`goal:g7.31.1.2.3`)."""
    sess = str(harness.get("tmux_session") or "").strip()
    if not sess:
        try:
            import locations
            root = locations.find_project_root(Path(__file__).resolve().parent)
            cfg = locations.load_config(root) if root else {}
            sess = str((cfg.get("box") or {}).get("tmux_session") or "").strip()
        except Exception:  # noqa: BLE001 -- no config: no box session to name
            sess = ""
    return sess or None


def _run(args):
    """A tmux call. None means the call itself could not be made."""
    try:
        return subprocess.run(args, capture_output=True, text=True)
    except OSError:
        return None


def _ok(cp) -> bool:
    return cp is not None and cp.returncode == 0


def panes(harness: dict) -> list[tuple[str, str, str]]:
    """[(window_name, pane_id, pane_pid)] session-wide. `-s` is load-bearing:
    without it tmux lists only the CURRENT window, so a seat whose window is
    not current is invisible here and gets duplicated."""
    sess = session(harness)
    cp = _run(["tmux", "list-panes", "-s", "-t", sess, "-F",
               "#{window_name} #{pane_id} #{pane_pid}"]) if sess else None
    return [] if not _ok(cp) else [
        tuple(ln.split()) for ln in cp.stdout.splitlines() if len(ln.split()) == 3]


def _pane(harness: dict, name: str):
    hit = next(((i, p) for w, i, p in panes(harness) if w == name), None)
    return (hit[0], int(hit[1])) if hit else None


def _cmd(argv, log_file):
    return list(argv) if not log_file else [
        "sh", "-c", "exec >>" + shlex.quote(str(log_file)) + " 2>&1; exec "
        + " ".join(shlex.quote(a) for a in argv)]


def start(harness: dict, agent_id: str, argv: list[str], *, cwd,
          log_file=None) -> int | None:
    """Enter the seat's pane (founding it if the session has none) and run argv
    in it. `remain-on-exit` is set BEFORE the real argv is respawned: set after,
    it races a fast-failing process and the pane is lost."""
    name, sess = pane_name(agent_id), session(harness)
    if not sess:
        return None
    hit = _pane(harness, name)
    if hit is None:
        args = (["tmux", "new-session", "-d", "-s", sess, "-n", name]
                if not panes(harness)
                else ["tmux", "new-window", "-t", sess, "-n", name])
        if not _ok(_run([*args, "-c", str(cwd)])):
            return None
        hit = _pane(harness, name)
    if hit is None:
        return None
    _run(["tmux", "set-option", "-w", "-t", hit[0], "remain-on-exit", "on"])
    cp = _run(["tmux", "respawn-pane", "-k", "-t", hit[0], "-c", str(cwd),
               "--", *_cmd(argv, log_file)])
    hit = _pane(harness, name)
    return hit[1] if _ok(cp) and hit else None


def hold_or_none(harness: dict, agent_id: str, argv: list[str], *, cwd,
                 log_file=None) -> int | None:
    """THE seam: a pane pid when the seat is held, None when it is not. No
    exception escapes — a failed hold is a fallback, and Popen is not a fault."""
    if not enabled(harness) or not shutil.which("tmux"):
        return None
    try:
        return start(harness, agent_id, argv, cwd=cwd, log_file=log_file)
    except Exception:  # noqa: BLE001 -- see docstring
        return None
