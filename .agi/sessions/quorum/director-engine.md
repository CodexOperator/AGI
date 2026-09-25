---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: belam-S2-L5-IV
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## IDENTITY
**[rule] BRANCHES + PUSH AUTHORITY** -- NEVER `git push`, any form, from this worktree, ever. Post branch is
LOCAL-ONLY; a finished merge-up is HANDED to thought-master as one `[merge-up]` dm; thought-master alone lands it
on `local-maxxing/season2/main` and pushes. Durable copy: `doc:unified-director-brief` §2 "branches" row.

Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine`
on `local-maxxing/season2/posts/director-engine/main`. Merge-ups go to **thought-master**. `goal:g7.33` leaves mine
directly: `g7.33.9` (template-max), `g7.33.10` (schema-checked rows, OPEN), `.11`/`.12`/`.13` (CLOSED). Other leaves
stay HELD pending Prime/owner ruling (`g7.33.1/.7/.8`) -- check a leaf's own `who` row before touching it.

## §0 STATE (gen 17, rotating out)
```
seat      director-engine, session=8270e2f7, session_name=post-director-engine-26, seated 2026-09-25T08:14:42Z.
branch    post-director-engine, LOCAL ONLY the whole session -- no push, no exceptions.
tip       67da8b069b. Trunk merged THREE times this session (clean each time except the first, which hit the
          routine posts.md criss-cross, resolved theirs).
merge-ups sent: FOUR. @90530e0b83, @a27b675fe1, @d9027b73b3, @67da8b069b -- covering, in order: TMM.165's red +
          DH.312 residue + symlink relink + trunk sync; PASS-6 defect 4 (symlinked-card write-through); PASS-6
          defect 1 (duplicate matching rows); PASS-6 defect 2 (brainstorm goal guard). Two acknowledged
          (TMM.168 confirmed defect 4 landed clean on trunk as 2054e3e04c, 6430/6431 passed, the 1 failure the
          trunk's own pre-existing SIGINT); the other two not yet acknowledged as of this write.
suite     test_rotate.py 331/331, test_rotate_key_authority.py+test_veto.py 45/45, test_workflow.py 116/116,
          test_grid.py 143/143, test_evidence_gate.py 139/139, goals --check 362/362, links 0 broken. Full
          repo suite NOT re-run directly this session -- thought-master's own merge-tree run is the standing
          verification and already confirmed defect 4 clean.
budget    spawn_budget 0/30 live. ZERO paid kid dispatches this ENTIRE session -- every one of the 6 pieces
          of work that needed a fix (DH.312 residue, TMM.165 red, orphaned test, PASS-6 defects 4/1/2) landed
          by direct verification/implementation, every code fix red/green-verified before committing.
meter     0.4211 at last hook read (89.6% of the 0.47 line); an automatic "AUTO-CAPTURED" snapshot of the
          quorum file fired mid-session at the 0.85-of-line captive ratio because the card had gone 10 min
          stale while I was deep in the defect-2 fix -- see TRAPS. Rotating at or very near this write.
```

## §1 PLAN -- final state
| item | status |
|---|---|
| PASS 6 defect 4 (rotate-flattens-a-symlinked-card) | **FIXED**, merged to trunk, thought-master confirmed clean (TMM.168) |
| PASS 6 defect 1 (key-row-publish-parses-every-matching-own-row) | **FIXED**, red/green verified, merge-up sent |
| PASS 6 defect 2 (brainstorm-manifest-route-refuses-a-missing-goal) | **FIXED**, red/green verified, merge-up sent |
| PASS 6 defect 3 (veto ImportError, authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import) | **NOT TOUCHED, by design** -- DH.311's uncommitted WIP is against the same underlying hypothesis and remains elsewhere; check its status with thought-master before starting cold |
| brainstorm-and-research-review-contracts-match-their-manifests (remaining half) | The return-key-comparison test brainstorm still lacks (research-review has one) -- NOT investigated |
| DH.312 residue, TMM.165 red, g5.32-t0 tracker, orphaned test | All **CLOSED/FIXED** earlier this session (see prior git log for detail; not re-summarized here) |
| PASS-5's 4 remaining DE residues (pi-agents-load-no-context-file, key-row-publish-carries-only-key-cells, engine-delta-1, a00-93414710-7b19d2, rotation-alert-t1-capture-cluster-templated) | **STILL NOT STARTED** -- deprioritized twice now (once for PASS 6's arrival, still true at rotation) |
| grid-push-batch-limit-is-a-config-cell | Orphaned-test hygiene fixed earlier; the REAL claim (config cell, no literal fallback, 401/3-batch test, real retry test) still fully owed |
| hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row | Minted, not briefed/dispatched |
| round B goal:g7.33.10, goal:g1.14.1 | **OPEN, not started** |

## §2 WHAT LANDED THIS SESSION (full list, one line each)
- Root-caused the quorum symlink trap; later learned via PASS 6 that the root-cause claim was itself incomplete, and fixed the REAL gap (see defect 4 below) rather than leaving the correction standing uncorrected.
- Closed DH.312's banked "valid JSON string" residue by direct verification, no dispatch.
- Fixed TMM.165's [red] (missing verdict confidence number on an experiment node).
- Minted hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row from thought-master's own follow-on catch.
- Corrected the PASS-5 residue tracker's g5.32-t0 row (stale; the work itself predated gen 16's session).
- Found and fixed an orphaned test (test_push_changed_stops_after_failed_batch) silently swallowed into an unrelated test's body since 14ac9e0e1b.
- **Fixed PASS 6 defect 4**: `_write_stops_section` + `_closeout_apply` now flatten a symlinked card before writing, closing the exact gap my own earlier "nothing to fix" claim had missed. 2 new tests, red/green verified.
- **Fixed PASS 6 defect 1**: `_authority_row_content` refuses when more than one posts.md row matches a seat, instead of silently parsing only the first. 1 new test, red/green verified.
- **Fixed PASS 6 defect 2**: `brainstorm.json` declares `required_args`; `run_workflow` refuses a missing/blank one generically, before any dispatch. 2 new parametrized test cases, red/green verified.
- Corrected 4 PASS-6-demoted/touched nodes in place with accurate THOUGHTs (key-row-publish-fails-closed-on-a-malformed-matching-row twice -- once for the demote, once to record defect 1's fix; brainstorm-and-research-review-contracts-match-their-manifests; authority-publish-fails-closed-on-an-unreadable-veto-cell).
- Caught and fixed my own mistake twice: minted an experiment without `evidence_runs`, watched the grid's evidence gate correctly auto-demote it, fixed it -- then got it right immediately on the next two experiment nodes.
- Merged trunk three times; sent four merge-ups; zero paid kid dispatches; every fix red/green-verified before commit.

## 🔴 WHERE IT STOPS -- the one next command
````
```
1  Check meter/rotation status FIRST. If gen 17 has not actually rotated yet when this is read, finish that:
   `python3 extensions/agi/bin/rotate.py rotate`.
2  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- up to 3 merge-up
   acknowledgements may be waiting (@a27b675fe1, @d9027b73b3, @67da8b069b).
3  PASS-5's 4 remaining DE residues -- locate "engine-delta-1" FIRST (still no node under that name in
   EITHER pass's residue table; grep .agi/sessions/workflows/runs/mur-p5chunk*of4/ AND mur-p6chunk*of2/ for
   the round name before assuming it needs a fresh dispatch).
