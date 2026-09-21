---
id: experiment:a00-4ddd398d-c9c1f5
mint_id: 9c8390a77fed4e7bb53d0a3e93a99816
type: experiment
parents:
  - hypothesis:l4-the-closeout-merge-up-gate-ignores-cron-owned-dirty-paths-and-blocks-only-on-a-dirty-path-the-merge-touches
next_edges: []
confidence: 0.93
edited_by: a00-d3019b0e
evidence_runs:
  - experiment:a00-4ddd398d-c9c1f5
loop: hypothesis:l4-the-closeout-merge-up-gate-ignores-cron-owned-dirty-paths-and-blocks-only-on-a-dirty-path-the-merge-touches@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3deee8b4eab0c38d
season: 2
title: A00 4ddd398d c9c1f5
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4ddd398d-c9c1f5

## Experiment

ROUND-2 ADJUSTMENT on top of round 1 (`experiment:a00-54b63391-9708d6`, which
landed `CLOSEOUT_CRON_OWNED_PREFIXES`, the touch-set gate, the refusal text
and the first five tests). Round 1's fix was correct in direction but hit the
claim's own falsifier (the prefixes spelled in THREE places) and bypassed the
file's ONE porcelain extractor. This run fixes all three defects in place and
proves the built bytes.

### DEFECT 1 — three spellings -> ONE literal
`:5996` held `CLOSEOUT_CRON_OWNED_PREFIXES = (".agi/comms/",
".agi/sessions/rotations/",)`, while `:12095` held `PREPARE_CHURN_PREFIXES`
and `PREPARE_CHURN_DIRS` spelling the same fact. Moved the two PREPARE
constants (with their comments) ABOVE the closeout site and derived the
closeout constant: `CLOSEOUT_CRON_OWNED_PREFIXES =
PREPARE_CHURN_PREFIXES + PREPARE_CHURN_DIRS`. The closeout gate treats the
whole `.agi/sessions/rotations/` prefix as cron-owned (per the claim); the
prepare-side `.json` narrowing lives ONLY in `_prepare_churn_path`
(`... and path.endswith(".json")`) — the difference is deliberate and visible
at one line, not a second copy of the literal. Verified: a non-.json file
under rotations/ is churn for closeout but NOT a prepare captive.

### DEFECT 2 — the gate now uses the ONE extractor
`_closeout_main_clean` did `dirty = [line[3:] for line in ...]` (a second
spelling of the path-extraction rule, forbidden by `_porcelain_path`'s own
docstring). It now does `dirty = [_porcelain_path(line) for line in ...]`.
`_porcelain_path` is defined below `_closeout_main_clean` in the module, which
is fine at import time (referenced only inside the function body) — proven by
running the suite. Consequence fixed: a rename row (`R old -> new`) is now
reduced to the NEW path, so a cron-owned rename stays cron-owned and is not a
blocker.

### DEFECT 3 — the unmeasurable arm truthful wording
When the tree cannot be measured (clean is None, git rc != 0) the refusal now
reads `merge_up: MAIN's tracked tree could not be measured (git status
--porcelain, untracked ignored) -- merge refused by name` — it says it could
not be MEASURED, not that it is dirty. Claim (3) still holds: it still
REFUSES.

### Tests (1 new, 2 hardened in place; round 1's five kept)
- (new) `test_closeout_merge_up_rename_row_judged_on_new_path`: a staged
  `git mv` under `.agi/comms/` produces an `R` porcelain row; the gate's
  extractor reduces it to the new path, so it is cron-owned and NOT a blocker
  (`clean is True, blockers == [], ignored == 1`). Tested at the
  `_closeout_main_clean` seam directly, because driving the full merge over an
  uncommitted rename hits git's own uncommitted-change overwrite refusal
  (which is git working, not the gate).
- (hardened) `test_closeout_cron_owned_prefixes_single_spelling` now asserts
  the DERIVED relationship `CLOSEOUT == PREPARE_PREFIXES + PREPARE_DIRS`
  (fails if anyone re-spells the literal) AND the F20 value.
