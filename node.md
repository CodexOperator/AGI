---
id: hypothesis:l4-the-parents-last-line-is-a-self-check
mint_id: 7b8d9989833443cb8d8c831efe76b786
type: hypothesis
parents:
  - hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit
  - goal:g4.7
next_edges: []
edited_by: sanctuary-director
scaffold_hash: bd1b71598eae4731
season: 2
status: pending
tags:
  - l4
  - g4.7
  - dispatch
  - brief
testable_claim: "THE PARENT'S TERMINAL STEP IS AN INVARIANT HANDED TO A MODEL, SO IT BECOMES AN EXPLICIT, SELF-CHECKING, LAST LINE OF THE BRIEF. THIS IS THE PRIME'S SPEC AND IT IS NOT YOURS TO REDESIGN -- quoted: *the parent's terminal step becomes explicit, self-checking and LAST in the brief -- \"if every kid is terminal and you have not run cli.py done, you are not finished\", with the exact command on the line. Last, not buried; recency is the only lever a weak model reliably answers to.* MEASURED CAUSE, do NOT re-derive it (`experiment:a00-f2f8465a-b4eb8e`, L4.75): two parents this loop idled ~45 minutes at ~0.4% CPU with both kids terminal and the work staged, and they NEVER REACHED `cli.py done` AT ALL. Proof: `cmd_done` writes `status` and `finished_at` into the record BEFORE `_auto_commit_worktree` runs, and both dispatcher-side records still read `status: running`, no `finished_at`, mtime equal to spawn. And `done` would NOT have refused -- the exact resolution it performs resolves `exists=True` from each parent's own worktree, and from the parent's own tree `cli.py status` printed every kid as `done`. The poll loop had everything it needed to terminate and did not. It is parent-loop judgement, not a code defect, which is why the remedy is the BRIEF. REQUIRED: in `dispatch.py`'s parent brief assembly, the terminal step becomes the LAST thing the parent is told, stated as a SELF-CHECK it can apply to itself rather than as a step in a list -- and carrying the literal command with its real flags, the same ones the brief already specifies (`cli.py done <iter> <agent-id> --verdict pending --owns <kid-node-id> ...`; read what the brief assembles today and match it exactly, including that a parent uses `--owns` and NOT `--node-id` because it authors no node of its own). 🔴 LAST MEANS LAST. The existing brief already ends with an `--append-system-prompt` carrying `lib/agent-prompt.md` and then the 'Begin iteration ...' line; work out what actually arrives last in the assembled prompt and put the self-check there, rather than assuming the order of the code is the order of the prompt. Say in your node HOW you established what lands last. 🔴 NOTHING ELSE IN THE BRIEF IS REMOVED OR REWORDED. The instruction `DO NOT commit, push, or sync` is CORRECT and stays -- `cli.py done` is what commits (`cli.py:677` -> `_auto_commit_worktree`), so the parent genuinely must not commit by hand. Do not 'resolve' that as a contradiction; it is not one. PROVED BY: (a) a test that the assembled PARENT brief contains the self-check, and that it is the LAST line -- assert on the built command/prompt, never on a live agent; (b) a test that the self-check carries the literal `cli.py done` invocation with `--owns`, so a parent cannot be told to run a command it must then guess the flags for; (c) a test that a KID's brief does NOT gain it -- a kid authors a node and signals differently, and a self-check aimed at the wrong tier is noise that trains agents to skip the end of the brief; (d) a test that the pre-existing brief content is unchanged -- assert the `DO NOT commit` instruction and the kid-ceiling line still appear; (e) `python3 extensions/agi/bin/dispatch.py . L4.99 --target <any node> --tier parent --dry-run` prints the brief with the new last line -- paste its tail; (f) `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_dry_run.py -q` GREEN, paste the count; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: the self-check is not last; it lacks the literal command or uses `--node-id` for a parent; a kid's brief gains it; any existing brief text is removed or reworded; `DO NOT commit` is changed; an existing test is edited (🔴 and if one MUST be, the replacement asserts the SPECIFIC fact the old one obscured IN ADDITION to whatever it counted -- never merely relaxes the constraint; the prime's standing standard); or the fix is attempted in `cli.py` or the reaper instead of the brief. Do NOT touch `provisioning.py` (two rounds just landed there), `cli.py`, or `_branch_has_done_commit`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE, and it is the joke that keeps writing itself: THIS ROUND'S OWN PARENT IS THE THING BEING FIXED. If it idles with the work staged that is data, but the director watching will kill it. Commit early."
thought_session: sanctuary-director-genIV-L4
title: An invariant handed to a model is a coin flip; recency is the only lever it answers to
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-parents-last-line-is-a-self-check

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE PRIME OWNS THIS ONE AND SAID SO. It ruled that a terminal step handed to a model is an invariant turned into a coin flip, and that the remedy is the brief -- explicit, self-checking, LAST. I am dispatching it with that spec verbatim rather than my improvement of it, because a director redesigning a ruling it was handed is the same move as a kid loosening a falsifier.

