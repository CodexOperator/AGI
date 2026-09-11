---
id: experiment:a00-a0199077-a74dce
mint_id: 8b7e609504a84341aad200793391e8c4
type: experiment
parents:
  - hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp
next_edges: []
confidence: 0.95
edited_by: a00-998f84ec
evidence_runs:
  - experiment:a00-a0199077-a74dce
loop: hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 850ab1d8bb3b4503
season: 2
title: A00 a0199077 a74dce
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a0199077-a74dce

## Experiment

A g15 CLAIM (behavior to build, not measure) — extension/agi/tests/test_workflow.py
predated the tmp-path tracking seam, so a suite run appended a phantom row to
the production `.agi/sessions/workflows/review.jsonl`. Measured the pre-fix
defect, built both halves of the claim, and proved it on the built bytes.

**Claim (1) — :630 redirected to the tmp seam.** `test_claude_code_path_feeds_
the_same_view` (:630) ran a NON-dry claude-code workflow against the REAL
project root, so `_track_run` (workflow.py:1186 → `_loc.shared_project_root`
→ `sessions/workflows/review.jsonl`) appended one phantom row per suite run. I
rewrote it to take `tmp_path_factory` and redirect TRACKING through the same
`_tmp_session_root` seam its neighbours (:664/720/739) already use —
monkeypatching the `_loc.shared_project_root` RESOLVER for the duration, never
the real path — and it now additionally asserts the tracking row landed ONLY
inside the tmp seam (`tmp/sessions/workflows/review.jsonl`, len==1).

**Claim (2) — suite-wide guard pins the class.** Added a session-scoped
autouse fixture `_no_workflow_row_leaks_to_real_sessions` (in test_workflow.py;
conftest has no per-file scope and this is a workflow-suite property) that
snapshots every real `.agi/sessions/workflows/*.jsonl` line count at session
start and asserts them IDENTICAL at session end, so any future non-dry test
that leaks a row is red on its next instance.

**Claim (3) — real file untouched.** The 240/241 phantom rows are state, not
edited; I added no status flag and removed nothing.

## Evidence

Pre-fix falsifier (`pytest extensions/agi/tests/test_workflow.py -q`):
```
before: 238 lines of .agi/sessions/workflows/review.jsonl
48 passed; after: 239  ->  delta +1 (phantom row)   [confirmed leak]
-k claude_code_path_feeds_the_same_view -> delta +1 (the offender)
-k pi_live_run_renders_tree_through_view -> delta +0
```
Post-fix falsifier (run twice as the claim demands):
```
run 1: before 241, 48 passed, after 241 -> delta 0
run 2: before 241, 48 passed, after 241 -> delta 0
```
Guard falsifier (temporarily removed the redirect — leak restored):
```
E AssertionError: workflow tests leaked rows into the real sessions dir
  (changed/added: ['.../sessions/workflows/review.jsonl'])
1 passed, 47 deselected, 1 error  ->  guard goes RED on a leak
```
After restoring the fix: 48 passed, delta 0 twice — guard green, no leak.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-998f84ec, L4.286). (1) INSTRUCTION: claim (1) redirect :630 to the seam, (2) suite-wide guard pinning the class, (3) do not prune the real file. (2) MACHINE: read the diff, not the report — git diff --cached -- extensions/agi/tests/test_workflow.py shows test_claude_code_path_feeds_the_same_view now takes tmp_path_factory, calls the existing _tmp_session_root seam (monkeypatching _loc.shared_project_root, test_workflow.py _tmp_session_root), and asserts len(lines)==1 under tmp; the new session-scoped autouse fixture _no_workflow_row_leaks_to_real_sessions snapshots/compares real *.jsonl line counts. Independently re-ran: pytest extensions/agi/tests/test_workflow.py -q -> 48 passed; shared_project_root resolved to /home/ubuntu/work/agi/.agi; line count before=262 after=262, delta 0 (the kid measured 241->241; absolute count moved because other rounds ran, the DELTA is the claim and it holds). (3) NEAR MISS: the plausible-but-wrong fix is passing a tmp path as the run ROOT (run_workflow(tmp)) — that satisfies "no row in the real dir" by making the whole run synthetic and loses the property under test (that a real claude-code run writes exactly one row). The kid kept the real root and redirected only the sessions RESOLVER, which is the correct seam. A second near miss: a guard asserting only pre-existing files are unchanged misses a NEW *.jsonl key created by a leak — the fixture covers that with the after-not-in-before set union. (4) DEVIATION: none from standing rule; file scope honoured (test_workflow.py only, no conftest, no workflow.py). Real file untouched per claim (3). Proved is accepted: evidence_runs names this same experiment, which is the run itself.
<!-- THOUGHT:END -->

## Agent Notes
Fixed test_workflow.py:630 to redirect tracking to the tmp_path_factory seam and added an autouse session guard in test_workflow.py that asserts real sessions/workflows/*.jsonl line counts are unchanged across the suite; pre-fix +1 phantom row/run, post-fix delta 0 across two runs, guard proven red on a deliberate leak. Real file not pruned.

Parent a00-998f84ec accepted proved: reviewed the artifact (diff, not report); 48 passed and real-sessions delta 0 reproduced independently. Claim (1)+(2)+(3) all present in test_workflow.py; workflow.py untouched per file scope. Parents link resolves; evidence_runs names the run itself.
