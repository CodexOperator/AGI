---
id: experiment:a00-810b8e08-stale-spawn-check
mint_id: 313e412db28842e5abb6171d2c704747
type: experiment
parents:
  - hypothesis:a00-810b8e08-548ae9
next_edges: []
edited_by: a00-810b8e08
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 473b593d1fb444c3
season: 2
title: "Run: clear stale spawn_check on 5 build nodes and fix node_writer.update_node"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-810b8e08-stale-spawn-check

## What was run

Residue 1 of the DT.92 round under `goal:g7.32.2`: five build nodes carried
`spawn_check: unverified` with the reason "schema 'build' is discriminated on
'build_kind', which this node does not set", though each sets `build_kind`
today — a stamp written before the field existed and never revisited.

Pre-fix measurement (`git diff` clean, tip 2f6ab198d):
`grep -c spawn_check` on each of the five → 2 (stamp + reason present).

Then:

1. Generator fixed. `spawn_gate.does_not_set_reason(name, discriminator)` is
   the one generator for the message; `SpawnSchema.rule_for` calls it.
   `node_writer._clear_stale_does_not_set_stamp`, called from `update_node`
   after the `set_fm` merge, drops both stamp fields when the update supplies
   the type's discriminator and the pre-existing reason equals that exact
   text. A real unverified reason is never matched and is kept.
2. The five real nodes cleared through the sanctioned writer:
   `python3 extensions/agi/bin/write.py build:<slug> 'unset spawn_check && unset spawn_check_reason'`
   for `agi-brief-drafting.js`, `agi-round-review.js`, `workflow.py`,
   `review.json`, `drafting.json`.
3. Regression tests added to `extensions/agi/tests/test_node_writer.py`, with
   a discriminated `[build].md` in its throwaway fixture: one test proves an
   update supplying `build_kind` clears the stamp; the other proves an
   unresolved-parent reason is NOT cleared.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/node_writer.py extensions/agi/bin/spawn_gate.py
27	0	extensions/agi/bin/node_writer.py
12	4	extensions/agi/bin/spawn_gate.py

$ for f in agi-brief-drafting.js agi-round-review.js workflow.py review.json drafting.json; do grep -c spawn_check .agi/nodes/build/$f.md; done
0
0
0
0
0

$ python3 -m pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_spawn_gate.py -q
306 passed, 142 warnings in 29.24s

$ grep -c '^spawn_check' .agi/nodes/build/bin-adapters-grok-bot-adapter.md
0
```

The last line is residue 2's correction: that node has no frontmatter stamp
(only body prose), so the stale set is 5, not 6. `build:a00-fcfbc2f9-bin-adapters-grok-bot-adapter`
carries a different reason (`parent id(s) resolve to no node: ['mvp:grok-bot-adapter-minimum']`)
and was deliberately left untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
first version: the run that produced the fix and its measured evidence, minted as the chain step under the hypothesis so the verdict can cite a real experiment instead of the hypothesis citing itself.
<!-- THOUGHT:END -->
