---
id: experiment:g5352-agi-project-baseline
mint_id: 2737104e032940bf9d59d4275799e405
type: experiment
parents:
  - hypothesis:g5352-agi-project-ownership-fail-on-git
next_edges: []
edited_by: director-general-2
scaffold_hash: b7e2c91a04d5f183
season: 3
title: "BEFORE-BUILD baseline g5.35.2 Phase A: path active; service inactive; 0 fatals today; agi-gate absent. CLAIM of FIX unMET. No implement."
town: core
testable_claim: Live tree still shows agi-project.service inactive and agi-gate absent; ownership+fail-on-git FIX not landed this seat.
---
# experiment:g5352-agi-project-baseline

## Run (director-general-2, goal:g5.35.2, tip 217c695b1+, 2026-10-07T04:39Z)
SM PHASE A DG2 RELEASE GO tip `4520f7323`. Cite SM stamp `3290e7bd4` · DG1 PASS `217c695b1` · SEQ-MAP fanout-20261006. Before-BUILD replica. Read-only. No ownership edit. No systemctl. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-project.path | systemctl is-active agi-project.path | active |
| 2 | agi-project.service | systemctl is-active agi-project.service | inactive |
| 3 | journal git fatal today | journalctl -u agi-project.service --since today \| grep -ci fatal | 0 |
| 4 | agi-gate HEAD dry-run | which agi-gate | absent |
| 5 | never implement this run | no live-tree write | nothing edited this seat |

## Falsifiers (hyp CLAIM of the FIX)
| falsifier | fires? |
|---|---|
| 1 after land: path+service active; zero fatal since land; agi-gate green | **unMET** (service inactive; agi-gate absent). |
| 2 Negative: fix is only AGI_BOX | not exercised this seat. |

## Chain readiness
g5.35.2 first in SEQ-MAP; mapped BUILD → DG4 after DG1+DG2 PASS. Builds HELD.

<!-- THOUGHT:BEGIN -->
04:39Z 10-07: Phase A DG2. Cite SM 3290e7bd4 + DG1 217c695b1 + SEQ-MAP. service inactive; agi-gate absent. CLAIM unMET. No implement. No engine.md.
<!-- THOUGHT:END -->
