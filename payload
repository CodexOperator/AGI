#!/usr/bin/env python3
"""nest.py slice|log REV ID: a slice is held IN its container's front matter (nest: subtree | a list of ids or mint ids); no ref, no store (D1, post-grid).

slice prints the sorted ids of the container and its members, nothing else: no retired MARK (D3, goal:g7.16.1.11.22, reads members() for that) and no count verb.
A nest value that is NEITHER exactly `subtree` NOR a list ('Subtree', 'subtree # x', a bare id) is MALFORMED: slice|log exit 1 with `nest: malformed nest <value> on <id>` on stderr; links.nest_malformed reports each one. A comment after the value is not stripped by fm(): it is refused."""
import re, subprocess, sys
USAGE = "nest.py slice|log REV ID"
def git(*a, inp=None): return subprocess.run(("git",) + a, input=inp, capture_output=True, text=True, check=True).stdout
def fm(body):
    if not body.startswith("---"): return {}
    d, k = {}, None
    for l in body.split("\n---", 1)[0].split("\n")[1:]:
        m = re.match(r"^([a-z_]+):\s*(.*)$", l)
        if m:
            k, v = m.group(1), m.group(2).strip().strip('"')
            d[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") and v.endswith("]") else (v or [])
        elif k and re.match(r"^\s*- ", l) and isinstance(d[k], list): d[k].append(l.split("- ", 1)[1].strip().strip('"'))
    return d
def graph(rev):
    ps = [p for p in git("ls-tree", "-r", "--name-only", rev, "--", ".agi/nodes").split() if p.endswith(".md")]
    out = subprocess.run(("git", "cat-file", "--batch"), input="".join(f"{rev}:{p}\n" for p in ps).encode(), capture_output=True, check=True).stdout; nodes, i = {}, 0
    for p in ps:
        j = out.index(b"\n", i); n = int(out[i:j].split()[2]); d = fm(out[j + 1:j + 1 + n].decode("utf-8", "replace")); i = j + 2 + n
        if "id" in d: nodes[d["id"]] = (p, d)
    return nodes
class Malformed(Exception): pass
def malformed(spec): return spec is not None and spec != "subtree" and not isinstance(spec, list)  # absent | `subtree` | a list; anything else
def known(nodes, x):  # an exact id wins over a mint id; neither = None (stays out of a slice)
    if x in nodes: return x
    return next((k for k, (_, d) in nodes.items() if d.get("mint_id") == x), None)
def members(nodes, n):
    mints = {}
    for k, (_, d) in nodes.items():
        if isinstance(d.get("mint_id"), str): mints.setdefault(d["mint_id"], k)
    ch = {}
    for k, (_, d) in nodes.items():
        for q in d.get("parents") or []: ch.setdefault(q, []).append(k)
    out, st = set(), [n]  # out = the slice; each member expands ONCE, however it was reached
    while st:
        c = st.pop(); c = c if c in nodes else mints.get(c)  # an exact id wins over a mint id; neither stays out
        if c is None or c in out: continue
        out.add(c); spec = nodes[c][1].get("nest")
        if malformed(spec): raise Malformed(f"nest: malformed nest {spec} on {c}")
        if isinstance(spec, list): st += spec
        elif spec == "subtree":  # down the parents edges THROUGH nest-less members (its OWN visited set); a member with its own nest expands itself
            vis, dn = set(), list(ch.get(c, []))
            while dn:
                m = dn.pop()
                if m in vis: continue
                vis.add(m); st.append(m)
                if "nest" not in nodes[m][1]: dn += ch.get(m, [])
    return out
def live(p): return "/".join(s for s in p.split("/") if s != "deprecated")  # a retire is <type>/f.md <-> deprecated/<type>/f.md: the same node
def log(rev, paths):
    walk = git("log", "--first-parent", "-M", "--name-status", "--format=@%H", rev, "--", ".agi/nodes", "nodes")  # nodes/ = before the one-repo move
    cs, ps, hits = [], set(paths), []
    for l in walk.split("\n"):
        if l.startswith("@"): cs.append((l[1:], []))
        elif len(l.split("\t")) > 1: cs[-1][1].append(l.split("\t"))
    for h, fs in cs:  # newest first
        if any(x in ps for f in fs for x in f[1:]): hits.append(h)
        for f in fs:
            if f[0].startswith("R") and f[2] in ps: ps.add(f[1])  # a retire move maps back to the old path
            elif f[0] == "A" and f[1] in ps: ps.update(g[1] for g in fs if g[0] == "D" and live(g[1]) == live(f[1]))  # a retire that also edits is D + A: the same path once `deprecated/` is stripped (never the same basename across types)
    return hits
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]): print("usage: " + USAGE); sys.exit(0)
    if len(a) != 3 or a[0] not in ("slice", "log"): print("usage: " + USAGE, file=sys.stderr); sys.exit(2)
    verb, rev, n = a
    try: nodes = graph(rev)
    except subprocess.CalledProcessError as e: print("nest: git failed: " + (e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr or "").strip(), file=sys.stderr); sys.exit(1)
    if known(nodes, n) is None: print(f"nest: unknown id {n}", file=sys.stderr); sys.exit(1)
    try: s = members(nodes, n)
    except Malformed as e: print(e, file=sys.stderr); sys.exit(1)
    print("\n".join(sorted(s)) if verb == "slice" else "\n".join(log(rev, [nodes[m][0] for m in s])))
