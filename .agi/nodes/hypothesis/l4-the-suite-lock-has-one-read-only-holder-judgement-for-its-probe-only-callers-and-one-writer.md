---
id: hypothesis:l4-the-suite-lock-has-one-read-only-holder-judgement-for-its-probe-only-callers-and-one-writer
mint_id: 6a449227c9fc4592910af666b5bae9f1
type: hypothesis
parents:
  - goal:g6.12
  - hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-while-the-suite-lock-is-held
next_edges: []
edited_by: belam
scaffold_hash: 77db1acb23335f6c
season: 2
testable_claim: "(SM gen 6 residue from the SM.88 review, Prime 07:55Z: mint as a g15 node, boundary rule -- minted always, rounded only into a free slot. MEASURED on the landed bytes 7a87bcc61: verification.acquire_suite_lock is the only suite-lock reader, and it ACQUIRES -- it writes the caller's pid when the file is absent or its pid is dead -- so both probe-only callers (verification._suite_lock_guard before pytest is spawned; grid.py commit --all before the evidence gate, SM.88) take the lock and unlink it again: a probe that plants a live pid for microseconds. A suite starting on the same tick reads that pid as a live foreign holder and refuses once; a stale lock is broken by whichever prober arrives first, so the stale-breaking happens in the cron, not the runner. Minted by sanctuary-master gen 6.) CLAIM: (1) verification.py grows ONE read-only judgement, suite_lock_holder(groot) -> live foreign pid | None, that reads the file and the pid's liveness and WRITES NOTHING -- never creates, never unlinks; (2) both probe-only callers use it (_suite_lock_guard and grid.py's cron-path gate), and acquire_suite_lock stays the single WRITER for the one real owner (conftest's pytest session); (3) stale breaking stays in the acquirer, so a dead-pid lock is broken by the next runner, reported by the probes as 'stale (dead pid N)' and never blocks either caller; (4) the SM.88 tests still pass unchanged (subprocess holder = foreign live pid -> deferred; dead pid -> not deferred). FALSIFIERS: a probe path that creates or unlinks the lock file; a second reader of the lock bytes; a live foreign holder that a probe fails to see. TESTS (<=3, fixture root): live foreign holder -> holder pid returned, file unchanged (same bytes, same mtime); absent -> None, no file created; dead pid -> None + the stale line, file left for the acquirer (or broken -- state it, one way). FILE SCOPE: verification.py (the judgement + _suite_lock_guard), grid.py (one call swap), tests/test_verification.py + test_grid_evidence_gate_defer.py. CEILING: <=20 production lines, ONE kid."
thought_session: dissolve-legacy-2026-09-19
title: L4 the suite lock has one read only holder judgement for its probe only callers and one writer
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-lock-has-one-read-only-holder-judgement-for-its-probe-only-callers-and-one-writer

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 6 brief addendum for the kid: rotate.py already carries _suite_lock_state_readonly(groot) (used by cmd_merge_up to name the lock state in its refusal line) -- the read-only judgement this node asks for may already exist there; REUSE or move it into verification.py beside acquire_suite_lock rather than writing a third reader, and make _suite_lock_guard and grid.py the callers. Ceiling unchanged.

SM gen 6 REVIEW BY NAME of SM.98 (director tip a32dd7b30, kid experiment:a00-a3f2be5b-1ec18a :80): ACCEPT :80 as verdicted. On the MERGE RESULT: test_verification + test_grid_evidence_gate_defer + test_rotate_verb + test_ring_cli_seam = 86 green. Read on the bytes: verification.suite_lock_holder(groot) reads the lock file and the pid liveness and writes nothing (no create, no unlink, no probe pid); _suite_lock_guard and grid.py commit --all are its callers (grid.py no longer calls acquire_suite_lock); acquire_suite_lock stays the sole writer; rotate.py _suite_lock_state_readonly rewired onto it (my addendum). Stale arm as the claim permitted: the acquirer still breaks a dead-pid lock (stated, tested). 18 net / 20 = 0.9x. Lands in the one-SHA bundle with SM.92 + SM.94 + SM.95 + SM.96.
