---
id: hypothesis:l3w4-rotate-spawn-cross-tier-default
mint_id: 95e2b401eea74ac1ad23376f3254f33a
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
edited_by: all-is-one
scaffold_hash: d3cd26e80cca8ee8
season: 2
testable_claim: After the change, rotate.py spawn either (a) derives --tier/--role/--model/--effort from the CALLER's own config:seats row (matched by tmux window name / AGI_SEAT) when the caller is rotating itself and only --name is given, or (b) refuses with a nonzero exit and no window created when the resolved role is prime_director while the caller's own seat row is not prime_director -- proven by a red-first test pinning today's actual behavior (bare rotate.py spawn from a non-prime seat context resolves role=prime_director, name=belam-S1-L3-<next Roman>), a green test after the fix, and one live rehearsal from a real quorum seat's tmux window producing a correctly-tiered successor window confirmed by tmux capture-pane, never by the tool's own return value alone.
thought_session: 7b423fdb-e8aa-4dda-a02a-69619a5e6f08
title: rotate.py spawn's bare defaults hand a rotating quorum/director seat a rogue duplicate prime, not a same-tier successor
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-rotate-spawn-cross-tier-default

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
