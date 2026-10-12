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
`guard-init.sh --status` lists it) and ONE line in the sending seat's alarm spool
(goal:g7.16.1.11.20.2: every alarm is a signed box message, never the old mail path and
never a pane write). This job only APPENDS, no key: alarm_spool.py's drain, a cron row in
the seat's own uid, signs and box-sends it, exactly once. The seat is a cell in config:crons
(--alarm-seat) and the job must run as agi-<seat> (its spool is in that uid): box refuses
self-mail and mails only adjacent levels, so belam is mailed by sanctuary-master's drain.
Of the two cron rows ONE owns the alarm (memory_alarm_posts); the user@ job passes no
--alarm flags. From any other uid nothing is spooled, one stderr line and one alerts.log
line say so, and nothing falls back.
On the fall back to ok: one CLEARED line + notice -- but only once the reading has stayed
past the CLEAR line (--clear-margin-frac: each warn/crit line moved toward calm) for
--clear-hold-mins without a break, so a reading hovering at the warn line cannot flap. A run that changes nothing writes
nothing (hypothesis:cron-layer-keeps-its-disk-footprint-bounded).
"""
from __future__ import annotations

import argparse
import json
import os
import pwd
import socket
import subprocess
import sys
import time
from pathlib import Path

import alarm_spool
import locations

#: The alarm's state file, a bare NAME inside the sessions room the ONE
#: resolver (`locations.sessions_dir`) names -- never a `<root>/"sessions"`
#: literal here, which a reader could not move with the room.
STATE_FILE = "memory-alarm.state.json"

LEVELS = {"ok": 0, "warn": 1, "crit": 2}

#: the box's memory PSI file: the ONE place it is named (heal's recovery gate reads it here)
BOX_PSI = Path("/proc/pressure/memory")


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
           "box_psi": read_psi(BOX_PSI),
           "cg_psi": {}, "cg_current": None, "cg_max": None}
    if cgroup is not None:
        sig["cg_psi"] = read_psi(cgroup / "memory.pressure")
        sig["cg_current"] = read_int(cgroup / "memory.current")
        sig["cg_max"] = read_int(cgroup / "memory.max")
    return sig


def clear_line(th: argparse.Namespace) -> argparse.Namespace:
    """The thresholds a RAISED alarm is held against: every line moved `clear_margin_frac` (0 < f <= 1)
    toward calm -- PSI and cgroup-fill lines scaled DOWN by f, the MemAvailable lines scaled UP by 1/f -- so a
    reading that raised at the warn line must fall past this one to read ok (f = 1: no band)."""
    f = th.clear_margin_frac
    return argparse.Namespace(**{**vars(th),
                                 "warn_avail_mib": th.warn_avail_mib / f, "crit_avail_mib": th.crit_avail_mib / f,
                                 "warn_psi_some_avg60": th.warn_psi_some_avg60 * f,
                                 "crit_psi_full_avg60": th.crit_psi_full_avg60 * f,
                                 "warn_cgroup_max_frac": th.warn_cgroup_max_frac * f})


def decide(sig: dict, th: argparse.Namespace, prev: str = "ok") -> tuple[str, list[str]]:
    """(level, reasons). Every comparison reads its threshold from `th`; once raised (`prev` != ok) from its clear line."""
    if prev != "ok":
        th = clear_line(th)
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


def transition(state: dict, level: str, now: float, repeat_s: float, hold_s: float = 0.0) -> str | None:
    """'raise' | 'repeat' | 'clear' | None, against the previous state. A clear waits until the
    reading has been ok (past the clear line) for `hold_s` without a break: `state['ok_since']`."""
    prev = state.get("level", "ok")
    if LEVELS[level] > LEVELS.get(prev, 0):
        return "raise"
    if level == "ok":
        if prev == "ok":
            return None
        return "clear" if now - float(state.get("ok_since", now)) >= hold_s else None
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


def _uid_name() -> str:
    """The user name this job runs as (a seam: the rows pin who may write whose notice)."""
    return pwd.getpwuid(os.getuid()).pw_name


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--root", required=True, type=Path, help="the graph root (.agi)")
    ap.add_argument("--warn-avail-mib", type=float, required=True)
    ap.add_argument("--crit-avail-mib", type=float, required=True)
    ap.add_argument("--warn-psi-some-avg60", type=float, required=True)
    ap.add_argument("--crit-psi-full-avg60", type=float, required=True)
    ap.add_argument("--warn-cgroup-max-frac", type=float, required=True)
    ap.add_argument("--repeat-mins", type=float, required=True)
    ap.add_argument("--clear-margin-frac", type=float, required=True,
                    help="a raised alarm clears only below its warn line moved this fraction toward calm "
                         "(PSI / cgroup-fill x f, MemAvailable / f); 1 = no band")
    ap.add_argument("--clear-hold-mins", type=float, required=True,
                    help="...and only after the reading has stayed below that line this long, unbroken; 0 = first tick")
    ap.add_argument("--alarm-seat", default=None,
                    help="the SENDING seat: the alarm is appended to its spool and its drain signs it (the job "
                         "must run as agi-<it>); of the two cron rows ONE owns it (memory_alarm_posts): the "
                         "other passes none, so one alarm is one message")
    ap.add_argument("--alarm-to", default=None, help="the post that reads the alarm (the drain box-sends to it)")
    ap.add_argument("--alarm-job", default=None, help="the job name in the message subject (default: this cron row's name is not known here, so it is required with --alarm-to)")
    ap.add_argument("--alarm-spool-max", type=int, default=None, help="refuse to spool beyond this many lines (required with --alarm-to)")
    ap.add_argument("--alarm-spool", type=Path, default=None, help="default: ~/alarm.spool")
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
    alarm = (a.alarm_seat, a.alarm_to, a.alarm_job, a.alarm_spool_max)
    if any(v is not None for v in alarm) and not all(v is not None for v in alarm):
        ap.error("--alarm-seat --alarm-to --alarm-job --alarm-spool-max go together (or none: the job logs only)")
    if not 0 < a.clear_margin_frac <= 1 or a.clear_hold_mins < 0:
        ap.error("--clear-margin-frac must be in (0, 1] and --clear-hold-mins >= 0")
    state_path = a.state or (locations.sessions_dir(a.root) / STATE_FILE)
    try:
        state = json.loads(state_path.read_text())
    except (OSError, ValueError):
        state = {}
    level, reasons = decide(read_signals(cg if cg.is_dir() else None), a, state.get("level", "ok"))
    now = time.time()
    held = level == "ok" and state.get("level", "ok") != "ok"       # past the clear line, not yet cleared
    if held and "ok_since" not in state:
        state["ok_since"] = now
        if not a.dry_run:
            _write_state(state_path, state)
    elif not held and "ok_since" in state:
        del state["ok_since"]                                         # the reading came back over the line: the hold restarts
        if not a.dry_run:
            _write_state(state_path, state)
    act = transition(state, level, now, a.repeat_mins * 60, a.clear_hold_mins * 60)
    if a.dry_run:
        print(json.dumps({"level": level, "reasons": reasons, "action": act,
                          "prev": state.get("level", "ok")}))
        return 0
    if act is None:
        if state.get("level", "ok") != level and not held:  # e.g. crit -> warn inside the repeat window
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
    kind = "cleared" if act == "clear" else level
    if a.alarm_to:
        me = _uid_name()
        if me != f"agi-{a.alarm_seat}":
            why = (f"uid {me} cannot spool for {a.alarm_seat} (the job must run as agi-{a.alarm_seat}: "
                   f"config:crons `user:`, goal g7.16.1.11.42 C1)")
        else:   # `[memory-alarm-<kind>] ...`: one line per event, kinds apart so a CLEARED never reads as the ALARM
            why = alarm_spool.append(a.alarm_job, a.alarm_to, f"[memory-alarm-{kind}] {ts} {msg}{tail}",
                                     spool=a.alarm_spool, max_lines=a.alarm_spool_max, now=now)
        if why:
            print(f"memory_alarm: alarm to {a.alarm_to} NOT spooled: {why}", file=sys.stderr)
            _append_alert(alerts_log, ts, f"ALARM to {a.alarm_to} NOT spooled: {why}")
    if state.get("level", "ok") != level:
        state["since"] = ts
    state.update(level=level, last_alert=now)
    state.pop("ok_since", None)
    _write_state(state_path, state)
    print(msg)  # reaches the crons log only when an alert fires
    return 0


if __name__ == "__main__":
    sys.exit(main())
