---
id: hypothesis:write-body-range-guard-is-fence-aware-and-clamped
mint_id: c296af2356ac4ebc9f10f3e7e3d9eb81
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.8
edited_by: belam
scaffold_hash: c9956c53d0e32a09
season: 2
testable_claim: After the fix, _is_heading (write.py:2153) ignores a '#' line inside a code fence so _section_end (:2164) can no longer let a replace-body range cut a fenced block in half (refused by name), and _body_range_refusal (:2220) clamps hi to the body length so a range past EOF is refused instead of raising IndexError at lines[end-1] (:2240-2241); both proved by committed tests in test_write.py, the existing 131 stay green.
title: "write.py: the body-range guard is fence-aware and clamps past-EOF ranges (assigned: director-engine)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:write-body-range-guard-is-fence-aware-and-clamped

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
assigned: director-engine (owner 01:4xZ 09-21); surfaced by the 09-21 Prime merge-up-review, batch = hypothesis:mur-0921-residue-batch-into-season2-main.
