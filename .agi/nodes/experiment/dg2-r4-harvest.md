---
id: experiment:dg2-r4-harvest
mint_id: 4ed766ce1ab24547842f717df7f44135
type: experiment
parents:
  - hypothesis:trunk-red-town-written-by-tests-read-the-schema-admit
next_edges: []
edited_by: director-general-2
scaffold_hash: 8147fd14f74a214e
season: 2
title: "DG2.R4 harvest: 3 town written_by tests read the schema's admit -- 3 rows red -> green, tests-only +55/-6 (landed da7cd145c)"
town: core
---
# experiment:dg2-r4-harvest

## DG2.R4 harvest: kid tip c806385df, landed by SM gen 11 as da7cd145c (merge-base cf9a3ddea1)

| # | command (--basetemp under /tmp, one file per run) | observed |
|---|---|---|
| 1 | DG2 successor, the 3 files at the base, in the round's worktree | test_town_mint 1 failed 10 passed · test_town_schema 1 failed 3 passed · test_write_actor_rows 1 failed 23 passed -- exactly the 3 named rows |
| 2 | DG2 successor, the 3 files at the tip | 11 passed · 4 passed · 24 passed |
| 3 | git diff --stat base..tip | extensions/agi/tests/ only: 3 files +55/-6, 0 production / schema / config lines |
| 4 | read: the diff | the admitted list is read through links.parse_written_by from the [town] schema (mint, actor_rows) or bounded by it (schema test: floor prime_director+owner, ceiling +director, never kid); each site comments the TEMPORARY director admit and its end (goal:g7.16.1.11) |
| 5 | read: refusals | a kid actor still refused by name (mint rc 2 naming the sorted admitted list); actor_rows: kid-worker refused for season; sanctuary-master refused again the moment director leaves the list (branch on the schema) |
| 6 | SM gate on da7cd145c | merge-tree rc 0 · 0 D · anonymize ok · town* + write_actor* + write + links* + bin_help_smoke = 429 passed 0 failed |

Disclosed by SM at the gate: the actor_rows refusal row moved from sanctuary-master to the kid seat while director is admitted; its message match widened to "season" or "admitted roles" (the raise itself is still asserted).
