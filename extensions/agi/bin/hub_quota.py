#!/usr/bin/env python3
"""hub_quota.py -- a hub's quota cooldown is SAID, never silent (goal:g7.16.1.11.46.35 target (a), the ENGINE half).

20:53Z 11-10 to 06:01Z 11-11 hub A answered every claude-opus-5-5 call with a 429 cooldown and every post on it went dark;
nothing a human or the crew reads said 'quota'. The HOST half (a root timer: the hub's journal and the post routes are
root-only) writes <HUBDIR>/state, the shape agreed DG2 + belam 06:5xZ 11-11:

  written EPOCH                     line 1; older than --max-age = unread, nothing said, rc 1
  HUB MODEL ok|quota|hub-down T     quota: T = the reset from the hub's own reset header, 0 = none given; ok: T = the last 200
  HUB - hub-down T                  the hub-wide down line (not said here: target (a) is quota only)

  say --state FILE --memory FILE [--said FILE] [--spool FILE --to POST] [--now N] [--max-age S]

reads that file and its OWN memory of what it last said (one JSON file, this uid's) and says ONE line per change, per
(hub, model), to --said (the place a human reads with no post's turn running; the host half names it) and to the alarm
spool (job hub-quota) so the first post back reads it in its mail:

  a quota line appears                       `hub A (M) out of quota until HH:MMZ`   (`until unknown` for T 0, never a guess)
  it turns ok, its T after the cooldown      `hub A (M) back HH:MMZ`                 (a recorded 200: a fact, never a prediction)
  still quota, the reset T has passed        `hub A (M) reset HH:MMZ passed, not confirmed: no call since`   (never `back`)
  anything else                              nothing

It carries the hub, the model and a time only, and moves no post between hubs (the fallback is the owner's rule, banked).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import alarm_spool  # noqa: E402


def hhmm(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%H:%MZ")


def read_state(path: Path, now: int, max_age: int) -> dict[tuple[str, str], tuple[str, int]] | str:
    """{(hub, model): (state, T)} from the host file, or WHY it cannot be read (then nothing is said)."""
    try:
        lines = path.read_text().splitlines()
    except OSError as exc:
        return f"{path}: {exc.strerror or exc}"
    head = lines[0].split() if lines else []
    if len(head) != 2 or head[0] != "written" or not head[1].isdigit():
        return f"{path}: no `written EPOCH` line 1"
    if now - int(head[1]) >= max_age:
        return f"{path}: written {now - int(head[1])}s ago (>= {max_age}s)"
    out: dict[tuple[str, str], tuple[str, int]] = {}
    for ln in lines[1:]:
        w = ln.split()
        if len(w) == 4 and w[1] != "-" and w[2] in ("ok", "quota", "hub-down") and w[3].isdigit():
            out[(w[0], w[1])] = (w[2], int(w[3]))
    return out


def step(state: dict[tuple[str, str], tuple[str, int]], mem: dict, now: int) -> list[str]:
    """Advance the memory one run; return the lines to say. mem: {"HUB MODEL": {"since", "reset", "said"}}."""
    say: list[str] = []
    for (hub, model), (st, t) in sorted(state.items()):
        key, who = f"{hub} {model}", f"hub {hub} ({model})"
        m = mem.get(key)
        if st == "quota":
            if m is None:
                mem[key] = {"since": now, "reset": t, "said": "cooldown"}
                say.append(f"{who} out of quota until {hhmm(t) if t else 'unknown'}")
                continue
            m["reset"] = t
            if m["said"] == "cooldown" and t and t <= now:
                m["said"] = "passed"
                say.append(f"{who} reset {hhmm(t)} passed, not confirmed: no call since")
        elif st == "ok" and m is not None and t > m["since"]:
            del mem[key]
            say.append(f"{who} back {hhmm(t)}")
    return say


def load_mem(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return {}


def save_mem(path: Path, mem: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}")
    tmp.write_text(json.dumps(mem, sort_keys=True) + "\n")
    os.replace(tmp, path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("say")
    p.add_argument("--state", type=Path, required=True, help="the host-written <HUBDIR>/state")
    p.add_argument("--memory", type=Path, required=True, help="this uid's own memory of what it last said (JSON)")
    p.add_argument("--said", type=Path, default=None, help="the human-read file a line is appended to")
    p.add_argument("--spool", type=Path, default=None, help="the alarm spool (unset = no spool line)")
    p.add_argument("--to", default="sanctuary-master", help="the reader the spool's drain mails it to")
    p.add_argument("--max-lines", type=int, default=500)
    p.add_argument("--max-age", type=int, default=180, help="a state file written longer ago than this is unread")
    p.add_argument("--now", type=int, default=None)
    a = ap.parse_args(argv)
    now = a.now if a.now is not None else int(time.time())
    state = read_state(a.state, now, a.max_age)
    if isinstance(state, str):
        print(f"hub_quota: unread: {state}; nothing said", file=sys.stderr)
        return 1
    try:
        mem = load_mem(a.memory)
    except (OSError, ValueError) as exc:
        print(f"hub_quota: unread: memory {a.memory}: {exc}; nothing said", file=sys.stderr)
        return 1
    lines = step(state, mem, now)
    rc = 0
    stamp = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for line in lines:
        if a.said is not None:
            try:
                with open(a.said, "a") as fh:
                    fh.write(f"{stamp} {line}\n")
            except OSError as exc:
                print(f"hub_quota: said file {a.said} not written: {exc}", file=sys.stderr)
                rc = 1
        if a.spool is not None:
            why = alarm_spool.append("hub-quota", a.to, f"[quota] {line}", spool=a.spool, max_lines=a.max_lines, now=now)
            if why is not None:                          # append returns WHY NOT, never raises
                print(f"hub_quota: spool append FAILED ({why}): {line}", file=sys.stderr)
                rc = 1
        print(line)
    if rc == 0:
        save_mem(a.memory, mem)                          # a line not delivered is said again next run
    return rc


if __name__ == "__main__":
    sys.exit(main())
