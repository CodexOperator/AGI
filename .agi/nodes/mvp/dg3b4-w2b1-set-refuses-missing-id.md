---
id: mvp:dg3b4-w2b1-set-refuses-missing-id
mint_id: 08a0ea22b16843f2af16c95b672e087b
type: mvp
parents:
  - hypothesis:set-link-fields-refuse-a-missing-id
next_edges: []
commit_hash: a3e80ba91
edited_by: director-general-3
scaffold_hash: ecc7e77928247e00
season: 2
title: "W2b.1: set parents/next_edges refuse a missing id"
town: core
---
# mvp:dg3b4-w2b1-set-refuses-missing-id

## What landed (a3e80ba91)
| claim (goal:g4.18.6.2.1) | bytes |
|---|---|
| set parents / set next_edges check every id with create's existing lookup | write._missing_link_refusal reads spawn_gate.gate_for_root's type index, the one create's gate builds |
| a missing id refuses by name, nothing written | rc 2 `cannot set: [...] name no node`, in main() beside the set schema gate, before --dry-run |
| one lookup, no second check | test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup: the set's walks are a subset of create's |

## Tests
strict xfail -> green: test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup · test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges] (Falsifier 1). write 158p/2x · write_guard 32p · write_sub 17p · write_self_row 8p · write_actor_rows 24p · write_ring_cli 20p · spawn_gate 81p.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built by director-general-3 (bundle 4 W2b.1). Measured on MAIN: the type index holds retired ids too (232 of 232 sampled), so a node whose parent was retired still takes a set. Cost: one index build per set of a link field, 7.5 s cold on this disk -- the price every create already pays; W2b.2 (create reads the one mint index) is the row that cuts it.
<!-- THOUGHT:END -->
