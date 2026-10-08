---
id: experiment:a00-eaa90551-7d8383
mint_id: efaaf8ed3265433d823d617d999db07c
type: experiment
parents:
  - hypothesis:l4-cmd-spawn-initialises-rowgen-display-cmd-resolves-by-key-presence-and-preserve-swept-latches-never-inherits-a-stale-sweep
next_edges: []
confidence: 0.9
edited_by: a00-b4a76d81
evidence_runs:
  - experiment:a00-eaa90551-7d8383
loop: hypothesis:l4-cmd-spawn-initialises-rowgen-display-cmd-resolves-by-key-presence-and-preserve-swept-latches-never-inherits-a-stale-sweep@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1aec8af55167adbb
season: 2
title: A00 eaa90551 7d8383
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eaa90551-7d8383

## Experiment

FIX-ONLY round (goal:g15 lineage — hypothesis:l4-a-g15-claim-is-a-build-order-
not-a-measurement). Three defects (d)(h)(i) verified present on this tip, fixed,
tested. FAIL-BEFORE / PASS-AFTER ordering demonstrated for every one.

### (d) rotate.py cmd_spawn — UnboundLocalError on `_rowgen` (seat-less, non-dry, in-root)

MECHANISM verified: `_rowgen = _seat_row_generation(root, seat)` was assigned
ONLY inside `if seat is not None:`; both readers (~1769 `_compose_seating_base_block`,
~1799 `_first_seating_announce`) are gated on ROOT, not SEAT. A seat-less spawn
inside a project root read an unbound local → `UnboundLocalError`.

FIX: initialise `_rowgen = None` alongside `_spawn_gen = FIRST_SEATING_GEN`
BEFORE the seat block. Seat-less path reads the named `FIRST_SEATING_GEN`
fallback; seat branch byte-identical. Docstring comment added at the site.

TEST (`test_rotate_startup.py::test_cmd_spawn_seatless_in_root_resolves_rowgen_and_uses_first_gen`):
drive `cmd_spawn` with no `--seat`, inside a project root, NON-dry (the fault
sits under `if not args.dry_run:`), `spawn_window` FAKED to `(0, "win")` and
`_compose_seating_base_block` wrapped to capture its `generation` kwarg (the
generation expression at the call site still evaluates `_rowgen`, so the fault
is exercised). Assert `rc == 0` and generation == FIRST_SEATING_GEN.

PRE-FIX:
```
>  assert rc == 0
>  captured.get("generation") == rotate.FIRST_SEATING_GEN
E  UnboundLocalError: cannot access local variable '_rowgen' where it is not associated with a value
   extensions/agi/bin/rotate.py:1769
FAILED test_cmd_spawn_seatless_in_root_resolves_rowgen_and_uses_first_gen
```
POST-FIX: PASS.

### (h) sensei.py `_display_cmd` — resolve by KEY PRESENCE, not truthiness

MECHANISM verified: `for key in (...): if inp.get(key): return ...` —
`{"command": ""}` → all values falsy → falls to `json.dumps(inp)` → prints
`{"command":""}` instead of `-`.

FIX: `if key in inp: return str(inp[key]) or "-"` — empty input `/` explicit
empty command prints `-`; non-empty prints as before. Docstring rewritten to
describe the live key-presence order and the new rule (the old docstring
claimed "an empty input prints '-'" and was a lie on the empty-key case).

TESTS (`test_sensei.py::test_display_cmd_empty_command_...`,
`test_display_cmd_non_empty_mapping_unchanged`): (1) `{"command": ""}` -> `-`;
(2) `{"file_path": "/tmp/x"}` -> `/tmp/x` and `{"command": "git log"}` -> `git log`.

PRE-FIX:
```
>  assert sensei._display_cmd({"command": ""}) == "-"
E  assert '{"command":""}' == '-'
FAILED test_display_cmd_empty_command_resolves_by_key_and_prints_dash
```
POST-FIX: PASS.

### (i) rotate.py `_preserve_swept_latches` — never inherit a stale sweep

MECHANISM verified: it copied `doc["swept_latches"]` from the pre-existing
record file into `rec` UNCONDITIONALLY; a re-run on an old record path carried
the old sweep list forward as if measured now.

FIX: copy from the existing file ONLY when `"swept_latches" not in rec` — a
sweep THIS run always wins. An inherited list is marked `inherited: true` in
the record (reader can tell measured from carried). Docstring documents the rule.