- (hardened) `test_closeout_merge_up_refuses_an_unmeasurable_tree` now forces
  the clean-is-None arm on a still-resolvable MAIN (monkeypatched
  `_closeout_main_clean`) and asserts `could not be measured` in the refusal.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py -q
............................                                     [100%]
28 passed in 1.92s

$ python3 -m pytest extensions/agi/tests/test_rotate_closeout.py \
    extensions/agi/tests/test_rotate_closeout_steps.py \
    extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
..........................(dots)..........                     [100%]
359 passed, 3 skipped in 46.85s

$ python3 -c "from agi.bin import rotate as r; \
print(r.CLOSEOUT_CRON_OWNED_PREFIXES == r.PREPARE_CHURN_PREFIXES + r.PREPARE_CHURN_DIRS); \
print(r._prepare_churn_path(' M .agi/sessions/rotations/seq.json')); \
print(r._porcelain_path('R  .agi/comms/season-2/dm/x.md -> .agi/comms/season-2/dm/y.md'))"
True
True
.agi/comms/season-2/dm/y.md
```

Constraints: <= 40 lines production change (net diff is a few lines: constants
moved + derived + parse-line + wording), 1 new test, no touch to
ask/grant/suite/grid/stamp/push runners, `_closeout_step_list`, `cmd_meter`,
the bootstrap writers, the fake seam table, or `_prepare_dirty_paths`
semantics.

## Agent Notes
Round-2 adjustment on top of a00-54b63391: (1) ONE literal — CLOSEOUT_CRON_OWNED_PREFIXES now derived from the moved PREPARE_CHURN_{PREFIXES,DIRS} (prepare-side .json narrowing kept as the deliberate extra); (2) _closeout_main_clean now uses _porcelain_path so a rename row is judged on the new path; (3) the unmeasurable arm says 'could not be measured', still refuses. 28 step + 359/3-skip nbhd tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round 2 is the ACCEPTED version. I verified the artifact rather than the report: (1) the prefix fact now has ONE literal — rotate.py:5994 PREPARE_CHURN_PREFIXES, :5998 PREPARE_CHURN_DIRS, :6008 CLOSEOUT_CRON_OWNED_PREFIXES = PREPARE_CHURN_PREFIXES + PREPARE_CHURN_DIRS; grep over extensions/ and src/ shows no other definition and no other consumer outside rotate.py and the test; the prepare-side .json narrowing stays at :12134 as a deliberate extra, so the two consumers differ only where they mean to. (2) _closeout_main_clean:6259 now calls _porcelain_path, the file’s one extractor, so a rename row is judged on the new path. (3) the unmeasurable arm says "could not be measured", not "dirty". I re-ran both suites in this worktree: 28 passed on test_rotate_closeout_steps.py, and 359 passed / 3 skipped on test_rotate_closeout.py + test_rotate_closeout_steps.py + test_rotate.py + test_bin_help_smoke.py — matching the node. Verdict proved stands: this is a goal:g15 FIX-ONLY build order and the built bytes are in the tree. Parent change on top: deleted three orphaned comment lines that round 2 left at rotate.py:12107-12109 — they were the PREPARE_CHURN_PREFIXES comment copied up to the new site but not removed from the old, and they sat directly above `def _porcelain_path`, describing a constant that no longer lives there. Comment-only, py_compile clean, no behaviour change. Remaining weakness, recorded not fixed: the unmeasurable arm is proven by monkeypatching _closeout_main_clean (test at :1040), so the seam table’s own handling of a resolvable-but-unmeasurable MAIN is not exercised end to end; and the touch-set uses `git diff season2/main..seat_branch` as a stand-in for git’s merge-base computation, which agrees for the linear fixtures here and is an approximation for a diverged seat.
<!-- THOUGHT:END -->

Parent review (SL7.101, a00-d3019b0e): ACCEPTED. Verified by running both suites myself (28 passed; 359 passed / 3 skipped), by grepping the prefix literals across extensions/ and src/, and by reading the diff — the claim’s falsifier (prefixes spelled in two places) is resolved by derivation, the one-extractor invariant holds, and the unmeasurable arm refuses with truthful wording. One parent cleanup: three orphaned comment lines at rotate.py:12107-12109 removed.
