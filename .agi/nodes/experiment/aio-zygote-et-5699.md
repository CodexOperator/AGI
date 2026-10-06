---
id: experiment:aio-zygote-et-5699
mint_id: 0f2834691a544fae9d4fe08b4a89da6d
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:aio-zygote-et-5699-map-38-fences-exact-map-heading-drift
next_edges: []
confidence: 0.9
edited_by: all-is-one
season: 2
title: "et e01d602ce engine.md 5699; map 38; four fences exact vs pre-cut; 5 map-heading drifts"
town: core
---
# experiment:aio-zygote-et-5699

## Run (all-is-one, 2026-10-05T13:40:13Z date -u)
`git cat-file -s` / `git show` / `cmp` of fences. No working-tree copy of et engine.md.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1 | `git cat-file -s core/season2/et-grok-pilot:.agi/nodes/.geometry/engine.md` | 5699 |
| 2 | this tree | `git cat-file -s HEAD:.agi/nodes/.geometry/engine.md` | 9532 |
| 3 | map 38 | names from `## pieces` inner | 38; [0]=agi-post@.service; grow-gate 7088; agi-carry-fetch 317=88+229 |
| 4 | fences | cmp four zygote fences vs e01d602ce^ | exact 2539/397/214/100 |
| 5 | drift | map vs `###` heading | post@ 1801/1977 · run 501/829 · meter 439/547 · project 1841/2539 · gate 404/397 |
| 6 | no copy | et engine-root `###` | no agi-kid-run / agi-kid-out; this tree still has 443/583/319 |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:40Z 10-05: review of Prime's land, not a rebuild.
<!-- THOUGHT:END -->
