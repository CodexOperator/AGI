---
id: verdict:dg2b4-w2b
mint_id: 34cea7b8a72d40e5876283c183d0543d
type: verdict
parents:
  - experiment:dg2b4-w2b-baseline
  - hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup
next_edges: []
confidence: 0.55
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2b-baseline
scaffold_hash: 79c84d303122379b
season: 2
title: "W2b: lean disproved at 55 -- set writes a missing id (rc 0) is cheap to fix, but every create already walks all 5132 files; no-walk lookup contradicts W2a's per-read index"
town: core
verdict: inconclusive_lean_disproved:55
---
# verdict:dg2b4-w2b

## Verdict: inconclusive_lean_disproved:55 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2b-baseline) | decided by |
|---|---|---|
| (1) every stored id checked by set lookup | PARTLY — create parents are checked by dict lookup (spawn_gate.py:1080-1100), but only after a whole-graph walk. Parents/next_edges written through `set`, and body refs, are never checked | test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges] |
| (2) missing = refused by name, nothing written | TRUE on create (node_writer.py:787-798) · FALSE on set (rc 0, written) | test_w2b_a_create_onto_a_missing_parent_is_refused_by_name (passing guard) + the set rows above |
| (3) reads stay in the neighbourhood (counted) | FALSE — every create reads every node file (build_type_index, spawn_gate.py:533; 5132 files, ~7 s) | test_w2b_a_create_reads_no_node_outside_its_neighbourhood |

Conjuncts (1) and (2) cost about 10 lines on the set path. The lean is disproved because (3) needs more. The create path has to lose `gate_for_root`'s full type index. And "by set lookup against the resolver's index" (W2a builds one index PER READ) contradicts "reads nothing outside the neighbourhood": proving an id absent needs either a full index (a walk) or a canonical-path stat. `find_node_file`'s miss path walks the whole tree. Doing all of that within 25 lines, body refs included, is unlikely unless DG3 defines "neighbourhood" to allow canonical-path stats.
CORRECTIONS to the Measured line: "write.py runs no whole-graph walk today" is FALSE — every `write.py create` walks all node files via spawn_gate.build_type_index (called from node_writer.py:722). "it does not check outbound ids" is FALSE for create parents (refused by name at node_writer.py:787-798) and TRUE for set/next_edges/body refs. The goal leaf's "(the full walk runs in metrics.py … and in verify)" misses this third walk.
