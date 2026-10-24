#!/usr/bin/env python3
"""prereq_notice.py -- goal:g7.16.1.11.46.12: tell a claimer, by mail, that its leaf's prerequisites have cleared.

ONE claim source: a goal node's `Assigned to **<post>**` line on the trunk (cards are never one; refs/claims is left alone).
Two events, EDGE-triggered between the last-seen tip (refs/notices/prereq/seen) and the trunk tip:
  a  a claimed, active leaf with no unmet `needs:` is on the trunk for this claimer for the first time (new, or re-assigned to it);
  b  a claimed, active leaf that was held by an unmet `needs:` list now has every id in it terminal (complete | supported | retired).
`run` only COMPUTES and APPENDS: one line per claimer per move to THIS uid's alarm spool (alarm_spool.py append, with a
DETERMINISTIC --id); the alarm_drain row signs and sends it. This file never calls `box`. One marker ref per
(claimer, leaf mint, event[, needs ids]) guards the append; the deterministic id guards the send.
  run   [--repo R] [--trunk REF] [--spool S] [--max-lines N]   rc 0 ok / 1 an append failed (seen NOT advanced: retried) / 3 no seen ref (LOUD, nothing sent)
  seed  --at SHA                                               create the seen ref ONCE (refuses an existing one)
  line  [--repo R]                                             the board segment `notices: claims= cleared= sent= lag= red=...`
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

SEEN = "refs/notices/prereq/seen"
SENT = "refs/notices/prereq/sent"
BUNDLE = "refs/notices/prereq/bundle"
STATUS = "refs/notices/prereq/status"
TERMINAL = {"complete", "supported", "retired"}
ASSIGNED = re.compile(r"^Assigned to \*\*([A-Za-z0-9._-]+)\*\*\.?\s*$", re.M)
LEAF_DIRS = (".agi/nodes/goal", ".agi/nodes/hypothesis")
JOB = "prereq_notice"
LAG_RED_MIN = 60       # the default of the config cell `prereq_notice.notice_lag_red_min` (minutes): the OLDEST unseen trunk commit older than this reads red


def git(repo, *a, check=True, inp=None):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, input=inp)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)[:80]}: {(r.stderr or r.stdout).strip()[:200]}")
    return r


def rev(repo, ref):
    r = git(repo, "rev-parse", "-q", "--verify", ref, check=False)
    return r.stdout.strip() if r.returncode == 0 else None


def parse(text):
    import frontmatter  # noqa: PLC0415
    fm = frontmatter.read_frontmatter(text) or {}
    body = text.split("\n---\n", 1)[1] if text.startswith("---") and "\n---\n" in text else text
    return fm, body


class Tree:
    """Read nodes at one revision: by path, and an id -> status index built lazily from `git grep`."""

    def __init__(self, repo, rv):
        self.repo, self.rv, self._st, self._fm = repo, rv, {}, {}

    def read(self, path):
        if path not in self._fm:
            r = git(self.repo, "show", f"{self.rv}:{path}", check=False)
            self._fm[path] = parse(r.stdout) if r.returncode == 0 else None
        return self._fm[path]

    def status(self, node_id):
        """status of the node with this id, or None when no node carries it (a deprecated copy counts: it is the node)."""
        if node_id not in self._st:
            r = git(self.repo, "grep", "-l", "-E", f"^id: {re.escape(node_id)}$", self.rv, "--", ".agi/nodes", check=False)
            st = None
            for line in r.stdout.splitlines():
                p = line.split(":", 1)[1] if ":" in line else line
                got = self.read(p)
                if got and got[0].get("id") == node_id:
                    st = str(got[0].get("status") or "")
                    if "/deprecated/" in p:
                        st = "retired"
                    break
            self._st[node_id] = st
        return self._st[node_id]

    def leaf(self, path):
        """(claimer, status, mint, type, needs) of a claimable leaf at this revision, or None."""
        got = self.read(path)
        if not got:
            return None
        fm, body = got
        m = ASSIGNED.search(body)
        needs = fm.get("needs") or []
        if not isinstance(needs, list):
            needs = []
        return (m.group(1) if m else None, str(fm.get("status") or ""), str(fm.get("mint_id") or ""),
                str(fm.get("type") or ""), [str(n) for n in needs], str(fm.get("id") or path))

    def ready(self, path):
        """(ready, claimer, mint, id, needs, held) at this revision."""
        lf = self.leaf(path)
        if not lf or "/deprecated/" in path:
            return (False, None, "", "", [], False)
        claimer, status, mint, typ, needs, nid = lf
        if not claimer or status != "active" or typ not in ("goal", "hypothesis"):
            return (False, claimer, mint, nid, needs, False)
        unmet = [n for n in needs if self.status(n) not in TERMINAL]
        return (not unmet, claimer, mint, nid, needs, bool(unmet))


def key(claimer, mint, event, needs):
    return hashlib.sha1("|".join([claimer, mint, event, *sorted(needs)]).encode()).hexdigest()[:16]


def compute(repo, old, new):
    """[(claimer, leaf id, key, event)] newly ready between old and new; and the number of candidates looked at."""
    changed = [p for p in git(repo, "diff", "--name-only", "--no-renames", old, new, "--", *LEAF_DIRS).stdout.splitlines() if p.endswith(".md")]
    to, tn = Tree(repo, old), Tree(repo, new)
    cand = set(changed)
    # a leaf whose `needs:` names a node that changed (any type) may have cleared without being edited itself
    chg_ids = set()
    for p in git(repo, "diff", "--name-only", "--no-renames", old, new, "--", ".agi/nodes").stdout.splitlines():
        if p.endswith(".md"):
            got = tn.read(p) or to.read(p)
            if got and got[0].get("id"):
                chg_ids.add(str(got[0]["id"]))
    for line in git(repo, "grep", "-l", "-E", "^needs:", new, "--", ".agi/nodes/goal", ".agi/nodes/hypothesis", check=False).stdout.splitlines():
        p = line.split(":", 1)[1]
        lf = tn.leaf(p)
        if lf and set(lf[4]) & chg_ids:
            cand.add(p)
    out = []
    for p in sorted(cand):
        rn, claimer, mint, nid, needs, _ = tn.ready(p)
        if not rn:
            continue
        ro, c_old, _, _, needs_old, held_old = to.ready(p)
        if ro and c_old == claimer:
            continue                                    # was already ready for this claimer: no edge
        event = "b" if (held_old and c_old == claimer) else "a"
        extra = needs if event == "b" else [intro(repo, new, p, claimer)]
        out.append((claimer, nid, key(claimer, mint, event, extra), event))
    return out, len(cand)


def intro(repo, new, path, claimer):
    """N5: the trunk commit where the leaf's CURRENT `Assigned to **<claimer>**` line was introduced, so a re-claim (X -> Y -> X) is a NEW key
    and a claim that merely survives later moves is not."""
    r = git(repo, "log", "-1", "--format=%H", f"-SAssigned to **{claimer}**", new, "--", path, check=False)
    return r.stdout.strip() or new


def cell(repo, trunk):
    """the config cell `prereq_notice.notice_lag_red_min` (minutes) on the trunk's .agi/config.json; the default when absent or unusable."""
    r = git(repo, "show", f"{trunk}:.agi/config.json", check=False)
    try:
        v = json.loads(r.stdout)["prereq_notice"]["notice_lag_red_min"]
        return v if isinstance(v, int) and not isinstance(v, bool) and v > 0 else LAG_RED_MIN
    except (ValueError, KeyError, TypeError):
        return LAG_RED_MIN


