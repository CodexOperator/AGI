---
id: hypothesis:launch-memory-cap-tests-never-touch-real-systemd
mint_id: 1a0b0686d8e54452b2a4c4ae191d87f4
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass7-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 431ff85c47beb48f
season: 2
testable_claim: Every test in test_launch_memory_cap.py runs against a fake probe and systemctl seam, and a guard fails the file if any test execs systemd-run or systemctl.
thought_session: belam-S2-L5-VII
title: "test_launch_memory_cap never touches real systemd (assigned: director-engine)"
town: core
---
# hypothesis:launch-memory-cap-tests-never-touch-real-systemd

# hypothesis:launch-memory-cap-tests-never-touch-real-systemd

assigned: director-engine. PASS 7 residue (hypothesis:pass7-0926-residue-batch).

## Measured
tests/test_launch_memory_cap.py:121 reaches the real systemd-run probe, and this delta widened it to a real `systemctl --user reset-failed` (PASS 7, engine-delta-1). Standing rule: no test touches real tmux / systemd / crontab / processes (a test probe TERM'd a Prime on 09-11).

## CLAIM
Every test in test_launch_memory_cap.py runs against a fake probe / systemctl seam, and a guard fails the file if any test execs systemd-run or systemctl.

## Dispatch line
config-max: none / template-max: none / code: the seam in mem_cap.py + the fakes in the test file.

## FALSIFIERS
A PATH shim records a real systemd-run or systemctl exec while the file runs.

## TESTS
extensions/agi/tests/test_launch_memory_cap.py + a PATH-shim guard inside it.

## FILE SCOPE
extensions/agi/tests/test_launch_memory_cap.py · extensions/agi/bin/mem_cap.py (the seam only)

## CEILING
1 parent (pi-free) · <= 2 kids · 10-12 production lines per conjunct · 0 USD
