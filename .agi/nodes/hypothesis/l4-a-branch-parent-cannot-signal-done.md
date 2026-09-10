---
id: hypothesis:l4-a-branch-parent-cannot-signal-done
mint_id: a267f458e982449ab68c17d3716bea08
type: hypothesis
parents:
  - hypothesis:l4-reaper-restarts-a-committed-round-on-a-typed-id
  - goal:g4.7
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 18d4b5a80eb2f60f
season: 2
status: pending
tags:
  - l4
  - g4.7
  - dispatch
  - cli
  - worktree
testable_claim: "A `--branch` PARENT CAN NEVER SIGNAL DONE THROUGH THE TOOL, AND BOTH PARENTS I EXAMINED WORKED AROUND IT BY HAND. `dispatch.py:1270` sets `sess_dir = iter_dir / agent_id` and `:1632` writes `agent.json` there — the DISPATCHER's tree, and only that tree. A `--branch` parent runs in its OWN worktree, so `cli.py done`'s `_session_root()` finds nothing, and `_legacy_fallback` then falls back to the MAIN checkout — which for a SEAT-dispatched round is also the wrong tree, because the record is in the SEAT's worktree. Three trees, and the record is in the one nobody looks in. MEASURED, on two real rounds, do NOT re-derive: L4.55's parent reported the refusal verbatim (`no agent record at .../a00-9dd6f7bd/agent.json`) and said it hand-wrote its own record from the kid's shape; L4.56's parent left a child-side `agent.json` too, with a DIFFERENT key set (18 keys, no `slot`/`strategy`/`context_file`/`log_file`; L4.55's has 22 with them) — two hand-made records of different shapes, which is what a workaround looks like when nobody wrote the format down. Dispatch wrote neither: it writes exactly one, in the dispatcher's tree. THE SECOND HALF, AND THE REASON THIS MATTERS BEYOND ONE REFUSAL: even once the hand-written record makes `cli.py done` succeed, it writes `status: done` into the CHILD's tree, which the reaper never reads. Both rounds ended with `status: done` in the child worktree and `done-unreported` in the dispatcher's — two records for one agent, in two trees, that never reconcile. **That is why the reaper needs a git-commit signal at all**, and it means the commit-based completion check (landed 2026-09-10) is load-bearing rather than a belt. REQUIRED: (1) root-cause it yourself to file:line before writing — I have given you the lines, confirm them; (2) make the parent's `done` reach the record the reaper actually reads. Decide WHERE: either dispatch writes a record into the child's tree too and `cli.py done` reconciles both, or `cli.py done` resolves the dispatcher's tree from the branch/worktree fields already on the record it is updating. Say which you chose and why the other is worse. 🔴 DO NOT make `cli.py done` succeed by writing a record it then reads — a tool that creates the evidence it checks certifies nothing, and that is exactly the hand-written workaround with a nicer name. PROVED BY: (a) a test that a `--branch` parent's `cli.py done` updates the DISPATCHER's record, asserted on the file the reaper reads, not the one the parent wrote; (b) a test that the refusal path still refuses when there is genuinely no record — absence must stay distinguishable from a wrong lookup; (c) a fixture built from a REAL artefact: read `.agi/sessions/iter-L4.56/a00-04c03dd9/agent.json` and its child-tree twin at `/home/ubuntu/work/agi/.agi/worktrees/a00-04c03dd9/.agi/sessions/iter-L4.56/a00-04c03dd9/agent.json` before inventing one — they differ, and the difference is the bug; (d) `python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_completion.py -q` GREEN, paste the count. DISPROVED IF: the commit-based reaper check is weakened or removed on the grounds that this fix replaces it — it does not, keep both; the refusal path stops refusing on a genuinely missing record; a record is created by the checker; or any existing assertion is weakened. Do NOT touch `locations.py`, `write.py`, or the reaper's `_branch_has_done_commit`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: this round is subject to the machinery it repairs. Watch `spawn_budget.py status` for an `-r1` suffix and kill the `dispatch.py` WRAPPER if one appears."
thought_session: sanctuary-director-genIV-L4
title: Three trees, and the agent record is in the one nobody looks in
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-branch-parent-cannot-signal-done

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THIS NODE EXISTS BECAUSE I CHECKED A CLAIM I HAD ALREADY REPORTED, and it was wrong in the way that matters. In the reaper finding I named the upstream cause as "`cli.py done` refuses for a detached parent" and sent that to the prime. I had it from L4.55's parent's own struggle line and passed it on without measuring. Measuring it changed the answer: `cli.py done` is not broken. It is looking in the right place for a record that dispatch never puts there.

