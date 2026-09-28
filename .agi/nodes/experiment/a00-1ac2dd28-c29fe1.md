---
id: experiment:a00-1ac2dd28-c29fe1
mint_id: df852a3ad2e4409fabb3b5e70bdd4919
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.9
edited_by: a00-62509010
evidence_runs:
  - experiment:a00-1ac2dd28-c29fe1
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "pytest probe_no_setenv.py -k box_local -- copy of the tip test with the added monkeypatch.setenv(\"AGI_BOX\",\"local\") line deleted", "expected": "FAILS -- with no declared box, boxes.row_is_local drops the fixture row and the dm block never prints", "observed": "1 failed, 13 deselected, AssertionError at :415; control copy with the line intact: 1 passed", "result": "the one added byte is the discriminating one and reaches boxes.this_box live at the call site: the red was the FIXTURE"}
  - {"conjunct": 2, "class": "auth", "cmd": "probe_gate_auth.py -- drive send.main([... read --box-local]) on live bytes with a stubbed _locally_loaded_rows, one row per box cell", "expected": "a row the box rule KEEPS is still swept; rows the rule DROPS are refused by name; an unset AGI_BOX is refused", "observed": "box local -> printed_inbox_line=True; box elsewhere -> printed_inbox_line=False; row_is_local: local True / elsewhere False / empty False / LOCAL False; this_box() with AGI_BOX unset RAISED -- CLASS CORRECTED by experiment:a00-62509010-30266f: at a root that RESOLVES an agi project (a `.agi/config.json`, the test fixture's shape) it raises builtins.RuntimeError at boxes.py:167 (\"no AGI_BOX in the env and none in the box env file\"); only at a bare /tmp root with NO project does envfile.resolve raise SecretsError at envfile.py:247 first, before boxes.py's own guard. Both are the bare `except Exception` at boxes.py:186 -> `return not own` -> False, so the gate outcome is identical either way", "result": "the --box-local branch still sweeps every row the landed EG.72 rule keeps -- the kid sent 0 production lines and the sweep is intact, so fixing the code side would have been the wrong half"}
  - {"conjunct": 3, "class": "gate", "cmd": "pytest probe_foreign_leg_weakened.py -k box_local -- the tip test with the new foreign-box row changed to box=local", "expected": "the new leg FAILS -- a row named as local must print, proving the leg is not vacuous", "observed": "1 failed, 13 deselected, AssertionError at :430 (\"inbox for seat-x: empty\" in out)", "result": "the added foreign-box leg discriminates: the fix pins the rule instead of waving the gate through"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 04e7e4baf8850564
season: 2
title: "box-local D5 test: the fixture predates the landed box rule, so the test was the defect"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1ac2dd28-c29fe1 — the D5 box-local red is a TEST-side defect

## The red, reproduced at the cut

```
$ pytest extensions/agi/tests/test_send_dm_read_and_nudge.py \
           extensions/agi/tests/test_box_identity.py \
           extensions/agi/tests/test_box_guard.py -q
>       assert "dm-only-body-xyz" in out, "the row's dm block never printed: " + out
E       AssertionError: the row's dm block never printed:
E       assert 'dm-only-body-xyz' in ''
extensions/agi/tests/test_send_dm_read_and_nudge.py:411: AssertionError
1 failed, 37 passed, 1 warning in 16.77s
```

## Item 1 — which reader drops the row, proved

The chain: `main()` -> `if getattr(args, "box_local", False):` (send.py, the
`--box-local` branch) -> `for r in _locally_loaded_rows(root)` -> the gate
`if boxes.row_is_local(root, r):` -> else `print("mail_poll: skipped
foreign-box post ...")`.  The gate is the dropper, not the loop and not
`read_dms`.

Probe (scratch `probe_box_gate.py`, throwaway project root, `env -u AGI_BOX`),
row = `{"name": "seat-a", "box": "local"}`:

```
AGI_BOX in env: ''
this_box RAISED: RuntimeError no AGI_BOX in the env and none in the box env file under /tm
row_is_local(row box='local') -> False
after AGI_BOX=local: this_box -> local row_is_local -> True
```

`boxes.row_is_local` is the landed EG.72 rule: `own` is non-empty ("local"),
`this_box` RAISES (no `AGI_BOX` in env, none in the box env file), the bare
`except` returns `not own` = **False** — so the row is skipped as foreign and
nothing reaches stdout. `out == ''` is the gate speaking, not a lost dm.

## Item 2 — DECISION: the defect is in the TEST, not the code

The landed EG.72 rule is the contract and was not touched. The test's fixture
predates it: it hands the branch a row that NAMES a box ("local") while the
test never says which box it is standing on, so `row_is_local` cannot match the
two halves. The `--box-local` branch is correct as written — it must keep
sweeping a row the rule keeps, and it does the moment both halves agree.

Fix, one side only, in the fixture (FILE SCOPE test file):

* `monkeypatch.setenv("AGI_BOX", "local")` — declare the box this box-local
  reader stands on, matching the row's own `box` cell;
* + a foreign-box leg: a row `{"name": "seat-x", "box": "elsewhere"}` is
  STILL skipped under the same `AGI_BOX`, so the fix pins the rule rather than
  waving the gate through.

No `assert` deleted or weakened: D5 still discriminates on the same two
strings (`"dm-only-body-xyz" in out`, `"inbox for" not in out`) and the
post-sweep `empty` verdict for `seat-c` is still required.

send.py: **0 lines changed.** `--box-local` untouched.

## Item 3 — green at the tip

```
$ pytest extensions/agi/tests/test_send_dm_read_and_nudge.py \
           extensions/agi/tests/test_box_identity.py \
           extensions/agi/tests/test_box_guard.py \
           extensions/agi/tests/test_send.py \
           extensions/agi/tests/test_bin_help_smoke.py -q
465 passed, 7 skipped, 12 warnings in 28.33s
```

## CEILING — measured, not estimated

`git diff --numstat 42b212b06 -- extensions/agi/tests/test_send_dm_read_and_nudge.py extensions/agi/bin/send.py`
(the one read-only measurement this kid may run; measured BEFORE any paste commit):

```
12	1	extensions/agi/tests/test_send_dm_read_and_nudge.py
```

Production lines net over the cut: **0** (cap 10). Test lines net: **+11**
(cap 12). No file outside FILE SCOPE touched. No live pane, seat, worktree or
real mint; tmp repos only.

## Anchor rule — names at this tip

```
$ git grep -n "def row_is_local" -- extensions/agi/bin/boxes.py
$ git grep -n "def this_box"      -- extensions/agi/bin/boxes.py
$ git grep -n "box_local"         -- extensions/agi/bin/send.py
$ git grep -n "test_box_local_row_does_not_print_empty_before_the_dm_sweep" -- extensions/agi/tests/
```

Anchor cells: `boxes.row_is_local`, `boxes.this_box`, `main()`'s
`getattr(args, "box_local", False)` branch, and the test's own name.

## Note for the director (outside FILE SCOPE — not touched)

None. The fix needed no file beyond the test.

## Agent Notes
EG.72 box rule is the contract: boxes.row_is_local drops the fixture row (box 'local', AGI_BOX unset -> this_box RAISES -> not own == False); fixed the TEST (setenv AGI_BOX + a foreign-box leg), send.py 0 lines; 465 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-a603ca83, EG.120) -- I read the DIFF (42b212b06..f1647d766), not the result file, and ran three negative probes of my own against the kid tip. ACCEPTED, verdict proved stands, probes recorded above.

