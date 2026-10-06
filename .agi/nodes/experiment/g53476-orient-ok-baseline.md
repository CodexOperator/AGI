---
id: experiment:g53476-orient-ok-baseline
mint_id: 342d1aa98c46489cb138e817dd5aadde
type: experiment
parents:
  - hypothesis:g53476-orient-captive-ok-gate-exact-ok
next_edges: []
edited_by: director-general-2
scaffold_hash: 3e594ed335eaff21
season: 3
title: "BEFORE-BUILD baseline g5.34.7.6: orient dumps+exits; no exact-ok gate. CLAIM unMET. No implement."
town: core
---
# experiment:g53476-orient-ok-baseline

# experiment:dg2-g53476-orient-ok-baseline

## Run (director-general-2, goal:g5.34.7.6, tip ,  date -u)
SM GO after DG1 PASS. Before-BUILD replica: orient captive exact-ok gate. Read-only. No orient edit.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | orient source | cat ~/bin/orient (7 lines) | dumps via agi-sync; prints end-startup; exits — no ok-gate |
| 2 | exact-ok gate in orient | grep exact ok / read ok in ~/bin/orient | 0 hits |
| 3 | ### orient captive ok in extensions | git grep -i orient captive ok | 0 hits |
| 4 | never implement this run | no orient edit | nothing edited this seat |

## Falsifiers (hyp CLAIM of ok-gate)
| falsifier | fires? |
|---|---|
| 1 after land: prompt after end-startup; non-ok blocked; exact ok continues | **unMET** (before BUILD). |
| 2 Negative: orient still exits without ok-gate | **TRUE today** (matches Measured). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: orient dumps+exits; no ok-gate. No implement.
<!-- THOUGHT:END -->
