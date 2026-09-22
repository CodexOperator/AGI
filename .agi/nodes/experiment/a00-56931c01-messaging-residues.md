---
id: experiment:a00-56931c01-messaging-residues
mint_id: dc40f094ee904c23b5ec25f40df38a84
type: experiment
parents:
  - hypothesis:a00-56931c01-45f6df
next_edges: []
edited_by: a00-7d52f792
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 610e81cef144fbd4
season: 2
testable_claim: "Four residues left by r1/r2 are closed: decorative canary deleted, dead _RealSend binding exercised, both messaging files grid-covered, r2 prose overclaim corrected; messaging.py byte-unchanged"
title: "Messaging residue closure: grid mint, canary deleted, binding exercised"
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

## Raw output (DT.88 residual round)

Commands run from the worktree root
`/data/work/agi/.agi/worktrees/a00-7d52f792` on 2026-09-22. Pasted verbatim.

```
$ python3 -m pytest extensions/agi/tests/test_messaging.py -q
.....................                                                    [100%]
21 passed in 0.43s

$ grep -c '_ExplodingSend' extensions/agi/tests/test_messaging.py
0

$ grep -c 'replaces r1' .agi/nodes/experiment/a00-81747954-messaging-r2.md
0

$ git diff --numstat -- extensions/agi/bin/messaging.py
(no output — 0 added, 0 deleted)

$ grep -c '^## Agent Notes' .agi/nodes/goal/g7.32.2.md
1
```

`git diff --numstat` is the one read-only git measurement this round runs;
`extensions/agi/bin/messaging.py` is byte-unchanged.

## Spawn-stamp residue closed

Both new build nodes had `spawn_check: unverified` with the false reason
`schema 'build' is discriminated on 'build_kind', which this node does not
set`, stamped before `build_kind` was set at `write.py` `create` time
(`spawn_gate.py:166-169`, `stamp()` at `spawn_gate.py:1370-1380` — approval is
deliberately NOT stamped). Cleared through the sanctioned writer:

```
$ python3 extensions/agi/bin/write.py build:bin-messaging \
    'unset spawn_check && unset spawn_check_reason'
updated: build:bin-messaging
$ python3 extensions/agi/bin/write.py build:tests-test-messaging \
    'unset spawn_check && unset spawn_check_reason'
updated: build:tests-test-messaging
$ grep -c spawn_check .agi/nodes/build/bin-messaging.md \
    .agi/nodes/build/tests-test-messaging.md
(0 for both)

$ python3 extensions/agi/bin/spawn_gate.py check --type build \
    --parent goal:g7.32.2 \
    --parent idea:lm-magic-pane-llm-autocorrect-and-autofill \
    --id build:bin-messaging --set build_kind=code
SPAWN-GATE APPROVED build:bin-messaging type=build \
  schema=context/schemas/[build].md rules=... parent_shapes=[goal, idea]

$ python3 extensions/agi/bin/spawn_gate.py check --type build \
    --parent goal:g7.32.2 --parent idea:engine-tests \
    --id build:tests-test-messaging --set build_kind=code
SPAWN-GATE APPROVED build:tests-test-messaging type=build \
  schema=context/schemas/[build].md rules=... parent_shapes=[goal, idea]
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent set this node's title (DT.82) because the kid left the auto-derived title 'A00 56931c01 messaging residues'. The harvest's _auto_titled check (cli.py:757) compares the field to node_writer._derive_title(stem) and would have named the node untitled. No body or claim was changed by the parent.
<!-- THOUGHT:END -->

## Agent Notes
parent a00-1c474b6e: title repaired from the auto-derived string; node bytes otherwise the kid's.
