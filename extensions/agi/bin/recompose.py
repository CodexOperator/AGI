#!/usr/bin/env python3
"""recompose.py -- goal:g7.16.1.11.46.17 (G1b-1): posts/P recomposed as a VIEW from the grid.

    recompose.py [--trunk REF] [--view REF] [--write]

The trunk (default refs/heads/posts/belam) is read ONCE: its sha is printed and every comparison is against THAT tree.
The view is composed from three sets, each printed with its size:
  * NODE paths  -- every `.agi/nodes/**.md`; its bytes come from the tip of refs/grid/node/<mint> (`node.md`), never from
                   the trunk. Its path is DERIVED from those bytes (`.agi/nodes/[deprecated/]<type>/<slug>.md`, deprecated/
                   iff `status: deprecated`), or named by the frozen legacy map (LEGACY_MAP_ID, read from ITS grid tip).
  * PAYLOAD paths -- each composed node's `payload_ref` (location source_root / repo_root / absent = the repo root), its
                   bytes the tip's `payload` blob; a payload the tip lacks reads as retired only when the trunk lacks it too.
  * CARRIED paths -- every other trunk path, taken from the trunk as is.
A trunk node path no grid ref composes, a ref git cannot read, or a payload the grid cannot place is `unread <name>`, rc 1:
never a diff 0, never filled from the trunk. A ref the map names never-composed (a ghost) is counted and named, never written.
goal:g7.16.1.11.46.18 G1b-2 (rows 5-7): MEMBERSHIP comes from the grid (T11): a ref whose path is not a trunk node path is
counted and named, and must carry a `<mint> never-landed` map row, else `unread <mint>` (a dropped live node is a +row in a
reviewed map diff, never a silent diff 0); a never-landed row whose mint composes a live path is unread too. A tip whose
node.md differs from the trunk's composes the TIP (the grid is the source) and is AHEAD only when the trunk's blob is an
EARLIER version on that mint's ref, else BEHIND (trunk bytes not on the grid) (T12); both rc 1. The map is FROZEN (T13):
every PATH row and never-composed row on its tip is on its FIRST grid version, an added one is unread; never-landed rows
are the only kind a later version may add (U2 as corrected), and T11 governs them. `--write` points the VIEW ref at a parentless commit of the composed
tree; the view ref lives outside every namespace a land, a box or the grid owns (VIEW_FORBIDDEN). Nothing else is written.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from node_writer import node_dir    # T10 (alive 05:20:25Z): ONE path rule, the writer's own, never a second spelling

NODE_NS = "refs/grid/node/"
#: a view ref may live under none of these: a land reads refs/heads/posts/, the box refs/box/ + refs/held/, and grid.py's
#: migrated_trunk_namespaces refuses every grid commit once a ref sits under refs/grid/<v>/node/ (T7, SM 04:57Z 10-28)
VIEW_FORBIDDEN = ("refs/heads/posts/", "refs/box/", "refs/held/", "refs/grid/")
LEGACY_MAP_ID = "config:legacy-paths"
#: the payload bases that resolve to the repo root in this one-repo layout (locations.payload_base)
REPO_BASES = (None, "source_root", "repo_root")


def git(*args: str, inp: bytes | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, input=inp, env=env)


def cat_batch(objs: list[str]) -> list[bytes | None]:
    """Contents of each `<rev>:<path>` / sha, None when missing; one `git cat-file --batch`."""
    if not objs:
        return []
    res = git("cat-file", "--batch", inp=("\n".join(objs) + "\n").encode())
    if res.returncode != 0:
        raise RuntimeError(f"cat-file --batch rc {res.returncode}")
    out, i, got = res.stdout, 0, []
    for _ in objs:
        j = out.index(b"\n", i)
        head = out[i:j].split()
        if head[-1] == b"missing" or head[-1] == b"ambiguous":
            got.append(None)
            i = j + 1
            continue
        n = int(head[2])
        got.append(out[j + 1:j + 1 + n])
        i = j + 1 + n + 1
    return got


def batch_sha(objs: list[str]) -> list[str | None]:
    """The object name of each `<rev>:<path>`, None when missing; one `git cat-file --batch-check`."""
    if not objs:
        return []
    out = git("cat-file", "--batch-check=%(objectname)", inp=("\n".join(objs) + "\n").encode()).stdout.decode().splitlines()
    return [None if x.endswith(" missing") else x.strip() for x in out]


def frontmatter(blob: bytes) -> dict[str, str]:
    """The first value of each top-level `key: value` line of a node's frontmatter."""
    text = blob.decode("utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    fm: dict[str, str] = {}
    for line in (text[4:end] if end > 0 else "").splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m and m.group(1) not in fm:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def live_path(fm: dict[str, str]) -> str | None:
    """The LIVE-form path a node's own bytes derive: `node_writer.node_dir` of its type (NODE_HOME: config -> .geometry)
    + `<slug of id>.md`, or None when id/type are absent."""
    nid, typ = fm.get("id", ""), fm.get("type", "")
    if ":" not in nid or not typ:
        return None
    return f"{node_dir('.agi', typ).as_posix()}/{nid.split(':', 1)[1]}.md"


def placed(live: str, fm: dict[str, str]) -> str:
    """`deprecated/` comes from STATUS, never from a row (term (i)): retire_node moves `nodes/<rest>` to
    `nodes/deprecated/<rest>`, the basename kept."""
    return live.replace(".agi/nodes/", ".agi/nodes/deprecated/", 1) if fm.get("status") == "deprecated" else live


def derived_path(fm: dict[str, str]) -> str | None:
    lp = live_path(fm)
    return None if lp is None else placed(lp, fm)


def is_node_path(p: str) -> bool:
    return p.startswith(".agi/nodes/") and p.endswith(".md")


def view_ref_problem(ref: str) -> str | None:
    if not ref.startswith("refs/") or git("check-ref-format", ref).returncode != 0:
        return f"view ref {ref!r} is not a well-formed ref under refs/"
    for ns in VIEW_FORBIDDEN:
        if ref.startswith(ns):
            return f"view ref {ref} sits under {ns}, a namespace a land, a box or the grid owns"
    return None


def map_rows(text: str) -> tuple[list[tuple[str, str]], str | None]:
    """The `(mint, where)` rows of a legacy-map node.md: its ONE `## rows` section, up to the next heading or the THOUGHT block;
    every non-blank line there is a row (one that does not parse is a problem, never skipped)."""
    end = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    body = (text[end + 5:] if end > 0 else "").splitlines()
    at = [i for i, ln in enumerate(body) if ln.startswith("## rows")]
    if len(at) != 1:
        return [], f"{LEGACY_MAP_ID} carries {len(at)} '## rows' sections (exactly one holds the rows)"
    rows = []
    for line in body[at[0] + 1:]:
        if line.startswith("#") or line.startswith("<!--"):
            break                                           # the row region ends at the next heading or the THOUGHT block
        if not line.strip():
            continue
        # every other body line IS a row: one that does not parse is never skipped (a skipped row would compose nothing there)
        m = re.fullmatch(r"([A-Za-z0-9][A-Za-z0-9/._-]*) (\S+)", line.strip())
        if not m:
            return [], f"{LEGACY_MAP_ID} body line {line.strip()[:60]!r} is not '<mint> <path|never-composed|never-landed>'"
        rows.append((m.group(1), m.group(2)))
    return rows, None


MEMBERSHIP = ("never-composed", "never-landed")


def legacy_map(tips: dict[str, str], blobs: dict[str, bytes | None]) -> tuple[dict[str, str], set[str], set[str], str | None, str | None]:
    """The frozen legacy map, read from ITS OWN grid tip (the node whose id is LEGACY_MAP_ID): its ONE `## rows` section, up to
    the next heading or the THOUGHT block, holds the rows; every non-blank line there is a row, `<mint> <path>` (a legacy path) or `<mint> never-composed` (a ghost), the mint any grid ref name
    (31-hex and `hyp/...` names exist); `<mint> never-landed` is a MEMBERSHIP row (T11). Returns (paths, ghosts, never_landed,
    the map's mint, problem)."""
    hits = [m for m, b in blobs.items() if b is not None and frontmatter(b).get("id") == LEGACY_MAP_ID]
    if not hits:
        return {}, set(), set(), None, None
    if len(hits) > 1:
        return {}, set(), set(), None, f"{len(hits)} grid refs carry {LEGACY_MAP_ID}: {' '.join(sorted(hits))}"
    paths: dict[str, str] = {}
    member: dict[str, set[str]] = {k: set() for k in MEMBERSHIP}
    rows, problem = map_rows(blobs[hits[0]].decode("utf-8", errors="replace"))
    if problem:
        return {}, set(), set(), None, problem
    for mint, where in rows:
        if mint in paths or any(mint in s for s in member.values()):
            return {}, set(), set(), None, f"{LEGACY_MAP_ID} names mint {mint} twice"
        if mint not in tips:
            return {}, set(), set(), None, f"{LEGACY_MAP_ID} names mint {mint}, which has no grid ref"
        if where in MEMBERSHIP:
            member[where].add(mint)
            continue
        if not is_node_path(where) or where.startswith(".agi/nodes/deprecated/"):
            return {}, set(), set(), None, f"{LEGACY_MAP_ID} row {mint}: {where} is not a LIVE-form node path (deprecated/ comes from status)"
        if where == live_path(frontmatter(blobs[mint] or b"")):
            return {}, set(), set(), None, f"{LEGACY_MAP_ID} row {mint}: {where} is the derived path (a map row must be needed)"
        paths[mint] = where
    if len(set(paths.values())) != len(paths):
        return {}, set(), set(), None, f"{LEGACY_MAP_ID} names one path for two mints"
    return paths, member["never-composed"], member["never-landed"], hits[0], None


def frozen_problems(tip: str, rows_now: dict[str, str]) -> tuple[list[str], str | None]:
    """T13 (sp 05:50:03Z) + U2 as corrected (sp [correction] 07:55:06Z, 3/3 alive 07:56:52Z): every PATH row and every
    never-composed row on the map's tip is on the map's FIRST grid version (the root of its first-parent chain); an added or
    re-pointed one = `row added after the freeze <mint>`; a removed row is legal. never-landed rows are the ONLY kind a later
    version may add (T11 governs them), so T11's freeze version passes. A ghost row is frozen because a ghost mint is dropped
    before any claim and never reaches T11's no-live-path check: an added ghost row would bypass T11."""
    r = git("rev-list", "--first-parent", tip)
    first = r.stdout.decode().split()[-1:] if r.returncode == 0 else []
    if not first:
        return [], f"the first grid version of {LEGACY_MAP_ID} (rev-list {tip[:12]} rc {r.returncode})"
    blob = cat_batch([f"{first[0]}:node.md"])[0]
    rows, problem = map_rows((blob or b"").decode("utf-8", errors="replace"))
    if blob is None or problem:
        return [], f"the first grid version {first[0][:12]} of {LEGACY_MAP_ID} ({problem or 'no node.md'})"
    at_first = {(m, w) for m, w in rows if w != "never-landed"}
    return [f"unread {m} (row added after the freeze {m}: {LEGACY_MAP_ID} row {m} {w} is not on its first grid version "
            f"{first[0][:12]})" for m, w in sorted(rows_now.items()) if (m, w) not in at_first], None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--trunk", default="refs/heads/posts/belam")
    ap.add_argument("--view", default=None, help="default refs/view/<trunk ref tail>")
    ap.add_argument("--write", action="store_true", help="point the view ref at the composed tree")
    a = ap.parse_args(argv)
    say = lambda s: print(f"recompose: {s}")
    unread: list[str] = []

    view = a.view or "refs/view/" + a.trunk.split("refs/heads/", 1)[-1]
    why = view_ref_problem(view)
    if why:
        say(f"unread ({why})")
        return 1
    r = git("rev-parse", "-q", "--verify", f"{a.trunk}^{{commit}}")
    if r.returncode != 0:
        say(f"unread (trunk {a.trunk} does not name a commit)")
        return 1
    trunk = r.stdout.decode().strip()                       # read ONCE (T8): every comparison is against this tree
    say(f"trunk {a.trunk} = {trunk}")

    r = git("ls-tree", "-r", "-z", "--full-tree", trunk)
    if r.returncode != 0:
        say(f"unread (ls-tree {trunk} rc {r.returncode})")
        return 1
    ptree: dict[str, tuple[str, str]] = {}                  # path -> (mode, sha)
    for e in r.stdout.split(b"\0"):
        if e:
            meta, p = e.split(b"\t", 1)
            mode, _, sha = meta.decode().split()
            ptree[p.decode()] = (mode, sha)

    r = git("for-each-ref", "--format=%(refname) %(objectname)", NODE_NS)
    if r.returncode != 0:
        say(f"unread (for-each-ref {NODE_NS} rc {r.returncode})")
        return 1
    tips = {ln.split()[0][len(NODE_NS):]: ln.split()[1] for ln in r.stdout.decode().splitlines() if ln.strip()}
    if not tips:
        say(f"unread ({NODE_NS} lists no ref)")
        return 1
    mints = sorted(tips)
    # a ref at a missing / non-commit object is unread BY NAME (T3), never a node that is simply absent
    kc = git("cat-file", "--batch-check", inp=("\n".join(tips[m] for m in mints) + "\n").encode())
    kinds = kc.stdout.decode().splitlines()
    if kc.returncode != 0 or len(kinds) != len(mints):     # N1: a short or failed read never zips into a shorter set
        say(f"unread (cat-file --batch-check over {len(mints)} grid tips: rc {kc.returncode}, {len(kinds)} line(s))")
        return 1
    readable = []
    for m, k in zip(mints, kinds):
        if not k.endswith("missing") and k.split()[1:2] == ["commit"]:
            readable.append(m)
        else:
            unread.append(f"unread {m} (its grid ref {NODE_NS}{m} names {k.split()[0][:12]}, not a readable commit)")
    nodemd = dict(zip(readable, cat_batch([f"{tips[m]}:node.md" for m in readable])))
    payload = dict(zip(readable, cat_batch([f"{tips[m]}:payload" for m in readable])))
    for m in readable:
        if nodemd[m] is None:
            unread.append(f"unread {m} (its grid tip {tips[m][:12]} carries no node.md)")

    lmap, ghosts, never, map_mint, problem = legacy_map(tips, nodemd)
    if problem:
        say(f"unread ({problem})")
        return 1
    if map_mint is not None:                                # T13: the map is read from its grid tip, its path rows frozen
        added, problem = frozen_problems(tips[map_mint], {**lmap, **{m: "never-composed" for m in ghosts}})
        if problem:
            say(f"unread ({problem})")
            return 1
        unread.extend(added)

    # bind every readable mint to the ONE path its bytes (or the map) name
    claim: dict[str, list[str]] = {}
    for m in readable:
        if nodemd[m] is None or m in ghosts:
            continue
        fm = frontmatter(nodemd[m])
        p = placed(lmap[m], fm) if m in lmap else derived_path(fm)
        if p is None:
            unread.append(f"unread {m} (its node.md names no id/type, so no path)")
            continue
        claim.setdefault(p, []).append(m)
    node_paths = {p for p in ptree if is_node_path(p)}
    composed: dict[str, str] = {}                           # node path -> mint
    no_live = []
    for p, ms in claim.items():
        if p not in node_paths:
            no_live.extend(ms)                              # never landed / an orphan: counted + named, never written
            # T11: membership from the GRID, never from the trunk listing: a ref with no live path is named by a never-landed
            # row, else it is a node the trunk dropped (or a new ref after the freeze): unread by mint
            unread.extend(f"unread {m} (no live path {p} and no '{m} never-landed' row in {LEGACY_MAP_ID})"
                          for m in ms if m not in never)
        elif len(ms) > 1:
            unread.append(f"unread {p} (claimed by {len(ms)} grid refs: {' '.join(sorted(ms))})")
        else:
            composed[p] = ms[0]
    for m in sorted(never):                                 # T11: a never-landed row is REMOVED in the land that lands its node
        p = next((q for q, x in composed.items() if x == m), None)
        if p is not None:
            unread.append(f"unread {m} (a '{m} never-landed' row in {LEGACY_MAP_ID}, but it composes the live path {p})")
    for p in sorted(node_paths - set(composed)):
        if not any(p == q for q, ms in claim.items() if len(ms) > 1):
            unread.append(f"unread {p} (no grid ref composes this node path; never filled from the trunk)")

    # payloads: node-owned, from the tip's `payload` blob at the node's payload_ref
    pay: dict[str, tuple[str, str]] = {}                    # payload path -> (mint, blob sha)
    retired = 0
    for p, m in sorted(composed.items()):
        fm = frontmatter(nodemd[m])
        ref = fm.get("payload_ref")
        if not ref:
            continue
        if fm.get("location") not in REPO_BASES:
            unread.append(f"unread {m} (payload location {fm.get('location')!r} does not resolve inside the repo)")
            continue
        if payload[m] is None:
            if ref in ptree:
                unread.append(f"unread {m} (its tip carries no payload, but the trunk has {ref})")
            else:
                retired += 1                                # the retired payloads: absent on both sides
            continue
        sha = batch_sha([f"{tips[m]}:payload"])[0]
        if ref in pay and pay[ref][1] != sha:
            unread.append(f"unread {ref} (payload of {pay[ref][0]} and {m}, two different blobs)")
            continue
        pay.setdefault(ref, (m, sha))

    carried = [p for p in ptree if not is_node_path(p) and p not in pay]
    say(f"sets: node {len(composed)} composed of {len(node_paths)} trunk node paths, payload {len(pay)} "
        f"(+{retired} retired, absent on both sides), carried {len(carried)} (from the trunk as is)")
    say(f"refs: {len(tips)} under {NODE_NS}; {len(no_live)} with no live path, {len(ghosts)} never-composed (map), "
        f"{len(lmap)} placed by the legacy map, {len(never)} never-landed (map); none of these written")
    for m in sorted(no_live):                               # WHOLE (alive 05:20:25Z (b)): a drop is a count change + a new name
        say(f"  no live path {m}")

    # the composed tree: carried entries as the trunk has them, node + payload entries from the grid
    entries = [(ptree[p][0], ptree[p][1], p) for p in carried]
    differ = []
    nodesha = dict(zip(composed, batch_sha([f"{tips[m]}:node.md" for m in composed.values()])))
    for p, m in composed.items():
        entries.append(("100644", nodesha[p], p))
        if nodesha[p] != ptree[p][1]:
            differ.append((m, p))
    for p, (m, sha) in pay.items():
        mode = git("ls-tree", tips[m], "payload").stdout.decode().split()[0]
        entries.append((mode, sha, p))
    # T12 (sp 05:50:03Z): AHEAD only when the trunk's blob is an EARLIER version on that mint's ref; the history is walked for
    # these candidates only (blob != the trunk's), never for every ref (aio's nit)
    for m, p in sorted(differ):
        r = git("rev-list", tips[m])
        hist = r.stdout.decode().split() if r.returncode == 0 else []
        if not hist:
            unread.append(f"unread {m} (rev-list {tips[m][:12]} rc {r.returncode}: its history is not readable)")
        elif ptree[p][1] in set(batch_sha([f"{c}:node.md" for c in hist])):
            say(f"  AHEAD {m} {p}: the grid tip {tips[m][:12]} is composed (the trunk's blob is an earlier version on its ref)")
        else:
            say(f"  BEHIND {m} {p} (trunk bytes not on the grid): the grid tip {tips[m][:12]} is composed")

    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_INDEX_FILE": os.path.join(d, "index")}
        info = "".join(f"{mode} {sha}\t{p}\n" for mode, sha, p in entries).encode()
        r = git("update-index", "--add", "--index-info", inp=info, env=env)
        w = git("write-tree", env=env) if r.returncode == 0 else r
    if r.returncode != 0 or w.returncode != 0:
        say(f"unread (the composed tree could not be built: {(r.stderr or w.stderr).decode().strip()[:160]})")
        return 1
    tree = w.stdout.decode().strip()
    diff = git("diff-tree", "-r", "--name-status", f"{trunk}^{{tree}}", tree)
    if diff.returncode != 0:
        say(f"unread (diff-tree rc {diff.returncode})")
        return 1
    lines = diff.stdout.decode().splitlines()
    say(f"diff vs the trunk {trunk[:10]}: {len(lines)} path(s)" + (f" (first 20 of {len(lines)})" if len(lines) > 20 else ""))
    for ln in lines[:20]:
        say(f"  {ln}")
    if len(unread) > 20:                                    # N2: a cut list says it is cut
        say(f"unread lines (first 20 of {len(unread)}):")
    for u in unread[:20]:
        print(f"  {u}")
    if unread:
        say(f"unread {len(unread)}: the view is NOT whole")
    if a.write and not unread:
        c = git("commit-tree", tree, "-m", f"recompose view of {a.trunk} {trunk}\n\nRecompose-Trunk: {trunk}\n")
        u = git("update-ref", view, c.stdout.decode().strip()) if c.returncode == 0 else c
        if c.returncode != 0 or u.returncode != 0:
            say(f"unread (the view ref {view} could not be written)")
            return 1
        say(f"view {view} = {c.stdout.decode().strip()} (tree {tree})")
    return 1 if unread or lines else 0


if __name__ == "__main__":
    sys.exit(main())
