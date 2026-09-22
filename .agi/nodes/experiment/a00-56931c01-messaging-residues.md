---
id: experiment:a00-56931c01-messaging-residues
mint_id: dc40f094ee904c23b5ec25f40df38a84
type: experiment
parents:
  - hypothesis:a00-56931c01-45f6df
next_edges: []
edited_by: a00-56931c01
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 610e81cef144fbd4
season: 2
testable_claim: "Four residues left by r1/r2 are closed: decorative canary deleted, dead _RealSend binding exercised, both messaging files grid-covered, r2 prose overclaim corrected; messaging.py byte-unchanged"
title: A00 56931c01 messaging residues
town: core
---
# experiment:a00-56931c01-messaging-residues

Residual cut under `goal:g7.32.2`, redoing the cut a prior kid
(`a00-5d873a33`) performed correctly in its worktree but failed to get
committed. The three `goal:g7.32.2` falsifiers are already proved by
`experiment:a00-885927de-messaging-r1` and
`experiment:a00-81747954-messaging-r2`; this round closes the four residues
those runs left behind. `extensions/agi/bin/messaging.py` stays byte-unchanged.

## Residue 1 — the decorative canary is closed

`class _ExplodingSend` and the canary block at the end of
`test_native_send_never_touches_transport_and_types_exactly` were DELETED.
That stub was called directly, never through `native_send`, so it proved
nothing. No transport parameter was added to `native_send` — its
no-transport signature *is* the property.

## Residue 3 — the dead `_RealSend` binding is exercised

In `test_native_path_never_reaches_real_send_py`, the dead line
`_RealSend(tmp_path, "grok-bot")` was replaced with
`with pytest.raises(AssertionError): _RealSend(tmp_path, "grok-bot").send("grok-b", "hello")`,
exercising the binding so the monkeypatched `_boom` guard is proved live.

## Residue 2 — grid coverage

Neither `extensions/agi/bin/messaging.py` nor
`extensions/agi/tests/test_messaging.py` had a build node. Both were minted
(`build:bin-messaging`, `build:tests-test-messaging`), so both now resolve.

```
python3 extensions/agi/bin/grid_coverage_check.py --engine . --verbose \
  | grep -c 'MISSING: extensions/agi/bin/messaging.py'
0
python3 extensions/agi/bin/grid_coverage_check.py --engine . --verbose \
  | grep -c 'MISSING: extensions/agi/tests/test_messaging.py'
0
```

(The checker stays red repo-wide on ~205 unrelated files; only these two were
cleared.)

## Residue 4 — r2 prose overclaim corrected

`experiment:a00-81747954-messaging-r2` said its test "replaces r1's decorative
`_ExplodingSend`". That is false: r2 added the guard *alongside* the stub and
removed nothing. The prose now says so, and names DT.82 as the cut that
removed the stub. Edited through `write.py` (`replace body`), never by hand.

## Command — the suite (named file, not the directory)

```
python3 -m pytest extensions/agi/tests/test_messaging.py -q
```

Raw output:

```
.....................                                                    [100%]
21 passed in 0.32s
```

## Production lines — messaging.py untouched

`git diff --numstat` (read-only) over the changed paths:

```
4	4	.agi/nodes/experiment/a00-81747954-messaging-r2.md
11	5	.agi/nodes/goal/g7.32.2.md
2	10	extensions/agi/tests/test_messaging.py
```

`extensions/agi/bin/messaging.py` is ABSENT from the diff — byte-unchanged.
Production lines over the given production path: **0** against
`line_ceiling: 40`. No re-brief needed.

## Evidence

| residue | artifact | result |
|---|---|---|
| 1 decorative canary | `test_messaging.py` stub deleted | passes (21 passed) |
| 2 grid coverage | both build nodes minted | both greps print 0 |
| 3 dead binding | `pytest.raises` exercise added | passes |
| 4 r2 prose | `experiment:a00-81747954-messaging-r2` corrected | read-back shows new sentence |

## Traps

- The prior kid's branch carried only its own two nodes and the test file; its
  build nodes and node edits were untracked/modified and never committed. This
  round passes all four ids to `--owns` so the round commit includes them.
- A bare `pytest extensions/agi/tests/` is refused by the kid tier gate; name
  the file.

Raw output, screenshots, logs.