TESTS (`test_rotate_latch_sweep.py::test_preserve_never_overwrites_a_fresh_sweep`,
`test_preserve_inherits_stale_list_and_marks_it`): (1) rec with its OWN
`swept_latches` is NOT overwritten by the file's stale list, and is not marked
inherited; (2) rec without one inherits it and IS marked `inherited: true`.

PRE-FIX:
```
>  assert rec.get("inherited") is True
E  AssertionError: assert None is True
FAILED test_preserve_never_overwrites_a_fresh_sweep
FAILED test_preserve_inherits_stale_list_and_marks_it
```
POST-FIX: PASS.

## Evidence

Full green run of the three target files (the mandated suite):
```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
           extensions/agi/tests/test_rotate_latch_sweep.py \
           extensions/agi/tests/test_sensei.py -q
132 passed in 14.85s
```
(tier-gate printed one phantom-running-record skip notice on a dead pid;
that is conftest diagnostics, not a test failure.)

5 tests added (1 cmd_spawn + 2 sensei + 2 latch-sweep), matching the three
TEST directives in the brief. Changed source: rotate.py `_rowgen` init +
`_preserve_swept_latches` guard/docstring; sensei.py `_display_cmd` +
docstring. Everything else in the two bin files untouched.

No git run. No commits made by the agent; `cli.py done` owns all versioning.

## Agent Notes
Three g15 fixes landed and proven fail-before/pass-after: (d) _rowgen=None init in cmd_spawn kills seat-less UnboundLocalError; (h) _display_cmd resolves by key presence so {command:''} -> '-'; (i) _preserve_swept_latches never overwrites a fresh sweep and marks inherited ones. 5 new tests, 132 pass across the three target files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-b4a76d81 (SL7.107). WHAT THE INSTRUCTION SAID: the target's testable_claim is goal:g15 FIX-ONLY for three one-function defects (d)(h)(i), and hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement says a kid that only reproduces the defect and reports disproved has not finished the round. WHAT THE MACHINE DOES NOW, cited to the artifact I read and ran rather than to the source's appearance: (d) rotate.py now initialises _rowgen = None beside _spawn_gen = FIRST_SEATING_GEN at the top of cmd_spawn, before the 'if seat is not None:' block; I read the PRE-fix source myself before this kid ran and confirmed the assignment sat only under 'if seat is not None:' while both readers (the _compose_seating_base_block call under 'if not args.dry_run:' and the _first_seating_announce call) are gated on ROOT, so a seat-less non-dry spawn inside a project root read an unbound local. (h) sensei.py _display_cmd now returns str(inp[key]) or '-' on 'key in inp', replacing 'if inp.get(key)'; {'command': ''} now prints '-' instead of the json fragment, and the docstring was rewritten to the live key-presence order. (i) rotate.py _preserve_swept_latches copies doc['swept_latches'] only when 'swept_latches' not in rec, and marks the carried list inherited: true. I ran the mandated suite myself: python3 -m pytest extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_latch_sweep.py extensions/agi/tests/test_sensei.py -q -> 132 passed in 13.02s, matching the kid's quoted 132 passed in 14.85s, and I read the five added tests: each targets the changed line, the (d) test is non-dry with spawn_window faked (necessary, since the fault is under 'if not args.dry_run:'), and no assertion is vacuous. NEAR MISS: a (d) fix that only silences the reported symptom would assign _rowgen inside the root branch or move the reads behind 'seat is not None' -- both satisfy the words 'no UnboundLocalError' while leaving the seat-less path with no generation at all; this fix restores the NAMED fallback FIRST_SEATING_GEN, which the (d) test asserts from the captured generation kwarg. A second near miss: fixing (h) by 'value or -' without changing truthiness to key presence would still dump {'command':''} as json when the value is a non-string empty, because 'if inp.get(key)' is the only failing line. DEVIATION, none: the file scope and the <=25-line ceiling were respected (5 tests, not 4, because the claim itself names two (h) cases). I accept verdict=proved at confidence 0.9 with evidence_runs naming this node: the kid's own run is the run under judgement, and I independently executed the post-fix suite and read the pre-fix code, so the fail-before/pass-after ordering rests on source I verified rather than on a claim I was handed.
<!-- THOUGHT:END -->
