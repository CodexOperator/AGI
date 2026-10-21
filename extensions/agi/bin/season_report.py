#!/usr/bin/env python3
"""season_report.py -- the FACTS half of the end-of-season report (goal:g5.4.1, council design 10-15).

    season_report.py [--repo DIR] facts --season N --at SHA --heads-file F [--box-facts F2]
    season_report.py [--repo DIR] refresh-facts --doc FILE --season N --at SHA --heads-file F [--box-facts F2]
    season_report.py [--repo DIR] render --doc doc:season-N-report --at SHA --out FILE --heads-file F [--box-facts F2] [--media AUDIO]

`facts` prints ONE sorted JSON object on stdout and nothing else. It WRITES NOTHING (no ref, no file, no index) and
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

`refresh-facts` rewrites ONLY the FACTS block of a doc node (between its BEGIN/END markers; every other byte is kept) with `facts` + the
sha256 of the heads / box-facts files it read. `render` is a pure function of (template blob, doc blob, both read AT --at, the facts
inputs it is handed): it RECOMPUTES the doc's facts block at the block's own `at` and refuses any byte of difference, runs the narrative
rules (shas never typed, digits only as a facts slot / node id / L-label / a time in the facts), HTML-escapes every fill, and writes the
page in ONE atomic move only when every check passed (rc 2 and NO file otherwise).
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

NODES = ".agi/nodes"
POSTS_PATH = f"{NODES}/.geometry/posts.md"
LADDER_PATH = f"{NODES}/.geometry/ladder.md"
TOP_K = 9                         # the type rows a page draws; every other type folds into ONE "other" row
BOX_KEYS = ("run_rc", "run_time", "complete_time", "posts_live", "pin", "freeze_window", "restarts")
BOX_FIELDS = ("value", "command", "reader_uid", "read_time")
BOX_EVENTS = "events"             # the run's timeline times: {event_name: a box cell whose value is an ISO-8601 UTC time}
TEMPLATE_PATH = "extensions/agi/templates/season_report/report.html"
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
    mismatch, dep_mismatch, from_path, by_type, goals, ids = [], [], [], Counter(), [], set()
    live = deprecated = status_active = status_deprecated = 0
    for (dep, tdir, stem, _), body in zip(files, bodies):
        fm = _frontmatter(body.decode("utf-8", "replace"))
        status = _fm_scalar(fm, "status")
        nid = _fm_scalar(fm, "id")
        if not nid:
            nid = f"{tdir}:{stem}"                  # the path spells the id only when the frontmatter does not: flagged
            from_path.append(nid)
        ids.add(nid)
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
        "_ids": ids,
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
    letter = _git(repo, "log", "-1", "--format=%G?", c["sha"]).decode().strip() or "?"      # a gpgsig HEADER proves nothing: git verifies it
    verified = letter == "G"
    kind = "signed" if verified else "UNVERIFIED"
    return {"value": _iso(c["ts"]), "sha": c["sha"], "signed": verified, "verify": letter,
            "label": f"season {season - 1} closed: committer time of the {kind} ladder-cell commit that opened season {season}"}


def land_names(repo: str, rng: list[str]) -> tuple[list[str], int]:
    """(the L<n> of the first-parent merges whose subject is a land shape, how many first-parent merges are ': LAND' at all).
    Prose that mentions an L<n> never counts; `names` is never the season's lands, `lands_total` is."""
    subjects = _git(repo, "log", "--first-parent", "--merges", "-z", "--format=%s", *rng).decode("utf-8", "replace").split("\0")
    nums = {int(m.group(1)) for s in subjects for m in (_LAND.match(s) or _LFORM.match(s),) if m}
    return [f"L{n}" for n in sorted(nums)], sum(1 for s in subjects if ": LAND" in s)


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
    names, lands = land_names(repo, rng)
    return {"from": prev["sha"], "to": cur["sha"],
            "window": f"[open(season {season - 1}), open(season {season})): the commit that opened season {season - 1} is in, the one that opened season {season} is out",
            "commits": commits, "signed": signed, "unsigned": commits - signed,
            "signed_label": "signature header (not verified)", "by_author": dict(sorted(authors.items())),
            "names": names, "names_count": len(names), "lands_total": lands,
            "names_rule": "L<n> of the first-parent merges whose subject is 'LAND stack <n>' or 'merge [season-<m> ]L<n>'; names is never the season's lands: lands_total counts every first-parent ': LAND' merge"}


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


