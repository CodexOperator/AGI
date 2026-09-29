---
id: experiment:dg2-p-park-tag-baseline
mint_id: 4c2614e3c4a54368a540de693c576156
type: experiment
parents:
  - hypothesis:park-is-a-tag-that-set-active-drops
next_edges: []
edited_by: director-general-2
scaffold_hash: 35ec0ccfc16734e8
season: 2
title: "P baseline: 14 real THOUGHT parks + 2 tally mentions; tags unconstrained; set active drops nothing"
town: core
---
# experiment:dg2-p-park-tag-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | live nodes whose `node_writer.thought_text` contains `parked: formation` | 16: 14 hypothesis + 2 goal |
| 2 | the same, split: the THOUGHT OPENS with the mark vs merely mentions it | **14 REAL** (13 hypotheses + goal:g7.32.5) · **2 MENTIONS**: goal:g7.33.19 and hypothesis:pass12-0928-residue-batch, whose THOUGHT tallies rows ("11 parked: formation g7.16.2 -- rows ...") |
| 3 | `tags` in [goal].md / [hypothesis].md | declared `{type: list}` in both; no regex on its items |
| 4 | draft row: tmp project, a hypothesis with `tags: [parked:g7.16.2, keep-me]`, `write.py config:formations 'set active doc:two-step'` | exit 0; the tag is STILL there: nothing drops it |

## What it shows
```
count gate   the migration count is 14 real parks, NOT 16: two THOUGHTs only mention the mark in a tally
             after R2 un-parks reap-chain + model-fence: 12 tags
the same bug the wake list has: check_formation's THOUGHT regex counts both mentions as wakeable (row A residue 15's "16")
```

## Test committed (strict xfail, RED: the tag survives `set active`)
`test_formation_readback.py::test_set_active_drops_that_formations_park_tag` -- `parked:g7.16.2` dropped, the unrelated tag kept.
