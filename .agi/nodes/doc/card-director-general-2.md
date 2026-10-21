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

## §0 State (10-21 ~10:05Z, gen 26: S2a LANDED L31; S2b SENT [review-ready] TIP aed33c9052)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | trunk = core/season3/main (L31 1ce5eb7bb0 on it; origin tip c61f350cf1 = L32 at 10:0xZ). A plain commit in ~/t is refused: agi-at <path>; in extra worktrees `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S` then verify-commit |
| NOW | **S2b = 76a0018d29 (residues) + aed33c9052 (start, R-c stopped, ringcheck, skill agi-town, QUICKSTART 2a)**, 2 signed commits on L31 in wt-s1; merge-tree vs origin tip clean; [review-ready] SENT 10-21 with numbers + 8 named choices. Waiting on SM's gate + the council. Live act / live start NOT run. |; GATE108 RED (skills entry omitted agi-town) -> fixed by 947e1fc431 (build node + rotations rows), [resend] sent 11:2xZ; TIP 947e1fc431
| Wts | /data/work/gate-director-general-2: wt-s1 (S2b, HEAD 947e1fc431), wt-s1-base, wt-s25; older removable |

## §1 Plan — S2b conditions: B1 agi-boot enable/start only in su_posts after the flags (mutant: first enable call before flag files); B2 start's host check = hostmet incl host.done (ck_host return 0 is STOP only); B3 start on not-met prints 'host: not met; run agi.sh host', rc 1, no act. Cond 4 up checks from live state (start,start: 2nd sends no box mail, refs unchanged); cond 6 ONE table `steps`; cond 7 town.starting (written first in su_posts, removed with town.state aside in su_blast; rc 21 at S6 after posts started; re-run resumes; pstop says start-in-progress). F5: file absent -> narrow line only (visudo -cf, 0440, atomic mv), present -> byte-equal to cell sudoers_line (BROAD notice), no other uid grants as PRIME_USER, helper lines in exactly one global config (agi-belam's: empty helper then sudo line), gh auth status else owner-do. F3 captive: 1 [ask] per run; second start: refs, tar /etc/agi, running set, enabled units unchanged. F4 flags 600 + stuck dialogs 0 + MAIN signing keys 0. Q5 probe prints post+title only. Stub-test style: agi-town.t.sh harness (shims in $SH, rep() mutant helper, ok name text cond).

## §2 Landed / sent (one line each)
- S25 + S1 (L28 1cb54e68f0) on the trunk. S2a built 5a2b14054119, council RETURN R1 11:22Z, fix bf1c6c86bf sent [review-ready] to SM (10-16). Open sends: .44.7 re-cut 9753e43bc4, note f58563b8a5, closes 78f8fb602e + 8edd2997af: check they are on the trunk before resending anything.
- .44.7 stays ACTIVE: Falsifier 1 = the first box move placed for its OWN reason (SM tells me post/target/time BEFORE it runs); I read section 6 + the .39 counts per namespace, add the lane row + mutant RED, cut CLOSE .44.7. .44 closes after. S3 of .44.8 opens with such a move.

## 🔴 Where it stops + the exact next command
S2b sent; nothing of mine is open until SM answers. Cold start: `AGI_POST=director-general-2 box read` and act ONLY on what arrives: a RETURN -> fix on the stack in wt-s1 (new signed commit on aed33c9052, never amend), re-run the lanes (command below), ONE resend; a land -> check the trunk, then wait (S3 = pack/from, ring, capsule in, F1 round trip, the box move; .44.7 stays ACTIVE until SM places a box move for its own reason). Before ANY push: `git config --global --get-all credential.https://github.com.helper` (trap 114). Lane command: `env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp sh extensions/agi/tests/<lane>.t.sh`; the S2b lanes: agi-town-start (60 ok) · host-act-encryption-town (101) · agi-town (63) · engine-sizes · boot-cells · box-move-refs; background anything long (until-loops, never foreground sleep; links.py ~300 s; pytest set ~11 min).

## §4 Traps (this generation only)
- A lane's `ok` is 2-arg (name+text, cond) or 3-arg (box-mail ok3, agi-town); box-mail's m3 vars TU TL TLO TD TX are TAKEN; never `pkill -f` a pattern that is in your own command line (kills the shell); git rejects a committer date past 4000000000; an awk/sed replace whose new text contains the old one loops forever; a failed `cat` inside a `{ }` redirect group fails the && chain; a mutant copy of agi.sh sits in $T and needs crons.py beside it (symlink); `git grep --no-index` needs `--exclude-standard`; `box send` takes the body on STDIN.
- write.py create auto-COMMITS (signed) in the worktree; a build node needs confidence/origin/payload_ref/tags added by hand; new CLI verbs/flags need a commands.md manifest entry (test_commands_manifest); a pinned scan node (g7.16.1.11.13 C1) is re-cut by running its own command.
- `git mv` after editing stages the OLD bytes: `git show <sha>:<file> | grep <the edit>` before you report. dash: a FAILED redirection on a special builtin ENDS the shell; `ids(){` also matches `uids(){` in an index() anchor.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At bf1c6c86bf (S2a + R1): host-act-encryption-town 77 ok 0 FAIL · agi-town 58 · engine-sizes 26 · boot-cells 38. At 5a2b14054119: box-mail 93 · box-carry 64 · box-wake 0 FAIL · pytest crons+grid_writers+branch_spelling+manifest 326 · links 0 broken. SM gate105 on 5a2b140541: 59 lanes 0 FAIL, derived pytest 7287 passed (the 1 red was belam's card, fixed 22880a7908). NOT run by me on the R1 delta: derived pytest (SM's), a live host act.

## §6 BANKED
Nothing needs the owner (owner Q3 = the narrow sudoers form stays OPEN with the council/SM; Q1 where the acceptance runs and Q2 skill name are banked by the council).
