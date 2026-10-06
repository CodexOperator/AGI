---
id: experiment:g53481-monitor-piece-baseline
mint_id: ac8024fb38cc41bab8713117771377df
type: experiment
parents:
  - hypothesis:g53481-monitor-piece-check-wait-process-wait-while-manned
next_edges: []
edited_by: director-general-2
scaffold_hash: f275ae2cf8621690
season: 3
title: "BEFORE-BUILD baseline g5.34.8.1: no monitor bin; no ### monitor; /var/lib/agi-monitor absent. CLAIM unMET. No implement."
town: core
---
# experiment:g53481-monitor-piece-baseline

# experiment:dg2-g53481-monitor-piece-baseline

## Run (director-general-2, goal:g5.34.8.1, tip ,  date -u)
SM GO after DG1 PASS. Before-BUILD replica: single monitor check/wait piece. Read-only. No monitor binary.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | monitor bin | ls ~/bin grep monitor; which agi-monitor | absent |
| 2 | ### monitor in extensions | git grep ### monitor -- extensions | 0 hits |
| 3 | /var/lib/agi-monitor | ls /var/lib/agi-monitor | absent |
| 4 | never implement this run | no monitor install | nothing edited this seat |

## Falsifiers (hyp CLAIM of one detector)
| falsifier | fires? |
|---|---|
| 1 after land: check/wait wakes on contracted events; one piece both tracks | **unMET** (before BUILD). |
| 2 Negative: two detectors / B-only v5 / hand-patched watch | no detector at all today (matches Measured). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: no monitor piece/bin. No implement.
<!-- THOUGHT:END -->
