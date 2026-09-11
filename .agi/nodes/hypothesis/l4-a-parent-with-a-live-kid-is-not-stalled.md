---
id: hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled
mint_id: f7047756159e4a11b6741675372c15d2
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-completion-signal-cannot-tell-dead-from-silent
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 44d21747f16541eb
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (vii) the prime's protocol finding at merge-up 29: L4.140 and L4.144 parents were TERM'd 06:26Z as 'stalled' on a parents-only check while each waited on a THIRD kid (the director listed parent rows only). CLAIM: `spawn_budget.py status --iter L4.NNN` prints every live row of that iteration (parent + kids) with pid, tier, elapsed, CPU ticks over a 2 s sample, established-socket count and the agent.json status, and ends with ONE verdict line — `round L4.NNN: parent alive, N live kid(s)` or `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` — a parent with ≥ 1 live kid is NEVER a stall candidate; unknown iter → a named message, exit 1; the director's stall procedure (skills/agi/SKILL.md or the seat scratchpad) cites the command. TESTS: fixture budget dir + agent.json files: parent + live kid → not a candidate; parent only with the sampled pid idle → candidate; unknown iter → named. FALSIFIER: a parent with a live kid printed as STALL-CANDIDATE. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (the new flag only) + its tests (+ one paragraph in skills/agi/SKILL.md if the procedure lives there). EXCLUDED: heal.py, dispatch.py."
thought_session: sanctuary-director-gen12
title: spawn_budget.py status --iter prints the whole round (parent + kids, ticks, sockets) and never calls a parent with a live kid a stall candidate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (vii) the prime's protocol finding at merge-up 29: L4.140 and L4.144 parents were TERM'd 06:26Z as 'stalled' on a parents-only check while each waited on a THIRD kid (the director listed parent rows only). CLAIM: `spawn_budget.py status --iter L4.NNN` prints every live row of that iteration (parent + kids) with pid, tier, elapsed, CPU ticks over a 2 s sample, established-socket count and the agent.json status, and ends with ONE verdict line — `round L4.NNN: parent alive, N live kid(s)` or `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` — a parent with ≥ 1 live kid is NEVER a stall candidate; unknown iter → a named message, exit 1; the director's stall procedure (skills/agi/SKILL.md or the seat scratchpad) cites the command. TESTS: fixture budget dir + agent.json files: parent + live kid → not a candidate; parent only with the sampled pid idle → candidate; unknown iter → named. FALSIFIER: a parent with a live kid printed as STALL-CANDIDATE. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (the new flag only) + its tests (+ one paragraph in skills/agi/SKILL.md if the procedure lives there). EXCLUDED: heal.py, dispatch.py.
