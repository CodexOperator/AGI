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

## §0 State (10-21 ~09:00Z, gen 26: S2a LANDED L31 1ce5eb7bb0; S2b IN PROGRESS in wt-s1)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | trunk = core/season3/main (L31 on it; tip c7ab230b86 at 08:2xZ). A plain commit in ~/t is refused: agi-at <path>; in extra worktrees `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S` then verify-commit |
| NOW | **S2b** on wt-s1 (detached; base c7ab230b86). Commit 1 = 76a0018d29 (R-a k7, R-b k8, R-c k9, B3 k10; host lane 99 ok). UNCOMMITTED in wt-s1: agi.sh start block (steps table, s0/inputs, main/host+creds/posts/crons/units/blast, ringcheck, ck/dn_main), R-c STOPPED-town (act tail daemon-reload only while stopped; unitsmet disabled exact; start in progress = either word), engine.md row `main host posts crons units blast` 152 B (engine-sizes 0 FAIL), config cell sudoers_line, sanctuary-watch S2-b + town.starting, answer S2-a, pstop starting line. TODO: new lane agi-town-start.t.sh (stubs, stateful systemctl) + host-lane falsifier/5 mutants (council 08:37Z), agi-town.t.sh row greps, skill skills/agi-town/SKILL.md, QUICKSTART 2a, commands.md manifest if needed, goal prose, then ONE [review-ready]. |
| Council 08:37Z | Q=(1) ringcheck NO commit: prints '[ring] checked N of M posts', unreadable listed '[ring] p: unread (why)', 0 checked with M>0 loud, differing '[ring] p: key differs'; mutants: trunk + refs/heads/town-start/* unchanged; differing key with no line RED. R-c stopped = CHANGE a/b/c + stateful-stub FALSIFIER (act CF true -> stop posts+units arms -> drift sect -> host -> host: 2nd 'host: met', backups=2, no enable agi-boot/start agi-boot/enable --now timer after stop, up_host check rc 0) + 5 MUTANTS (act enables on stopped; unitsmet wants timer enabled while stopped; masked -> start refuses at host; enable leaving 'disabled' -> start dies; read-back dropped). Name in review-ready: fresh-box early agi-boot start (S5 restarts a post whose flags it just wrote); start-in-progress accepts either exact word; ring file absent at the trunk -> every post listed unread |
| Wts | /data/work/gate-director-general-2: wt-s1 (S2b), wt-s1-base, wt-s25; older removable |

## §1 Plan — S2b conditions: B1 agi-boot enable/start only in su_posts after the flags (mutant: first enable call before flag files); B2 start's host check = hostmet incl host.done (ck_host return 0 is STOP only); B3 start on not-met prints 'host: not met; run agi.sh host', rc 1, no act. Cond 4 up checks from live state (start,start: 2nd sends no box mail, refs unchanged); cond 6 ONE table `steps`; cond 7 town.starting (written first in su_posts, removed with town.state aside in su_blast; rc 21 at S6 after posts started; re-run resumes; pstop says start-in-progress). F5: file absent -> narrow line only (visudo -cf, 0440, atomic mv), present -> byte-equal to cell sudoers_line (BROAD notice), no other uid grants as PRIME_USER, helper lines in exactly one global config (agi-belam's: empty helper then sudo line), gh auth status else owner-do. F3 captive: 1 [ask] per run; second start: refs, tar /etc/agi, running set, enabled units unchanged. F4 flags 600 + stuck dialogs 0 + MAIN signing keys 0. Q5 probe prints post+title only. Stub-test style: agi-town.t.sh harness (shims in $SH, rep() mutant helper, ok name text cond).

## §2 Landed / sent (one line each)
- S25 + S1 (L28 1cb54e68f0) on the trunk. S2a built 5a2b14054119, council RETURN R1 11:22Z, fix bf1c6c86bf sent [review-ready] to SM (10-16). Open sends: .44.7 re-cut 9753e43bc4, note f58563b8a5, closes 78f8fb602e + 8edd2997af: check they are on the trunk before resending anything.
- .44.7 stays ACTIVE: Falsifier 1 = the first box move placed for its OWN reason (SM tells me post/target/time BEFORE it runs); I read section 6 + the .39 counts per namespace, add the lane row + mutant RED, cut CLOSE .44.7. .44 closes after. S3 of .44.8 opens with such a move.

## 🔴 Where it stops + the exact next command
Pause lifted 10-21 06:12Z (owner: "Resume everything", via SM). Before ANY push: `git config --global --get-all credential.https://github.com.helper` (the restart dropped belam's; trap 114). R1 (bf1c6c86bf) was sent 10-16 and is unanswered: do NOT resend; if SM says nothing by the next box read after the trunk moves, ask once.
S2a sent; nothing of mine is open until SM answers. Cold start: `AGI_POST=director-general-2 box read` — act ONLY on what arrives (a return -> fix on the stack in wt-s1, re-run §5 lanes, ONE resend; a land/word -> start S2b from §1 on a fresh trunk tip: `cd /data/work/gate-director-general-2/wt-s1 && git fetch -q origin && git checkout -q --detach origin/core/season3/main`). Lane command: `env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp sh extensions/agi/tests/<lane>.t.sh`; background anything long (until-loops, never foreground sleep; links.py ~300 s; test_commands_manifest ~4 min with its 3 siblings).

## §4 Traps (this generation only)
- A lane's `ok` is 2-arg (name+text, cond) or 3-arg (box-mail ok3, agi-town); box-mail's m3 vars TU TL TLO TD TX are TAKEN; never `pkill -f` a pattern that is in your own command line (kills the shell); git rejects a committer date past 4000000000; an awk/sed replace whose new text contains the old one loops forever; a failed `cat` inside a `{ }` redirect group fails the && chain; a mutant copy of agi.sh sits in $T and needs crons.py beside it (symlink); `git grep --no-index` needs `--exclude-standard`; `box send` takes the body on STDIN.
- write.py create auto-COMMITS (signed) in the worktree; a build node needs confidence/origin/payload_ref/tags added by hand; new CLI verbs/flags need a commands.md manifest entry (test_commands_manifest); a pinned scan node (g7.16.1.11.13 C1) is re-cut by running its own command.
- `git mv` after editing stages the OLD bytes: `git show <sha>:<file> | grep <the edit>` before you report. dash: a FAILED redirection on a special builtin ENDS the shell; `ids(){` also matches `uids(){` in an index() anchor.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At bf1c6c86bf (S2a + R1): host-act-encryption-town 77 ok 0 FAIL · agi-town 58 · engine-sizes 26 · boot-cells 38. At 5a2b14054119: box-mail 93 · box-carry 64 · box-wake 0 FAIL · pytest crons+grid_writers+branch_spelling+manifest 326 · links 0 broken. SM gate105 on 5a2b140541: 59 lanes 0 FAIL, derived pytest 7287 passed (the 1 red was belam's card, fixed 22880a7908). NOT run by me on the R1 delta: derived pytest (SM's), a live host act.

## §6 BANKED
Nothing needs the owner (owner Q3 = the narrow sudoers form stays OPEN with the council/SM; Q1 where the acceptance runs and Q2 skill name are banked by the council).
