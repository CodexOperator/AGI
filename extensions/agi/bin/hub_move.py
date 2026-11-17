#!/usr/bin/env python3
"""hub_move.py -- an automatic hub fallback on a recorded QUOTA limit, and nothing else (goal:g7.16.1.11.46.37, the ENGINE half).

The owner said yes (Q3, 11-15, c:696556deb72a): any post may move to THE OTHER hub (A <-> B) when its own hub records a quota
limit. Not on hub-down alone, not on a symptom, never into a hub that is not ok, one automatic move per post, and LOUD. This is
the DECIDER: it reads the two host-written files (the shape of goal .46.35: line 1 `written EPOCH`, then

  state  `HUB MODEL ok|quota|hub-down T LAST`  and  `HUB - hub-down T LAST`      (read by hub_quota.read_state, the ONE reader)
  route  `POST HUB MODEL`  or  `POST direct`)                                   (a post with NO row is OFF-HUB)

and decides from them, with no token and no account name. It edits no route and no hub: the route file is root-only, so the
APPLYING step is belam's host act, which reads the file this writes (--moves: one `POST HUB MODEL` row per standing move, the
route row the post should have). stall_watch.sh and hub_quota.py `say` still act on nothing; this is a different unit.

  decide --state F --route F --memory F [--said F] [--spool F --to POST] [--moves F] [--post NAME ...] [--hubs A,B] [--now N] [--max-age S]
         MOVE   a post routed to HUB, MODEL, whose (HUB, MODEL) line reads `quota`, while the OTHER hub's (MODEL) line reads `ok`
                (an ok line of ANY age counts: an idle hub records nothing; only the FILE's `written` line must be fresh) and
                that hub has no hub-wide down line, and the post has no standing move. ONE loud line to --said and the spool:
                  post X (M) DECIDED B -> A on quota (B until HH:MMZ), pending the host step; A ok as of MM-DD HH:MMZ, unconfirmed since
                ONE standing line to --said:  post X decided onto hub A at HH:MMZ, moved from B on quota, pending the host step
                (DECIDED, never "on hub A since": the route changes only when the host step applies it; the host writes 'on hub A since')
                ONE line to the moved post's OWN box (a spool line --to X), so a post waking on the new hub knows why.
         REFUSE the target is quota, down, or has no line for the model: NO MOVE, ONE said line per (hub, model, reset) cooldown
                naming the posts held; and a post that already moved and now reads quota on its NEW hub: NO MOVE, ONE said line
                naming the standing move (a move back by another name is the owner's, banked).
         OFF-HUB a post with no route row (or `direct`) is never moved and never unread: `NAME: off-hub, no move`.
         unread a missing, malformed or stale state or route file: nothing moved, nothing said, rc 1.
  clear POST --memory F [--said F] [--moves F]      belam or the owner clears a post's standing move (the only way a post moves again).
         A move BACK is `clear X` THEN the route edit: the host applies each --moves row ONCE and never re-applies it, so a hand edit without `clear` leaves a standing move that stays in memory: the post is never auto-moved again and the old row stays listed.
         A post seen on its `to` hub and later on its `from` hub with the standing move kept: ONE said line (not silence) naming `clear X`.

Memory (this uid's own JSON): {"standing": {POST: {from, to, model, since, reset}}, "refused": {KEY: epoch}}. A line not delivered is
decided and said again next run (memory is saved only after every line went out); the --moves file is rewritten whole from memory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import alarm_spool  # noqa: E402
import hub_quota  # noqa: E402

KEEP = 7 * 86400   # a refusal's memo is dropped after a week


def aid(*parts, kind: str) -> str:
    """A DETERMINISTIC alarm id from the DECISION (post, from, to, model, reset, times cleared), never the wording: a replayed line is one id (goal .46.12)."""
    return f"hm-{kind}-" + hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


def hhmm(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%H:%MZ")


def mmdd(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%m-%d %H:%MZ")


def until(t: int) -> str:
    return hhmm(t) if t else "unknown"


def read_route(path: Path, now: int, max_age: int) -> dict[str, tuple[str, str] | None] | str:
    """{post: (hub, model) | None for `direct`} from the host route file, or WHY it cannot be read."""
    try:
        lines = path.read_text().splitlines()
    except OSError as exc:
        return f"{path}: {exc.strerror or exc}"
    head = lines[0].split() if lines else []
    if len(head) != 2 or head[0] != "written" or not head[1].isdigit():
        return f"{path}: no `written EPOCH` line 1"
    if now - int(head[1]) >= max_age:
        return f"{path}: written {now - int(head[1])}s ago (>= {max_age}s)"
    out: dict[str, tuple[str, str] | None] = {}
    for n, ln in enumerate(lines[1:], 2):
        w = ln.split()
        if not w:
            continue
        if len(w) == 2 and w[1] == "direct":
            out[w[0]] = None
        elif len(w) == 3 and w[1] != "direct":
            out[w[0]] = (w[1], w[2])
        else:
            return f"{path}: line {n} is not `POST HUB MODEL` or `POST direct`"
    return out


def trigger(state: dict, hub: str, model: str):
    """The (hub, model) line when it reads QUOTA: the one thing that may move a post (never hub-down, never a symptom)."""
    st = state.get((hub, model))
    return st if st is not None and st[0] == "quota" else None


def target_state(state: dict, other: str, model: str) -> str:
    """Why the OTHER hub is not a target, or `ok`: down (the hub-wide line), quota until HH:MMZ, no line for MODEL."""
    down = state.get((other, "-"))
    if down is not None:
        return f"down since {hhmm(down[1])}"
    ot = state.get((other, model))
    if ot is None:
        return "has no line for it"
    if ot[0] == "quota":
        return f"out of quota until {until(ot[1])}"
    return "ok"


def decide(state: dict, route: dict, mem: dict, now: int, hubs: list[str]) -> dict:
    """One run. Returns {said: [lines], tell: [(post, line)], report: [lines], moved, refused, offhub: [posts]}; mutates mem."""
    standing = mem.setdefault("standing", {})
    refused = mem.setdefault("refused", {})
    for k in [k for k, t in refused.items() if now - t > KEEP]:
        del refused[k]
    out = {"said": [], "tell": [], "report": [], "moved": 0, "refused": 0, "offhub": []}   # said: (line, also to the spool)
    held: dict[tuple, list[str]] = {}
    for post in sorted(route):
        hm = route[post]
        if hm is None:
            out["offhub"].append(post)
            out["report"].append(f"{post}: off-hub (direct), no move")
            continue
        hub, model = hm
        s = standing.get(post)
        if s is not None and hub == s["to"]:
            s["seen"] = True                         # the route has shown the post on its NEW hub: the host step applied the move
        elif s is not None and s.get("seen") and hub == s["from"]:      # moved back by a route edit WITHOUT `clear`: the host does NOT re-apply it (each row once)
            key = f"standing {post} back {hub}"
            if key not in refused:
                refused[key] = now
                out["refused"] += 1
                out["said"].append((f"post {post} is back on hub {hub} by hand; standing move to {s['to']} kept: the host does NOT re-apply it; "
                                    f"run hub_move.py clear {post} to drop the standing move", True, aid(post, s["from"], s["to"], s["since"], kind="back")))
            continue
        q = trigger(state, hub, model)
        if q is None:
            continue
        if s is not None:
            if hub == s["to"]:                       # moved already, and its NEW hub now reads quota: NO move back
                key = f"standing {post} {hub} {model} {q[1]}"
                if key not in refused:
                    refused[key] = now
                    out["refused"] += 1
                    out["said"].append((f"post {post} stays on hub {hub}: {hub} ({model}) out of quota until {until(q[1])}, but {post} "
                                        f"moved {s['from']} -> {s['to']} at {hhmm(s['since'])} (one automatic move per post): not moved back, "
                                        f"belam or the owner clears it (hub_move.py clear {post})", True, aid(post, hub, s["from"], s["to"], model, q[1], mem.get("cleared", {}).get(post, 0), kind="stay")))
            continue                                 # the same cooldown seen again: no second move, nothing said
        others = [h for h in hubs if h != hub]
        if hub not in hubs or len(others) != 1:
            held.setdefault((hub, model, q[1], f"no other hub is named (hubs {','.join(hubs)})"), []).append(post)
            continue
        other = others[0]
        why = target_state(state, other, model)
        if why != "ok":
            held.setdefault((hub, model, q[1], f"hub {other} ({model}) {why}"), []).append(post)
            continue
        ot = state[(other, model)]
        asof = mmdd(ot[1]) if ot[1] else "unknown"
        standing[post] = {"from": hub, "to": other, "model": model, "since": now, "reset": q[1]}
        loud = (f"post {post} ({model}) DECIDED {hub} -> {other} on quota ({hub} until {until(q[1])}), pending the host step; "
                f"{other} ok as of {asof}, unconfirmed since")
        mine = f"post {post} decided onto hub {other} at {hhmm(now)}, moved from {hub} on quota, pending the host step"
        did = (post, hub, other, model, q[1], mem.get("cleared", {}).get(post, 0))     # the clear count: move, clear, move in ONE window = two ids
        out["said"].append((loud, True, aid(*did, kind="loud")))   # the loud line: the said file AND the alarm spool
        out["said"].append((mine, False, None))          # the standing line: the said file only, once
        out["tell"].append((post, aid(*did, kind="tell"), f"[hub-move] you are decided onto hub {other} ({model}), moved from {hub} on quota (until {until(q[1])}): "
                                  f"{mine}; belam's host step applies the route; the mover never moves you back"))
        out["moved"] += 1
        out["report"].append(loud)
    for (hub, model, reset, why), posts in sorted(held.items()):
        key = f"{hub} {model} {reset} {why}"
        if key in refused:
            continue
        refused[key] = now
        out["refused"] += 1
        out["said"].append((f"hub {hub} ({model}) out of quota until {until(reset)}: no move for {', '.join(posts)}: {why}", True, aid(hub, model, reset, why, *posts, kind="held")))
    return out


def load_mem(path: Path) -> dict:
    return hub_quota.load_mem(path)


def write_moves(path: Path, mem: dict) -> None:
    """The route rows the host should apply, one per standing move, replaced whole (idempotent)."""
    rows = "".join(f"{p} {v['to']} {v['model']}\n" for p, v in sorted(mem.get("standing", {}).items()))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}")
    tmp.write_text(rows)
    os.replace(tmp, path)


def deliver(a, now: int, lines: list[tuple], tell: list[tuple]) -> int:
    rc = 0
    stamp = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for line, to_spool, lid in lines:
        if a.said is not None:
            try:
                with open(a.said, "a") as fh:
                    fh.write(f"{stamp} {line}\n")
            except OSError as exc:
                print(f"hub_move: said file {a.said} not written: {exc}", file=sys.stderr)
                rc = 1
        if a.spool is not None and to_spool:
            why = alarm_spool.append("hub-move", a.to, f"[quota] {line}", spool=a.spool, max_lines=a.max_lines, now=now, alarm_id=lid)
            if why is not None:
                print(f"hub_move: spool append FAILED ({why}): {line}", file=sys.stderr)
                rc = 1
    for post, tid, text in tell:
        if a.spool is not None:
            why = alarm_spool.append("hub-move", post, text, spool=a.spool, max_lines=a.max_lines, now=now, alarm_id=tid)
            if why is not None:
                print(f"hub_move: spool append to {post} FAILED ({why})", file=sys.stderr)
                rc = 1
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("decide")
    p.add_argument("--state", type=Path, required=True, help="the host-written <HUBDIR>/state")
    p.add_argument("--route", type=Path, required=True, help="the host-written <HUBDIR>/route (POST HUB MODEL | POST direct)")
    p.add_argument("--memory", type=Path, required=True, help="this uid's own memory (JSON): the standing moves")
    p.add_argument("--said", type=Path, default=None, help="the human-read file a line is appended to")
    p.add_argument("--spool", type=Path, default=None, help="the alarm spool (unset = no spool line)")
    p.add_argument("--to", default="sanctuary-master", help="the reader the spool's drain mails the loud line to")
    p.add_argument("--moves", type=Path, default=None, help="the route rows the host should apply (rewritten whole)")
    p.add_argument("--post", action="append", default=[], help="a post to name in the report when it has no route row (off-hub)")
    p.add_argument("--hubs", default="A,B", help="the two hubs a post may move between")
    p.add_argument("--max-lines", type=int, default=500)
    p.add_argument("--max-age", type=int, default=180, help="a state or route file written longer ago than this is unread")
    p.add_argument("--now", type=int, default=None)
    c = sub.add_parser("clear", help="drop a standing move (belam or the owner): the move back is the route edit, the host does NOT re-apply a row it applied once")
    c.add_argument("post")
    c.add_argument("--memory", type=Path, required=True)
    c.add_argument("--said", type=Path, default=None)
    c.add_argument("--moves", type=Path, default=None)
    c.add_argument("--now", type=int, default=None)
    a = ap.parse_args(argv)
    now = a.now if a.now is not None else int(time.time())
    if a.cmd == "clear":
        try:
            mem = load_mem(a.memory)
        except (OSError, ValueError) as exc:
            print(f"hub_move: unread: memory {a.memory}: {exc}", file=sys.stderr)
            return 1
        s = mem.get("standing", {}).pop(a.post, None)
        if s is None:
            print(f"hub_move: no standing move for {a.post}", file=sys.stderr)
            return 1
        mem.setdefault("cleared", {})[a.post] = mem.get("cleared", {}).get(a.post, 0) + 1     # joined into the next decision's alarm id
        mem["refused"] = {k: t for k, t in mem.get("refused", {}).items() if not k.startswith(f"standing {a.post} ")}
        line = f"post {a.post} standing move {s['from']} -> {s['to']} cleared"
        a.spool, a.to, a.max_lines = None, "", 0
        rc = deliver(a, now, [(line, False, None)], [])
        if rc == 0:
            hub_quota.save_mem(a.memory, mem)
            if a.moves is not None:
                write_moves(a.moves, mem)
        print(line)
        return rc
    hubs = [h for h in a.hubs.split(",") if h]
    state = hub_quota.read_state(a.state, now, a.max_age)
    if isinstance(state, str):
        print(f"hub_move: unread: {state}; no move", file=sys.stderr)
        return 1
    route = read_route(a.route, now, a.max_age)
    if isinstance(route, str):
        print(f"hub_move: unread: {route}; no move", file=sys.stderr)
        return 1
    try:
        mem = load_mem(a.memory)
    except (OSError, ValueError) as exc:
        print(f"hub_move: unread: memory {a.memory}: {exc}; no move", file=sys.stderr)
        return 1
    res = decide(state, route, mem, now, hubs)
    for name in a.post:
        if name not in route:
            print(f"{name}: off-hub, no move")
            res["offhub"].append(name)
    rc = deliver(a, now, res["said"], res["tell"])
    if rc == 0:
        hub_quota.save_mem(a.memory, mem)                # a line not delivered is decided and said again next run
        if a.moves is not None:
            write_moves(a.moves, mem)
    for line in res["report"]:
        print(line)
    print(f"hub_move: {len(route)} route row(s), {res['moved']} moved, {res['refused']} refused, {len(res['offhub'])} off-hub, "
          f"{len(mem.get('standing', {}))} standing")
    return rc


if __name__ == "__main__":
    sys.exit(main())