WHAT THE ORDERS SAID, quoted: "DECIDE AND STATE ... is the defect in the TEST (its fixture predates the box rule) or in the CODE (the --box-local branch must still sweep a row the rule keeps)? The landed EG.72 rule is the contract -- never weaken it to make this test pass."

WHAT THE MACHINE ACTUALLY DOES, from the diff: the ONLY changed file is the test (12 added, 1 deleted, numstat at f1647d766; send.py untouched, so production lines net 0 against a cap of 10, test lines net +11 against a cap of 12). The diff deletes no assert; it adds monkeypatch.setenv("AGI_BOX", "local") beside the fixture row whose own "box" cell already read "local", plus a second leg feeding a {"name": "seat-x", "box": "elsewhere"} row and asserting its inbox line is absent. I re-ran the named suite at the tip myself (test_send_dm_read_and_nudge + test_box_identity + test_box_guard + test_send): 393 passed, 0 failed. My probe 1 deletes the one added setenv line from a scratch copy of the tip test and the D5 test fails again at :415, so the added byte is the discriminating one and it reaches boxes.this_box live, not through a stub. My probe 2 drives send.main(["read","--box-local"]) on live bytes with _locally_loaded_rows stubbed: a row whose box cell equals this box still prints its inbox line (True) while a foreign row prints nothing, and row_is_local returns False for "elsewhere", "" and "LOCAL" and this_box() RAISES with AGI_BOX unset -- so the branch really does still sweep every row the landed rule keeps, which is exactly the condition the orders named for choosing the code side. My probe 3 weakens the new foreign leg to box="local" and the leg fails at :430, so the new assertion is not vacuous.

THE NEAR MISS: a fixture that sets AGI_BOX and stops there satisfies the orders words and loses the mechanism -- it would go green by declaring the box while the branch kept swallowing any row whose box cell is empty or differently cased, i.e. a fix that pins nothing. The added foreign-box leg is what closes that gap, and probe 3 is the case that would have caught its absence. A second near miss, the one this round exists to prevent: making the D5 test green by relaxing boxes.row_is_local (e.g. treating a raise as local) -- that would have been one line of production code, inside the cap, and would have turned the contract into a rubber stamp. The diff carries no such line.

DEVIATION: none from the standing rules. CEILING and FILE SCOPE were pasted verbatim into the brief and held; I ran no git write of my own on the kid branch and made no hand edit to any node file. CAVEAT I do not resolve here: the kid verified the box rule with a throwaway probe of boxes.row_is_local rather than with an assertion inside the test file, so a future AGI_BOX default in the config box env file could satisfy this_box() without the setenv line and turn the D5 red into a silent green -- worth a hypothesis, not worth a second kid inside a 1-kid ceiling.
<!-- THOUGHT:END -->

PARENT ACCEPT (a00-a603ca83, EG.120): kid a00-1ac2dd28. Claim (the D5 box-local red is a TEST-side defect; the --box-local branch is correct as written) is CONFIRMED by three parent-run negative probes on the kid tip -- no probe falsified it, so the verdict is not demoted. Deliverables claimed vs diff: the setenv fix (in the diff), the foreign-box leg (in the diff), "send.py 0 lines" (diff carries no send.py hunk), the numstat 12/1 (matches git diff --numstat 42b212b06..f1647d766 exactly), the anchor git-grep names (row_is_local, this_box, box_local branch, the test name -- all present at the tip). Nothing claimed is missing from the bytes. Title set in the kid own words; no rebrief_request outstanding. Ceiling: 1 kid used, 0 production lines of 10, +11 test lines of 12.
