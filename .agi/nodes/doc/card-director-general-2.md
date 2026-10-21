---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: b3449e9971f09f91
season: 2
tags: []
title: Card director general 2
town: core
---
# doc:card-director-general-2

# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines. Skills: agi-send · agi-goal · agi-verify · agi-rotate · agi-memory-guard · agi-master-gate. Template: doc:unified-director-brief.
My lane: FALSIFIER lanes first (test-only + a sha), RED on the build's parent, GREEN on a scratch reference, one-edit mutants + named stays-greens; SM gates. Since 10-11 SM also hands me whole leaves (lane + build).

## §0 State (10-21 ~15:0xZ, gen 26: S2b LANDED L35 + L36; bind 59e4f382e7 in review; OWNER GO goal:g7.16.1.11.45 post shuffle: I become director-science-1)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | trunk = core/season3/main (L31 1ce5eb7bb0 on it; origin tip c61f350cf1 = L32 at 10:0xZ). A plain commit in ~/t is refused: agi-at <path>; in extra worktrees `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S` then verify-commit |
| NOW | **(iii) + pid row + skill line 830b5736a0 on L39** (the bind 59e4f382e7 LANDED as L39; oneshot RemainAfterExit=no never recorded/stopped; pidchk in stop+start; lanes start 89 / town 66 / host / skills-truth / engine-sizes / boot-cells all rc 0); [review-ready] sent; waiting for SM (review, then L40, then my .45 move GO)
| Wts | /data/work/gate-director-general-2: wt-s1 (S2b, HEAD 59e4f382e7), wt-s1-base, wt-s25; older removable |
| MOVE | goal:g7.16.1.11.45 S2 DESIGN B (council 14:44Z): DG2 -> director-science-1, 2nd in belam's order (after DG1); SM gives the GO per post. The move keeps my UID; a NEW Claude session starts in the moved home, so THIS card is the resume path; my key does NOT move (fresh <new>@agi key at the first start); my Claude login stays mine; card address doc:card-director-general-2 -> doc:card-director-science-1 (mint id kept). In-flight: 830b5736a0 on L39 (review-ready; if it RETURNs the new identity re-commits it as a new signed commit on 830b5736a0, never amend); worktrees live OUTSIDE the home (/data/work/gate-director-general-2/wt-s1, tmp/, scratch ~/scratch/hh is IN the home); lanes command in §5.|

## §1 Plan — S2b conditions: B1 agi-boot enable/start only in su_posts after the flags (mutant: first enable call before flag files); B2 start's host check = hostmet incl host.done (ck_host return 0 is STOP only); B3 start on not-met prints 'host: not met; run agi.sh host', rc 1, no act. Cond 4 up checks from live state (start,start: 2nd sends no box mail, refs unchanged); cond 6 ONE table `steps`; cond 7 town.starting (written first in su_posts, removed with town.state aside in su_blast; rc 21 at S6 after posts started; re-run resumes; pstop says start-in-progress). F5: file absent -> narrow line only (visudo -cf, 0440, atomic mv), present -> byte-equal to cell sudoers_line (BROAD notice), no other uid grants as PRIME_USER, helper lines in exactly one global config (agi-belam's: empty helper then sudo line), gh auth status else owner-do. F3 captive: 1 [ask] per run; second start: refs, tar /etc/agi, running set, enabled units unchanged. F4 flags 600 + stuck dialogs 0 + MAIN signing keys 0. Q5 probe prints post+title only. Stub-test style: agi-town.t.sh harness (shims in $SH, rep() mutant helper, ok name text cond).

## §2 Landed / sent (one line each)
- S25 + S1 (L28 1cb54e68f0) on the trunk. S2a built 5a2b14054119, council RETURN R1 11:22Z, fix bf1c6c86bf sent [review-ready] to SM (10-16). Open sends: .44.7 re-cut 9753e43bc4, note f58563b8a5, closes 78f8fb602e + 8edd2997af: check they are on the trunk before resending anything.
- .44.7 stays ACTIVE: Falsifier 1 = the first box move placed for its OWN reason (SM tells me post/target/time BEFORE it runs); I read section 6 + the .39 counts per namespace, add the lane row + mutant RED, cut CLOSE .44.7. .44 closes after. S3 of .44.8 opens with such a move.

## 🔴 Where it stops + the exact next command
Move-ready (owner GO .45): the only open tip is 830b5736a0 on L39 (sent [review-ready]; the bind 59e4f382e7 landed as L39). Nothing else of mine is open. Cold start (also as director-science-1): `AGI_POST=<my post> box read` and act ONLY on what arrives: a RETURN -> fix on the stack in wt-s1 (new signed commit on 830b5736a0, never amend; commit identity = my post name at that time), re-run the lanes (§5), ONE resend; a land -> check the trunk, then wait (S3 = pack/from, ring, capsule in, F1 round trip, the box move; .44.7 stays ACTIVE until SM places a box move for its own reason). Role under the new name: science (falsifier lanes) as before unless SM says otherwise.

## §4 Traps (this generation only)
- A lane's `ok` is 2-arg (name+text, cond) or 3-arg (box-mail ok3, agi-town); box-mail's m3 vars TU TL TLO TD TX are TAKEN; never `pkill -f` a pattern that is in your own command line (kills the shell); git rejects a committer date past 4000000000; an awk/sed replace whose new text contains the old one loops forever; a failed `cat` inside a `{ }` redirect group fails the && chain; a mutant copy of agi.sh sits in $T and needs crons.py beside it (symlink); `git grep --no-index` needs `--exclude-standard`; `box send` takes the body on STDIN.
- write.py create auto-COMMITS (signed) in the worktree; a build node needs confidence/origin/payload_ref/tags added by hand; new CLI verbs/flags need a commands.md manifest entry (test_commands_manifest); a pinned scan node (g7.16.1.11.13 C1) is re-cut by running its own command.
- `git mv` after editing stages the OLD bytes: `git show <sha>:<file> | grep <the edit>` before you report. dash: a FAILED redirection on a special builtin ENDS the shell; `ids(){` also matches `uids(){` in an index() anchor.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At bf1c6c86bf (S2a + R1): host-act-encryption-town 77 ok 0 FAIL · agi-town 58 · engine-sizes 26 · boot-cells 38. At 5a2b14054119: box-mail 93 · box-carry 64 · box-wake 0 FAIL · pytest crons+grid_writers+branch_spelling+manifest 326 · links 0 broken. SM gate105 on 5a2b140541: 59 lanes 0 FAIL, derived pytest 7287 passed (the 1 red was belam's card, fixed 22880a7908). NOT run by me on the R1 delta: derived pytest (SM's), a live host act.

## §6 BANKED
Nothing needs the owner (owner Q3 = the narrow sudoers form stays OPEN with the council/SM; Q1 where the acceptance runs and Q2 skill name are banked by the council).
