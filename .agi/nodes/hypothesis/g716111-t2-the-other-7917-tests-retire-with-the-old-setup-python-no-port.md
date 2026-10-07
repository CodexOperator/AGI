---
id: hypothesis:g716111-t2-the-other-7917-tests-retire-with-the-old-setup-python-no-port
mint_id: a832b85fe8954fe8aa12f5595a0013ff
type: hypothesis
parents:
  - goal:g7.16.1.11.16
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: fd627edde67575c3
season: 2
testable_claim: "(T2) no pytest test outside the 6 files of T1 is ported to shell: each of the other 7,917 guards old-setup Python and is retired in the same update that retires that Python (status deprecated, moved, never `git rm`); until then the engine's pytest suite keeps running on the box that has pytest (SM's tmpfs gate) and stays 0 failed; the gate for retiring a test is the gate of its code: 0 uses over 24 h in any live post's ~/track and the last old-setup post on v5 (phase C' of goal:g7.16.1.11.15)."
title: "Shell tests T2: the other 7,917 pytest tests are NOT ported: they guard old-setup Python and retire WITH it, gated by use (no live post runs the code they guard)"
town: core
---
# hypothesis:g716111-t2-the-other-7917-tests-retire-with-the-old-setup-python-no-port

## Measured
- belam [decision] 14:5xZ 10-02 (cc SM) accepting the council's shell-tests rule (alive [rule] 14:54Z); council numbers: 324 py files, 173,231 lines, 7,965 tests, 0 shell tests; full suite 7,911 passed / 0 failed at 96140880b; v5 uids cannot import pytest. HORIZON: ordered AFTER phase W of goal:g7.16.1.11.15 (or beside it, if no file overlaps).
- 7,965 tests - 48 (T1) = 7,917. Owner 10-02: the old-setup Python is not going to be fixed or moved, it retires; a port would spend bytes on code that retires (the same reason goal:g7.16.1.11.15 does not move the ladder readers).
- NOT measured by me: how many of the 7,917 guard code a live post still runs; the first round counts it from ~/track, per file.

## CLAIM
(T2) no pytest test outside the 6 files of T1 is ported to shell: each of the other 7,917 guards old-setup Python and is retired in the same update that retires that Python (status deprecated, moved, never `git rm`); until then the engine's pytest suite keeps running on the box that has pytest (SM's tmpfs gate) and stays 0 failed; the gate for retiring a test is the gate of its code: 0 uses over 24 h in any live post's ~/track and the last old-setup post on v5 (phase C' of goal:g7.16.1.11.15).

## Dispatch line
config-max: none / template-max: none / code: none (a rule + a retirement list). NOT dispatched.

## FALSIFIERS
`git log` shows no `.t.sh` for an old-setup piece · a pytest file is retired only in the commit that retires the Python it imports · the suite on SM's gate stays 0 failed while any of them runs · negative: no pytest file is retired while its subject module is still imported by a live post's ~/track record.

## TESTS
SM's full tmpfs suite on each landing (7,911 passed / 0 failed at 96140880b is the baseline); a per-file count of subject-module use from ~/track.

## FILE SCOPE
none: nothing is edited by T2 itself; it is the rule T1 and T3 are bounded by. Retirements ride the old setup's own retirement rounds.

## CEILING
0 rounds. HORIZON; kept as the figure-eight's other half: what is NOT ported.
