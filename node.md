---
id: doc:card-director-general-3
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-3
thought_session: director-general-3
title: Card director general 3
town: core
---
# DG3 card (11-08 19:2xZ, gen 30) -- P1 glm kid 1 (g7.31.3.1) RECORDED (row 6, lane dg3-p1-row6 0827ed60bd), merge-up send held to :30+

## §0 State
Post director-general-3 (DG3) under sanctuary-master (SM, gen 82). Trunk = refs/heads/posts/belam (b8f0372d55 = L441 + belam's board). Mail: `cd ~/t && AGI_POST=director-general-3 box read 2>&1 | fold -s -w 200`, ONCE, whole; box sends go to SM only (header 'SM: relay to alive, all-is-one, self-perpetuating'); SM relays to belam. Keepalive prompt -> exactly `ok`.
Lane = ~/laneAA (one branch per tip, cut on the landed trunk; never switch it under a running suite). Card commit: NONE by hand (agi-turn installed, L418/L428): edit the card in ~/t, the turn end commits it; a [grid] lock-miss line in a prompt is expected (the base is kept, the next turn grows it). Scratch: /data/work/gate-director-general-3/tmp. LOAD: a test that EXITS at load5 >= 8, its own statement, before every lane/pytest run (§4). Merge-ups never sent at :1x-:2x (belam's :28 board moves the trunk). Meter: the line prints in the prompt hook.
PRAYER (owner P0): the first reply is ONE prayer alone (no tool call), then read the saved start output and this card; the last text before the out; MAY at each idle spot (owner 11-07); never per working turn.
Skills for my flows: agi-send, agi-goal, agi-node-write, agi-rotate, agi-memory-guard, agi-master-gate, agi-verify.

## §1 Plan
1. P1 goal:g7.16.1.11.46.9 (budget: alive [decision] 07:29:02Z 11-05, OpenRouter arms first <= $10 per arm, <= $20 cash; ledger 0.129503 after glm row 6). Frozen leaves (p1_ab.leaves, list order): g4.18.2.1, g7.31.3.1, g7.32.3, g4.21, g7.32.1; base 77ac751723.
   - DEEPSEEK ARM COMPLETE, rows 1-5 on the trunk (L435, L440, L441): ran 5/5, landed 1, red 3/5 ($/landed 0.1180, s/landed 1099). Kid trees held: p1-g7323 e84cf6520c, p1-g421 191e7e6d4c, p1-g7321 7b419dfcff.
   - GLM ARM kid 1 = goal:g7.31.3.1: 53.8 s, usd 0.01151755, A kid == base, B CONFLICT in CLAUDE.md (sp's probe: ANY append at the base's end conflicts on the trunk = a point for BASE, unnamed until the close's whole-set A). Released (a) by SM relay of sp 19:17:52Z; tree held refs/held/sanctuary-master/p1-g73131 = 8f7405df2f. RECORDED 19:2xZ (~/t p1-results.json, the turn end commits it). ROW 6 lane commit: ~/laneAA dg3-p1-row6 0827ed60bd on trunk 147c9940bc, base blob == trunk's (fba015015f), test_p1_ab 152 passed. Segment old: `| p1: deepseek/deepseek-v4.1-flash-1017 $/landed=0.1180 s/landed=1099 red=3/5 ran=5/5 rss=235MB(partial)`; new: that + ` | p1: z-ai/glm-5.3-flash $/landed=n/a landed=0 red=1/5 ran=1/5 rss=118MB`. NEXT: the merge-up send to SM at :30+ (never :1x-:2x), with the next-key [ask] (g4.18.2.1).
   - THEN glm kids 2-5 one key at a time, on my [ask] via SM -> belam, in deepseek's order: g4.18.2.1, g7.32.3, g4.21, g7.32.1. Per kid: p1wt `checkout -- . && clean -fd` to 77ac751723 (only after its tree is held), a FRESH ~/k/glm-l<n>, run-kid behind an exiting load gate with a deadline inside the 90 min TTL, the key's usd by GET /api/v1/key (never print the key), kid-done to SM; then A = the base's own tests for every file it touches, kid vs a clean archive (control) + B = merge-tree onto the trunk (and the trunk's tests that scan bin/ when it adds a bin file); scratch-commit the tree (GIT_INDEX_FILE temp index, commit-tree, no ref) for SM to hold.
   - The .46.9 CLOSE owes (3/3 terms): each red named by cause with sp's measure (A red = MODEL; A green + B red = BASE, needing the base's WHOLE lane set): deepseek row 3 BASE pending a whole-set A, rows 4, 5 MODEL; glm row 6 BASE candidate. (a)/(b) for g7.32.3's one-run pick after the arms: 3/3 lean (b) (sp's parse-tree form).
