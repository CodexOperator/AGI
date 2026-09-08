---
id: hypothesis:l3-killed-agent-restarts-unattributed
mint_id: e33ef149400043cfb4e9cacfc8628b65
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: f10044573ad2c66f
season: 2
testable_claim: "After the change, terminating a round's agents actually terminates them: a killed agent is not silently restarted, or if a restart is intentional it inherits the iteration id of the agent it replaces so spawn_budget.py status attributes it to its round rather than to iter=None, proven red-first by killing a dispatched agent and asserting no unattributed survivor."
thought_session: belam-S1-L3-XI
title: Killing a dispatched agent's tmux window does not stop the agent, and the survivor is auto-restarted with iter=None so it is invisible to the round it belongs to
---
<!-- BODY:BEGIN -->
# hypothesis:l3-killed-agent-restarts-unattributed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

MEASURED LIVE, 2026-09-08, L3.42 (Belam XI). Six parents were dispatched on `--harness claude-code`. The owner then said, verbatim, "Use openrouter" / "Subscription will get drained", so the prime killed the six tmux windows and the six parent pids and relaunched the same six briefs on pi.

`spawn_budget.py status` then showed FOURTEEN live agents where twelve were expected, and three of the extras carried names the round had never issued:

    a00-01409122-r1 tier=parent iter=None pid=1320910
    a00-5de9ba88-r1 tier=kid    iter=None pid=1321758
    a00-77d3444d-r1 tier=parent iter=None pid=1320888

All three were ALIVE (81 seconds of elapsed time), on the subscription the owner had just asked to stop spending, working the same briefs the pi parents were now working. They had to be found by eye and killed by hand.

THREE THINGS ARE WRONG AND THEY COMPOUND.
1. Killing the tmux window does not kill the agent. That much is arguably correct - a window is a view - but nothing anywhere says so, and every round's stop procedure in HANDOFF.md is written as if closing the window ends the work.
2. Something restarted them. The `-r1` suffix is a restart marker, so a supervisor treated a deliberate kill as a failure and revived the process. A deliberate stop and a crash are not the same event and must not produce the same response.
3. The restart lost its iteration. `iter=None` means the survivor is attributed to no round at all. **This is the dangerous one.** Every prime's round stop-condition is a loop on `spawn_budget.py status` reaching 0; an agent with `iter=None` still counts toward the total, so it can hold a round open forever, and an operator scanning for `iter=L3.42` will not see it. It is the mirror of the defect where workflow spawns took no lease at all - there the count was too low, here the attribution is missing - and both make the same number untrustworthy.

WHAT TO BUILD. A deliberate termination must be distinguishable from a crash, and must not be revived. If a restart is right in some path, the replacement inherits the iteration id, the seat and the tier of the agent it replaces, so it is attributable. `iter=None` on a live lease should be impossible; if it is reachable at all it should be loud.

COST DIMENSION, worth stating because it is what makes this urgent rather than tidy: these three survivors were spending on the exact harness the owner had just asked the loop to stop using, and nothing in the system noticed. A silent revival of a killed agent is a silent spend.

PROVE IT, RED FIRST. Dispatch an agent, kill it deliberately, and assert no `-rN` survivor appears and `status` returns to its prior count. Then assert that any restart that IS legitimate carries a real iteration id, never `None`. Verify both red by stashing the fix. Paste actual `spawn_budget.py status` output before, during and after.

DO NOT touch `workflow.py`, `rotate.py`, `brief.py`, `cli.py` or `zoom.py`. `dispatch.py` and `spawn_budget.py` are yours if the fix lives there. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window - the predecessor chain lives in them, and this brief is not a licence to experiment on them.
