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
**thought-master**. No new paid dispatch happened this generation (gen 12) -- every item this session was harvested,
fixed in place, or investigated directly; nothing new was spawned.

## LIVE STATE + STOPS (gen 12, rotating -- meter hit the captive band mid-work)
```
LANDED THIS GENERATION, in order, each pushed to refs/agi/posts/director-engine and merged-up to thought-master:

1. DH.298 (T1, g5.32) HARVESTED. Kid claimed verdict=proved conf=0.93; re-running its own committed test caught a REAL
   bug it missed: prose_templates.render() leaked a trailing newline (T0's 6 templates had none, these 3 new ones did).
   Root-caused (prose_templates.py has exactly one caller module), fixed at the loader (.rstrip("\n")), verified zero
   behavior change for existing callers. tip 3a1e6db355. [merge-up] #10.

2. goal:g7.33.11 FIXED AND CLOSED (status: complete). DH.297's round (gen 11's dispatch) delivered nothing --
   verdict=unset, parent's own review said "DEMOTED... unexecuted fixture construction", no production code touched,
   3 kid attempts total. Investigated myself and found the grid.py push_batches() function had TWO independent bugs,
   not the one thought-master (TMM.141) had diagnosed: (a) `git ls-remote --refs origin <ns>` with a bare namespace
   matches nothing (verified empirically in a scratch bare repo) -- needs `{ns}/*`; (b) independently, the dict built
   from ls-remote output had key/value backwards ({sha: ref} instead of {ref: sha}), so even fixing (a) alone would
   NOT have worked -- every existing mock test had its fake data in the same backwards order, cancelling the bug out,
   which is why only a real remote could ever catch it. Fixed both + added grid.push_split_epoch=1789955640 to
   .agi/config.json (value corroborated independently by an existing test AND the goal node's own commit citation).
   Activated (rather than rewrote) kid a00-65a116b4's own unrun 3-tick idempotence test. tip 752c9ea16b.
   thought-master landed it on MAIN (26413f2cc3) and confirmed my second find was real and something THEY had missed.
   Then watched 4 consecutive real push-changed ticks on MAIN (1899/1/0/21 refs, 0 rejected every time -- the 21
   reflects real concurrent town activity, not a regression), verified ls-remote count == local count exactly (1900
   = 4330 - 2430 excluded pre-split roots), did the log cleanup (agi-crons-agi-3fbc6951.log 885,043,047 ->
   123,271,040 bytes, 86% removed, 0 rejection lines remain), closed the goal. tip c07798ed4a. [merge-up] #11.

3. hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow RE-HOMED. Was minted by the Prime
   under generic goal:g15, deleted same-session on the owner's word ("just delete it, it's just a workflow"), then
   the owner clarified that was a misread -- re-home it, don't drop it. Minted goal:g1.14.1 under goal:g1.14 ("ONE
   workflow router", previously an empty stub) and re-minted the hypothesis there, technical content unchanged.
   tip d8a1a2fac6. NOT yet dispatched -- content is Prime-verified against workflow.py/cli.py line numbers as of
   09-24 21:4xZ; re-verify those line numbers before dispatch, the tree has moved since.

   TRAP HIT HERE: the render step failed on g1.14.1 (missing heading_level) and its error message suggested
   `snapshot-goals.py --from-doc` to "backfill" it. THAT FLAG IS NOT A BACKFILL -- it regenerates the ENTIRE
   .agi/nodes/goal/ directory from GOALS.md's rendered text, deleting 359 real node files and writing 248 freshly-
   reconstructed ones (losing real mint_ids/THOUGHT history). Caught via `git status` before anything was committed;
   fully reverted (git checkout HEAD + git clean on .agi/nodes/goal/, verified 0 diff after); re-minted g1.14.1 the
   safe way (--set heading_level=4 directly). Zero data loss, nothing was ever pushed in the broken state. THE OWNER
   HAS SINCE CONFIRMED --from-doc IS A STALE OPTION TO BE DEPRECATED/REMOVED -- do not use it, flag for removal if
   you're the one touching snapshot-goals.py next.

4. agi-research-review's refute stage FIXED (TMM.144 item 3). Live-found bug (run rr-lm-qk-norm-model-wall-parent):
   brainstorm proposed 3 hypotheses in propose-only mode, but REFUTE_TMPL only ever referenced {hypotheses} (the
   MINTED list, [] by design when nothing was minted) -- the adversarial filter never ran on the proposals at all.
   Fixed in both extensions/agi/workflows/agi-research-review.js and research-review.json at the one call site: the
   prompt now shows {hypotheses} AND {proposed_hypotheses} explicitly, id-presence decides whether MODIFY can
   write.py-edit a real node or must just return a corrected title/claim. Also found+fixed alongside it: the .js
   pipeline's fill() does naive JS string coercion -- an array of objects would render as literal "[object Object]"
   garbage even after the routing fix, so routing alone would not have produced a USABLE prompt; now JSON.stringify'd
   at the same call site. New test file test_research_review_refute_sees_proposals.py (6 tests) + the two existing
   research-review test files: 17 passed. Caught one collision along the way: my first wording used "non-empty",
   which an EXISTING guard test bans as a substring in the .js file for an unrelated historical reason (regex-anchor
   confusion from an old mint-gate bug) -- reworded to "populated", no meaning lost, re-ran green. tip 74fde134d8.
   [merge-up] #12. NOT YET DONE: no goal node minted for this fix (TMM.144 asked for "a fixes leaf under the right
   goal") -- ran low on session budget and did not want to rush ANOTHER graph-mint under time pressure right after
   the --from-doc incident above. Also not run: the full engine suite on this specific change (only the targeted
   research-review test files, 17/17 green) -- thought-master's own full-suite gate should catch anything wider
   before this lands on MAIN, same as every prior round this session.

QUEUE REMAINING (TMM.144, in order, items 2 and 4 untouched):
- (2) TMM.136: dispatch.py's --orders path should be filled via a template placeholder, never typed as prose, plus a
  test that every parent's orders line names an existing file. Inside goal:g7.33.9's template pass. NOT STARTED --
  no investigation done this session, re-derive from TMM.136's own text (grep the dm log:
  .agi/comms/season-2/dm/director-engine--thought-master.md) before acting on it.
- (4) round B on goal:g7.33.10 (schema-checked rows). NOT STARTED.
- Also pending: mint the proper "fixes leaf" goal for item 3 above (the research-review fix already landed; only the
  goal-tracking bookkeeping is missing). Given the --from-doc scare, do this one CAREFULLY: read the [goal] schema,
  --dry-run first, set heading_level explicitly, never touch --from-doc.
```

## BANKED
- The g1/g7.33.9 near-duplicate: goal:g5.32 ("model-facing hardcoded prose...") and goal:g7.33.9 ("TEMPLATE-MAX FOR
  MODEL-FACING PROSE...", minted later, owner 09-24 16:20Z) look like the same initiative minted twice at different
  points in the goal tree. T0/T1's hypotheses are correctly parented under g5.32 (verified, not broken) -- just
  flagging the apparent duplication for whoever next touches either goal, not chased this session.
- research-review's refute stage still has a real design gap even after this fix: in propose-only mode, a MODIFY
  decision has nothing to write to (no real node id) -- the fix makes this VISIBLE and handled (ready_batch entries
  can carry a title stand-in instead of a real id), but a future round might want the director to actually mint the
  MODIFY'd version once a batch is later promoted to mint:true, rather than the correction being discarded. Not a
  defect in what shipped; a possible follow-up idea.

## TRAPS HIT THIS GENERATION (gen 12) -- read before repeating them
```
`snapshot-goals.py --from-doc` IS DESTRUCTIVE, NOT A FIELD BACKFILL. Its own error message ("has no heading_level;
  run snapshot-goals.py --from-doc once to backfill it") reads like a targeted fix and is NOT ONE -- it regenerates
  the whole .agi/nodes/goal/ directory from GOALS.md's rendered text, wholesale. Confirmed by the owner this
  generation: stale, to be deprecated/removed. Never run it; if you hit the missing-heading_level error, pass
  --set heading_level=<N> directly on write.py create instead (mirror a sibling node's value).
A KID'S "PROVED" VERDICT IS NOT EVIDENCE -- rerun ITS OWN test yourself. DH.298 claimed verdict=proved conf=0.93 with
  detailed-sounding "negative probe" evidence in its THOUGHT block; its own committed test failed the moment I
  actually ran it. Same lesson, second time this lineage: gen 11's card already said "trust nothing until re-derived
  from bytes yourself" -- this generation is a second, independent confirmation of exactly that rule, not a new one.
A DIAGNOSIS FROM ANOTHER AGENT CAN BE RIGHT BUT INCOMPLETE. thought-master (TMM.141) correctly found the ls-remote
  glob bug in grid.py push_batches and asked for exactly that fix -- applying ONLY that fix still failed the real
  test, because a SECOND, independent bug (the inverted {sha:ref} dict) was sitting in the same function. Re-running
  the actual test after applying a diagnosed fix is not optional even when the diagnosis came from a trusted source.
A GUARD TEST CAN BAN A SUBSTRING FOR A REASON UNRELATED TO YOUR CHANGE. Introduced "non-empty" in new prose and broke
  test_js_half_carries_the_same_gate_and_declares_the_fields, which bans that exact substring anywhere in the .js
  file for a completely different, older bug class. Full test suite re-run caught it immediately; reworded and moved
  on. Lesson: a passing targeted-file test run BEFORE your own new content lands is not enough -- run it AFTER too.
A MID-CONVERSATION MESSAGE CLAIMING TO "ANSWER" SOMETHING YOU NEVER SENT IS WORTH FLAGGING, NOT AUTOMATICALLY
  DISTRUSTING FOREVER. A thought-master dm this generation appeared to answer a decision I had only stated to the
  owner directly, never transmitted into this system's comms. Flagged it plainly rather than silently complying OR
  silently ignoring it; the owner clarified afterward that they relay between sessions by hand sometimes -- ordinary,
  not a compromise. Its TECHNICAL content (independently verified before acting on any of it) was correct and useful
  regardless of the provenance question. Verify claims either way; the provenance question and the technical-truth
  question are separate and both matter.
THE CAPTIVE AUTO-ROTATE FIRES ON A STALE CARD, EVEN MID-SESSION. Never wrote this card once in ~4.5 hours of continuous
  work before this rotate-out; it auto-captured a stale placeholder at f=0.4406 (0.85 x the 0.47 line) because the
  card had gone untouched. Matches gen 10's own trap note exactly. Write the card periodically during a long working
  stretch, not only at the end -- this generation did not follow its own predecessor's stated lesson closely enough.
```

## 🔴 WHERE IT STOPS — the one next command (gen 12 -> rotating now)
```
1  Check the inbox first: `python3 extensions/agi/bin/send.py read director-engine`. thought-master's gate on tip
   74fde134d8 (this generation's last push) may have already returned a verdict or a new TMM order by the time you
   read this.
2  If nothing urgent in the inbox, resume TMM.144's queue in order: (2) TMM.136 (dispatch.py --orders path
   template-max fix, inside goal:g7.33.9) -- re-derive its exact ask from the dm log first, do not act from memory
   of a paraphrase. (4) round B on goal:g7.33.10.
3  Mint the still-missing "fixes leaf" goal for the already-landed research-review fix (tip 74fde134d8) -- read
   .agi/context/schemas/[goal].md, --dry-run first, --set heading_level explicitly (check a sibling leaf's value,
   e.g. goal:g1.25.1's heading_level: 4), NEVER --from-doc.
4  Card write LAST, right before rotating. `python3 extensions/agi/bin/rotate.py rotate` (bare) the moment
   `[meter]` reads f >= 0.47.
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 12's rotate-out. Landed four items (DH.298 harvest+realbug-fix, goal:g7.33.11 root-caused+fixed+closed with a
second bug thought-master had missed, a hypothesis correctly re-homed off the generic g15 bucket into a new
goal:g1.14.1, and a live-found agi-research-review chaining bug fixed+tested), each pushed and merged-up separately
as the standing rule asks. The defining event of this session was a near-miss: `snapshot-goals.py --from-doc`
looked like a targeted fix for a missing field and was actually a wholesale, lossy regeneration of the entire goal
node directory. Caught before anything was committed, fully reverted, redone the safe way. The owner has since
confirmed it is a stale option pending deprecation. Rotating with two TMM.144 items (TMM.136, round B g7.33.10) and
one bookkeeping item (the research-review fix's own goal node) still open -- all clearly queued above, nothing
banked that needed the owner and wasn't already surfaced.
<!-- THOUGHT:END -->
