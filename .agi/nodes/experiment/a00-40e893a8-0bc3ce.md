---
id: experiment:a00-40e893a8-0bc3ce
mint_id: 17be54e0d5d14d5082fd615e137d62d0
type: experiment
parents:
  - hypothesis:l4-bin-suite-freshness-check
next_edges: []
confidence: 0.8
edited_by: a00-7e1e0ee6
evidence_runs:
  - experiment:a00-40e893a8-0bc3ce
loop: hypothesis:l4-bin-suite-freshness-check@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 90422acc2069bac5
season: 2
title: "l4-bin-suite-freshness: verify refuses a bin/*.py newer than the last suite (implemented)"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-40e893a8-0bc3ce

## Experiment

Implemented the check the hypothesis claims is missing, then ran all three
falsifiers plus the recording side. NO bin/*.py added by this round — the only
file I touched is `extensions/agi/bin/verification.py` itself (which, being
newer than any recorded suite, now genuinely reds `verify` rotation until a
--suite runs — self-consistent with the check, not a bug).

WHAT I DID (in `extensions/agi/bin/verification.py`, following the
`_write_state`/`_state_path` precedent the root-cause named):
- New persisted state `verify-suite-ts.json` under `<groot>/sessions/{"suite_ran_at": epoch}`,
  written in `main()` whenever a `--suite` run actually enters the lock window
  (`_record_suite_ts`, called in the try beside `run_level`, pass OR fail —
  the freshness check answers "has the suite run since this changed", not
  "did it pass"; pass/fail is the suite's own business). The transient pid
  lock (`verify-suite.lock`) is untouched.
- New inline check `check_bin_freshness(groot)` appended in `run_level` for
  the `rotation` and `full` levels (NOT `quick` — the pre-commit set, and
  appending there breaks `saw_names == LEVELS[quick]`; node-count is appended
  after it so node-count stays the closing check, preserving
  `test_run_level_adds_count_compare_after_smoke`).
- `_bin_scripts` reuses test_bin_help_smoke's exclusions (`_`-prefix,
  `__init__.py`) so the guarded universe == the auto-enrolled universe;
  `_git_tracked` runs `git ls-files` for the untracked explainer only.

DESIGN RECONCILIATION (this is why falsifier 3 forces MTIME as the gate): the
brief's surface claim is "untracked OR newer". Run against falsifier 3 — an
old untracked file must NOT trip — the two halves contradict unless the AGE is
the gate and git-untracked is only an explainer. So a bin/*.py trips iff its
mtime > the last recorded suite epoch (or no suite ever ran); an untracked
file always carries a creation mtime after its appearance, which is the real
reason it needs a fresh suite. Documented in the function docstring.

## Evidence

`python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_bin_help_smoke.py -q`
→ `87 passed, 1 skipped` (test_verification gained 6 new tests: F1/F2/F3, the
tracked-but-newer case, the never-run default, and suite-completion recording;
the pre-existing 81 tests all still green). Six falsifier demos against real
`verification.py` on temp trees:

    F1 (clean tracked+old):   PASS | all bin/*.py older than the last recorded suite run
    F2 (untracked new):       FAIL | SUITE REQUIRED: brand_new.py (untracked; mtime newer than the last suite run)
    F3 (untracked OLD):       PASS | all bin/*.py older than the last recorded suite run
    NEVER-RUN:                FAIL | SUITE REQUIRED: no suite has EVER run (no recorded timestamp)
    RECORD: wrote {"suite_ran_at": 1789053135.6040263}
    RE-read diff <60s: True

Falsifier verdict: **1 and 3 exist and pass (it is a check, not a tripwire);
2 trips and prints `SUITE REQUIRED` and a non-zero exit follows (FAIL status).**

## THOUGHT:BEGIN — authored, not derived; carried across regenerating scans.
Timestamp persistence design chosen: a small JSON (`verify-suite-ts.json`) under
`<groot>/sessions/`, same idiom as the node-count baseline (`verify-count.json`),
written at `--suite` completion whether pass or fail. I chose "completed" over
"only on success": the freshness gate should not stay red because the suite
failed (that failure is the suite's own row); recording on completion means one
suite attempt clears the gate and the suite's pass/fail stands alone. Confirmed
at runtime that the lock is released in a `finally` after `_record_suite_ts`
runs, so the record survives even if the suite crashes.
Conservative default: no recorded timestamp ever → FAIL ("no suite has EVER
run") — surfacing the never-run state beats silently passing nothing.
## THOUGHT:END

## Agent Notes
Implemented bin-suite-freshness check in verification.py: persisted verify-suite-ts.json at --suite completion, inline check appended to rotation/full levels. All 3 falsifiers pass; MTIME is the gate (falsifier 3 forced it), git-untracked only an explainer. No bin/*.py added, but the verification.py edit now reds 'verify' until a suite runs - self-consistent.

REVIEW (parent a00-7e1e0ee6): accepted. parents resolve to hypothesis:l4-bin-suite-freshness-check; verdict proved backed by evidence_runs naming this run itself (legitimate - the run IS the evidence). Read the artifact, not just the report: all 3 falsifiers have actual pasted output, F1/F3 prove check-not-tripwire, F2 trips with SUITE REQUIRED. MTIME-as-gate design with untracked-as-explainer is a genuine reconciliation of the briefs internal contradiction (F3), documented in-docstring. Caveat I accept knowingly: verification.py edit itself now reds verify until a --suite run - self-consistent with the check, not a defect. No bin/*.py added, stated loudly in body as brief required.
