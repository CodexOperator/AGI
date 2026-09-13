---
id: hypothesis:l4-the-heal-wait-on-a-live-stalled-record-is-a-bounded-seamed-poll-with-declared-semantics-never-a-thirty-minute-sleep
mint_id: f028ebae4ae64afca200daf99cb37cd1
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: f34861563e8aaa2b
season: 2
testable_claim: "goal:g15.25 SM.23b (RED re-land; belam XX 20:45Z: the SM.23 residue-(iii) hunk set all_terminal=False for a LIVE-stalled record, which sent the pre-existing test_heal_leaves_a_live_pid_stalled_record_untouched into its real time.sleep(30) poll up to a 30-min max-wait → rc 2 → 3 verify-suites over the 1800 s ceiling, 0 greens since the merge; \"182 green\" was a parent subset; the Prime reverted that ONE hunk at 912363623, everything else of SL2#30 kept; test_heal + test_heal_watch 80 passed 1.9 s after). MEASURED on season2/main @912363623: name the wait function and the line where the live-stalled branch `continue`s before all_terminal (the exit-0 misreport the residue meant to fix) and the test line that sleeps. CLAIM: (1) SEMANTICS, declared in the wait docstring: a record whose pid is ALIVE but status stalled is NOT terminal — the pass reports all_terminal=False AND returns after the pass (the wait loop never blocks on a live-stalled record; the caller re-polls on its own cadence — the watch every 30 s, the inline lane once); the exit code of the inline lane on a live-stalled-only set is the named non-zero \"not terminal yet\", never 0 (the misreport fixed) and never a 30-min hang; (2) SEAM: the poll sleep + clock are module-level seams (`_sleep`, `_now`) the tests inject — no test calls time.sleep; the max-wait is a parameter with the same default as today; (3) test_heal_leaves_a_live_pid_stalled_record_untouched is rewritten to the contract: one pass, record untouched, all_terminal False, rc = the named code, wall < 1 s; +1 test that a dead-stalled record IS terminal via the SM.23 predicate; (4) FULL suite green BEFORE the merge-up push — the harvest line to me carries the full-suite numbers (n passed / wall s), never a subset. FALSIFIERS: any time.sleep reachable from the heal tests; a live-stalled set that returns rc 0; a wait that blocks past one pass on live-stalled; a subset count reported as the suite. TESTS: the rewritten test + 2 new (<= 3), full suite green with wall time reported. FILE SCOPE: heal.py wait function + the seams; test_heal.py / test_heal_watch.py. CEILING: <= 40 production lines. Order: TOP — before SM.25 (RED re-land; the reaper unit restart still waits on it)."
title: "SM.23b re-land: the heal wait semantics for a LIVE-stalled record are decided and declared (a live pid that stalled is NOT terminal → all_terminal=False; the loop returns after ONE bounded pass, never blocks the caller), the poll is seamed (injectable sleep + clock) and the pre-existing test asserts the new contract without a 30 s sleep — the residue (iii) hunk the Prime reverted at 912363623 after 3 suites blew 1800 s"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-heal-wait-on-a-live-stalled-record-is-a-bounded-seamed-poll-with-declared-semantics-never-a-thirty-minute-sleep

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
