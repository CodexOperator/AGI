---
id: verdict:dg2-s1-dm-family
mint_id: 55498f0ea4ac46cd9641b250706ae059
type: verdict
parents:
  - experiment:dg2-s1-dm-family-measure
  - hypothesis:dm-family-can-replace-the-inbox-route-measured
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-s1-dm-family-measure
scaffold_hash: 77fa467eed66d622
season: 2
title: "S1: proved -- VERDICT, not FOLD: routes are 3 today and 3 after a fold (core's family only plans); inbox refs 210 -> 238 on core; nothing ported"
town: core
verdict: proved
---
# verdict:dg2-s1-dm-family

## Verdict: proved (director-general-2, council bundle 3 stage 2) -- the measurement settles S1: VERDICT, not FOLD

| conjunct | on the trunk (experiment:dg2-s1-dm-family-measure) | decided by |
|---|---|---|
| (1a) routes BEFORE, from committed bytes | 3: R1 inbox file (`send TARGET`, sessions/inbox/<to>.md), R2 comms dm/room file (`send --to/--room`), R3 CC SendMessage (interim, harness) -- TRUE, measured | trunk send.py :3188 / :4271 / :4321 / :5541 |
| (1b) routes AFTER a fold of the family into one module / send.py | 3 delivering routes + 1 plan-only verb set: core's family plans and gates, never delivers ("does not yet push a grid version or retire sessions/inbox", core dm_engine.py:10-12); its `pane` seam delivers through R1. Routes do NOT go 2 -> 1 (nor 3 -> 2) -- measured | core dm_engine.py, core send.py :5595-5690 |
| (1c) inbox refs drop to a retirement pointer within ONE row | FALSE: trunk 210 lines / 8 files in bin (send.py 152, rotate.py 35) + 685 lines / 29 test files; core WITH the family carries 238 / 13 (+28). The delivery that would replace R1 (write.py push, g4.18.1 active) exists on neither ref | `git grep -n inbox <ref> -- extensions/agi/bin` |
| (2) g7.32.6 targets the trunk lacks | 6 of 6 design lines lack (post-branch send via write.py, remote_head address, per-box sync cron, sync-only nudge, read-flag push, no inbox); trunk g7.32.6 active with 0 children, core .1-.9 complete as plans | experiment rows 9-10 |
| rule: FOLD only if routes 2 -> 1 in the same row | FOLD condition fails on both halves -> **VERDICT**; nothing ported; FOLD's dm-format test is NOT owed to g7.16.1.3.3.2 | this table |

Why: the fold would import 742 module + 594 test lines that ADD a plan route and keep the inbox; retirement waits on goal:g4.18.1's mint route (owner order 01:0xZ 09-27: g4.18.1 first, then g7.32.6). CORRECTIONS to the hypothesis's Measured: (a) routes today are 3, not 2 -- the `send --to/--room` comms-file route (R2) is a live route distinct from the inbox file; (b) "8 modules" holds, but send_transport is a rotation adapter (lazy `rotate` shims), not a dm module, and has no test file -- so 7 dm modules + send_transport + magic_pane; (c) the 210 inbox-line count is exact (8 files); core's is 238 (13 files); (d) core marks g7.32.6.1-.9 complete while its own façade states inbox retirement and the push are not done -- core's "complete" is plan-complete, not route-complete.
