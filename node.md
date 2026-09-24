---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-III
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

## §0 State (17:3xZ 09-24)
| | |
|---|---|
| post | belam-S2-L5-III gen 3 → ROTATING at a clean seam (meter ~0.44): every owner order done, no PASS pending · Opus 5.5 · remote-control |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` |
| merge | PASS 3 → season2/main 6f5ee34e5c · PASS 4 → ad81688a0b · state file: last_merged 3b0c4e8e8f, notice/run_at/pass_started_at null, paused_by_owner dropped · 16:43Z CHECK: 23 commits, 0 exp → case (a) |
| lanes | parents + kids on **pi-free** (stealth/space-bunny-alpha): ladder roles + config spawn.harness (owner 16:5xZ) · credits 13.94 (13:47Z) · mint floor 1 USD |
| directors | director-engine + director-thought on **claude-sonnet-5 max** (owner 05:1xZ; model_confirm 05:50Z / 05:46Z) · both post branches carry my trunk sync with the pi-free change (not pushed) |
| stream | LIVE on Twitch + X since 00:33Z 09-24 (15-min delay) · stream-master standing by |
| crons | SESSION-ONLY, dead with this session: RE-ARM the CHECK (§1 of `.agi/sessions/prime-merge.crons.md`); §2 there is the PASS 4 text |
| quiet | `send.py read belam` is the signal (no belam dm-log entries landed in `.agi/comms` all day) |

## §1 Plan
```
done   PASS 3 + PASS 4 (0)-(9) · Sonnet-max directors · pi-free parent/kid spawns in all 4 spawning trees
       goal:g2.2 shape / imap / omap (owner verbatim) · goal:g5.24.3 magic-pane brainstorm (owner verbatim + reply condensed)
next   quiet on the CHECK; case (b) → 5 h notice → PASS 5 (refresh §2's FACTS line first: BASE = the state file's sha, p5 run keys)
open   residues with director-engine (pass3 batch + 11 defect hypotheses; pass4 batch) · thought-master permissions (§6)
```

## §2 Landed (this seat)
9fec964885 / 3b0c4e8e8f trunk syncs · 6f5ee34e5c PASS 3 · 21fd8d49cd residues · ad81688a0b PASS 4 · 92f34a2f27 residues · 3b6e0eb632 + 6d38b9742e Sonnet rows (trunk ab45488b39) · 431b8edc32 / 92142b5b9a pi-free · b70ed3c63c goal:g2.2 · 623dd1e2c2 goal:g5.24.3

## 🔴 Where it stops
````
```
17:3xZ 09-24 belam-S2-L5-III rotated at a clean seam: all owner orders done, no PASS pending, the CHECK is the only live duty.
 1. RE-ARM the CHECK: CronCreate "13 */4 * * *" with §1 of .agi/sessions/prime-merge.crons.md, verbatim; re-link the quorum symlink (trap 10).
 2. Then quiet: answer only decisions / reds / merge-ups and the owner.
 3. A PASS reuses /tmp/belam-pass4/ (build.py, launch.sh, verdicts.py) and /tmp/belam-trunk-sync/ (resolve.py, sync.sh): copy, retarget BASE / TIP / OS and the run-key prefix, as PASS 4 did.
```
````
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | read `send.py read belam`; the logs too when a post says it wrote |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject and re-fences the slot per run | first slot line = plain text; defect minted (hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced) |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py body numbering can differ from file lines; the paragraph guard refuses a cut ending inside a paragraph or into the THOUGHT | `read body N:M` first; insert at a BLANK line |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py: trunk rows + the Prime's cells, pubkeys must agree; temp index + ff-only, never a conflicted MAIN |
| 7 | two `note` units in one submit keep only one; `replace body` cannot share a submit with `thought` (dry-run admits it, live refuses rc 2) | one body writer per submit |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi / pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | after a rotation re-add `../../nodes/doc/card-belam.md` |
| 11 | a Prime row edit on season2/main is reverted by that post's next key-row publish (rotate.py:10368 splices the worktree's whole row) | before a post rotates on a new row cell, it merges origin/season2/main and confirms the cell (defect minted) |
| 12 | `cd` into prime-root moves the session's working directory | use `git -C` / subshells for prime-root |
| 13 | the stream is LIVE (15-min delay) | never print a secret, key, address or host name |
| 14 | `.env` on local-town is `/data/work/agi/.env` (F13 names another box) | read credits from the MAIN root |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 16 | background writes of many nodes outlast the 120 s Bash timeout | pass a timeout, or expect the task to move to the background |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · branch local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | its trigger (brief.py landed, b0b4fbc9b) is met; opening it stays the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance; the stream runs from local-town through the hub meanwhile |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) so a free lane can mint under 1 USD |
| thought-master: move goals / full Prime-level graph permissions (owner 17:xZ: "if it's too complicated leave it") | left as is — the write guard is per-schema data (role deny-lists, list_key grants) plus ring-signed config writes, so full Prime rights is a multi-schema change; recommend a scoped grant (goal moves + renumbers for thought-master) as a director-engine round, after measuring which gate refused thought-master before |
