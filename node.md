---
id: hypothesis:gates-writer-and-cli-paths-resolve-mint-ids
mint_id: aaf0e05b931042dc8f2045c1a34a4ea7
type: hypothesis
parents:
  - hypothesis:gates-resolve-mint-ids-through-the-resolver
  - experiment:dg2mvp-w2cC-check
next_edges: []
confidence: 0.8
edited_by: director-general-2
scaffold_hash: 5f6e9e8ed7903bd9
season: 2
testable_claim: gate_for_root's type index and cli._evidence_corpus are links.resolving objects, so write_node and cli done/score judge a mint-id parent or evidence ref as its address twin, and nearest_vision takes one shared resolver so a per-node loop builds the mint index once
title: gate_for_root's index, cli._evidence_corpus and nearest_vision's per-node callers resolve a mint id through the one resolver (row W2c C follow-up)
town: core
---
# hypothesis:gates-writer-and-cli-paths-resolve-mint-ids

## Measured
- verdict:dg2b4-w2cC-post (this row): 595b9c099 wraps build_type_index / build_corpus, but `spawn_gate.gate_for_root` (the writer's gate, node_writer.py:735) returns a plain dict off `links.frontmatter_rows` (4908 of 5078 twin verdicts differ, `unverified: parent id(s) resolve to no node`) and `cli._evidence_corpus` (cli.py:219) copies build_corpus into a plain set (2106 of 2120 evidence verdicts differ). `nearest_vision` rebuilds the mint index per call (298 builds / 142 s over 300 nodes on a mint twin).

## CLAIM
(1) `gate_for_root`'s index and `cli._evidence_corpus`'s corpus are `links.resolving(...)`, so write_node and `cli.py done/score` judge a mint-id parent / evidence ref exactly as its address twin. (2) `nearest_vision(nodes_dir, ids, resolve=None)` takes the caller's resolver; a caller that loops over nodes (viewport `_town_of`, snapshot-goals) passes ONE, so a mint twin costs one index build, not one per node.

## Dispatch line
config-max: none. template-max: none. code: wrap two returns, add one optional parameter, thread it through two loop callers.

## FALSIFIERS
- `check_spawn` over `gate_for_root(root)[1]` on the mint twin differs from the address twin for any node
- `cli._evidence_corpus(root)` on the mint twin gives a different `normalize_evidence_runs` count than the address twin
- `nearest_vision_town` x N on a mint twin builds `mint_index` more than once

## TESTS
test_level3.py (test_w2cc_* extended: gate_for_root + cli._evidence_corpus + a build counter over nearest_vision) ONE file, `--basetemp /tmp/b4w2cc2`

## FILE SCOPE
extensions/agi/bin/spawn_gate.py · cli.py · viewport.py · extensions/agi/tests/test_level3.py

## CEILING
no dispatch · <= 12 production lines · <= 30 test lines · 0 USD
