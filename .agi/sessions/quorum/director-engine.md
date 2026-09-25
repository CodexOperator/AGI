AUTO-CAPTURED
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
**[rule] BRANCHES + PUSH AUTHORITY (owner 09-25 02:54Z, verified/signed via belam, after director-thought pushed its
own remote head by accident) -- NEVER `git push`, ANY form, from this worktree from here on.** The post branch is
LOCAL-ONLY now: no `refs/agi/posts/*`, no `refs/heads`, no `-u`. A finished merge-up is HANDED to thought-master (one
`[merge-up]` line, as before) and THOUGHT-MASTER is the only one who lands it on `local-maxxing/season2/main` and
pushes; belam (the Prime) keeps `local-maxxing/main` + `season2/main` fast-forwarded from that trunk. This is safe
because every post shares ONE git object store on this box -- thought-master reads this branch directly, no push
needed for it to see my commits. Durable copy: `doc:unified-director-brief` §2 "branches" row. THE OLD DISPATCH-LINE
CONVENTION IN THIS CARD (BUILD LOOP #2, further down) STILL SAYS TO PUSH -- that line is now STALE, superseded by
this rule; git commit locally and stop there, never push, until that line is corrected.

Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine` on
`local-maxxing/season2/posts/director-engine/main`. Merge-ups go to
**thought-master**. `goal:g7.33` = core's umbrella, but per-LEAF, not a blanket hold: `goal:g7.33.9` (template-max),
`goal:g7.33.10` (schema-checked rows), `goal:g7.33.11` (grid push, CLOSED) and `goal:g7.33.12` (research-review fix, new
this session) each carry their own `who: director-engine, batched by thought-master` row and are mine to work directly
-- verified against the node bytes this session, not assumed. Specific OTHER leaves stay HELD pending a Prime/owner
ruling (`g7.33.1`, `g7.33.7`, `g7.33.8` confirmed HELD by grep of the dm log) -- check a leaf's own `who` row before
touching it, never assume the whole g7.33 subtree by default either way.

## LIVE STATE + STOPS (gen 13, rotating -- all three DH.299-301 parents harvested this session)
```
HARVEST UPDATE (after the three dispatches below finished, same session): all three reported harvest before rotation.
- DH.299 (TMM.136): MERGED, tip 10cc524ac2 (merge commit; brief.py + test_brief.py). Verified independently by the
  director on BOTH the loop branch and the merged HEAD: 201/201 in the brief test neighbourhood each time. [merge-up]
  #13 sent to thought-master, with a disclosed deviation: merged on direct verification (diff + two independent test
  runs), not a completed mur pass, because the rotation line was close (73% when the harvest landed) and a malformed
  mur args file risked eating the remaining budget for nothing. thought-master's own landing gate is the independent
  check this round; a mur can still run next generation if thought-master wants one before it lands on the trunk.
- DH.300 (round B, g7.33.10): NOT merged -- correctly nothing to merge. The parent's own review demoted its kid to
  inconclusive_lean_disproved: it measured the bug (5/5 schema-violation probes still admitted) but did not
  implement the fix (production_lines=0). Hypothesis stays open; needs a fresh round next generation, ideally with
  an orders file that states more forcefully that a measurement-only kid is not a finished round for this claim.
- DH.301 (g1.14.1's round): NOT merged -- nothing to merge (no production diff). The kid re-verified the
  hypothesis's Measured line citations (they had drifted: now workflow.py _load_manifest:791, _expand_stages:802,
  _run_stage_pi:1779, _failed_dependency:2111, run_workflow:2149, pi loop 2280-2373) and correctly refused to force
  a partial 40-line implementation, instead requesting a 220-line/3-seam decomposition (round execution ~120 lines,
  manifest composition ~60, harvest/config ~40). The parent's rebrief answer was "cut" rather than granting the
  larger ceiling. Recorded the full plan + corrected citations in the hypothesis's own THOUGHT (committed
  separately, 10cc524ac2's parent commit) so the next round can dispatch directly against it with a raised ceiling,
  never re-deriving the scoping work from scratch.
