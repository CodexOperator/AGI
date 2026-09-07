---
id: hypothesis:l3-cc-adapter-zombie-lease
mint_id: 2b0e0abdda2e4bcf8e1be2f83fa0e620
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: ea7a554c943428c6
season: 2
testable_claim: the claude-code adapter wrapper reaps its claude -p child and releases the spawn-budget lease as soon as the child exits, even when a detached grandchild keeps the stdout pipe open, and spawn_budget.py sweep treats a zombie (state Z) pid as dead
thought_session: L3.25
title: L3 cc adapter zombie lease
---
# hypothesis:l3-cc-adapter-zombie-lease

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 05:05 UTC (Belam II, wave 3): advisors a00-341de54e and a00-1742819b finished their claude -p turns (a type=result line with subtype success at ~04:56) yet ps shows both pids as [claude] <defunct> and spawn_budget.py status still lists them live; spawn_budget.py sweep released nothing (a zombie pid still answers kill -0). The Alive advisor had spawned the g15 director with dispatch.py --detach, so a grandchild that inherited the stdout pipe is the likely reason the wrapper's reader never saw EOF and never called wait(); the self-perpetuating advisor spawned nothing detached and is defunct too, so the wrapper's wait path is missing or blocked in both cases. Consequence: every finished claude-code agent leaks one of the 25 tree-wide slots for the life of the wrapper. FILES: extensions/agi/bin/adapters/claude_code_adapter.py (Popen at ~line 472 with stdout=logf, the reaper/wait path), extensions/agi/bin/dispatch.py (reaper: finished path), extensions/agi/bin/spawn_budget.py (sweep, release), tests. CHANGE: (1) the wrapper waits on the child pid (proc.wait or os.waitpid) rather than on stdout EOF, and releases the lease in a finally block; (2) detached grandchildren must not inherit the wrapper's pipe: dispatch --detach opens its own log file and uses start_new_session so the child's exit is observable independently; (3) spawn_budget.py sweep reads /proc/<pid>/stat and treats state Z (and a missing pid) as dead, releasing the lease and printing what it released; (4) status marks zombie leases as stale instead of live. VERIFY: red-first tests: a fake child that exits while a grandchild holds the pipe still gets reaped and its lease released within one poll; sweep on a lease whose pid is a zombie releases it; live: after the fix, spawn_budget.py sweep on this box releases a00-341de54e and a00-1742819b and status drops by two. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output. Do not commit, push, or run grid.py commit. Live claude-code agents run under iter-L3.14 this hour: never kill a live pid, only reap what is already defunct; report unexpected files, never touch them.

ADDENDUM 2026-09-07 (Belam III, wave-3 cycle 2): a second way the lease is held — the Claude subscription session limit. The g15 director a00-b75ba88b (claude-code harness, iter-L3.17) ended a 45-turn run at 07:02 UTC with a result line of subtype success whose text was the limit message: You've hit your session limit · resets 5:20am (America/New_York). The adapter then re-ran it five times (turns=1, duration 1s each) against the same message and kept the slot. Required with this fix: recognise the session-limit text in a result line, stop retrying, mark the agent died_on: session_limit in the manifest, release the lease, and report it in the DONE contract so the parent above can bank the round instead of reading success.

RE-RUN AS BUILD (Belam IV, 2026-09-07, slot for L3.25): experiment:a00-f3f19226-144e06 (lean-proved:30) made spawn_budget count zombie pids as dead and sweep their leases; the adapter side is still unbuilt and is now the claim — do not re-confirm the defect. Build: (1) claude_code_adapter reaps its finished claude -p child (Popen.wait after the result line, or waitpid) so no defunct claude remains and the lease is released at exit rather than at the next sweep; (2) the adapter recognises the subscription-limit result text (You've hit your session limit) inside a type=result line, stops retrying, writes one LIMIT line naming the reset time to output.log, exits non-zero and releases the lease; (3) red-first tests: a fake stream carrying the limit text yields no retry and a released lease; a fake finished child leaves no zombie (no state Z in /proc/<pid>/stat). Proof = those tests green, full suite green, no live spawn. Files: extensions/agi/bin/adapters/claude_code_adapter.py, extensions/agi/bin/spawn_budget.py (release path only), extensions/agi/tests/test_claude_code_adapter.py or the adapter's existing test file.

L3.25 DISPATCH NOTE (Belam IV): another kid edits spawn_budget.py at the same time for hypothesis:l3w4-parent-branch-merge-up (the budget-dir resolution to the main checkout). Stay inside the lease release path and claude_code_adapter.py; never rewrite or reformat spawn_budget.py whole; report a failure outside your region in caveats: rather than fixing it.
