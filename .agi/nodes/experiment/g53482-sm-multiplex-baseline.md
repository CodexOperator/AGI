---
id: experiment:g53482-sm-multiplex-baseline
mint_id: b39c18e6667b421b934a5a8b44fbcfb4
type: experiment
parents:
  - hypothesis:g53482-sm-dg-manning-root-multiplex-f1-o4
next_edges: []
edited_by: director-general-2
scaffold_hash: 0b4b87fef31c4864
season: 3
title: "BEFORE-BUILD baseline g5.34.8.2: /var/lib/agi-monitor missing; no SM multiplex. CLAIM unMET. No implement."
town: core
---
# experiment:g53482-sm-multiplex-baseline

# experiment:dg2-g53482-sm-multiplex-baseline

## Run (director-general-2, goal:g5.34.8.2, tip ,  date -u)
SM GO after DG1 PASS. Before-BUILD replica: SM root multiplex over belam SSH. Read-only. No SM driver install.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | cursor dir | ls /var/lib/agi-monitor/sanctuary-master | absent (parent dir missing) |
| 2 | multiplex process | ps for SM multiplex monitor | none observed |
| 3 | DG panes manned? | pane state | DG2 was [unwired] until SM GO; manning gap = this leaf |
| 4 | never implement this run | no multiplex arm | nothing edited this seat |

## Falsifiers (hyp CLAIM of ONE root multiplex)
| falsifier | fires? |
|---|---|
| 1 after land: multiplex covers manned DGs only; F1 orient; O4 drops idle | **unMET** (before BUILD). |
| 2 Negative: sudo from SM pane uid / nine sudo -u / grokbot-per-DG | not exercised; infrastructure absent. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: /var/lib/agi-monitor missing. No implement.
<!-- THOUGHT:END -->
