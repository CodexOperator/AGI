---
id: experiment:a00-f5b65962-e6c0b3
mint_id: b9cb3356e1c74119bcaa64e75e79ac34
type: experiment
parents:
  - hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
next_edges: []
confidence: 0.9
edited_by: a00-5103312c
evidence_runs:
  - experiment:a00-f5b65962-e6c0b3
loop: hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 39152de842f9c2be
season: 2
title: A00 f5b65962 e6c0b3
town: core
verdict: proved
---
# experiment:a00-f5b65962-e6c0b3

L4.322 KID A — cli.py change only. Build-order on
hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
(g15 claim, not a measurement). Sibling KID B owns branches.py; untouched.

## Defect (mur-46 verbatim)

> "(2) L4.319 residue: an explicit --kinds that parses to nothing (--kinds ,)
> is UNFILTERED - refuse by name". Measured at b6d3902ff:
`kinds_spec = (getattr(args, "kinds", "") or "").strip()` then
`kinds = _reshuffle_kinds(kinds_spec)`; the default was applied only under
`if not kinds_spec:`. So `--kinds ,` (a NON-empty spec, an EMPTY SET) skipped
the default AND the `if kinds:` filter, ran UNFILTERED. Verified in the
source of `cmd_branch_reshuffle` before the edit: that exact gate sequence.

## Placement decision (as the order required me to state)

The empty-set-from-explicit-spec refusal lives in `cmd_branch_reshuffle`,
immediately after the parse, as an `elif not kinds:` on the defaulting branch:

    if not kinds_spec:        # absent -> default posts,towns + print (L4.319)
        kinds = DEFAULT; print(defaulting line)
    elif not kinds:           # NEW: explicit-but-empty set -> refuse by name
        raise SystemExit("ERR: --kinds: <as-written> parsed to no kinds ...")

Reason it cannot live in `_reshuffle_kinds` alone: that function returns the
empty set for an absent flag too, and it is not passed whether the flag was
present. Only in the command, where kinds_spec (absent?) and kinds (empty?)
are held together, is the distinction decidable. Unknown words keep raising
inside `_reshuffle_kinds` (L4.319, unchanged). The refusal names the
CALLER'S AS-WRITTEN spec (captured raw before `.strip()`), so `--kinds " , "`
prints `' , '`, not the stripped `','`.

## What I changed

* `extensions/agi/bin/cli.py` — `cmd_branch_reshuffle`: capture
  `kinds_spec_raw` pre-strip; add the `elif not kinds:` refusal (exit 1 via
  SystemExit, ERR names as-written spec + legal words main, posts, loops,
  towns). No defaulting line, no job listing, nothing written — the raise
  fires before the plan baseline is saved.
* `extensions/agi/tests/test_branch_reshuffle.py` — four tests:
  `--kinds ,` / `" , "` / `,,,` refuse (exit 1, names spec, lists nothing);
  `--kinds ,` under `--delete-old` refuses; unknown word `posts,bogus` still
  refuses by name (L4.319 unchanged); absent `--kinds` still default-prints.

## Proof

Test suite (the file I changed):
`python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q`
-> 23 passed (was 19 before; +4 new).

Real tree (repo root, no --apply, no --delete-old):
```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds ,
branches.py: deprecated alias used: loop/hypothesis-harvest-table-subcomm-a00-26e81f42@s2 -> season2/loops/hypothesis-harvest-table-subcomm-a00-26e81f42
ERR: --kinds: ',' parsed to no kinds (one of main, posts, loops, towns)
EXIT=1
```
Refusal is BY NAME, exit 1, and changes nothing: the raise fires before any
job is listed, before the defaulting line, and before the plan baseline
(`.agi/sessions/branch-reshuffle-plan.json`) is saved — verified absent
after the run. (The leading `branches.py: deprecated alias used:` line is a
pre-existing parse notice emitted by branches.py during job scanning, present
before the refusal; not part of the fix.)

## Note

Absent `--kinds` behaviour verified UNCHANGED by both the real tree default
path and `test_absent_kinds_still_defaults_and_prints` (defaulting line
still printed, exit 0).

## Evidence

Raw output, screenshots, logs.

## Agent Notes
cli.py cmd_branch_reshuffle: explicit --kinds parsing to empty set (--kinds ,) now refuses by name (as-written spec + legal words, exit 1) instead of running unfiltered; absent --kinds still defaults posts,towns + prints. Placement: elif not kinds in cmd func (only place kinds_spec-vs-parse known). +4 tests, 23 passed; real tree dry-run refuses, changes nothing.

Parent review L4.322 (a00-5103312c): accepted proved. Read the artifact, not the report -- cli.py cmd_branch_reshuffle now has the elif not kinds: refusal after the parse, capturing kinds_spec_raw pre-strip, SystemExit before any plan baseline save. Parent re-ran test_branch_reshuffle.py: 23 passed. Parent re-ran the real tree: cli.py branch-reshuffle --dry-run --kinds , exits 1, prints ERR naming the as-written spec, lists no job and no defaulting line; absent --kinds exits 0 and still prints the defaulting line. Evidence is the run itself; verdict stands.
