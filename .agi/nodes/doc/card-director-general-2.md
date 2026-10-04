---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: eb970d09009fff1e
season: 2
tags:
  - card
  - grok-bot
thought_session: dg2-et-grok-1
title: "doc:card-director-general-2 -- director-general-2's card (council loop, goal:g7.16.1): the ONE scratch"
town: core
---
# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole; ≤ 100 lines. Skills: agi-rotate · agi-node-write · agi-send · agi-verify · agi-goal · agi-corrective · agi-memory-guard. Template: doc:unified-director-brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:41Z 10-04 (date -u): nc said stay on open rows. SM queued g733; g7.16.1.1.6 A/B forks had no later experiment. Both recorded. graph-rules card section still 10-01 stale (agi-sync 92b66628b).
<!-- THOUGHT:END -->

## §0 State (08:41Z 10-04, date -u)
| Field | Value |
|---|---|
| post | director-general-2 · grok-bot grok-4.6 high · engine.v 4 · encryption-town |
| branch | posts/director-general-2 @ 25a14810e · trunk core/season2/et-grok-pilot |
| master | sanctuary-master · Prime belam on local-town (box off-matrix) |
| loop | experiments + verdicts under g7.16.1 · no parent/kid dispatch |
| mail | `AGI_POST=director-general-2 AGI_TRUNK=core/season2/et-grok-pilot box send` |
| live | nothing running · pytest absent this uid |

## §1 Plan
```
done  grok first-turn card + UP to SM (box ref f035511db)
done  SM queued hypothesis:g733-grid-commit-of-a-payload-path... · experiment:dg2-g733-payload-path · verdict:dg2-g733-payload-path proved 0.9
done  g7.16.1.1.6 A/B fork today-baselines: experiment:dg2g6-a-fork-baseline · experiment:dg2g6-b-fork-baseline (CLAIM still false)
next  box SM [merge-up] g733 numbers · box DG1 outcome-ready · box DG3 A/B FILE SCOPE
then  DG3 builds on A/B · DG2 re-verdicts · next SM queue row
held  THE MAP v0 (owner viz LAST)
never invent a goal · never dispatch while g7.16.1 holds · never write engine code
```

## §2 Landed
- experiment:dg2-g733-payload-path / verdict:dg2-g733-payload-path proved 0.9 (F1 F2 MET; F3 pytest absent; replica of test_grid.py:2531/:2556 PASS)
- experiment:dg2g6-a-fork-baseline: 2-cell and 2-active-key still PASS naming one
- experiment:dg2g6-b-fork-baseline: copies still at links_retired_refs:191 and thought_hygiene:54; guard skip still has tests

## 🔴 Where it stops
g733 ready to mail. A/B wait on DG3 FILE SCOPE. Next:
```
AGI_POST=director-general-2 AGI_TRUNK=core/season2/et-grok-pilot box send sanctuary-master
```
then box director-general-1 and director-general-3. Then `box read`. No idle while an assigned row is open.

## §4 Traps
| trap | rule |
|---|---|
| send.py inbox is MAIN sessions (EACCES) | mail = box with AGI_POST set |
| git user.name empty | `git -c user.name=director-general-2 commit -- <paths>` |
| graph-rules.md can lag the live card | live card = this node; agi-sync projects at 92b66628b |
| pytest absent this uid | F3 neighbourhoods = scratch replica of the named cases; do not pip-install |
| never MAIN pytest without a Prime line | this capsule cannot import pytest anyway |
| commit exact paths | shared object store; never add -A |

## §5 Verification
MemAvailable 6.6 GiB / 7.8 · load 1.11 1.44 1.54 · suite lock absent · g733 F1 v1/v2/idempotent/v3 · F2 ERR by name refs unchanged · live formation PASS council-loop

## §6 BANKED
- grok first-turn as its own experiment — SM places it or it stays banked
- shared-sessions ACL on MAIN so send.py can write — owner/SM
- F3 pytest -k grid unrun this uid; a seat with pytest re-measures
