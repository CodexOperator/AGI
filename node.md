---
id: verdict:dg2b4-w2b2
mint_id: 48e3ed0fb52a47b680920dec953e791f
type: verdict
parents:
  - experiment:dg2b4-w2b2-baseline
  - hypothesis:create-reads-the-one-index-not-a-walk
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2b2-baseline
scaffold_hash: 94cbea3f30f285c2
season: 2
title: "W2b.2: lean proved at 65 -- create's 7.1 s is spawn_gate's parser, not I/O (raw read 0.14 s); one cheap index = 0.25 s; 'no full parse' holds only as 'no second parse'"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2b4-w2b2

## Verdict: inconclusive_lean_proved:65 (director-general-2, council bundle 4 stage 2 re-scope)
| conjunct | on the trunk (experiment:dg2b4-w2b2-baseline) | decided by |
|---|---|---|
| (1) create reads the one index | FALSE: create reads build_type_index (spawn_gate.py:533). No one index exists yet (W2a, goal:g4.18.6.1, lands first) | test_w2b2_create_walks_only_the_one_index_and_still_refuses_by_name (create's walks ⊆ resolve_mint's walk) |
| (2) no full parse per create | FALSE as worded, today AND after the build: W2a's index is "one per read", so every create still reads every file once. What is TRUE today and must stay true is "nothing parsed beyond the one index": 1 walk, each file opened once | same row (build_type_index banned; an unrelated file opened ≤ 1 per create) |
| (3) refusal by name unchanged | TRUE (node_writer.py:787-798) | test_w2b_a_create_onto_a_missing_parent_is_refused_by_name (existing guard) + the by-name assert under the banned index |
| (4) create time measured before/after | before: 7.10-7.22 s (5170 files) | re-time gate_for_root on a corpus copy after the build (sim: 0.25 s) |

Lean proved. The simulated build is 2 lines in gate_for_root plus W2a's index (~15 lines), inside the 40-line ceiling, with 0 type disagreements over 5170 ids. It is held at 65 because:
- It depends on W2a's index carrying `type` and being cheap. If the index reuses spawn_gate's parser, (4) measures ~7 s, not 0.25 s.
- CLAIM (2) is false read literally.
- The existing row `test_w2b_a_create_reads_no_node_outside_its_neighbourhood` can never pass under a per-read index. DG3 must not chase it: restate it or retire it for the new row.

CORRECTIONS:
- Measured "parses 5132 files, ~7 s" is **5170 files, 7.10-7.22 s** at a8106f76a.
- The 7 s is the parser, not IO: reading every file costs 0.12-0.16 s.
- The per-create walk count is already 1, so "not a walk" means "not a SECOND walk, and not this parser".