def bundle_id(claimer, keys):
    return "pn-" + hashlib.sha1((claimer + "|" + "|".join(sorted(keys))).encode()).hexdigest()[:16]


def append_line(here, claimer, text, aid, spool, max_lines):
    cmd = [sys.executable, str(here / "alarm_spool.py"), "append", "--job", JOB, "--to", claimer, "--text", text,
           "--max-lines", str(max_lines), "--id", aid]
    if spool:
        Path(spool).parent.mkdir(parents=True, exist_ok=True)
        cmd += ["--spool", str(spool)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return None if r.returncode == 0 else (r.stderr or r.stdout).strip()[:200]


def dead_count(spool):
    dead = (Path(spool).with_name("alarm.spool.dead") if spool else Path(os.path.expanduser("~")) / "alarm.spool.dead")
    try:
        return sum(1 for ln in dead.read_text().splitlines() if f'"job":"{JOB}"' in ln)
    except OSError:
        return 0


def run(a):
    repo = Path(a.repo)
    here = Path(__file__).resolve().parent
    new = rev(repo, a.trunk)
    old = rev(repo, SEEN)
    if new is None:
        print(f"prereq_notice: [red] trunk {a.trunk} does not resolve: nothing sent", file=sys.stderr)
        return 3
    if old is None:
        print(f"prereq_notice: [red] {SEEN} is MISSING: nothing sent, nothing re-seeded (seed it once with `seed --at <sha>`)", file=sys.stderr)
        return 3
    if old == new:
        _status(repo, a)
        return 0
    found, ncand = compute(repo, old, new)
    by = {}
    for claimer, nid, k, ev in found:
        if rev(repo, f"{SENT}/{claimer}/{k}"):
            continue                                     # already notified for this (claimer, leaf, event)
        by.setdefault(claimer, []).append((nid, k))
    bad = 0
    for claimer, items in sorted(by.items()):
        ids = sorted({i for i, _ in items})
        keys = [k for _, k in items]
        aid = bundle_id(claimer, keys)
        text = f"[landed] {new[:10]}: your leaf prerequisites cleared: {', '.join(ids)}"
        why = append_line(here, claimer, text, aid, a.spool, a.max_lines)
        if why:
            print(f"prereq_notice: [red] append for {claimer} failed ({why}): seen NOT advanced, retried next run", file=sys.stderr)
            bad = 1
            continue
        for k in keys:
            git(repo, "update-ref", f"{SENT}/{claimer}/{k}", new, "")
        git(repo, "update-ref", f"{BUNDLE}/{aid}", new, "", check=False)
        print(f"prereq_notice: {claimer}: {len(ids)} leaf id(s) {aid}")
    if bad:
        _status(repo, a)
        return 1
    git(repo, "update-ref", SEEN, new, old)              # CAS: advance last, so a crash re-runs against the markers
    _status(repo, a)
    return 0


def _status(repo, a):
    try:
        blob = git(repo, "hash-object", "-w", "--stdin", inp=f"dead={dead_count(a.spool)} ts={int(time.time())}\n").stdout.strip()
        git(repo, "update-ref", STATUS, blob)
    except RuntimeError as exc:
        print(f"prereq_notice: status not written: {exc}", file=sys.stderr)


def seed(a):
    repo = Path(a.repo)
    if rev(repo, SEEN):
        print(f"prereq_notice: {SEEN} exists; a seen ref is seeded ONCE", file=sys.stderr)
        return 1
    sha = rev(repo, a.at + "^{commit}")
    if not sha:
        print(f"prereq_notice: {a.at} is not a commit", file=sys.stderr)
        return 1
    git(repo, "update-ref", SEEN, sha, "")
    print(f"prereq_notice: seeded {SEEN} at {sha}")
    return 0


def line(a):
    """`notices: claims=<n> cleared=<k> sent=<j> lag=<n> red=<...>`: read from refs only (the metrics writer runs in another uid)."""
    repo = Path(a.repo)
    trunk, seen = rev(repo, a.trunk), rev(repo, SEEN)
    lim = a.lag_red_min or (cell(repo, trunk) if trunk else LAG_RED_MIN)
    red = []
    tn = Tree(repo, trunk) if trunk else None
    claims = loose = 0
    if tn:
        for ln in git(repo, "grep", "-l", "-E", "^Assigned to ", trunk, "--", ".agi/nodes/goal", ".agi/nodes/hypothesis", check=False).stdout.splitlines():
            p = ln.split(":", 1)[1]
            if "/deprecated/" in p:
                continue
            got = tn.read(p)
            if not got or str(got[0].get("status") or "") != "active":
                continue
            loose += 1
            if ASSIGNED.search(got[1]):
                claims += 1
    cleared = len(git(repo, "for-each-ref", "--format=%(refname)", BUNDLE, check=False).stdout.split())
    ids = set()
    refs = git(repo, "for-each-ref", "--format=%(refname)", "refs/box/sanctuary-master/", check=False).stdout.split()
    if refs:
        for msg in git(repo, "log", f"--grep=Alarm-job: {JOB}", "--format=%B%x00", *refs, check=False).stdout.split("\0"):
            if f"Alarm-job: {JOB}" in msg:
                ids |= {m for m in re.findall(r"^Alarm-id: (\S+)$", msg, re.M)}
    sent = len(ids)
    if not seen:
        red.append("seen-ref-missing")
        lag = -1
    elif not trunk:
        red.append("trunk-missing")                      # N1: a trunk that does not resolve is never "fine"
        lag = -1
    else:
        lag = int(git(repo, "rev-list", "--count", f"{seen}..{trunk}", check=False).stdout.strip() or 0)
        if lag:
            first = git(repo, "rev-list", "--reverse", f"{seen}..{trunk}", check=False).stdout.split()[:1]   # N2: the age of the OLDEST UNSEEN commit, not of the seen one
            age = (time.time() - int(git(repo, "log", "-1", "--format=%ct", first[0], check=False).stdout.strip() or 0)) / 60 if first else 0
            if age > lim:
                red.append(f"lag>{lim}min")
    if loose > claims:
        red.append(f"unparsed={loose - claims}")          # N3: an active leaf carries an `Assigned to` line the strict reader does not take
    unsent = 0
    for ref in git(repo, "for-each-ref", "--format=%(refname)", BUNDLE, check=False).stdout.split():
        ts = git(repo, "log", "-1", "--format=%ct", ref, check=False).stdout.strip()
        if ref.rsplit("/", 1)[-1] not in ids and ts and (time.time() - int(ts)) / 60 > lim:
            unsent += 1
    if unsent:
        red.append(f"unsent={unsent}")                    # N4: a bundle appended long ago whose Alarm-id never reached the outbox
    st = git(repo, "cat-file", "-p", STATUS, check=False).stdout
    m = re.search(r"dead=(\d+)", st)
    if m and int(m.group(1)):
        red.append(f"dead-letter={m.group(1)}")
    return f"notices: claims={claims} cleared={cleared} sent={sent} lag={lag} red={','.join(red) or 'none'}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    for name in ("run", "seed", "line"):
        sp = sub.add_parser(name)
        sp.add_argument("--repo", default=".")
        sp.add_argument("--trunk", default="refs/heads/core/season3/main")
        sp.add_argument("--spool", default=None)
        sp.add_argument("--max-lines", type=int, default=500)
        sp.add_argument("--lag-red-min", type=int, default=None, help="override the config cell prereq_notice.notice_lag_red_min")
        if name == "seed":
            sp.add_argument("--at", required=True)
    a = ap.parse_args(argv)
    if a.verb == "line":
        print(line(a))
        return 0
    try:
        return seed(a) if a.verb == "seed" else run(a)
    except RuntimeError as exc:
        print(f"prereq_notice: [red] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