def _cell(v, where: str, time_value: bool = False) -> dict:
    missing = [f for f in BOX_FIELDS if not isinstance(v, dict) or v.get(f) in (None, "")]
    if missing:
        raise Fail(f"--box-facts: {where} needs value, command, reader_uid, read_time (missing {missing})")
    if not _TIME.match(str(v["read_time"])):
        raise Fail(f"--box-facts: {where}.read_time must be ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)")
    if time_value and not _TIME.match(str(v["value"])):
        raise Fail(f"--box-facts: {where}.value must be ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)")
    return {f: v[f] for f in BOX_FIELDS}


# a box event's `command` must be a read anyone can run again: one of these three shapes (a vague "box log read" is refused, naming it)
_META = re.compile(r"[;&|$`<>\\]")
_EXACT_READ = (
    lambda c: c.startswith("journalctl ") and re.search(r"\s(?:-u|--unit)[ =]\S+", c) and re.search(r"\s--since[ =]\S+", c) and re.search(r"\s--until[ =]\S+", c),
    lambda c: re.fullmatch(r"systemctl show -p [A-Za-z]+ [A-Za-z0-9_.@:-]+", c),
    lambda c: re.fullmatch(r"/[A-Za-z0-9_./-]+:[1-9][0-9]*", c),
)


def exact_read(command: str) -> bool:
    return not _META.search(command) and any(shape(command) for shape in _EXACT_READ)


def _read_events(v) -> dict:
    """events: {name: EITHER {"sha": <commit at --at>[, "value": T]} (render recomputes the committer time) OR a box cell whose command is an exact read}."""
    if not isinstance(v, dict) or not v:
        raise Fail("--box-facts: events must be a non-empty object {event_name: cell}")
    out = {}
    for name in sorted(v):
        if not re.match(r"^[a-z][a-z0-9_]*$", name) or name == "value":
            raise Fail(f"--box-facts: events.{name}: a name is lowercase letters, digits and _ (and not 'value')")
        c = v[name]
        if isinstance(c, dict) and "sha" in c:
            if set(c) - {"sha", "value"} or not re.fullmatch(r"[0-9a-f]{40}", str(c["sha"])) or (c.get("value") is not None and not _TIME.match(str(c["value"]))):
                raise Fail(f"--box-facts: events.{name}: a commit event is {{\"sha\": <40 hex>}} (+ an optional ISO \"value\" that must equal its committer time)")
            out[name] = {"sha": c["sha"], "value": c.get("value")}
            continue
        out[name] = _cell(c, f"events.{name}", time_value=True)
        if not exact_read(out[name]["command"]):
            raise Fail(f"--box-facts: events.{name}: command {out[name]['command']!r} is not an exact re-runnable read "
                       "(journalctl -u UNIT --since T --until T | systemctl show -p PROP UNIT | /path:LINE), or give {\"sha\": <commit>}")
    return out


def resolve_events(repo: str, at_sha: str, box: dict) -> None:
    """A commit event's time is the committer time of its sha, RECOMPUTED here at --at; a cell time that disagrees is refused."""
    ev = box.get(BOX_EVENTS)
    if not isinstance(ev, dict) or ev.get("value") == NOT_RECORDED and len(ev) == 1:
        return
    for name, c in ev.items():
        if "sha" not in c or "reader_uid" in c:
            continue
        r = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", f"{c['sha']}^{{commit}}", at_sha], capture_output=True)
        if r.returncode != 0:
            raise Fail(f"--box-facts: events.{name}: {c['sha'][:10]} is not a commit in the history of {at_sha[:10]}")
        iso = _iso(_commit(repo, c["sha"])["ts"])
        if c["value"] is not None and c["value"] != iso:
            raise Fail(f"--box-facts: events.{name}: the cell time {c['value']} differs from the committer time {iso} of {c['sha'][:10]}")
        ev[name] = {"value": iso, "sha": c["sha"], "source": "git"}


