---
id: experiment:a00-5d873a33-residual-ledger
mint_id: 89d37ef963504a0cb948c144160b42a3
type: experiment
parents:
  - hypothesis:a00-5d873a33-936ddf
next_edges: []
edited_by: a00-5d873a33
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: b3b3e799c378345e
season: 2
testable_claim: test_messaging still passes with _ExplodingSend deleted; _RealSend binding exercised; grid-coverage greps print 0 for both paths; r2 prose corrected; one Agent Notes section in goal:g7.32.2
title: DT.82 residual ledger close for goal:g7.32.2 (test-only, 4 residues)
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5d873a33-residual-ledger

Residual-round ledger close under `hypothesis:a00-5d873a33-936ddf`
(parent `goal:g7.32.2`, MUR `mur-g7-32-2-dt-70-e92ee019a-3`,
`accept_with_residue`). The three falsifiers were already proved by
`experiment:a00-885927de-messaging-r1` and
`experiment:a00-81747954-messaging-r2`; this round does not re-prove them
and does not touch production logic.

### Residue 1 — decorative canary removed

`extensions/agi/tests/test_messaging.py`: the `_ExplodingSend` class and
its direct call `_ExplodingSend().send("grok-b", "hello")` are deleted.
`test_native_send_never_touches_transport_and_types_exactly` now asserts
only the recording pane (`calls == [("grok-b", "hello")]`) and
`trace["route"] == "native"`.

### Residue 2 — grid coverage mints

```
python3 extensions/agi/bin/write.py create build bin-messaging \
  --payload extensions/agi/bin/messaging.py \
  --parent goal:g7.32.2 \
  --parent idea:lm-magic-pane-llm-autocorrect-and-autofill
python3 extensions/agi/bin/write.py create build tests-test-messaging \
  --payload extensions/agi/tests/test_messaging.py \
  --parent goal:g7.32.2 \
  --parent idea:engine-tests
```

then the required fields set (`build_kind code`, `payload_ref`, `origin
build-scan`, `confidence 1.0`, `tags build code`). Proof, raw:

```
$ python3 extensions/agi/bin/grid_coverage_check.py --engine . --verbose \
    | grep -c 'MISSING: extensions/agi/bin/messaging.py'
0
$ python3 extensions/agi/bin/grid_coverage_check.py --engine . --verbose \
    | grep -c 'MISSING: extensions/agi/tests/test_messaging.py'
0
```

### Residue 3 — dead `_RealSend` binding exercised

In `test_native_path_never_reaches_real_send_py`, before `native_send`
runs:

```
with pytest.raises(AssertionError):
    _RealSend(tmp_path, "grok-bot").send("grok-b", "hello")
```

This exercises the monkeypatched-real binding instead of constructing and
discarding it; `native_send` then runs with no raise, pane typed exactly.

### Residue 4 — prose corrected

`experiment:a00-81747954-messaging-r2` now states the r2 cut added the
monkeypatched-real-transport guard ALONGSIDE the r1 decorative
`_ExplodingSend`, and the DT.82 residual cut removed that stub.
`goal:g7.32.2` Agent Notes is a single residue table, one row per residue.

### Command — the suite

```
python3 -m pytest extensions/agi/tests/test_messaging.py -q
```

Raw output (tier-gate phantom lines elided, three of them):

```
.....................                                                    [100%]
21 passed in 0.37s
```

### Command — diff, production untouched

```
$ git diff --numstat -- extensions/agi/bin/messaging.py extensions/agi/tests/test_messaging.py
2	10	extensions/agi/tests/test_messaging.py
```

`messaging.py` is absent from numstat = byte-unchanged; the test file sheds
the canary and gains the exercised binding. Test files are excluded from
the production-line ceiling; this round's production additions are 0.

### Claim check

| # | residue | status |
|---|---|---|
| 1 | decorative canary | closed |
| 2 | grid coverage | closed |
| 3 | dead `_RealSend` binding | closed (exercised, not deleted) |
| 4 | experiment + goal prose | closed |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First cut of this round contained no production change at all: test-file deletion of the decorative canary, test-file exercise of the dead binding, two build mints, and two prose corrections. The earlier replace body 68:76 on the r2 node consumed its blank line and left a stray line, fixed with a second replace 67:77 and verified by raw grep.
<!-- THOUGHT:END -->
