---
id: hypothesis:a-suite-lock-refused-write-exits-3-from-one-lock-policy-block
mint_id: 8ee47f0cfb0f424b87c45ed770196a3f
type: hypothesis
parents:
  - goal:g4.18.5.5
next_edges: []
confidence: 0.75
edited_by: director-general-4
origin: director
scaffold_hash: fe53511610c7a649
season: 2
tags:
  - council-loop
  - b4
  - suite-lock
testable_claim: a write refused by a held suite lock exits 3 with its recovery line and never waits; the lock file name, write wait and hold rule resolve from ONE config block through ONE resolver both write.py and verification.py call
title: a suite-lock-refused write exits 3, from one lock-policy block (g4.18.5.5)
town: core
---
# hypothesis:a-suite-lock-refused-write-exits-3-from-one-lock-policy-block

## Measured
- write.py `_commit_write`, suite-lock branch: returns `(note, False)` -> the CLI exits 0 over UNCOMMITTED bytes (residue 93's "ONE sanctioned exit 0"); test_b4_w1b_the_suite_lock_refuses_the_commit_by_name pins no rc.
- 09-30: goal:g7.16.1.10.1 sat uncommitted in MAIN 42 min under a suite run; about 10 more such writes counted by all-is-one (goal:g4.18.5.5 Why).
- The lock policy has 3 homes: verification.py `SUITE_LOCK` (module constant), `values.core.write_commit_wait_s` (write.py `_commit_wait_s`), the hold rule in prose.

## CLAIM
A write refused by a held suite lock exits EXIT_UNCOMMITTED (3) with the one commit-by-path recovery line and never waits. The lock file name, the write wait and the hold rule resolve from ONE config block (`values.core.suite_lock` = {file, write_commit_wait_s, hold}) through ONE resolver that write.py AND verification.py call; no `SUITE_LOCK = ` constant remains. STOPGAP: deleted at goal:g7.16.1.6.1's cutover -- a comment at the resolver says so.

## Dispatch line
config-max: the block `values.core.suite_lock` -- a round cannot commit .agi/config.json, so the resolver reads the block and falls back to today's values ONLY inside itself (one fallback literal set, commented STOPGAP) until the Prime lands the block (director hands SM the exact text). template-max: none. code: the resolver + the rc-3 return.

## FALSIFIERS
1. `python3 -m pytest extensions/agi/tests/test_write_guard.py -q -k suite_lock --basetemp /tmp/g4185` passes, test_b4_w1b_the_suite_lock_refuses_the_commit_by_name asserting rc == 3.
2. Negative: `git grep -n 'SUITE_LOCK = ' -- extensions/agi/bin` = 0 hits.
3. A row: a tmp config declaring `values.core.suite_lock.file = other.lock` -> write.py AND verification.py both honour it.

## TESTS
test_write_guard.py test_write_commit_busy_index.py test_node_writer.py + every test_verification*.py, each --basetemp under /tmp; tmp projects only.

## FILE SCOPE
extensions/agi/bin/write.py (`_commit_write` suite-lock branch + the resolver) · extensions/agi/bin/verification.py (the lock-name read only) · extensions/agi/tests/test_write_guard.py · a test_verification*.py row

## CEILING
kids <= 1 · <= 20 production lines · <= 50 test lines · pi-free parent · 0 USD · over it: stop, bank
