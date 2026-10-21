#!/usr/bin/env python3
"""season_report.py -- the FACTS half of the end-of-season report (goal:g5.4.1, council design 10-15).

    season_report.py [--repo DIR] facts --season N --at SHA --heads-file F [--box-facts F2]

Prints ONE sorted JSON object on stdout and nothing else. It WRITES NOTHING (no ref, no file, no index) and
NEVER reads the clock: every time in the output is a git committer time or a value from a named input file, so two runs over the
same inputs are byte-equal.

Every source is read AT SHA (the report's commit, not the working tree):
  counts      `git ls-tree -r SHA .agi/nodes`: active_by_dir (md files outside deprecated/), active_by_status (the
              same set minus `status: deprecated`), BOTH mismatch lists (a live-dir file marked deprecated; a deprecated/ file
              not marked), engine_active (metrics.py's rule: every node .md minus the `status: deprecated` ones), by_type
              (the frontmatter `type:`). Every id is the frontmatter `id:`; the path spells it only as a flagged fallback
  posts       config:posts, every named row and its trunk cell (engine.trunk)
  season      the ladder's current_season and each town's season_history row for season N (the open time)
  close       the committer time of the ladder-cell commit that OPENED season N (labelled so; `signed` only when git verifies it)
  ledger      the commits of season N-1 = [open(N-1), open(N)): the window ends at the close, never at --at (so a later --at
              leaves it byte-equal); signature-header counts per author; `names` = the L<n> of the first-parent LAND merges
  goals       goal counts by season:status, and how many `active` goals carry over from season N-1
Heads and archives come from ONE captured ls-remote file whose FIRST line is the read time (ISO-8601 UTC) and the rest
`<sha><TAB><ref>`. Facts with no git source come ONLY from a named --box-facts file (JSON): each value carries its
command, reader uid and read time; with no file, or with a key missing, the cell is {"value": "not recorded"}.
rc 2 + a message on stderr on any input that is malformed; nothing is guessed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter

NODES = ".agi/nodes"
POSTS_PATH = f"{NODES}/.geometry/posts.md"
LADDER_PATH = f"{NODES}/.geometry/ladder.md"
TOP_K = 9                         # the type rows a page draws; every other type folds into ONE "other" row
BOX_KEYS = ("run_rc", "run_time", "complete_time", "posts_live", "pin", "freeze_window", "restarts")
BOX_FIELDS = ("value", "command", "reader_uid", "read_time")
NOT_RECORDED = "not recorded"
_TIME = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
_HEADLINE = re.compile(r"^[0-9a-f]{40}\t\S+$")
# the land shapes, each cited from a real first-parent merge subject of season 2 (names come from these and from NOTHING else):
_LAND = re.compile(r"^[A-Za-z0-9_.-]+: LAND stack (\d+)\b")                       # 'sanctuary-master: LAND stack 16 (gate tip efbe2cf03e) -- ...'
_LFORM = re.compile(r"^[A-Za-z0-9_.-]+: merge (?:season-\d+ )?L(\d+)\b")        # 'belam: merge season-2 L21 (8a12fdc239) into ...' / 'belam: merge L22 db1ac1324d (...'


class Fail(Exception):
    """A refused input: printed as one line, rc 2."""


def _git(repo: str, *args: str, inp: bytes | None = None) -> bytes:
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    r = subprocess.run(["git", "-C", repo, *args], input=inp, capture_output=True, env=env)
    if r.returncode != 0:
        raise Fail(f"git {' '.join(args[:3])}: {r.stderr.decode(errors='replace').strip()[:200]}")
    return r.stdout


def _iso(ts: int) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def _frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end > 0 else ""


def _fm_scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:[ \t]*['\"]?([^'\"\n#]*?)['\"]?[ \t]*$", fm, re.M)
    return m.group(1) if m else None


def _blobs(repo: str, oids: list[str]) -> list[bytes]:
    """The blob bodies, in the order asked: ONE `cat-file --batch` pass."""
    if not oids:
        return []
    out = _git(repo, "cat-file", "--batch", inp=("\n".join(oids) + "\n").encode())
    bodies, i = [], 0
    for _ in oids:
        nl = out.index(b"\n", i)
        head = out[i:nl].split()
        if len(head) != 3 or head[1] != b"blob":
            raise Fail(f"cat-file --batch: unexpected header {out[i:nl]!r}")
        size = int(head[2])
        bodies.append(out[nl + 1:nl + 1 + size])
        i = nl + 1 + size + 1
    return bodies


def read_tree(repo: str, sha: str) -> dict:
    """Counts, by_type, BOTH status/dir mismatch lists and the goals, from ONE ls-tree pass at SHA. Ids and types come from the frontmatter."""
    raw = _git(repo, "ls-tree", "-r", "-z", sha, "--", NODES).decode()
    files: list[tuple[bool, str, str, str]] = []   # (in deprecated/, type dir, stem, oid)
    for ent in raw.split("\0"):
        if not ent:
            continue
        meta, path = ent.split("\t", 1)
        if not path.endswith(".md"):
            continue
        parts = path.split("/")
        dep = parts[2] == "deprecated"
        files.append((dep, parts[3] if dep else parts[2], "/".join(parts[4:] if dep else parts[3:])[:-3], meta.split()[2]))
    bodies = _blobs(repo, [f[3] for f in files])
    mismatch, dep_mismatch, from_path, by_type, goals = [], [], [], Counter(), []
    live = deprecated = status_active = status_deprecated = 0
    for (dep, tdir, stem, _), body in zip(files, bodies):
        fm = _frontmatter(body.decode("utf-8", "replace"))
        status = _fm_scalar(fm, "status")
        nid = _fm_scalar(fm, "id")
        if not nid:
            nid = f"{tdir}:{stem}"                  # the path spells the id only when the frontmatter does not: flagged
            from_path.append(nid)
        typ = _fm_scalar(fm, "type") or (nid.split(":", 1)[0] if ":" in nid else tdir)
        if status == "deprecated":
            status_deprecated += 1
        if dep:
            deprecated += 1
            if status != "deprecated":
                dep_mismatch.append(nid)
            continue
        live += 1
        by_type[typ] += 1
        if status == "deprecated":
            mismatch.append(nid)
        else:
            status_active += 1
        if typ == "goal":
            goals.append((nid, status, _fm_scalar(fm, "season")))
    rows = sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0]))
    type_rows = [{"type": t, "label": t, "nodes": n} for t, n in rows[:TOP_K]]
    rest = rows[TOP_K:]
    if rest:
        type_rows.append({"type": "other", "label": f"other ({len(rest)} types)", "types": len(rest), "nodes": sum(n for _, n in rest)})
    widest = max((r["nodes"] for r in type_rows), default=1) or 1
    for r in type_rows:
        r["pct"] = f"{100 * r['nodes'] / widest:.1f}"            # the bar width, relative to the widest row
    return {
        "active_by_dir": live,
        "active_by_status": status_active,
        "deprecated_by_dir": deprecated,
        "engine_active": len(files) - status_deprecated,         # metrics.py's rule: every node .md minus the status-deprecated ones
        "status_dir_mismatch": sorted(mismatch),
        "deprecated_status_mismatch": sorted(dep_mismatch),
        "ids_from_path": sorted(from_path),
        "by_type": {t: n for t, n in rows},
        "type_rows": type_rows,
        "_goals": goals,
    }


def goal_counts(goals: list[tuple[str, str | None, str | None]], season: int) -> dict:
    """Goals by season:status (a COUNT: the graph holds hundreds of carried goals, a list of them is not a fact a page can draw)."""
    c = Counter(f"{s or '?'}:{st or '?'}" for _, st, s in goals)
    carried = sum(1 for _, st, s in goals if st == "active" and s == str(season - 1))
    return {"by_season_status": dict(sorted(c.items())), "carried_active": carried, "total": len(goals)}


def read_posts(repo: str, sha: str) -> dict:
    text = _git(repo, "show", f"{sha}:{POSTS_PATH}").decode("utf-8", "replace")
    fm = _frontmatter(text)
    posts = []
    for line in fm.splitlines():
        if not line.startswith("  - {"):
            continue
        try:
            row = json.loads(line.strip()[2:])
        except ValueError as e:
            raise Fail(f"config:posts: a row is not JSON ({e})")
        if not row.get("name"):
            continue
        trunk = (row.get("engine") or {}).get("trunk") or row.get("trunk")
        posts.append({"name": row["name"], "trunk": trunk or None})
    posts.sort(key=lambda p: p["name"])
    trunks = Counter(p["trunk"] for p in posts if p["trunk"])
    return {"posts": posts, "posts_named": len(posts), "trunk_cells": sum(trunks.values()),
            "trunks": dict(sorted(trunks.items()))}


def _history(fm: str) -> list[dict]:
    rows, on = [], False
    for line in fm.splitlines():
        if line.startswith("season_history:"):
            on = True
            continue
        if on:
            if not line.startswith("  - "):
                break
            try:
                rows.append(json.loads(line.strip()[2:]))
            except ValueError as e:
                raise Fail(f"season_history: a row is not JSON ({e})")
    return rows


def read_cells(repo: str, sha: str, season: int) -> dict:
    ladder = _fm_scalar(_frontmatter(_git(repo, "show", f"{sha}:{LADDER_PATH}").decode("utf-8", "replace")), "current_season")
    towns = {}
    for ent in _git(repo, "ls-tree", "--name-only", sha, f"{NODES}/town/").decode().split("\n"):
        if not ent.endswith(".md"):
            continue
        fm = _frontmatter(_git(repo, "show", f"{sha}:{ent}").decode("utf-8", "replace"))
        slug = ent.rsplit("/", 1)[1][:-3]
        hist = [h for h in _history(fm) if h.get("season") == season]
        towns[slug] = {"season": _fm_scalar(fm, "season"),
                       "opened": hist[0].get("opened") if hist else None,
                       "closed": hist[0].get("closed") if hist else None}
    opened = (towns.get("core") or {}).get("opened") or min((t["opened"] for t in towns.values() if t["opened"]), default=None)
    return {"ladder_current_season": ladder, "towns": dict(sorted(towns.items())), "opened": opened,
            "town_count": len(towns), "town_names": ", ".join(sorted(towns))}


def _commit(repo: str, sha: str) -> dict:
    raw = _git(repo, "cat-file", "commit", sha).decode("utf-8", "replace")
    return _parse_commit(raw)


def _parse_commit(raw: str) -> dict:
    head, _, msg = raw.partition("\n\n")
    out = {"signed": "\ngpgsig " in "\n" + head, "subject": msg.split("\n", 1)[0], "author": "", "ts": 0}
    for line in head.split("\n"):
        if line.startswith("author "):
            out["author"] = line[7:].split(" <", 1)[0]
        elif line.startswith("committer "):
            out["ts"] = int(line.rsplit(" ", 2)[-2])
    return out


def open_commit(repo: str, sha: str, season: int) -> dict | None:
    """The first commit (oldest first) on SHA's history whose ladder cell reads current_season == SEASON and whose first parent's does not."""
    cands = _git(repo, "log", "--reverse", "--format=%H", f"-Scurrent_season: {season}", sha, "--", LADDER_PATH).decode().split()
    for c in cands:
        def cur(rev: str) -> str | None:
            r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{LADDER_PATH}"], capture_output=True)
            return _fm_scalar(_frontmatter(r.stdout.decode("utf-8", "replace")), "current_season") if r.returncode == 0 else None
        if cur(c) == str(season) and cur(f"{c}^") != str(season):
            info = _commit(repo, c)
            return {"sha": c, **info}
    return None


def _parent(repo: str, rev: str) -> str | None:
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "-q", f"{rev}^"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def read_close(repo: str, sha: str, season: int) -> dict:
    c = open_commit(repo, sha, season)
    if c is None:
        return {"value": NOT_RECORDED}
    verified = _git(repo, "log", "-1", "--format=%G?", c["sha"]).decode().strip() == "G"      # a gpgsig HEADER proves nothing: git verifies it
    kind = "signed" if verified else "UNVERIFIED"
    return {"value": _iso(c["ts"]), "sha": c["sha"], "signed": verified,
            "label": f"season {season - 1} closed: committer time of the {kind} ladder-cell commit that opened season {season}"}


def land_names(repo: str, rng: list[str]) -> list[str]:
    """The L<n> of the first-parent merges whose subject is a land shape; prose that mentions an L<n> never counts."""
    subjects = _git(repo, "log", "--first-parent", "--merges", "-z", "--format=%s", *rng).decode("utf-8", "replace").split("\0")
    nums = {int(m.group(1)) for s in subjects for m in (_LAND.match(s) or _LFORM.match(s),) if m}
    return [f"L{n}" for n in sorted(nums)]


def read_ledger(repo: str, sha: str, season: int) -> dict:
    """Season N-1's own commits: the window [open(N-1), open(N)). --at only names the tree the other sources are read at."""
    prev, cur = open_commit(repo, sha, season - 1), open_commit(repo, sha, season)
    if prev is None or cur is None or _parent(repo, cur["sha"]) is None:
        return {"value": NOT_RECORDED}
    below = _parent(repo, prev["sha"])
    rng = [f"{cur['sha']}^"] + ([f"^{below}"] if below else [])
    revs = _git(repo, "rev-list", *rng).decode().split()
    out = _git(repo, "cat-file", "--batch", inp=("\n".join(revs) + "\n").encode()) if revs else b""
    commits, signed, authors, i = 0, 0, {}, 0
    for _ in revs:
        nl = out.index(b"\n", i)
        size = int(out[i:nl].split()[2])
        c = _parse_commit(out[nl + 1:nl + 1 + size].decode("utf-8", "replace"))
        i = nl + 1 + size + 1
        commits += 1
        a = authors.setdefault(c["author"], {"commits": 0, "signed": 0})
        a["commits"] += 1
        if c["signed"]:
            signed += 1
            a["signed"] += 1
    return {"from": prev["sha"], "to": cur["sha"],
            "window": f"[open(season {season - 1}), open(season {season})): the commit that opened season {season - 1} is in, the one that opened season {season} is out",
            "commits": commits, "signed": signed, "unsigned": commits - signed,
            "signed_label": "signature header (not verified)", "by_author": dict(sorted(authors.items())),
            "names": land_names(repo, rng), "names_rule": "L<n> of the first-parent merges whose subject is 'LAND stack <n>' or 'merge [season-<m> ]L<n>'"}


