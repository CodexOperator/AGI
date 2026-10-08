---
id: doc:rse-d1-nest
mint_id: 3b8692c89a6e4e348024c493df258a09
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: alive
model: claude-opus-5-5
role: director
season: 2
tags:
  - council
  - design
  - g7.16.1.11
  - d1
title: "D1 after the grid: a slice lives IN its container's front matter (nest: subtree | a list); the collapse is ONE one-node commit; its history is one git walk (council design, alive)"
town: core
---
# doc:rse-d1-nest

Owner 10-07 14:3xZ (verbatim in AA1.N): "recursively enable any arbitrary slice of the whole graph ... to be encapsulated into a given graph node since each node is itself a mini branch inside the grid trunk ... as long as our stats are read from the grid graph not the flat graph nothing changes. Only the overall appearance changes." Owner 01:5xZ 10-08 (belam [rule] 02:02Z): "Finish encapsulation of grid slices and do a season rollover after getting you on the new engine." Owner 01:4xZ 10-08 on grid commit: "It's already decided" (doc:radically-simple-engine:82, history = `git log -- <path>`; AA1.V, no refs/grid, no cron).

Split (unchanged, 14:40Z 10-07): D1 = alive · D2 (which slices collapse at rollover) = self-perpetuating · D3 (legacy marker + renderer) = all-is-one · trajectory row E1 on town:local-maxxing.

## Why D1 is restated
D1 WAS written and landed (AA1.N in doc:rse-aa1-boxes, 5a1760e82, 15:13Z 10-07), but as ONE grid commit on `refs/grid/<town>/node/<N>` (tree + `nest/<mint>`), plus three grid.py seams G1-G3 and an 11-line fix (goal:g4.13.1). grid commit now retires (E2), so a collapse written onto a grid ref would be written onto a store nobody versions. This node moves the SAME collapse onto the surface that stays: the node file and plain git history.

## The design, one screen
```
 hold      container N's front matter carries the slice:   nest: subtree        (N + every node whose parents name N, recursively through
                                                                                  members that carry their own nest)
                                                            nest:                (an ARBITRARY slice: any ids, any types)
                                                              - <id>
 collapse  ONE edit of N = ONE one-node commit (AA1.V's invariant V4 holds by construction: only N's file changes); no ref, no store, no cron
 expand    members(N): N, then each listed / child member, recursing into a member's own nest; a cycle stops at the seen set
 history   ONE `git log --first-parent -M --name-status -- .agi/nodes` walk, filtered to the slice's paths; a rename (a retire move to
           deprecated/<type>/) maps back to the old path, so a retired member keeps its whole history
 before    versions made before the cutover stay on the frozen refs/grid/<town>/node/<mint>, read-only, never deleted (goal:g7.16.1.6:71)
 counts    members stay files: links.py and metrics.py walk nodes/ with rglob, so active + deprecated counts do not move (AA1.N's F1)
 tangle    a member may sit in two containers (lists overlap freely); the tangle stat (nodes under >= 2 top goals) is D2's input, unchanged
```

## Measured (trunk d9e0ee099e and 8c97e29724, read-only, 02:0xZ 10-08, as agi-alive)
| fact | measured |
|---|---|
| one walk over .agi/nodes | 5,826 first-parent trunk commits, 1.5 s (nice 19); 408 rename entries in it |
| slice goal:g7.16.1.11 (closure of parents edges) | 116 nodes; touched by 540 commits (340 first-parent) |
| slice goal:g7 | 1,326 nodes; touched by 3,270 of the 5,826 trunk commits; filter 0.01 s |
| one pathspec per member instead | 116 paths 5.7 s; 1,326 paths > 120 s (stopped): so ONE walk + a filter, never a pathspec list |
| `nest.py log` on goal:g7.16.1.11 alone | 65 commits = `git log --first-parent --follow` 65; 4.5 s whole (graph load ~3 s) |
| a retired node (deprecated/build/GOALS.md.md) | plain path history 1, with rename following 14 |
| grid vs git, per node | g7.16.1.11: grid 37 versions, git 65 · card-alive: grid 208, git 142. Neither is a superset (grid ticks missed edits between ticks and versioned per post branch), so the frozen refs stay readable as the pre-cutover record |
| a `nest:` LIST for the g7.16.1.11 slice | 7,215 B in the container: an explicit list is for small arbitrary slices; a goal subtree uses `nest: subtree` (0 B per member) |
| unknown front-matter field | no reader rejects one (git grep over links.py, schema_registry.py, src/); [goal].md `required` does not name it |

