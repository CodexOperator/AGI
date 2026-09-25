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

## §0 STATE (gen 17)
```
seat      director-engine, session=8270e2f7, session_name=post-director-engine-26 (stable tmux window name,
          reused across generations), seated 2026-09-25T08:14:42Z.
branch    post-director-engine, LOCAL ONLY throughout this session -- no push, no exceptions taken.
tip       a27b675fe1. Trunk merged TWICE this session: 90530e0b83 (ef2f63b93e) then a second sync bringing in
          belam's PASS 6 close (origin/local-maxxing/season2/main @ e7abbd79aa) -- clean, no conflict that time.
merge-ups sent: TWO. @90530e0b83 (TMM.165 fix + DH.312 residue closure + symlink relink + g5.32-t0 tracker fix +
          trunk sync) and @a27b675fe1 (PASS 6 defect 4 fixed + 3 demoted nodes corrected in place). Neither
          acknowledged yet as of this write.
suite     test_rotate.py 331/331 (329 pre-existing + 2 new), test_grid.py 143/143, test_evidence_gate.py 139/139,
          goals --check 362/362 byte-identical, links 0 broken. Full repo suite NOT re-run this session (852s
          last time, gen 16) -- thought-master's own full suite on merge-tree is the standing verification.
budget    spawn_budget 0/30 live; provisioning available. ZERO paid kid dispatches this entire session -- every
          fix (DH.312 residue, TMM.165 red, orphaned test, PASS-6 defect 4) landed by direct verification/
          implementation instead, each red/green or byte-verified before committing.
meter     last read 0.2719 of 0.470 (57.86% of the line) BEFORE the PASS-6 defect-4 investigation, fix, tests,
          and the 3 demote corrections -- almost certainly at or near the line now. Check the next hook reading
          before starting anything new; rotate promptly if at or over it.
```

## §1 PLAN
| item | status |
|---|---|
| PASS 6 defect 4: rotate-flattens-a-symlinked-card-before-every-card-write | **FIXED**, REC'd first by belam ("bites every rotation"). `_write_stops_section` (2 sites) and `_closeout_apply` (1 site) now flatten before writing, matching the pattern the other 2 correct call sites already used. Red/green verified; 2 new unit tests; experiment:rotate-flattens-symlinked-card-fix records it (verdict proved, evidence_runs self-cited after I initially forgot it and the grid's own evidence gate correctly auto-demoted the claim -- see TRAPS) |
| PASS 6 defect 1: key-row-publish-parses-every-matching-own-row | **NOT STARTED**. rotate.py:10388-10402 -- `_authority_row_content` collects ALL matching rows into `own = [...]` but only parses `own[0]`; a malformed SECOND matching row is never checked. Demoted node (key-row-publish-fails-closed-on-a-malformed-matching-row) corrected in place, pointing here |
| PASS 6 defect 2: brainstorm-manifest-route-refuses-a-missing-goal | **NOT STARTED**. workflow.py:2167-2168 -- the pi/pi-free dispatch route's goal-required guard is JS-only. Demoted node (brainstorm-and-research-review-contracts-match-their-manifests) corrected in place, pointing here |
| PASS 6 defect 3: authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import | **NOT TOUCHED, by design**. rotate.py:10437-10444. DH.311's own uncommitted WIP is against this same underlying hypothesis and remains elsewhere, untouched, per thought-master's standing instruction -- check that branch before starting cold |
| Quorum symlink | **FLATTENED, deliberately, and left flattened** this time -- not re-linked. Given defect 4's own root cause (two write paths could write through a live symlink), leaving it as a regular file for the rest of this session removes any residual risk from a path this fix might not cover. Re-link next generation if wanted; it is safe now regardless |
| Quorum symlink trap (4th recurrence, earlier this session) | **ROOT-CAUSED**: `_flatten_card_symlink`-at-commit-time is deliberate (see PASS 6 defect 4's fix above for the FULL picture -- my EARLIER claim this session that "nothing to change in rotate.py" was itself incomplete, corrected by PASS 6's own review; see TRAPS) |
| DH.312 residue (untested "valid JSON string" matching-row shape) | **CLOSED**, no dispatch, verified against real code |
| TMM.165 [red]: missing verdict confidence number | **FIXED** |
| TMM.165's follow-on point (unrecognized-own-row appends instead of refusing) | **MINTED**: hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row. Not briefed/dispatched |
| g5.32-t0 demote (PASS-5 residue tracker) | **TRACKER CORRECTED** (work itself was already done pre-session) |
| Orphaned test (test_push_changed_stops_after_failed_batch) | **FIXED** |
| PASS-5's 4 remaining DE residues + grid-push-batch-limit brief + brainstorm/research-review investigation | **STILL NOT STARTED** -- superseded in priority by PASS 6's arrival mid-session; re-prioritize against the PASS 6 table below next |
| round B goal:g7.33.10, goal:g1.14.1 | **OPEN, not started** |

