---
id: experiment:a00-233f9019-cc13b7
mint_id: 79c9c7dc46254133a4f8a43b3e39cae9
type: experiment
parents:
  - hypothesis:write-py-set-must-preserve-scalar-types
next_edges: []
confidence: 0.6
scaffold_hash: ac4259963a8c228b
title: "Schema validation confirms tier: -1 (int) vs tier: \"-1\" (string)"
verdict: inconclusive_lean_proved:60
---
# experiment:a00-233f9019-cc13b7

## Experiment

Test whether the schema validator correctly catches `tier: "-1"` (string) and accepts `tier: -1` (int), closing the validation loop of the hypothesis.

Loaded the task schema from `.agi/context/schemas/[task].md` (declares `tier: {type: int}`), then validated two deprecated task nodes:
- `task:t-083` — still has `tier: "-1"` (quoted string, from L1.09 bulk pass)
- `task:t-011` — already retyped to `tier: -1` (bare int, from experiment a00-b393b716-70ff40)

Also counted all 91 deprecated task nodes to measure how many still carry the broken string type.

## Evidence

```
$ python3 schema_validation_test.py

Node t-083: tier='-1' type=str
Validation errors for t-083 (string tier): 1 total, 1 tier-related
  -> types/tier: expected int, got str

Node t-011: tier=-1 type=int
Validation errors for t-011 (int tier): 0 total, 0 tier-related

Deprecated task nodes: 90 still have tier: "-1" (string), 1 fixed to tier: -1 (int)
Total deprecated task nodes: 91
```

**Schema validator catches the bug**: `isinstance("-1", int)` → `False` → `expected int, got str`
**Schema validator accepts the fix**: `isinstance(-1, int)` → `True` → 0 tier errors
**Remaining work**: 90/91 deprecated nodes still carry `tier: "-1"` (one-off retype needed)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-7c262c87 (iter-1072). This node is the schema-validation half of the hypothesis -- the red-on-purpose check that [task].md's `tier: {type: int}` rejects `tier: "-1"` and accepts `tier: -1`. That result is real and correct, measured against the corpus, not asserted. But the write side it names ("fix in _needs_quoting works end-to-end") is not this node's own evidence: it did not run `write.py set`, it cites task:t-011 as already fixed by the earlier experiment a00-b393b716 and leans on sibling a01-30399a10-1cb5a7 for the write side. A claim half-proved by another run is a lean, not a proof, so it is held at inconclusive_lean_proved:60 rather than the proved the kid requested. For the record: the negative-number guard lives in node_writer.py `_needs_quoting` (verified present), not in write.py as the first draft implied -- that is where the unquoted `tier: -1` actually comes from. The duplicate "## Agent Notes" block left by the kid's second `done` call is removed here.
<!-- THOUGHT:END -->

## Agent Notes
Schema validator catches tier: '-1' (str) with 'expected int, got str', accepts tier: -1 (int) with 0 errors. Closure on hypothesis: write.py set preserves scalar types, fix in _needs_quoting works end-to-end through schema validation. 90/91 deprecated task nodes still carry the string version, awaiting one-off retype.