def read_box(path: str | None) -> dict:
    """Every cell is a dict with a `value`: a recorded one carries its provenance, the others read {"value": "not recorded"}."""
    if not path:
        return {k: {"value": NOT_RECORDED} for k in (*BOX_KEYS, BOX_EVENTS)}
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Fail(f"--box-facts: {e}")
    if not isinstance(data, dict):
        raise Fail("--box-facts: the file must be one JSON object")
    unknown = sorted(set(data) - set(BOX_KEYS) - {BOX_EVENTS})
    if unknown:
        raise Fail(f"--box-facts: unknown key(s) {unknown} (allowed: {list(BOX_KEYS) + [BOX_EVENTS]})")
    out = {BOX_EVENTS: _read_events(data[BOX_EVENTS]) if BOX_EVENTS in data else {"value": NOT_RECORDED}}
    for k in BOX_KEYS:
        if k not in data:
            out[k] = {"value": NOT_RECORDED}
            continue
        out[k] = _cell(data[k], k)
    return out


def facts(repo: str, season: int, at: str, heads_file: str, box_file: str | None) -> dict:
    return facts_full(repo, season, at, heads_file, box_file)[0]


def facts_full(repo: str, season: int, at: str, heads_file: str, box_file: str | None) -> tuple[dict, set]:
    """(the facts, every node id at AT): the ids are what a narrative's node references must resolve against."""
    sha = _git(repo, "rev-parse", "--verify", f"{at}^{{commit}}").decode().strip()
    tree = read_tree(repo, sha)
    goals = tree.pop("_goals")
    ids = tree.pop("_ids")
    cells = read_cells(repo, sha, season)
    posts = read_posts(repo, sha)
    box = read_box(box_file)
    resolve_events(repo, sha, box)
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
        "box": box,
    }
    return out, ids


# ---- the doc node: the FACTS block, the narrative sections ---------------------------------------------------------------------------
_BEGIN = re.compile(r"^<!-- FACTS:BEGIN at=([0-9a-f]{40}) -->$", re.M)
_END = re.compile(r"^<!-- FACTS:END -->$", re.M)
NARR_SCALARS = ("narr.lede", "narr.day_intro", "narr.map_intro", "narr.graph_note", "narr.engine_note")
NARR_ROWS = {"narr.timeline": ({"when", "title", "text"}, {"cls"}), "narr.open": ({"text"}, set())}
MEDIA_FIELDS = ("src", "title", "credit", "first_line", "lines")
_SECTION = re.compile(r"^## (\S+)[ \t]*$", re.M)
_SLOT = re.compile(r"\{\{(#rows |/rows|#media|/media)?\s*([^}|]*?)\s*(?:\|(\w+))?\}\}")


class Safe(str):
    """Text that is already HTML (a filled narrative, a JS-safe JSON): the one kind of value `_fmt` does not escape."""


def doc_path(doc_id: str) -> str:
    if not re.match(r"^doc:[A-Za-z0-9][A-Za-z0-9_.-]*$", doc_id):
        raise Fail(f"--doc {doc_id!r}: render reads a doc node by its id (doc:season-<N>-report)")
    return f"{NODES}/doc/{doc_id[4:]}.md"


def _block_span(text: str) -> tuple[int, int, str]:
    begins, ends = list(_BEGIN.finditer(text)), list(_END.finditer(text))
    if len(begins) != 1 or len(ends) != 1 or ends[0].start() < begins[0].end():
        raise Fail(f"the doc needs exactly one '<!-- FACTS:BEGIN at=<sha> -->' ... '<!-- FACTS:END -->' pair (found {len(begins)} BEGIN, {len(ends)} END)")
    return begins[0].start(), ends[0].end(), begins[0].group(1)


def _block_text(facts_json: dict) -> str:
    return (f"<!-- FACTS:BEGIN at={facts_json['at']} -->\n```json\n" + json.dumps(facts_json, sort_keys=True, indent=1)
            + "\n```\n<!-- FACTS:END -->")


