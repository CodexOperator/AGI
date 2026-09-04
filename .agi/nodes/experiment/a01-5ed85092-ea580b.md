---
id: experiment:a01-5ed85092-ea580b
mint_id: 21377f74f207404989c60d1078d582fc
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
confidence: 0.95
scaffold_hash: ec589fe786a9280e
title: Live-graph attractor verification — filter holds on the real INJECTION.md
verdict: proved
evidence_runs:
  - experiment:a01-5ed85092-ea580b
---
# experiment:a01-5ed85092-ea580b

## Experiment

Closed the remaining gap from sibling `experiment:a00-a2533db0-095680` (which verified code+tests+negative control but noted the live-graph observation was unchecked).

**Live-graph verification (new in this run):**
1. Loaded the actual graph (`zoom._load_wired_graph(root)`) with `fm_by_id` across all types, replicating `inject.py`'s build path
2. Measured the deprecated idea tree sizes (unfiltered `count_descendants`): `idea:domain-graph-core` (75), `idea:domain-schema-registry` (45), `idea:domain-chain-engine` (44), `idea:domain-autoresearch-tree-skill` (41), `idea:domain-renderers` (40), `idea:domain-embeddings` (39), `idea:domain-environment-indexers` (38) — all `status: deprecated`
3. Measured the live attractor list (with `count_live_descendants` + `_is_deprecated` filter): `idea:engine-tests` (31) heads the list, then `idea:domain-chain-bootstrap` (20), `idea:engine-graph-core` (20) — **no deprecated ideas appear**
4. Verified `inject.py --stdout` produces the same correct attractor list in INJECTION.md
5. **Negative control confirmed:** without the filter, 7 of top 10 positions are deprecated ideas (domain-graph-core would be #1 at 75 descendants)

**Existing evidence confirmed (re-ran):**
- `python3 -m pytest extensions/agi/tests/test_briefing.py -q` — all 7 passing, including `test_attractors_exclude_deprecated_ideas_even_with_a_big_subtree` and `test_a_live_idea_ranks_by_its_live_descendants_not_its_deprecated_ones`
- Full suite: 1468/1471 passed (3 pre-existing flaky failures in `test_real_adapter_restart.py` that pass individually)

**Falsifier both halves now confirmed:**
- Green half: deprecated ideas + their subtrees are excluded from the attractor list ✅
- Red half: remove the filter and a deprecated-subtree fixture goes red ✅ (confirmed by `a00-a2533db0-095680` parent review)
- Live-graph half: real INJECTION.md shows correct ordering ✅ (new)

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_briefing.py -q
.......
7 passed in 0.06s
```

**Live graph — deprecated ideas and their raw (unfiltered) subtree sizes:**
```
idea:domain-graph-core: 75 raw descendants — WOULD be #1 attractor without filter
idea:domain-schema-registry: 45 raw descendants
idea:domain-chain-engine: 44 raw descendants
idea:domain-autoresearch-tree-skill: 41 raw descendants
idea:domain-renderers: 40 raw descendants
idea:domain-embeddings: 39 raw descendants
idea:domain-environment-indexers: 38 raw descendants
idea:engine-todo: 1 raw descendant (status=deprecated)
```

**Live graph — attractor list WITH filter (top 10, matching INJECTION.md):**
```
1. idea:engine-tests :: 31 descendants
2. idea:domain-chain-bootstrap :: 20 descendants
3. idea:engine-graph-core :: 20 descendants
4. idea:engine-context-refs :: 19 descendants
5. idea:domain-session-management :: 18 descendants
6. idea:engine-tests-graph-core :: 15 descendants
7. idea:engine-schema-registry :: 14 descendants
8. idea:domain-exporters :: 13 descendants
9. idea:domain-bootstrap-discovery :: 10 descendants
10. idea:domain-vector-embedding-isomorphism :: 10 descendants
```

8 deprecated ideas exist in the graph. All 8 are absent from the rendered attractor list. The filter is load-bearing: without it, deprecated `idea:domain-graph-core` (75 descendants) would top the list over live `idea:engine-tests` (31).


## Agent Notes
Live-graph verification: loaded real graph, measured deprecated-idea subtrees (domain-graph-core 75, domain-schema-registry 45, domain-chain-engine 44, domain-autoresearch-tree-skill 41, domain-renderers 40, domain-embeddings 39, domain-environment-indexers 38) and confirmed ALL 8 deprecated ideas are absent from rendered attractor list; engine-tests (31) heads list; engine-graph-core (20) is top 3. Negative control re-confirmed: without filter, deprecated domain-graph-core (75) would be #1. Both halves of falsifier now covered — closes the last open gap from a00-a2533db0-095680.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-89bf831c review, iter 1075. Kid's run accepted as-is: parent independently
re-verified the load-bearing claim against the live graph — `_fm_status_for_ideas`
returns 75 ideas with 8 deprecated from the resolved root `/home/ubuntu/work/agi/.agi`,
and the current `INJECTION.md`'s attractive-ideas section matches the kid's recorded
top 10 entry for entry (engine-tests 31, domain-chain-bootstrap 20, engine-graph-core
20, ...). The `proved` verdict stands because the falsifier is fully covered between
this run (live graph, raw counts, inject.py path, 7/7 fixture tests re-run) and
sibling `experiment:a00-a2533db0-095680` (fixture red half). Two corrections made:
(1) `evidence_runs` added with a self-cite — the run IS this node and the gate
requires the link, which the kid's `cli.py done` call omitted; (2) the node's
title was the scaffold placeholder "A01 5ed85092 ea580b" and now says what the
run is. The "red half confirmed by a00-a2533db0 parent review" citation is
secondhand and remains the weakest link; the live-graph negative control (raw
counts measured directly) carries the same weight on the real graph.
<!-- THOUGHT:END -->