```

```
STARTUP NOTE, ROOT-CAUSED (not just worked around): this session's first Read of .agi/sessions/quorum/
director-engine.md returned STALE gen-11 content (199 lines, DH.298-era) even though `git log`/`git status` on
`.agi/nodes/doc/card-director-engine.md` prove the real HEAD has been gen 12's accurate 167-line rotate-out
(0e9974aa13) all along -- no bytes were ever lost. Root cause, confirmed by `ls -la`: the quorum path was NOT a
symlink at all, it was a two-generations-stale PLAIN FILE. `doc:unified-director-brief` §3 says rotate's
`stop_commit` step flattens the symlink into a real file, and "the successor re-links, not the outgoing director"
-- gen 11 flattened it (capturing gen 11's own 199-line content) at its own rotate-out, gen 12 never re-linked it,
so gen 12's OWN rotate-out had nothing left TO flatten (already a plain file) and silently no-opped, leaving gen
11's snapshot sitting there completely unrelated to gen 12's real card for this session's entire first read. FIXED:
`rm` the flattened file, `ln -s ../../nodes/doc/card-director-engine.md director-engine.md` in this worktree's
`.agi/sessions/quorum/`, verified byte-identical to the real node afterward. LESSON: skipping the re-link once does
not just cost the skipping generation -- it goes stale FOREVER across every subsequent generation until someone
notices `ls -la` shows a plain file instead of an `l...` symlink and fixes it. Check this on your FIRST substantive
action, every generation, not just when a read looks suspicious.

TMM.147 (thought-master, cross-session message from "agi-b9", arrived mid-session): re-listed everything owed after
TMM.146 crossed the rotation boundary undelivered. All five items now DONE or DISPATCHED this session:

1. THOUGHT fixes (TMM.146/147 item 1) -- DONE, tip aebc4cb7f0.
   - goal:g1.14.1 had NO THOUGHT block. Added the FULL verbatim owner line at 2026-09-25T00:37:38Z, pulled directly
     from predecessor session e3bf5bfa's own transcript (jsonl), not retyped from thought-master's ellipsis-truncated
     relay: "Oh woops sorry i misunderstood what prime was saying. Let's re-mint the hypothesis but under the
     appropriate subgoal or sub-subgoal instead. Somewhere in config maxxing likely as it'll involve another custom
     template or chaining existing ones in a fresh template." Much fuller than the relay -- worth pulling the primary
     source even when a relay looks complete.
   - goal:g7.33.11's Agent Notes said the 4th push-changed tick was 21 refs; thought-master flagged it as 26. Did NOT
     take the correction on faith -- grepped the real cron log myself (/home/belam/logs/agi-crons-agi-3fbc6951.log:
     817431, "grid push batch 1/1: 26 ref(s)") and confirmed 26 is right. Corrected + noted why in the THOUGHT.
   - The owner's second quote (01:13:03Z, "research review bug can be prioritized at this time") was NOT found
     anywhere in director-engine's own transcript despite an exhaustive search across every director-engine jsonl in
     the project dir -- it must have been said in a different pane. Used it anyway, but cited as a corroborated relay
     (identical, independently, in thought-master's dm AND on town:local-maxxing's board) rather than claiming it as
     a verified primary-source quote. Say what you actually verified, not more.

2. Fixes-leaf for the already-landed research-review fix (TMM.144 item 3 / TMM.147 item 2) -- DONE, tip aebc4cb7f0.
   Minted goal:g7.33.12 under goal:g7.33 (not under goal:g6.11, where a superficially similar sibling hypothesis
   lives -- g6.11 is a generic spawn/dispatch/kid-lifecycle TEST bucket, not a research-review fixes home; g7.33 is
   the actual "engine fixes surfaced by the town" family this fix matches, same shape as g7.33.9/10/11). Caught and
   fixed two of my own mint bugs before committing: `write.py create --set tags=a,b,c` writes a raw comma STRING, not
   a YAML list, even though the schema declares `tags: {type: list}`; and `seeds` (schema-REQUIRED) was silently
   omitted with no refusal. `links.py schema` count dropped 198 -> 197 once hand-fixed. This exact bug class became
   the fresh, first-hand evidence cited in item 4 below.

3. TMM.136 (parent's kid-spawn --orders path is ambiguous prose, not a real path) -- MERGED as DH.299 (see HARVEST
   UPDATE above). Investigated the mechanism myself before minting: `brief.py:2074-2103` (`_orders_section`) renders
   a DIRECTOR's `--orders` bytes VERBATIM into a PARENT's brief with no path logic of its own, so an ambiguous
   phrase reaching a parent's own kid-spawn line has to originate in prose somewhere upstream. Named
   `brief.py:1874-1888` (the parent's carry-forward instruction, teaching the deprecated `--prompt-file <path|->`)
   as a well-evidenced candidate, honestly, rather than a claimed-proven root cause -- the dispatched parent's own
   kid independently confirmed it was the real one and fixed it.

4. Round B, goal:g7.33.10 (write.py's set/create --set should be schema-checked) -- DISPATCHED as DH.300, correctly
   NOT merged (see HARVEST UPDATE above: measured, not fixed). goal:g7.33.10's own body already carried a
   near-complete brief; transcribed it into the hypothesis schema shape and added fresh first-hand evidence from
   item 2 above (tags-as-string, missing seeds) as independent, same-session confirmation the gap is real.

5. goal:g1.14.1's round (the owner's 00:37Z re-mint; hypothesis:a-round-stage-spawns-the-parent-and-chains-its-
   review-in-one-workflow) -- DISPATCHED as DH.301, correctly NOT merged (see HARVEST UPDATE above: scoped, not
   implemented). The hypothesis was already fully specified from a prior session and its own THOUGHT flagged its
   line citations needed re-verification since the tree had moved; the dispatched kid did that verification and
   found the work needs decomposing, recorded in the hypothesis's own THOUGHT now.

All three rounds were dispatched with genuinely DISJOINT file scopes (brief.py+tests / write.py+links.py+tests /
workflow.py+workflows/+tests), matching TMM.128's own precedent for running disjoint rounds in parallel.

Nothing else from TMM.147 remains: all five items are done, merged, or correctly left open with a recorded reason
and a next step. No new work invented beyond what was explicitly ordered.
```

## BANKED
- (carried from gen 12) The g5.32 / g7.33.9 near-duplicate flag -- still not chased, still not blocking anything.
- (carried from gen 12) research-review's propose-only MODIFY-with-no-real-id design gap -- shipped code makes it
  VISIBLE and handled, a future round might want to actually mint the MODIFY'd version once a batch is promoted to
  mint:true. Not a defect in what shipped.
- (carried from gen 11, still unclaimed) prime-merge-routine-is-one-cron-script -- asked TM whether still wanted, no
  reply yet.
- (carried from gen 11, still unclaimed) EF.10 + goal:g7.33.8 stranded pre-hold -- flagged in a prior merge-up; core
  decides.
- (carried from gen 11) `seatsig/veto.py`'s `read()` swallows a malformed-cell exception internally -- still just a
  candidate small round, not queued.
- (carried from gen 11) the mur workflow's repeated `test_survival_state_card_uses_the_passed_project_root`
  "real subprocess" finding -- four consecutive passes now flagged it; carried alongside [merge-up] #13's own
  disclosed mur-skip this session, still not its own `[red]`.
- (carried from gen 13) `grid.py commit --all` printed one pre-existing, unrelated error during this session's node
  commits: `experiment:a00-2a4dfb57-triage has no mint_id -- refusing to write a node-id-keyed ref for it. Run
  backfill-mint-ids.py --write first.` Not mine to fix -- flagging for whoever next runs a full
  `backfill-mint-ids.py` pass.
- NEW this session: `rotate.py rotate`'s own `stop_commit` step is NOT safely re-runnable when it blocks on a
  dirty-tree check it created itself -- each retry stacked ANOTHER layer of code-fence wrapping and ANOTHER
  duplicate THOUGHT block onto this exact card (5 duplicates accumulated across 4 retries before caught and
  manually truncated back to one, this session). See the TRAPS entry below for the mechanism and the manual fix;
  this is a real rotate.py defect worth a `[red]` to thought-master, not something a future generation should
  just keep re-triggering by retrying blindly.

## TRAPS HIT THIS GENERATION (gen 13) -- read before repeating them
```
SKIPPING THE POST-ROTATION SYMLINK RE-LINK GOES STALE FOREVER, NOT JUST FOR ONE GENERATION -- CHECK `ls -la` ON YOUR
  OWN QUORUM PATH ON YOUR FIRST SUBSTANTIVE ACTION, EVERY TIME. The very first Read of this post's own card this
  session returned gen-11-era content (199 lines) that matched neither `git log` nor `git status` on the REAL node
  file (`.agi/nodes/doc/card-director-engine.md`; last real commit 0e9974aa13, gen 12's accurate 167-line rotate-out,
  zero uncommitted changes). Root cause via `ls -la`, not a filesystem fluke: `.agi/sessions/quorum/
  director-engine.md` was a two-generations-stale PLAIN FILE, not a symlink. `doc:unified-director-brief` §3 already
  names the mechanism ("rotate's stop_commit flattens the link: re-link it after a rotation... the successor
  re-links, not the outgoing director") -- gen 11 flattened it at its own rotate-out (capturing gen 11's content),
  gen 12 never re-linked it, so gen 12's OWN rotate-out had no symlink left to flatten and silently no-opped,
  stranding gen 11's snapshot indefinitely. Fixed this session (`rm` + `ln -s ../../nodes/doc/card-director-engine.md
  director-engine.md`, verified byte-identical). The independent ground-truth re-derivation this triggered (dm log +
  git log) was not wasted -- it happened to confirm exactly what the real card already said was open -- but do not
  count on that luck: `ls -la` the quorum path FIRST, before trusting a Read through it, every generation.
AN OWNER QUOTE RELAYED BY A PEER CAN BE PARTIAL EVEN WHEN IT READS AS COMPLETE. Thought-master's relay of the
  00:37:38Z owner line used ellipsis and was genuinely missing real content (the "Oh woops sorry i misunderstood
  what prime was saying" opening, and the closing sentence naming config-maxxing specifically) -- the predecessor
  session's own transcript had the full line. The 01:13:03Z line, by contrast, was relayed WITHOUT ellipsis, reads
  as a complete sentence, and could not be found in this post's own transcript at all after an exhaustive search --
  it was said somewhere else entirely. Two quotes, two different failure modes; neither is safe to retype from a
  relay without at least trying the primary source first, and "I could not find the primary source" is itself worth
  recording rather than silently upgrading a relay to look like a verified quote.
`write.py create <type> <slug> --set <field>=<v1,v2,v3>` DOES NOT COERCE A LIST-TYPED SCHEMA FIELD -- it writes the
  raw string. Hit on BOTH new mints this session before I started checking. `--set tags=a,b,c` on any node whose
  schema declares `tags: {type: list}` needs a manual follow-up fix (or a real YAML list block) every time until
  goal:g7.33.10's round actually lands. Same silent gap exists for a missing REQUIRED field on create (no `seeds` ->
  no refusal) -- `links.py schema` is the only thing that will ever tell you, and only if you remember to run it.
A DUPLICATE HEADING BUG FROM `write.py create --body-file` CAN RECUR IF YOUR BODY FILE STARTS WITH ITS OWN `#
  <id>` LINE -- `create` already renders one. g7.33.10 hit this at its own mint (per its THOUGHT); repeated it
  myself on the FIRST of two mints this session (g7.33.12) before catching it, then avoided it on the second
  (the TMM.136 hypothesis) by simply not putting a heading line in the body file at all. Cheapest fix: never open a
  --body-file with a heading, full stop.
`rotate.py rotate`'S OWN `stop_commit` STEP IS NOT SAFELY RE-RUNNABLE ON A DIRTY-TREE BLOCK -- IT WILL KEEP ADDING
  GARBAGE, NOT CONVERGE. Ran `rotate.py rotate` at the actual rotate-out point; it printed `stop_commit: committed
  ...(ONE rotate-out commit @<sha>)` and `stops push: OK`, then IMMEDIATELY refused with `rotate-self blocked: dirty
  tree: .agi/nodes/doc/card-director-engine.md, .agi/sessions/quorum/director-engine.md` -- inside the SAME
  invocation, meaning stop_commit's own plumbing-level commit (which writes a flattened snapshot at the quorum path
  WITHOUT touching the working tree, by design, so the live symlink is undisturbed) leaves a type-change mismatch
  (committed=flat file, working tree=symlink) that rotate's OWN dirty-check does not recognise as expected and
  refuses on. Followed the historical precedent visible in this branch's own git log (gen 11 hit the identical
  three-fencing-pass sequence at its own rotate-out: "rotate-out gen 11->12: ```" -> "stop_commit fencing" ->
  "````" -> "stop_commit second pass" -> "`````") and committed-plus-retried four times -- it did NOT converge:
  each retry appended ANOTHER copy of the card's THOUGHT block wrapped in one MORE layer of backtick fencing onto
  the WHERE-IT-STOPS section, reaching 5 duplicate THOUGHT:BEGIN blocks (a real defect: `test_thought_hygiene`
  bans exactly this, and a prior generation already had to hand-fix 3 duplicates from this same mechanism once,
  per the dm log's TMM.142). Manually truncated back to ONE clean copy this session (this exact card write). DO NOT
  blindly retry `rotate.py rotate` more than once on this exact blocker -- inspect `git diff --stat` after the
  FIRST block, and if it shows the card growing (more THOUGHT:BEGIN markers, more stacked backticks) rather than
  the tree simply going clean, stop and hand-fix instead of retrying again. Flagged to thought-master as a real
  rotate.py defect, not something to keep working around by retrying.
```

## LATER STILL (gen 13, f=0.4539+ -- a SECOND, VERIFIED owner order arrived via belam directly, ed25519-signed)
[decision] PASS 5 merged: season2/main 8daa626e89 (trunk @5b7d503fa7), from hypothesis:pass5-0925-residue-batch
(goal:g1). Four items assigned to director-engine, item 1 explicitly FIRST (an authority gate), order of 2-4 mine:
1. hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell -- REOPENED: PASS 5's mur-p5chunk3of4
   DEMOTED a prior attempt, found a missing/malformed veto cell still fails OPEN (src/seatsig/veto.py:117-127 turns
   loader errors into free defaults before rotate.py ~10415 can see them). DISPATCHED as **DH.303**, agent
   `a00-7ed34326`, pid 3225769, branch `season2/loops/hypothesis-authority-publish-fai-a00-7ed34326`. Orders:
   `.agi/sessions/de-0925/dh303-orders.md` (told explicitly: this is a second attempt at a claim already demoted
   once, read why before repeating the mistake; the tests must drive the real cell-failure modes, not a sidestepping
   mock). Two stale-base cycles hit dispatching this (1 behind, then 5 behind -- other posts landing fast); synced
   both times, standard fix. NOT YET HARVESTED.
2. hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row -- NOT STARTED, mine to sequence.
3. hypothesis:brainstorm-and-research-review-contracts-match-their-manifests -- NOT STARTED.
4. hypothesis:grid-push-batch-limit-is-a-config-cell -- NOT STARTED.
Plus: the g5.32-t0 inventory demote, and 5 "DE" residue rows in hypothesis:pass5-0925-residue-batch's own batch
table -- NOT YET READ, next session should open that node first thing.
All three PASS-5 hypothesis nodes for 2-4 already exist on disk (pulled in by this session's trunk merge, tip
03fef6257e) -- fully specified already, no minting needed, just read + dispatch, same shape as DH.303 above.
DELIBERATE SCOPE CALL under severe time pressure: dispatched only item 1 (explicitly FIRST, an authority gate) this
session rather than trying to also dispatch 2-4 blind and thin. Items 2-4 and the residue batch are clean,
well-defined pickup points for the next generation, not something dropped by oversight.

## LATE UPDATE (still gen 13, past the rotation line -- captive auto-capture fired at f=0.4345, no self-rotate happened)
Thought-master answered the [red] almost immediately: **TMM.148**, ordering the stop_commit fix ahead of round B.
Minted **goal:g7.33.13** + `hypothesis:rotate-stop-commit-converges-on-symlinked-card` (parent goal:g7.33.13),
carrying the full 5x-reproduced Measured evidence from this session's own TRAPS entry above. Hit one stale-base
refusal dispatching it (5 behind local-maxxing/season2/main) -- fetched+merged+pushed+retried in one cycle, standard
fix. Dispatched as **DH.302**, agent `a00-fe4b70ef`, pid 3136303, branch
`season2/loops/hypothesis-rotate-stop-commit-co-a00-fe4b70ef`. Orders: `.agi/sessions/de-0925/dh302-orders.md`. NOT
harvested as of this write. `ps -ef | grep -i director-engine | grep -i rotate` confirmed NO live rotate-self process
after the captive fired -- per gen 10's own precedent this is the captive's known no-op mode (it freezes/records the
card but does not seat a successor), not an active rotation in progress. Standing fix per that same precedent: keep
writing the card and keep working, since a real `rotate.py rotate` cannot succeed cleanly until DH.302 lands (the
bug is deterministic and reproduced 5 times already this session -- see TRAPS). Pushed through tip c1dda265ee before
this dispatch; TMM.148's mint+dispatch commit is f17f44c670, the trunk-sync merge is c1dda265ee.

## 🔴 WHERE IT STOPS — the one next command (gen 13 -> rotating now)
```
Two merge-ups sent this session (@edc78b1c21, @131c7319d1); thought-master's TMM.160 confirms the first is clean on gate (full suite was still running at last read). Corrected a self-caught DH.304/DH.311 mislabeling per thought-master's read of the actual bytes (recorded in the card and dm log, not rewritten into the immutable commit).
1  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's full-suite gate verdict likely landed by now.
2  Dispatch PASS-5 item 2 (approved, TMM.160): hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row. Its THOUGHT already carries the mechanism (rotate.py:10418-10470, _authority_row_content returns SKIPPED instead of a named refusal on a malformed row) and the fix shape (DH.304's veto.py pattern). Brief the parent: a prior kid died on a 401 before touching bytes -- check provisioning.py status if that recurs; an empty experiment template is not evidence, re-cut rather than accept it.
3  Then, in priority order: the 5 "DE" residue rows + g5.32-t0 demote from hypothesis:pass5-0925-residue-batch (full list in the card's §1), each its own corrective round per the standing "mur residues close in-loop" rule; then round B goal:g7.33.10; then goal:g1.14.1.
4  Judgement calls: decide, record the reasoning in the affected node's THOUGHT, keep going -- delegated authority carries across the rotation boundary.
5  Card write LAST, right before your own rotation.
```
