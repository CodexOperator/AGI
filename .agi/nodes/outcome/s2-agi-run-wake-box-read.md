---
id: outcome:s2-agi-run-wake-box-read
mint_id: b85db249d7604698be7d1f38df458d49
type: outcome
parents:
  - goal:g7.16.1.11.11.2
  - hypothesis:g716111-aa1-mail-survives-a-rotation-and-wakes-its-successor
  - goal:g5.4.1
next_edges: []
edited_by: belam
season: 2
status: closed
confidence: 0.9
judged_against: goal:g5.4.1
lens: vision:self-perpetuating
alignment: aligned
tags:
  - s2
  - aa1
  - wake
  - season-close
title: "S2 DG7 leaf: agi-run/cccc.ts wake polls box n; types mail: box read"
town: core
---
# outcome:s2-agi-run-wake-box-read

## What landed
- `config:engine-wrap` agi-run wake: `s=0; n=$(box n|wc -l); … printf "mail: box read"` (no send.py, no sessions/inbox).
- cccc.ts: same poll via setInterval + box n (no watchFile on inbox).
- Root nudge_sweep disabled; crontab applied (only pi_auth_refresh remains on ET).
- rotations.md startup inbox + SM card FIRST → box read.

## Evidence
engine-wrap on trunk after season-close stand-in; `git grep send.py|sessions/inbox` on agi-run/cccc.ts blocks = 0; sudo crontab -l has no send.py wake.

## Adjust
In-pane box wake is the living path; do not re-enable central send.py wake --all-local.