def _sha256(path: str | None) -> str | None:
    if not path:
        return None
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError as e:
        raise Fail(f"cannot read {path}: {e}")


def _write_atomic(path: str, data: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".season-report-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def refresh_facts(repo: str, doc_file: str, season: int, at: str, heads_file: str, box_file: str | None) -> None:
    """Replace ONLY the bytes of the doc's FACTS block; refuse (file untouched) on a missing / duplicated marker."""
    try:
        text = Path(doc_file).read_text(encoding="utf-8")
    except OSError as e:
        raise Fail(f"--doc: {e}")
    a, b, _ = _block_span(text)
    out = facts(repo, season, at, heads_file, box_file)
    out["inputs"] = {"heads_sha256": _sha256(heads_file), "box_sha256": _sha256(box_file)}     # what render must be handed again
    _write_atomic(doc_file, text[:a] + _block_text(out) + text[b:])


def read_doc(text: str) -> dict:
    """The doc blob -> {block, narr (scalars as raw text), rows, roles, media}; every missing or malformed section is a Fail."""
    a, b, at = _block_span(text)
    m = re.search(r"```json\n(.*)\n```", text[a:b], re.S)
    if not m:
        raise Fail("the FACTS block holds no ```json fence")
    try:
        block = json.loads(m.group(1))
    except ValueError as e:
        raise Fail(f"the FACTS block is not JSON ({e})")
    if not isinstance(block, dict) or block.get("at") != at:
        raise Fail("the FACTS block's JSON `at` is not the BEGIN marker's at")
    rest = text[:a] + text[b:]
    heads = list(_SECTION.finditer(rest))
    secs: dict[str, str] = {}
    for i, h in enumerate(heads):
        name = h.group(1)
        if name in secs:
            raise Fail(f"section {name} appears twice")
        secs[name] = rest[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(rest)].strip()
    known = {*NARR_SCALARS, *NARR_ROWS, "roles", "media"}
    odd = sorted(n for n in secs if n.startswith("narr.") and n not in known)
    if odd:
        raise Fail(f"unknown narrative section(s) {odd} (known: {sorted(known)})")
    missing = [n for n in (*NARR_SCALARS, *NARR_ROWS, "roles") if not secs.get(n)]
    if missing:
        raise Fail(f"narrative section(s) missing or empty: {missing}")
    rows: dict[str, list[dict]] = {}
    for name, (need, opt) in NARR_ROWS.items():
        rows[name] = []
        for n, ln in enumerate(secs[name].splitlines(), 1):
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except ValueError as e:
                raise Fail(f"{name} line {n} is not JSON ({e})")
            if not isinstance(r, dict) or set(r) - need - opt or need - set(r) or not all(isinstance(v, str) for v in r.values()):
                raise Fail(f"{name} line {n}: a row is an object of strings with keys {sorted(need)} (+ {sorted(opt)})")
            rows[name].append(r)
        if not rows[name]:
            raise Fail(f"narrative section {name} holds no rows")
    try:
        roles = json.loads(secs["roles"])
    except ValueError as e:
        raise Fail(f"roles is not JSON ({e})")
    if not isinstance(roles, dict) or not all(isinstance(v, str) and v for v in roles.values()):
        raise Fail("roles must be one JSON object {head name: role text}")
    media = None
    if secs.get("media"):
        try:
            media = json.loads(secs["media"])
        except ValueError as e:
            raise Fail(f"media is not JSON ({e})")
        if not isinstance(media, dict) or sorted(media) != sorted(MEDIA_FIELDS) or not isinstance(media["lines"], list):
            raise Fail(f"media must be one JSON object with exactly {list(MEDIA_FIELDS)}")
    return {"block": block, "scalars": {n: " ".join(secs[n].split()) for n in NARR_SCALARS}, "rows": rows, "roles": roles, "media": media}


def _first_diff(a, b, path: str = "") -> str | None:
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}{k}"
            d = _first_diff(a[k], b[k], f"{path}{k}.")
            if d:
                return d
        return None
    return None if a == b else path.rstrip(".")


