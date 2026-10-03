---
id: hypothesis:g716111-aa2-a-baton-survives-an-out-line-and-goes-only-to-phis-next-post
mint_id: f74ba94b1a904e23a0823ee058fead01
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 0a483fbe202bb1f9
season: 2
testable_claim: "(a) an unread `[lap]` mail survives an agi-meter out-line and a successor's wake: the successor's first unread listing is non-empty; (b) agi-send in lap mode picks the recipient from the ONE lap.tsv row `F me T` for the dart the baton came in on; (c) grow-gate refuses a `[lap]` commit on refs/box/P/T unless row `F P T` exists; (d) the lap's first `[lap]` (belam -> council) is legal only from belam."
title: "AA2: an unread [lap] baton survives an out-line + wake, and a [lap] sent to any recipient other than PHI's is refused at the gate"
town: core
---
# hypothesis:g716111-aa2-a-baton-survives-an-out-line-and-goes-only-to-phis-next-post

## Measured
- doc:radically-simple-engine §AA2 'Two rotations, one product': LAP (PHI on darts) and GENERATION (the in-session rotation, g -> g+1) commute; the baton survives because it is an unread ref, not session memory.
- Limit (4) of the section: the route check needs the dart a baton came in on, so the first [lap] is legal only from the lap's root: one more row condition, NOT measured yet.
- DEPENDS ON goal:g7.16.1.11.11 (boxes) for the unread ref and on the lap hypothesis.

## CLAIM
(a) an unread `[lap]` mail survives an agi-meter out-line and a successor's wake: the successor's first unread listing is non-empty; (b) agi-send in lap mode picks the recipient from the ONE lap.tsv row `F me T` for the dart the baton came in on; (c) grow-gate refuses a `[lap]` commit on refs/box/P/T unless row `F P T` exists; (d) the lap's first `[lap]` (belam -> council) is legal only from belam.

## Dispatch line
config-max: the `post lap lap.tsv agi-send` matrix row (~+110 B shared) / template-max: none / code: lap mode folded into agi-send; the route check folded into grow-gate (existing pieces).

## FALSIFIERS
AA2.5 an unread [lap] survives an out-line + wake · AA2.6 a [lap] to any T other than PHI's is refused at the gate · the first-lap rule (belam only) · negative: a [lap] with a named recipient is refused.

## TESTS
stub-pane rotation test; a gate test over a fixture lap.tsv with one legal and three illegal routes.

## FILE SCOPE
agi-send lap mode · grow-gate route check · tests. HORIZON behind the boxes build.

## CEILING
1 parent · kids <= 2 · 0 new pieces · regular review.
