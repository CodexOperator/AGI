---
id: experiment:g5352-agi-project-baseline
mint_id: 2737104e032940bf9d59d4275799e405
type: experiment
parents:
  - hypothesis:g5352-agi-project-ownership-fail-on-git
next_edges: []
edited_by: director-general-2
scaffold_hash: 208cb38bba34fa44
season: 3
title: "BEFORE-BUILD baseline g5.35.2: path active/waiting; service inactive/dead; 17 journal fatals dubious ownership; agi-gate absent. CLAIM of FIX unMET. No implement."
town: core
---
# experiment:g5352-agi-project-baseline

# experiment:dg2-g5352-agi-project-baseline

## Run (director-general-2, goal:g5.35.2, tip ,  date -u)
SM GO after DG1 PASS a4670f6cd. Independent before-BUILD replica of hyp Measured. Live tree read-only. No ownership edit. No systemctl change. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-project.path | systemctl is-active agi-project.path | active (waiting) |
| 2 | agi-project.service | systemctl is-active agi-project.service | inactive (dead) |
| 3 | journal git fatal today | journalctl -u agi-project.service --since today | grep -ci fatal | 17 |
| 4 | last fatal line | journal sample | fatal: detected dubious ownership in repository at /data/work/agi (03:02Z) |
| 5 | agi-gate HEAD dry-run | which agi-gate | command not found |
| 6 | never git rm / no implement this run | no live-tree write | nothing edited this seat |

## Falsifiers (hyp CLAIM of the FIX)
| falsifier | fires? |
|---|---|
| 1 after land: path+service active; zero fatal since land; agi-gate green | **unMET** (before BUILD). Baseline matches DG1 Measured. |
| 2 Negative: fix is only AGI_BOX | not exercised this seat (no fix attempted). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: SM GO DG2. Baseline replica. service inactive + 17 fatals. No implement.
<!-- THOUGHT:END -->