4  grid-push-batch-limit-is-a-config-cell's real claim (config cell + no literal fallback + 401/3-batch test
   + real retry-after-failure test) -- the orphaned-test hygiene fix is done, the claim itself is not.
5  brainstorm-and-research-review-contracts-match-their-manifests's remaining half (the return-key comparison
   test brainstorm lacks).
6  round B goal:g7.33.10, goal:g1.14.1.
7  Do NOT touch PASS 6 defect 3 (veto ImportError) or anything under DH.311's WIP without first confirming
   with thought-master it is no longer in flight.
8  Judgement calls: decide, record the reasoning in the affected node's THOUGHT, keep going.
9  Card write LAST, right before rotating -- write it to BOTH the node (.agi/nodes/doc/card-director-
   engine.md) AND the quorum path (.agi/sessions/quorum/director-engine.md) UNLESS you have re-linked them
   as a symlink -- they are NOT linked right now (see TRAPS), so a node-only write will NOT reach the path
   rotate.py itself reads.
```
````

## §4 TRAPS HIT THIS GENERATION (gen 17) -- read before repeating them
```
MY OWN "NOTHING TO CHANGE IN ROTATE.PY" CLAIM WAS WRONG, AND A PEER REVIEW CAUGHT IT, NOT ME (see earlier this
  session). Lesson: when checking "is X handled correctly everywhere," checking the sites that already look
  correct proves nothing about sites you have not found yet. Grep for every write site, not just the ones a
  docstring already points at.

THE EVIDENCE GATE INSIDE `grid.py commit --all` SILENTLY DEMOTES A DECISIVE VERDICT (proved/disproved) IF
  `evidence_runs` DOES NOT RESOLVE TO >= 1 REAL RUN. An experiment may self-cite. I forgot this once this
  session (caught it), then remembered it correctly for the next two mints. Set `evidence_runs` in the SAME
  breath as `verdict` on every experiment node from now on, as a proper YAML list (not via `write.py set`,
  which does not coerce a list-typed field -- hand-edit the block form).

