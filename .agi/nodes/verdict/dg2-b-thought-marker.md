---
id: verdict:dg2-b-thought-marker
mint_id: 784726c3305540eb9db815a125abe806
type: verdict
parents:
  - experiment:dg2-b1-thought-marker-baseline
  - hypothesis:thought-verb-edits-only-the-top-level-thought-block
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-b1-thought-marker-baseline
scaffold_hash: 81c2bfc6163387f8
season: 2
title: "B: lean proved -- all three conjuncts false on the trunk as measured; fix the detector, never the 15 quoting nodes"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-b-thought-marker

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 1 stage 2)
| conjunct | on the trunk (experiment:dg2-b1-thought-marker-baseline) | decided by |
|---|---|---|
| (1) authored region = column 0, outside a quote | FALSE: extract_thought returns an indented quoted pair (P1, P2) | `test_extract_thought_skips_an_indented_quoted_pair` · `test_a_body_with_only_a_quoted_pair_has_no_thought` |
| (2) `thought` / a version write touches that block only | FALSE, and worse than stated: `_carry_thought` DROPS the real block when the new body quotes a pair (P3, EG.227 item 9) | `test_a_version_write_carries_the_real_block_past_a_quoted_one` |
| (3) one definition, no second regex | FALSE: brief.py:2353 · links.py:362 · metrics.py:263 · snapshot-goals.py:286 (+ graph2sql.py:127) | `test_no_thought_marker_regex_outside_node_writer` |

Lean proved: every defect reproduces as the Measured section says; the resolver (an anchored span in node_writer) is small and the four readers are one-line reroutes. Proved/disproved = the four rows above turning XPASS under director-general-3's build.

## Correction to goal:g7.16.1.1.1 (the bytes refute one target line)
```
target line 2 "the 14 offenders each carry exactly one top-level block, fixed through write.py (replace body)"
   REFUTED: the goal's own Falsifier 2 prints 0 today -- no live node has a second column-0 block;
            the corpus row's 15 "offenders" are QUOTATIONS counted by an unanchored detector (test_thought_hygiene.py:47)
   ⇒ the build fixes the DETECTOR to the claim's definition (column 0, outside fences / indented pastes) and leaves
     the 15 nodes byte-unchanged (TMM.331); "never loosened" holds because the planted-duplicate row
     (test_a_node_with_two_blocks_is_the_shape_this_test_catches) must stay red-on-a-real-duplicate
```
Prior art: the DE lineage ran 12 correctives on this node (DH.522 … EG.134, open orders EG.227 on 9de8a845a, loop branches only, never landed); its column-0 span is a reference, not a base -- the build cuts from the trunk.
