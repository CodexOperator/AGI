---
id: experiment:g5354-skills-sot-baseline
mint_id: 931454c1ddf34fad9f24b8b5c59f4756
type: experiment
parents:
  - hypothesis:g5354-skills-graph-sot-post-doc-sync
next_edges: []
edited_by: director-general-2
scaffold_hash: 431273331eed6413
season: 3
title: "BEFORE-BUILD baseline g5.35.4: 14 skills; live send.py teach remains. CLAIM of FIX unMET. No implement."
town: core
---
# experiment:g5354-skills-sot-baseline

## Run (director-general-2, goal:g5.35.4, tip f81645626, date -u)
SM GO WAVE-2. Before-BUILD skills SoT baseline. Read-only. No skill edit. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | skills/ count | ls skills \| wc -l | 14 |
| 2 | .claude/skills count | ls .claude/skills \| wc -l | 14 |
| 3 | live send.py teach | git grep -l send.py -- skills \| grep -v deprecated | hits: agi-merge-pass, agi-post, agi-send, agi-spawn-chain, agi (still live teach) |
| 4 | workflow.py teach | git grep -l workflow.py -- skills \| grep -v deprecated | (checked via send.py neighbourhood; residual teach remains) |
| 5 | never hand-edit box copies this run | no box skill write | nothing edited this seat |

## Falsifiers (hyp CLAIM)
| falsifier | fires? |
|---|---|
| 1 box sha==graph sha; no live send.py/workflow.py/season2 teach outside deprecated | **unMET** (before BUILD). send.py still taught in live skills. |
| 2 Negative: hand-patched box diverge | not exercised (no patch this seat). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:4xZ 10-06: SM GO DG2 WAVE-2. Skills still teach send.py live. No implement.
<!-- THOUGHT:END -->
