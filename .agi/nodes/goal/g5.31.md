---
id: goal:g5.31
mint_id: 64b9be63b2124da98b9d2abf2133a67f
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G5.31
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 187117de0913bd3b
season: 2
status: active
tags:
  - local-maxxing
  - comms
  - diagram-max
title: "G5.31: DIAGRAM-MAX + BATCH-MAX — every dm, note, card, board section and (where possible) thought stream on the town is ONE compact flow or table that carries MORE meaning in FEWER tokens than the prose it replaces, never dropping a negation, condition, attribution or supersession; directors batch-max (many rounds per order, one merge-up per batch)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.31
## Agent Notes
**Owner source (verbatim on goal:g14):** 01:57Z 09-21 (Prime pane): "Tell everyone else to diagram max as well to maximally compress all comms and card content/updates while retaining even more meaning than without doing the compression" · 02:1xZ 09-21 (thought-master pane): "break it out into a proper subgoal … including the standard format. Then refine the doc pass even more for yourself and the directors based on that format and tell both directors to sync theirs and refine even further to allow batch-maxxing for them as well. Do self-comms using diagram maxxing as well. And even thought stream if possible for all roles."
**Commits to.**
```
scope      every dm · note · card · board section · [merge-up] line · THOUGHT block · (if the harness allows) the thought stream itself — every role on local-maxxing
shape      ONE compact flow or table per message/section; prose ONLY where a diagram would drop meaning
keep       negations (NOT/never) · conditions (if/only when) · attributions (who said/measured) · supersessions (X supersedes Y) — always explicit
verbatim   owner text stays verbatim, in nodes (goal:g14 notes), never compressed
batch-max  a director's order carries MANY rounds; ONE [merge-up] per batch; a dm per round is a defect
target     fewer tokens AND more meaning than the prose replaced — measured, not felt
```
**Invariants.** A compressed artifact is checked against its source for the four shapes before it replaces it; owner verbatim is never rewritten; a card stays ≤ 40 lines with state on `doc:lm-town-trajectory` (versions, not notes); the trajectory node's metric table is the model of the shape.
**Falsifiers.** (a) A diagram-maxed card/dm loses a fact its source held (found by a reader or a mur) → it is not done; the fact is restored and the shape revised. (b) Token count of the compressed artifact is not below the prose it replaced (measured with the same tokenizer) → not compression. (c) A director's turn count per landed round does not fall after batch-maxxing → the batching is nominal.
**Done when.** All three cards and both role briefs are in the shape with measured token reduction (a before/after table on this node); every [merge-up] and board update of one full week is in the shape; one measured batch (≥ 3 rounds per order) landed with one merge-up.
**First chunk (the master, no spend):** the card pass — thought-master card §4+ (done 02:0xZ), director-thought + director-engine cards synced to the shape (TMM.20 / TME.05), before/after line counts on this node; then G5.31.1 (director-engine, same format): the measurement round — a tokenizer count of each card/brief before and after, the four-shape checklist as a committed script, run as one pi round.

thought-master 02:2xZ 09-21 card pass, measured: thought-master card 97 lines (09-20) -> 93 (§4 in the shape, 02:1xZ) -> 54 lines (§0-§3 in the shape, 02:2xZ); facts kept: every NEVER, both recorded exceptions, GATE 0 / ROUND 0 status, cadence, floor, alerts, prayers rule; owner quotes moved out of the card into their nodes (goal:g14, doc:l4-owner-decisions) rather than compressed. Directors' before/after arrive as their own notes here.

director-engine 02:11Z 09-21 (via thought-master, verified dm): card diagram-max 2bd43c299 -> e4cc6aca3 = lines 33 -> 37 (+4: the table shape costs rows) · words 1063 -> 959 (-9.8 pct) · chars 7541 -> 6741 (-10.6 pct); its own flag: line count is a weak proxy for the shape -- words/chars are the measure, adopted for this goal's before/after table.

thought-master 02:1xZ 09-21 (owner via the Prime, goal:g14 L240: diagram-max ALL spawn-in context docs -- card, brief, standing instructions): ADD G5.31.2 THE BRIEF PASS (director-engine, after G5.31.1): doc:unified-director-brief (94 lines prose; §4 'thought' still names season1 paths) + doc:lm-director-brief-customizations rewritten into the shape by a KID, a parent verifies the four shapes against the source line by line, tokens measured before/after; stale facts corrected from the cards/box doc, never invented. NOT by a master's hand: a rule doc every director spawns with is exactly what a round with a reviewer is for.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.31 → g5.31 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
