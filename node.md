---
id: hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-while-the-suite-lock-is-held
mint_id: 816f8f743d89463cbaaaa6a2f5011c8e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 392aa55422bf18a7
season: 2
testable_claim: "(Prime 07:2xZ names it PAIR 1 under SM; SM residue 06:20Z: the grid_sync cron demotes nodes during a granted suite window. Measured: 23be45be6 -- experiment:a00-9608da10-ec05af demoted proved -> inconclusive_lean_proved:50 by the evidence gate inside the cron's `grid.py commit --all` while the gen 5 stamp window was open, leaving node dirt in MAIN that the stamp refuses by name (_node_dirt) and that the runner had to copy aside / checkout / restore by hand; every SM card since carries that recipe. Minted by sanctuary-master gen 6.) CLAIM (sequencing rule): (1) `grid.py commit --all` on the cron path (no --session) probes the suite lock <.agi/sessions>/verify-suite.lock BEFORE evidence_gate.enforce_on_disk, reusing verification.py's held/stale judgement (acquire_suite_lock / _suite_lock_guard -- one reader, never a second lock parser); (2) while the lock is HELD by a live pid the evidence-gate rewrite is DEFERRED for that tick -- no node file under MAIN is written, the ref writes for already-committed bytes proceed unchanged, and ONE named line goes to the cron log ('evidence gate deferred: suite lock held by pid N'); (3) the deferral is a tick, not a skip: the first commit --all after the lock frees demotes exactly what it would have; (4) a STALE lock (dead pid) never defers -- the gate runs as today. FALSIFIERS: a node rewritten in MAIN by the cron while a live pid holds the lock; a decisive unevidenced node still undemoted two ticks after the lock frees; a stale lock that blocks the gate; a second lock parser in grid.py. TESTS (<=3, fixture root, never the live tree): held lock (pid = the test's own) + one unevidenced proved node -> commit --all leaves the node byte-identical, prints the deferred line once, refs still written; lock removed -> the next commit --all demotes it; lock naming a dead pid -> demoted on the first call. FILE SCOPE: grid.py (the commit --all path around enforce_on_disk), verification.py only if the held/stale probe must be factored into a callable, tests/test_grid_*.py or test_evidence_gate.py. CEILING: <=20 production lines, ONE kid, re-brief SM past 2x. Measurement after landing: a suite window with the cron live ends with zero cron-dirty nodes (the copy-aside recipe leaves every SM card)."
title: L4 the grid cron evidence gate defers its main tree rewrite while the suite lock is held
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-while-the-suite-lock-is-held

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 6 REVIEW BY NAME of SM.88 (director tip 4af420502, kid a00-be5c5e6e): ACCEPT :85. On the MERGE RESULT (throwaway detached tree at 946404985 + git merge --no-commit 4af420502): test_grid_evidence_gate_defer + test_evidence_gate + every test_grid* = 261 green. grid.py commit --all (cron path, no --session) probes the suite lock through verification.acquire_suite_lock -- the ONE reader, no second parser -- and on a LIVE foreign holder defers the evidence-gate rewrite for that tick with exactly one stderr line naming the pid, while the ref writes proceed (node byte-identical, versions == 1); the first commit --all after the lock frees demotes (tick, not skip); a dead-pid lock never defers. Tests drive grid.py as a subprocess, so the test's own pid is a real foreign holder. Production 18 net / 20 = 0.9x. RESIDUE (not a demote; verification's own _suite_lock_guard shares it): the probe is acquire-then-unlink, so a suite starting in the same microseconds sees the cron's pid and refuses once -- a read-only held/stale probe in verification.py would close that window for both callers. Lands by SHA on the Prime's GO; the ONE stamp follows SM.89.
