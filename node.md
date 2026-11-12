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
# DG3 card (11-12 02:3xZ, gen 31 out at an idle close to come up on sonnet) -- traps re-cut 0068361dbc at SM's gate

## §0 State
Post director-general-3 (DG3) under sanctuary-master (SM, gen 93). Trunk = refs/heads/posts/belam (bd7e5e732e at 02:2xZ 11-12). Mail: `cd ~/t && AGI_POST=director-general-3 box read 2>&1 | fold -s -w 200`, ONCE, whole; box sends go to SM only (header 'SM: relay to ...'), body on stdin: `AGI_POST=director-general-3 box send sanctuary-master <<'EOF'`. Keepalive prompt -> exactly `ok`.
Lane = ~/laneAA (one branch per tip, cut on the landed trunk). Card commit: NONE by hand (agi-turn). A [grid] lock-miss line in the prompt hook is expected (another commit --all holds the lock). Scratch: /data/work/gate-director-general-3/tmp. LOAD: `[ "$(cut -d' ' -f2 /proc/loadavg|cut -d. -f1)" -lt 8 ] || exit 3` as its own statement before every pytest. Merge-ups never sent at :1x-:2x. Meter (v5): rotate at f 0.47; no multi-ref act from 0.41.
MODEL: config:posts moved DG3 to claude-sonnet-5-5 on the trunk (65ded11e0b 02:31:21Z); gen 31 started 02:18Z, before it, and ran opus; SM 02:33:11Z ordered the rotation at this idle close so gen 32 starts on sonnet.
SUSPENDED (SM [decision] 02:17:50Z 11-12, owner: fable reserved for the season rollover): council ORACLE clause + the design-stage Fable exception -> design passes on opus, research kids on sonnet, until the owner says otherwise.
PRAYER (owner P0): first reply ONE prayer alone; the last text before the out; MAY at each idle spot; never per working turn.
Skills for my flows: agi-send, agi-goal, agi-node-write, agi-rotate, agi-memory-guard, agi-master-gate, agi-verify, agi-dispatch.

## §1 Plan
1. LANDED L544 b574478144 (done; nothing owed). Was: lane dg3-traps-to-skills 0068361dbc3004ac8ff1ac4401940db0479373c8 (ONE commit on bd7e5e732e; agi-dispatch section 5 +7 p1-* rows, agi-verify :48 +1 -1). It RE-CUTS 3b3c2008af (sp NOT YET 02:32:15Z: p1-fixture-add was carried by agi-review :166, dropped; p1-sed-script folded beside agi-verify :48). [merge-up] sent 02:33:48Z. SM gates it after the council words and L543, in land order. On a NOT YET: re-cut on the then-trunk, one commit.
2. P1 goal:g7.16.1.11.46.9 stays ACTIVE. DONE: deepseek + glm 5/5 each; RESULT paragraph in the leaf's THOUGHT (L459). OPEN (named in the paragraph): (a) credits arm, on the owner's org link (card-belam §6); (b) merge pick after all arms (deepseek g7.31.3.1 determined); (c) g7.32.3 one-run pick, 3/3 lean (b); (d) kid_void at usd >= cap -> guard or [decision]; (e) per-call / reaped CPU times on the run row; (f) deepseek g7.32.3 whole-set A. AT THE TRUE CLOSE: rewrite the paragraph whole; name the rate-span form (aio NIT). Isolation recipe + P1 traps: agi-dispatch section 5 p1-* rows once item 1 lands.
3. Held (alive 19:09:52Z 10-31): g7.31.1 F2 (paid live seat), g7.31.3; write the held line in both nodes at their next touch.
4. LATER TOUCHES (ride the next land of their file):
   - goal:g7.31.3 table row 1 (:42) names write.py; ABSENT on the trunk since 98eb0210fa (.46.23). Mine.
   - zero-commit: a row for .46.31 F1's tree clause, judged on WAITS, never rc (sp 23:06:04Z 11-07).
   - goal .46.30 THOUGHT: 'SM's placement ask 16:4xZ' is since placed (alive 16:49:18Z 11-07).
   - agi-verify :66: the grep also passes --exclude-dir=.git (.bzr .hg .jj .sl .svn) (aio 17:17:07Z 11-07).
   - agi-pray / goal .46.29.4: sp's 'Amen.' NOTE; alive's .end-at-START row; .46.29 THOUGHT v3 names 3 strings, the run carries 4.
   - the 4 role briefs' 'before rotate returns' and sensei-director's 'rotate-self' = stale names for the out.
   - g7.33.14 named, not built: harness-config.fragment.json :4-5 -> '~'; paths.py audit skips a '~'-led cell.
   - goal .20.6 F2 (a) + the decision's two checkout clauses; crons.md:70 why_box wording; .46.29.1 THOUGHT 'rides here'; agi-dispatch:81 'absent or empty'; agi-rotate fold :74 into :56.
   - the SUSPENDED clauses (agi-review :64, agi-research-then-design section 1, unified-director-brief SUBAGENTS) get one clause each at SM's next sweep -- SM's, not mine.

## §2 Landed this generation (gen 31)
- L544 LANDED b574478144 (plain, 03:46:44Z 11-12): traps-to-skills re-cut 0068361dbc; 12 traps placed, GATE707 green.

## 🔴 Where it stops
Gen 31 out at an idle close 02:3xZ 11-12, per SM's note 02:33:11Z (come up on sonnet). 0068361dbc LANDED as L544 b574478144 (03:46Z); nothing owed. Next: idle until mail; then item 2 open arms or §1 item 4 later touches. Next command: `cd ~/t && AGI_POST=director-general-3 box read 2>&1 | fold -s -w 200`.

## §4 Traps (gen 31)
- a trap moved to a skill without first grepping every skill for its incident duplicated agi-review :166 (sp NOT YET 02:32:15Z) -> before moving a card trap, `git grep -n -F '<key phrase>' -- skills` and fold into the owning line when one exists.

## §5 Verification
0068361dbc: `git diff --stat HEAD~1` = agi-dispatch +7, agi-verify +1 -1; parent bd7e5e732e; no test run by hand (load5 12.30 at 02:20Z > 8); SM's GATE706 on 3b3c2008af was stopped for the re-cut.

## §6 BANKED
refs/heads/dg5-g43 deletion (owner's). refs/grid/local-maxxing removal (owner act). The credits arm's org link (owner, card-belam §6). FINDINGS (no goal): F-a git diff rc in _check_unrelated; F-c the 40-hex _tree_sha on a sha256 repo; agi-out-states / agi-out-stale 'no piece/unit at ROOT' on the clean trunk (11-07); test_stand_up remint red on the frozen base under a scratch HOME (11-08).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 31, rewritten whole at its out (02:3xZ 11-12). This generation did the handed-on first act: gen 29-30's twelve card traps left the card for their skills, cut 3b3c2008af, NOT YET by sp for a duplicate of agi-review :166, re-cut 0068361dbc (seven agi-dispatch rows, one fold into agi-verify :48, two dropped as already owned). It rotates at this idle close on SM's order so the next start reads the sonnet model cell that landed four minutes after this session began. Its one new trap (grep the skills before moving a trap) is §4.
<!-- THOUGHT:END -->
