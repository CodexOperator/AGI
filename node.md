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
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: spawn_budget status --iter samples ticks long enough and counts every socket, so a reviewing parent between API calls is not a STALL-CANDIDATE
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (xi) L4.167's real-tree probe: L4.170 and L4.172 parents mid-review printed `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` (2 s tick sample; only established TCP counted while the pid held 3 open sockets) and both exited normally minutes later. CLAIM: the tick sample is 8 s (the director's stall definition), the socket count includes unix + non-established sockets, the line reads `CANDIDATE` only when ALL of: 0 ticks over 8 s, 0 sockets, 0 live kids, no done:, and otherwise prints `parent alive, reviewing (ticks=N, sockets=M)`. TESTS: fixture with a fake sampler. FALSIFIER: a parent with ticks or sockets printed as CANDIDATE. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (_round_status only) + test_spawn_budget.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.177, 2026-09-11 09:57Z). Kept kid 1's proved (0.8) and kid 2's proved (0.9) and the parent's line-cited verification. Ran myself: `pytest test_spawn_budget.py test_dispatch.py test_heal.py test_commands.py -q` on the round bytes -> 180 passed; test_spawn_budget + test_dispatch on the merged seat bytes -> green. Real-tree probe, `spawn_budget.py status --iter L4.180` against the LIVE L4.180 round (parent pid 2289288, kid pid 2290545), pre-fix seat bytes at 09:57:37Z: parent `ticks=0 sockets=0`, kid `ticks=2 sockets=1`; round bytes at 09:57:41Z: parent `ticks=0 sockets=3`, kid `ticks=1 sockets=2`. Same parent, same minute: the pre-fix count sees no socket on an API-bound parent (state-01 only) and would print STALL-CANDIDATE the moment its kid exits; the round bytes see its three LISTEN/unix sockets. Both runs printed `parent alive, 1 live kid(s)` because the kid was live, and both printed `agent=(no agent.json)` for every row -- the round's agent.json lives under the seat worktree's .agi/sessions/iter-L4.180/, not MAIN's: g15-36b (hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir) confirmed live on this probe. Residue: none beyond g15-36b, already minted.
