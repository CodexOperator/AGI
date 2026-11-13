---
id: fuel:s4-retire-the-python-engine
mint_id: 0d0a324a5d884474a6440728813c9682
type: fuel
parents:
  - goal:g5.4
next_edges: []
edited_by: meme-master
scale: big
status: open
season: 3
tags:
  - fuel
  - season-4
title: "FUEL for season 4 (owner 11-09): finish the move off Python. Measured: the live engine is ~1.2k lines of shell held in graph nodes, yet 16 live Python entry points still reach 84.5k of the 121k non-test Python lines by import"
---

## The owner's words 2026-11-09 19:38:57Z (c:12ed484271c7), verbatim (in meme-master's own session) [meme-master store; not an OWNER heading under the interim rule, sp 19:55:55Z 11-09: OWNER blocks cite belam's store only, until the cite leaf under .46 lands]
> "Yes let's do that it will be useful for season 4 anyway so we can add it into the 'fuel' node if you know where to find it so it can be included as a season 4 thingy. Like to finalize moving away from python code entirely and make it redundant by making the overall turn-based commit system even more robust and elegant."

## The owner's words 2026-11-09 19:39:39Z (c:7d8196eccf23) and 19:39:53Z (c:6f3adc806769), verbatim [meme-master store; not an OWNER heading under the interim rule, sp 19:55:55Z 11-09: OWNER blocks cite belam's store only, until the cite leaf under .46 lands]
> "you can make your own fuel node"
> "follow the schema or add one if there isn't one in .geometry"

Context: the owner had asked whether the ~104k "engine Python" lines on the 11-07 Atlas were stale, believing nearly everything is shell now.

## Measured (trunk e289cd776b + this post's turns, 2026-11-09; static, read-only)
```
LIVE SHELL ENGINE   ~1,170 lines in 6 nodes .agi/nodes/.geometry/engine*.md  ── sect ──▶ ~/bin (687 lines in one post's home)
                    agi-turn · agi-at · box · agi-pray · agi-meter · agi-out · agi-wt · ...
        │ calls
        ▼
LIVE PY ENTRY (16)  from ~/bin:  grow.py(home) → spawn_gate · send · grid · brief · anonymize · board_job
                    crons.md:    evidence_gate · crons · metrics_cell · memory_alarm · alarm_spool · prereq_notice · grid_stale · board_job
                    services:    rotate.py alarms (agi-alarms-sanctuary-master) · heal.py watch (agi-reaper)
        │ import (transitive, static)
        ▼
REACHED             77 files · 84,549 lines   of 168 files · 121,168 non-test lines
  + by a .py name in a string only (subprocess/message, ambiguous):  29 files · 20,702 lines
  unreached even by name (dead candidates):                          62 files · 15,917 lines
TESTS               ~194k Python lines (+ 96 shell lanes, ~18.5k) exercise all of it
```
- The hubs: `rotate.py` (23.8k lines) imports 23 engine modules, `heal.py` 15 (dispatch, sensei, cli, verification, node_writer, provisioning...). Both are kept loaded by the two always-on services above, and that is most of the 84.5k.
- Import reach is an UPPER bound on what must stay loadable, not what executes: a module-level import pulls a whole file for one function.
- `prime_merge.py` is named by a cron but absent from the tree (the cron guards with `test -f`).
- Largest unreached: src/agi_algos/graph_builder.py 2,830 · bin/graphweb.py 1,622 · bin/season_report.py 970 · bin/decompose-engine.py 564 · bin/snapshot-goals.py 500 · bin/snapshot-build-site.py 411 (the CLAUDE.md "paid-for" file).
- Method, to re-run: an AST walk of import/from-import/import_module over extensions/agi/{bin,bin/adapters,hooks,src} (tests excluded), seeded by the 16 entry points; the second pass also follows any `<name>.py` string. Script kept in meme-master's scratchpad, not committed; re-derivable from this description.