def head_map(heads: list[dict]) -> dict:
    """The branch map as rows a template loops over: one station per DISTINCT tip, in head-name order, labels alternating between two
    heights so neighbours do not overprint. Every head belongs to exactly one station, so `drawn` is the whole count."""
    groups: dict[str, list[str]] = {}
    for h in heads:
        groups.setdefault(h["sha"], []).append(h["name"])
    stations = []
    for i, (sha, names) in enumerate(groups.items()):
        first = names[0] if len(names[0]) <= 22 else names[0][:21] + "…"
        low = i % 2
        stations.append({"x": 80 + 130 * i, "short": sha[:10], "label": first + (f" +{len(names) - 1}" if len(names) > 1 else ""),
                         "sha_y": 112 + 38 * low, "label_y": 128 + 38 * low, "names": " · ".join(names)})
    return {"stations": stations, "drawn": sum(len(n) for n in groups.values()), "width": 80 + 130 * len(stations) + 40}


def read_heads(path: str, season: int, opened: str | None) -> dict:
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        raise Fail(f"--heads-file: {e}")
    if not lines or not _TIME.match(lines[0].strip()):
        raise Fail("--heads-file: line 1 must be the read time, ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)")
    heads, archive_all = [], []
    for n, ln in enumerate(lines[1:], 2):
        if not _HEADLINE.match(ln):
            raise Fail(f"--heads-file: line {n} is not <40 hex sha><TAB><ref>")
        sha, ref = ln.split("\t")
        if ref.startswith("refs/heads/"):
            heads.append({"name": ref[len("refs/heads/"):], "sha": sha, "short": sha[:10]})
        elif ref.startswith("refs/agi/archive/"):
            archive_all.append({"name": ref[len("refs/agi/archive/"):], "sha": sha, "short": sha[:10]})
    if not heads:
        raise Fail("--heads-file: no refs/heads/* line (an empty capture is refused, not drawn)")
    # the named 9-row rule (season 3): the closed season's archived mains, and the mains overwritten on the rollover day
    day = opened[:10].replace("-", "") if opened else None
    pats = [re.compile(rf"^(?:[^/]+/)?season{season - 1}/main$")]
    if day:
        pats.append(re.compile(rf"^[^/]+-main-pre-{day}T\d{{4}}Z$"))
    archives = [a for a in archive_all if any(p.match(a["name"]) for p in pats)]
    heads.sort(key=lambda h: h["name"])
    return {"read_time": lines[0].strip(), "heads": heads, "heads_total": len(heads), "map": head_map(heads),
            "archives": sorted(archives, key=lambda a: a["name"]), "archives_total": len(archive_all),
            "archive_rule": " | ".join(p.pattern for p in pats)}


