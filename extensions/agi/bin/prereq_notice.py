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
  line  [--repo R] [--leaves]                                  the board segment `notices: claims= held= self= cleared= sent= lag= red=...` (a red class names CLAIMERS with counts); --leaves lists the slugs
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
PREFIX = re.compile(r"^Assigned to \*\*([^*\n]+)\*\*", re.M)      # R-1: the prefix, anything after it allowed
PLACEMENT = ("the council", "the directors")                        # placement phrases match WHOLE: held, never notified, never red
CENSUS = "refs/notices/prereq/census"
LEAF_DIRS = (".agi/nodes/goal", ".agi/nodes/hypothesis")
GOAL_DIR = ".agi/nodes/goal"
JOB = "prereq_notice"
LAG_RED_MIN = 60       # the default of the config cell `prereq_notice.notice_lag_red_min` (minutes): the OLDEST unseen trunk commit older than this reads red


def git(repo, *a, check=True, inp=None):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, input=inp)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)[:80]}: {(r.stderr or r.stdout).strip()[:200]}")
    return r


def top(*paths):
    """F-a: a pathspec from the REPO TOP, whatever directory git runs in (the board CLI's root is the .agi dir: a bare `.agi/nodes/goal` resolved there reads `.agi/.agi/nodes/goal` = nothing)."""
    return tuple(":(top)" + p for p in paths)


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

    def __init__(self, repo, rv, mx=None):
        self.repo, self.rv, self.mx, self._st, self._fm = repo, rv, mx, {}, {}

    def read(self, path):
        if path not in self._fm:
            r = git(self.repo, "show", f"{self.rv}:{path}", check=False)
            self._fm[path] = parse(r.stdout) if r.returncode == 0 else None
        return self._fm[path]

    def status(self, node_id):
        """status of the node with this id, or None when no node carries it (a deprecated copy counts: it is the node)."""
        if node_id not in self._st:
            r = git(self.repo, "grep", "--full-name", "-l", "-E", f"^id: {re.escape(node_id)}$", self.rv, "--", *top(".agi/nodes"), check=False)
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
        cl = classify_at(self.mx, self.repo, self.rv, path, body) if self.mx else None
        needs = fm.get("needs") or []
        if not isinstance(needs, list):
            needs = []
        return (cl[1] if cl and cl[0] == "claim" else None, str(fm.get("status") or ""), str(fm.get("mint_id") or ""),
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


class Matrix:
    """box's OWN matrix function `a` (the `box` piece of engine-post.md at this trunk), extracted from the landed bytes and CALLED, never copied:
    `a sanctuary-master NAME` is true iff SM may mail NAME. The posts.md rows are read from the same trunk."""

    def __init__(self, repo, rev_):
        self.repo, self.rev, self.memo = repo, rev_, {}
        txt = git(repo, "show", f"{rev_}:.agi/nodes/.geometry/engine-post.md").stdout
        m = re.search(r"^### box \(.*?\n~~~sh\n(.*?)\n~~~\n", txt, re.S | re.M)
        fns = [ln for ln in (m.group(1).split("\n") if m else []) if ln.startswith("a(){")]
        if len(fns) != 1:
            raise RuntimeError(f"box's matrix function `a` not found exactly once in engine-post.md at {rev_[:10]} ({len(fns)} hits)")
        self.fn = fns[0]
        self.rows = {}
        for ln in git(repo, "show", f"{rev_}:.agi/nodes/.geometry/posts.md").stdout.split("\n"):
            if ln.startswith("  - {"):
                try:
                    row = json.loads(ln[4:])
                    self.rows[row.get("name")] = row
                except ValueError:
                    continue
        self.succ = {}                                   # name -> the live row whose `was` is that name (a RE-USED name's old holder)
        for n, row in self.rows.items():
            if row.get("was") and not n.endswith("-retired"):
                self.succ.setdefault(row["was"], n)

    def renamed_to(self, name):
        """(successor, since) when NAME is a RE-USED name: it has its own live row with a `since` date AND some other live row says `was: NAME`; else None."""
        row, succ = self.rows.get(name), self.succ.get(name)
        if row and row.get("since") and succ and succ != name:
            return succ, str(row["since"])
        return None

    def ok(self, name):
        if name not in self.memo:
            r = subprocess.run(["sh", "-c", self.fn + '\na "$1" "$2"', "x", "sanctuary-master", name], cwd=self.repo,
                               env={**os.environ, "AGI_TRUNK": self.rev}, capture_output=True, text=True)
            self.memo[name] = r.returncode == 0
        return self.memo[name]

    def kind(self, name):
        """held = a posts.md row whose role is council (a placement group, no harness); dead = no posts.md row, a *-retired row or a row with no harness; claim = on SM's matrix; unreachable = a LIVE row that is OFF it."""
        row = self.rows.get(name)
        if row is not None and row.get("role") == "council" and not name.endswith("-retired"):
            return "held"                               # a council row (council, keep) is a PLACEMENT group with no harness: held like `the council`, never dead
        if name.endswith("-retired") or row is None or not row.get("harness"):
            return "dead"
        return "claim" if self.ok(name) else "unreachable"


def classify_at(mx, repo, rv, path, body):
    """classify() plus the LINEAGE class (council 06:40Z): a claim whose `Assigned to **N**` line was written BEFORE N's rename date (N's row `since`) and whose name N has a
    `was:` successor S was written to the post NOW named S: class `renamed`, name `N>S`, red, never a claim and never notified."""
    c = classify(mx, body)
    if c and c[0] == "claim":
        rt = mx.renamed_to(c[1])
        if rt:
            r = git(repo, "log", "-1", "--format=%cs", f"-SAssigned to **{c[1]}", rv, "--", *top(path), check=False)
            born = r.stdout.strip()
            if born and born < rt[1]:
                return ("renamed", f"{c[1]}>{rt[0]}")
    return c


def classify(mx, body):
    """(class, name) of a node's Assigned-to line, or None when it has none. claim | held | self | dead | unreachable | unparsed."""
    m = PREFIX.search(body)
    if not m:
        return ("unparsed", "") if re.search(r"^Assigned to ", body, re.M) else None
    raw = " ".join(m.group(1).split())
    if raw.lower().startswith(PLACEMENT):
        return ("held", raw)
    name = re.split(r"[ (]", raw, maxsplit=1)[0]
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        return ("unparsed", raw)
    if name == "sanctuary-master":
        return ("self", name)
    return (mx.kind(name), name)


def classify_path(repo, rev_, path, mx):
    if "/deprecated/" in path:
        return None
    got = Tree(repo, rev_, mx).read(path)
    if not got or str(got[0].get("status") or "") != "active":
        return None
    return classify_at(mx, repo, rev_, path, got[1])


GEOMETRY = (".agi/nodes/.geometry/posts.md", ".agi/nodes/.geometry/engine-post.md")


def claimer_key(who):
    """the bracket key of a red row: the claimer's name; a raw `Assigned to` text that names nobody (unparsed) is cut to the characters a bracket can carry."""
    return re.sub(r"[^A-Za-z0-9._>-]+", "_", (who or "").strip()).strip("_")[:40] or "unparsed"


def by_claimer(items):
    """`claimer:count,claimer:count` for [(claimer, slug)]: the counts SUM to len(items) by construction (every row lands in exactly one key), largest first."""
    c = {}
    for who, _ in items:
        c[who] = c.get(who, 0) + 1
    return ",".join(f"{w}:{n}" for w, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def leaves(a):
    """`line --leaves`: one `<class> <claimer> <slug>` line per red leaf the board bracket counts (dead | unreachable | unparsed), so the board names claimers and the slugs are here."""
    repo = Path(a.repo)
    trunk = rev(repo, a.trunk)
    if not trunk:
        return [f"prereq_notice: [red] trunk {a.trunk} does not resolve"]
    cen = census_catchup(repo, load_census(repo), trunk, Matrix(repo, trunk))
    rows = sorted((cls, claimer_key(who), p.rsplit("/", 1)[-1][:-3]) for p, (cls, who) in cen["rows"].items() if cls in ("renamed", "dead", "unreachable", "unparsed"))
    return [" ".join(r) for r in rows]


def census_full(repo, rev_, mx):
    rows = {}
    for ln in git(repo, "grep", "--full-name", "-l", "-E", "^Assigned to ", rev_, "--", *top(*LEAF_DIRS), check=False).stdout.splitlines():
        p = ln.split(":", 1)[1]
        c = classify_path(repo, rev_, p, mx)
        if c:
            rows[p] = list(c)
    return {"commit": rev_, "rows": rows}


def census_catchup(repo, cen, rev_, mx):
    """R-3: reclassify only the goal files changed since the census commit (one full pass when posts.md or the box piece changed)."""
    old = (cen or {}).get("commit")
    if not old:
        return census_full(repo, rev_, mx)
    if old == rev_:
        return cen
    r = git(repo, "diff", "--name-only", "--no-renames", old, rev_, "--", *top(*LEAF_DIRS, *GEOMETRY), check=False)
    if r.returncode:
        return census_full(repo, rev_, mx)
    names = r.stdout.split()
    if any(n in GEOMETRY for n in names):
        return census_full(repo, rev_, mx)
    rows = dict(cen["rows"])
    for p in names:
        rows.pop(p, None)
        c = classify_path(repo, rev_, p, mx) if p.endswith(".md") else None
        if c:
            rows[p] = list(c)
    return {"commit": rev_, "rows": rows}


def load_census(repo):
    r = git(repo, "cat-file", "-p", CENSUS, check=False)
    try:
        c = json.loads(r.stdout) if r.returncode == 0 else None
        return c if isinstance(c, dict) and "rows" in c and "commit" in c else None
    except ValueError:
        return None


def save_census(repo, cen):
    blob = git(repo, "hash-object", "-w", "--stdin", inp=json.dumps(cen, sort_keys=True)).stdout.strip()
    git(repo, "update-ref", CENSUS, blob)


def refresh_census(repo, rev_, mx):
    cen = census_catchup(repo, load_census(repo), rev_, mx)
    save_census(repo, cen)
    return cen


def key(claimer, mint, event, needs):
    return hashlib.sha1("|".join([claimer, mint, event, *sorted(needs)]).encode()).hexdigest()[:16]


def compute(repo, old, new):
    """[(claimer, leaf id, key, event)] newly ready between old and new; and the number of candidates looked at."""
    changed = [p for p in git(repo, "diff", "--name-only", "--no-renames", old, new, "--", *top(*LEAF_DIRS)).stdout.splitlines() if p.endswith(".md")]
    mx = Matrix(repo, new)
    to, tn = Tree(repo, old, mx), Tree(repo, new, mx)
    cand = set(changed)
    # a leaf whose `needs:` names a node that changed (any type) may have cleared without being edited itself
    chg_ids = set()
    for p in git(repo, "diff", "--name-only", "--no-renames", old, new, "--", *top(".agi/nodes")).stdout.splitlines():
        if p.endswith(".md"):
            got = tn.read(p) or to.read(p)
            if got and got[0].get("id"):
                chg_ids.add(str(got[0]["id"]))
    for line in git(repo, "grep", "--full-name", "-l", "-E", "^needs:", new, "--", *top(*LEAF_DIRS), check=False).stdout.splitlines():
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
    r = git(repo, "log", "-1", "--format=%H", f"-SAssigned to **{claimer}", new, "--", *top(path), check=False)
    return r.stdout.strip() or new


def cron_state(repo, trunk):
    """`on` | `off` | `unread`: the cron cell `cadences.prereq_notice.enabled` in the trunk's crons.md (council 08:02Z, notices OFF). Anything but a real YAML bool is `unread`, never `off`."""
    r = git(repo, "show", f"{trunk}:.agi/nodes/.geometry/crons.md", check=False)
    if r.returncode:
        return "unread"
    try:
        import yaml  # noqa: PLC0415
        v = yaml.safe_load(r.stdout.split("---")[1])["cadences"][JOB]["enabled"]
    except Exception:  # noqa: BLE001 -- an unreadable cell is a state, not a crash
        return "unread"
    return "on" if v is True else "off" if v is False else "unread"


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
    refresh_census(repo, new, Matrix(repo, new))        # R-3: one classified census of the active Assigned-to leaves, caught up per run
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
    try:
        refresh_census(repo, sha, Matrix(repo, sha))
    except RuntimeError as exc:
        print(f"prereq_notice: census not built at seed ({exc}); the first run builds it", file=sys.stderr)
    return 0


def line(a):
    """`notices: claims=<n> cleared=<k> sent=<j> lag=<n> red=<...>`: read from refs only (the metrics writer runs in another uid)."""
    repo = Path(a.repo)
    trunk, seen = rev(repo, a.trunk), rev(repo, SEEN)
    lim = a.lag_red_min or (cell(repo, trunk) if trunk else LAG_RED_MIN)
    red = []
    state = cron_state(repo, trunk) if trunk else "on"     # no trunk: its own named red; the cell cannot be read
    if state == "unread":
        red.append("cell-unread")
    cnt, files = {}, {}
    if trunk:
        mx = Matrix(repo, trunk)
        cen = census_catchup(repo, load_census(repo), trunk, mx)     # read-only here (another uid): the run persists it
        for p, (cls, who) in cen["rows"].items():
            cnt[cls] = cnt.get(cls, 0) + 1
            files.setdefault(cls, []).append((claimer_key(who), p.rsplit("/", 1)[-1][:-3]))
    claims = cnt.get("claim", 0)
    cleared = len(git(repo, "for-each-ref", "--format=%(refname)", BUNDLE, check=False).stdout.split())
    ids = set()
    refs = git(repo, "for-each-ref", "--format=%(refname)", "refs/box/sanctuary-master/", check=False).stdout.split()
    if refs:
        for msg in git(repo, "log", f"--grep=Alarm-job: {JOB}", "--format=%B%x00", *refs, check=False).stdout.split("\0"):
            if f"Alarm-job: {JOB}" in msg:
                ids |= {m for m in re.findall(r"^Alarm-id: (\S+)$", msg, re.M)}
    sent = len(ids)
    if not seen:
        red.append("seen-unresolved")                    # F-f: each ref is its own check, whatever the other says (a clone has neither refs/notices/* nor the trunk branch)
    if not trunk:
        red.append("trunk-unresolved")                   # N1: a trunk that does not resolve is never "fine"
    if not seen or not trunk:
        lag = -1
    else:
        lag = int(git(repo, "rev-list", "--count", f"{seen}..{trunk}", check=False).stdout.strip() or 0)
        if lag:
            first = git(repo, "rev-list", "--reverse", f"{seen}..{trunk}", check=False).stdout.split()[:1]   # N2: the age of the OLDEST UNSEEN commit, not of the seen one
            age = (time.time() - int(git(repo, "log", "-1", "--format=%ct", first[0], check=False).stdout.strip() or 0)) / 60 if first else 0
            if age > lim and state != "off":    # OFF suppresses ONLY the lag red: the owner alone can clear it (enabled: false); lag is still PRINTED
                red.append(f"lag>{lim}min")
    if trunk:
        # F-b: a reader that read NOTHING is red. These probes run FROM the repo top on the goal tree as a tree-ish (`<trunk>:.agi/nodes/goal`): no cwd and no pathspec magic can shift them
        tree, tl = f"{trunk}:{GOAL_DIR}", git(repo, "rev-parse", "--show-toplevel", check=False).stdout.strip() or repo
        if not git(tl, "ls-tree", "-r", "--name-only", tree, check=False).stdout.split():
            red.append("no-goal-files-read")
        elif not sum(cnt.values()) and git(tl, "grep", "-l", "--all-match", "-e", "^Assigned to ", "-e", "^status: active$", tree, check=False).stdout.strip():
            red.append("no-claims-read")                 # the census classified nothing while an ACTIVE goal file carries `Assigned to `
    for kind in ("renamed", "dead", "unreachable", "unparsed"):    # R-2: each red names its files (dead: re-assign or retire; unreachable: a ROUTING question; unparsed: no rule takes the line)
        if cnt.get(kind):
            red.append(f"{kind}={cnt[kind]}[{by_claimer(files[kind])}]")
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
    head = {"off": "notices: OFF (prereq_notice enabled: false; owner GO banked, card-belam sec6) ",
            "unread": "notices: cell unread (crons.md cadences.prereq_notice.enabled is not a readable bool) "}.get(state, "notices: ")
    return (f"{head}claims={claims} held={cnt.get('held', 0)} self={cnt.get('self', 0)} cleared={cleared} sent={sent} lag={lag} "
            f"red={','.join(red) or 'none'}")


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
        if name == "line":
            sp.add_argument("--leaves", action="store_true", help="list every renamed|dead|unreachable|unparsed leaf: <class> <claimer> <slug>")
    a = ap.parse_args(argv)
    if a.verb == "line":
        try:
            if a.leaves:
                print("\n".join(leaves(a)))
                return 0
            print(line(a))
        except (RuntimeError, OSError) as exc:
            print(f"notices: UNMEASURED(source failed: {type(exc).__name__})")
        return 0
    try:
        return seed(a) if a.verb == "seed" else run(a)
    except RuntimeError as exc:
        print(f"prereq_notice: [red] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
