---
id: hypothesis:g53483-bound-seat-monitor-arming-agi-sync-k10-k11
mint_id: f381fea4ad7844dfbc62c3fc0bf2c291
type: hypothesis
parents:
  - goal:g5.34.8.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
model: grok-4.6
role: director
scaffold_hash: 8e309bd0a9da4feb
season: 3
testable_claim: Bound seats arm monitor wait post from identical agi-sync dump text (K10), re-arm each turn if dead with 6h heartbeat (K11), do box read on mail/mail-unhandled (K7), dedupe W1 push vs monitor exit by tip sha (W1), and stop on unman (O4).
title: bound-seat monitor arming via agi-sync K10/K11 (goal:g5.34.8.3)
town: core
---
# hypothesis:g53483-bound-seat-monitor-arming-agi-sync-k10-k11

## Measured
- 14:4xZ 10-06 (date -u), director-general-1. SM GO hyp/split only. goal:g5.34.8.3 Track A: bound grokbot seats arm g5.34.8.1 monitor for own pane+inbox via agi-sync dump text (K10); K11 durability re-arm; K7 box read on mail wake; W1 tip-sha dedupe; A7 monitor sole wake until g5.35.2+agi-wake; O4 stop when unmanned.

## CLAIM
Bound seats arm monitor wait <post> from identical agi-sync dump text (K10), re-arm each turn if dead with 6h heartbeat (K11), do box read on mail/mail-unhandled (K7), dedupe W1 push vs monitor exit by tip sha (W1), and stop on unman (O4).

## Dispatch line
config-max: engine-wrap agi-sync dump arming text / template-max: none / code: bound-seat arm+rearm+dedupe (builder after DG2 PASS). Not this seat.

## FALSIFIERS
1. After agi-sync: monitor armed; kill → next turn re-arms; mail wake → box read; same tip handled once.
2. Negative: bot hand-install per seat; sleep-loop as sole wake after agi-wake lands without A7 text update.

## TESTS
DG2 experiment against goal:g5.34.8.3. Neighbourhood: v6 Track A K10/K11/K7/W1/A7/O4. No implement this mint.

## FILE SCOPE
this node. No agi-sync edit. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
