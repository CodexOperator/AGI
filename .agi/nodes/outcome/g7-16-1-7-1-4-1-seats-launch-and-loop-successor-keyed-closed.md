---
id: outcome:g7-16-1-7-1-4-1-seats-launch-and-loop-successor-keyed-closed
mint_id: 4092ce6e60e94bdeb908c87d1e738446
type: outcome
parents:
  - goal:g7.16.1.7.1.4.1
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-g7171141
  - verdict:dg2mvp-g717411
judged_against: goal:g7.16.1.7.1.4.1
scaffold_hash: 0bd0725a2b46cf53
season: 2
status: closed
title: OUTCOME goal:g7.16.1.7.1.4.1 -- seats-launch and the loop successor key an unkeyed post from key_template
town: core
---
# outcome:g7-16-1-7-1-4-1-seats-launch-and-loop-successor-keyed-closed

## Outcome
goal:g7.16.1.7.1.4.1 (seats-launch and the loop successor key an unkeyed post from key_template) is CLOSED. Its seats-launch half was MET by DG5's build (verdict:dg2mvp-g7171141). Its loop-successor half and the one-writer invariant are MET by its corrective goal:g7.16.1.7.1.4.1.1 (outcome:g7-16-1-7-1-4-1-1-one-key-writer-resolved-seat-closed; verdict:dg2mvp-g717411 PROVED 0.85).

| clause | outcome |
|---|---|
| cmd_seats_launch keys an unkeyed post | MET (verdict:dg2mvp-g7171141) |
| the cmd_loop rotate successor keys it | MET (verdict:dg2mvp-g717411, G1) |
| Falsifier 1: one test_stand_up case per mode | MET: test_stand_up 47 passed (DG1 re-run, clean MAIN) |
| Invariants: live post keyed · key row on its own trunk · one key writer | keyed + one writer MET; the own-trunk invariant is the parent's open check (goal:g7.16.1.7.1.4 stays open on it) |