## Musing for season 4 (fuel, not a plan)
- The turn-end commit (agi-turn, shell) already made Python unnecessary on the hot path. What's left is a short list of jobs, not a codebase: growth-order check (spawn_gate), grid split (grid), mail (send), alarms (rotate alarms), reaping (heal watch), crons apply.
- Cut the two services first: each is one loop that needs a few functions, yet imports ~40 modules. A shell loop in an engine node per service would drop the reach from ~84k toward the dozen files the shell tools call directly.
- The 62 unreached files (15.9k lines) are a retire-never-delete sweep, a near-free first step that needs no rewrite.
- Elegance check, the owner's rule: every part should do several jobs. Then the turn-end commit should check the node as well as save it, and the cron that heals the graph should also be the cron that alarms, not two Python programs.
- For the presentation (doc:draft-presentation-outline, slide 7): the true line is "~1.2k lines of shell, stored in the graph, run the town; ~100k lines of older Python are being retired".

## The owner's words 2026-11-09 19:48:22Z (c:710151823175), verbatim [meme-master store; not an OWNER heading under the interim rule, sp 19:55:55Z 11-09: OWNER blocks cite belam's store only, until the cite leaf under .46 lands]
> "cool yeah that's still not terrible but we could do the whole engine in shell only I imagine and make it more robust that way by leaning on the math more instead. Maybe add that to the fuel node as well for now."

## Musing: the whole engine in shell, robust by leaning on the math (fuel, not a plan)
- Target: zero engine Python. Each remaining job becomes an invariant a short shell line can check, not a program that has to be right.
- What "the math" already gives us, measured in this node: a node is a file; its parents are edges; the grid is a content-addressed version per node. Checks over those are set and graph checks git already does well: every parent resolves (`git cat-file -e`), nothing new is parentless, `active + deprecated` never drops (a count), a tree hash equals a tree hash.
- So the growth-order check, the grid split and the alarms reduce to a few such invariants run at the turn end. Robustness comes from what an invariant cannot do: it cannot half-run, cannot drift from its spec, and is re-checked on every turn by agi-turn.
- Open question for the season: which of the 16 entry points is NOT an invariant check (mail transport? dispatch?), and what is its smallest shell form.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, meme-master gen 1: v1. The owner asked for the trace and a fuel entry for season 4, then said to mint this post's own fuel node following the schema. No [fuel] type exists in .agi/context/schemas or .geometry, and the existing fuel node (idea:fuel-dead-simple-patterns-in-plain-sight) is an idea, so this follows [idea].md (min 1 parent, goal/vision; grow cell [idea, doc, task] allows it). Minting a new [fuel] type would be an engine/RULES change for the council, not a post's mint. Parent goal:g5.4 (season review and rollover = where season 4 is bundled), not this post's leaf g5.4.3 (the presentation), because the finding outlives the talk. Near miss corrected in-session: my first answer to the owner said "about 13 of 97 files" are live, counting only direct calls. The import trace shows the two services pull 84.5k lines; the owner was told.
v2, same day: the owner's second ask added, the whole engine in shell, robust through the math. Placed as its own musing section, kept apart from the measured part, because it is a direction, not a finding.
v3, same day: the store came up (belam 4e346a04d5, "mem": "full"), so both owner quotes became OWNER headings citing their chunk ids (c:12ed484271c7, c:7d8196eccf23, c:6f3adc806769, c:710151823175), each verified speaker: owner in ~/.mem/meme-master.git. No other text changed.
Then, same day: OWNER headings turned back into plain headings (words and chunk ids kept) on the council's interim rule (self-perpetuating 19:55:55Z 11-09, via SM): verify-land runs agi-mem cite as belam, so an OWNER block citing a chunk in this post's store would HOLD every later OWNER-file land town-wide. They return to OWNER once the cite leaf under .46 lands.
v4, same day 22:4xZ: re-typed idea -> fuel on the land of the [fuel] schema (L485 4785261b05, belam's wrap 7f9432d579; the re-type was named mine, OUT of that lane). id idea:fuel-s4-retire-the-python-engine -> fuel:s4-retire-the-python-engine, path .agi/nodes/idea/ -> .agi/nodes/fuel/, type idea -> fuel; mint_id 0d0a324a5d884474a6440728813c9682 kept, every reference re-pointed in the same commit (only my card named it). Checked before the turn end: spawn_gate.check_spawn APPROVED against [fuel].md (goal parent, 1 of 1-2); the schema's body check from the repo top: 'fuel nodes read: 1', rc 0. fuel is not in my row's grow cell [idea, doc, task] (adding it is belam's cell, named OUT), so grow.py reports this add as [scope], never a refusal. No body text changed.
<!-- THOUGHT:END -->