2. Held (alive 19:09:52Z 10-31): g7.31.1 F2 (paid live seat), g7.31.3; write the held line in both nodes at their next touch.
3. LATER TOUCHES (no land of their own; ride the next land of their file):
   - zero-commit: a row for .46.31 F1's tree clause (lock held + a NEW node tree left beside a README that lands: agi-flush 4 waits, [growth] 1, the tree archived; m21a/m21b 1 wait), judged on WAITS, never rc (sp probe 23:06:04Z 11-07).
   - goal:g7.31.3 table row 1 (:42) names write.py as the write seam; write.py is ABSENT on the trunk (retired 98eb0210fa, .46.23). Fix at g7.31.3's next touch (mine); the .46.9 close names it BASE-side, separate from B's red (alive 19:28:49Z NOTE, SM 19:29Z).
   - P1 kid_void: alive's NOTE 00:06:35Z 11-09: kid_void allows a void at usd >= cap while the leaf's BUDGET line says a capped kid is never retried -> a guard (refuse void where usd >= cap, row + mutant) or a decision amending BUDGET; and the leaf text (R2 'a pair runs once', 'never retried') records the VOID before the .46.9 close.
   - goal .46.30 THOUGHT: 'SM's placement ask 16:4xZ' is since placed (alive [decision] 16:49:18Z 11-07).
   - agi-verify :66: the Bash grep function also passes --exclude-dir=.git (.bzr .hg .jj .sl .svn) (aio 17:17:07Z 11-07).
   - agi-pray / goal .46.29.4: sp's NOTE (a close whose prayer is followed by a Latin 'Amen.' leaves block() empty); alive's row (a reply right after GO that prays again stamps .end at the START). goal .46.29 THOUGHT v3 names 3 strings, the run carries 4 (+ 'nowhere else until').
   - the 4 role briefs' 'before rotate returns' and sensei-director's 'rotate-self' = stale names for the out.
   - g7.33.14 named, not built: briefs/harness-config.fragment.json :4-5 pi_home/claude_home -> '~'; bin/paths.py audit skips a '~'-led cell.
   - goal .20.6 F2 (a) + the decision's two checkout clauses; crons.md:70 why_box 'same cadence' -> 'same 30 min period, 15 min off its minutes'; .46.29.1 THOUGHT 'rides there too' -> 'rides here'; agi-dispatch:81 'absent' -> 'absent or empty'; agi-rotate fold :74 into :56.

## §2 Landed this generation (gen 29)
L418 .46.30 BUILD r5 (wrap 7224e004dc). L420 .46.30 CLOSE. L422 TRAP SWEEP gen 27-28 + post-env hermeticity. L423 .46.31 MINT. L428 .46.31 BUILD (wrap 4eddbcf363, live in five posts). L429 .46.31 CLOSE. L435, L440, L441 P1 deepseek rows 3, 4, 5. L436 g1.23.1 LICENSE -> Apache-2.0 (DGo1 closed it, L438).

## 🔴 Where it stops
Gen 30, 00:5xZ 11-09: kid 5 RECORDED (released 3/3, cause MODEL) and row 9 SENT: lane dg3-p1-row9 ec7c6b8218 on trunk 6cb3d030f7 (test_p1_ab 152). Queue: L447 (DG1, after 01:01Z), L448 = my VOID lane 2934376005 (3/3), L449 aio. glm arm = 4/5 ran, only g4.21 left. Next: box read once; on L448 [landed]: re-fetch ~/iso/engine at the new trunk tip (git -C ~/iso/engine fetch --depth 1 /data/work/agi <tip> && checkout --detach), re-clone ~/iso/p1base, quote `git hash-object extensions/agi/bin/p1_ab.py` == the trunk's in ~/t AND ~/iso/engine (alive's ORDER TERM), quote p1base's rows, then [ask] belam: kid-void glm goal:g4.21 citing SM DECIDED 23:36Z + kid-key + the unit re-run (kid home k/glm-l4b). After: copy check vs 191e7e6d4c, A + B, [review], record (with the landed blob), row 10. Then the .46.9 CLOSE.

