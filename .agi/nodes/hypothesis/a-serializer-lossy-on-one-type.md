---
id: hypothesis:a-serializer-lossy-on-one-type
mint_id: 008dff516e6742519d90a1f206d76662
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: director
scaffold_hash: a533ea9e47ea561e
testable_claim: A frontmatter serializer with a str(v) fallback branch will silently destroy the first node type it does not recognise, and the loss will look like a successful write
thought_session: L1.07
title: A str(v) fallback is how losing data looks like working
---
# hypothesis:a-serializer-lossy-on-one-type

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
