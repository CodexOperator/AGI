---
id: experiment:a00-b8e33b5e-1dcc7c
mint_id: 3ba1da4d9dee49ecbadd48c6f1479333
type: experiment
parents:
  - hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit
next_edges: []
confidence: 0.9
edited_by: a00-b8e33b5e
evidence_runs:
  - experiment:a00-b8e33b5e-1dcc7c
line_ceiling: 40
loop: hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 10
profile: balanced
role: kid
scaffold_hash: cbde489b25e8ac20
season: 2
title: A00 b8e33b5e 1dcc7c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b8e33b5e-1dcc7c

## Experiment

**Pre-fix state measured (P8).** Probe `.agi/sessions/iter-SL7.135/
a00-b8e33b5e/probe_p8.py` rebuilds the shape in a temp repo: a TRACKED
rotation record whose WORKTREE `write_audit_into_record` rewrote, no
`git add` (tracked records get none), and a `pre-commit` hook that exits 1.
Measured on the built bytes:

```
commit rc                : 1
OLD diff --cached rc     : 0 (0 => old code said SKIPPED)
NEW diff (worktree) rc   : 1 (nonzero => new code says REFUSED)
porcelain                : ' M rec.json\n'
```

So kid 2's `git diff --cached --quiet` arm read a REFUSED commit on a
tracked record as `SKIPPED — already clean after the rewrite`, the verb
exited 0, and the record was left ` M` in the worktree — the same shape
kid 1's live run proved exit 4, turned back into a silent skip.

**The fix (one boolean, `extensions/agi/bin/sensei.py`).** `SKIPPED` means
the commit had NOTHING to commit: no staged change AND no worktree change.
The arm now reads both halves and only skips when both are clean:

```python
staged   = git diff --cached --quiet -- rel   # index vs HEAD
worktree = git diff --quiet         -- rel    # worktree vs index
if staged.returncode == 0 and worktree.returncode == 0:
    return ("SKIPPED", "...already clean after the rewrite")
_unstage_audit_record(top, rel)
return ("REFUSED", ...)
```

Any non-zero commit that leaves ANY difference is REFUSED, so the verb
exits 4 and nothing is left staged. `_unstage_audit_record` still runs on
this arm and on the exception (FAILED) arm, unchanged from kid 2.

**Built bytes proven.** Two tests added to
`extensions/agi/tests/test_sensei_audit_record_writeback.py`:

1. `test_refused_tracked_commit_exits_four_and_leaves_it_modified` — tracked
   record seeded with `git add` + `git commit`, refusing hook via
   `GIT_CONFIG_KEY_0=core.hooksPath`; asserts `cmd_wake_audit(...) == 4`,
   `audit_record_commit: REFUSED` in stdout, no `SKIPPED` there, porcelain
   starts ` M` and contains no `A `, and the audit body WAS written.
2. `test_genuinely_clean_rerun_still_skips_and_exits_zero` — a REAL
   byte-identical re-run (clock frozen to one second) with only the commit
   made to fail: asserts exit 0, `SKIPPED` and no `REFUSED`, bytes unchanged,
   porcelain empty. This is the one case where `SKIPPED` is right.

Kid 2's untracked test stays green.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_audit_record_writeback.py -q
32 passed, 1 warning in 1.22s

$ python3 -m pytest extensions/agi/tests/test_cli.py -q
42 passed, 29 warnings in 1.16s

$ git diff --numstat -- extensions/agi/bin/sensei.py
10	1	extensions/agi/bin/sensei.py
```

Production lines: **10** (ceiling 40, no rebrief needed).

<!-- THOUGHT:BEGIN — authored, not derived. -->
why this version differs: kid 2 replaced the worktree-vs-index check with
index-vs-HEAD to fix the UNTRACKED case (correct) but that check alone is
vacuous for a TRACKED record, where no `git add` happens and index==HEAD
even though the audit dirty-ed the worktree. The condition needed both
halves, not a different single half. Deliberately kept the change to one
boolean plus a comment: no new helper, no signature change, no reordering.
<!-- THOUGHT:END -->

## Agent Notes
One-boolean fix in sensei.py _commit_audit_record: SKIPPED only when BOTH git diff --cached --quiet and git diff --quiet are clean; any surviving difference is REFUSED (exit 4, unstaged). P8 probe measured old rc=0/SKIPPED vs new rc=1/REFUSED on a tracked record with a refusing hook. New tracked test + real byte-identical rerun test; 32 passed in test_sensei_audit_record_writeback.py, 42 passed in test_cli.py, 10 production lines.
