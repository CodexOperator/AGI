#!/usr/bin/env python3
"""grid_stale.py -- goal:g7.16.1.11.20.4: alarm when the grid stops recording what the trunk changed.

A STALENESS READER, run as a cadence in sanctuary-master's crontab (crons.md `cadences.grid_stale`, `user: agi-sanctuary-master`).
It reads MAIN and writes nothing there: `git show`, `for-each-ref`, `ls-tree`, `log`, `cat-file` only (F8).
  compare PER NODE (S5's second form, no shared anchor): every trunk node blob is looked up in the set of `node.md` blobs held by
          the grid tips (NS/<mint_id>). Only a blob the grid does not hold is read for its mint_id and dated. Older than 2 x the grid_sync cell's every_mins (S1, read from
          the trunk's crons.md at run time, never a literal) = stale. A trunk change after the grid tip's time dates it BY TIME; with
          none after it, by CONTENT: the tip's blob in the path's trunk history = BEHIND (dated from the oldest change after it);
          not in it = AHEAD (grid_sync versions MAIN's disk, which can lead the trunk): counted, never an alarm. A split version on ANOTHER node (10-29: 03:56:30Z after the
          03:25:48Z board change), or a grid_sync run that versions other nodes but not this one, never hides it.
  anchor  the newest grid_sync version: the newest NS commit whose subject starts `cron: ` (crons.py renders
          `grid.py commit --all --prefix 'cron: '`); the alarm id keys on it, and none found is the alarm.
  read    every run prints what it READ (S2 as amended by (Q)): trunk, refs=<count>, the anchor, compared=<trunk nodes read>,
          differ=<nodes the grid does not hold>, ahead=<of those, grid newer than the trunk>, unminted=<nodes with no mint_id line> (differ 0 is the healthy quiet between a grid_sync version and the next board). An
          unresolved trunk (a ladder that cannot derive it included), an unreadable grid_sync cell, 0 node refs, no grid_sync version
          or any exception in the read (named by its class) IS the alarm.
  alarm   ONE line to THIS uid's alarm spool (alarm_spool.py append, `--to` the reader), with a DETERMINISTIC --id over the reading's
          CLASS (stale, or the fault) + the anchor, never the stale set (S3 as amended: a set that grows under one dead grid_sync
          re-alarmed per board; the drain's Alarm-id search makes a repeat a no-op; a new grid_sync version still stale = a new id). The text names a count, the oldest age in minutes and the anchor sha:
          never a path (F5).
  off     crons_live: false or grid_sync enabled: false on the trunk -> one `crons off` / `grid_sync off` line, nothing appended
          (a decided switch is not a fault; both are named LIMITs: a stopped grid is then not alarmed).
  run [--repo R] [--trunk REF] --to POST --max-lines N [--spool S] [--now EPOCH]   rc 0 read (alarm or not) / 1 the append failed
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

JOB = "grid_stale"
NS = "refs/grid/node"
PREFIX = "cron: "
CRONS = ".agi/nodes/.geometry/crons.md"
NODES = ".agi/nodes/"
MINT = re.compile(r'^mint_id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)   # == grid.py MINT_ID_RE, the grid's own reader (pinned by a row)


def git(repo, *a, inp=None):
    return subprocess.run(["git", "-c", "core.quotePath=false", "-C", str(repo), *a], capture_output=True, text=True, input=inp)


def git_ok(repo, *a):
    """git() for a read whose failure must not read as a benign class (alive (G) 09:32:41Z: a lost object made the history read AHEAD,
    the blob read unminted and the tree read fewer nodes, each silent): rc != 0 RAISES, so read_safe names it 'read error <Class>'."""
    r = git(repo, *a)
    if r.returncode:
        raise RuntimeError(f"git {a[0]} unread")
    return r


def rev(repo, ref):
    r = git(repo, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def cells(repo, trunk):
    """(crons_live, grid_sync enabled, grid_sync every_mins) from the TRUNK's crons.md; None for any cell that is not a real value."""
    r = git(repo, "show", f"{trunk}:{CRONS}")
    if r.returncode:
        return None, None, None
    try:
        import yaml  # noqa: PLC0415
        fm = yaml.safe_load(r.stdout.split("---")[1])
        gs = fm["cadences"]["grid_sync"]
        live, on, every = fm.get("crons_live"), gs.get("enabled"), gs.get("every_mins")
    except Exception:  # noqa: BLE001 -- an unreadable cell is a reading, not a crash
        return None, None, None
    ok = lambda v: v if isinstance(v, bool) else None  # noqa: E731
    return ok(live), ok(on), every if isinstance(every, int) and not isinstance(every, bool) and every > 0 else None


