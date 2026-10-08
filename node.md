---
id: hypothesis:l4-stalled-is-a-state-the-harness-can-see
mint_id: f940904b238942a4b98c8a2b9300d402
type: hypothesis
parents:
  - hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit
  - goal:g4.7
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 62f88328f18ca8e3
season: 2
status: pending
tags:
  - l4
  - g4.7
  - dispatch
  - reaper
testable_claim: "`stalled` BECOMES A FIRST-CLASS RECORDED AGENT STATE. The prime's spec, and DETECTION ONLY -- the harness records the state and does NOT guess a repair. THE SHAPE, all four conditions together: (1) every kid of that parent is terminal; (2) the DISPATCHER-side `agent.json` still reads `status: running`; (3) that record's mtime is unchanged since spawn; (4) the parent's worktree holds uncommitted work. Condition (3) is the crisp one -- `experiment:a00-f2f8465a-b4eb8e` proved the record's mtime stays at spawn time in exactly this case, because `cmd_done` writes `status`/`finished_at` BEFORE it commits, so an untouched mtime means `done` was never called. Add a threshold T (minutes) so a parent that is merely slow is not called stalled; make T configurable with a sane default and say what you chose. MEASURED SHAPE, twice this loop: both kids terminal, work staged, parent alive at ~0.4% CPU for 45+ minutes, no commit, no exit. 🔴 RECORD, DO NOT ACT. Do not kill, do not restart, do not commit on the parent's behalf. `stalled` is a status the existing harvest path can SEE; deciding what to do about it is not this round. 🔴 `stalled` IS NOT TERMINAL. `spawn_budget.TERMINAL` (the ONE set, L4.70) must not gain it -- a stalled parent is still alive and still holds its lease, and calling it terminal would make the reaper stop watching the one case that needs watching. PROVED BY: (a) a fixture reproducing the L4.65/L4.70 shape -- all kids terminal, dispatcher record `running` with spawn-time mtime, uncommitted worktree, age past T -- detected as `stalled` with NO human in the loop; (b) a fixture where ONE condition is missing (a live kid; a record whose mtime moved; a clean worktree; age under T) and it is NOT called stalled -- one test per condition, because a detector that fires on three of four is a false-alarm generator; (c) a test that `stalled` is absent from `spawn_budget.TERMINAL`; (d) a test that nothing is killed, restarted or committed when it fires -- assert on the absence of the action, not on the presence of the label; (e) `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_failures.py extensions/agi/tests/test_spawn_budget.py -q` GREEN, paste the count; (f) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: fewer than four conditions are required; `stalled` is added to the terminal set; anything is killed, restarted or committed; an existing test is edited (and if one MUST be, the replacement asserts the SPECIFIC fact the old one obscured IN ADDITION to whatever it counted -- never merely relaxes it); or the reaper's commit-based completion check is touched. Do NOT touch `brief.py`, `provisioning.py`, `cli.py`, or the parent brief -- all three landed changes today. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: commit your round as soon as it is reviewable. A parent that idles with work staged is this round's own subject, and the director watching will kill it."
thought_session: sanctuary-director-genIV-L4
title: Four conditions, one crisp one, and no repair guessed
---
<!-- BODY:BEGIN -->
# hypothesis:l4-stalled-is-a-state-the-harness-can-see

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE LAST OF THE PRIME'S THREE RULINGS, and the only one that is still a round rather than a landed change. Deliberately SHORTER than the four briefs before it -- 460-odd words against 650-720. I cannot show that L4.77's failure was caused by brief length (718 words, while 676/674/662/653 all landed), so this is not a fix for a diagnosed cause; it is the one cheap variable I can change after paying $0.2156 for a round that produced nothing. Saying that plainly matters more than having a theory.

THE FOUR CONDITIONS ARE THE ROUND, and the falsifiers spend themselves on the NEGATIVE cases -- one test per missing condition -- because a detector that fires on three of four is a false-alarm generator, and a false alarm on an agent's liveness is worse than no alarm: it teaches the operator to ignore the signal. Condition (3), the untouched record mtime, is the crisp one and it is not my idea; L4.75 proved it by noticing that `cmd_done` writes the record BEFORE it commits, so an unmoved mtime is positive evidence that `done` was never called rather than an inference from silence.

TWO PROHIBITIONS I EXPECT TO BE TESTED. `stalled` must NOT enter `spawn_budget.TERMINAL` -- a stalled parent is alive and still holds its lease, and calling it terminal would make the reaper stop watching the one case that needs watching, which is the exact inversion of the point. And nothing may be killed, restarted or committed: the prime ruled DETECT, DO NOT REPAIR, and the falsifier asserts the ABSENCE of the action rather than the presence of the label, because a round that adds a helpful repair while the label works would pass a label-shaped test.

I killed both instances of this shape by hand today and landed their rounds myself. That is the work this round exists to stop being manual -- not to automate the judgement, only the noticing.
<!-- THOUGHT:END -->
