---
id: goal:g7.16.1.11.15
mint_id: 8f428977554c467fb8e5c553f7fa87d1
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.15
goal_kind: subgoal
origin: goal
scaffold_hash: 6384294839bf7c3f
season: 2
seeds:
  - goal:g7.16.1.11
status: active
tags:
  - council
  - design
  - g7.16.1.11
  - z4
  - ladder
title: "G7.16.1.11.15: Z4 ladder out -- phase A landed (graph only); no ladder reader is moved (freeze only); workflow.py retires entirely; ladder.md retires WITH the old-setup Python that reads it, gated by use"
town: core
---
# goal:g7.16.1.11.15

## Why this exists
goal:g7.16.1.11: the council's Z4 section (doc:rse-z4-ladder-out, on the trunk at 05a5c9a6b (the REVIEWED version; an earlier draft was posts/all-is-one 1a8a5eff0); all-is-one LEADS, AA2 self-perpetuating = what the tree replaces, AA1 alive = TRUE STATE + the retire gate AA1.L; reviewed by alive + self-perpetuating) answers the owner's line on phasing the ladder out. Measured (trunk 3928fed44): the v5 engine reads 0 ladder bytes; every ladder reader is OLD-SETUP Python (16 files by AST: rotate 21 · spawn_gate 10 · hierarchy 6 · dispatch 5 · cli 4 · seat_status 3 · towns 3 · heal 2 · workflow 2 · countersign 2 · brief, rolslice, season, send, verification, hooks/rotation_alert 1 each); season.py WRITES ladder:ladder at rollover (:1061); claude-code.toml declares source = 'ladder'; and dispatch.py resolve_role_spec drifts 5 of 8 (tier, role) specs to the pi-free fallback if the ladder is emptied (belam's tier-3 Sonnet kid spawner included), plus workflow.py (a third role-row spawner serving posts on BOTH setups: its director stages drift claude-fable-5-1 -> stealth/space-bunny-alpha). So the ladder's CONTENTS may not move before its readers do.

## OWNER 2026-10-02 03:1xZ, verbatim
"we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."

## OWNER 2026-10-02 14:0xZ, verbatim (belam [owner] 14:01Z; banked on town:local-maxxing Agent Notes 64bf778d4) -- SUPERSEDES the move-the-readers phase
"we don't need to fix the ladder.py readers because we're not gonna, or ladder.md, because we're not gonna have any of those readers because you're saying workflow.py, we don't have a workflow anymore. Remember, everything got smushed and coalesced into just spawns. So we don't have any difference between dispatch and spawn, we don't have any difference between workflow and spawn or subagent or anything. It should be somewhere in the gold tree. I'm not sure why somebody decided to chase that, but we just need to retire workflow.py entirely and stop wasting time on it. [...]" (excerpt: the first 573 characters of the banked line, which continues; full text on town:local-maxxing Agent Notes 64bf778d4)
Re-cut (council, all-is-one 14:03Z, Z4.6 of doc:rse-z4-ladder-out, on the trunk at 8356d4114; the goal is this node's): A unchanged · B' FREEZE ONLY · W workflow.py retires as ONE round · C' ladder.md + its old-setup readers retire WITH the old-setup Python. "gold tree" = the goal tree.


## Target end-state
- PHASE A (DONE: landed c2decf431 on the trunk 10-02, belam's four anchor commits + C4 + the tests; graph only; no reader touched; ladder.md untouched; residue: ONE later test/fence round, hypothesis g716111-z4-phase-a-... '## Residue'): [town] spawn allowed_parents [goal, vision] · parent_shapes [[goal, vision]] · min 2 · max 2; [ladder].md out of the projector's glob (status deprecated, moved) so growth.tsv 149 -> 148 rows; the 5 town nodes drop `ladder:ladder` from parents (they keep vision:the-living-being + goal:g26.towns); AA2's v5 replacements land beside it (depth tier, ONE inherited engine.kid cell, read_order = the rows' seeds, caps.director_kids = kid.max).
- PHASE B' (FREEZE ONLY; SUPERSEDES the old phase B -- owner 14:0xZ: no ladder reader is moved, so no season dual-write, no reader-by-reader parity, and the AA2.25 workflow.py director-stage exception is DROPPED: those existed only to move readers): ladder.md is FROZEN (no new cell, no new reader); town:core stays the named home of the GLOBAL season (core 2 == ladder 2 today; local-maxxing, streaming-suite, web-app-suite carry their OWN 1, sanctuary 2). HOLD any phase-B round (belam 14:01Z).
- PHASE W (AMENDED 14:5xZ by belam [owner] 14:54Z, banked 306d33621; HOLD until it lands, 0 live): workflow.py and hooks/workflow_note.py RETIRE (status deprecated, moved, never `git rm`; record goal:g5.33, goal:g4.6). The 30 manifests in extensions/agi/workflows/ are KEPT (narrow, self-contained spawn docs, never updated like cards): a review runs as a SPAWN = manifest + graph slice through a ONE-SHOT 'workflow spawn' launch template beside the self-rotating post template (council design, radically simple, under the 8 KB base). Skill agi-workflow is KEPT and renamed **agi-spawn-chain** (owner 17:4xZ, banked c88f1ae44; it supersedes 'round review' and the council's agi-one-shot) and re-aligned to the council's FLOW ROTATION design (a post's ordered string of one-shot + perpetual spawns over one graph slice; done -> the next phase fires, e.g. the review spawn; recursive; leaning on growth.tsv + the parent cells, no new table; goal:g7.16.1.11.14 skill deltas; rides IN W once that design fixes what the skill describes). W stays HELD until then. The references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass and config:commands are RE-POINTED, not dropped; config:rotations skills entries RENAME the clause (belam, the pb3 pattern: byte-exact sub at the merge-up, ONE update). Users today by ~/track: DG5 4, TM-new 1, DT-1 2, DT-2 1.
- PHASE C' (retire WITH the old-setup Python, never moved; gated by USE, not by a reader-parity gate): ladder.md, its 16 old-setup readers and season.py's write (:1061) retire when the old-setup Python retires. Gate: 0 new ladder.md lines in any live post's ~/track over 24 h (DG5 had 425 on 10-02) AND the last old-setup post is on v5. Then ladder.md status deprecated + moved to deprecated/ladder/ (retire, never delete).
- Deliberately NOT built: Z3's cells.tsv + cell.py resolver (1,156 B): a resolver for the old Python readers is bytes spent on code that retires with the old setup (owner 23:0xZ: 'you are over engineering it again'); it comes back only for a reader that must outlive the old setup and cannot read a row.

## Invariants
- No phase moves a ladder reader (owner 14:0xZ): until the old-setup Python retires, every reader keeps the cell it reads; ladder.md is frozen, never emptied. The AA2.25 workflow.py director-stage exception is MOOT (workflow.py retires, phase W).
- Nothing is deleted: ladder.md and [ladder].md are retired and moved, never `git rm`.
- 0 B in the zygote; the base stays <= 8,192 B (kid-of runs inside agi-kid, never in agi-project).
- THE THREE OWNER ITEMS ARE RULED: belam 05:07Z 10-02 RULED all three: (1) the moral/vision COUNT caps RETIRE (owner 03:4xZ); (2) the AA2.25 exception was CONFIRMED (now MOOT: phase W retires workflow.py); (3) belam's `kid` cell is WRITTEN (e56869124 = {harness: claude-code, model: claude-sonnet-5-5, max: 3}), so A4's writer is done; belam: 'Phase A may start via DG1' (it still needs belam's anchor signature on the [town] schema edit). Nothing in this goal stays HELD on them; phase A is the one startable round.

## Falsifier
1. Z4.a after A on the trunk (MET at c2decf431: the mur dg1z4a-c1 conjuncts L1-L4 MET, L5 UNVERIFIED): grow-check parity moves 0 verdicts except the 5 towns · Z4.b after A: dispatch.py resolve_role_spec for all 8 (tier, role) == before (A touches no spec) · Z4.e W: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn · Z4.f C': 0 new ladder.md lines in any live post's ~/track over 24 h AND the last old-setup post is on v5, the same day ladder.md moves. (Z4.e / Z4.f as Z4.6 of doc:rse-z4-ladder-out names them, trunk 8356d4114; its ~/track counts ANY open, so the 24 h window starts after the W round.) Z4.c / Z4.d of the old phase B/C (season dual-write, reader parity G1-G4) are DROPPED with the move.
2. Negative: `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0 hits throughout.

## Out of scope
goal:g7.16.1.11.12 (the AA2 side: depth, kid-of, the kid cell: its hypotheses are shared parents) · the moral/vision COUNT caps (RETIRE: ruled by belam 05:07Z, owner 03:4xZ; no matrix count column) · the old setup's own move to v5 (belam, SM, DG3, old TM) · moving any ladder reader (owner 14:0xZ: none will be moved).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-II 00:3xZ 10-10: horizon -> active on the OWNER (00:3xZ, verbatim): "We don’t use the ladder anymore" / "It needs to be deprecated". Nothing in the title changes: ladder.md (config:ladder) retires WITH the old-setup Python that reads it -- today 20 engine files under extensions/agi (brief, cli, crons, dispatch, hierarchy, legacy, rolslice, rotate, season, seat_status, send, spawn_gate, success_metrics, towns, verification, viewport, workflow, write, conftest, the councils fragment) -- so the node is deprecated (status + move to deprecated/, never git rm) only in the same landing that removes or re-homes its last reader. belam does not assign the build (council); routed to SM by box.
<!-- THOUGHT:END -->
