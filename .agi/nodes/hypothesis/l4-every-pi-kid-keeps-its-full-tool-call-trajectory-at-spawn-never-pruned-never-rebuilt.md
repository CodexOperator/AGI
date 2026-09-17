---
id: hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt
mint_id: 043f7bbc2de04601ab39d7dd5eac046e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: a3c999e8f7721a60
season: 2
testable_claim: "(thought-master [ask] 00:08Z, measured on TM.21 mur-0fa8ce058: the pi session store PRUNES kid tool-call trajectories -- only 10 of 354 accepted kid rounds on this box still carry one, and those are rebuilt 400-char summaries; the local-maxxing kid-persona SFT corpus needs the full trajectories. Minted by sanctuary-master gen 4 as node G for the SM lane, after node F; the owner's 17:5xZ ruling keeps TM's lane a side pursuit, so this waits behind the loop's own nodes.) CLAIM: (1) at spawn, the pi adapter (dispatch.py / the pi harness adapter) records the kid's FULL tool-call trajectory -- every tool call with its arguments and result, in order, timestamps -- either appended to the kid's output.log or as a sidecar `trajectory.jsonl` beside it in the kid's session dir, written as the calls happen (never rebuilt afterwards), and never pruned by the pi session store or by session-complete; (2) a rebuilt or truncated summary is never written in its place -- a kid whose trajectory could not be captured gets ONE named line in its record ('trajectory: not captured: <reason>'), never a fake; (3) cli.py session-complete brings the sidecar home with the session dir. FALSIFIERS: an accepted kid round after landing with no trajectory file and no named line; a trajectory whose entries are 400-char summaries; a sidecar dropped by session-complete. TESTS (<=3, fake-pi kid): three tool calls -> three ordered jsonl entries with args+result; capture failure -> the named line; session-complete carries the file. FILE SCOPE: the pi adapter under dispatch (pi_adapter or dispatch.py's pi branch), cli.py session-complete, their tests. CEILING: <=40 production lines, ONE kid, re-brief SM past 2x. Measurement after landing: the next accepted pi kid round carries a trajectory with > 1 entry."
title: L4 every pi kid keeps its full tool call trajectory at spawn never pruned never rebuilt
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
