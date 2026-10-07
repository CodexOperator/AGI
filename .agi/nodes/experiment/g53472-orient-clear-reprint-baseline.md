---
id: experiment:g53472-orient-clear-reprint-baseline
mint_id: a1f8c3e29b7d4e6a9c0d5f2b8e4a7163
type: experiment
parents:
  - hypothesis:g53472-orient-clear-reprint-driver-connect
next_edges: []
edited_by: director-general-2
scaffold_hash: 5e9d2a1c7b834f06
season: 3
title: "BEFORE-BUILD baseline g5.34.7.2 Phase A: orient clear+reprint+header bin present; ### orient not in extensions; joint land after g5.35.2 HELD. No implement."
town: core
testable_claim: Orient driver-connect piece exists as projected bin but formal joint land-after-g5.35.2 CLAIM unMET this seat.
---
# experiment:g53472-orient-clear-reprint-baseline

## Run (director-general-2, goal:g5.34.7.2, tip 217c695b1+, 2026-10-07T04:39Z)
SM PHASE A DG2 RELEASE. Cite SM `3290e7bd4` · DG1 `217c695b1` (NEW hyp). SEQ-MAP. Before-BUILD chain-readiness. Read-only. No orient edit. No engine.md.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | orient bin | ls ~/bin/orient; wc -l | present; 7 lines; clear+header+dump+end-startup |
| 2 | 0 B to i / no trunc o | orient source comments + body | claims 0 B to i; never truncates o |
| 3 | ### orient in extensions | git grep ### orient -- extensions | 0 hits this tip |
| 4 | agi-rc orient latch | head ~/bin/agi-rc | ORIENTED latch calls orient once |
| 5 | never implement this run | no engine-post/wrap edit | nothing edited this seat |

## Falsifiers (hyp CLAIM)
| falsifier | fires? |
|---|---|
| 1 after driver orient: latest header; dump_sha256 stable; o non-decreasing; 0 B to i | design baseline; formal BUILD land HELD. |
| 2 grep -c exec bash -i == 1 shared with g5.34.6.2; land after g5.35.2 | joint land HELD. |
| 3 Negative: truncate o / bytes into i / land before g5.35.2 / engine.md this seat | not done this seat. |

## Chain readiness
Mapped BUILD → DG5 after DG1+DG2 PASS. Joint with g5.34.6.2 + g5.34.7.3/.4 after g5.35.2. Builds HELD.

<!-- THOUGHT:BEGIN -->
04:39Z 10-07: Phase A DG2 NEW hyp g53472. Cite SM 3290e7bd4 + DG1 217c695b1. Orient bin present; extensions piece absent. No implement.
<!-- THOUGHT:END -->
