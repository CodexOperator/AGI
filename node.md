---
id: hypothesis:l4-h-g178-messaging-restrictions
mint_id: eb397e1a82394a4abf92b5a3d2488a1f
type: hypothesis
parents:
  - idea:l4-g178-messaging-restrictions
  - goal:g17.8
next_edges: []
edited_by: a00-8f32f863
loop: hypothesis:l4-chains-for-the-mapped-subgoals@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6492122c87a1c826
season: 2
testable_claim: "send.py resolves message targets through the seat nodes and refuses a recipient outside the sender tells, while the inbox-only prime and the closed quorum room refuse exactly what they refuse today. Proved: a send to a recipient outside the sender tells is refused; a regression check confirms the prime and quorum refusals are unchanged."
thought_session: iter-L4.28
title: "L4.14: send.py resolves targets through seat nodes and refuses outside tells"
---
<!-- BODY:BEGIN -->
# hypothesis:l4-h-g178-messaging-restrictions

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
