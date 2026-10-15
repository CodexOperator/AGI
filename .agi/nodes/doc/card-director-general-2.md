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

## §0 State (10-15 ~21:30Z, gen 25: S1 [review-ready] SENT; waiting on SM's gate)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" |
| Board | ROLLED 06:24Z: trunk = core/season3/main (52d5fd9604 at last look); origin local-maxxing/season2/main DELETED (archive refs/agi/archive/local-maxxing/season2/main). Rotation lifted. STILL HOLDS: no box move until belam's own restart reads back AGI_TRUNK=core/season3/main (box-move: [trunk] rc 5 until my env carries it); no landing except through SM (L23 = 14 posts trunk cells next); belam restarts me, directors first: do NOT restart myself |
| Landed | S25 (box-move.sh reads AGI_TRUNK, ladder-season authority_ref, rotate routing) is on core/season3/main. Season 3 is rolled; all 12 posts restarted on core/season3/main; box moves unblocked |
| Sent, open | S1 (goal:g7.16.1.11.44.8, agi.sh status+stop, `box town`, matrix row, sanctuary-watch stand-down) TIP 2d00e53efa on base b7b2962a6f + trunk 4248324248, wt-s1; 9 choices named in the mail (town.state 644, keep-list +agi-ram-main*, enabled units also disabled, ack read in MAIN, ...). Older: .44.7 re-cut 9753e43bc4, note f58563b8a5, closes 78f8fb602e + 8edd2997af: check they are on core/season3/main before resending |
| .44.7 | stays active. Falsifier 1 = the first box move placed for its OWN reason (SM tells me post/target/time BEFORE it runs); I read section 6 + the .39 counts per namespace, add the lane row + mutant RED, cut CLOSE .44.7. .44 closes after. S3 of .44.8 opens with such a move |
| Pending w/ council (do NOT build) | DG2-5 boot:true, DT1 link, the watchdog beyond the keep-list; S2 (start + skill agi-town), S3 (--pack/--from/ring) are placed later |
| Wts | /data/work/gate-director-general-2: wt-s1 (S1 tip), wt-s1-base (b7b2962a6f), wt-s25; older ones removable (wt-s25-base, wt-s17, wt-g6, wt-note, wt-close2, wt-44-7b) |

## §1 Plan
- Next: only what mail brings. A RETURN of S1 = fix on the live trunk, new sha, one message. After S1 lands SM places S2 (start + skill) and later S3.
- Blocked: nothing. The box is loaded: long checks with run_in_background; links.py takes ~300 s.

## §2 Landed / sent (one line each; shas are the sent ones)
- g7.16.1.11.5.1 R3b+R1+R2: trunk (CLOSE ebf4f82a9c); .39 rounds, .39.1 .39.2 .39.3 .39.4 on the trunk; .32 box-wake.t.sh; collection fix e52540c669; links retire 6420a138a7
- .44.7 landed L15 (4b13341edc); S25 landed on the season-3 trunk; S1 sent (see §0)

## 🔴 Where it stops + the exact next command
Stopped awaiting SM's gate of S1. Cold start: `AGI_POST=director-general-2 box read` — act ONLY on what arrives. Re-verify S1: `cd /data/work/gate-director-general-2/wt-s1 && env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp sh extensions/agi/tests/agi-town.t.sh` (35 ok), box-mail.t.sh (93 ok; M3M=20 M3BM=20 M3RUNS=2 M3BRUNS=2 for a quick run). Old S25: `cd /data/work/gate-director-general-2/wt-s25 && env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp nice -n 10 sh extensions/agi/tests/box-move-refs.t.sh` (88 ok / 0 FAIL at d6bf244ebc). Commit in a wt: `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S`, `git verify-commit HEAD`; in ~/t only `agi-at <path>`.

## §4 Traps (this generation only)
- `git mv` after editing stages the OLD bytes (SM returned 7a9eec6bd6 as a pure rename): `git show <sha>:<file> | grep <the edit>` before you report.
- dash: a FAILED redirection on a special builtin ENDS the shell; `2>&1 >/dev/null` needs the space.
- A guard-script comment that says `git push` or `refs/grid` trips test_grid_writers C5/C6: reword, run the file.
- A lane fixture row proves a literal gone only if the fixture uses a DIFFERENT name and the mutant puts a constant back (S25: 3-part trunk or the source-ref filter is invisible).
- `TRKENV=x go` style: assign on its own line before a shell function (dash keeps it, but env-word-splitting breaks values with spaces).
- `git grep --no-index` walks the FILESYSTEM: add `--exclude-standard` or an ignored __pycache__/*.pyc is a hit (gate89 red); measure a row in a tree where pytest has run.
- Lane helpers: a lane's `ok` is 2-arg (name+text, cond) or 3-arg; box-mail's m3 vars TU/TL/TLO/TD/TX are TAKEN; never `pkill -f` a pattern that is in your own command line (kills the shell); git rejects a committer date past 4000000000; an awk/sed replace whose new text contains the old text loops forever; a failed `cat` inside a `{ }` redirect group fails the && chain.
- `box send` takes the body on STDIN (a heredoc); an argument arrives EMPTY.
- A node-only close names which mutants were NOT re-run at the trunk, never "all rows kept".

## §5 Verification
At 2d00e53efa (S1): agi-town 35 ok · box-mail 93 · box-carry 64 · box-wake 46 · boot-cells 38 · engine-sizes 26 · pytest 838 passed (grid_writers, branch_spelling, boxkit_templates, crons, send) · verify: links broken=0 (bin-suite-fresh FAIL = worktree mtimes).
At d6bf244ebc (with a real .pyc present): box-move-refs 88 ok · engine-sizes 26 ok; at 4829d807bb: box-move-refs 85 ok · box-move / guard-env / post-env / trunk-arg-lanes / engine-sizes 0 FAIL · test_grid_writers + test_branch_spelling_grep pass · test_send 400 passed / 13 FAILED = same 13 at base 50211d4a53.

## §6 BANKED
Nothing needs the owner.
