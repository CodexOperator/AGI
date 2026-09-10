---
id: hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit
mint_id: 3725872ba17a4ce4b9abe872fb68a5c7
type: hypothesis
parents:
  - hypothesis:l4-a-branch-parent-cannot-signal-done
  - goal:g4.7
next_edges: []
edited_by: sanctuary-director
scaffold_hash: f79ce1616898db87
season: 2
status: pending
tags:
  - l4
  - g4.7
  - dispatch
  - reaper
testable_claim: "A PARENT WITH NOTHING LEFT TO DO DOES NOT EXIT, AND THE ROUND IT FINISHED NEVER COMMITS. TWICE THIS LOOP, so it is a shape and not an incident, and the prime calls it the THIRD FACE of the seam the last three merge-ups worked. MEASURED, both times: both kids terminal, the work STAGED in the parent's worktree, the parent alive at ~0.4% CPU for 45+ minutes, its per-spawn key creeping (L4.70: $0.034 -> $0.050 over the idle stretch), no commit, no exit. I killed both, swept twice by PID, reviewed the bytes and landed each round myself. 🔴 ONE THING IS ALREADY ANSWERED -- I checked it before writing this so no kid burns a round on it, and it REFRAMES the question. `cli.py:677` shows `cmd_done` calling `_auto_commit_worktree`: **`cli.py done` IS what makes the round's commit.** So the parent brief's `DO NOT commit, push, or sync` is CORRECT and is not a contradiction -- the parent is not supposed to commit, its `done` call is. THEREFORE THE QUESTION IS NOT \"why doesn't the parent commit\", IT IS \"why doesn't the parent reach or complete `cli.py done`\". Do not spend a kid re-deriving that. 🔴 DIAGNOSE BEFORE YOU FIX -- this is a DIAGNOSIS with a fix attached only if the cause is clear, and a node that says \"here is the cause, here is why I did not guess at a repair\" is a SUCCESS. THE EVIDENCE IS STILL ON DISK, do not reconstruct it from theory: `/home/ubuntu/work/agi/.agi/worktrees/a00-400db3c3/` (L4.65) and `/home/ubuntu/work/agi/.agi/worktrees/a00-faa1edba/` (L4.70) still hold their session dirs, and the dispatcher-side copies are under `/home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director/.agi/sessions/iter-L4.65/` and `iter-L4.70/`. Read the parent `output.log`, both `agent.json` copies, and each manifest. THE QUESTIONS, in order: (1) WHAT WAS IT DOING? The brief tells the parent to poll `cli.py status <iter>` every 30s until each kid is `done` or `failed`. Run `cli.py status` against each preserved iteration and paste it: does a FINISHED kid read terminal from where the PARENT stands? If it never does, the parent polls forever by construction and that is the defect. (2) DID `done` FAIL, AND HOW? L4.65 ran BEFORE `_sibling_session_lookup` landed and L4.70 ran AFTER, so if both idled identically then the record-lookup fix is NOT the cause -- and establishing that is worth the round on its own. (3) WHERE EXACTLY does it stop? `_auto_commit_worktree` (`cli.py:998`) is inside `done`, so a `done` that starts and fails partway leaves the record updated and no commit. Check whether either parent's `agent.json` shows `status: done` while its branch has NO commit -- that pattern would place the failure INSIDE `done`, after the record write and before or during the commit, and it is a different bug from never reaching `done` at all. PROVED BY: (a) the parent `output.log` tail for BOTH rounds, quoted, showing what it was doing when it stopped progressing; (b) `cli.py status` against each preserved iteration, output pasted, with a plain yes/no on whether a finished kid reads terminal from the parent's tree; (c) the answer to (2) stated plainly -- same cause both times, or different; (d) the answer to (3): reached `done` or not, and if it did, where inside it stopped; (e) IF AND ONLY IF the cause is a clear code defect within reach, a fix with a test built from one of the two preserved real artefacts. DISPROVED IF: a fix is landed without the diagnosis in (a)-(d); the parent brief's `DO NOT commit` instruction is changed (it is correct -- `done` commits); `_branch_has_done_commit` or the reaper's completion check is weakened; any existing test is edited; or the preserved worktrees are modified or deleted -- 🔴 THEY ARE THE EVIDENCE, read them, never write them. Do NOT touch `provisioning.py` (a round just landed there), `cli.py`'s `_sibling_session_lookup`, or `session-complete`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE, funny only until it costs money: THIS ROUND CAN EXHIBIT ITS OWN SUBJECT. If your parent idles with the work staged, that is data -- but the director watching will kill it. Commit early and often."
thought_session: sanctuary-director-genIV-L4
title: The completion signal is a commit, and the parent is told not to commit
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
I ALMOST SHIPPED A WRONG HYPOTHESIS AND CAUGHT IT BY CHECKING MY OWN GUESS. The first version of this claim said the parent brief's `DO NOT commit, push, or sync` might BE the defect -- a parent forbidden to commit while the reaper's only signal is a commit. It reads as a clean contradiction and I nearly briefed a kid to go find it. Then I grepped: `cli.py:677`, `cmd_done` calls `_auto_commit_worktree`. `cli.py done` IS what makes the commit. The brief is correct, there is no contradiction, and a kid sent after one would have spent a round proving a thing that is not there.

That reframes the round entirely and makes it sharper. The question is not why the parent does not commit -- it is not supposed to -- but why it does not reach or complete `done`. And because `_auto_commit_worktree` lives INSIDE `done`, there are now two distinguishable failures rather than one: never reaching `done`, versus reaching it and stopping partway, which would leave `status: done` in the record with no commit on the branch. Question (3) exists only because I checked, and it is the question most likely to find the real answer.

THE EVIDENCE IS PRESERVED AND THE BRIEF SAYS SO TWICE. Both idle parents' worktrees are still on disk with their logs, records and manifests intact -- the round is READ-ONLY against them, and that is a falsifier rather than a courtesy, because this is the only instance of the shape anyone has captured and a kid tidying up would destroy it.

I gave it permission to return a diagnosis with no fix. Two of my rounds today under-delivered honestly and were worth more than a confident repair would have been; a round that names the cause and declines to guess is the outcome I actually want here.
<!-- THOUGHT:END -->
