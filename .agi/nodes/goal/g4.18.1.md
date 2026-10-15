---
id: goal:g4.18.1
mint_id: 7f7a1727da744a33a38712c7c8b58f74
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.7
edited_by: director-general-2
goal_id: G4.18.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: deab01afeb1e7d97
season: 2
seeds: []
status: active
tags:
  - engine
  - write
thought_session: belam-S2-L5-XI
title: "G4.18.1: ONE MINT ROUTE -- the node and its raw file through one captive write flow, row by row, format-checked, stamped from the calling post; a storage picker; a location row renames the file (assigned: director-engine)"
town: core
---
# goal:g4.18.1

## OWNER 2026-09-26 ~23:2xZ (belam-S2-L5-X's pane; forwarded to the successor on the owner's go, 00:07Z 09-27), verbatim
"Another thing is that why do we write files and mint nodes separately. Why can't minting just use the write function one step at a time as a captive flow the models follow? Each row filled out and format checked. Heck have skills for each major engine function to explain how it works as stand in for future MCP that show how to chain the needed inputs but recommending doing it manually one at a time to avoid backtick and quote confusion errors. The mint uses the calling posts info to stamp info appropriately. Only needs a template showing where each major storage category is at and have the model pick from options listed during flow for things like extension code, template storage in .geometry, etc. and can add a custom path on top. The template pick in the flow just populates it into the pane verbatim and you can then emit the rest of the pathname before sending submit or just submit. Then also modifying an existing node with a new version could also use the same shared mint route as a brand new node with a fresh file. And each build node contains a reference to the location of its actual file. But basically mint is unified into a common route to both mint the node and the corresponding raw file, and write is used for both or at least the node part and raw file is just written to disk. Then the node automatically gains the file name as well, and the file can be renamed via a node write/mint by using the location row change. It just checks and confirms if you literally ask to move the file to a new location not just a rename."

## The predecessor's reading (the owner saw it before the go; the owner's words above win)
Most of the plumbing exists: `write.py create`'s spawn gate, `--payload` (links a source file, created if absent), `payload_ref` on build nodes, and a new version = an in-place edit + `grid.py commit`. So this is a new front door plus a location row. Five refinements:
- (a) a batch twin: the captive flow for models, one answers file for crons and scripts, the same validator behind both;
- (b) the storage picker is built from the config paths and the schemas, never a hand list;
- (c) the location row = the file path; the mint id never changes (G2.5); a rename is one commit (move + ref); a directory move asks first;
- (d) the per-function skills are generated from each script's argparse + schema, so they cannot drift;
- (e) the role templates that teach `create` / `--body-file` / `--set` change with it.

## Evidence (09-26)
- The predecessor had to drop the apostrophes from an owner quote to get it through `write.py`'s single-quoted script; this node's quote came in through `--body-file` for the same reason.
- The swarm parents struggled with node creation.

## Routing
assigned: director-engine. FIRST of the three graph redesigns (OWNER 01:0xZ 09-27, verbatim: "Would the mint write design be first? Um send pieces depend on it, and rotate depends on send"): the hub-only send is written through write.py, so it builds on this route; spawn/rotate (goal:g7.31.3.3) comes after send.

## Falsifier
1. `for i in 1 2 3 4 5; do grep -m1 '^status:' .agi/nodes/goal/g4.18.1.$i.md; done | grep -vc complete` prints 0: every leaf's own Falsifier has run green (.1 `test_write_answers_file.py` · .3 `test_storage_categories.py` · .2 .4 .5 the rows their builds commit).
2. Negative: `git grep -nE "\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|\"mint_id\": *mint_permanent_id" -- extensions/agi/bin extensions/agi/src | wc -l` prints 1: one mint route assigns ids (goal:g7.16.1.1.4; 4 before 5a828b3ce).
Run 13:1xZ 09-29 at 686531ce9 (director-general-2, bundle 2 R4, goal:g7.16.1.2.4): F1 prints `3` -- NOT met: g4.18.1.2 · .4 · .5 read active, each with its measured gap line; .1 · .3 complete. F2 prints `1` -- met: one mint route assigns ids.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Third version, director-general-3 (council bundle 1 row D, goal:g7.16.1.1.4): a Falsifier section added (the node had none) and RUN 09-29 on 0055d30a2. F1 prints 3, NOT MET: .1 and .3 are complete (their committed rows green), and .2 .4 .5 each hold one measured gap line. F2 prints 1, MET: assign-if-missing is one function (graph_core.identity.ensure_mint_id, 4 sites before 5a828b3ce). So the goal stays active, narrowed to three gap-only leaves. The prior version's routing (first of the three graph redesigns, owner 01:0xZ 09-27) is unchanged in the Routing section.
<!-- THOUGHT:END -->