`dispatch.py:1270` sets `sess_dir = iter_dir / agent_id` and `:1632` writes `agent.json` into it — the DISPATCHER's tree, once, and nowhere else. A `--branch` parent lives in its own worktree. So there are three trees in play (child, seat, main), the record is in the seat's, and `cli.py done` looks in the child's and then falls back to main. A round dispatched against "fix `cli.py done`" would have gone looking in the wrong file.

The evidence that both parents worked around it is in the shapes, not in their reports. L4.55's parent SAID it hand-wrote a record from the kid's shape — 22 keys, carrying `slot`, `strategy`, `context_file`, `log_file`. L4.56's parent said nothing and left one too — 18 keys, without any of those. Two hand-made records of different shapes for the same job is what a workaround looks like when nobody wrote the format down, and it is a firmer proof than either agent's prose.

THE HALF I DID NOT EXPECT, and the reason this outranks the refusal: even after the workaround succeeds, the parent's `status: done` lands in the CHILD's tree, and the reaper reads the DISPATCHER's. Both rounds ended `done` in one tree and `done-unreported` in the other. Two records for one agent that never reconcile. So the git-commit completion signal I landed this morning is not a belt over a working braces — it is the ONLY signal that crosses the tree boundary, which is why the falsifiers here forbid weakening it on the grounds that this fix supersedes it.

The one thing I would not let a kid do is the tempting one: make `cli.py done` write the record it then reads. That turns the refusal green while certifying nothing, and it is the hand-written workaround with a nicer name. It is called out by name rather than left to the falsifiers, because it is the path of least resistance and it goes green.
<!-- THOUGHT:END -->

## Agent Notes
DESIGN CONSTRAINT, added mid-round on the prime L4-III's ruling and delivered to the live parent's inbox: this round found ONE HALF of a boundary the owner already asked about at 03:5xZ (L4.37's remainder, quoted in goal:g17.1) -- agent session dirs land in the MAIN checkout, not the seat worktree. A proposal that fixes only the completion path is HALF A DESIGN. Whatever home is proposed for the agent record must satisfy three things at once: (1) the iter dir belongs to the worktree that RAN the round; (2) shared state -- spawn budget, comms root, meter pins -- stays in MAIN through `locations.git_common_root` rather than moving; (3) a session-complete step MIGRATES the worktree's iter dirs into main, because `sessions/` is gitignored and a merge carries nothing across.

A THIRD INSTANCE OF THE SAME CLASS, found while delivering that constraint and worth more than the delivery: `send.py send <agent-id> <text>` run from a SEAT worktree wrote the inbox to `<seat>/.agi/sessions/inbox/<id>.md` and printed that path as success. Read from the agent's own worktree, `send.py peek <id>` returned `inbox for <id>: empty`. The message was never going to arrive. So the parent's agent record, the parent's `done` status and now the parent's INBOX are all split across the same tree boundary, and in every case the writer is told it succeeded. That makes point (2) above load-bearing rather than tidy: the comms root is named as shared state that must resolve to main, and today it does not. Measured 2026-09-10 against live parent `a00-400db3c3`; the message was copied into its own tree by hand so the round could receive it.
