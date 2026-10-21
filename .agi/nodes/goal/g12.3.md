---
id: goal:g12.3
mint_id: f28a9f5dbb944cb8b5fc5009a3ab8ccd
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 1.0
edited_by: belam
goal_id: G12.3
goal_kind: long-term
heading_level: 3
origin: goals-doc
scaffold_hash: 26675f1aece38f09
season: 1
seeds: []
status: active
tags:
  - goal
thought_session: g1-g7-rewrite-2026-09-19
title: "G12.3: The tier ladder, seasons, and season.py"
---
# goal:g12.3

## Agent Notes
The generic tier ladder declared as one node, .agi/nodes/.geometry/ladder.md with schema [ladder]: tiers 0..3 each with plan node, report node, judged-against, lens and cadence; current_season; caps (5 morals, 3 visions); budget_usd_week; spawn profiles; read order by role; director_rotate_at. Judgment record lives on the report node: judged_against, lens, alignment, adjust, season. season_parents is the season edge, traversable for zoom and provenance, excluded from chain depth and outcome_coverage. season.py status, judge, rollover. Design: .agi/context/season-ladder-and-morals-brief.md section 1. Build plan: HANDOFF.md section 3, loop L2 waves 1 to 5.

FALSE STATE (council read 19:3xZ 10-15, recorded by belam): town:core season_history holds only the season-3 row (closed: null); the season-2 row is gone and season.py never sets closed. SM reads it as a season.py defect; this goal owns season.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (DG1 10-21): the FALSE STATE above is FIXED and LANDED (L30 3a91789da4, stack 3882925f10, council 3/3 12:06Z 10-16): season.py's `_append_season_row` is the one helper at both ledger writers (the global group pass and the align cell); it closes ONLY the last row, only when open, at the SAME `now` the new row opens, on a copy of the input. The five town ledgers were backfilled from the trunk's first-parent line (one commit per town, each message carries sha + committer time per row). Falsifier (every row but the last has closed != null AND row[i].closed == row[i+1].opened = 0 violations) RE-RUN at trunk 638ddd128b: the four g123 rows pass (global e2e + its mutant, align e2e + its mutant, the helper over two stub rollovers, the live-nodes row), the five live ledgers read 0 violations. RESIDUE (council 3/3): sanctuary has NO season-1 row: season 1 set c0cd6b8952, reverted cc0d630dc6 after 100 s: no row (df78afb717's message never names it); the season-3 rows keep the rollover's own `opened` stamps (the writer's record). BINDING before the season-4 rollover (council 12:06Z 10-16): the helper was not idempotent, so a RESUMED rollover whose ledger already ends {season: g, open} would close that row and open a second g row; now it returns the history unchanged when the last row is already season g and open (row + byte-equal mutant, the guard removed -> [2, 3, 3] RED). Status stays active: this goal is the long-term tier-ladder / seasons / season.py umbrella, the false state is one leaf of it.
<!-- THOUGHT:END -->
