---
id: hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning
mint_id: a4bf00b9b8734523b58f9736d2358646
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 3578a2a12ba938b3
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Sensei wake-audit of belam XV->XVI 141419Z, code line P4: the Prime's call 148 removed a stale hook latch by hand). Cite at seat tip 75120ad7c (all ten digest rounds merged; SL7.46/48/49/52 moved rotate.py lines); re-measure on your base. MEASURED: the rotation_alert hook latches once per generation at <sessions>/<_LATCH_SUBDIR>/hook-<seat>-gen<gen>.lock (rotation_alert.py:741-751, gitignored) holding pid <n> of the rotate-self it spawned (_latch_holder_pid :754, _latch_held :769); the hook releases a DEAD latch only on its own next run (test_dead_latch_is_released_and_rerotates), so a latch left by a rotate-self that died (or whose pid was reused) blocks nothing but sits there until the hook fires again, and a Prime that notices it spends a wake call. rotate-self itself never looks at latches before spawning. CLAIM: rotate-self, in its prepare/spawn step, sweeps every hook-<seat>-gen*.lock for ITS seat whose holder pid is not alive (os.kill(pid, 0) fails, or pid unparseable) — unlink + one stderr line naming each swept file — before spawning the successor; a latch whose pid is alive is left alone; the sweep is best-effort and never refuses the rotation. FALSIFIERS: a dead-pid latch survives a rotate-self; a live-pid latch is removed; a sweep failure aborts the rotation; the hook's own dead-latch release changes. TESTS: test_rotate_handover.py (or the rotate-self spawn tests) — dead latch swept and named; live latch kept; unreadable latch swept. FILE SCOPE: extensions/agi/bin/rotate.py — one sweep helper called from the spawn step (reuse rotation_alert's _latch_path/_latch_holder_pid by import if the hooks dir is importable there, else duplicate the two-line pid read and say so); its test file. EXCLUDED: rotation_alert.py itself, the hook's release logic, the latch format. CEILING: one helper, one call, three tests."
thought_session: sensei-director-genXIII-L13
title: rotate-self sweeps the seat's dead rotations hook-*.lock latches (holder pid not alive) before spawning the successor, so no wake call is spent removing a stale latch by hand
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
