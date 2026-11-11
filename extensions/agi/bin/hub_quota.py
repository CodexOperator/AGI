#!/usr/bin/env python3
"""hub_quota.py -- a hub's quota cooldown is SAID, never silent (goal:g7.16.1.11.46.35 target (a), the ENGINE half).

20:53Z 11-10 to 06:01Z 11-11 hub A answered every claude-opus-5-5 call with a 429 cooldown and every post on it went dark;
nothing a human or the crew reads said 'quota'. The HOST half (a root timer: the hub's journal and the post routes are
root-only) writes <HUBDIR>/state, the shape agreed DG2 + belam 06:5xZ 11-11:

  written EPOCH                          line 1; older than --max-age = unread, nothing said, rc 1
  HUB MODEL ok|quota|hub-down T LAST     quota: T = the reset from the hub's own reset header, 0 = none given; ok: T = the last 200
  HUB - hub-down T LAST                  the hub-wide down line: T = the first failed upstream dial after the last 200
  LAST = the newest hub log line for that hub (and model), any status (alive 06:50Z, taken 07:1xZ); a body line not in
  this shape = unread, nothing said, rc 1

  say --state FILE --memory FILE [--said FILE] [--spool FILE --to POST] [--now N] [--max-age S]

reads that file and its OWN memory of what it last said (one JSON file, this uid's) and says ONE line per change, per
(hub, model), to --said (the place a human reads with no post's turn running; the host half names it) and to the alarm
spool (job hub-quota) so the first post back reads it in its mail:

  a quota line appears                       `hub A (M) out of quota until HH:MMZ`   (`until unknown` for T 0, never a guess)
  it turns ok, its T after the cooldown      `hub A (M) back HH:MMZ`                 (a recorded 200: a fact, never a prediction)
  still quota, the reset T has passed        `hub A (M) reset HH:MMZ passed, not confirmed: no call since`   (never `back`)
  the hub-wide `-` hub-down line appears    `hub A down (no upstream) since HH:MMZ`  (third child 667abfb390, F9)
  it is gone, a 200 recorded after it        `hub A back HH:MMZ`
  still down, its LAST older than --max-age  `hub A no failed dial since HH:MMZ, not confirmed back`   (sp 06:49Z; never `back`)
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


def read_state(path: Path, now: int, max_age: int) -> dict[tuple[str, str], tuple[str, int, int]] | str:
    """{(hub, model): (state, T, LAST)} from the host file (model `-` = the hub-wide down line), or WHY it cannot be read."""
    try:
        lines = path.read_text().splitlines()
    except OSError as exc:
        return f"{path}: {exc.strerror or exc}"
    head = lines[0].split() if lines else []
    if len(head) != 2 or head[0] != "written" or not head[1].isdigit():
        return f"{path}: no `written EPOCH` line 1"
    if now - int(head[1]) >= max_age:
        return f"{path}: written {now - int(head[1])}s ago (>= {max_age}s)"
    out: dict[tuple[str, str], tuple[str, int, int]] = {}
    for n, ln in enumerate(lines[1:], 2):
        w = ln.split()
        if not w:
            continue
        if (len(w) != 5 or w[2] not in ("ok", "quota", "hub-down") or (w[1] == "-") != (w[2] == "hub-down")
                or not w[3].isdigit() or not w[4].isdigit()):
            return f"{path}: line {n} is not `HUB MODEL STATE T LAST`"
        out[(w[0], w[1])] = (w[2], int(w[3]), int(w[4]))
    return out


def step(state: dict[tuple[str, str], tuple[str, int, int]], mem: dict, now: int, max_age: int = 180) -> list[str]:
    """Advance the memory one run; return the lines to say. mem: {"HUB MODEL": {"since", "reset", "said"}}; model `-` = hub-wide."""
    say: list[str] = []
    for hub in sorted({h for h, _ in state} | {k.split()[0] for k in mem if k.endswith(" -")}):
        key, down = f"{hub} -", state.get((hub, "-"))
        m = mem.get(key)
        if down is not None:
            _, t, last = down
            if m is None:
                mem[key] = {"since": t, "said": "down"}
                say.append(f"hub {hub} down (no upstream) since {hhmm(t)}")
            elif m["said"] == "down" and now - last >= max_age:
                m["said"] = "unconfirmed"
                say.append(f"hub {hub} no failed dial since {hhmm(last)}, not confirmed back")
        elif m is not None:
            oks = [t for (h, md), (st, t, _) in state.items() if h == hub and md != "-" and st == "ok" and t > m["since"]]
            if oks:                                      # the host clears the line only on a 200; `back` names that 200
                del mem[key]
                say.append(f"hub {hub} back {hhmm(min(oks))}")
    for (hub, model), (st, t, _) in sorted(state.items()):
        if model == "-":
            continue
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
    lines = step(state, mem, now, a.max_age)
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
