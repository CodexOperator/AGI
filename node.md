---
id: exp:node-type-corpus-survey
mint_id: c0f08ab06be947f0a9954e0d868f19c2
type: experiment
parents:
  - hyp:spawn-check-on-writer-path
next_edges:
  - verdict:spawn-gate-lands-on-writer-path
confidence: 0.9
edited_by: season.py
season: 1
subgraph: false
tags:
  - s17
  - schema
  - survey
thought_session: season
title: "Corpus survey: the spawn rule table reproduces, and 53 nodes already violate it"
---
# exp:node-type-corpus-survey

**Sub-claim 1 of the hypothesis: is the rule derivable?** Re-ran the S17
survey independently rather than trusting the table in `GOALS.md` §S17.

Runner (re-runnable, gitignored): `sessions/iter-9010/kid-schema/survey.py`.
It reads every `nodes/**/*.md` frontmatter, tallies `type` / `len(parents)` /
resolved parent types, then replays the shipped rules over the same corpus.

## Run 1 — 769 nodes, before this iteration's own writes

```
type                  n maxp parentless  parent types (count)
level3              185    2          2  idea:178, goal:6
hypothesis          105    2         24  idea:77, goal:3, hypothesis:1, experiment:1
task                 91    1          0  hypothesis:91
verdict              83    2         21  experiment:57, verdict:30, hypothesis:12
experiment           75    2          4  hypothesis:40, verdict:31, goal:7, task:1, level3:1, idea:1, experiment:1
goal                 75    1         27  goal:48
idea                 71    1         42  goal:29
mvp                  26    2          0  verdict:20, goal:5, experiment:2, hypothesis:1
outcome              19    2          0  mvp:19, verdict:2
bigger_outcome       17    2          0  outcome:17, mvp:2
app_purpose          15    2          0  bigger_outcome:14, outcome:2, bigger-outcome:1
<none>                3    2          0  idea:1, hypothesis:1, verdict:1, experiment:1
app-purpose           2    1          0  bigger-outcome:2
bigger-outcome        2    1          0  outcome:2
```

**Reproduces §S17 exactly** on every `n`, every `max parents`, and every
parent-type set — `goal` reads 75 not 73 only because two goal nodes (`g6.9`,
`s17` itself) were minted this session. Parentless counts match too: 24
hypothesis, 21 verdict, 4 experiment, 2 level3.

## Four things the §S17 table did not say

1. **Zero unresolved parent references in the entire corpus.** Every parent id
   on every node names a node that exists. That is what makes an
   `allowed_parents` rule checkable at all: the type of a parent is always
   knowable, so a rejection is never a guess.

2. **Three nodes carry no `type:` field at all** —
   `hyp:environment-indexers-r1-chain-extension`,
   `verdict:a01-7031af17-449ecb-r11`,
   `verdict:environment-indexers-r1-chain-extension`. They have ids, mint_ids
   and parents, but the field every schema lookup keys on is absent. No
   schema can ever apply to them; the gate reports them `unverified`. Not
   fixed here — a `type:` written now would be inferred from the directory,
   and inferring is inventing (G7.1).

3. **`goal` has three shapes, not two.** `goal_kind` reads `long-term` (10),
   `short-term` (17), `subgoal` (48), and the correlation with structure is
   exact with zero exceptions:

   | `goal_kind` | n | parents | `goal_id` |
   |---|---|---|---|
   | `long-term` | 10 | 0 | undotted `G7` |
   | `short-term` | 17 | 0 | undotted `S4` |
   | `subgoal` | 48 | exactly 1, always `goal` | dotted `G7.2` |

   This decides sub-claim 2 and it decides the G-goal/S-goal question: see
   `context/schemas/[goal].md`.