# ---- the narrative rules (council E2, E4): read with the slots MASKED ----------------------------------------------------------------
_WORD = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.:@/\-]*")
_SHA_TOKEN = re.compile(r"^(?=[0-9a-f]*\d)[0-9a-f]{7,40}$")        # 7-40 hex with a digit in it: 'defaced' is a word, 2a8056bcb5 is a sha
_NODE_TOKEN = re.compile(r"^[a-z_]+:\S+$")
_L_TOKEN = re.compile(r"^L\d+$")
_TIME_TOKEN = re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?Z$")     # 06:24Z or 06:24:17Z, the only spelling of a time
_DATE_TOKEN = re.compile(r"^\d{4}-\d\d-\d\d$")


def _leaves(obj, path: str = ""):
    if isinstance(obj, dict):
        for k in sorted(obj):
            yield from _leaves(obj[k], f"{path}{k}.")
    elif not isinstance(obj, list):
        yield path.rstrip("."), obj


def _facts_times(facts_json: dict) -> tuple[set, set]:
    """The ISO times and dates anywhere in the facts, normalised: 'HH:MM' and 'HH:MM:SS' (the Z dropped), and 'YYYY-MM-DD'."""
    times, dates = set(), set()
    for _, v in _leaves(facts_json):
        if isinstance(v, str) and _TIME.match(v):
            times.update({v[11:16], v[11:19]})
            dates.add(v[:10])
    return times, dates


def narr_problems(text: str, facts_json: dict, ids: set, where: str) -> list[str]:
    """Every rule broken by one narrative text, one line each (empty = clean). `text` has its {{facts.*}} slots masked here."""
    out: list[str] = []
    for m in _SLOT.finditer(text):
        path = m.group(2)
        if m.group(1):
            out.append(f"{where}: {m.group(0)} is a template block, not a narrative slot")
        elif path.startswith("narr."):
            out.append(f"{where}: {{{{{path}}}}} inside a narrative is refused")
        elif not path.startswith("facts."):
            out.append(f"{where}: slot {{{{{path}}}}} is not a facts slot")
    masked = _SLOT.sub("\x00", text)
    times, dates = _facts_times(facts_json)
    names = set(facts_json.get("ledger", {}).get("names", []))
    leafmap = {}
    for p, v in _leaves(facts_json):
        leafmap.setdefault(str(v), p)
    for w in _WORD.findall(masked):
        tok = w.rstrip(".:-/@")
        if not tok or not any(c.isdigit() for c in tok):
            continue
        hint = f"use {{{{facts.{leafmap[tok]}}}}}" if tok in leafmap else "use a {{facts.*}} slot that holds it"
        tm = _TIME_TOKEN.match(tok)
        if _SHA_TOKEN.match(tok):
            out.append(f"{where}: sha-shaped token {tok!r}: a sha is never typed, use a {{{{facts.*}}}} slot")
        elif tm:
            norm = f"{int(tm.group(1)):02d}:{tm.group(2)}" + (f":{tm.group(3)}" if tm.group(3) else "")
            if norm not in times:
                out.append(f"{where}: time {tok!r} is not a time in the facts: use a {{{{facts.*|hms}}}} time slot")
        elif _DATE_TOKEN.match(tok):
            if tok not in dates:
                out.append(f"{where}: date {tok!r} is not a date in the facts: use a {{{{facts.*}}}} slot")
        elif _L_TOKEN.match(tok):
            if tok not in names:
                out.append(f"{where}: {tok!r} is not a stack label in facts.ledger.names")
        elif _NODE_TOKEN.match(tok):
            if tok not in ids:
                out.append(f"{where}: {tok!r} is not a node id at {facts_json.get('at_short')}")
        else:
            out.append(f"{where}: digit token {tok!r}: {hint}")
    return out


# ---- the template engine --------------------------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, facts_json: dict, narr: dict, media: dict | None):
        self.facts, self.narr, self.media, self.iters = facts_json, narr, media, Counter()
        self.sources: dict[str, dict] = {}        # the box cells whose values this page printed, first use first: the legend lists them


MARK = '<sup class="src">†</sup>'                 # a value read from a box cell, not recomputed from git
_BOXVAL = re.compile(r"^facts\.box\.((?:events\.)?[a-z_][a-z0-9_]*)\.value$")


