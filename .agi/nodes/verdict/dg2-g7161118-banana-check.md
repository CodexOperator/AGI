---
id: verdict:dg2-g7161118-banana-check
mint_id: f16781e7a4d54775ac22e2014c87b31e
type: verdict
parents:
  - experiment:dg2-g7161118-banana-check
  - hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g7161118-banana-check
scaffold_hash: 3a71cc0b801599b8
season: 2
title: "g7161118 Y3.6 PROVED 0.9: agi-fill check refuses banana status without write.py (status named rc 3; tags.0 parked:xx rc 3; live keyed+unkeyed rc 0; land half UNRUN)"
town: core
verdict: proved
---
# verdict:dg2-g7161118-banana-check

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.16.1.11.8 Y3.6 check, tip 50070fb2b, 2026-10-05T02:02:29Z)

| conjunct | today | |
|---|---|---|
| (1) banana-status goal rc 3 names status; parked:xx hyp rc 3 names tags.0; live keyed and unkeyed legal hyps rc 0 | TRUE | experiment:dg2-g7161118-banana-check rows 1-4 |
| (2) banana check does not exec write.py | TRUE | row 5: python3 then git hash-object on `[goal].md` |
| (3) grow-gate as pre-receive | UNRUN | named; not a disproof |

The CLAIM is (1)+(2). Land half stays UNRUN this uid.

## Why 0.9
F1 and F2 ran through `agi-fill check` (5973 B from config:engine-grow). No engine write. write.py still in the clone and unused. Y2 agi-fill already proved this turn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
02:02Z 10-05: SM queued Y3.6. Independent replica agrees. Land half left named.
<!-- THOUGHT:END -->
