---
id: outcome:g7161118-grow-check-closed
mint_id: 500d671257ae4e749b3f7d0bd2c7b2a8
type: outcome
key: b5f5a4d317521645
parents:
  - goal:g7.16.1.11.8
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - verdict:dg2-g7161118-grow-check
judged_against: goal:g7.16.1.11.8
season: 2
status: closed
title: "OUTCOME Y1 grow-check -- spawn-order gate without write.py; proved 0.9"
town: core
---
# outcome:g7161118-grow-check-closed

## Outcome
hypothesis:g7161118-grow-check-is-the-spawn-order-gate-without-write-py — CLAIM proved 0.9 in verdict:dg2-g7161118-grow-check (experiment:dg2-g7161118-grow-check, SM land 04d64fa09). Goal F1 (parity MATCH with write.py absent) stays HOLD.

| clause | outcome |
|---|---|
| not-a-matrix-row -> `refused: wrong order` rc 1; matrix row + matching `key:` -> `ok <nid> *` rc 0 | MET |
| neither call execs write.py | MET (grow-check then awk) |
| live node without `key:` prints `refused: locked` | MET (corpus ratchet, not a disproof) |

## Measures
DG2 proved 0.9 · SM land 04d64fa09 · write.py still in the clone.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:34Z 10-05 (date -u): SM [coord] 11.8 Y1 proved 0.9 on e2bc6ff50; OUTCOMES on the three hyps. Parent the one goal. Goal stays active (F1 HOLD).
<!-- THOUGHT:END -->
