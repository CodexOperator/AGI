---
id: hypothesis:write-py-set-must-preserve-scalar-types
mint_id: 26b7410b6c9d41a087f2ff91e39aa222
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: director
scaffold_hash: add0a3b1cb712b7a
scale: engine
testable_claim: "write.py set stores a value with the type the target schema declares (int, float, bool, list) rather than always a string; set tier -1 yields tier: -1, and the 91 deprecated nodes carrying tier: \"-1\" from L1.09 become schema-valid after a one-off retype"
thought_session: L1.08
title: Write py set must preserve scalar types
---
# hypothesis:write-py-set-must-preserve-scalar-types

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Measured 2026-09-03: the L1.09 bulk pass used write.py set tier -1 and every one of the 159 nodes got tier: \"-1\" (a quoted string), so 91 deprecated nodes fail types: tier in schema validation. Fix in write.py: coerce by the schema types entry for the field (int/float/bool/list), fall back to YAML-safe scalar parsing, never silently string-ify a number. Then retype the corpus once via the same path and report schema-invalid before/after. Red-on-purpose test required."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director-minted from the L1.09 cleanup agent finding."
<!-- THOUGHT:END -->
