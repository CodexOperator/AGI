---
id: experiment:a00-c1873bad-167cfb
mint_id: 4e1d3f62a2da4945af461722f3164c66
type: experiment
parents:
  - hypothesis:context-fixture-tests-run-in-a-configured-suite
next_edges: []
confidence: 0.8
edited_by: a00-9a906e4f
evidence_runs:
  - experiment:a00-c1873bad-167cfb
loop: hypothesis:context-fixture-tests-run-in-a-configured-suite@s2
model: stealth/space-bunny-alpha
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 2d832bc2ce00aa19
season: 2
title: a declared-but-unusable suite cell FAILs where an absent one SKIPs
town: core
verdict: proved
---
# experiment:a00-c1873bad-167cfb

## The hole I inherited

`experiment:a00-7bc04de0-bc3bff` (parent probe C) declared a second suite from
the config cell `paths.core.suite_roots` and SKIPped when the cell was absent.
Its `_declared_suite_roots` folded ABSENT and UNUSABLE into one return: a
non-list, an empty list, or a list of objects all produced `([], cell)`, so
`check_extra_suite` answered

```
SKIP | no suite roots declared in config cell paths.core.suite_roots
```

A typo in a declaration that WAS written switched the whole second suite off
while the tool claimed nothing had been declared. The declaration is a cell
name; an unusable declaration must be distinguishable from an absent one.

## What I did

Split the read into `_suite_cell_state(groot) -> (declared, value, cell)` and
made `check_extra_suite` branch on `declared`:

| cell value | before | after |
|---|---|---|
| `.agi/context` (a string) | SKIP "nothing declared" | FAIL "IS declared but unusable ... got str" |
| `[]` | SKIP "nothing declared" | FAIL "IS declared but unusable ... got list" |
| `[""]` | SKIP "nothing declared" | FAIL, same message |
| `[{"path": ".agi/context"}]` | FAIL, but on a str()-coerced nonsense path | FAIL, naming the value |
| `null` / absent / no `paths` | SKIP | SKIP (unchanged) |
| a valid non-empty list of strings | runs | runs (unchanged) |

Non-string entries are no longer `str()`-coerced into a path — they fall
through to the same unusable-declaration FAIL.

## Evidence (live, after)

```
STRING cell    FAIL  cell paths.core.suite_roots IS declared but unusable: expected a non-empty list of repo-relative paths, got st
EMPTY list     FAIL  cell paths.core.suite_roots IS declared but unusable: ... got li
LIST of dict   FAIL  cell paths.core.suite_roots IS declared but unusable: ... got list [{'path': '.agi/c
NULL cell      SKIP  no suite roots declared in config cell paths.core.suite_roots
ABSENT         SKIP  no suite roots declared in config cell paths.core.suite_roots
no paths       SKIP  no suite roots declared in config cell paths.core.suite_roots
```

### tests

```
$ python3 -m pytest extensions/agi/tests/test_verification.py -q
65 passed                     # was 64; +1 test, 3 malformed shapes FAIL, absent SKIPs
$ python3 -m pytest extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_seat_model.py -q
47 passed
```

`extensions/agi/bin/verification.py`: 32 added / 7 removed (the 7 are the lines
the old reader's guard block replaced), under the 40-line ceiling. No config
cell was added, no suite root became a literal (falsifier 2 of the parent stays
shut), no model is touched.

## Honest limits

* Still no cell is committed to `.agi/config.json`, so on this graph the second
  suite still SKIPs by name. The change only separates the two states; a human
  still owns the declaration.
* `[]` is treated as UNUSABLE (FAIL) rather than "declared empty". Defensible
  (a declared suite that runs nothing is a silent no-op) but it is a choice;
  an empty-list-is-fine repo would want the other branch.
* The prior round's UNNAMED flake (one FAIL in five `check_extra_suite` runs of
  `.agi/context`) is untouched — still unrecorded, still the next thing to hunt.
# experiment:a00-c1873bad-167cfb

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
split ABSENT from UNUSABLE in the suite cell read: a string/empty/obj-list cell now FAILs naming the value, absent still SKIPs; 65+47 tests pass; 32 production lines

PARENT REVIEW DH.387 (a00-9a906e4f) — read the DIFF (af71ac5c5: _suite_cell_state split, 3-line refusal in check_extra_suite, 1 new test), not the report. ACCEPTED at proved, and the lean is honest because the node title scopes the claim to the malformed-cell hole, which is exactly what the bytes do. Probes I ran myself: (auth) a cell holding a STRING, an INT, an EMPTY LIST, or a LIST OF OBJECTS each returns FAIL "cell paths.core.suite_roots IS declared but unusable ... got <type> <value>" -- the unusable declaration is now distinguishable from an absent one, which is the whole point; (auth) a cell explicitly set to null SKIPs, since a null cell is an absent declaration and not a typo -- that boundary is the one judgement call in the diff and I agree with it; (auth) a declared root that is not a directory still FAILs by name; (wire) with the cell injected, check_extra_suite on this graph runs the suite and returns PASS; (wire, second site) run_level(groot, "quick", suite=True) calls check_extra_suite exactly 1 time and suite=False calls it 0 times -- the --suite flag really threads to the changed bytes, a stub never sees the roots. Falsifier 1 re-measured independently from a neutral cwd: 133 collected, 0 errors. 85 passed in the verification test files. The three claims the kid makes are all carried by the diff; nothing demoted. STILL NOT THE CLAIM ITSELF: the config cell paths.core.suite_roots is still ABSENT from .agi/config.json (a round cannot commit it; dm to director-engine), so the second suite remains a named SKIP in production until a human adds it, and the unnamed context flake from experiment:a00-7bc04de0-bc3bff is still unnamed. That is why the hypothesis is not proved, whatever this node says.
