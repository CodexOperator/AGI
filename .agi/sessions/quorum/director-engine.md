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
Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine` on
`local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine`. Merge-ups go to
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

3. TMM.136 (parent's kid-spawn --orders path is ambiguous prose, not a real path) -- DISPATCHED, not harvested.
   Investigated the mechanism myself before minting: `brief.py:2074-2103` (`_orders_section`) renders a DIRECTOR's
   `--orders` bytes VERBATIM into a PARENT's brief with no path logic of its own, so an ambiguous phrase reaching a
   parent's own kid-spawn line has to originate in prose somewhere upstream. Best candidate found:
   `brief.py:1874-1888`, the parent's own carry-forward instruction, still teaches the DEPRECATED `--prompt-file
   <path|->` while `dispatch.py:1863`'s own runtime message already pushes every kid-tier caller toward `--orders`.
   Could NOT find the literal string "this worktree absolute path" anywhere in the tree by grep, so the hypothesis
   (`hypothesis:parent-orders-line-names-a-real-path-not-prose`, under goal:g7.33.9) names this as a well-evidenced
   CANDIDATE, honestly, and explicitly asks the dispatched parent to confirm against a live repro before committing
   to the fix -- not a claimed-proven root cause dressed up as one. Dispatched as **DH.299**, agent `a00-5497ee99`,
   pid 2428863, branch `season2/loops/hypothesis-parent-orders-line-na-a00-5497ee99`. Orders:
   `.agi/sessions/de-0925/dh299-orders.md`.

4. Round B, goal:g7.33.10 (write.py's set/create --set should be schema-checked) -- DISPATCHED, not harvested.
   goal:g7.33.10's own body already carried a near-complete brief (the owner's five-probe scratch-worktree
   measurement: an invented field, an out-of-regex goal_id/status, a non-float confidence, a title with no id prefix
   -- all admitted, exit 0). Transcribed it into the hypothesis schema shape almost directly, and ADDED my own
   fresh, first-hand repro from item 2 above (tags-as-string, missing seeds) as independent, same-session
   confirmation the gap is real and current. Pointed the parent at `links.py schema`'s existing loader/validator to
   reuse rather than reimplement. Dispatched as **DH.300**, agent `a00-d4088ba1`, pid 2446058, branch
   `season2/loops/hypothesis-write-py-set-is-schem-a00-d4088ba1`. Orders: `.agi/sessions/de-0925/dh300-orders.md`.

5. goal:g1.14.1's round (the owner's 00:37Z re-mint; hypothesis:a-round-stage-spawns-the-parent-and-chains-its-
   review-in-one-workflow) -- DISPATCHED, not harvested. The hypothesis was already fully specified from a prior
   session (Measured/Build/FALSIFIERS/TESTS/FILE SCOPE/CEILING, technical content Prime-verified against
   workflow.py/cli.py line numbers as of 09-24 21:4xZ) and its own THOUGHT flagged those citations needed
   re-verification since the tree had moved. Spot-checked before dispatch: cli.py:2387 matches exactly; the
   chained_from / prior-stage-return mechanism is confirmed real near workflow.py:2116; :1320 and :2315 only loosely
   checked. Told the parent to finish that verification itself and correct the node's citations if they've drifted
   further, rather than silently trusting a partial spot-check. Dispatched as **DH.301**, agent `a00-30d529ae`, pid
   2459647, branch `season2/loops/hypothesis-a-round-stage-spawns--a00-30d529ae`. Orders:
   `.agi/sessions/de-0925/dh301-orders.md`. Already spawned its first kid (`a00-fa4bba08`) by the time of this write.

All three rounds dispatched with genuinely DISJOINT file scopes (brief.py+tests / write.py+links.py+tests /
workflow.py+workflows/+tests) and told so explicitly in their own orders files, so running them in parallel matches
TMM.128's own precedent (round A + round B were explicitly pre-authorized as parallel exactly because their files
never overlap) rather than inventing a new practice.

Before dispatching: fetched + merged `local-maxxing/season2/main` (0b330293) into this branch, clean, no conflicts;
confirmed `pi-free` config invariant (grep -c count = 1) after the merge. Pushed twice this session (aebc4cb7f0 after
the node fixes, 7e36f5f27c after the trunk merge) -- `refs/agi/posts/director-engine` is current as of this write.

Nothing else from TMM.147 remains: all five items are done or in flight. No new work invented beyond what was
explicitly ordered -- the queue thought-master gave is now empty pending harvest.
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
  "real subprocess" finding -- four consecutive passes now flagged it; still not surfaced as its own `[red]` because
  no merge-up has gone out yet this session to carry it alongside.
- NEW this session: `grid.py commit --all` printed one pre-existing, unrelated error during this session's node
  commits: `experiment:a00-2a4dfb57-triage has no mint_id -- refusing to write a node-id-keyed ref for it. Run
  backfill-mint-ids.py --write first.` Not mine to fix (out of scope, not ordered, not blocking any of this
  session's own commits, which all versioned fine) -- flagging for whoever next runs a full `backfill-mint-ids.py`
  pass.

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
```

