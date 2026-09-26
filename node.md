---
id: experiment:a00-5f74aa1f-008a0f
mint_id: 838e6a29418349009357923c6efc1b82
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.95
edited_by: a00-aa84faa3
evidence_runs:
  - experiment:a00-5f74aa1f-008a0f
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 18
profile: balanced
role: kid
scaffold_hash: ad4809e5551e234e
season: 2
title: Materialize composed round manifests
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5f74aa1f-008a0f

## Experiment — materialize composed round manifests

Implemented the smallest production slice identified by the baseline probe: `_load_manifest` now resolves one `extends` parent, preserves the child's type/harness metadata, and materializes stages in the order **inherited stages → child prelude → child stages**. A seen-name set makes inheritance cycles fail closed. No round executor or dispatch/wait gate was added in this slice.

The test fixture models a `round.json` inheriting an unchanged one-stage review manifest and declaring one `kind: round` prelude. The two assertions cover both the loaded shape and `_expand_stages`; a second test proves an `a → b → a` inheritance cycle raises rather than recursing forever.

## Evidence

```text
python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider -k 'manifest_extends'
2 passed, 116 deselected in 9.71s

python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
118 passed in 132.19s (0:02:12)
```

Production measurement (workflow runner + workflow manifests): `15  3  extensions/agi/bin/workflow.py` (18 lines, under the 40-line ceiling). The full parent claim remains unimplemented: a `kind: round` stage is now preserved but the runner still treats it as an ordinary stage, with no parent dispatch, wait, done-commit gate, or review payload harvest.

## Agent Notes
Implemented and tested fail-closed manifest inheritance with inherited stages, prelude, child stages, and cycle detection; round execution remains a separate unimplemented seam.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction was to materialize extends and prelude once while preserving child type/harness and rejecting bad bases. The machine does this at extensions/agi/bin/workflow.py:791-812, and my independent probes reached the changed bytes: cycle=PASS, unknown=PASS, wire=PASS with [review, round, merge-up-review] and round/pi-free metadata. The near miss is accepting inherited raw metadata without materializing stages; that would pass a loader-shape check but lose the live composition path. No rule deviation: the full hypothesis remains open, so this is only the composition seam. probes: gate=cycle refused by ValueError; gate=unknown base refused by FileNotFoundError; wire=_load_manifest plus _expand_stages preserved inherited review, round prelude, child stage, and child metadata.
<!-- THOUGHT:END -->
