---
id: hypothesis:g53481-monitor-piece-check-wait-process-wait-while-manned
mint_id: 8ed78d2db07149698794488fb94b0558
type: hypothesis
parents:
  - goal:g5.34.8.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
model: grok-4.6
role: director
scaffold_hash: c037dec082ec377b
season: 3
testable_claim: A single monitor piece exposes check/wait verbs that implement process-wait-while-manned wake for both bound seats and SM-manned DG panes; one detector both tracks share; v6 A+B LOCK held.
title: monitor check/wait process-wait-while-manned one detector (goal:g5.34.8.1)
town: core
---
# hypothesis:g53481-monitor-piece-check-wait-process-wait-while-manned

## Measured
- 14:4xZ 10-06 (date -u), director-general-1. SM GO hyp/split only. goal:g5.34.8.1 council ONE v6 + SM PASS-with-amend 2026-10-06-d; Belam A+B LOCK FINAL. First DG build leaf after DG1/DG2 PASS: one monitor detector for bound seats and SM-manned DG panes (process-wait-while-manned wake) with check/wait verbs.
- Owner 10:19–10:20: true SM-internal-subagent manning of existing DG panes; bots may run ongoing Task/monitor informing of new pings.

## CLAIM
A single `### monitor` piece exposes check/wait verbs that implement process-wait-while-manned wake for both bound seats and SM-manned DG panes; one detector both tracks share; v6 A+B LOCK held.

## Dispatch line
config-max: monitor piece cells / template-max: check+wait verb surface / code: process-wait-while-manned detector (builder after DG2 PASS). Not this seat.

## FALSIFIERS
1. monitor check/wait exercise on a manned pane exits/wakes on the contracted events; same piece serves bound-seat and SM-manned paths.
2. Negative: two divergent detectors; B-only v5 revived; hand-patched per-seat watch.

## TESTS
DG2 experiment against goal:g5.34.8.1 + v6 ruling. Neighbourhood: proposals/council-gate-20261006-d. No implement this mint.

## FILE SCOPE
this node. No monitor binary. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
