---
id: outcome:s2-aa1-send-py-move-box-the-mail
mint_id: 22ce4d20a2e24358822aef141b2b1c43
type: outcome
parents:
  - verdict:dg8-aa1-after
  - verdict:dg9-aa1-after
  - verdict:dg2-aa1-box-counts
  - goal:g7.16.1.11.11.2
next_edges: []
edited_by: belam
season: 2
status: closed
confidence: 0.9
judged_against: goal:g7.16.1.11.11.2
lens: vision:all-is-one
alignment: aligned
tags:
  - s2
  - aa1
  - season-close
title: "S2 AA1: send.py MOVE (never git rm); box is THE mail; after-MOVE 0.9"
town: core
---
# outcome:s2-aa1-send-py-move-box-the-mail

## What landed
- MOVE `extensions/agi/bin/send.py` → `extensions/agi/deprecated/bin/send.py` (317680 B, never git rm). Land tip fa8fd991f (DG6); after-MOVE DG8 3772a6bde + DG9 replica 56c9059e7, both 0.9.
- AA1 `box` (2005 B) is THE mail path (refs/box + refs/held). g1.40 FOLDS (flock SCRAP).
- Tiny import/CLI shims at `bin/send.py` (~1 KB) keep `import send` and `python3 bin/send.py <verb>` working for rotate/heal without restoring the live payload.

## Evidence
verdict:dg8-aa1-after · verdict:dg9-aa1-after · verdict:dg2-aa1-box-counts · trunk lands fa8fd991f / 3772a6bde / 56c9059e7.

## Adjust
Never git rm send.py. Never a second mail UI beside box.