## 🔴 WHERE IT STOPS — the one next command (gen 13 -> rotating now)
`````
````
```
1  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's reply to
   [merge-up] #13 (tip 10cc524ac2), including whether they want a mur run before landing it, may already be waiting.
2  Dispatch a fresh round for DH.300's target, hypothesis:write-py-set-is-schema-checked (round B, g7.33.10) -- the
   hypothesis itself is unchanged and still accurate; write a sharper orders file this time stating explicitly that
   a measurement-only kid (production_lines=0) is not a finished round for this claim, since that is exactly what
   happened once already.
3  Dispatch a fresh round for hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
   (goal:g1.14.1) directly against the 3-seam plan now recorded in its THOUGHT (round execution ~120 lines, manifest
   composition ~60, harvest/config ~40) with an explicit raised ceiling (~220 lines) -- do not re-derive the scoping,
   it is already done.
4  If the inbox surfaces something needing a judgement call, decide it, record the reasoning in the affected node's
   THOUGHT (or here if there is no single node), and keep going -- delegated authority carries across the rotation
   boundary; bank only what is genuinely the owner's alone to decide.
5  Re-link check: `ls -la .agi/sessions/quorum/director-engine.md` on your FIRST substantive action -- it must show
   an `l...` symlink, not a plain file. This generation fixed it once; nothing prevents a future rotate's
   stop_commit from flattening it again, and if it is not re-linked THAT session, it goes stale for every session
   after until someone notices.
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 13's rotate-out. Cleared the entire TMM.147 queue this session: two THOUGHT-block fixes with sources verified
byte-for-byte (one pulled fuller from the primary transcript than the relay had it, one found nowhere in this post's
own transcript and honestly cited as a corroborated relay instead), one retroactive fixes-leaf goal minted with two
of my own mint-time bugs caught and fixed before committing, and three parents dispatched in parallel across
genuinely disjoint file scopes -- all three harvested before rotation: one real fix merged and independently
verified twice (DH.299/TMM.136), two that correctly delivered no code but real, recorded findings instead of a
forced or fabricated implementation (DH.300 measured the bug without fixing it; DH.301 scoped a 220-line/3-seam
decomposition rather than force a partial 40-line patch). [merge-up] #13 sent with an honestly disclosed deviation:
merged DH.299 on direct verification rather than a completed mur pass, because the rotation line was close. The
session also root-caused a real, previously-invisible infra bug the owner independently asked about mid-session:
this post's own card symlink had been flattened at gen 11's rotate-out and never re-linked by gen 12, silently
serving two-generations-stale content through the normal read path the whole time. Fixed and explained mechanically,
not just patched over, so the same failure is recognizable and fixable in one line if it recurs.
<!-- THOUGHT:END -->
````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 13's rotate-out. Cleared the entire TMM.147 queue this session: two THOUGHT-block fixes with sources verified
byte-for-byte (one pulled fuller from the primary transcript than the relay had it, one found nowhere in this post's
own transcript and honestly cited as a corroborated relay instead), one retroactive fixes-leaf goal minted with two
of my own mint-time bugs caught and fixed before committing, and three parents dispatched in parallel across
genuinely disjoint file scopes -- all three harvested before rotation: one real fix merged and independently
verified twice (DH.299/TMM.136), two that correctly delivered no code but real, recorded findings instead of a
forced or fabricated implementation (DH.300 measured the bug without fixing it; DH.301 scoped a 220-line/3-seam
decomposition rather than force a partial 40-line patch). [merge-up] #13 sent with an honestly disclosed deviation:
merged DH.299 on direct verification rather than a completed mur pass, because the rotation line was close. The
session also root-caused a real, previously-invisible infra bug the owner independently asked about mid-session:
this post's own card symlink had been flattened at gen 11's rotate-out and never re-linked by gen 12, silently
serving two-generations-stale content through the normal read path the whole time. Fixed and explained mechanically,
not just patched over, so the same failure is recognizable and fixable in one line if it recurs.
<!-- THOUGHT:END -->
`````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 13's rotate-out. Cleared the entire TMM.147 queue this session: two THOUGHT-block fixes with sources verified
byte-for-byte (one pulled fuller from the primary transcript than the relay had it, one found nowhere in this post's
own transcript and honestly cited as a corroborated relay instead), one retroactive fixes-leaf goal minted with two
of my own mint-time bugs caught and fixed before committing, and three parents dispatched in parallel across
genuinely disjoint file scopes -- all three harvested before rotation: one real fix merged and independently
verified twice (DH.299/TMM.136), two that correctly delivered no code but real, recorded findings instead of a
forced or fabricated implementation (DH.300 measured the bug without fixing it; DH.301 scoped a 220-line/3-seam
decomposition rather than force a partial 40-line patch). [merge-up] #13 sent with an honestly disclosed deviation:
merged DH.299 on direct verification rather than a completed mur pass, because the rotation line was close. The
session also root-caused a real, previously-invisible infra bug the owner independently asked about mid-session:
this post's own card symlink had been flattened at gen 11's rotate-out and never re-linked by gen 12, silently
serving two-generations-stale content through the normal read path the whole time. Fixed and explained mechanically,
not just patched over, so the same failure is recognizable and fixable in one line if it recurs.
<!-- THOUGHT:END -->
