#!/usr/bin/env python3
"""memory_alarm.py -- raise a climb toward memory exhaustion before the box wedges.

OWNER 2026-09-26 04:0xZ (relayed by the sanctuary session, after the 03:20Z
memory livelock and the 03:56Z power cycle): "Set a memory alarm if possible,
so a climb toward exhaustion is raised before the box wedges again (guard's
watch covers cap kills; add whatever pressure / available-memory alarm fits
the engine's alarm system)."

One run = one reading. config:crons declares the cadence (`memory_alarm`,
every minute, on the box it reads) AND every threshold: the values live in
that one declared place, never as a literal here.

Signals, all read from the kernel (never from a process list):
  * MemAvailable                  /proc/meminfo
  * box memory pressure           /proc/pressure/memory (some/full avg60)
  * the user manager's cgroup     memory.pressure, and memory.current against
                                  memory.max. Guard caps user@<uid>; a thrash
                                  inside that cap never shows box-wide.

Levels ok < warn < crit. On a rise, and every --repeat-mins while raised:
one line to the guard's alerts.log (its `TS HOST MESSAGE` shape, so
`guard-init.sh --status` lists it) and one [red] dm per --notify post through
send.py (the seat's mail_alert hook and the 2-min wake surface it). On the
fall back to ok: one CLEARED line + dm. A run that changes nothing writes
nothing (hypothesis:cron-layer-keeps-its-disk-footprint-bounded).
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import locations

#: The alarm's state file, a bare NAME inside the sessions room the ONE
#: resolver (`locations.sessions_dir`) names -- never a `<root>/"sessions"`
#: literal here, which a reader could not move with the room.
STATE_FILE = "memory-alarm.state.json"

LEVELS = {"ok": 0, "warn": 1, "crit": 2}


def read_psi(path: Path) -> dict:
    """{'some': {'avg10': f, 'avg60': f, ...}, 'full': {...}}; {} if unreadable."""
    out: dict = {}
    try:
        for line in path.read_text().splitlines():
            kind, *fields = line.split()
            out[kind] = {k: float(v) for k, v in
                         (f.split("=", 1) for f in fields) if k.startswith("avg")}
    except (OSError, ValueError):
        return {}
    return out


def read_meminfo_mib(key: str, path: Path = Path("/proc/meminfo")) -> float | None:
    try:
        for line in path.read_text().splitlines():
            if line.startswith(key + ":"):
                return int(line.split()[1]) / 1024.0
    except (OSError, ValueError, IndexError):
        pass
    return None


def read_int(path: Path) -> int | None:
    """An integer cgroup file; None for `max` or when unreadable."""
    try:
        raw = path.read_text().strip()
    except OSError:
        return None
    return int(raw) if raw.isdigit() else None


def read_signals(cgroup: Path | None) -> dict:
    sig = {"avail_mib": read_meminfo_mib("MemAvailable"),
           "box_psi": read_psi(Path("/proc/pressure/memory")),
           "cg_psi": {}, "cg_current": None, "cg_max": None}
    if cgroup is not None:
        sig["cg_psi"] = read_psi(cgroup / "memory.pressure")
        sig["cg_current"] = read_int(cgroup / "memory.current")
        sig["cg_max"] = read_int(cgroup / "memory.max")
    return sig


def decide(sig: dict, th: argparse.Namespace) -> tuple[str, list[str]]:
    """(level, reasons). Every comparison reads its threshold from `th`."""
    crit: list[str] = []
    warn: list[str] = []
    avail = sig.get("avail_mib")
    if avail is not None:
        if avail < th.crit_avail_mib:
            crit.append(f"MemAvailable {avail:.0f} MiB < {th.crit_avail_mib:g}")
        elif avail < th.warn_avail_mib:
            warn.append(f"MemAvailable {avail:.0f} MiB < {th.warn_avail_mib:g}")
    for label, psi in (("box", sig.get("box_psi") or {}),
                       ("user@", sig.get("cg_psi") or {})):
        full60 = psi.get("full", {}).get("avg60")
        some60 = psi.get("some", {}).get("avg60")
        if full60 is not None and full60 >= th.crit_psi_full_avg60:
            crit.append(f"{label} PSI full avg60 {full60:.1f}% >= {th.crit_psi_full_avg60:g}")
        elif some60 is not None and some60 >= th.warn_psi_some_avg60:
            warn.append(f"{label} PSI some avg60 {some60:.1f}% >= {th.warn_psi_some_avg60:g}")
    cur, cap = sig.get("cg_current"), sig.get("cg_max")
    if cur is not None and cap:
        frac = cur / cap
        if frac >= th.warn_cgroup_max_frac:
            warn.append(f"user@ at {frac:.0%} of its cap "
                        f"({cur / 1048576:.0f}/{cap / 1048576:.0f} MiB)")
    if crit:
        return "crit", crit + warn
    if warn:
        return "warn", warn
    return "ok", []


def transition(state: dict, level: str, now: float, repeat_s: float) -> str | None:
    """'raise' | 'repeat' | 'clear' | None, against the previous state."""
    prev = state.get("level", "ok")
    if LEVELS[level] > LEVELS.get(prev, 0):
        return "raise"
    if level == "ok":
        return "clear" if prev != "ok" else None
    if now - float(state.get("last_alert", 0)) >= repeat_s:
        return "repeat"
    return None


def _write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, sort_keys=True) + "\n")
    tmp.replace(path)


def _append_alert(log: Path, ts: str, msg: str) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fh:
        fh.write(f"{ts} {socket.gethostname().split('.')[0]} {msg}\n")


def _dm(repo: Path, post: str, body: str) -> None:
    """One [red] dm through the engine's own channel; a failure is printed, never raised."""
    send = Path(__file__).resolve().parent / "send.py"
    try:
        r = subprocess.run([sys.executable, str(send), "send", "--from", "memory-alarm",
                            post, body], cwd=repo, capture_output=True, text=True,
                           timeout=60)
        if r.returncode != 0:
            print(f"memory_alarm: dm to {post} failed (exit {r.returncode}): "
                  f"{(r.stderr or r.stdout).strip()[:200]}")
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"memory_alarm: dm to {post} failed: {exc}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--root", required=True, type=Path, help="the graph root (.agi)")
    ap.add_argument("--warn-avail-mib", type=float, required=True)
    ap.add_argument("--crit-avail-mib", type=float, required=True)
    ap.add_argument("--warn-psi-some-avg60", type=float, required=True)
    ap.add_argument("--crit-psi-full-avg60", type=float, required=True)
    ap.add_argument("--warn-cgroup-max-frac", type=float, required=True)
    ap.add_argument("--repeat-mins", type=float, required=True)
    ap.add_argument("--notify", action="append", default=[],
                    help="a post to dm on each alert; repeatable")
    ap.add_argument("--cgroup", type=Path, default=None,
                    help="default: this uid's user@ service cgroup")
    ap.add_argument("--state", type=Path, default=None,
                    help="default: the sessions resolver + "
                         "memory_alarm.STATE_FILE")
    ap.add_argument("--alerts-log", type=Path, default=None,
                    help="default: the `logs.alerts_file` cell inside the "
                         "box logs dir `crons.enforce_log_caps` bounds")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the reading and the decision; write and send nothing")
    a = ap.parse_args(argv)

    uid = os.getuid()
    # The alert log is resolved through crons, the ONE owner of the capped
    # logs dir: a path derived here is a path the cap may never reach.
    import crons  # noqa: PLC0415 -- after the parser, so a probe never pays for it
    alerts_log = a.alerts_log or crons.alerts_log(a.root)
    cg = a.cgroup or Path(f"/sys/fs/cgroup/user.slice/user-{uid}.slice/user@{uid}.service")
    level, reasons = decide(read_signals(cg if cg.is_dir() else None), a)
    state_path = a.state or (locations.sessions_dir(a.root) / STATE_FILE)
    try:
        state = json.loads(state_path.read_text())
    except (OSError, ValueError):
        state = {}
    now = time.time()
    act = transition(state, level, now, a.repeat_mins * 60)
    if a.dry_run:
        print(json.dumps({"level": level, "reasons": reasons, "action": act,
                          "prev": state.get("level", "ok")}))
        return 0
    if act is None:
        if state.get("level", "ok") != level:  # e.g. crit -> warn inside the repeat window
            state["level"] = level
            _write_state(state_path, state)
        return 0

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    if act == "clear":
        msg = f"CLEARED memory back to ok (was {state.get('level')} since {state.get('since', '?')})"
        tail = ""
    else:
        msg = f"{'ALARM' if level == 'crit' else 'WARN'} memory {level}: " + "; ".join(reasons)
        tail = (" -- hold new dispatches; guard's watchdog reboots at PSI full "
                ">= 40% for 5 min")
    _append_alert(alerts_log, ts, msg)
    for post in a.notify:
        _dm(a.root.parent, post, f"[red] {ts} {msg}{tail}")
    if state.get("level", "ok") != level:
        state["since"] = ts
    state.update(level=level, last_alert=now)
    _write_state(state_path, state)
    print(msg)  # reaches the crons log only when an alert fires
    return 0


if __name__ == "__main__":
    sys.exit(main())
