---
id: hypothesis:l4-session-dirs-come-home-when-the-round-is-done
mint_id: 28dcee0bc977478f848254948c1bef4e
type: hypothesis
parents:
  - hypothesis:l4-a-branch-parent-cannot-signal-done
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 39945522da859017
season: 2
status: pending
tags:
  - l4
  - g17.1
  - sessions
  - worktree
testable_claim: "THE OTHER HALF: A ROUND'S SESSION DIRS ARE STRANDED IN THE WORKTREE THAT RAN IT, AND NOTHING EVER BRINGS THEM HOME. This is the owner's L4.37 remainder (quoted in `goal:g17.1`) and the prime's third design constraint, and it is the half `hypothesis:l4-a-branch-parent-cannot-signal-done` deliberately did NOT answer -- that round left the record where it was and taught the reader to find it (`cli.py` `_sibling_session_lookup`, landed). READ ITS NODES FIRST so you do not redo it: `experiment:a00-293e8c51-f9619e` and `experiment:a00-23a3db9f-41e02c`. WHY IT MATTERS AND IS NOT TIDINESS: `sessions/` is GITIGNORED, so a merge-up carries none of it. Every round this loop has run left its `manifest.json`, `agent.json`, `context.md` and `output.log` in a per-agent worktree that is deleted or reused, and the main checkout -- the one place a cold reader or a later audit looks -- has no `iter-L4.NN/` dir for them at all. VERIFY THAT CLAIM FIRST, in one command, before you build anything: `ls /home/ubuntu/work/agi/.agi/sessions/ | grep iter-L4.6` against `ls /home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director/.agi/sessions/ | grep iter-L4.6`. If the main checkout already has them, SAY SO AND STOP -- a round that builds a migration for a problem that does not exist is worse than no round. REQUIRED, and all three of the prime's constraints must hold in ONE design, stated by number in your node: (1) the iter dir belongs to the worktree that RAN the round -- during the round, resolution does not change; (2) shared state -- spawn budget, comms root, meter pins -- stays in MAIN through `locations.git_common_root` and is NOT part of what moves; (3) a SESSION-COMPLETE step migrates the worktree's iter dirs into main. Build (3) as a named, explicitly-invoked command -- a subcommand on an existing entry point, declared in `command:commands` if it earns a place there -- never as a side effect of another command and never on a timer. 🔴 IT MUST BE COPY-THEN-VERIFY, NEVER MOVE. Copy the tree, compare the copy byte-for-byte, and only then remove the source -- and offer `--dry-run` that prints what would move and touches nothing, as the default posture in your own testing. 🔴 DO NOT RUN IT AGAINST THE LIVE TREE. Other seats are dispatching rounds right now and a live round's `manifest.json` is being written while you read this; moving one out from under its own reaper is a real outage, not a hypothetical. Build it, test it on FIXTURES, and prove it with `--dry-run` output against the real tree at most. A round that is still running MUST be skipped: define 'complete' explicitly (no live lease in `spawn_budget.py status` for that iteration, and every agent record terminal) and refuse to migrate anything that is not. PROVED BY: (a) the verification command above, pasted, showing the gap is real; (b) the command exists, has `--dry-run`, and `--dry-run` is proven to write nothing -- assert on a filesystem snapshot before and after, not on the absence of an error; (c) a fixture test that a COMPLETE iteration migrates and its bytes match after; (d) a fixture test that an INCOMPLETE iteration -- one live lease -- is REFUSED, not partially moved; (e) a fixture test that the source is removed only after the copy verifies, and that a failed verify leaves BOTH sides intact; (f) `python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_locations.py extensions/agi/tests/test_shared_state_worktree.py -q` GREEN, paste the count; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: anything moves without a verified copy; `--dry-run` writes; an incomplete iteration is migrated; the step runs as a side effect or on a timer; shared state (budget, comms, meter pins) is moved; `_sibling_session_lookup` or the reaper's commit-based completion check is weakened or removed on the grounds that migration supersedes them -- BOTH STAY, they are what makes the system work while dirs are still stranded; or it is run against the live tree. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: watch `spawn_budget.py status` for an `-r1` suffix between harvests; the dispatch wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid directly and sweep twice by PID."
thought_session: sanctuary-director-genIV-L4
title: sessions/ is gitignored, so a merge carries nothing — the dirs have to walk home
---
<!-- BODY:BEGIN -->
# hypothesis:l4-session-dirs-come-home-when-the-round-is-done

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The prime named this half out loud before L4.65 even reported: "if L4.65 comes back proposing a home for the record that only fixes the completion path, that is half a design and I will send it back." L4.65 did not propose a home at all -- it proposed a RESOLVER, and left the record where it was. That is a legitimate fix for the completion path and it is not an answer to the owner's question, so the remainder is still open and this round is it, not an invention of mine.

THE HAZARD HERE IS DIFFERENT IN KIND FROM THE LAST THREE ROUNDS and the brief is shaped around it rather than around the feature. Everything I have dispatched this session edited a resolver or a test: wrong answers were cheap. This one moves DIRECTORIES, in a tree where other seats are dispatching right now and a live round's `manifest.json` is being written as the kid reads its brief. Moving one out from under its own reaper is an outage, not a defect. So: copy-then-verify and never move; `--dry-run` proven to write nothing by a filesystem snapshot rather than by the absence of an error; an incomplete iteration REFUSED rather than partially migrated; and the whole thing built and tested on fixtures with the live tree touched only by a dry run. The falsifiers test the refusals, not the feature, because the refusals are what keep this safe.

I ALSO GAVE IT PERMISSION TO STOP. The first falsifier is a one-command check that the gap is real, with an explicit instruction to say so and stop if the main checkout already carries the dirs. I believe it does not -- I looked for `iter-L4.56` in main earlier today and found nothing while it sat in my seat tree -- but I checked one iteration on one day, and a round that builds a migration for a problem that does not exist is worse than no round at all. A brief that cannot be answered "there is nothing here" is a brief that will be answered with something.

TWO THINGS ARE NAMED AS NOT-SUPERSEDED, because the tempting story is that migration makes them redundant: `_sibling_session_lookup` (L4.65) and the reaper's commit-based completion check. Both stay. Dirs will be stranded for the whole window between a round finishing and the step running, and during that window those two are the only reason anything works.
<!-- THOUGHT:END -->
