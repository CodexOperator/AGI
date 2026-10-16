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

## §0 State (10-16, gen 26: S2a BUILT + SENT [review-ready]; waiting on SM's gate)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | Season 3 rolled; trunk = core/season3/main (S1 = L28 1cb54e68f0 is ON it; origin tip 4b1cf25ef2 at 09:15Z). Box moves unblocked; rotation lifted. A plain commit in ~/t is refused: agi-at <path>; in extra worktrees `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S` then verify-commit |
| DONE | S25 (on trunk). S1 = goal:g7.16.1.11.44.8 agi.sh status+stop, `box town`, matrix row, sanctuary-watch stand-down (R1-R7 fixed; council APPROVED 3/3; landed L28) |
| NOW | **S2a = 5a2b14054119b14beb5395ecab94bde70809b4c8** (ONE signed commit on trunk tip ee43b8f10e, wt-s1 detached): [review-ready] sent to SM; the host fold per council 09:20Z conditions 1/2/3/8 + timer gate, each with a mutant (host-act lane 63 ok = 49 + 14 k-rows; agi-town 58). Live act NOT run (root, belam's). **S2b** (start S0-S9, skill agi-town, QUICKSTART 2a, F3-F5, S2-a, S2-b, R6 binding; §1 below) starts AFTER S2a lands + SM's word. NOT in S2a: retire a4, `move POST` (-> S3) |
| Wts | /data/work/gate-director-general-2: wt-s1 (detached at origin tip 4b1cf25ef2, CLEAN: start S2a here: `git checkout -q --detach origin/core/season3/main` first), wt-s1-base (b7b2962a6f), wt-s25; older ones removable |

## §1 Plan — S2a DONE (5a2b14054119). Shape for the next reader: agi.sh `up_host(){ ( ... );}` = old preamble + PC (ONE piece list for writer AND hostmet) + hostmet before STEP 0 + `tm` (timer only when cell carry_fetch true; rehearsal prints it) ; route `host)up_host`; `ck_host/dn_host` return 0 (STOP); old script `act)` = one exec line. If SM returns it: fix on the SAME stack (amend via a new signed commit on ee43b8f10e or on the new trunk tip), re-run the lanes in §5, resend ONE [review-ready].
S2b (after S2a lands + SM's word). F5 per council 09:21Z (S2b only): cell values.local_maxxing.agi_town.sudoers_line = the 34-byte line `agi-belam ALL=(ALL) NOPASSWD: ALL` (expected bytes of an EXISTING file; I write the cell on my S2 branch); file absent -> agi.sh writes ONLY the narrow one-command line under condition 3 (temp + visudo -cf + root:root 0440 + atomic mv; visudo absent -> [owner-do]), never the cell's bytes, never ALL; byte-equal pass on a broad line prints "[sudoers] present, byte-equal to the cell; BROAD grant (ALL), owner ruling pending"; the Q5 probe prints ONLY post name + dialog title (never tail bytes). S2b conditions 4-7: up ck_ from live state (a fresh box's running set = the AGI_BOX posts rows); pubkey commit to refs/heads/town-start/<box>/<UTC>, signed belam@agi, printed as an [owner-do]/[ask], never moves the trunk; ONE table (S-step -> row name); /etc/agi/town.starting <UTC> (root 600) written at S5, removed with the town.state move-aside at S9; pstop + sanctuary-watch say "a start is in progress since <UTC>: finish it with agi.sh start". belam's answers: folder trust = $HOME/.claude.json projects[<MAIN root>].hasTrustDialogAccepted; bypass = $HOME/.claude/settings.json skipDangerousModePermissionPrompt; renderer = .claude.json fullscreenUpsellSeenCount 3 (NOT enough) + settings.json "tui":"default" (the real key); dialog probe = tail of $HOME/o, strip ANSI, match the TITLE ("Try the new fullscreen renderer"); trust/bypass titles UNMEASURED: take them from a scratch-HOME `script` capture.

## §2 Landed / sent (one line each)
- S25 + S1 (L28 1cb54e68f0) on the trunk. S2a built 5a2b14054119 and sent [review-ready] to SM (10-16). Open sends: .44.7 re-cut 9753e43bc4, note f58563b8a5, closes 78f8fb602e + 8edd2997af: check they are on the trunk before resending anything.
- .44.7 stays ACTIVE: Falsifier 1 = the first box move placed for its OWN reason (SM tells me post/target/time BEFORE it runs); I read section 6 + the .39 counts per namespace, add the lane row + mutant RED, cut CLOSE .44.7. .44 closes after. S3 of .44.8 opens with such a move.

## 🔴 Where it stops + the exact next command
S2a sent; nothing of mine is open until SM answers. Cold start: `AGI_POST=director-general-2 box read` — act ONLY on what arrives (a return -> fix on the stack in wt-s1, re-run §5 lanes, ONE resend; a land/word -> start S2b from §1 on a fresh trunk tip: `cd /data/work/gate-director-general-2/wt-s1 && git fetch -q origin && git checkout -q --detach origin/core/season3/main`). Lane command: `env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp sh extensions/agi/tests/<lane>.t.sh`; background anything long (until-loops, never foreground sleep; links.py ~300 s; test_commands_manifest ~4 min with its 3 siblings).

## §4 Traps (this generation only)
- A lane's `ok` is 2-arg (name+text, cond) or 3-arg (box-mail ok3, agi-town); box-mail's m3 vars TU TL TLO TD TX are TAKEN; never `pkill -f` a pattern that is in your own command line (kills the shell); git rejects a committer date past 4000000000; an awk/sed replace whose new text contains the old one loops forever; a failed `cat` inside a `{ }` redirect group fails the && chain; a mutant copy of agi.sh sits in $T and needs crons.py beside it (symlink); `git grep --no-index` needs `--exclude-standard`; `box send` takes the body on STDIN.
- write.py create auto-COMMITS (signed) in the worktree; a build node needs confidence/origin/payload_ref/tags added by hand; new CLI verbs/flags need a commands.md manifest entry (test_commands_manifest); a pinned scan node (g7.16.1.11.13 C1) is re-cut by running its own command.
- `git mv` after editing stages the OLD bytes: `git show <sha>:<file> | grep <the edit>` before you report. dash: a FAILED redirection on a special builtin ENDS the shell; `ids(){` also matches `uids(){` in an index() anchor.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At 5a2b14054119 (S2a): host-act-encryption-town 63 ok 0 FAIL · agi-town 58 · engine-sizes 0 FAIL · boot-cells 0 FAIL · box-mail 93 · box-carry 64 · box-wake 0 FAIL · pytest test_crons+test_grid_writers+test_branch_spelling_grep+test_commands_manifest 326 passed · links 0 broken, schema clean. NOT run: SM's gate (full pytest on the touched files), a live host act.

## §6 BANKED
Nothing needs the owner (owner Q3 = the narrow sudoers form stays OPEN with the council/SM; Q1 where the acceptance runs and Q2 skill name are banked by the council).
