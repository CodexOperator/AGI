---
id: outcome:g7-16-1-11-3-5-live-posts-boot-under-8k
mint_id: c24029e7980c4288b04fe0b09a3e1fd4
type: outcome
parents:
  - goal:g7.16.1.11.3
  - goal:g7.16.1.11.5
next_edges: []
adjust: "name an owning leaf for the 15 parity rows not live (3 short: 18 30 33; 12 not run)"
alignment: adjust
confidence: 0.75
edited_by: sanctuary-master
judged_against: goal:g7.16.1.11.5
lens: goal:g7.16.1.11
model: claude-opus-5-5
role: director
scaffold_hash: 5c4301ed9348c733
season: 2
status: closed
title: OUTCOME goal:g7.16.1.11.3 + .5 -- the new engine runs live posts and boots from 7,649 fenced bytes, under the owner's 8 KiB bar
town: core
---
# outcome:g7-16-1-11-3-5-live-posts-boot-under-8k

# OUTCOME goal:g7.16.1.11.3 + goal:g7.16.1.11.5 -- the new engine runs live posts and boots from 7,649 fenced bytes, under the owner's 8 KiB bar

## Outcome
.3 (stages 1-2.5, director-general-3, complete 10-10): S1 PASS, S2 PASS 7/7, DG5 live on pi-free. .5 (round 5, director-general-3 + DG1, complete 10-10 09:1xZ): the bootstrap fits the owner's bar "the bootstrap package is under 8kb". belam's ruling R' (08:4xZ 10-10) reads that bar as the FENCED bytes of engine.md, the code that boots.

| claim | bytes on trunk fd54ab759b (sanctuary-master, 02:5xZ 10-11) | verdict |
|---|---|---|
| bootstrap <= 8,192 B | engine-sizes.t.sh b5: 7,649 fenced bytes in 12 balanced fences, 543 B left (whole file 9,109 B, not asserted). At close it was 7,582 B (610 left): 67 B spent since close | holds |
| one counting rule | b5 counts BYTES (LC_ALL=C), not characters. DG1's 8,099 draft was a character count; DG2 caught it (lane 44d423b0e2) | holds |
| a live post on the new engine | S1/S2 PASS per the goal; all 11 posts restarted on the agi-post@ unit and carry AGI_POST (belam 02:39-02:48Z 10-11) | holds |
| parity with the old engine | 55 rows: 40 matched-or-better LIVE, 3 named short (18, 30, 33), 12 not run. The 52/55 was the plan figure (SM mur RI1, 10-07) | ADJUST |

## What stayed open
The 15 parity rows that are not live (3 short + 12 not run) have no owning leaf. g1.43 row 9 records the .5 title's 20,480 B total clause as disclosed, not asserted.
