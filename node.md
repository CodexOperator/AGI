---
id: doc:rse-z4-ladder-out
mint_id: a593eb3819ab45fdba6cbbebf21f53ab
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: director
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: "Z4 ladder out: retire ladder:ladder in favor of the post tree, without stranding a reader (council design, all-is-one lead)"
town: core
---
# doc:rse-z4-ladder-out

Owner 03:1xZ 10-02 (belam [decision] 04:43Z): "we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."
Council split (04:4xZ 10-02): all-is-one LEADS (cells, order, this doc) · AA2 self-perpetuating = what the tree replaces ("LADDER OUT" in doc:radically-simple-engine) · AA1 alive = TRUE STATE + the retire gate (AA1.L in doc:rse-aa1-boxes). Builds on Z3 (doc:radically-simple-engine §Z3, 18:1xZ 10-01).

## Z4.1 TRUE STATE (trunk 3928fed44, 04:4xZ 10-02)
```
v5 ENGINE      reads 0 ladder bytes (git grep ladder -- .geometry/engine*.md = 0 hits). Every ladder reader is OLD-SETUP Python.
READERS        16 files by AST (alive AA1.L): rotate 21 · spawn_gate 10 · hierarchy 6 · dispatch 5 · cli 4 · seat_status 3 · towns 3 · heal 2 ·
               workflow 2 · countersign 2 · brief, rolslice, season, send, verification, hooks/rotation_alert 1 each
WRITER         season.py writes ladder:ladder at rollover (:1061) · templates/harness/claude-code.toml declares source = "ladder"
LIVE DEPENDENCY dispatch.py resolve_role_spec: emptying the ladder silently drifts 5 of 8 (tier, role) specs to the pi-free fallback,
               including belam's tier-3 Sonnet kid spawner (alive, measured) => the ladder's CONTENTS may not move before its readers do
               + workflow.py (alive, measured): a third role-row spawner beside dispatch + heal, serving posts on BOTH setups; without the
               ladder its director stages drift claude-fable-5-1 -> stealth/space-bunny-alpha (its own _resolve_pi_model)
GRAPH EDGE     [town] allowed_parents: [ladder] · growth.tsv rows `ladder - goal` + `town - ladder` · 5 town:* nodes parent ladder:ladder
```

## Z4.2 The plan: three phases, each strands nothing
```
A  NOW, graph only (no reader touched, ladder.md untouched)                                   Option A: anchor-signed schema edit
   A1 [town] spawn: allowed_parents [goal, vision] · parent_shapes [[goal, vision]] · min 2 · max 2
   A2 [ladder].md out of the projector's glob (status deprecated, moved) -> grow-project: growth.tsv 149 -> 148 rows
   A3 the 5 towns drop `ladder:ladder` from parents (they keep vision:the-living-being + goal:g26.towns)
   A4 v5 replacements land beside it (AA2): tier = depth from parent cells (never stored; the stale `tier` cell retires from v4 rows)
      · the roles table = ONE inherited engine.kid cell (kid-of, nearest ancestor-or-self) · read_order = the rows' seeds · caps.director_kids = kid.max
      A4's WRITER = belam: WRITTEN e56869124 (05:0xZ 10-02) `"kid": {"harness":"claude-code","model":"claude-sonnet-5-5","max":3}` on
      belam's row; kid-of covers the whole tree. A4 lands BEFORE B2 (workflow.py's move reads it).
B  FREEZE + MOVE (old setup still running)
   B1 ladder.md FROZEN: no new cell. ONE exception until its readers move: the rollover DUAL-WRITES the global season (ladder
      current_season AND town:core's `season`), because 11 reader sites in 6 files still read the ladder's (alive): spawn_gate :742 :1414 ·
      dispatch :1457 :2349 · send :1153 · rotate :275 :885 :21902 :22240 · seat_status :191 · towns :285. Dual-write ends when they read 0.
   B2 each reader in a tool a v4 post still RUNS reads the tree/row instead, one file per round, FIRST the three spawners
      (workflow.py serves both setups, then dispatch.py, heal.py), then send, brief, verification, ...;
      G4 = parity EXCEPT ONE named change: workflow.py's director stages move claude-fable-5-1 -> claude-sonnet-5-5 (AA2.25; owner
      02:27Z 10-01 "Everyone else on sonnet 5.5 for everything they need"), CONFIRMED by belam 05:07Z; every other spec stays equal
      parity (alive's G4) proven per file before the next
   B3 readers in tools only old-setup posts run stay on the ladder until that post moves
C  RETIRE when the LAST old-setup post (belam, last) is on v5 AND alive's gate reads 0/equal:
      G1 AST readers = 0 · G2 writers = 0 · G3 source = "ladder" = 0 · G4 spec parity for every (tier, role) + every row a spawner reads
   -> ladder.md status deprecated + moved to deprecated/ladder/ (retire, never delete)
```
NOT BUILT, deliberately: Z3's `cells.tsv` + `cell.py` resolver (1,156 B). A resolver for the old Python readers is bytes spent on code that retires with the old setup; the v5 engine needs none of the ladder's cells (owner 23:0xZ: "you are over engineering it again"). If phase B finds a reader that must outlive the old setup and cannot read a row, the resolver comes back for that one reader.

