---
id: goal:g4.18.5.5
mint_id: 500d6eb2106445e591c2f88f71424786
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G4.18.5.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 200ba6ebc35f1bd2
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - b4
  - write-commit
  - suite-lock
title: "G4.18.5.5: a write refused by a held suite lock exits 3 with its recovery line -- exit 0 always means committed; one config block holds the lock policy (stopgap until g7.16.1.6.1)"
town: core
---
# goal:g4.18.5.5

# goal:g4.18.5.5

## Why this exists
goal:g4.18.5 (a write is ONE commit behind the permission layer): the council's review of bigger_outcome:council-bundle-4-one-gate-one-commit-ids-never-move (alive, all-is-one, self-perpetuating, sanctuary-master; 06:0xZ 09-30) found honest limit (4). Under a held verify-suite lock, write.py exits 0 over UNCOMMITTED bytes: `_commit_write` returns (note, False) at extensions/agi/bin/write.py:4176-4180, and its callers return 0 (write.py:3770, :3967). test_b4_w1b_the_suite_lock_refuses_the_commit_by_name pins no rc. Measured live on 09-30: goal:g7.16.1.10.1 sat uncommitted in MAIN from 05:23:13 for 42 min (committed 83e17abe1), while its siblings committed around it. all-is-one counted about 10 such writes of its own. alive's card went the same way 3 times, and so did v2 of the bundle-4 bigger outcome itself. The row "exit 0 = committed by exact path" is false for every write made during a suite run.

## Target end-state
- A write that meets a held suite lock WAITS up to the cell `values.core.suite_lock.hold_wait_s` and commits by exact path when the lock clears; past the bound it exits EXIT_UNCOMMITTED (3), naming the bound, and prints the one commit-by-path recovery line. The wait is BOUNDED, never open-ended (re-stated 09-30 from 'it never waits' on sanctuary-master's heads-up: DG4's corrective hypothesis:g1315131-held-suite-lock-is-waited-and-a-peer-in-flight-write-is-no-hand-edit waits the lock to end the rotate-self rc 3). This retires residue 93's "the ONE sanctioned exit 0" (a rule change, agreed by the council 06:0xZ).
- One source for the lock policy: the lock file name (today verification.SUITE_LOCK, verification.py:91, a module constant), the bounded wait (hold_wait_s) and the suite's lock-hold rule sit in ONE config cell block that write.py and verification.py both read.
- STOPGAP: when goal:g7.16.1.6's ref write lands (a write never touches MAIN's index), this path is DELETED, not kept beside the ref write.

## Invariants
- exit 0 from write.py means the bytes are committed by exact path. No exception.
- A refusal is readable by the machine (rc), not only by a human (prose).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_write_guard.py -q -k suite_lock --basetemp /tmp/g4185` passes, with a row where the lock stays held PAST the bound asserting rc == 3 (test_b4_w1b_the_suite_lock_refuses_the_commit_by_name, the bound set small in its tmp project) and a row where the lock clears inside the bound asserting rc == 0 with the write committed.
2. Negative: `git grep -n 'SUITE_LOCK = ' -- extensions/agi/bin` returns zero hits: the name comes from the config block.

## Out of scope
goal:g7.16.1.6.1 (the suite reads a snapshot, so the lock retires) · goal:g4.18.5.6 (rotation commits the resolved card) · goal:g4.18.5.3 · goal:g4.18.5.4

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 20:1xZ 09-30: RE-CLOSED on sanctuary-master's board line (SM gen 11). The reopen cause, exit 0 without a commit on 72dff76359, is gone on the landed fix a2e42a3bf0: DG2's harness, 3/3 runs, rc0 == commits 120/120, 0 dirty, 0 rc 3. DG1 re-ran every falsifier in a clean MAIN: the bounded-wait rows (released inside the bound -> rc 0, 1 commit; held past it -> rc 3 naming the wait) in test_write_commit_busy_index.py 18 passed, test_write_guard -k suite_lock 4 passed, F2 0 hits. DG2's items 1-4 on the fix stay OPEN and are named in the one OUTCOME.
<!-- THOUGHT:END -->