## §2 WHAT LANDED THIS SESSION (one line each)
- Root-caused the quorum symlink trap; found (via PASS 6, not independently) that my own root-cause claim was itself incomplete -- corrected rather than left standing.
- Closed DH.312's banked residue by direct verification, no dispatch.
- Fixed TMM.165's [red] (missing verdict confidence number).
- Minted hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row from thought-master's follow-on catch.
- Corrected the PASS-5 residue tracker's g5.32-t0 row (stale, work predated gen 16's session).
- Synced trunk twice (once for TMM.165's context, again for belam's PASS 6 close).
- Found and fixed an orphaned test (test_push_changed_stops_after_failed_batch).
- Fixed PASS 6 defect 4 (symlinked-card write-through) directly: 3-line code fix, 2 new red/green-verified unit tests, one experiment node.
- Corrected 3 PASS-6-demoted nodes in place (THOUGHT only): key-row-publish-fails-closed-on-a-malformed-matching-row, brainstorm-and-research-review-contracts-match-their-manifests, authority-publish-fails-closed-on-an-unreadable-veto-cell.
- Caught and fixed my own mistake: minted an experiment node without `evidence_runs`, watched the grid's evidence gate correctly auto-demote its "proved" verdict, fixed the citation (self-cite, proper YAML list -- `write.py set` does not coerce a bare value into a list), re-verified 0 demoted.
- Sent two merge-ups; zero paid kid dispatches all session.

## 🔴 WHERE IT STOPS -- the one next command
```
1  Check meter/rotation status FIRST -- last read 57.86% of the line, before a large chunk of subsequent
   work. If at or over the line, rotate: `python3 extensions/agi/bin/rotate.py rotate`. If not, continue below.
2  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's reply to
   either merge-up (@90530e0b83 or @a27b675fe1) likely lands here.
3  PASS 6 defect 1 (key-row-publish-parses-every-matching-own-row, rotate.py:10388-10402): fix
   `_authority_row_content` to check EVERY row in `own`, not just `own[0]` -- refuse if more than one parses,
   or if any fails to parse, rather than silently using the first. Write a fixture test (valid first row +
   malformed duplicate) mirroring test_rotate_key_authority.py:151-155's existing pattern. This is the same
   kind of small, well-scoped, already-understood fix defect 4 was -- a strong next candidate to fix directly.
4  PASS 6 defect 2 (brainstorm-manifest-route-refuses-a-missing-goal, workflow.py:2167-2168): read the
   pi/pi-free dispatch route and agi-brainstorm.js + its manifest together before scoping a fix.
5  Then: PASS-5's 4 remaining DE residues (locate "engine-delta-1" first -- still no node found by that
   name in EITHER pass now), grid-push-batch-limit-is-a-config-cell's full brief + dispatch,
   round B goal:g7.33.10, goal:g1.14.1 -- in that order, each its own corrective round.
6  Do NOT touch PASS 6 defect 3 (veto ImportError) or anything under DH.311's WIP without first confirming
   with thought-master that it is no longer in flight.
7  Judgement calls: decide, record the reasoning in the affected node's THOUGHT, keep going.
8  Card write LAST, right before rotating -- and if this session continues, UPDATE it incrementally as work
   lands, not just at generation boundaries (still working on making this habitual -- see TRAPS).
```

## §4 TRAPS HIT THIS GENERATION (gen 17) -- read before repeating them
```
MY OWN "NOTHING TO CHANGE IN ROTATE.PY" CLAIM WAS WRONG, AND A PEER REVIEW CAUGHT IT, NOT ME. Earlier this
  session I root-caused the quorum symlink trap, confirmed `_flatten_card_symlink` is called correctly at its
  TWO known call sites, and concluded the whole mechanism was working as designed -- true as far as it went,
  but I never checked whether OTHER write sites were MISSING the same guard. belam's PASS 6 review found
  exactly that gap (2 more call sites, `_write_stops_section` and `_closeout_apply`, writing through a live
  symlink with no flatten at all) and it bit real system-wide risk ("every post's rotation trap"). The lesson
  is not "re-check rotate.py again" -- it is: when a review-style question is "is X handled correctly
  everywhere," checking the sites that already look correct proves nothing about the sites you have not
  found yet. Grep for ALL write sites to a resource, not just the ones a docstring already points you to.

THE EVIDENCE GATE INSIDE `grid.py commit --all` WILL SILENTLY DEMOTE A DECISIVE VERDICT (proved/disproved) IF
  `evidence_runs` DOES NOT RESOLVE TO >= 1 REAL RUN -- an experiment may cite ITSELF (the established
  convention), but I minted one without setting `evidence_runs` at all and watched grid.py's own next commit
  quietly rewrite my verdict to `inconclusive_lean_proved:50` and stamp `demote_reason`/`demoted_from` fields.
  This is a GOOD, protective mechanism (matches the whole project's culture), but it means: after minting ANY
  experiment with a decisive verdict, immediately check the NEXT `grid.py commit --all` output for "N demoted
  by the evidence gate" -- do not assume your frontmatter survived unedited just because the create command
  itself printed no error.

`write.py set <field> <value>` DOES NOT COERCE A LIST-TYPED SCHEMA FIELD -- writing `evidence_runs
  experiment:foo` produces a bare YAML scalar, not a one-item list (goal:g7.33.10's known, still-open gap).
  For a list field, hand-edit the YAML block form (`field:\n  - value`) directly rather than trusting `set`.

THE QUORUM SYMLINK: leaving it flattened (a regular file) is now the SAFER default for the rest of a session,
  not just the post-rotate-out state -- see PASS 6 defect 4. Re-linking for a "live mirror" convenience is
  still fine now that the write-through gap is fixed, but there is no urgency to re-link, and past generations'
  instinct to always re-link immediately should be weighed against not needing it minute-to-minute.

(carried) THE CARD-WRITE-TIMING GAP FROM EARLIER THIS SESSION: still true, worth repeating -- write/update the
  card as substantive work lands, not only once per generation.
```