def trunk_lines(posts: dict) -> dict:
    """The branch names a page speaks of, read from the posts' own trunk cells (the most common one), never typed."""
    trunk = (Counter(posts["trunks"]).most_common(1) or [(None, 0)])[0][0] if posts["trunks"] else None
    if not trunk:
        return {"trunk": NOT_RECORDED, "prime": NOT_RECORDED, "integration": NOT_RECORDED}
    town, _, rest = trunk.partition("/")
    return {"trunk": trunk, "prime": rest or trunk, "integration": f"{town}/main" if rest else trunk}


def read_box(path: str | None) -> dict:
    """Every cell is a dict with a `value`: a recorded one carries its provenance, the others read {"value": "not recorded"}."""
    if not path:
        return {k: {"value": NOT_RECORDED} for k in BOX_KEYS}
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Fail(f"--box-facts: {e}")
    if not isinstance(data, dict):
        raise Fail("--box-facts: the file must be one JSON object")
    unknown = sorted(set(data) - set(BOX_KEYS))
    if unknown:
        raise Fail(f"--box-facts: unknown key(s) {unknown} (allowed: {list(BOX_KEYS)})")
    out = {}
    for k in BOX_KEYS:
        if k not in data:
            out[k] = {"value": NOT_RECORDED}
            continue
        v = data[k]
        missing = [f for f in BOX_FIELDS if not isinstance(v, dict) or v.get(f) in (None, "")]
        if missing:
            raise Fail(f"--box-facts: {k} needs value, command, reader_uid, read_time (missing {missing})")
        if not _TIME.match(str(v["read_time"])):
            raise Fail(f"--box-facts: {k}.read_time must be ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)")
        out[k] = {f: v[f] for f in BOX_FIELDS}
    return out


