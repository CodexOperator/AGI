---
id: hypothesis:l4-a-round-alarms-its-dispatcher-by-default
mint_id: 9a555d21d4a1430cb3fd959523587fa4
type: hypothesis
parents:
  - goal:g4.7
next_edges: []
edited_by: belam-S1-L4-VI
scaffold_hash: 3795501d6babdec3
season: 2
testable_claim: "OWNER 2026-09-10 22:44Z (verbatim in doc:l4-owner-decisions): 'For some reason it missed the completion for L4.120 and L4.121. Maybe forgot to set an alarm, but that is the error. A round doing anything should auto-alarm the agent that dispatched it automatically as part of the dispatch routine without having to set any extra flags or anything'. MEASURED: L4.120 (a00-698453a0) and L4.121 (a00-321c00b2) completed on their agent branches (done commits 379a4fb33 proved, 76d8deee6 pending) and the dispatching seat learned nothing - dispatch.py records the dispatcher (AGI_SEAT provenance in the spawn record) but no completion path sends it anything: cli.py done writes the done: commit and stops, heal.py restarts or gives up in silence, rotate.py alarms meters context fractions only. CLAIM: a round alarms its dispatcher BY DEFAULT. (1) dispatch.py stamps the dispatching seat (resolved AGI_SEAT, else the ladder-derived name) into the round's manifest.json as dispatched_by at spawn - no flag; (2) every terminal event of a round sends the dispatcher exactly ONE dm through send.py (the transport that already nudges the seat's tmux pane): completion from the writer path (cli.py done / post_wire.py, right after the done: commit, carrying iteration, agent, node id and verdict), death and timeout from heal.py (carrying the reason), and the reaper's give-up (dispatch.py reaper: finished) carrying which agents were still running; (3) a dispatcher that is absent from the manifest gets no dm and ONE stderr line naming the gap, never a crash; a dm that cannot be delivered is logged, never fatal to the round. PROVED BY: a dispatch from a fixture seat with NO extra flags whose kid completes, dies and times out in three runs, each landing exactly one dm in the fixture dispatcher's inbox with the event named, measured from the inbox file and the nudge log; and the live helper's inbox receiving the dm for the first round it dispatches after this lands. DISPROVED BY: a completed round whose manifest names a dispatcher and whose dispatcher's inbox is empty, or any flag a dispatcher must pass to get the dm. HARD RULES: dispatch.py, cli.py, post_wire.py, heal.py and send.py are build nodes edited through write.py; the dm is ONE message per event, numbers and ids only (owner standing order on message discipline); never nudge a pane that is not the dispatcher's (test_send.py nudges real panes - fixtures use --comms-root and a fake pane); no new bin/*.py; disjoint from rotate.py, so it runs CONCURRENT with the rotate chain."
thought_session: belam-S1-L4-VI
title: A round alarms its dispatcher by default — completion, death and timeout each send ONE dm to the seat recorded at dispatch, no flag
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-round-alarms-its-dispatcher-by-default

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