def _slot(ctx: "Ctx", rows: list, path: str, flt: str | None) -> str:
    """One filled slot, plus the † mark when it prints a box cell's value (a git-sourced time prints none)."""
    text = _fmt(_resolve(ctx, rows, path), flt, path)
    m = _BOXVAL.match(path)
    if m:
        cell = _resolve(ctx, rows, path[: -len(".value")])
        if isinstance(cell, dict) and cell.get("reader_uid") and cell.get("value") not in (None, NOT_RECORDED):
            ctx.sources.setdefault(m.group(1), cell)
            return text + MARK
    return text


def _parse_template(text: str) -> list:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)        # the slot-grammar legend is not part of the page
    root: list = []
    stack: list[tuple[str, list]] = [("root", root)]
    pos = 0
    for m in _SLOT.finditer(text):
        if m.start() > pos:
            stack[-1][1].append(("text", text[pos:m.start()]))
        pos = m.end()
        kind, path, flt = m.groups()
        if kind == "#rows ":
            body: list = []
            stack[-1][1].append(("rows", path, body))
            stack.append(("rows", body))
        elif kind == "#media":
            body = []
            stack[-1][1].append(("media", body))
            stack.append(("media", body))
        elif kind in ("/rows", "/media"):
            if stack[-1][0] != kind[1:]:
                raise Fail(f"template: {m.group(0)} closes {stack[-1][0]!r}")
            stack.pop()
        else:
            stack[-1][1].append(("slot", path, flt))
    if len(stack) != 1:
        raise Fail(f"template: an unclosed {stack[-1][0]!r} block")
    root.append(("text", text[pos:]))
    return root


def _resolve(ctx: Ctx, rows: list, path: str):
    head, _, rest = path.partition(".")
    if head == "facts":
        cur = ctx.facts
    elif head == "narr":
        cur = ctx.narr
    elif head == "media":
        if ctx.media is None:
            raise Fail(f"slot {{{{{path}}}}} outside a media block")
        cur = ctx.media
    elif head == "render":
        cur = {"box_sources": [{"key": k, "reader_uid": c["reader_uid"], "read_time": c["read_time"], "command": c["command"]} for k, c in ctx.sources.items()]}
    elif head == "row":
        if not rows:
            raise Fail(f"slot {{{{{path}}}}} outside a rows loop")
        cur = rows[-1]
    else:
        raise Fail(f"unknown slot {{{{{path}}}}}")
    for part in rest.split(".") if rest else []:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif head == "facts" and isinstance(cur, dict) and cur.get("value") == NOT_RECORDED:
            return NOT_RECORDED        # N3: a key UNDER a not-recorded cell reads 'not recorded'; a typo anywhere else stays loud
        else:
            raise Fail(f"unknown slot {{{{{path}}}}} (no {part!r})")
    return cur


def _fmt(v, flt: str | None, path: str) -> str:
    if isinstance(v, Safe):
        return str(v)
    if v is None:
        return NOT_RECORDED         # a cell the facts could not read (cells.opened with no town row) reaches the page as 'not recorded'
    if isinstance(v, (dict, list, bool)):
        raise Fail(f"slot {{{{{path}}}}} is not a scalar")
    if flt == "n":
        if isinstance(v, int):
            s = f"{v:,}"
        elif v == NOT_RECORDED:
            s = v
        else:
            raise Fail(f"slot {{{{{path}|n}}}} is not an integer")
    elif flt == "hms":
        if isinstance(v, str) and _TIME.match(v):
            s = v[11:]
        elif v == NOT_RECORDED:
            s = v
        else:
            raise Fail(f"slot {{{{{path}|hms}}}} is not an ISO time")
    elif flt:
        raise Fail(f"slot {{{{{path}|{flt}}}}}: unknown filter")
    else:
        s = str(v)
    return html.escape(s)


def _rows_of(ctx: Ctx, path: str) -> list:
    items = _resolve(ctx, [], path)
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        raise Fail(f"rows over {path}: not a list of rows")
    return items


