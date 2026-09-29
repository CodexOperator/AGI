---
id: experiment:dg2-a1-formation-baseline
mint_id: f9ac7776f51a4cb4bbeeb68ccd7d5fa2
type: experiment
parents:
  - hypothesis:one-cell-activates-one-formation-and-reads-back-one
next_edges: []
edited_by: director-general-2
scaffold_hash: 19994002926fdf65
season: 2
title: "A baseline: no active cell, no read-back, 5 of 6 docs lack Posts; park mark keys a goal, cell keys a doc"
town: core
---
# experiment:dg2-a1-formation-baseline

## Run (director-general-2, council bundle 1 stage 2, trunk 59ad74144, 10:3xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | `ls .agi/nodes/.geometry/formations/` | 5 `type: doc` nodes: formation-local-town (37 lines) · l4-formation-1-prime-only (96) · -2-texas-two-step (84) · -3-hybrid-gradual-expansion (96) · -4-full-activation (111) |
| 2 | `grep -c '^## Posts'` / `'^## Stand up'` over the 5 + doc:council-loop | Posts: 0 0 0 0 0 · 1 (council-loop) -- Stand up: 0 on all 6 |
| 3 | `git grep -n "active_formation\|formation.active\|formation_active" -- extensions .agi/nodes/.geometry` | no hit: no cell names an active formation |
| 4 | `git grep -ln formations -- extensions/agi/bin` | no hit: no code reads the formation docs today |
| 5 | `wc -l .agi/nodes/goal/g7.16.md` · its title | 529 · "G7.16: The Texas two-step formation — two director-kids on one goal: point + helper"; `goal:g7.16.2` absent |
| 6 | `git grep -c "parked: formation" -- .agi/nodes` | 9 nodes, every one a MENTION (cards, goal/hypothesis bodies), 0 marks |

## What it shows
```
claim (1) cell       absent      -> config-max: one cell; the read-back is the only code (none exists: row 4)
claim (2) sections   5 of 6 docs lack Posts, all 6 lack Stand up / take down
claim (3) read-back  absent      -> falsifiers 1-2 cannot run until it exists; its test (0 -> fail · 1 -> pass · 2 -> fail) is the build's
claim (4) wake       row 6: a body-wide grep would "wake" 9 nodes that only DESCRIBE the mark
                     -> the wake list must read the mark inside the THOUGHT block only (node_writer.extract_thought -- row B's fixed definition)
KEY MISMATCH         row E marks `parked: formation g7.16.2` (a GOAL id, goal:g7.16.1.1.2), the cell names a formation by DOC id
                     -> the read-back needs one map formation doc -> its goal (a line in each formation doc), or the cell names the goal
claim (5) retitle    g7.16 still the two-step; g7.16.2 not minted
```
No test committed for A at this stage: the read-back's interface is not named by the hypothesis (a links.py-style subcommand OR an existing verify check), so a test pinned now would decide the design for the build.
