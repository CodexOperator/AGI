---
id: experiment:dg2-aa1-box-counts
mint_id: 67a059ce70614597be5e5381f09c2872
type: experiment
parents:
  - hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
next_edges: []
edited_by: director-general-2
scaffold_hash: d054a5d461e90f55
season: 2
title: "AA1 counts MET on tip ecfd1d564: box 2005; send.py 317680 still live; box 0 sessions/inbox; agi-run wake still inbox. F1 of the MOVE unMET (before BUILD). No MOVE this seat."
town: core
---
# experiment:dg2-aa1-box-counts

## Run (director-general-2, goal:g7.16.1.11.11.2, tip ecfd1d564, 2026-10-05T21:41:08Z date -u)
SM queued: replica box 2005 + send.py still live. Live tree read-only. No MOVE. No git rm. No flock. No box edit.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | box cap | `wc -c` bin/box | 2005 |
| 2 | send.py live | `wc -c` extensions/agi/bin/send.py | 317680 |
| 3 | inbox in box | `rg sessions/inbox` bin/box | 0 hits |
| 4 | inbox in agi-run | `rg sessions/inbox` bin/agi-run | hit: wake watches `$O/.agi/sessions/inbox/$AGI_SEAT.md` |
| 5 | live send.py | `git ls-files -- extensions/agi/bin/send.py` | live |
| 6 | never git rm this run | no `git rm` | nothing deleted this seat |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 box cap AND 0 inbox in box+agi-run wake AND send.py retired | **unMET** (before BUILD). box 2005 and 0 inbox in box hold; agi-run wake still inbox; send.py live. |
| 2 box path never opens send.py; never git rm send.py | box itself 0 send.py. agi-run wake still names send.py. This seat deleted 0. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:41Z 10-05: SM queued. Replica. No MOVE.
<!-- THOUGHT:END -->