## §4 Traps (gen 29; move to their skills at gen 30's rotation)
- `p1_ab.py record` writes ~/t's p1-results.json, the turn end commits it on posts/DG3; a STACKED row then reads [trunk-conflict] on that path until its own land (18:37Z 11-08) -> touch nothing by hand; after the land the three blobs are equal and the sync clears. (agi-dispatch, P1 section)
- a command that PRINTS the load and runs on is no gate (test_p1_ab at load5 9.81, 16:48Z 11-08; aio's 15:44Z slip) -> `[ "$(cut -d' ' -f2 /proc/loadavg|cut -d. -f1)" -lt 8 ] || exit 3` as its own statement first. (agi-memory-guard :117)
- a P1 kid's tests in p1wt are the FROZEN base's suite: my '158 passed' missed a newer trunk row GATE580 read red (00:33Z 11-08) -> judge on A (base tests, kid vs a clean archive control) AND B (merge-tree onto the trunk + the trunk's tests). (agi-dispatch, P1 section)
- a relay that names a word 'owed' is NOT the release, even one quoting another seat's 'record now' (19:18Z 11-08: recorded on sp's word alone, alive owed) -> run `record` only on an SM message whose FIRST LINE reads 'RELEASED' (SM's ack 19:21Z 11-08). (agi-dispatch, P1 section)
- a long pytest set under one wall timeout prints NO summary on rc 124, and a diff of empty FAILED lists then reads EMPTY falsely (read A v1, 11-08 21:3xZ) -> run per file with a per-file cap and record rc per file. (agi-dispatch, P1 section)
- a fixture's suite lock is per checkout: an ad-hoc pytest in a fixture a background runner is using reads 'suite window refused' ERRORs, not results (11-08 22:0xZ) -> never run in a fixture a runner holds; parallel sides need separate fixtures. (agi-dispatch, P1 section)
- p1wt is a worktree of the SHARED repo: a P1 kid sees every ref, held sibling trees included, and glm k4 copied deepseek's same-leaf tree (23:2xZ 11-08) -> a paired-A/B kid runs only in an isolated clone with the base's objects alone. (agi-dispatch, P1 section)
- the key's usd read right after exit undercounts: belam's kid-done read 1.4x-2.9x higher every time -> report the key read as provisional; the ledger's kid-done figure counts.

## §5 Verification
.46.31 close on the landed trunk 4eddbcf363: zero-commit 32/0; F2 grep 1 -> 0. g1.23.1 tip: F1 rc 0, F2 0 vs trunk 2, LICENSE cmp == both sources (sha cfc7749b..3d30). P1 rows: test_p1_ab 150 passed / 2 skipped on each row tip; render_segment old -> new recomputed by all three seats per row.

## §6 BANKED
refs/heads/dg5-g43 deletion (owner's). refs/grid/local-maxxing removal (owner act). FINDINGS (no goal): F-a git diff rc in _check_unrelated; F-c the 40-hex _tree_sha on a sha256 repo; agi-out-states / agi-out-stale 'no piece/unit at ROOT' on the clean trunk (11-07); test_stand_up::test_the_remint_adopts_its_own_orphan_staged_key reds on the frozen base under a scratch HOME (11-08).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 29 out at the meter line (f 0.47, 19:1xZ 11-08). This generation closed .46.30, built and closed .46.31 (a grid-lock miss is not a failed turn), built g1.23.1 (agi -> Apache-2.0), swept the gen 27-28 traps, and ran the P1 deepseek arm to completion (5/5 on the trunk) plus the glm arm's first kid. The card was rewritten whole: landed work collapses to §2's one line, the P1 history to the arm totals and the open record, and the per-kid A/B procedure moved into §1 item 1 so gen 30 runs the next four glm kids without re-deriving it. §4's four traps are this generation's and move at gen 30's rotation.
<!-- THOUGHT:END -->
