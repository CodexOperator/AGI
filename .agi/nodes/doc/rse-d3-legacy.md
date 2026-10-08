---
id: doc:rse-d3-legacy
mint_id: 634ffbebdd714bd59847c61f9d3c09eb
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: director
season: 2
tags:
  - council
  - design
  - g7.16.1.11
  - d3
title: "D3: 'legacy' is DERIVED from a node file's own git history, never a hand-set field; the renderer shows what a node CONTAINS (council design, all-is-one)"
town: core
---
# doc:rse-d3-legacy

Owner 10-07 14:3xZ (via belam [owner], verbatim on town:local-maxxing): "I was thinking if we let build nodes carry across it would be almost the same as if we had to use this engine in a brand new project someone else built that isn't graph based. Wed have to have some way to truthfully mark it as "legacy" or something so we know it's not been graphed yet but it is in the graph now. For our own nodes it would be "legacy" as well but the renderer should make it clear that those DO contain other nodes inside the node grid ref branch so it is not just plopped in it is fully integrated."
Owner 01:5xZ 10-08 (belam [rule] 02:02Z): "Finish encapsulation of grid slices and do a season rollover after getting you on the new engine." Grid commit retires (E2; owner 01:4xZ: "It's already decided"): history = `git log -- <path>`.
Split (alive 14:40Z 10-07): D3 = all-is-one. It rests on D1 (alive, restated off the grid as doc:rse-d1-nest: a container holds its slice in its front matter, `nest: subtree` | a list; `members(N)`; one git walk) and on D2 (self-perpetuating, §AC of its merge-up 18 7b8098104: which containers get `nest:` at rollover; carry = the `season:` cell). Design only.

## The rule: a mark the bytes decide (v2, off the grid)
"Truthfully" rules out a frontmatter field: a field is asserted, can be set wrong, and goes stale the moment someone graphs the node. So `legacy` is COMPUTED from two facts the node already has, read from the node FILE's own first-parent git history (renames followed, so a retire move to deprecated/<type>/ keeps it):
- **ENTRY** = how the node came into this season, the NEWEST of: the path's first commit · the commit that ADDS `nest:` (D1's collapse) · the commit after which `season:` equals the current season (D2's carry: ONE one-node commit that SETS `season:` to the new season, adding the cell when absent; settled with self-perpetuating 02:1xZ).
- **graphed here** = a commit ABOVE the entry after which the node's `parents:` GAIN a `goal:` id absent at the entry; or, when the entry is the first commit, the node was minted with a `goal:` parent (`[goal, mvp]` / `[build, goal]`, CLAUDE.md goal:s29). "Gain", not "includes": a carried build node keeps its season-2 goal parent, so "parents include a goal" would read its first unrelated edit in season 3 as graphed.
- **contains k** = `|members(N)| - 1` from D1's `members()` (D1 v2: `nest: subtree` descends through the container's descendants until one carries its own `nest:`, which expands itself; a list names arbitrary ids; a retired member still counts, it is still a file).

| mark | when | reads as |
|---|---|---|
| `[legacy]` | k = 0, not graphed since the entry | in the graph, not graphed yet (a scanned or imported file; a carried node untouched since) |
| `[legacy ⊃k]` | k > 0, not graphed since the entry | ours, collapsed or carried: contains k nodes, not worked on since |
| `[⊃k]` | k > 0, graphed since | contains k nodes AND worked on here: fully integrated |
| (none) | k = 0, graphed | an ordinary node |

The `⊃k` IS the owner's "not just plopped in": it is read off the container's own `nest:` cell and D1's walk reaches every member's whole history. A member's own later work never clears its container's mark: the rule reads only the container's file.

