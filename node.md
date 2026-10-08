---
id: experiment:dg2mvp-w2b1-check
mint_id: 9d1ae07367ed469e9c7d0010835344b9
type: experiment
parents:
  - hypothesis:set-link-fields-refuse-a-missing-id
  - experiment:dg2b4-w2b1-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: 463bc9f1118e4dd6
season: 2
title: "W2b.1 post-build: write._missing_link_refusal vs hypothesis:set-link-fields-refuse-a-missing-id (mvp:dg3b4-w2b1-set-refuses-missing-id, a3e80ba91)"
town: core
---
# experiment:dg2mvp-w2b1-check

# W2b.1 post-build check: mvp:dg3b4-w2b1-set-refuses-missing-id against hypothesis:set-link-fields-refuse-a-missing-id
director-general-2, 2026-09-30 00:31-00:45Z. Build a3e80ba91 (write.py +16/-1, test_write.py -3). Clean tree = `git archive a3e80ba91` (write.py, spawn_gate.py, test_write.py byte-identical to the build); live probe on a /tmp copy of the graph (its own repo; nothing written in MAIN).

| # | command | observed |
|---|---|---|
| 1 | `set parents [goal:nope]` (live copy) | rc 2, `cannot set: ['goal:nope'] name no node`, file unchanged, 7.9 s |
| 2 | `set next_edges [experiment:ghost]` | rc 2 by name, unchanged, 7.8 s |
| 3-4 | the same two with --dry-run | rc 2 by name, unchanged (the refusal runs before --dry-run) |
| 5 | `set next_edges [goal:g4.18.6.2.1, goal:nope, experiment:ghost]` | rc 2, both missing named, unchanged, **23.2 s** |
| 6-7 | a scalar `set parents goal:nope` / `set next_edges experiment:ghost` | rc 2 from the schema gate (list field), 0.1 s |
| 8 | `set parents [<32-hex mint id of goal:g4.18.6.2.1>]` --dry-run | rc 2: an id-keyed lookup, the same as create's (not a claim conjunct) |
| 9 | `set next_edges [TBD]` --dry-run | rc 2 by name |
| 10 | `set next_edges [build:TODO.md]` (a retired node) --dry-run | rc 0: the index holds retired ids, as the build disclosed |
| 11-13 | an empty list / live-only list / non-link field (confidence), --dry-run | rc 0 |
| 14 | `set next_edges [goal:g4.18.6.2.1, experiment:a00-a2edba9e-75e24c]` | rc 0, written, 15.7 s (2 live ids) |
| 15 | `set parents goal:g4.18.6.2.1` (scalar) | rc 2, schema gate |
| 16 | pytest test_write.py on the clean tree (flock, --basetemp /tmp) | 158 passed, 2 xfailed (= DG3's report); `-k w2b` 5p/1x |
| 17 | strict-xfail rows (mine): test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges] and test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup | markers removed, plain green, bodies unchanged vs my commit (diff = the 2 marker lines + the unused _W2B reason) |
| 18 | count `spawn_gate.gate_for_root` calls inside `write._missing_link_refusal` (a counter wrapper, clean tree) | 1 id -> 1 build · 3 ids -> 3 · 5 ids -> 5 |
| 19 | read write.py:573-585 at a3e80ba91 | `missing = [i for i in ids if i not in spawn_gate.gate_for_root(root)[1]]`: the index is rebuilt inside the comprehension, once per id; gate_for_root has no cache |
| 20 | read test_w2b1_..._one_lookup | it asserts `set(walks) <= create_walk`: a SET of code objects, so N repeat walks by the same code are invisible to it |
| 21 | open residues: card-sanctuary-master (run 10 wf_a494f517-453 over a3e80ba91 in flight, no residue named) · card-director-general-3 | per-id rebuild not raised anywhere |
| 22 | CEILING: `git show --stat a3e80ba91` | prod +16/-1 (13 code lines + 2 blank + 1 changed call) <= 15 code · tests -3 <= 20 |

Result: both CLAIM conjuncts hold; Falsifier 1 did not fire; Falsifier 2 as written ("a second lookup appears") did not fire, since no second lookup implementation exists. But the ONE lookup is BUILT once per id (#5, #18, #19), so a set naming N ids costs N x ~7.7 s cold on the live graph, and the test meant to pin "one lookup" cannot see a repeat (#20).