def facts(repo: str, season: int, at: str, heads_file: str, box_file: str | None) -> dict:
    sha = _git(repo, "rev-parse", "--verify", f"{at}^{{commit}}").decode().strip()
    tree = read_tree(repo, sha)
    goals = tree.pop("_goals")
    cells = read_cells(repo, sha, season)
    posts = read_posts(repo, sha)
    out = {
        "season": season,
        "at": sha,
        "at_short": sha[:10],
        "prev_season": season - 1,
        "lines": trunk_lines(posts),
        "counts": tree,
        "goals": goal_counts(goals, season),
        **posts,
        "cells": cells,
        "close": read_close(repo, sha, season),
        "ledger": read_ledger(repo, sha, season),
        "grid": read_heads(heads_file, season, cells["opened"]),
        "box": read_box(box_file),
    }
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="season_report.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=".", help="the git repo to read (default: the cwd)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("facts", help="print the report's FACTS as sorted JSON; writes nothing")
    f.add_argument("--season", type=int, required=True, help="the season that OPENED (the report closes season N-1)")
    f.add_argument("--at", required=True, help="the commit every git source is read at")
    f.add_argument("--heads-file", required=True, help="ONE captured ls-remote: line 1 the read time, then <sha><TAB><ref>")
    f.add_argument("--box-facts", help="JSON of facts with no git source: each value + command, reader_uid, read_time")
    a = ap.parse_args(argv)
    try:
        out = facts(a.repo, a.season, a.at, a.heads_file, a.box_facts)
    except Fail as e:
        print(f"season_report: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(out, sort_keys=True, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
