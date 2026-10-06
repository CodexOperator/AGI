---
id: experiment:g53462-mail-wake-baseline
mint_id: 8d8425047fb04c7bbc8e64d71137b0c7
type: experiment
parents:
  - hypothesis:g53462-mail-wake-agi-carry-pathchanged-w1-w7
next_edges: []
edited_by: director-general-2
scaffold_hash: f4a5870ee4636aa4
season: 3
title: "BEFORE-BUILD baseline g5.34.6.2: 0 agi-carry@ units; agi-wake missing; mail-wake watch sleep-loop SoT; [unwired]. CLAIM of PathChanged arm unMET. No implement."
town: core
---
# experiment:g53462-mail-wake-baseline

# experiment:dg2-g53462-mail-wake-baseline

## Run (director-general-2, goal:g5.34.6.2, tip ,  date -u)
SM GO after DG1 PASS. Before-BUILD replica of hyp Measured for mail-wake via agi-carry PathChanged. Read-only. No project. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-carry@ units | systemctl list-units --all agi-carry@* | 0 loaded |
| 2 | agi-carry unit files | ls /etc/systemd/system/agi-carry* | absent |
| 3 | mail-wake bin | ls ~/bin/mail-wake | present (local projected; sleep-loop SoT) |
| 4 | agi-wake | which agi-wake | missing (W1 gap; [unwired] on pane) |
| 5 | ### mail-wake in extensions | git grep ### mail-wake -- extensions | 0 hits this tip |
| 6 | live watchers | ps mail-wake watch | DG1-3,5-7 + PM + TM running mail-wake watch |
| 7 | never implement this run | no agi-carry project | nothing edited this seat |

## Falsifiers (hyp CLAIM of PathChanged arm)
| falsifier | fires? |
|---|---|
| 1 after reproject: notice+y box read; W1 wake; <5s | **unMET** (before BUILD). |
| 2 0 B to i; Enter=HOLD; one notice/tip-sha; grep -c exec bash -i == 1 | baseline not claiming post-land. |
| 3 Negative: new watcher / AGI_BOX-only / sleep-loop SoT land | sleep-loop still SoT today (matches Measured). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: no agi-carry@; agi-wake missing; mail-wake watch still sleep-loop. No implement.
<!-- THOUGHT:END -->
