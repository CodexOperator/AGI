---
id: experiment:a00-50a86053-scoped-falsifier2
mint_id: 2e7ad0174d184d2da4f7aebbfb604734
type: experiment
parents:
  - hypothesis:a00-50a86053-4d374b
confidence: 0.85
edited_by: a00-1c745a92
evidence_runs:
  - experiment:a00-50a86053-scoped-falsifier2
loop: goal:g1.31.4.1@s2
production_lines: 62
scaffold_hash: 0f9be287ba0bf0d9
title: The scoped check is green on the live graph and red on a planted node
verdict: proved
---
# experiment:a00-50a86053-scoped-falsifier2

The run behind hypothesis:a00-50a86053-4d374b. Bytes, not prose.

## What the instruction said

goal:g1.31.4.1 falsifier 2: the goal's line-42 grep
(the pattern lives in `caveat_residue.PHRASE`, not in prose here) returns ZERO hits. The parent's order: land
that as a RUNNABLE, SATISFIABLE check, and do NOT hand-weaken the goal — keep
the goal's text exactly, give the check a stated scope that excludes
`.agi/nodes/goal/**`, and prove the check can fail.

## What the machine does

| probe | how it was run | result |
|---|---|---|
| C1 the bar is unsatisfiable as written | the goal's line-42 grep over `.agi/nodes` (the pattern lives in `caveat_residue.PHRASE`, not in prose here) | 2 hits, BOTH inside `goal/g1.31.4.1.md` — line 33 (end-state quotes the phrase) and line 42 (the falsifier's own command). The caveat file `experiment/a00-eccace59-e6cb6a.md` is NOT among them: the caveat IS retired, the bar is unmeetable |
| green arm, live graph | `python3 extensions/agi/bin/caveat_residue.py` and `pytest test_caveat_residue.py -k live` | rc=0, `hits == []` over experiment/hypothesis/verdict/build/mvp/outcome |
| negative self-test | `test_negative_self_test_the_check_can_go_red` — plants BOTH spellings in a `tmp_path/experiment/e.md` | red: 1 hit, `('experiment/e.md', 1, ...)`; the alias spelling is caught too; deleting the line turns it green |
| the exclusion is honest, not a filter | `test_the_excluded_goal_quote_exists_and_is_excluded_by_name` | a synthetic `goal/g.md` carrying the phrase scans clean AND `goal` is asserted absent from `SCOPE` |
| the scope is pinned | `test_scope_is_the_asserting_kinds_only` | `SCOPE == {experiment, hypothesis, verdict, build, mvp, outcome}`; a future widening/redirection is a diff on a test, visible |

Suites: `extensions/agi/tests/test_caveat_residue.py` 4 passed;
`extensions/agi/tests/test_dispatch_dry_run.py` 31 passed (untouched by this
round, re-run so the green is on today's bytes).

## The artifact

```
extensions/agi/bin/caveat_residue.py      the mechanism: PHRASE, SCOPE, scan(), main()
extensions/agi/tests/test_caveat_residue.py  the runnable check + the negative self-test
```

`caveat_residue.py [nodes_root]` exits 1 on a live residue; with no argument it
resolves the project root through `locations.find_project_root`, so the same
command is what a later reader runs.

## The scope decision, stated

A goal legitimately QUOTES the caveat it retired — that quote IS the record of
what was closed. A round node that ASSERTS a finding may not: re-asserting the
retired caveat in an experiment, hypothesis, verdict, build, mvp
or outcome node is a false claim about the live system, and it is exactly what
falsifier 2 exists to catch. So the scope is the node kinds that assert
findings, and `goal/` (plus `deprecated/`, which is a status holding prior
art) are excluded BY NAME, with the exclusion asserted in a test so it cannot
be quietly widened. The goal's own two quotes are shown to exist, so the
exclusion is provably not hiding anything.

## Rule deviations

None in the goal: `goal/g1.31.4.1.md` is byte-identical to HEAD. The deviation
is the ORDER of work — the near miss named in the brief (rewrite the goal's
line 42 to a narrower grep) was NOT taken.

## Not done (budget)

- The `--branch` asymmetry (a dry run resolves `--target` against `root`'s
  graph while a live `--branch` spawn resolves in the fresh worktree's graph).
- The RAM completeness gap (the report names the reader-visible symlink, not
  the tmpfs checkout). Neither is required by the goal's end-state; falsifier 2
  was the order.

## Unrelated, left where it is

`.agi/nodes/experiment/a00-eccace59-e6cb6a.md` carries an uncommitted diff
from kid a00-829ed05f (the caveat retirement). Not mine, not touched. Note for
the parent: its `<!-- THOUGHT -->` block currently reads `-`, a placeholder.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
-
<!-- THOUGHT:END -->

## Agent Notes
Falsifier 2 landed as a scoped runnable check: extensions/agi/bin/caveat_residue.py + test_caveat_residue.py (4 passed, negative self-test red on a planted node); goal:g1.31.4.1 text byte-identical.

## Agent Notes
Falsifier 2 landed as a scoped runnable check: extensions/agi/bin/caveat_residue.py + test_caveat_residue.py (green live, red on a planted node); goal:g1.31.4.1 text byte-identical.
