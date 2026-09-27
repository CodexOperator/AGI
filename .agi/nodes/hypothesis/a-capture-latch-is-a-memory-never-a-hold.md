---
id: hypothesis:a-capture-latch-is-a-memory-never-a-hold
mint_id: 1b4eda68f7d1486fb7f6b002a493d674
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: 054b0c984bfc460f
season: 2
testable_claim: a latched over-line seating prints no hold claim; captured and capture-no-spawn still return True, pinned; the stamp write re-reads before writing
title: "A capture latch prints as a memory, never as a hold (assigned: director-engine)"
town: core
---
# hypothesis:a-capture-latch-is-a-memory-never-a-hold

# hypothesis: A capture latch prints as a memory, never as a hold (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
rotation_alert.py:979-985 -> _gated_rotate :1575 -> gate (a) :1144-1147 -> :1577-1580 prints "(capture-latched) ... not rotating this seat while that holds" on a latched over-line seating; the latch records a capture whose chain already ran (PASS 10 c1 re-review of b6438bd7e). Same family (c1, c8): the quiet half of the predicate unpinned (captured :919 / capture-no-spawn :897), session key written only if session_id (:911-913), the read hoist widens the stamp write window (:871-874 -> :911-916)

## Testable claim
a latched over-line seating prints no hold claim; captured and capture-no-spawn still return True, pinned; the stamp write re-reads before writing