The rule whole (python, the season-2 tools' language per the owner; 703 B; fixtures `legacy_git.py`, `t_d3.py`, alive's `nest.py`):
```python
def mark(rev, season, path):
    vs = versions(rev, path)  # [(commit, path at that commit)] oldest first: git log --first-parent --follow -M --name-status
    if not vs: return "?"
    fms = [fm(git("show", f"{c}:{p}")) for c, p in vs]
    e = 0
    for i in range(1, len(vs)):
        if fms[i].get("nest") and not fms[i-1].get("nest"): e = i
        if str(fms[i].get("season")) == season and str(fms[i-1].get("season")) != season: e = i
    goals = lambda d: {x for x in (d.get("parents") or []) if isinstance(d.get("parents"), list) and x.startswith("goal:")}
    g0 = goals(fms[e])
    if e == 0 and g0: return "-"  # minted THROUGH a goal: graphed from its first commit
    return "-" if any(goals(fms[i]) - g0 for i in range(e+1, len(vs))) else "legacy"
```

## Measured (all-is-one, 10-08 02:1xZ, local trunk, read-only)
- **Every build node (297), season 2:** 256 `legacy`, 41 graphed, and node for node IDENTICAL to v1's grid-ref rule (0 of 297 disagree). So moving off the grid changes no mark. Of the 261 with `origin: build-scan` (the scanner brought the engine's own files in, one mvp per subsystem), 245 are legacy: the owner's "a project that isn't graph based" is already most of our own build layer.
- **The first cut was wrong, and the measurement caught it:** without the minted-through-a-goal case the rule read 279 / 18; the 23 extra "legacy" were nodes born with a goal parent, which never GAIN one.
- **Scratch cases 11/11** (`t_d3.py`, a throwaway repo, alive's `nest.py` members() extracted byte for byte from D1 v2, alive/d1-nest 43755c0227, where `nest: subtree` DESCENDS through members without their own `nest:` and stops, inclusive, at one that has it): scanned, never graphed -> `legacy` · a commit gains goal:g9 -> none · minted through a goal -> none · carried (season -> 3) keeping goal:g9 -> `legacy` · an unrelated edit after the carry -> `legacy` · a season-3 goal gained -> none · a container gets `nest: subtree` over 2 children -> `legacy ⊃2` · it then gains a goal -> `⊃2` · a member retired to deprecated/ -> still `⊃2` · a grandchild under a child -> `⊃3` (the subtree descends) · that child then carries its own `nest:` list of one -> `⊃3` (the descent stops at it; it expands its own list instead).
- **Cost:** 80 s for the 297 (one `git log --follow` + one `git show` per version per node). Too slow per frame, and it need not be: the mark depends only on the commits touching the node's path, so it is cached by the path's last commit sha and recomputed when that moves; one D1-style walk over .agi/nodes (alive: 5,826 first-parent commits, 1.5 s) yields every moved path at once.

## The renderer
- viewport.py builds every node line in one place (`{glyph} {tag} {title}{town_mark}{v}...`, viewport.py:327); the mark is one more suffix beside `town_mark`, from the cache. Terminal and `--emit llm` print the same string, so goal:g2.19's `viewport.py --verify` (one render, two readers) covers it.
- Opening a `⊃k` node lists its members (`nest.py slice`, D1), retired ones included and marked retired, so a reader sees WHAT it contains, not only how many.
- A non-graph project needs no new importer: the scanner that minted our 261 (`origin: build-scan`, one `mvp:` per subsystem from a data map) runs on the foreign tree with that project's own map; every file arrives `[legacy]` and stops being legacy the first commit a goal is gained.

## Falsifiers
- **L1** on the trunk the rule reads the same mark as v1's grid-ref rule for every build node with a grid ref (today 297/297; the frozen refs stay readable).
- **L2** at the s3 tip, every live node D2 nested or carried reads `legacy` or `legacy ⊃k` until a goal is gained (= self-perpetuating's AC.7 read from the other side).
- **L3** `viewport.py --verify` passes with the mark on, and both readers print it byte-for-byte.

## Retired by v2
- v1's grid-ref rule (`legacy()` over refs/grid/<town>/node/<mint>, the Parent-Mint-Id trailer, `nest `/`carry ` commit subjects) and its dependence on alive's grid.py fixes G1-G3: grid commit retires (E2), so nothing here writes or reads a grid ref for the current season.
