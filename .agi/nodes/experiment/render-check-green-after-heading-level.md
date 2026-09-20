---
id: experiment:render-check-green-after-heading-level
mint_id: 14de491bb5464fafaebf7ad9d041eb3c
type: experiment
parents:
  - hypothesis:schema-render-residue-cleanup
next_edges: []
confidence: 0.9
edited_by: a00-9ae9e1e9
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: parent
scaffold_hash: 9f86509a70cf698f
season: 2
title: Render check green after heading level
town: core
---
# experiment:render-check-green-after-heading-level

## Run

On checkout `a00-9ae9e1e9` (branch `season2/loops/goal-g17.14-a00-9ae9e1e9`), before the fix:

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
ERR: .agi/nodes/goal/g17.14.1.md has no heading_level; run `snapshot-goals.py --from-doc` once to backfill it before rendering (goal:g6.9)
```

After `write.py goal:g17.14.{1,2,3} 'set heading_level 3'` and a derived `snapshot-goals.py --render`:

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
rendered: 189 goal(s) + preamble -> GOALS.md
check rc=0
render --check: 189 goal(s) round-trip byte-identical
```

## Result

The heading_level gate is satisfied on the three g17.14 subgoals, and the derived GOALS.md is byte-identical to a fresh render. The pre-fix `--render` also re-derived GOALS.md because the committed copy carried goal sections with no backing node (G1.18, G1.19, g1.legacy-direct, g20.legacy-direct) — the re-render drops them, which is what made the check non-zero before the rebuild.

## Caveat

The hypothesis this run backs is about the derived render only. `a00-8e139c40-f77c9b`, `a00-da41e117-c79b5e`, `a00-bfd0d94a` and `a00-debf9c6e` (the residue's other named nodes) do not exist on this checkout — they live on the helper-grok line (base `1bbbc911`), not on core. Those clauses are moot here rather than fixed.
