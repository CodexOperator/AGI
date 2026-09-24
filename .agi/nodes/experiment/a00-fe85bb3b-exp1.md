---
id: experiment:a00-fe85bb3b-exp1
mint_id: 9c1f2b6b7a1d4e0f8a3c5d7e9b0a1c2d
type: experiment
parents:
  - hypothesis:a00-fe85bb3b-b92d4e
next_edges: []
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
testable_claim: A small adapter-neutral hold seam can be specified so first spawn records a stable pane identity before launching the provider process, and restart can reattach to that identity.
title: Specify the first-spawn durable hold seam
town: core
---
# experiment:a00-fe85bb3b-exp1

## Purpose

Turn the adjacent first-spawn hypothesis into one focused, adapter-neutral
contract rather than repeating the AST absence probe. The seam is intentionally
small: it records a stable pane identity, launches the provider under that
identity, and exposes the same handle to restart.

## Contract

```text
hold_start(seat_id, command, env) -> pane_id, process
hold_attach(seat_id, pane_id) -> process
```

`_open_round` must call `hold_start` before the first provider process is
recorded; an existing held pane must call `hold_attach`. The returned pane_id
must be persisted with the seat record. Direct anonymous `Popen` is permitted
only inside the hold implementation, never at the first-spawn call site.

## Focused acceptance probe

1. Replace the hold implementation with a recorder and replace the provider
   launcher with a fake process.
2. Call the first-spawn path with a fresh seat; assert `hold_start` runs before
   the fake process and returns one stable pane_id.
3. Simulate kill -9, then call restart with only the persisted pane_id; assert
   `hold_attach` receives that exact id and no new id is minted.
4. Repeat the same contract for each adapter-backed restart implementation.

## Status

This node specifies the smallest seam and its falsifiable probe; it does not
claim the production bytes implement it. The next experiment must execute this
probe against the actual dispatch and adapter call sites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The prior negative probe established that anonymous Popen is present. Repeating
that observation would add no leverage, so this experiment narrows the target to
one adapter-neutral ownership contract with an ordering and identity check.
<!-- THOUGHT:END -->
