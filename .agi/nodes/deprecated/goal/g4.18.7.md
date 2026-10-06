---
id: goal:g4.18.7
mint_id: 5b1933433ae746768a7f2331b780104c
type: goal
parents:
  - goal:g4.18
  - goal:g2.19
next_edges: []
confidence: 0.75
edited_by: alive
goal_id: G4.18.7
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: deae8817eca8ca75
season: 2
seeds: []
status: deprecated
tags:
  - engine
  - render-path
  - write-path
  - owner
title: "G4.18.7: read leaves write.py -- one render path (viewport, goal:g2.19) reads a node for agents and humans; write.py writes and prints only its own diff"
town: core
---
# goal:g4.18.7

## OWNER 2026-09-29 18:0xZ, verbatim (Prime pane, relayed by belam-S2-L5-XVI to the council)
"Write shouldn't need a read path. We should only need a render path. Add it to bundle if needed I've been meaning to improve the way the graph is rendered for agents for a while. Unify everything into the correct slots. Read doesn't belong to write semantically im surprised the council didn't catch it"

## Why this exists
goal:g4.18: write.py is the one node WRITER, yet it carries the graph's most-taught READ verb. Measured 09-29 17:4xZ: `write.py:543` registers `"read": verb_read` in VERBS; `read body` / `read payload` appears in 21 tracked files under skills/, extensions/agi/ and CLAUDE.md, tests included (test_rotate_templates.py 12, test_write.py 7, rotate.py 4, agi-node-write SKILL.md 3); the TEACHERS (files that instruct a reader to read through write.py) are 8 files / 13 lines by director-general-1's measure at db3e22e55. Every agent read therefore enters the write tool, and its output is the writer's raw file slice, not a render.

goal:g2.19: "one render, two readers" already names the slot a read belongs in: `viewport.py --emit llm|human|both` draws one stream for an agent and a human. Measured: viewport.py takes `--anchor <id> --depth N` (a neighbourhood) but has no view of ONE node's body, rows or payload, so an agent has no render-path way to read what it was given. The owner has wanted better agent rendering "for a while": this is a first-class row, not cleanup.

## Target end-state
- write.py has NO read verb: `read body` / `read payload` leave VERBS; a write prints only its own diff (the `--dry-run` preview is part of the write).
- ONE render path reads a node for both readers: `viewport.py` (goal:g2.19) renders a single node (its resolved names and titles, its body by row or range, its payload) as `--emit llm` for an agent and `--emit human` for a person, from one stream.
- ONE cut, no alias: the row that drops `read` from VERBS is the SAME row that repoints every teaching file (8 files / 13 lines, director-general-1 at db3e22e55; the agi-node-write skill grammar included, so one source owns reading) and CLAUDE.md's "Read YOUR goal by id" line; there is never a window with two read paths.
- The agent render is designed for the agent: names never bare ids (goal:g4.18.6's resolution), rows addressable by the same index a write uses (goal:g4.18.5).

## Invariants
- The render path never gains a write (goal:g9: the viewport stays read-only, its self-grep test still passes).
- write.py never renders a node it is not writing.
- One render, two readers: `viewport.py --verify` exits 0.

## Falsifier
1. `python3 extensions/agi/bin/viewport.py --anchor goal:g4.18.7 --emit llm` (or the single-node flag it grows) prints this node's body, and `python3 extensions/agi/bin/viewport.py --verify` exits 0.
2. Negative: `git grep -n '"read":' -- extensions/agi/bin/write.py` = 0 hits, and `git grep -nE "write\.py [^ ]+ '?read (body|payload)" -- skills extensions/agi/bin CLAUDE.md` = 0 hits.

## Out of scope
goal:g4.18.5 (rows + a write is a commit: the renderer addresses rows by its index) · goal:g4.18.6 (mint-id links: the renderer's name resolution is shared with it) · goal:g4.18.3 · goal:g4.18.4 · goal:g4.19 (the intercept layer; its title routes Read through write.py, which this owner line reverses: the Prime's to re-word).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by alive (council) on the Prime belam-S2-L5-XVI [owner] relay (SendMessage, 18:0xZ 09-29): the third row of the write/render split, beside the Prime-minted goal:g4.18.5 + goal:g4.18.6; owner verbatim banked in the body section above. Second parent goal:g2.19 because the render path a read moves INTO is that goal (one render, two readers), not a new tool. Council lenses (17:5xZ) taken into the cut rule: all-is-one, drop read from VERBS in the SAME row that repoints the teaching files, no alias, never two read paths; self-perpetuating, the agi-node-write skill grammar moves in that row. THIS version (20:2xZ) corrects my own measurement: the earlier "23 teaching files" counted a WIDER scope than the text named (it included .agi/nodes/doc + .geometry: 21 in the named scope) and counted every mention, tests included, which assert the verb rather than teach it. The teachers are 8 files / 13 lines (director-general-1, db3e22e55); my strict write.py-invocation pattern finds 5 outside tests. The measurement time was also 17:4xZ, not 18:0xZ. goal:g4.19 (its title routes Read through write.py) is resolved in bundle 4 row W0 by retitle (director-general-1).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: deprecated old-engine Python goal; not carried. -->
