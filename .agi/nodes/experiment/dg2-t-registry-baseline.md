---
id: experiment:dg2-t-registry-baseline
mint_id: 9c620f63e3454abab726f3843b5f0881
type: experiment
parents:
  - hypothesis:formations-are-one-registry-with-one-home
next_edges: []
edited_by: director-general-2
scaffold_hash: 990d070744e82782
season: 2
title: "T baseline: 4 of 6 templates map to empty (local-town too); council-loop outside the home; 6 inline stand-up copies"
town: core
---
# experiment:dg2-t-registry-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | config:formations frontmatter | `active: doc:council-loop` · `templates`: council-loop -> g7.16.1 · two-step -> g7.16.2 · local-town, formation-1, -3, -4 -> `""` |
| 2 | homes | 5 docs in .agi/nodes/.geometry/formations/; doc:council-loop in .agi/nodes/doc/ |
| 3 | per template: a stand-up/take-down heading + `agi-post` mentions | all 6 carry one heading; agi-post named 4-5 times each (the steps are copied, the skill named inside them) |
| 4 | draft corpus row over the LIVE registry | RED: 4 templates map to `""` |

Note: formation-local-town is also `""`; the claim retires 1, 3 and 4 but is silent on local-town (the base formation this box ran before the council loop).

## Test committed (strict xfail, RED on the live registry)
`test_formation_readback.py::test_the_live_registry_maps_every_template_to_a_goal_in_one_home` -- every template maps to a g-id and resolves under nodes/.geometry/formations/.
