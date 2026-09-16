---
id: experiment:a00-b8e33b5e-1dcc7c
mint_id: 3ba1da4d9dee49ecbadd48c6f1479333
type: experiment
parents:
  - hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit
next_edges: []
confidence: 0.9
edited_by: a00-19566029
evidence_runs:
  - experiment:a00-b8e33b5e-1dcc7c
line_ceiling: 40
loop: hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": "P7-fix", "class": "gate", "cmd": "parent P7: linked-worktree kid audits an UNTRACKED shared-MAIN record with the real hook refusing the commit", "expected": "REFUSED carried by a non-zero exit; record never left staged", "observed": "record left untracked (`?? .agi/sessions/`), not `A `; commit refused as before", "result": "pass"}
  - {"conjunct": "P8-fix", "class": "gate", "cmd": "parent P8: TRACKED record rewritten on disk, commit fails rc=1", "expected": "REFUSED (not SKIPPED); verb exits 4; record left ` M`, never staged", "observed": "status REFUSED 'hook refused; ... left uncommitted'; porcelain ' M belam...json'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "regression re-run of the parent's full 13-probe suite + the wire P5a/P5b pair on the kid-3 bytes", "expected": "all 13 hold; the hook admits the fixed call site and refuses the raw one", "observed": "PROBES: 13 run, 0 failed", "result": "pass"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-19566029, SL7.135. Instruction said: "(2) A commit REFUSED/FAILED ... the exit code must carry it" and "(4) ... never a dirty record". Machine actually does on the kid-3 bytes: the commit-failure arm now requires BOTH `git diff --cached --quiet` (index vs HEAD) and `git diff --quiet` (worktree vs index) to be clean before reporting SKIPPED; any surviving difference calls `_unstage_audit_record` and returns REFUSED. My P8 (tracked record, commit rc=1) now returns REFUSED with ` M` and no staging; my P7 (untracked shared-MAIN record, real hook refused) leaves the record untracked, not `A `. My full 13-probe suite plus the P5a/P5b wire pair pass on the frozen bytes. NEAR MISS: the previous round tested only the index half of the pair (kid 2) after the previous one tested only the worktree half (kid 1) -- each single half reads a refused commit as clean on the other shape. DEVIATION: none. This round closes the target: all six items hold and both falsifiers (P7, P8) are green.
<!-- THOUGHT:END -->

## Agent Notes
One-boolean fix in sensei.py _commit_audit_record: SKIPPED only when BOTH git diff --cached --quiet and git diff --quiet are clean; any surviving difference is REFUSED (exit 4, unstaged). P8 probe measured old rc=0/SKIPPED vs new rc=1/REFUSED on a tracked record with a refusing hook. New tracked test + real byte-identical rerun test; 32 passed in test_sensei_audit_record_writeback.py, 42 passed in test_cli.py, 10 production lines.
