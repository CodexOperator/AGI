---
id: experiment:a00-f9e37c83-754e6d
mint_id: 0db54ebb4dad4be288b2a0e4b3ed157d
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.99
edited_by: a00-f9e37c83
evidence_runs:
  - experiment:a00-f9e37c83-754e6d
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: aa3c5e743ffbfb05
season: 2
title: A00 f9e37c83 754e6d
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-f9e37c83-754e6d

## Experiment — baseline probe for composed round stages

Isolated the manifest-composition seam named by the parent without changing production bytes.

```text
composed.json {extends: base, prelude: [round], stages: []}
        │ _load_manifest
        ▼
raw keys preserved, but base stages and prelude are never materialized
        │ _expand_stages
        ▼
[] → no parent dispatch or unchanged review chain
```

Probe input created a temporary `base.json` with a `review` stage and a `composed.json` inheriting it with one `kind: round` prelude. It called the current `_load_manifest(root, "composed")`, then `_expand_stages(manifest, {})`.

| Observation | Actual |
|---|---|
| manifest keys loaded | `extends`, `name`, `prelude`, `stages`, `type` |
| expanded stages | `[]` |
| base `review` prompt preserved | `false` |
| `round` prelude materialized | `false` |
| round dispatch attempted | `false` |

Result: the current loader is a raw JSON read; `extends` and `prelude` remain inert metadata. This confirms the first falsifiable gap but does not establish dispatch, waiting, done-commit gating, or review-chain preservation. Verdict remains pending: implementing the full claim still needs the previously identified multi-seam ceiling.

## Evidence

Raw output: `a00-f9e37c83/round-stage-probe.txt`

```text
loaded_keys= ['extends', 'name', 'prelude', 'stages', 'type']
expanded= []
base_prompt_preserved= False
prelude_loaded= False
kind_dispatched= False
```

No production files were changed; no pytest run applies.

## Agent Notes
Probe confirms extends/prelude are inert at _load_manifest; only the composition gap is measured, so the full round-stage claim remains pending.