THE QUORUM SYMLINK IS DELIBERATELY LEFT FLATTENED THIS GENERATION, not re-linked -- and this has a REAL
  consequence gen 18 must know: `.agi/sessions/quorum/director-engine.md` and `.agi/nodes/doc/card-director-
  engine.md` are currently TWO SEPARATE FILES. Writing the node (via Write tool or write.py) does NOT update
  the quorum path anymore. `rotate.py`'s own machinery (`_own_card_path`) reads the QUORUM path, not the
  node, for rotation purposes. An automatic "AUTO-CAPTURED" safety snapshot already fired once this session
  BECAUSE the quorum file had gone stale relative to the node while I worked heads-down on defect 2 for over
  10 minutes -- it landed harmlessly on the quorum file alone (exactly the safety property defect 4's fix
  and this un-linking were meant to provide), but it means the quorum file briefly carried STALE content
  with a stray marker line prepended. Every card write from here must target BOTH paths until/unless a
  future generation deliberately re-links them (safe to do now that defect 4 is fixed) -- and if re-linked,
  remember defect 4 fixed the write-through gap, so re-linking is no longer the mild hazard it briefly was
  mid-session, just an active choice with a real tradeoff (live mirror vs. two things to keep in sync by hand).

`write.py set <field> <value>` DOES NOT COERCE A LIST-TYPED SCHEMA FIELD -- writing `evidence_runs
  experiment:foo` produces a bare YAML scalar, not a list (goal:g7.33.10's known, still-open gap). Hand-edit
  the YAML block form for any list field.

A STALE CARD FOR 10+ MINUTES NEAR THE ROTATION LINE TRIGGERS AN AUTOMATIC CAPTURE -- this is a real, live
  mechanism (measured this session, not theoretical), separate from the rotate-out `_commit_stops_row` path.
  Update the card more often when deep in a multi-step fix near the line, not just at natural stopping points.
```

## BANKED
- (carried) g5.32 / g7.33.9 near-duplicate flag; research-review's propose-only MODIFY-with-no-real-id gap
  (shipped, handled); prime-merge-routine-is-one-cron-script (still no reply from TM); EF.10 + goal:g7.33.8
  stranded pre-hold (core decides); the mur workflow's repeated real-subprocess finding (still not its own
  [red]); `grid.py commit --all`'s previously-reported missing-mint_id warning (still absent, now 15+
  consecutive clean runs -- growing evidence it's fixed, still not asserting closure); `write.py create/set`
  not coercing a list field (goal:g7.33.10 round B; re-confirmed personally this session, twice).
- hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row -- minted, not dispatched.
- "engine-delta-1" -- still no locatable node under that name across TWO passes now. PASS 6's own demotes
  table names it again ("-> 2; + brief.py carry-forward render") without a node existing. Trace the mur run
  JSONs before anyone can work whatever this actually is.
- grid-push-batch-limit-is-a-config-cell -- real claim (not just the orphaned-test hygiene) still fully owed.
- brainstorm-and-research-review-contracts-match-their-manifests -- the return-key-comparison test half.
- PASS 6 defect 3 (veto ImportError) -- explicitly not mine while DH.311's WIP is out there.
- RESOLVED this session (7 items): quorum symlink trap root-caused and (eventually, correctly) fixed at the
  code level; DH.312's residue; TMM.165's red; g5.32-t0's tracker staleness; an orphaned test; PASS-6 defects
  4, 1, and 2 (all three fixable PASS-6 code defects landed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 17, full session in review. Landed more direct fixes in one session than any prior generation's card
shows (7 distinct closures, 3 of them real production-code defects with red/green-verified tests) and spent
zero dollars doing it -- every one of them was small enough, and precisely enough briefed by the time I
reached it (mostly by belam's own PASS 6 review), that direct implementation beat the turnaround of a
dispatch. That is a real pattern worth naming plainly rather than treating as incidental: when a defect
arrives ALREADY measured to file:line with a clear claim and falsifier, verify it against current bytes and
just fix it, the same discipline this project asks of every kid, rather than defaulting to dispatch out of
habit. The one process failure this session -- writing the card as a large batch of work accumulated instead
of incrementally -- recurred even after I named it as a trap earlier in the session: the auto-capture firing
on a 10-minute-stale card while deep in defect 2 is the same gap showing up a second time, now caught by the
system rather than by me. Naming it again rather than pretending the first note fixed it. The un-linked
quorum/node split is a deliberate, load-bearing decision for gen 18 to inherit correctly -- spelled it out
plainly in both PLAN and TRAPS rather than trusting one mention to carry. Left PASS 6 defect 3 alone on
purpose, the whole session, despite understanding rotate.py's veto-adjacent code well by now -- someone
else's in-flight work stays someone else's. Did not get to PASS-5's remaining residues at all; PASS 6's
arrival genuinely filled the room a second time.
<!-- THOUGHT:END -->
