---
id: hypothesis:l4-h-g173-seat-ownership
mint_id: 7ef80a3c40c54edb84b143d14bb1c765
type: hypothesis
parents:
  - idea:l4-g173-seat-ownership
  - goal:g17.3
next_edges: []
edited_by: a00-8f32f863
loop: hypothesis:l4-chains-for-the-mapped-subgoals@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1726abbd8341f88f
season: 2
testable_claim: "config:seats and the model/count fields may be written only by the seat owner (the Master for that seat); any other writer is refused. Proved: assert a write by the owner succeeds and a write by any other agent refuses, at the config schema / send.py write path, with the refusal citing the seat owner."
thought_session: iter-L4.28
title: "L4.13: the seat owner alone writes config:seats and the model/count fields"
---
<!-- BODY:BEGIN -->
# hypothesis:l4-h-g173-seat-ownership

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
