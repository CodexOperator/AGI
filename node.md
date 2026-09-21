---
id: hypothesis:l4-the-full-suite-runs-under-600-s-solo-real-waits-and-process-reaps-are-seamed-not-slept
mint_id: 39a5ebc2e1714c2fa3c9777e298451b1
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 6f65d12134ad6bdd
season: 2
testable_claim: "goal:g15 SM.30 (Prime XX 01:12Z: the tests leg read 471 -> 519 -> 724 s in three runs 2026-09-13; 590 s was the ceiling flag, 1800 s the wrapper; the claim is a NUMBER, full suite under 600 s solo). MEASURED from the point 19:36Z run (--durations=15, 4766 passed in 519 s, load ~7 on 4 cores): slowest 15 sum 131 s, of which test_rotation_alerts.py:126 test_after_join_dm_to_silent_post_refused and :171 test_after_join_type_seam_to_silent_never_fires read 20.00 s EACH — they call rotate.run_after_join without delay_override, so they sleep the REAL DEFAULT_AFTER_JOIN_DELAY_S = 20 (rotate.py:11853; delay_override exists :12632/:12685 and 0 is honoured); test_rotate_selfreap.py test_reap_belam_oldest_pane_seam_detached_tree 18.76 s + test_reap_chain_detached_nonchild_no_error 9.67 s (real process reaps); test_node_writer.py live-tree round trips 9.87 + 9.71 s (real 3k-node corpus, twice); test_grid.py corpus round trip 5.43 s; the rest of the top 15 are 4-6 s rotate/heal fixtures. The 724 s run coincided with a 15-agent review workflow on the same 4 cores — load, not tests, explains the spread; xdist and pytest-timeout are NOT installed (measured). CLAIM: (1) no test sleeps a production default: the two after_join tests pass delay_override=0 (-40 s); every other `time.sleep`/real-wait in tests (39 sleep sites measured by grep) is either a seam or <= 0.2 s — the kid lists each with its reason in the experiment; (2) the two node_writer live-corpus round trips share ONE session-scoped corpus load (or one test proves both properties) (-10 s); (3) the selfreap real-process tests keep their real reaps but bound them: a reap that waits for a child uses the seam already present in rotate (the kid measures why 18.76 s and names the wait); (4) verification.py --suite records the wall time and the slowest-15 table into .agi/sessions/verify-suite-ts.json beside suite_ran_at, so the next ceiling round measures from the record, not a scratch log; (5) ACCEPTANCE = a solo run (no other pytest/workflow on the box; the kid records loadavg at start and end) under 600 s, with the number in the experiment. FALSIFIERS: a solo run over 600 s after the round; any test that still sleeps a production default; a removed assertion. TESTS: the two after_join tests re-run singly under 1 s each; the suite number. FILE SCOPE: the named test files, verification.py (record only), rotate.py ONLY if a seam is missing for (3). CEILING: <= 40 production lines across <= 2 kids; assertions are never weakened to buy time."
title: L4 the full suite runs under 600 s solo real waits and process reaps are seamed not slept
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-full-suite-runs-under-600-s-solo-real-waits-and-process-reaps-are-seamed-not-slept

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.30 reviewed by name (mur-sl2-33): ACCEPT with residue. Reap-wait seaming 40s to 1.35s with no assertion weakened or deleted (asserts diffed, refuter reproduced); a Prime-tier production run observed during review stamped 485.379 s through the new plumbing. Residue 1: conjunct 5 (a SOLO run with loadavg recorded) was never produced, verdict honestly inconclusive_lean_proved:80 with evidence cited - close it when the box is quiet. Residue 2: verification.py:545-556 records suite_wall_s/slowest_15 with no status or counts beside them. 51 vs 40 lines disclosed, under the line, note only.
