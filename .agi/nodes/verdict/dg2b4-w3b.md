---
id: verdict:dg2b4-w3b
mint_id: f300604eac6c40d3bf048164ae6958ff
type: verdict
parents:
  - experiment:dg2b4-w3b-baseline
  - hypothesis:node-search-lives-beside-node-writer
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w3b-baseline
scaffold_hash: 60622ec3eb028fef
season: 2
title: "W3 B3: lean proved at 85 -- grep_live/parked_carriers move beside node_writer; GrepError must move too; test_formation_readback.py:236-245 joins the file scope"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2b4-w3b

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w3b-baseline) | decided by |
|---|---|---|
| (1) one node-search module beside node_writer holds both | FALSE: both in rotation_record.py:49/:77 | `test_b3_rotation_record_keeps_only_the_record_helpers` + `test_b3_each_node_search_function_has_one_def` (guard, green now) |
| (2) every caller re-pointed | FALSE: verification.py:53/1314/1320/1326/1327, write.py:2353/2361/2362, test_formation_readback.py:236-245 | `test_b3_no_caller_reaches_the_node_search_through_rotation_record[*]` + test_formation_readback.py staying green |
| (3) rotation_record keeps dump/resolve/home_rel only | FALSE (also holds GrepError, grep_live, parked_carriers) | `test_b3_rotation_record_keeps_only_the_record_helpers` |
| (4) write.py no longer imports rotation_record | FALSE (write.py:2353) | `test_b3_no_caller_reaches_the_node_search_through_rotation_record[write.py]` |
A pure move (~37 lines out, ~45 in with a header, ~8 re-pointed): fits <= 30 net. CORRECTIONS: (a) `GrepError` (rotation_record.py:17) must move with the two functions (every caller catches it) -- the hypothesis names only grep_live/parked_carriers; (b) FILE SCOPE misses extensions/agi/tests/test_formation_readback.py:236-245, which monkeypatches `rotation_record.parked_carriers` and raises `rotation_record.GrepError`: after the move it fails (monkeypatch raising=True) unless re-pointed in the same row (+2 test lines). Measured refs :49 :77 :2353 :53 all TRUE.