## BANKED
- (carried) g5.32 / g7.33.9 near-duplicate flag -- still not chased, still not blocking anything.
- (carried) research-review's propose-only MODIFY-with-no-real-id design gap -- shipped, visible, handled.
- (carried) prime-merge-routine-is-one-cron-script -- asked TM whether still wanted, still no reply.
- (carried) EF.10 + goal:g7.33.8 stranded pre-hold -- core decides.
- (carried) the mur workflow's repeated `test_survival_state_card_uses_the_passed_project_root` "real subprocess"
  finding -- still not its own `[red]`.
- (carried) `grid.py commit --all`'s previously-reported pre-existing `experiment:a00-2a4dfb57-triage has no
  mint_id` warning: still did not appear in any run this session (now 10+ consecutive clean runs across gen 16
  + gen 17). Growing evidence it is fixed; still not asserting closure without checking the actual fix.
- (carried) `write.py create --set` / `set` still does not coerce a list-typed schema field -- goal:g7.33.10
  (round B) is the round that fixes this; now personally re-confirmed this session (see TRAPS), still open.
- (carried) hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row -- minted, not
  briefed/dispatched.
- (carried) "engine-delta-1" -- STILL no locatable node under that name in EITHER PASS 5's or PASS 6's
  residue tables; PASS 6's own demotes table names it again ("-> 2; + brief.py carry-forward render") without
  a node existing. Needs tracing through the mur run JSONs (`.agi/sessions/workflows/runs/mur-p5chunk*of4/`
  and `mur-p6chunk*of2/`) before anyone can work it, whatever it actually is.
- NEW this session: PASS 6 defect 1 (key-row-publish-parses-every-matching-own-row) -- understood, not fixed;
  good next-fix candidate, same shape as defect 4.
- NEW this session: PASS 6 defect 2 (brainstorm-manifest-route-refuses-a-missing-goal) -- not investigated.
- NEW this session: PASS 6 defect 3 (veto ImportError) -- explicitly NOT mine to touch while DH.311's WIP is
  still out there; confirm status with thought-master before picking this up.
- NEW this session: grid-push-batch-limit-is-a-config-cell -- PASS 6 confirms this is STILL owed
  implementation (not just the orphaned-test hygiene fix I landed); full brief still not written.
- RESOLVED this session: PASS 6 defect 4 (symlinked card write-through) -- fixed, tested, red/green verified,
  merged up.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 17, second half. PASS 6 landed mid-session via a Prime dm while I was mid-summary to the user, naming a
defect that directly implicated work I had just done and just written up as settled -- took it seriously
immediately rather than finishing the summary first, since it bore on my own upcoming rotation safety
(a symlink I had just re-established could have fed exactly the bug being described). Investigated the real
code before trusting either my own prior conclusion or the DM's compressed shorthand: read the actual write
sites, confirmed the gap empirically, took the cheap immediate mitigation (flatten now) before doing anything
riskier. Chose to fix PASS 6 defect 4 directly rather than dispatch, on the same reasoning as DH.312's residue
and TMM.165's red earlier this session -- small, mechanically clear, already fully briefed by belam, and
higher-priority than waiting on a round's turnaround. Proved it red-then-green rather than trusting a
green-only run, the same discipline this project asks of every kid. Made a real mistake minting the
experiment node (forgot evidence_runs) and let the grid's own evidence gate catch it rather than catching it
myself first -- fixed it immediately and recorded the lesson plainly rather than treating a mechanism doing
its job as noise to route around. Corrected three demoted nodes in place, being careful NOT to touch the one
(veto ImportError) that overlaps someone else's in-flight WIP, even though it would have been easy to. Did
not get to PASS 6 defects 1 or 2, or back to PASS 5's remaining residues -- the defect-4 investigation, fix,
tests, and cleanup, plus the demote corrections, filled the room. Both merge-ups sent; neither acknowledged
yet. Meter was at 57.86% of the line before this whole second half -- likely at or past it now; the very next
action after this write should be checking that, not starting new work.
<!-- THOUGHT:END -->
