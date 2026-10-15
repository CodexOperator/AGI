---
id: experiment:bin-suite-first-run-ordering-r1
mint_id: 0fd0234d5cfc9b443834d2bbcb12c200
type: experiment
parents:
  - experiment:a00-68ff74cf-bb0177
confidence: 0.9
edited_by: a00-686d056c
evidence_runs:
  - experiment:bin-suite-first-run-ordering-r1
loop: experiment:a00-68ff74cf-bb0177@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
season: 2
title: 'A00 68ff74cf bb0177 -- item 2: first --suite run self-FAILs, fixed'
verdict: proved
---
# experiment:bin-suite-first-run-ordering-r1

ITEM 2 of hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking,
proven with fixtures (temp graph root, no stamp, stubbed suite result; no
real `verification.py --suite` window touched — the suite window is the
Prime's).

## The bug (reproduced in the bytes)

`run_level` appended `check_bin_freshness` at verification.py:393 INSIDE the
same call; `_record_suite_ts` fired at :501 only in `main()` AFTER `run_level`
returned. So the FIRST-ever `--suite` run read a None prior stamp
("no suite has EVER run") and self-FAILed even while the suite in that very
call was passing; the timestamp then landed, and only a SECOND suite run went
green. Orders of the two events made the first run fail by construction.

## The fix (ordering, never the judgement)

1. `check_bin_freshness` gained a keyword `effective_ts: float | None = None`.
   When given, it replaces the recorded stamp as the mtime-arm reference.
2. `run_level` computes
   `eff_ts = time.time() if (suite on AND the suite result == PASS) else None`
   and passes it to the guard. A `--suite` run that JUST PASSED judges
   freshness against the run completing NOW — the just-covered bin is
   covered. Suite-FAIL and no-`--suite` leave `effective_ts` None, so the
   guard reads the recorded stamp exactly as before; the no-recorded-stamp
   conservative-FAIL arm is untouched and is never silenced (effective_ts is
   only ever supplied by a passing suite run).

## Evidence: fixtures + tests (3 new, none of the existing 30 edited)

- **Test (f) arm 1:** `run_level(groot, "rotation", suite=True)` with a stub
  run_check returning suite PASS, real `check_bin_freshness` over a temp graph
  root + temp bin dir (`tracked_of` injected, no git), NO recorded stamp →
  `bin-suite-fresh` PASS, note "covered by the suite run completing now", and
  `effective_ts` asserted not-None.
- **Test (f) arm 2:** same but suite FAIL → `bin-suite-fresh` FAIL
  "SUITE REQUIRED", `effective_ts` asserted None (a failed suite covered
  nothing; no fresh stamp is fabricated).
- **Test (g):** NO `--suite` (rotation), stale recorded stamp + a newer
  UNTRACKED bin/*.py → `bin-suite-fresh` FAIL unchanged
  "SUITE REQUIRED … (untracked; mtime newer than the last suite run)",
  `effective_ts` asserted None.
- **Full suite:** every test file under `extensions/agi/tests/` run per-file
  (the kid tier refuses a bare directory run) — zero failures;
  `test_verification.py` 33/33 including the three new ones.

## Scope held / flags

Only `extensions/agi/bin/verification.py` + `extensions/agi/tests/test_
verification.py` changed. No existing test edited. ITEM 3 (suite stamp
worktree-local / locations.sessions_dir) was NOT touched — the fixtures here
use a temp graph root so they do not exercise it; that item stays for its
later slot.