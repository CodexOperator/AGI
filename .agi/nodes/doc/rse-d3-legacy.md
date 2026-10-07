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
title: "D3: 'legacy' is DERIVED from a node's grid ref, never a hand-set field; the renderer shows what a node CONTAINS (council design, all-is-one)"
town: core
---
# doc:rse-d3-legacy

Owner 10-07 14:3xZ (via belam [owner], verbatim on town:local-maxxing): "I was thinking if we let build nodes carry across it would be almost the same as if we had to use this engine in a brand new project someone else built that isn't graph based. Wed have to have some way to truthfully mark it as "legacy" or something so we know it's not been graphed yet but it is in the graph now. For our own nodes it would be "legacy" as well but the renderer should make it clear that those DO contain other nodes inside the node grid ref branch so it is not just plopped in it is fully integrated."
Split (alive 14:40Z): D3 = all-is-one. It rests on alive's D1 (AA1.N `nest()`: a collapse = ONE grid commit on the container, tree + `nest/<mint>`, members keep their refs) and on self-perpetuating's D2 (which rollover collapse). Design only.

## The rule: a mark the bytes decide
"Truthfully" rules out a frontmatter field: a field is asserted, can be set wrong, and goes stale the moment someone graphs the node. So `legacy` is COMPUTED from the node's grid ref `refs/grid/<town>/node/<mint>` (the live grid is town-scoped, alive AA1.N), from two facts that are already written there:
- **graphed here** = a first-parent version ABOVE the node's latest ENTRY names a `goal:` parent. grid.py already writes every version's parents into its commit body (`Parent-Mint-Id: <mint> <parent id>`, goal:g2.7), and a build node versioned through the graph has the `[build, goal]` shape (CLAUDE.md, goal:s29). An ENTRY = how the node came into this season: its first version (a scan or an import mints it), a `nest ` commit (D1's collapse), or a `carry ` commit (D2's rollover, if it carries a node without collapsing anything into it).
- **contains k** = the `nest/<mint>` trees in the ref's tip tree, at any depth (D1 nests recursively).

| mark | when | reads as |
|---|---|---|
| `[legacy]` | k = 0, nothing graphed since the entry | in the graph, not graphed yet (a scanned or imported file) |
| `[legacy ⊃k]` | k > 0, nothing graphed since the entry | ours, carried across: contains k nodes in its own grid ref, not touched since |
| `[⊃k]` | k > 0, graphed since | contains k nodes AND has been worked on here: fully integrated |
| (none) | k = 0, graphed | an ordinary node |

The `⊃k` IS the owner's "not just plopped in": the count is read off real nested trees in the node's own ref, and those trees reach every member's whole history (D1's parents). A member's own later work never clears its container's mark: the walk is first-parent, so only the container's own line counts.

The recipe (one shell function over git, no new store, no new ref; `text` because AA3.9's extract runs every `sh` block after it):
```text
legacy(){ k=$(git ls-tree -r -d --name-only $1|grep -cE '(^|/)nest/[^/]+$');g=0
 for c in $(git rev-list --first-parent $1);do s=$(git log -1 --format=%s $c);case $s in "nest "*|"carry "*)break;;esac
  git log -1 --format=%b $c|grep -q '^Parent-Mint-Id: [^ ]* goal:'&&{ g=1;break;};done
 [ $g = 1 ]&&m=||m=legacy;[ $k -gt 0 ]&&m="${m:+$m }⊃$k";echo "${m:--}";}
```

## Measured (all-is-one, 10-07 14:5xZ)
- **Today's trunk (51a56f858), every build node (297):** 256 `legacy`, 41 graphed. Of the 261 with `origin: build-scan` (the scanner brought the engine's own files in, one mvp per subsystem), 245 are legacy and 16 graphed; the flat files agree exactly (the same 16 list a `goal:` parent). So the owner's "a project that isn't graph based" is already most of our own build layer, and the rule needs no new data to say so.
- **Scratch cases (6/6):** scanned, never graphed -> `legacy`; a version whose only parent is its mvp -> `legacy`; a version made by a goal -> none; a container after `nest 2` -> `legacy ⊃2`, with a member's own goal-made version NOT clearing it; one goal-made version on the container, `nest/` carried forward -> `⊃2`; the same with today's grid.py -> none (G1 below).
- **Cost:** 24 s for the 297 (about 82 ms a node: one forked `git log` per version walked). Too slow for a per-frame viewport, and it need not be: the mark depends ONLY on the ref's tip, so it is cached by tip sha and recomputed when a ref moves (grid_sync already knows which refs it moved).

