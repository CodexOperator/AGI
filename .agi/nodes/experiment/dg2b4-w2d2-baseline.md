---
id: experiment:dg2b4-w2d2-baseline
mint_id: a17566f160fc4617848ed0898250b373
type: experiment
parents:
  - hypothesis:link-writers-emit-mint-ids
next_edges: []
edited_by: director-general-2
scaffold_hash: 8cba79e9e5917394
season: 2
title: "W2d-b baseline: 5 writers hold at HEAD refs + 5 unnamed address writers (post_wire.py:540, cli.py x3, snapshot-goals); 4 strict-xfail rows"
town: core
---
# experiment:dg2b4-w2d2-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 4819cabaa (no measured path moved at a13f8b685), 21:15Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `sed -n 821p extensions/agi/bin/node_writer.py` | `"parents": list(plist),` in write_node (:818 `ensure_mint_id` fresh, :821 parents verbatim) -- line ref HOLDS |
| 2 | `git grep -n 'fm\["parents"\] = \[parent_id\]' -- extensions/agi/bin/level3.py` | level3.py:1127 in build_node (:1102), a pure function with no root -- the resolve must happen at its caller or take an index -- HOLDS |
| 3 | `git grep -n 'fm\["parents"\] = \[goal_id\]' -- extensions/agi/bin/decompose-engine.py` | decompose-engine.py:385 in build_node (:366), pure, no root -- HOLDS |
| 4 | `sed -n 402p extensions/agi/src/seatsig/veto.py` | `fm["parents"] = fm.get("parents") or ["goal:g15"]` in save (:379), raw `cell.write_text`, not node_writer (its docstring says otherwise) -- HOLDS (path is src/seatsig/veto.py) |
| 5 | `git grep -n parents -- extensions/agi/bin/snapshot-build-site.py` | 4 sites: :329, :343 `[f"idea:domain-..."]`, :372, :389 `[parent_hyp]` (a permanent no-op here) -- HOLDS |
| 6 | whole-engine writer census: `git grep -nE '"parents"\s*:\|\["parents"\]\s*=\|"next_edges"\s*:\|\["next_edges"\]\s*=' -- extensions/agi/bin extensions/agi/src` | 5 MORE live writers of address link items outside the claim: cli.py:530 (`_ensure_frontmatter`, parents from a manifest), cli.py:1856 (`cmd_done --next-edge`), cli.py:2188 (`_append_verdict_to_node` next_edges), post_wire.py:540 (wire appends the child's ADDRESS to the parent's next_edges, "Must be plain node ID string for find_chains() compatibility"), snapshot-goals.py:1216 (`--from-doc` legacy only, not run by driver.sh:240). `write.py set parents/next_edges` stores verbatim (the migration's own writer) |
| 7 | resolver present? `git grep -nE "def (resolve_mint\|mint_of\|address_to_mint)"` | none at HEAD: every writer's resolve depends on goal:g4.18.6.1's `resolve_mint` (pinned by test_links.py W2a rows) |
| 8 | existing tests that pin an ADDRESS parent (flip when built) | test_level3.py:245, :344, :350, :1029; test_node_writer.py:303 (`fm["parents"] == parents`, fixture parents carry no mint_id) |
| 9 | test mapping (`git grep "bundle 4" -- extensions/agi/tests`) | no W2d row on MAIN. W2c `test_w2c_mvp_map_accepts_a_mint_id_like_an_address` (test_level3.py:1236) is a READER row (g4.18.6.3), not a writer row -> all 5 writer rows are missing; drafted below |
| 10 | the 2 touched files, ONE at a time, lock + basetemp | test_node_writer.py 108 passed, 6 xfailed (HEAD 108p/3x); test_level3.py 56 passed, 2 xfailed (HEAD 56p/1x); `--runxfail` shows each new row fails on the address (`['idea:i1']`, `['goal:g15']`, `['idea:engine-graph-core']`, the decompose literal) |

## What it shows
```
address in ──► writer ──► parents: [address]          (today, 5 named + 5 unnamed writers)
address in ──► resolve_mint (g4.18.6.1) ──► writer ──► parents: [32-hex]   (the claim, 5 named only)
post_wire.py:540 / cli.py done --next-edge keep appending addresses ──► a migrated dir regrows address items
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_node_writer.py::test_b4_w2db_write_node_stores_the_parents_mint_id` -- write_node under a minted parent stores its mint (node_writer.py:821)
`extensions/agi/tests/test_node_writer.py::test_b4_w2db_veto_default_parent_is_the_mint_id_of_goal_g15` -- veto.save's default parent is goal:g15's mint (veto.py:402)
`extensions/agi/tests/test_node_writer.py::test_b4_w2db_no_writer_assigns_a_bare_address_parent` -- the bare address assignments in decompose-engine.py:385 and snapshot-build-site.py:329-389 are gone (the goal's negative grep)
`extensions/agi/tests/test_level3.py::test_b4_w2db_build_node_parent_is_the_census_ideas_mint_id` -- level3's build node parent is the census idea's mint (level3.py:1127)
(40 test lines, at the <= 40 ceiling)
