#!/usr/bin/env python3
"""legacy.py: a node's legacy mark, COMPUTED from the bytes (D3, goal:g7.16.1.11.22, doc:rse-d3-legacy v2).

mark(rev, season, path) -> "legacy" | "-" | "?"   read off the node FILE's own first-parent history (renames followed, so a retire move keeps it):
  ENTRY = the NEWEST of the path's first commit, the commit that ADDS `nest:`, and the commit after which `season:` equals the current season;
  graphed = a commit ABOVE the entry after which `parents:` GAIN a `goal:` id absent at the entry (or the node was minted with a goal parent): "-", else "legacy". "?" = no history.
label(rev, season, path[, nodes]) -> "" | "[legacy]" | "[legacy ⊃k]" | "[⊃k]"   k = |members(N)| - 1 from nest.py (a retired member still counts).
labels(rev, season, paths, nodes) -> {path: label}   the viewport's batch: one history walk for the cache keys, a per-user cache for the slow half.
A library (no CLI, so no _OUTSIDE_CLIS entry): viewport.py calls it. No front-matter field carries the mark and no ref is read: git history and nest.py's fm()/graph()/members() only. Git runs in CWD (the repo root), or in `CWD` when set.
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nest import fm, graph, members, Malformed
CWD = None
def git(*a, inp=None): return subprocess.run(("git",) + a, input=inp, capture_output=True, text=True, cwd=CWD).stdout
def versions(rev, path):
    out = git("log", "--first-parent", "--follow", "-M", "--name-status", "--format=@%H", rev, "--", path)
    vs, cur = [], None
    for l in out.split("\n"):
        if l.startswith("@"): cur = l[1:]; continue
        f = l.split("\t")
        if cur and len(f) >= 2 and f[0][:1] in "AMR": vs.append((cur, f[-1])); cur = None
    return vs[::-1]  # oldest first
def bodies(vs):  # every version's bytes in one cat-file
    out = subprocess.run(("git", "cat-file", "--batch"), input="".join(f"{c}:{p}\n" for c, p in vs).encode(), capture_output=True, cwd=CWD).stdout; got, i = [], 0
    for _ in vs:
        j = out.index(b"\n", i); h = out[i:j].split()
        if len(h) < 3: got.append(""); i = j + 1; continue
        n = int(h[2]); got.append(out[j + 1:j + 1 + n].decode("utf-8", "replace")); i = j + 2 + n
    return got
def mark(rev, season, path):
    vs = versions(rev, path)  # [(commit, path at that commit)] oldest first
    if not vs: return "?"
    fms = [fm(b) for b in bodies(vs)]
    e = 0
    for i in range(1, len(vs)):
        if fms[i].get("nest") and not fms[i-1].get("nest"): e = i
        if str(fms[i].get("season")) == season and str(fms[i-1].get("season")) != season: e = i
    goals = lambda d: {x for x in (d.get("parents") or []) if isinstance(d.get("parents"), list) and x.startswith("goal:")}
    g0 = goals(fms[e])
    if e == 0 and g0: return "-"  # minted THROUGH a goal: graphed from its first commit
    return "-" if any(goals(fms[i]) - g0 for i in range(e+1, len(vs))) else "legacy"
def render(m, k):
    if m == "?": return ""
    parts = ([] if m == "-" else ["legacy"]) + ([f"⊃{k}"] if k > 0 else [])
    return "[" + " ".join(parts) + "]" if parts else ""
def contains(nodes, nid):  # k; a malformed nest reads as 0 here (links.nest_malformed reports it)
    try: return len(members(nodes, nid)) - 1 if nid in nodes else 0
    except Malformed: return 0
def label(rev, season, path, nodes=None):
    nodes = graph(rev) if nodes is None else nodes
    nid = next((i for i, (p, _) in nodes.items() if p == path), None)
    return render(mark(rev, season, path), contains(nodes, nid))
# the cache: ${XDG_CACHE_HOME:-~/.cache}/agi/legacy.tsv  `path TAB season TAB last-commit TAB mark`, never committed, rebuilt whole when missing.
# The mark depends only on the commits touching the path, so it is keyed by the path's newest commit; k is NOT cached (a subtree's members change with no commit on the container).
def cache_path(): return os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache"), "agi", "legacy.tsv")
def cache_read():
    try:
        with open(cache_path(), encoding="utf-8") as f: rows = [l.rstrip("\n").split("\t") for l in f]
        return {(r[0], r[1]): (r[2], r[3]) for r in rows if len(r) == 4}
    except OSError: return {}
def cache_write(c):
    try:
        p = cache_path(); os.makedirs(os.path.dirname(p), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(p));
        with os.fdopen(fd, "w", encoding="utf-8") as f: f.writelines(f"{a}\t{s}\t{l}\t{m}\n" for (a, s), (l, m) in sorted(c.items()))
        os.replace(tmp, p)
    except OSError: pass
def newest(rev, paths):  # path -> its newest first-parent commit, from ONE walk (stops once every path is found)
    want, got = set(paths), {}
    p = subprocess.Popen(("git", "log", "--first-parent", "--no-renames", "--name-only", "--format=@%H", rev, "--", ".agi/nodes", "nodes"), stdout=subprocess.PIPE, text=True, cwd=CWD, stderr=subprocess.DEVNULL)
    cur = None
    for l in p.stdout:
        l = l.rstrip("\n")
        if l.startswith("@"): cur = l[1:]
        elif l in want and l not in got:
            got[l] = cur
            if len(got) == len(want): break
    p.kill(); p.wait()
    return got
def labels(rev, season, paths, nodes):
    paths = sorted(set(paths)); last = newest(rev, paths); c = cache_read(); dirty = False; out = {}
    ids = {v[0]: k for k, v in nodes.items()}
    for p in paths:
        if p not in last: continue  # uncommitted: no history, no mark
        hit = c.get((p, season))
        if hit and hit[0] == last[p]: m = hit[1]
        else: m = mark(rev, season, p); c[(p, season)] = (last[p], m); dirty = True
        out[p] = render(m, contains(nodes, ids.get(p)))
    if dirty: cache_write(c)
    return out
def season_of(rev):  # current_season of the ladder geometry node at rev ("" when absent)
    return str(fm(git("show", f"{rev}:.agi/nodes/.geometry/ladder.md")).get("current_season") or "")