## Z4.3 Where each ladder cell goes (Z3's map, re-cut for v5)
| ladder cell | v5 home | already there? |
|---|---|---|
| roles · tiers · mantles · captive_rotate_masters | parent cells (depth) + engine.kid (AA2) | parent cells yes (f3a7eb1da, 1efd017e6); engine.kid NO (AGI_KID_MODEL empty on all 12 v4 rows) |
| director_rotate_at · director_context_tokens | each row's engine.rotate_pct (47) + the meter's window | rotate_pct yes |
| current_season (GLOBAL) | town:core's `season` (core = the root town, "every vision no other town claims") | yes: core 2 == ladder 2 today; the other towns keep their OWN counters (local-maxxing 1, streaming-suite 1, web-app-suite 1, sanctuary 2), so the global needs ONE named home and towns.py's global-vs-town compare reads core |
| season_names · caps_apply_from_season | the town node's season cells | yes |
| current_loop | none on v5 (the loop counter is the old driver's) | retires |
| towns · town_branches | each row's `town` cell + the town nodes | yes |
| caps (moral 5, vision 3, director_kids 3) · caps_vision_scope | director_kids -> kid.max (AA2; belam's kid cell max 3); moral/vision count caps RETIRED | owner 03:4xZ 10-02 chose "Retire the caps (Recommended)" (belam 05:07Z): a count cap limits the graph, not the engine; no v5 piece enforced one |
| read_order | the rows' seeds | yes |
| captive_rotate_ratio · capture_chain_log · card_capture_minutes · alarms_idle_minutes | config:rotations (old setup) | retire with the old setup |
| budget_usd_week · spawn_profiles · zoom | none (0 readers, Z3) | dead |

## Z4.4 Measured (scratch, trunk 3928fed44, 04:4xZ; schemas + nodes via git archive, 0 live bytes touched)
| # | case | result |
|---|---|---|
| L1 | grow-project over TODAY's schemas vs the live growth.tsv | byte-identical (149 shape rows) |
| L2 | grow-project after A1 + A2 | 149 -> 148; exactly 3 rows differ: - `43644068064c42f1 ladder - goal` - `0bdfa51c9e997b40 town - ladder` + `00b8ef0c7c6395ec town - goal+vision`; 147 nids unchanged (same new key as Z3 at 18:1xZ) |
| L3 | the 5 towns as they stand, today's matrix | refused: wrong order (town under goal+ladder+vision) |
| L4 | the 5 towns after A3, new matrix | legal order; only `locked: key none` (no live node carries a key yet) |
| L5 | grow-check over EVERY live node, old matrix vs new | 5,494 nodes, 0 verdicts move |
Bytes: phase A = 3 schema lines + 1 matrix row fewer + 5 parent lines out; A4 per AA2 (tier 77 B, kid-of ~327 B, in agi-kid ~+360 B, never in agi-project). 0 B in the zygote. Removed at C: ladder.md 10,670 B + [ladder].md.

## Z4.5 Falsifiers (for DG1)
Z4.a after A on the trunk: grow-check parity moves 0 verdicts except the 5 towns (L5 on the landed bytes).
Z4.b after A: dispatch.py resolve_role_spec for all 8 (tier, role) AND workflow.py's director-stage model == before (phase A touches no spec). After B2: equal except the ONE named AA2.25 change.
Z4.c B1: after a rollover, EVERY season reader (the 11 sites) returns the new season, read from town:core once moved; when they read 0 from the ladder, the dual-write stops and G2 = 0.
Z4.d C: G1-G4 all 0/equal on the trunk the same day ladder.md moves; `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0.
RULED (belam [decision] 05:07Z 10-02): (1) the moral/vision count caps RETIRE (owner 03:4xZ) · (2) the AA2.25 G4 exception CONFIRMED · (3) belam's `kid` cell WRITTEN e56869124. "Phase A may start via DG1."
Reviews folded (04:5xZ): self-perpetuating (G4 exception, A4 writer, caps -> retire) · alive (B1 season split -> dual-write + 11 readers, the GLOBAL season's home = town:core, G4 exception; CLEARED: A2 before B1 is safe, write.py's set gate returns no refusal without a schema).

## Z4.6 RE-CUT on the owner's 14:0xZ 10-02 line (belam [owner] 14:01Z): phases B and C SUPERSEDED as written above
OWNER, verbatim: "we don't need to fix the ladder.py readers ... we're not gonna have any of those readers ... we don't have a workflow anymore. Remember, everything got smushed and coalesced into just spawns ... we just need to retire workflow.py entirely and stop wasting time on it." (record: goal:g5.33 owner 09-28 + goal:g4.6 one spawn path: spawn = dispatch = workflow = subagent)
MEASURED 14:0xZ, every post's ~/track (agi-track: each opened path once per unit run; a v5-native record of what a post actually RUNS):
| post | ladder.md lines | workflow.py lines |
|---|---|---|
| director-general-5 (pi) | 425 | 4 |
| thought-master-new | 6 | 1 |
| director-thought-1 · -2 | 4 · 4 | 2 · 1 |
| director-general-4 | 2 | 0 |
| self-perpetuating | 1 | 0 |
| alive · all-is-one · DG1 · DG2 · DG3 · stream-master | 0 | 0 |
So v5 posts DO still reach the ladder, through old-setup Python tools they call, and the thought side (DG5, TM-new, DT-1, DT-2) still runs workflow.py.
```
A   UNCHANGED (graph only; DG1's round is in flight): [town] -> [goal, vision] · [ladder].md out · 149 -> 148 · 5 towns drop ladder:ladder
B'  FREEZE ONLY. No ladder reader moves (owner). ladder.md takes no new cell. The season dual-write and the AA2.25 parity exception
    are DROPPED: they existed only to move readers. town:core stays the named home of the global season, for whenever a v5 piece
    needs one (none does today).
W   workflow.py RETIRES ENTIRELY, now (owner), as ONE round:
    users today (track): DG5, TM-new, DT-1, DT-2 -> their review/research runs become plain spawns (agi-kid / the engine.kid cell)
    retire (status deprecated + moved, never deleted): extensions/agi/bin/workflow.py · the 30 manifests in extensions/agi/workflows/
      · skill agi-workflow · config:workflows · hooks/workflow_note.py
    drop the reference: skills agi, agi-corrective, agi-master-gate, agi-merge-pass · config:commands
    old-setup callers (dispatch, heal, adapters, glitch_master) keep their dead branch until they retire with the old setup
C'  ladder.md (+ the 16 old-setup readers, + season.py's write) retire WITH the old-setup Python, never moved.
    GATE = by USE, not by AST (code nobody runs strands nobody): every live post's ~/track gains 0 ladder.md lines over 24 h
    (snapshot the counts above, compare a day later) AND the last old-setup post (belam, last) is on v5.
```
Falsifiers: Z4.e after W, 0 posts' tracks gain a workflow.py line over 24 h, and DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn · Z4.f C' as gated above; at the move, `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0.
Limit: ~/track counts ANY open, including a design read like this one (self-perpetuating's 1 line), so the 24 h window starts after this round.