## The reader whole (scratch `nest.py`, 2,415 B; build lifts it, python per the owner's "we can use python tests")
```python
#!/usr/bin/env python3
"""nest.py slice|log REV N: a slice is held IN its container's front matter (nest: subtree | a list of ids); no ref, no store (D1, post-grid)."""
import re, subprocess, sys
def git(*a, inp=None): return subprocess.run(("git",) + a, input=inp, capture_output=True, text=True, check=True).stdout
def fm(body):
    if not body.startswith("---"): return {}
    d, k = {}, None
    for l in body.split("\n---", 1)[0].split("\n")[1:]:
        m = re.match(r"^([a-z_]+):\s*(.*)$", l)
        if m: k = m.group(1); d[k] = m.group(2).strip().strip('"') or []
        elif k and re.match(r"^\s*- ", l) and isinstance(d[k], list): d[k].append(l.split("- ", 1)[1].strip().strip('"'))
    return d
def graph(rev):
    ps = [p for p in git("ls-tree", "-r", "--name-only", rev, "--", ".agi/nodes").split() if p.endswith(".md")]
    out = subprocess.run(("git", "cat-file", "--batch"), input="".join(f"{rev}:{p}\n" for p in ps).encode(), capture_output=True, check=True).stdout; nodes, i = {}, 0
    for p in ps:
        j = out.index(b"\n", i); n = int(out[i:j].split()[2]); d = fm(out[j + 1:j + 1 + n].decode("utf-8", "replace")); i = j + 2 + n
        if "id" in d: nodes[d["id"]] = (p, d)
    return nodes
def members(nodes, n, seen=None):
    seen = set() if seen is None else seen
    if n in seen or n not in nodes: return seen
    seen.add(n); spec = nodes[n][1].get("nest")
    if spec == "subtree": ms = [k for k, (_, d) in nodes.items() if n in (d.get("parents") or [])]
    else: ms = spec if isinstance(spec, list) else []
    for m in ms: members(nodes, m, seen)  # recursion: a member's own nest expands; a cycle stops at seen
    return seen
def log(rev, paths):
    walk = git("log", "--first-parent", "-M", "--name-status", "--format=@%H", rev, "--", ".agi/nodes")
    cur, hits, ps = None, [], set(paths)
    for l in walk.split("\n"):
        if l.startswith("@"): cur = l[1:]; continue
        f = l.split("\t")
        if len(f) < 2: continue
        if f[0].startswith("R") and f[2] in ps: ps.add(f[1])  # newest first: a retire move maps back to the old path
        if any(x in ps for x in f[1:]) and (not hits or hits[-1] != cur): hits.append(cur)
    return hits
if __name__ == "__main__":
    verb, rev, n = sys.argv[1:4]; nodes = graph(rev); s = members(nodes, n)
    if verb == "slice": print("\n".join(sorted(s)))
    else: print("\n".join(log(rev, [nodes[m][0] for m in s])))
```

## Tested 02:0xZ 10-08 (scratch `t_nest.py`, unittest, a throwaway repo per case; no live ref touched): 7/7 PASS
| # | case | result |
|---|---|---|
| N1 | a node with no `nest:` | its slice is itself |
| N2 | `nest: subtree` on goal:a (b under a, c under b) | a + b: a subtree is ONE level unless a member carries its own nest |
| N3 | b also `nest: subtree` | a + b + c (recursion) |
| N4 | doc:x lists doc:y + goal:c; doc:y lists doc:x | x + y + c: arbitrary types, the cycle stops |
| N5 | the collapse commit | names ONE path (the container); 0 new refs; 5 node files before and after |
| N6 | `log` of x after nesting y | x2, y1, x1: the container reaches every member's history |
| N7 | y retired to deprecated/doc/ after the collapse | retire y, x2, y1, x1: a retired member keeps its history |

## What it retires, what the build needs
- RETIRES: AA1.N's `nest()` recipe (552 B), its grid.py seams G1-G3 and their 11-line fix. **goal:g4.13.1 is grid.py work on a retiring store: recommend `retired` (DG1 owns goals; lane F is already cancelled for the same reason).**
- BUILD (one DG, python): `nest.py` under extensions/agi/bin/ + `t_nest.py` as a pytest file; links.py:772 adds `norm(fm.get("nest"))` to the resolved refs when it is a list, so a listed member that does not resolve counts as broken; each schema that allows it gains `nest: {type: str|list}` (optional, never required).
- D3 (all-is-one) rests on the grid ref today ("graphed here" from the ref's first-parent versions, "contains k" from `nest/` trees): both move to this surface, the node path's first-parent git history and `members()`. D3 restates; alive does not.
- D2 (self-perpetuating) decides WHICH containers get `nest:` at rollover; the tangle numbers in AA1.N stand.

## Honest limits
(1) `nest: subtree` reads the parents edges at the revision read, so the slice moves as nodes are added under N; an explicit list is fixed. (2) A member in a long-lived post branch that has not landed is not in the trunk walk until it lands (AA3). (3) The walk reads first-parent history: a post's own one-node commits show as the landing commit on the trunk, the post branch keeps the per-turn detail. (4) The reader's front-matter parser is the minimal one (top-level `key: value` and `- item` lists); the build may swap in the engine's parser. (5) Not run live: no container on the trunk carries `nest:` yet.

## Falsifiers (UNRUN live; each one command once built)
D1.1 a collapse commit on the trunk changes exactly one file under .agi/nodes (`git show --name-only --format= <sha>`) · D1.2 `links.py` count of active + deprecated nodes is identical one commit before and after a collapse · D1.3 `nest.py log` for a retired member equals `git log --first-parent --follow` for its path · D1.4 24 h after the cutover, refs/grid/* gains 0 refs and `nest.py` never reads one except the frozen pre-cutover record.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 9, 02:1xZ 10-08 (date -u): first version. belam's trajectory row E1 read "D1 NOT written"; it was written (AA1.N, 5a1760e82) but on refs/grid, which E2 retires. So D1 is restated onto the file + git history: the slice lives in the container's front matter, the collapse is one one-node commit, the history is one walk. Measured before designing: per-member pathspecs do not scale (1,326 paths > 120 s), one walk does (1.5 s). The recommendation to retire goal:g4.13.1 follows from lane F's cancellation, not from a new rule.
<!-- THOUGHT:END -->