4. **The six pre-existing schemas were mostly fiction.** Field-frequency
   measured against each schema's own `required:` list:

   | schema | required field | present | share |
   |---|---|---|---|
   | `[experiment]` | `run_id` | 0/75 | **0%** |
   | `[experiment]` | `verdict` | 5/75 | 7% |
   | `[mvp]` | `source_files` | 0/26 | **0%** |
   | `[outcome]` | `input_shape` | 0/19 | **0%** |
   | `[outcome]` | `output_shape` | 0/19 | **0%** |
   | `[outcome]` | `behavior` | 0/19 | **0%** |
   | `[idea]` | `scale` regex `open\|extended\|abandoned` | `active` used, `extended`/`abandoned` never | — |
   | `[task]` | all of `title, cavekit_req, status` | 91/91 | 100% |

   Four of six schemas required at least one field no node has ever carried,
   and no error was ever raised — because nothing ran them. `[task]` is the
   control: all 91 tasks come from one generator, so declared shape and
   written shape were produced together. **The schemas that drifted describe
   types written by agents, freehand.**

   Also found: `context/schemas/agent_session.md` had no YAML frontmatter, so
   it was not merely inactive — `load_schemas_from_dir` raised
   `FrontmatterError: md file missing opening '---'` and recorded it on
   *every* load. A permanent parse error, sitting unnoticed.

## Run 2 — 778 nodes, corpus replayed against the shipped rules

```
$ python3 sessions/iter-9010/kid-schema/survey.py
nodes with frontmatter: 778
type                    n maxp parentless unresolved  parent types
level3                187    2          4          0  idea:178, goal:6
hypothesis            106    2         24          0  idea:78, goal:3, hypothesis:1, experiment:1
task                   91    1          0          0  hypothesis:91
verdict                84    2         21          0  experiment:59, verdict:30, hypothesis:12
experiment             77    2          4          0  hypothesis:42, verdict:31, goal:7, task:1, level3:1, idea:1, experiment:1
goal                   75    1         27          0  goal:48
idea                   72    1         42          0  goal:30
mvp                    27    2          0          0  verdict:21, goal:5, experiment:2, hypothesis:1
outcome                19    2          0          0  mvp:19, verdict:2
bigger_outcome         17    2          0          0  outcome:17, mvp:2
app_purpose            15    2          0          0  bigger_outcome:14, outcome:2, bigger-outcome:1
<NO TYPE FIELD>         3    2          0          0  idea:1, hypothesis:1, verdict:1, experiment:1
app-purpose             2    1          0          0  bigger-outcome:2
bigger-outcome          2    1          0          0  outcome:2
doc                     1    0          1          0

=== corpus checked against the SHIPPED spawn rules ===
  approved      721
  rejected       53
  unverified      4
  rejections by type+rule:
      24  hypothesis: rule 'min_parents' (1) from context/schemas/[hypothesis].md
      21  verdict: rule 'min_parents' (1) from context/schemas/[verdict].md
       4  experiment: rule 'min_parents' (1) from context/schemas/[experiment].md
       4  level3: rule 'min_parents' (1) from context/schemas/[level3].md
```

**721 of 778 already conform** — 92.7%. The rule is not an imposition on the
corpus; it is a description of it with 53 exceptions.

**Every one of the 53 is the same rule**, `min_parents`. Not one node in the
whole graph exceeds its type's `max_parents`, and not one names a parent of a
type its schema disallows. So `max_parents` and `allowed_parents` are pure
description; only `min_parents` is a claim the corpus contradicts.

The 4 `unverified` are the 3 typeless nodes plus `doc:goals-preamble`, a type
minted this session with no schema yet.

## Deltas between the two runs, stated rather than smoothed

+9 nodes (769 → 778): 6 are this chain, and the rest are the parent agent's
concurrent work in the same checkout (`level3` +2, `verdict` +1, `experiment`
+2, `mvp` +1, `idea` +1, `hypothesis` +1, `doc` +1). Parentless `level3` went
2 → 4; the two new ones are `build:bin-spawn-gate` and
`build:bin-publish-engine.sh`, both minted parentless by the census scan.
**Node count only ever rose.** Nothing was deleted.