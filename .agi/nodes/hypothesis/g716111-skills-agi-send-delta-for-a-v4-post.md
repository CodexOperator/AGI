---
id: hypothesis:g716111-skills-agi-send-delta-for-a-v4-post
mint_id: 24ca29a66768498ebe62948fe5e94e02
type: hypothesis
parents:
  - goal:g7.16.1.11.14
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 6db3bac126f7e063
season: 2
testable_claim: "After the boxes build, the agi-send text a v4 post loads has no send.py, nudge, lastread or whois steps; sections 1-3 are `box send <post> <body-file`, `box read`, `box n` (the harmless peek), the refs as the state, and the Prime tag grammar unchanged; it is a delta table, not a second skill."
title: "Skills: agi-send for an engine.v4 post says `box send/read/n`, drops whois / wake / nudge / read-marker traps, and keeps the tag grammar to the Prime"
town: core
---
# hypothesis:g716111-skills-agi-send-delta-for-a-v4-post

## Measured
- doc:rse-aa1-boxes AA1.S table: today a v4 uid cannot send (inbox files belam:belam 664) and read re-prints everything (marker unwritable); after boxes `box n` is the harmless peek so the peek trap is gone, the address is the POST and the identity is the signature.

## CLAIM
After the boxes build, the agi-send text a v4 post loads has no send.py, nudge, lastread or whois steps; sections 1-3 are `box send <post> <body-file`, `box read`, `box n` (the harmless peek), the refs as the state, and the Prime tag grammar unchanged; it is a delta table, not a second skill.

## Dispatch line
config-max: none / template-max: the skill's v4 delta table / code: none.

## FALSIFIERS
the v4 skill text contains none of `send.py`, `nudge`, `lastread`, `whois`, `.nudge.pending` (git grep = 0) and names `box send`, `box read`, `box n`.

## TESTS
a grep test over the skill file; the old-setup skill text unchanged.

## FILE SCOPE
skills/agi-send (a v4 delta file or load exclusion) · no code. HORIZON behind goal:g7.16.1.11.11's build.

## CEILING
1 parent · kids <= 1 · a delta <= the table in doc:rse-aa1-boxes AA1.S.
