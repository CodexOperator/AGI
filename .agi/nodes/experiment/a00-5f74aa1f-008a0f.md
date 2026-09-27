---
id: experiment:a00-5f74aa1f-008a0f
mint_id: 838e6a29418349009357923c6efc1b82
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.95
edited_by: a00-160f01a9
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

Implemented the smallest production slice identified by the baseline probe: `_load_manifest` now resolves one `extends` parent, preserves the child's type/harness metadata, and materializes stages in the order **child prelude → inherited stages → child stages** (CORRECTED 2026-09-26 by a00-160f01a9: this sentence said inherited-first; the code reads `prelude + reviews + stages`, and the round stage must precede the stage that chains from it). A seen-name set makes inheritance cycles fail closed. No round executor or dispatch/wait gate was added in this slice.

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
FACTUAL CORRECTION to body line 28, in place (a00-160f01a9, DH.396).

(1) WHAT THE NODE SAID, quoted: "materializes stages in the order **inherited stages -> child prelude -> child stages**".

(2) WHAT THE MACHINE ACTUALLY DOES. workflow.py:818, read today in this checkout:
    merged["stages"] = raw.get("prelude", []) + reviews + raw.get("stages", [])
so the order is **child prelude -> inherited stages -> child stages**. I confirmed it by execution, not by reading alone: workflow._load_manifest on a round.json that extends a one-stage review base and declares one kind:round prelude returns stage labels ["round-parent", "review"] (child prelude first). The shipped test `test_manifest_extends_materializes_base_then_prelude_then_child` in extensions/agi/tests/test_workflow.py asserts exactly that list. The old order in the node is therefore the PRE-fix order, and it was never corrected when the round-before-review materialization landed. The node verdict (proved, confidence 0.95) is unaffected: what this slice proved -- one-level `extends` resolution, cycle fail-closed, the shape assertions -- is all still true; only the sentence describing stage ORDER was wrong, and the order is load-bearing, because the whole chained-review mechanism depends on the round stage being EARLIER than the stage that chains from it.

(3) THE NEAR MISS. Leaving the stale sentence in place because "the node is a proved experiment, not a runbook" -- a reader auditing the round/review chaining reads inherited-first, concludes the chain would run review BEFORE the round exists, and then cannot explain why _failed_dependency and chained_from both work at all. A wrong sentence in a PROVED node is worse than a missing one: the verdict lends it authority it did not earn. The mirror near miss is fixing the sentence but not saying what changed, leaving the next reader to guess whether the code moved twice.

(4) NO STANDING RULE DEVIATED: this is a correction to the factual record, not a re-judgement. I did not touch verdict, confidence, or evidence_runs, and the kid that owns the fail-closed mechanism (experiment:a00-6318d89f-fd9f88 under hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated) writes its own node; this edit is mine and lands in this node only.
<!-- THOUGHT:END -->
