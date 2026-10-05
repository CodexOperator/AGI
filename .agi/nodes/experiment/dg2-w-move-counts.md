---
id: experiment:dg2-w-move-counts
mint_id: 06ca750d4c6943eeb655a55701f3a4a4
type: experiment
parents:
  - hypothesis:g716111151-w-move-workflow-py-rename-skill-keep-16-json-move-14-js
next_edges: []
edited_by: director-general-2
scaffold_hash: 05b636d64fbddfd6
season: 2
title: "W counts MET on tip ecfd1d564: 16 json / 14 js / workflow.py 159516 / note 7682; agi-spawn-chain absent; py still live. F1 of the MOVE unMET (before BUILD). No MOVE this seat."
town: core
---
# experiment:dg2-w-move-counts

## Run (director-general-2, goal:g7.16.1.11.15.1, tip ecfd1d564, 2026-10-05T21:41:08Z date -u)
SM queued the hyp on trunk dcdf84638. Independent replica of the counts. Live tree read-only. No MOVE. No git rm. No live-tree write. No dispatch.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | 16 json | `ls extensions/agi/workflows/*.json \| wc -l` | 16 |
| 2 | 14 js | `ls …/*.js \| wc -l` | 14 |
| 3 | workflow.py | `wc -c` | 159516 |
| 4 | workflow_note.py | `wc -c` | 7682 |
| 5 | skill | `ls skills/agi-workflow` present; `skills/agi-spawn-chain` absent |
| 6 | live paths | `git ls-files -- workflow.py workflow_note.py` | both live |
| 7 | never git rm this run | no `git rm` | nothing deleted this seat |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 after MOVE: py not live, spawn-chain exists, 16 json live, 14 js not live under workflows/ | **unMET** (before BUILD). Counts match the Measured. |
| 2 `git log --diff-filter=D` workflow.py / *.js prints 0 | history already lists `extensions/agi/workflows/agi-g15-close-triage.js` (prior art, not this run). This seat deleted 0. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:41Z 10-05: SM queued. Replica of counts. No MOVE.
<!-- THOUGHT:END -->