WHAT IS MINE IS THE EVIDENCE UNDERNEATH, and it is unusually clean: L4.75 proved the parents never reached `done` at all, using the fact that `cmd_done` writes the record BEFORE it commits -- so an untouched mtime and an absent `finished_at` rule out 'reached it and failed inside'. Without that, the obvious fix would have been another patch to the record seam, and three of my merge-ups were already spent there. A brief change is only defensible because the code was exonerated first.

THE INSTRUCTION MOST LIKELY TO BE GOT WRONG IS 'LAST', which is why it has its own falsifier and its own demand for method. The parent brief is assembled from many `--append-system-prompt` fragments plus a trailing 'Begin iteration ...' line, and the order of the CODE is not obviously the order of the PROMPT. A kid that appends its self-check where the code reads last, rather than where the prompt ends, satisfies the letter and loses the entire mechanism -- recency is the lever, and a self-check in the middle is just more middle. So the brief asks it to say HOW it established what lands last.

I ALSO FORBADE THE TEMPTING CLEANUP TWICE OVER: `DO NOT commit, push, or sync` stays. I nearly briefed a round to hunt that as a contradiction before I grepped `cli.py:677` and found that `done` is what commits. A kid arriving at this brief with fresh eyes will see the same apparent conflict I did, so the node tells it the answer rather than letting it spend a kid on the discovery I already paid for.
<!-- THOUGHT:END -->

## Agent Notes
LANDED BY THE DIRECTOR, NOT BY A ROUND, and the dispatch that failed is recorded here rather than quietly retried. I dispatched this as L4.77 to parent `a00-20cf47c7`. It ran 25 minutes at ~1.0-1.3% CPU, spawned NO kid, changed NO file, and burned **$0.2156** on `account.used` ($88.0995 -> $88.3151) -- more than twice a successful round, for nothing. I killed it and swept twice by PID.

I CHECKED MY FIRST EXPLANATION AND IT DID NOT HOLD, so I am not asserting it. My instinct was that the brief was too long: this claim is 718 words. But the four rounds before it are 676, 674, 662 and 653 words and all landed. Length is in the same band, so length alone does not explain it. One failure, cause unknown, cost measured. That is the whole honest reading.

WHY I THEN LANDED IT BY HAND RATHER THAN RETRYING: this round IS the exception my own brief names. A parent dispatched to fix the parent brief is reading, as its own instructions, the very text it was sent to change -- the same shape as the reaper fix that could not be dispatched to the reaper. Having already paid $0.22 to learn that, spending another round to relearn it would be a decision made by momentum.

WHAT LANDED, and where, because the placement was the hard half. The self-check is in `brief.closing_line`'s parent branch, NOT in the parent's system fragments. `closing_line` is appended by `adapters/pi_adapter.py` as the USER TURN, after every `--append-system-prompt`, so it is literally the last thing the parent reads -- which is what the prime's ruling requires and what a fragment placed 'at the end of the list' would NOT have achieved. I established that by building the real command: 21 args, and arg 21 is the user turn ending with the self-check. `cli_py` is threaded from the adapter so the line carries the actual command with `--owns` rather than a shape the parent must reconstruct; it stays optional so every existing caller and test keeps working.

Three tests: the self-check is the TAIL of the parent's line (asserted by splitting on it and checking nothing from the original instruction follows), it carries the real command with `--owns` and names why not `--node-id`, and NO other tier gains it -- a self-check aimed at the wrong tier is noise, and noise at the end of a brief teaches agents that the end of a brief is skippable. Nothing existing was removed or reworded: `DO NOT commit, push, or sync` stands, because `cli.py done` is what commits.
