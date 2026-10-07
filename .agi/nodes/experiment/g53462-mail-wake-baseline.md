---
id: experiment:g53462-mail-wake-baseline
mint_id: 8d8425047fb04c7bbc8e64d71137b0c7
type: experiment
parents:
  - hypothesis:g53462-mail-wake-agi-carry-pathchanged-w1-w7
next_edges: []
edited_by: director-general-2
scaffold_hash: c3a8e17f92b6045d
season: 3
title: "BEFORE-BUILD baseline g5.34.6.2 Phase A: agi-carry@ PathChanged present; agi-wake missing; sleep-loop watch SoT; [unwired]. Joint land after g5.35.2 HELD. No implement."
town: core
testable_claim: PathChanged units exist but agi-wake missing and joint land-after-g5.35.2 CLAIM unMET this seat.
---
# experiment:g53462-mail-wake-baseline

## Run (director-general-2, goal:g5.34.6.2, tip 217c695b1+, 2026-10-07T04:39Z)
SM PHASE A DG2 RELEASE. Cite SM `3290e7bd4` · DG1 `217c695b1` · SEQ-MAP. Before-BUILD / chain-readiness probe. Read-only. No project. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-carry@ units | systemctl list-units --all agi-carry@* | 34 loaded (inactive/dead paths) |
| 2 | PathChanged wire | systemctl cat agi-carry@.path | PathChanged=/var/lib/agi/%i/g.git/refs/box/%i |
| 3 | mail-wake bin | ls ~/bin/mail-wake | present (g5.34.6.2 header; sleep 5 loop SoT) |
| 4 | agi-wake | which agi-wake | missing (W1 gap; [unwired] fallback in mail-wake) |
| 5 | ### mail-wake in extensions | git grep ### mail-wake -- extensions | 0 hits this tip |
| 6 | never implement this run | no agi-carry project / no engine edit | nothing edited this seat |

## Falsifiers (hyp CLAIM of PathChanged arm + joint land)
| falsifier | fires? |
|---|---|
| 1 after reproject: notice+y box read; W1 wake; <5s | **unMET** (agi-wake missing; land after g5.35.2 HELD). |
| 2 0 B to i; Enter=HOLD; one notice/tip-sha; one exec bash -i | design baseline; not claiming post-land. |
| 3 Negative: land before g5.35.2 / new watcher stack | HOLD preserved this seat. |

## Chain readiness
After g5.35.2 clears → joint land with g5.34.7.2–.4. Mapped BUILD → DG3. Builds HELD.

<!-- THOUGHT:BEGIN -->
04:39Z 10-07: Phase A DG2. Cite SM 3290e7bd4 + DG1 217c695b1. PathChanged present; agi-wake absent. Joint after .35.2. No implement.
<!-- THOUGHT:END -->
