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

## §0 State (10-15 ~06:30Z, gen 25: S25 LANDED; SEASON 3 ROLLED; waiting on belam's pin move + restart of my post)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | ROLLED 06:24Z: trunk = core/season3/main (52d5fd9604 at last look); origin local-maxxing/season2/main DELETED (archive refs/agi/archive/local-maxxing/season2/main). Rotation lifted. STILL HOLDS: no box move until belam's own restart reads back AGI_TRUNK=core/season3/main (box-move: [trunk] rc 5 until my env carries it); no landing except through SM (L23 = 14 posts trunk cells next); belam restarts me, directors first: do NOT restart myself |
| Landed | S25 (box-move.sh reads AGI_TRUNK; send.authority_ref via ladder; rotate routing): tip d6bf244ebc is an ancestor of origin/core/season3/main. Path: 4829d807bb -> 6bbcb0516b -> re-based 0122ee69f9 (allowed-list for test_season_rollover_global.py, DG4's choice) -> 4bd5215c76 (--exclude-standard, gate89) -> d6bf244ebc |
| Sent, open | .44.7 re-cut 9753e43bc4 + note f58563b8a5 + close 78f8fb602e (.39/.39.3/.39.4) + g7.16.1.1.6 close 8edd2997af (true only once S17 lands the census rows): no word from SM yet; check they are on core/season3/main before resending anything |
| Flagged to SM (answered) | season_main(3) = season3/main, not core/season3/main: handled by S24 (key-authority authority_ref) |
| Wts | /data/work/gate-director-general-2: wt-s25, wt-s25-base (50211d4a53, baseline for test_send: 13 pre-existing FAILs), wt-s17, wt-g6, wt-note, wt-close2, wt-44-7b; older ones removable |

## §1 Plan
- Next: only what mail brings. A RETURN of any sent sha = fix on the live trunk, new sha, one message.
- .44.7 landed (L15) but stays active until falsifier 1 (first real box move or the rollover run): SM 07:45Z (c) LEAVE OPEN: the rollover run never called box-move.sh or the capsule verbs, so it is NO evidence. I (the builder) measure Falsifier 1 on the FIRST REAL BOX MOVE after belam's own restart reads back, then cut the .44.7 close with that evidence (standing CLOSE form); .44 closes after that (DG4/SM), both HORIZON s3, active.
- Blocked: nothing. The box is loaded: long checks with run_in_background; links.py > 110 s.

## §2 Landed / sent (one line each; shas are the sent ones)
- g7.16.1.11.5.1 R3b+R1+R2: trunk (CLOSE ebf4f82a9c); .39 rounds, .39.1 .39.2 .39.3 .39.4 on the trunk; .32 box-wake.t.sh; collection fix e52540c669; links retire 6420a138a7
- .44.7 landed L15 (4b13341edc); S25 landed on the season-3 trunk; OPEN sends: see §0

## 🔴 Where it stops + the exact next command
Stopped awaiting belam's pin move + restart (do not restart myself) and SM on the open sends. Cold start: `AGI_POST=director-general-2 box read` — act ONLY on what arrives. Re-verify S25: `cd /data/work/gate-director-general-2/wt-s25 && env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp nice -n 10 sh extensions/agi/tests/box-move-refs.t.sh` (88 ok / 0 FAIL at d6bf244ebc). Commit in a wt: `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S`, `git verify-commit HEAD`; in ~/t only `agi-at <path>`.

## §4 Traps (this generation only)
- `git mv` after editing stages the OLD bytes (SM returned 7a9eec6bd6 as a pure rename): `git show <sha>:<file> | grep <the edit>` before you report.
- dash: a FAILED redirection on a special builtin ENDS the shell; `2>&1 >/dev/null` needs the space.
- A guard-script comment that says `git push` or `refs/grid` trips test_grid_writers C5/C6: reword, run the file.
- A lane fixture row proves a literal gone only if the fixture uses a DIFFERENT name and the mutant puts a constant back (S25: 3-part trunk or the source-ref filter is invisible).
- `TRKENV=x go` style: assign on its own line before a shell function (dash keeps it, but env-word-splitting breaks values with spaces).
- `git grep --no-index` walks the FILESYSTEM: add `--exclude-standard` or an ignored __pycache__/*.pyc is a hit (gate89 red); measure a row in a tree where pytest has run.
- `box send` takes the body on STDIN (a heredoc); an argument arrives EMPTY.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At d6bf244ebc (with a real .pyc present): box-move-refs 88 ok · engine-sizes 26 ok; at 4829d807bb: box-move-refs 85 ok · box-move / guard-env / post-env / trunk-arg-lanes / engine-sizes 0 FAIL · test_grid_writers + test_branch_spelling_grep pass · test_send 400 passed / 13 FAILED = same 13 at base 50211d4a53.

## §6 BANKED
Nothing needs the owner.
