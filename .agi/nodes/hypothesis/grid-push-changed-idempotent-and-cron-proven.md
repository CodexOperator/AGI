---
id: hypothesis:grid-push-changed-idempotent-and-cron-proven
mint_id: 0c7f57dbe4144a96b9a4c6bd2e82eb77
type: hypothesis
parents:
  - goal:g7.33.11
next_edges: []
edited_by: director-engine
scaffold_hash: a3d756a6dd398245
season: 2
testable_claim: A second grid.py push-changed run sends nothing for tips origin already has; three real grid_sync cron ticks each report 0 rejected; the failure log is truncated only after that, with before/after byte counts reported.
title: grid push-changed is idempotent on a second real push, three real cron ticks confirm zero rejects, and the failure log is safe to clean
town: core
---
# hypothesis:grid-push-changed-idempotent-and-cron-proven

## Measured
grid.py:171-219 (push_spec_for/push_batch_limit/push_batches) and grid.py:220 (cmd_push_changed) exist
since DH.292 (merged 84fa64fba8); crons.py's grid_sync job now calls `grid.py push-changed` instead of the
single wildcard refspec that issued all 4,298 refs in one request (the 967-failure mechanism). DH.292's 4
kids each landed inconclusive_lean_proved/disproved (never outright proved): no git-ls-remote/fresh-clone
evidence for the IDEMPOTENT second-push case (only mocked), no real cron ticks run yet, log cleanup not
started. goal:g7.33.11's own DONE row requires: origin's ref count for grid.storage_trunk matches the
local post-split count, 0 rejected in 3 consecutive real cron runs, and the push-rejection lines stripped
from the grid_sync cron's 775 MB log only once those 3 runs are clean, with before/after byte counts
reported.

## CLAIM
A second `grid.py push-changed` run, after refs already landed once, sends nothing for tips origin
already has (only genuinely new/changed refs go out); three real `grid_sync` cron ticks in a row each
report 0 rejected against the real remote; and the grid_sync cron's failure-log is safe to truncate only
once that is proven, with before/after byte counts reported.

## Dispatch line
config-max: none identified -- this is a behavior/test-evidence gap, not a missing config cell.
template-max: none identified.
code: (1) a real-remote integration test extending the existing test_push_changed_advances_real_bare_remote
pattern in test_grid.py -- push twice against a real bare git remote, assert the second push's batch list
is empty or covers only genuinely new refs; (2) let grid_sync tick 3 times for real (or a real,
non-mocked simulation of 3 applier runs) and confirm 0 rejected via git ls-remote against the real
remote; (3) ONLY THEN strip the push-rejection lines from the grid_sync cron's log (path lives on the
crontab's grid_sync job line, cron:crons node -- NOT config:crons, that id does not resolve), reporting
before/after byte counts in the experiment node.

## FALSIFIERS
A second push sends any ref whose tip already matches origin's. Any of the 3 real cron ticks reports a
rejected ref. The log cleanup runs before all 3 ticks are clean, or reports no before/after byte counts.
origin's ref count for the grid.storage_trunk namespace does not reach the local post-split count.

## TESTS
extensions/agi/tests/test_grid.py (existing push_batches/push_batch_limit/cmd_push_changed coverage,
including test_push_changed_advances_real_bare_remote) and extensions/agi/tests/test_crons.py (grid_sync
job wiring). Extend, do not replace or weaken existing coverage.

## FILE SCOPE
extensions/agi/bin/grid.py, extensions/agi/bin/crons.py, extensions/agi/tests/test_grid.py,
extensions/agi/tests/test_crons.py, and the grid_sync cron's own log file (cleanup step only, after the
3-tick proof lands). Nothing else.

## CEILING
Parent round, pi-free (ladder tier-0 parent row, no --harness flag). This is a 3-part sequential proof
(idempotent second push -> 3 real cron ticks -> log cleanup) -- reasonable to split across 2-3 kids if the
parent judges that useful, or sequence it through one kid at a time; the parent reviews, corrects and
re-briefs its own kids per the standing dispatch rule. Do not start part (3) before parts (1) and (2) are
both proved on real bytes, not mocked.
