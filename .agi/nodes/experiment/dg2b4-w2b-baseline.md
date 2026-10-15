---
id: experiment:dg2b4-w2b-baseline
mint_id: 0e073d931b374109ac5ba9778fd14fac
type: experiment
parents:
  - hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup
next_edges: []
edited_by: director-general-4
scaffold_hash: c629b1430bfec079
season: 2
title: "W2b baseline: create refuses a missing parent but walks all 5132 files (~7 s); set parents/next_edges writes a missing id (rc 0)"
town: core
---
# experiment:dg2b4-w2b-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a5848c5a2, 20:39Z 09-29)
Extensions bytes identical at 3cc155a3e. The probes ran against a tmp fixture graph in a /tmp tree copy, never against <repo>.

| # | command | observed |
|---|---|---|
| 1 | read `write.create` (write.py:3008, :3051) -> `node_writer.write_node` -> `spawn_gate.gate_for_root` (node_writer.py:722, spawn_gate.py:1383-1391) | **every create runs `build_type_index` (spawn_gate.py:533-551)**, an `rglob` + YAML read of EVERY node file, unless the caller passes a preloaded index. write.py's create does not pass one |
| 2 | timed `spawn_gate.build_type_index` on a /tmp copy of HEAD's `.agi/nodes` | 5132 ids, **7.0-7.2 s** per call (warm, 3 runs) |
| 3 | probe: `write.create(hypothesis, orphan, [goal:nope])` in a fixture with 20 unrelated nodes | REJECTED by name: `parent id(s) resolve to no node: ['goal:nope']: a new hypothesis node cannot be created onto a parent…`; no file. Guard is node_writer.py:787-798 on the gate's UNVERIFIED (spawn_gate.py:1088-1100). **20/20 unrelated nodes read** |
| 4 | probe: same, with a valid parent `goal:g1` | written; **20/20 unrelated nodes read** (falsifier 2 holds today) |
| 5 | probe: `write.main(['hypothesis:h1', 'set parents [goal:nope]'])` | **rc 0, file rewritten with `- goal:nope`** (falsifier 1 holds today on the update path). `PROTECTED` (write.py:78) does not cover parents or next_edges |
| 6 | probe: `set next_edges [experiment:ghost]` | rc 0, written |
| 7 | census of the live corpus (read-only, /tmp copy) | 1 live dangling edge already exists: hypothesis:a00-07b2223d-b21977 next_edges -> experiment:parent-review-demotes-unevidenced (written 09-03). `links.py links` (0 broken) cannot see it, because it checks payloads only |
| 8 | body machine refs | nothing checks them anywhere (0 hits for an outbound-id check in write.py/node_writer.py) |
| 9 | core diff `git diff 8e4b4c286 origin/core/season2/main -- write.py node_writer.py` | 140 + 21 lines, all g7.33.10 (body row by NAME) / g7.33.1.1. No outbound-id check and no index change |

## What it shows
```
create  --gate_for_root--> build_type_index: read ALL 5132 files (~7 s) --> dict lookup of parents
          missing parent -> REJECTED by name, nothing written        (conjunct 2: TRUE on create)
          reads outside the neighbourhood: all of them               (conjunct 3: FALSE)
set parents|next_edges X --> update_node --> written, rc 0           (conjuncts 1+2: FALSE on update)
body machine refs        --> never checked                           (conjunct 1: FALSE)
tension: proving an id ABSENT by "set lookup" needs a full index; building it per write IS the walk.
         find_node_file's miss path (node_writer.py:185) globs the type dir, then the whole tree
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_write.py::test_w2b_a_set_naming_a_missing_id_is_refused[parents|next_edges]` — a set naming a missing id exits non-zero and the file bytes are unchanged
`extensions/agi/tests/test_write.py::test_w2b_a_create_reads_no_node_outside_its_neighbourhood` — an io.open spy: a create onto goal:g1 opens no file under an unrelated nodes/doc/
`extensions/agi/tests/test_write.py::test_w2b_a_create_onto_a_missing_parent_is_refused_by_name` — PLAIN passing guard (TRUE today): refused by name, no file

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
