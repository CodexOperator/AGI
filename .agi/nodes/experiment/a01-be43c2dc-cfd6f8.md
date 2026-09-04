---
id: experiment:a01-be43c2dc-cfd6f8
mint_id: 3ece2337406a4344b6f9aa87992bd072
type: experiment
parents:
  - hypothesis:write-py-set-must-preserve-scalar-types
next_edges: []
confidence: 0.85
scaffold_hash: 4193abe5973414a9
title: Verify write.py set preserves scalar types through full pipeline
verdict: proved
evidence_runs:
  - experiment:a01-be43c2dc-cfd6f8
---
# experiment:a01-be43c2dc-cfd6f8

## Experiment

Tested whether `write.py set` preserves scalar types (int, float, bool, list) through the full write path, supporting the hypothesis that `set tier -1` produces `tier: -1` (int) not `tier: "-1"` (string).

Command: `python3 -c """...test script..."""`

Five tests covering all relevant scalar types:
1. `write.verb_set(e, 'tier', '-1')` — int negative, the exact case from the hypothesis
2. `write.verb_set(e, 'confidence', '0.9')` — float
3. `write.verb_set(e, 'active', 'true')` — bool
4. `write.verb_set(e, 'parents', '[a, b]')` — list
5. `write.verb_set(e, 'confidence', '-0.5')` — negative float

Each test:
- Creates a temp project with a node file
- Submits the edit through `write.submit()` (full path: `_coerce` → `update_node` → `render_frontmatter` → file)
- Reads the file, parses YAML frontmatter, asserts the type

## Evidence

**All 5 tests passed.**

```
Test 1 — tier = -1 (type=int) — OK
  raw line: tier: -1 — OK
Test 2 — confidence = 0.9 (type=float) — OK
Test 3 — active = True (type=bool) — OK
Test 4 — parents = ['goal:g1', 'idea:i1'] (type=list) — OK
Test 5 — confidence = -0.5 (type=float, negative) — OK

✅ ALL 5 TESTS PASS — write.py set preserves scalar types correctly
```

Additional verification:
- `_needs_quoting` correctly returns False for `"-1"`, `"-42"`, `"-0.5"`
- `_needs_quoting` correctly returns True for `"-"`, `"- "`, `"-x"` (genuinely dangerous cases)
- The raw file line `tier: -1` has no quoting, confirmed by assertion
- All 70 existing tests in test_write.py + test_node_writer.py pass after the fix

The fix in `_needs_quoting` (check for negative number pattern before the general `sval[0] in "..."` set check) is correct and complete.

## What this experiment does NOT show

- No live node was modified — all five tests run against a temp project.
  The sibling experiment `experiment:a00-b393b716-70ff40` covered the live-node case.
- The one-off retype of the 90 remaining deprecated task nodes with
  `tier: "-1"` was not run. That is a data-migration step, not a code fix
  test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter-1068. Kid wrote five unit-level tests through the full
`write.submit` pipeline (coerce, update_node, render_frontmatter, file read-back).
All five pass. Added `evidence_runs` (self-reference, legal for an experiment)
and lowered confidence from 1.0 to 0.85: the tests are solid but do not
touch a live node, and the 90-node batch retype is not part of this run.
The sibling experiment `a00-b393b716-70ff40` covers the live-node case at
higher confidence. Renamed the title from the auto-generated slug.
<!-- THOUGHT:END -->


## Agent Notes
Proved write.py set preserves int/float/bool/list types through full write path. _needs_quoting handles negative numbers, _coerce handles scalar coercion, render_frontmatter writes them unquoted. 5/5 tests passed, YAML round-trip verified, 70 existing tests unchanged.