def grid_tips(repo):
    """{mint_id: (tip sha, unix time)} and the newest grid_sync version (unix time, sha), from ONE for-each-ref over NS."""
    r = git(repo, "for-each-ref", "--sort=-committerdate", "--format=%(refname) %(objectname) %(committerdate:unix) %(subject)", NS + "/")
    tips, anchor = {}, None
    for ln in r.stdout.splitlines():
        ref, sha, ct, *subj = ln.split(" ", 3)
        tips[ref.rsplit("/", 1)[-1]] = (sha, int(ct))
        if anchor is None and subj and subj[0].startswith(PREFIX):
            anchor = (int(ct), sha)
    return tips, anchor


def batch_check(repo, specs):
    r = git(repo, "cat-file", "--batch-check=%(objectname) %(objecttype)", inp="".join(s + "\n" for s in specs))
    return [ln.split(" ")[0] if ln.endswith(" blob") else None for ln in r.stdout.splitlines()]


def mint_of(repo, blob):
    m = MINT.search(git_ok(repo, "cat-file", "blob", blob).stdout)
    return m.group(1) if m else None


def waiting_since(repo, trunk, path, tip_blob, tip_time):
    """unix time the node has waited since, or None when the grid is AHEAD. The path's first-parent trunk history (newest first, --raw,
    following a rename) gives each change's time and new blob; a failed or empty read RAISES (read_safe: 'read error <Class>').
      no grid ref (tip_blob None)       every change is lacking: dated from the oldest.
      a trunk change after the tip time stale BY TIME, whatever blob the tip holds (alive's B3: an in-flight version never on the
                                        trunk, then a different trunk change, is a real lag).
      none after it: by CONTENT (sp)    the tip's blob in the history = BEHIND, dated from the oldest change after the commit that wrote
                                        it; not in it = AHEAD (grid_sync versions MAIN's disk, which can lead the trunk): None."""
    r = git_ok(repo, "log", "--first-parent", "--follow", "--no-abbrev", "--raw", "--format=C %ct", trunk, "--", f":(top){path}")
    changes, ct = [], None
    for ln in r.stdout.splitlines():
        if ln.startswith("C "):
            ct = int(ln[2:])
        elif ln.startswith(":") and ct is not None:
            changes.append((ct, ln.split("\t", 1)[0].split()[3]))
    if not changes:
        raise RuntimeError("path history empty")                    # a node ls-tree lists on the trunk has >= 1 change: empty = unread
    if tip_blob is None:
        return changes[-1][0]
    after = [c for c, _ in changes if c > tip_time]
    if after:
        return min(after)                                           # B3: stale by time
    for i, (_, new) in enumerate(changes):
        if new == tip_blob:
            return min(c for c, _ in changes[:i]) if i else None    # BEHIND: dated from the oldest change after the tip's blob
    return None                                                     # AHEAD


