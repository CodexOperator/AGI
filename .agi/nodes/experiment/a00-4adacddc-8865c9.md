---
id: experiment:a00-4adacddc-8865c9
mint_id: f659f7e8096941aa9f50bc86cac76aa7
type: experiment
parents:
  - hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates
next_edges: []
confidence: 0.9
edited_by: a00-276f7aff
evidence_runs:
  - experiment:a00-4adacddc-8865c9
loop: hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 732e0e8d57b89cd7
season: 2
title: A00 4adacddc 8865c9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4adacddc-8865c9

## Experiment

KID A — cli.py fix for Prime mur-47 (L4.331): an explicit empty/whitespace
`--kinds` must be refused by name like ',', never defaulted. Only cli.py and
test_branch_reshuffle.py were touched; branches.py is owned by a sibling kid.

### Pre-fix (measured)

`cli.py` had `--kinds default=""`, and cmd_branch_reshuffle did
`kinds_spec_raw = getattr(args, "kinds", "") or ""; kinds_spec = kinds_spec_raw.strip()`,
then `if not kinds_spec:` -> DEFAULT branch. So `--kinds ''` and `--kinds '  '`
took the ABSENT-flag branch: they were defaulted to posts,towns and printed the
"not given" line, rc 0. Reproduced on the real tree:

```
$ cli.py branch-reshuffle --dry-run --kinds '' ; echo RC=$?
branch-reshuffle: --kinds not given; defaulted to kinds posts,towns (main/loops excluded until named explicitly)
RC=0
$ cli.py branch-reshuffle --dry-run --kinds '  ' ; echo RC=$?
branch-reshuffle: --kinds not given; defaulted to kinds posts,towns (main/loops excluded until named explicitly)
RC=0
```

### Fix (implemented)

1. `--kinds` argparse entry: `default=""` -> `default=None`; help updated to
   say an explicit empty/whitespace value is refused by name.
2. cmd_branch_reshuffle: `getattr(args, "kinds", None)`. `None` = ABSENT ->
   existing default to posts,towns + defaulting line (unchanged). Otherwise
   `kinds_spec_raw.strip()`; if blank -> `raise SystemExit(ERR: --kinds:
   <as-written repr()> is blank; explicitly name one or more of main, posts,
   loops, towns)` (exit 1, zero jobs, no defaulting line). Non-blank spec keeps
   the L4.319 `elif not kinds:` "parsed to no kinds" refusal for ',' / ' , '.

### Post-fix (measured on the real tree)

```
$ cli.py branch-reshuffle --dry-run --kinds '' ; echo RC=$?
ERR: --kinds: '' is blank; explicitly name one or more of main, posts, loops, towns
RC=1
$ cli.py branch-reshuffle --dry-run --kinds '  ' ; echo RC=$?
ERR: --kinds: '  ' is blank; explicitly name one or more of main, posts, loops, towns
RC=1
$ cli.py branch-reshuffle --dry-run | grep "not given"   # absent, unchanged
branch-reshuffle: --kinds not given; defaulted to kinds posts,towns (main/loops excluded until named explicitly)
RC=0
```

`git status --short` after the two runs shows only the two intentional edits
(cli.py, test_branch_reshuffle.py) plus the pre-existing scaffold node — the
dry-run runs changed nothing in the tree.

## Evidence

New tests (test_branch_reshuffle.py, test_cli.py had no fitting home):

- `test_explicit_blank_kinds_refuses_by_name_and_lists_nothing` — for '', '  ':
  rc 1, stderr names the as-written spec, stdout empty (no defaulting line, no
  branch-rename jobs).
- `test_explicit_blank_kinds_refuses_under_delete_old` — --delete-old --kinds
  '  ' refuses before any delete step.
- Existing regression guards re-confirmed by the run: `test_absent_kinds_still_defaults_and_prints`
  (absent -> defaulting line), `test_explicit_empty_kinds_refuses_by_name_and_lists_nothing`
  (',' / ' , ' / ',,,' -> "parsed to no kinds"), `test_explicit_empty_kinds_refuses_under_delete_old`.

Suite result (the two changed/coverage files, as required):

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_cli.py -q
.................................................                        [100%]
49 passed in 26.78s
```

(One pre-existing tier-gate silent-skip of a phantom dead record, unrelated.)

Note: the sibling kid owns branches.py; this node proves only the cli.py
half of the hypothesis. The ref_candidates/branches.py half is a separate
kid's experiment.

## Agent Notes
KID A cli.py fix for mur-47: explicit empty/whitespace --kinds now refuses by name (exit 1, no jobs, no default line); absent still defaults to posts,towns. default=None on argparse; blank check on stripped spec. 49 tests pass (test_branch_reshuffle.py, test_cli.py); real-tree dry-run proofs pasted on node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-276f7aff, L4.331): (1) THE INSTRUCTION: Prime mur-47 verbatim -- "a whitespace-only/empty explicit --kinds is defaulted with a --kinds not given line (cli.py:2688) - refuse by name like ,". (2) WHAT THE MACHINE NOW DOES: cli.py:3166 sets the --kinds argparse default to None; cli.py:2722 tests `if kinds_spec_raw is None` for the ABSENT case (default posts,towns + the defaulting line, unchanged); cli.py:2736-2745 strips a present spec and raises SystemExit on a blank one, naming the AS-WRITTEN repr. The parent RE-RAN it, not just read it: branch-reshuffle --dry-run --kinds "" and --kinds "  " both print "ERR: --kinds: ... is blank; explicitly name one or more of main, posts, loops, towns" rc 1, --kinds , still prints "parsed to no kinds" rc 1, and 49 passed (test_branch_reshuffle.py + test_cli.py); git status showed no tree change from the dry-run runs. (3) THE NEAR MISS: keeping `default=""` and testing only `if not kinds_spec_raw.strip()` -- that satisfies the words "empty is refused" for a present-but-blank value ONLY if absent is separately distinguishable, and `""` is not; the pre-fix line did exactly this and collapsed both into the default. Equally, `or ""` on the getattr re-fuses absent and explicit-empty into the same value. None-vs-empty is the mechanism; the strip is only the predicate. (4) NO DEVIATION from the standing rule: a blank spec is refused, never defaulted and never unfiltered. CAVEAT the parent records rather than demotes: on the real tree the refusal is preceded on stdout by a pre-existing "branches.py: deprecated alias used: ..." warning from _reshuffle_jobs, so stdout is not empty there (the fixture test asserts empty stdout because the fixture has no stale loop branch). Not introduced here, not in scope.
<!-- THOUGHT:END -->
