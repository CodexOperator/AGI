---
id: hypothesis:g716111-t1-every-test-that-guards-a-v5-piece-is-a-shell-t-sh-exit-is-the-fail-count
mint_id: 5a20e2edc20d4d90a2d7b720b4d9ea95
type: hypothesis
parents:
  - goal:g7.16.1.11.16
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 508647f7713d5165
season: 2
testable_claim: "(T1) each of the 6 pytest files that guard a v5 piece is replaced by `extensions/agi/tests/<piece>.t.sh`: every one of its 48 cases is a shell case that prints `ok <name>` or `FAIL <name>` and the script exits with the FAIL count; `sh <piece>.t.sh` exits 0 on the trunk when run by a v5 uid (no pytest, no python import for an assertion a shell tool can make); no case is weakened or dropped; the replaced pytest file is retired (deprecated, moved), not deleted."
title: "Shell tests T1: the 6 test files (48 tests) that guard a v5 piece become extensions/agi/tests/<piece>.t.sh beside what they replace, one ok/FAIL line per case, exit = the FAIL count, runnable by a v5 uid with sh"
town: core
---
# hypothesis:g716111-t1-every-test-that-guards-a-v5-piece-is-a-shell-t-sh-exit-is-the-fail-count

## Measured
- belam [decision] 14:5xZ 10-02 (cc SM) accepting the council's shell-tests rule (alive [rule] 14:54Z); council numbers: 324 py files, 173,231 lines, 7,965 tests, 0 shell tests; full suite 7,911 passed / 0 failed at 96140880b; v5 uids cannot import pytest. HORIZON: ordered AFTER phase W of goal:g7.16.1.11.15 (or beside it, if no file overlaps).
- NOT KNOWN to me: the names of the 6 files and their 48 cases (alive's list; its [rule] text is not on the trunk). The round's FIRST step names them from alive's list and records them on its experiment node; if the list is not obtainable, the round derives it: the test files whose subject is a v5 piece (an engine*.md piece), by `git grep` over extensions/agi/tests against the pieces in engine.md.
- The shape already exists once: `sh extensions/agi/tests/aa3-lanes.t.sh` (goal:g7.16.1.11.13 falsifier 1; exit 13 / 2 / 0 by state).

## CLAIM
(T1) each of the 6 pytest files that guard a v5 piece is replaced by `extensions/agi/tests/<piece>.t.sh`: every one of its 48 cases is a shell case that prints `ok <name>` or `FAIL <name>` and the script exits with the FAIL count; `sh <piece>.t.sh` exits 0 on the trunk when run by a v5 uid (no pytest, no python import for an assertion a shell tool can make); no case is weakened or dropped; the replaced pytest file is retired (deprecated, moved), not deleted.

## Dispatch line
config-max: none / template-max: none / code: the 6 `.t.sh` files; the pytest files they replace retire. NOT dispatched: HORIZON until phase W (belam).

## FALSIFIERS
`sh extensions/agi/tests/<piece>.t.sh` exits 0 for each of the 6, printing 48 ok lines in all, run as a v5 uid · each ported case is traceable to its pytest case by name (a table on the experiment node: 48 rows) · negative: `git grep -l -E 'pytest|^import ' -- 'extensions/agi/tests/*.t.sh'` 0 hits; no pytest file is `git rm`'d.

## TESTS
run each `.t.sh` on the landing tree by a v5 uid (no venv); run the replaced pytest on the base tree and diff the case lists by name (equal); a mutation per file: break the piece it guards, the `.t.sh` exits >= 1 (a test that cannot fail is not a test).

## FILE SCOPE
extensions/agi/tests/<piece>.t.sh x 6 · the 6 pytest files (retire, move) · its own experiment node. NEVER a production file.

## CEILING
1 parent · kids <= 3 (two files each) · 0 production lines · regular review. HORIZON.