def _render(nodes: list, ctx: Ctx, rows: list) -> str:
    out: list[str] = []
    for n in nodes:
        if n[0] == "text":
            out.append(n[1])
        elif n[0] == "slot":
            out.append(_slot(ctx, rows, n[1], n[2]))
        elif n[0] == "media":
            if ctx.media is not None:
                out.append(_render(n[1], ctx, rows))
        else:
            items = _rows_of(ctx, n[1])
            ctx.iters[n[1]] += len(items)
            for it in items:
                out.append(_render(n[2], ctx, rows + [it]))
    return "".join(out)


def _fill_narr(text: str, ctx: Ctx) -> Safe:
    """A narrative text -> HTML: the literal parts are escaped, each {{facts.*}} slot is filled (and escaped)."""
    out, pos = [], 0
    for m in _SLOT.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        out.append(_slot(ctx, [], m.group(2), m.group(3)))
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return Safe("".join(out))


_REL = re.compile(r'\b(?:src|href)="([^"]*)"')


def _page_problems(page: str, facts_json: dict, template: str, ctx: Ctx, out_dir: Path) -> list[str]:
    out: list[str] = []
    if "{{" in page:
        out.append("an unfilled '{{' is left on the page")
    allowed = set(re.findall(r"\b[0-9a-f]{7,40}\b", json.dumps(facts_json))) | set(re.findall(r"\b[0-9a-f]{7,40}\b", template))     # F2
    stray = sorted({t for t in re.findall(r"\b[0-9a-f]{7,40}\b", page) if t not in allowed and _SHA_TOKEN.match(t)})
    if stray:
        out.append(f"F2: hex token(s) {stray} on the page are in neither the facts nor the template")
    for ref in _REL.findall(page):                                                                                                    # F7
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", ref, re.I) or not ref:
            continue
        if not (out_dir / ref).exists():
            out.append(f"F7: {ref!r} does not resolve next to the out file")
    g = facts_json["grid"]
    for path, want, tag in (("facts.grid.heads", g["heads_total"], "F8"), ("facts.grid.archives", len(g["archives"]), "F4")):
        if ctx.iters[path] != want:
            out.append(f"{tag}: the page draws {ctx.iters[path]} rows over {path}, the facts hold {want}")
    return out


