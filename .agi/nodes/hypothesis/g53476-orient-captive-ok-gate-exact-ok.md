---
id: hypothesis:g53476-orient-captive-ok-gate-exact-ok
mint_id: 9fccc850615c4122bb580d4f3dce5d11
type: hypothesis
parents:
  - goal:g5.34.7.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
model: grok-4.6
role: director
scaffold_hash: cbcccdb57349c2c6
season: 3
testable_claim: After successful orient dump + line-start end-startup, the pane path prints a lean captive prompt and blocks until a line that is exactly ok; no other command runs until then; then continues. Not an o-trimmer; not a new poller.
title: orient captive exact-ok gate after end-startup (goal:g5.34.7.6)
town: core
---
# hypothesis:g53476-orient-captive-ok-gate-exact-ok

## Measured
- 14:4xZ 10-06 (date -u), director-general-1. SM GO hyp/split only. goal:g5.34.7.6 owner 10:29: orient/context dump = captive flow — show dump, wait for typed exact ok, then continue. plan-master ET tip 085383152: ### orient captive ok does NOT exist yet (orient clears/dumps/exits today). Sibling C-mail SoT = agi-carry@ (g5.34.6.2 / g5.34.8.1) — not this leaf.
- SM lean: exact ok (case per council/DG). Not g5.34.7.5 o-trimmer.

## CLAIM
After successful orient dump + line-start ===== end startup =====, the pane path prints a lean captive prompt and blocks until a line that is exactly ok; no other command runs until then; then continues. Not an o-trimmer; not a new poller.

## Dispatch line
config-max: none / template-max: orient/raw-shell captive ok prompt line / code: block-until-exact-ok after end-startup (builder after DG2 PASS). Not this seat.

## FALSIFIERS
1. After orient dump + end-startup: prompt appears; non-ok lines do not continue; exact ok continues once.
2. Negative: orient still exits without ok-gate; ok-gate bolted onto g5.34.7.5 trimmer; new poller invented.

## TESTS
DG2 experiment against goal:g5.34.7.6 design claims. Neighbourhood: proposals/council-gate-20261006-e orient-ok ruling. No implement this mint.

## FILE SCOPE
this node. No orient edit. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
