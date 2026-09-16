---
id: hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-logged-by-name-never-a-real-failure
mint_id: 630428a8d09749ec84c678ff0110c0ca
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ef502b92fe00b02b
season: 2
testable_claim: "Measured 2026-09-16 (SM gen 3, Prime XXIII ruling 12:17Z): a transient upstream 5xx on the pi route kills the unit of work instead of being retried. Bytes: workflow.py:1413 _run_stage_pi runs ONE subprocess.run of `pi -p` (1464-1467); any rc != 0 returns (3, None) at 1474-1480 with no classification, so a stage whose whole output is the pi catalogue warning plus `error code: 520` (my runs mur-sm-36 11:57Z and mur-deepseek-deepseek-v4-1-flash-sm-36, SD.05) fails the workflow at once; dispatch.py:2507 Popens a round kid detached and returns, so a kid that dies at its FIRST call with the same bytes (iter-TM.07/a00-1fec07a8/output.log = two lines: the catalogue warning, `error code: 520`; no commit, no node) is a dead round nobody re-runs. The tilde model id is NOT the cause (SL7.130 kid a00-f6bca347 runs on it, billed on its own key): `Model not found for provider openrouter - using custom model id` is pi own local catalogue warning and prints for the working ids too. CLAIM: (1) _run_stage_pi classifies a failed attempt as TRANSIENT when rc != 0 AND the output tail matches `error code: 5\\d\\d` (or an HTTP 5xx / connection-reset signature) AND no schema-valid JSON candidate was produced, and retries only that class, bounded at 3 attempts with backoff 15/45/135 s, each attempt logged by name into the run record (stage label, attempt n, signature, sleep); a non-transient rc != 0, a timeout and a parse error are NOT retried and keep their rc 3/2/4; (2) the dispatcher, after Popen, polls the child for a bounded startup grace (20 s, 2 s steps): a child that exits within it with rc != 0 whose output.log holds ONLY the catalogue warning and/or 5xx signature lines and no other bytes is re-spawned under the SAME lease, agent id, worktree and log (an `attempt n` line appended) with the same backoff, bounded at 3; a child that exits 0, exits with other output, or outlives the grace is never touched; the fourth failure refuses by name and releases the lease as today. FALSIFIERS: a stage retried on a failure without the 5xx signature or after a schema-valid candidate; a stage or kid retried more than 3 times; a retry with no by-name line in the record/log; a kid re-spawned after it wrote anything but the signature bytes; a dispatch that blocks longer than the grace on a healthy child. TESTS (<=7, fixture pi stub scripts, no live spawn, no network): stub fails 520 twice then returns valid JSON -> stage ok, record names 3 attempts and the sleeps (sleep injected, never real); stub fails rc 1 without the signature -> rc 3, one attempt; stub times out -> rc 2, one attempt; stub fails 520 four times -> rc 3 with attempts=3 named; dispatch fixture child exits 1 within the grace with signature-only log -> attempt 2 line, same agent id and lease; child exits 0 within the grace -> untouched; child alive past the grace -> dispatch returns as today. FILE SCOPE: workflow.py (_run_stage_pi and its caller at ~1699), dispatch.py (the Popen site ~2507 and the lease/commit lines after it), test_workflow.py, test_dispatch*.py. CEILING: <=60 production lines across <=2 kids (one per runner) -- re-brief SM past 2x."
title: L4 the pi runners retry a transient 5xx with bounded backoff logged by name never a real failure
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-logged-by-name-never-a-real-failure

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
