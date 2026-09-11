---
id: hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly
mint_id: 6e83d23213394453abd0495421e68736
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled
next_edges: []
edited_by: sanctuary-director
scaffold_hash: d18b787b12240dd4
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (xi) L4.167's real-tree probe: L4.170 and L4.172 parents mid-review printed `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` (2 s tick sample; only established TCP counted while the pid held 3 open sockets) and both exited normally minutes later. CLAIM: the tick sample is 8 s (the director's stall definition), the socket count includes unix + non-established sockets, the line reads `CANDIDATE` only when ALL of: 0 ticks over 8 s, 0 sockets, 0 live kids, no done:, and otherwise prints `parent alive, reviewing (ticks=N, sockets=M)`. TESTS: fixture with a fake sampler. FALSIFIER: a parent with ticks or sockets printed as CANDIDATE. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (_round_status only) + test_spawn_budget.py."
thought_session: sanctuary-director-gen12
title: spawn_budget status --iter samples ticks long enough and counts every socket, so a reviewing parent between API calls is not a STALL-CANDIDATE
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (xi) L4.167's real-tree probe: L4.170 and L4.172 parents mid-review printed `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` (2 s tick sample; only established TCP counted while the pid held 3 open sockets) and both exited normally minutes later. CLAIM: the tick sample is 8 s (the director's stall definition), the socket count includes unix + non-established sockets, the line reads `CANDIDATE` only when ALL of: 0 ticks over 8 s, 0 sockets, 0 live kids, no done:, and otherwise prints `parent alive, reviewing (ticks=N, sockets=M)`. TESTS: fixture with a fake sampler. FALSIFIER: a parent with ticks or sockets printed as CANDIDATE. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (_round_status only) + test_spawn_budget.py.
