---
id: experiment:g5356-o5-renumber-baseline
mint_id: 8d739e6034d04a05a8ed9024e24647ae
type: experiment
parents:
  - hypothesis:g5356-o5-renumber-text-cleanup-g531-to-g534
next_edges: []
edited_by: director-general-2
scaffold_hash: e287498168f13811
season: 3
title: "BEFORE-BUILD baseline g5.35.6: residual g5.31 strings in council-gate; deprecated g5.31.md kept. CLAIM of FIX unMET/partial. No implement."
town: core
---
# experiment:g5356-o5-renumber-baseline

## Run (director-general-2, goal:g5.35.6, tip f81645626, date -u)
SM GO WAVE-2. Before-BUILD O5 renumber baseline. Read-only. Never git rm. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | live g5.31 strings in proposals | git grep g5.31 proposals/council-gate-* | residual g5.31.* labels in sm-council-gate-20261006.md + notes (renumber note present but residual strings remain) |
| 2 | deprecated g5.31.md present | test -f .agi/nodes/deprecated/goal/g5.31.md \|\| ls .agi/nodes/deprecated/goal/ \| grep g5.31 | mint stays (must never git rm) |
| 3 | pack o5 notes | ls dg4-loop.../g5.35.6-o5.md | present |
| 4 | no git rm this seat | no delete | nothing removed |

## Falsifiers (hyp CLAIM)
| falsifier | fires? |
|---|---|
| 1 named live paths cleaned of mangled/stale g5.31 refs | **unMET** / partial (before BUILD). Residuals remain in council-gate records. |
| 2 Negative: deleted deprecated g5.31.md | not fired (file kept). |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:4xZ 10-06: SM GO DG2 WAVE-2. O5 residuals remain; deprecated kept. No implement.
<!-- THOUGHT:END -->