## What D3 needs from D1 (found while testing; sent to alive 15:0xZ)
- **G1 grid.py drops `nest/` on the next tick.** `commit_file` compares `build_tree` (node.md [+ payload], grid.py:802) with the WHOLE tip tree (grid.py:880). A collapsed tip carries `nest/`, so it always reads changed, and `grid.py commit --all` (grid_sync, every 5 min) writes a version WITHOUT it, even with no edit. Measured with the real `commit_file`. The members stay reachable through history, but the tip no longer shows them, so `⊃k` would read 0. Fix (Python, this season): `build_tree` carries the tip's `nest` entry forward unchanged.
- **G2 the version number jumps.** `n = rev-list --count tip + 1` follows every parent: nest 2 members of 2 versions each into a 2-version node and the next version is v8, not v4. Every version count (commit_file, `grid.py versions|log`) reads `--first-parent`.

## The renderer
- viewport.py builds every node line in one place (`{glyph} {tag} {title}{town_mark}{v}...`, viewport.py:327); the mark is one more suffix beside `town_mark`, from the tip-sha cache. Terminal and `--emit llm` print the same string, so goal:g2.19's `viewport.py --verify` (one render, two readers) covers it.
- Opening a `⊃k` node lists its members from their nested `node.md` blobs (`git show <tip>:nest/<mint>/node.md`, two levels like D1's recursion test), so a reader sees WHAT it contains, not only how many.
- A non-graph project needs no new importer: the scanner that minted our 261 (`origin: build-scan`, one `mvp:` per subsystem from a data map) runs on the foreign tree with that project's own map; every file arrives `[legacy]` and stops being legacy the first time a goal versions it.

## Falsifiers
- **L1** on the trunk the rule and the flat parents agree on every scanned build node (today 245 legacy / 16 graphed, 0 disagreeing).
- **L2** a scratch `nest` of k members reads `legacy ⊃k`; one goal-made version on the container reads `⊃k`, and stays `⊃k` across a `grid.py commit --all` with no edit. MEASURED 15:0xZ with the real `commit_file`: today's grid.py FAILS (unedited tick writes v5 and the mark falls to `legacy`, members gone from the tip); with alive's AA1.N patch (5cc55defa, G1 + G2 + G3) PASSES: after nest `legacy ⊃2` · unedited tick = no version, `legacy ⊃2` · goal-made edit = v3, `⊃2` · unedited tick after = no version, `⊃2`.
- **L3** `viewport.py --verify` passes with the mark on, and both readers print it byte-for-byte.

## Settled by the owners of D1 and D2 (15:0xZ)
- D1 (alive, AA1.N 5cc55defa): the grid.py patch carries `nest/` forward, versions by `--first-parent`, and writes the ref with CAS (alive's G3: a tick that read the tip before a collapse overwrote it). Still for its build: a CAS refusal skips the node, not the whole `--all` run; the other `--count` readers.
- D2 (self-perpetuating, §AC step 4 of its merge-up 16 re-cut 8ad18f230): YES, each carried node gets ONE grid commit on its own ref, same tree, subject `carry s2->s3`, written by grid.py (never a rollover script); a node that also receives a `nest ` commit gets no separate carry. Its falsifier AC.7 (every live carried node at the s3 tip has exactly one carry or nest commit newer than its last goal-made version) is the same boundary this rule reads.
