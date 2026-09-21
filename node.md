---
id: experiment:a00-f5916ca2-2ee024
mint_id: bc2349a4a1f34f0a9fce8ea8c9867c2a
type: experiment
parents:
  - hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
next_edges: []
confidence: 0.9
edited_by: a00-c3c7193d
evidence_runs:
  - experiment:a00-f5916ca2-2ee024
line_ceiling: 40
loop: hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "/tmp/probe_stale_red.py — real green run then real RED run, real resolvers, check cli._find_root()/'sessions/verified.stamp'", "expected": "red run retracts the green certification", "observed": "after GREEN stamp exists True; after RED rc=1 stamp exists False; restored True", "result": "HOLDS — kid 3's _retract_verified_stamp closes the hazard I raised on kid 2"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_verified_stamp_from_suite.py -q", "expected": "green writes at the gate path in a real worktree; red retracts at every path", "observed": "6 passed", "result": "holds"}
production_lines: 20
profile: balanced
role: kid
scaffold_hash: 4b773d0b1c91deeb
season: 2
title: a-red-suite-run-retracts-the-green-certification-stamp-at-every-gate-readable-path
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# A red `--suite` run retracts the green certification at every gate-readable path

## Experiment

Parent kid 2 made the writer land where `cli.py --delete-old` reads
(`_verified_stamp_path(wt_graph)` = the worktree's local graph dir, plus the
shared sessions dir). Their own probe found the hazard this round closes:

```
after GREEN: gate stamp exists? True
after RED  : rc=1 gate stamp still exists? True
```

`cli.py:5336` tests `stamp.exists()` and NOTHING else, so a stamp left by an
earlier green run certifies a suite that has since gone red, and `--delete-old`
would proceed on red evidence.

**Change** (`extensions/agi/bin/verification.py`, +20/-0, ceiling 40):

- New `_retract_verified_stamp(groot)` — `path.unlink(missing_ok=True)` over
  `_verified_stamp_paths(groot)`, so a first-ever red run retracts nothing and
  never crashes.
- `main()` gains an `else:` under the existing all-green predicate:

```python
if not any(r.status == "FAIL" for r in results):
    _write_verified_stamp(groot, ran_at=_run_ts, ran_on=_run_sha)
else:
    _retract_verified_stamp(groot)
```

The retract predicate IS the rc predicate, so **`rc==0` iff certified** holds
in both directions. No `cli.py` change — its read expression is fixed and kid
2 already made the writer agree with it.

**Tests** (`extensions/agi/tests/test_verified_stamp_from_suite.py`, +35):

- `test_red_retracts_a_prior_green_stamp` — green then red, gate's own read
  expression.
- `test_worktree_red_retracts_a_prior_green_stamp` — REAL linked git worktree,
  no `find_project_root` monkeypatch, asserts every path in
  `_verified_stamp_paths()` is gone after red.

## Evidence

### The touched test file — 6 passed (kid 2's 4 + 2 new)

```
$ python3 -m pytest extensions/agi/tests/test_verified_stamp_from_suite.py -q
tier-gate: phantom running record ... (dead) -- skipped
......                                                                   [100%]
6 passed in 0.25s
```

### LIVE green-then-red probe — real resolvers, real git, real linked worktree

Run from this checkout (a real `git worktree`; `git worktree list` shows it).
Only the pytest spawn (`run_level`) and the suite lock are stubbed; every
resolver is production. Script:
`.agi/sessions/iter-L5.07/a00-f5916ca2/probe_green_red.py`.

```
graph root            : /home/ubuntu/work/agi/.agi/worktrees/a00-c3c7193d/.agi
gate reads (cli._find_root): .../a00-c3c7193d/.agi/sessions/verified.stamp
writer paths          : ['.../a00-c3c7193d/.agi/sessions/verified.stamp',
                         '/home/ubuntu/work/agi/.agi/sessions/verified.stamp']

after GREEN rc=0
  gate stamp exists? True -> .../a00-c3c7193d/.agi/sessions/verified.stamp
  all writer paths  : [True, True]

after RED   rc=1
  gate stamp exists? False -> .../a00-c3c7193d/.agi/sessions/verified.stamp
  all writer paths  : [False, False]

OK: green certified, red retracted, at the gate's own read path.
```

Both conjuncts hold: green writes where the gate reads (worktree AND shared),
red removes it there even after a prior green run created it. The probe ENDS
red, so the on-disk final state is the honest one — no certification standing.

### Production-line ceiling

```
$ git diff --numstat -- extensions/agi/bin/verification.py
20      0       extensions/agi/bin/verification.py
```

20 of 40 — no re-brief needed. (Test diff, excluded: 35.)

## Notes

- Kid 2's two-path behaviour is intact; no test needed changing, only two
  added. Nothing in kid 1/kid 2 was re-opened.
- Scope respected: `verification.py`, one test file, this node. `cli.py`
  untouched. No git-mutating command was run (only read-only
  `git worktree list` / `git diff --numstat`).

## Agent Notes
Red --suite now retracts the green stamp at every gate-readable path; rc==0 iff certified holds both ways. Live worktree probe: green -> exists True/True, red -> False/False at cli._find_root()/sessions/verified.stamp. 6 tests pass; 20/40 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c3c7193d, L5.07) — verdict kept proved.

WHAT THE INSTRUCTION SAID. My brief to this kid: on a --suite run where any result is FAIL, retract the certified stamp at every path _verified_stamp_paths writes, with the SAME predicate main() returns its rc on.

WHAT THE MACHINE ACTUALLY DOES. I re-ran my own probe (/tmp/probe_stale_red.py) against the kid's committed bytes: a real green run leaves the stamp True at cli._find_root()/"sessions/verified.stamp"; a following real red run (rc=1) leaves it False — retracted. The kid's `_retract_verified_stamp` unlinks every path in `_verified_stamp_paths` with `missing_ok=True`, called from the `else` of the same `not any(r.status == "FAIL" ...)` predicate that writes. rc==0 iff certified now holds in both directions. Its own six tests pass, including two that cut a REAL linked git worktree with resolvers left alone.

THE NEAR MISS. A retraction that only removes the local path leaves the shared stamp standing, and a gate run from the main checkout would still pass on red evidence — half a retraction reads exactly like a retraction. The kid loops over the same path set the writer uses, so write and retract cannot drift; that symmetry is the fix, not the unlink itself.

WHAT IS WEAK IN THE NODE. (a) The retraction is global: a red suite in ANY worktree also deletes the shared stamp at the main checkout, so a seat's red run can deny a legitimate --delete-old elsewhere. That errs toward refusal (safe direction), but it is a liveness cost the node does not name. (b) cli.py's gate still tests existence only — the stamp's sha and timestamp are for a human, never validated — so the certificate can be satisfied by any file at that path. That is the gate's pre-existing design and widening it is outside this hypothesis; recorded so it does not look closed.

NEXT. The target's two conjuncts and this hazard are all proved. The chain is complete unless the owner wants the gate to validate the stamp's sha, which is a different hypothesis.
<!-- THOUGHT:END -->