def render(repo: str, doc_id: str, at: str, out_file: str, heads_file: str, box_file: str | None, media_file: str | None) -> None:
    b = _git(repo, "rev-parse", "--verify", f"{at}^{{commit}}").decode().strip()
    def blob(path: str) -> str:
        r = subprocess.run(["git", "-C", repo, "show", f"{b}:{path}"], capture_output=True, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        if r.returncode != 0:
            raise Fail(f"{path} is not committed at {b[:10]}")
        return r.stdout.decode("utf-8")
    template, doc = blob(TEMPLATE_PATH), read_doc(blob(doc_path(doc_id)))
    block = doc["block"]
    inputs = block.pop("inputs", None)
    if not isinstance(inputs, dict) or "heads_sha256" not in inputs:
        raise Fail("the FACTS block names no inputs (run refresh-facts)")
    if _sha256(heads_file) != inputs["heads_sha256"]:                                                                              # E3
        raise Fail("heads not re-checkable: pass the heads file the block names (sha256 " + str(inputs["heads_sha256"])[:12] + "...)")
    if _sha256(box_file) != inputs.get("box_sha256"):
        raise Fail("box facts not re-checkable: pass the --box-facts file the block names" if inputs.get("box_sha256") else "the block names no box-facts file, but one was passed")
    fresh, ids = facts_full(repo, int(block.get("season", -1)), block.get("at", ""), heads_file, box_file)
    bad = _first_diff(fresh, block)
    if bad:
        raise Fail(f"the FACTS block differs from a recompute at its own `at`: {bad}")
    rfacts = copy.deepcopy(fresh)
    names = [h["name"] for h in rfacts["grid"]["heads"]]
    if sorted(doc["roles"]) != sorted(names):
        gone, extra = sorted(set(names) - set(doc["roles"])), sorted(set(doc["roles"]) - set(names))
        raise Fail(f"roles must name every head exactly once (missing {gone}, not heads {extra})")
    problems: list[str] = []
    for name, text in doc["scalars"].items():
        problems += narr_problems(text, fresh, ids, name)
    for name, lst in doc["rows"].items():
        for i, r in enumerate(lst, 1):
            for k, v in r.items():
                if k == "cls":
                    if v not in ("", "warn"):
                        problems.append(f"{name} row {i}: cls is '' or 'warn'")
                else:
                    problems += narr_problems(v, fresh, ids, f"{name} row {i} {k}")
    for h, text in doc["roles"].items():
        problems += narr_problems(text, fresh, ids, f"roles[{h}]")
    if problems:
        raise Fail("; ".join(problems[:12]) + (f"; ... {len(problems)} in all" if len(problems) > 12 else ""))
    media = None
    if media_file:
        spec = doc["media"]
        if spec is None:
            raise Fail("--media was passed but the doc holds no media section")
        if os.path.basename(media_file) != spec["src"]:
            raise Fail(f"--media {os.path.basename(media_file)!r} is not the doc's media src {spec['src']!r}")
        safe = json.dumps(spec["lines"]).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
        media = {**{k: spec[k] for k in ("src", "title", "credit", "first_line")}, "lines_json": Safe(safe)}
    ctx = Ctx(rfacts, {}, media)
    for h in rfacts["grid"]["heads"]:
        h["role"] = _fill_narr(doc["roles"][h["name"]], ctx)
    ctx.narr = {**{n[5:]: _fill_narr(t, ctx) for n, t in doc["scalars"].items()},
                **{n[5:]: [{k: (v if k == "cls" else _fill_narr(v, ctx)) for k, v in r.items()} for r in lst] for n, lst in doc["rows"].items()}}
    for lst in ctx.narr.values():
        if isinstance(lst, list):
            for r in lst:
                r.setdefault("cls", "")
    page = _render(_parse_template(template), ctx, [])
    probs = _page_problems(page, fresh, template, ctx, Path(out_file).resolve().parent)
    if probs:
        raise Fail("; ".join(probs))
    _write_atomic(out_file, page)



def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="season_report.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=".", help="the git repo to read (default: the cwd)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("facts", help="print the report's FACTS as sorted JSON; writes nothing")
    f.add_argument("--season", type=int, required=True, help="the season that OPENED (the report closes season N-1)")
    f.add_argument("--at", required=True, help="the commit every git source is read at")
    f.add_argument("--heads-file", required=True, help="ONE captured ls-remote: line 1 the read time, then <sha><TAB><ref>")
    f.add_argument("--box-facts", help="JSON of facts with no git source: each value + command, reader_uid, read_time")
    r = sub.add_parser("refresh-facts", help="rewrite ONLY the FACTS block of a doc node; every other byte is kept")
    r.add_argument("--doc", required=True, help="the doc node file")
    r.add_argument("--season", type=int, required=True)
    r.add_argument("--at", required=True, help="the season's close pin: every git source is read here")
    r.add_argument("--heads-file", required=True)
    r.add_argument("--box-facts")
    d = sub.add_parser("render", help="the report page: a pure function of the template and doc blobs at --at; rc 2 and NO file on any broken rule")
    d.add_argument("--doc", required=True, help="the doc node id, doc:season-<N>-report")
    d.add_argument("--at", required=True, help="the commit that holds the template and the committed doc")
    d.add_argument("--out", required=True)
    d.add_argument("--heads-file", required=True, help="the heads file the block's inputs name (its sha256 is checked)")
    d.add_argument("--box-facts", help="the box-facts file the block's inputs name, when it names one")
    d.add_argument("--media", help="the audio file; its basename must be the doc's media src and it must sit next to --out")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "refresh-facts":
            refresh_facts(a.repo, a.doc, a.season, a.at, a.heads_file, a.box_facts)
            return 0
        if a.cmd == "render":
            render(a.repo, a.doc, a.at, a.out, a.heads_file, a.box_facts, a.media)
            return 0
        out = facts(a.repo, a.season, a.at, a.heads_file, a.box_facts)
    except (Fail, OSError) as e:
        print(f"season_report: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(out, sort_keys=True, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
