---
id: goal:g7.16.1.11.15
mint_id: 8f428977554c467fb8e5c553f7fa87d1
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.15
goal_kind: subgoal
origin: goal
scaffold_hash: 6384294839bf7c3f
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - design
  - g7.16.1.11
  - z4
  - ladder
title: "G7.16.1.11.15: Z4 ladder out -- the ladder is phased out in three phases (graph only; freeze + move each reader; retire at the last old-setup move) with every (tier, role) spec unchanged until a reader moves"
town: core
---
# goal:g7.16.1.11.15

## Why this exists
goal:g7.16.1.11: the council's Z4 section (doc:rse-z4-ladder-out, on the trunk at 05a5c9a6b (the REVIEWED version; an earlier draft was posts/all-is-one 1a8a5eff0); all-is-one LEADS, AA2 self-perpetuating = what the tree replaces, AA1 alive = TRUE STATE + the retire gate AA1.L; reviewed by alive + self-perpetuating) answers the owner's line on phasing the ladder out. Measured (trunk 3928fed44): the v5 engine reads 0 ladder bytes; every ladder reader is OLD-SETUP Python (16 files by AST: rotate 21 · spawn_gate 10 · hierarchy 6 · dispatch 5 · cli 4 · seat_status 3 · towns 3 · heal 2 · workflow 2 · countersign 2 · brief, rolslice, season, send, verification, hooks/rotation_alert 1 each); season.py WRITES ladder:ladder at rollover (:1061); claude-code.toml declares source = 'ladder'; and dispatch.py resolve_role_spec drifts 5 of 8 (tier, role) specs to the pi-free fallback if the ladder is emptied (belam's tier-3 Sonnet kid spawner included), plus workflow.py (a third role-row spawner serving posts on BOTH setups: its director stages drift claude-fable-5-1 -> stealth/space-bunny-alpha). So the ladder's CONTENTS may not move before its readers do.

## OWNER 2026-10-02 03:1xZ, verbatim
"we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."


## Target end-state
- PHASE A (NOW, graph only; no reader touched; ladder.md untouched; Option A = an anchor-signed schema edit): [town] spawn allowed_parents [goal, vision] · parent_shapes [[goal, vision]] · min 2 · max 2; [ladder].md out of the projector's glob (status deprecated, moved) so growth.tsv 149 -> 148 rows; the 5 town nodes drop `ladder:ladder` from parents (they keep vision:the-living-being + goal:g26.towns); AA2's v5 replacements land beside it (depth tier, ONE inherited engine.kid cell, read_order = the rows' seeds, caps.director_kids = kid.max).
- PHASE B (freeze + move; the old setup keeps running): ladder.md FROZEN (no new cell); season.py's rollover DUAL-WRITES the GLOBAL season -- the ladder's current_season AND town:core's `season` (core = the root town: core 2 == ladder 2 today, while local-maxxing, streaming-suite and web-app-suite carry their OWN counters of 1 and sanctuary 2, so a per-town season cannot replace the global; the global needs ONE named home, town:core, and towns.py's global-vs-town compare reads core) -- until the 11 season reader sites in 6 files read town:core (spawn_gate :742 :1414 · dispatch :1457 :2349 · send :1153 · rotate :275 :885 :21902 :22240 · seat_status :191 · towns :285); each reader in a tool a v4 post still RUNS moves to the tree/row, ONE FILE PER ROUND, FIRST the three spawners (workflow.py, then dispatch.py, heal.py), then send, brief, verification; parity (alive's G4) proven per file before the next; readers in tools only old-setup posts run stay on the ladder until that post moves.
- PHASE C (retire at the LAST old-setup move, belam last, when alive's gate reads 0 / equal): G1 AST readers = 0 · G2 writers = 0 · G3 source = 'ladder' = 0 · G4 spec parity for every (tier, role) + every row a spawner reads; then ladder.md status deprecated + moved to deprecated/ladder/ (retire, never delete).
- Deliberately NOT built: Z3's cells.tsv + cell.py resolver (1,156 B): a resolver for the old Python readers is bytes spent on code that retires with the old setup (owner 23:0xZ: 'you are over engineering it again'); it comes back only for a reader that must outlive the old setup and cannot read a row.

## Invariants
- Each phase strands nothing: no reader loses a cell it reads before it moves; G4 parity per file; ONE named exception: workflow.py's director stages move claude-fable-5-1 -> Sonnet 5.5 by the owner's 'every subagent Sonnet 5.5' (AA2.25), a deliberate change, CONFIRMED by belam 05:07Z.
- Nothing is deleted: ladder.md and [ladder].md are retired and moved, never `git rm`.
- 0 B in the zygote; the base stays <= 8,192 B (kid-of runs inside agi-kid, never in agi-project).
- THE THREE OWNER ITEMS ARE RULED: belam 05:07Z 10-02 RULED all three: (1) the moral/vision COUNT caps RETIRE (owner 03:4xZ); (2) the AA2.25 exception is CONFIRMED; (3) belam's `kid` cell is WRITTEN (e56869124 = {harness: claude-code, model: claude-sonnet-5-5, max: 3}), so A4's writer is done; belam: 'Phase A may start via DG1' (it still needs belam's anchor signature on the [town] schema edit). Nothing in this goal stays HELD on them; phase A is the one startable round.

## Falsifier
1. Z4.a after A on the trunk: grow-check parity moves 0 verdicts except the 5 towns (L5 on the landed bytes: 5,494 nodes, 0 verdicts move on scratch) · Z4.b after A: dispatch.py resolve_role_spec for all 8 (tier, role) AND workflow.py's director-stage model == before (A touches no spec) · Z4.c B1: a season rollover writes 0 bytes to ladder.md (G2 = 0) and the town's season cell moves · Z4.d C: G1-G4 all 0/equal on the trunk the same day ladder.md moves.
2. Negative: `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0 hits throughout.

## Out of scope
goal:g7.16.1.11.12 (the AA2 side: depth, kid-of, the kid cell: its hypotheses are shared parents) · the moral/vision COUNT caps (RETIRE: ruled by belam 05:07Z, owner 03:4xZ; no matrix count column) · the old setup's own move to v5 (belam, SM, DG3, old TM).

## Agent Notes
Assigned to **director-general-1**.