def read(repo, trunk, now):
    """The reading: a dict with every field the run prints, and `fault` (a short class) or `stale` (a list of (mint, age_min))."""
    t = rev(repo, trunk)
    out = {"trunk": t[:10] if t else "UNRESOLVED", "refs": 0, "anchor": None, "compared": 0, "differ": 0, "ahead": 0, "unminted": 0, "stale": [], "fault": None}
    if t is None:
        out["fault"] = "trunk unresolved"
        return out
    live, on, every = cells(repo, t)
    out["every"] = every
    if live is False:
        out["off"] = "crons off"
        return out
    if on is False:
        out["off"] = "grid_sync off"
        return out
    if live is None or on is None or every is None:
        out["fault"] = "grid_sync cell unread"
        return out
    tips, anchor = grid_tips(repo)
    out["refs"] = len(tips)
    if not tips:
        out["fault"] = "0 grid node refs"
        return out
    if anchor is None:
        out["fault"] = "no grid_sync version"
        return out
    out["anchor"] = anchor
    held = set(batch_check(repo, [f"{sha}:node.md" for sha, _ in tips.values()]))
    nodes = [ln.split(None, 3) for ln in git_ok(repo, "ls-tree", "-r", t, "--", f":(top){NODES}").stdout.splitlines()]
    nodes = [(n[3], n[2]) for n in nodes if len(n) == 4 and n[3].endswith(".md")]
    out["compared"] = len(nodes)
    limit = 2 * every * 60
    for p, b in nodes:
        if b in held:
            continue
        m = mint_of(repo, b)
        if m is None:
            out["unminted"] += 1             # no mint_id line at all: the grid never versions it (counted, never silent)
            continue
        out["differ"] += 1
        tip_blob = batch_check(repo, [f"{tips[m][0]}:node.md"])[0] if m in tips else None
        since = waiting_since(repo, t, p, tip_blob, tips[m][1] if m in tips else 0)
        if since is None:
            out["ahead"] += 1                # the grid holds bytes the trunk never had: not the grid failing to record
            continue
        age = now - since
        if age > limit:
            out["stale"].append((m, age // 60))
    return out


def read_safe(repo, trunk, now):
    """read() whose every failure is a reading (sp (F), 09:12:52Z): a trunk the ladder cannot derive (prereq_notice.default_trunk
    exits) is the `trunk unresolved` fault, and any other exception is a fault naming its CLASS only (never its text: no path)."""
    if trunk is None:
        try:
            trunk = default_trunk()
        except (SystemExit, Exception):  # noqa: BLE001 -- a missing ladder or current_season: the 10-29 silence, read as a fault
            trunk = None
    if trunk is None:
        return {"trunk": "UNRESOLVED", "refs": 0, "anchor": None, "compared": 0, "differ": 0, "ahead": 0, "unminted": 0, "stale": [],
                "fault": "trunk unresolved"}
    try:
        return read(repo, trunk, now)
    except Exception as exc:  # noqa: BLE001
        return {"trunk": "?", "refs": 0, "anchor": None, "compared": 0, "differ": 0, "ahead": 0, "unminted": 0, "stale": [],
                "fault": f"read error {type(exc).__name__}"}


def alarm(r):
    """(id, text) for a reading that alarms, else None. Path-free by construction: only counts, minutes, shas and fixed words."""
    a = r["anchor"]
    asha = a[1][:10] if a else "none"
    if r["fault"]:
        key = f"{r['fault']}|{asha}"
        text = f"[grid stale] the grid could not be read as fresh: {r['fault']} (trunk {r['trunk']}, refs={r['refs']}, newest grid_sync version {asha})"
    elif r["stale"]:
        key = f"stale|{asha}"                # S3 as amended (alive 09:12:02Z): the class + the anchor, never the set
        oldest = max(age for _, age in r["stale"])
        text = (f"[grid stale] {len(r['stale'])} node(s) differ from their grid tip for more than {2 * r['every']} min: oldest {oldest} min;"
                f" newest grid_sync version {asha} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(a[0]))}; trunk {r['trunk']}")
    else:
        return None
    return "gs-" + hashlib.sha1(key.encode()).hexdigest()[:16], text


def run(a):
    now = int(a.now if a.now is not None else time.time())
    r = read_safe(Path(a.repo), a.trunk, now)
    anc = f"{r['anchor'][1][:10]}@{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(r['anchor'][0]))}" if r["anchor"] else "none"
    print(f"grid_stale: trunk={r['trunk']} refs={r['refs']} newest_grid_sync={anc} compared={r['compared']} differ={r['differ']} ahead={r['ahead']} unminted={r['unminted']}"
          f" stale={len(r['stale'])}" + (f" threshold={2 * r['every']}m" if r.get("every") else "") + (f" {r['off']}" if r.get("off") else ""))
    if r.get("off"):
        return 0
    al = alarm(r)
    if al is None:
        return 0
    aid, text = al
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "alarm_spool.py"), "append", "--job", JOB, "--to", a.to,
           "--text", text, "--max-lines", str(a.max_lines), "--id", aid]
    if a.spool:
        cmd += ["--spool", str(a.spool)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    import alarm_spool  # noqa: PLC0415
    import pwd  # noqa: PLC0415
    where, uid = a.spool or alarm_spool.spool_path(), pwd.getpwuid(os.getuid()).pw_name
    if p.returncode:
        print(f"grid_stale: [red] NOT appended to {where} as uid {uid}: {(p.stderr or p.stdout).strip()[:200]}", file=sys.stderr)
        return 1
    print(f"grid_stale: alarm {aid} appended to {where} as uid {uid}, to {a.to}")
    return 0


def default_trunk():
    import prereq_notice  # noqa: PLC0415  (the ONE derivation of the trunk ref from the ladder, never hand-spelled)
    return prereq_notice.default_trunk()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    r = sub.add_parser("run", help="read the grid against the trunk; append ONE alarm line when it is stale or unreadable")
    r.add_argument("--repo", default=".")
    r.add_argument("--trunk", default=None)
    r.add_argument("--to", required=True, help="the reader the seat's drain mails the alarm to")
    r.add_argument("--max-lines", type=int, required=True)
    r.add_argument("--spool", type=Path, default=None)
    r.add_argument("--now", type=int, default=None, help="a fixed unix time (tests)")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
