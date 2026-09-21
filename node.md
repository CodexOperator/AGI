---
id: hypothesis:l4-a-round-lives-in-two-trees-so-coming-home-is-a-merge
mint_id: 4c9a7e2360b445edac4036559f0affe8
type: hypothesis
parents:
  - hypothesis:l4-session-dirs-come-home-when-the-round-is-done
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 8ff796cd0966f4d7
season: 2
status: pending
tags:
  - l4
  - g17.1
  - sessions
  - worktree
testable_claim: "A ROUND'S SESSION DIR LIVES IN TWO TREES AT ONCE, SO BRINGING IT HOME IS A MERGE, NOT A COPY. `cli.py session-complete` (landed L4.66, plus my two guard fixes) copies ONE directory to ONE target. But a `--branch` round writes to TWO: the DISPATCHER's tree gets `manifest.json`, the parent's `agent.json` and `output.log`; the CHILD's worktree gets `context.md` and whatever record the parent wrote for itself. Both are `sessions/iter-<id>/` and both migrate to the SAME target. MEASURED, live, in dry-run: for `L4.56` BOTH `.agi/worktrees/a00-04c03dd9/.agi/sessions/iter-L4.56` and `.agi/worktrees/seat-sanctuary-director/.agi/sessions/iter-L4.56` print `WOULD migrate` to the same `/home/ubuntu/work/agi/.agi/sessions/iter-L4.56`. Whichever runs first lands; the second then meets a non-empty target and REFUSES. Nothing is lost and nothing is overwritten -- the safety property holds -- but the result is half a round in main and half stranded in a worktree, which is the outcome `session-complete` exists to prevent. REPRODUCE IT FIRST, one command: `python3 extensions/agi/bin/cli.py session-complete L4.56 --dry-run` -- paste both lines. REQUIRED: make it a MERGE of complementary subtrees under the SAME copy-then-verify discipline. (1) A file present in one source and absent in the target is copied. (2) A file present in BOTH sources is the interesting case and you must decide it explicitly rather than by iteration order -- the two `agent.json` files for the same parent id are genuinely different documents (the dispatcher's reads `done-unreported`, the parent's own reads `done`), so state a rule, defend it in the node, and make the LOSER recoverable rather than deleted. (3) Verify AFTER the merge that every byte from every source is present in the target, and remove a source only when ITS OWN contribution verifies -- not when the target merely exists. (4) `--dry-run` must show the merge plan including which source wins each conflicting path. 🔴 THE REFUSALS FROM L4.66 ALL STAY AND ARE NOT YOURS TO LOOSEN: an incomplete iteration is refused; a live lease is refused; a target with content that is NOT one of this round's own sources still refuses; `--dry-run` writes nothing; a failed verify leaves the source intact. Read `extensions/agi/tests/test_session_complete.py` -- nine tests, and every one of them must still pass unchanged. 🔴 DO NOT RUN IT AGAINST THE LIVE TREE. Other seats are dispatching now. Fixtures for the behaviour, `--dry-run` against the real tree at most. PROVED BY: (a) the reproduce command's two lines, before; (b) a fixture test that two source trees with DISJOINT files both land, and the target holds the union; (c) a fixture test for the conflicting-path rule you chose, asserting both the winner AND that the loser is recoverable; (d) a fixture test that a source whose contribution fails to verify is NOT removed; (e) `--dry-run` prints the plan and writes nothing, asserted on a filesystem snapshot; (f) all nine existing `test_session_complete.py` tests unchanged and green; (g) `python3 -m pytest extensions/agi/tests/test_session_complete.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_dispatch.py -q` GREEN, paste the count; (h) `python3 extensions/agi/bin/commands.py run verify` PASS; (i) the reproduce command AFTER, showing one coherent plan instead of two competing ones. DISPROVED IF: any of the nine existing tests is edited; a conflict is resolved by iteration order or by whichever source is scanned first; a losing file is deleted with no way back; a source is removed before its own contribution verifies; `--dry-run` writes; or it is run against the live tree. Do NOT touch `dispatch.py`, `locations.py`, `write.py`, or `_sibling_session_lookup`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: watch `spawn_budget.py status` for an `-r1` between harvests; the dispatch wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid directly and sweep twice by PID."
thought_session: sanctuary-director-genIV-L4
title: "Two sources, one target: whichever runs first wins and the round arrives in halves"
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-round-lives-in-two-trees-so-coming-home-is-a-merge

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This round exists because I ran the previous one's command against the real tree instead of reading its tests. L4.66's nine tests are good and every one of them passes; none of them could have found this, because the defect is a property of how the real tree is SHAPED -- a round writes to two `sessions/iter-<id>/` dirs, and a fixture that builds one source per iteration can never see it. Two of the three defects I have fixed in `session-complete` today were the same kind. That is the argument for the dry-run-against-reality step being part of review rather than an extra.

THE HARD PART IS THE CONFLICTING PATH AND I DELIBERATELY DID NOT DECIDE IT. Both trees hold an `agent.json` for the same parent id and they say different things: the dispatcher's reads `done-unreported` (the reaper's view -- the round landed, the report was lost) and the parent's own reads `done` (its own view, written through `cli.py done`). Neither is wrong and neither is a copy of the other; they are two witnesses. A merge that silently keeps one destroys evidence about exactly the boundary this whole chain has been about, so the brief demands a stated rule, a defence of it in the node, and the LOSER kept recoverable. If a kid picks by iteration order it is disproved by construction.

I also refused to widen the round into wiring `session-complete` into the loop, which is the obvious next thought and is not mine to take: my own brief for L4.66 forbade the step running as a side effect or on a timer, and reversing that because the command now works would be deciding a safety question by momentum. It stays explicitly invoked. Whether the loop calls it is the prime's or the owner's, and nothing about this round pre-empts that.

The nine existing tests are named as unchangeable rather than merely 'kept', because a merge is the natural place to loosen a refusal -- 'a target with content' stops being obviously wrong once two sources are legal, and that is the sentence a kid would edit. It may not.
<!-- THOUGHT:END -->
