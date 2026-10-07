---
id: experiment:g53474-joint-one-bash-arm-baseline
mint_id: c3f0e5a41d9f6b8c2e1f7a4d0b6c9385
type: experiment
parents:
  - hypothesis:g53474-joint-g5346-g5347-one-bash-arm-regression
next_edges: []
edited_by: director-general-2
scaffold_hash: 7a1f4c3e9d056b28
season: 3
title: "BEFORE-BUILD baseline g5.34.7.4 Phase A: agi-rc single arm sources orient+mail-wake; formal joint regression after g5.35.2 HELD. No implement."
town: core
testable_claim: One rcfile arm observed locally; joint wake-then-orient regression CLAIM unMET until BUILD land after g5.35.2.
---
# experiment:g53474-joint-one-bash-arm-baseline

## Run (director-general-2, goal:g5.34.7.4, tip 217c695b1+, 2026-10-07T04:39Z)
SM PHASE A DG2 RELEASE. Cite SM `3290e7bd4` · DG1 `217c695b1` (NEW hyp). SEQ-MAP. Before-BUILD joint-regression readiness. Read-only. No engine.md. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-rc single arm | cat ~/bin/agi-rc | one rcfile: orient latch then . ~/bin/mail-wake |
| 2 | mail-wake after orient | mail-wake header + agi-rc order | watch intended AFTER orient (agi-run); keys refs/box tip shas |
| 3 | ### pieces in extensions | git grep exec bash -i -- extensions .agi/nodes/.geometry | 0 hits this tip (arm is projected bins, not extensions body) |
| 4 | never implement this run | no engine-post/wrap edit | nothing edited this seat |

## Falsifiers (hyp CLAIM)
| falsifier | fires? |
|---|---|
| 1 grep -c exec bash -i == 1; one reproject o shows wake then orient | design baseline; formal joint land HELD. |
| 2 card commit fail => no kill; g5.34.6 W2-W5 still pass | not exercised this seat. |
| 3 Negative: two bash arms / land before g5.35.2 / split .6 vs .7 | HOLD preserved; chain says joint after .35.2. |

## Chain readiness
Mapped BUILD → DG7 after DG1+DG2 PASS. Joint land of g5.34.6.2 + g5.34.7.2–.4 after g5.35.2 → one reproject. Builds HELD.

<!-- THOUGHT:BEGIN -->
04:39Z 10-07: Phase A DG2 NEW hyp g53474. Cite SM 3290e7bd4 + DG1 217c695b1. One agi-rc arm. Joint after .35.2 HELD. No implement.
<!-- THOUGHT:END -->
