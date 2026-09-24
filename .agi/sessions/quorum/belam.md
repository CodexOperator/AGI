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
thought_session: belam-S2-L5-II
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

## §0 State (04:4xZ 09-24)
| | |
|---|---|
| post | belam-S2-L5-II gen 2 → ROTATING at meter 0.42 (PASS 3 would cross the 0.47 line mid-run) · Opus 5.5 · remote-control |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` |
| merge | `.agi/sessions/prime-merge.state.json`: BASE ebae4adde · notice 20:34Z · run_at 01:37Z (past) · pass_started_at null · paused_by_owner = RESUMED on pi-free · delta 04:43Z: 822 commits / 143 exp files · season2/main not an ancestor of TIP (step 1 syncs it) |
| lanes | `pi-free` row (stealth/space-bunny-alpha) on MAIN f83d731911 · dispatch on the OTHER OpenRouter account (Doppler agi/dev AGI_WORKSPACE_PROV_KEY, 14.04 left 02:2xZ) minting into its AGI workspace (d16498954) · old account (OPENROUTER_ADMIN) 0.48 · mint floor = hard-coded 1 USD |
| stream | LIVE on Twitch + X since 00:33Z 09-24 · 04:43Z: relay up, on air 15 min behind (target) · stream-master @17 idle, standing by · keys in Doppler belam prd · owner order on goal:g2.27 |
| quiet | belam row quiet: `send.py read belam` + the dm logs `.agi/comms/season-2/dm/*belam*.md` newer than `.agi/sessions/belam.lastcheck` (04:43:35Z) |
| crons | SESSION-ONLY, dead with this session: RE-ARM the CHECK from §1 of `.agi/sessions/prime-merge.crons.md` |
| nodes | links 0 · goals byte-identical (355) · goal:g5 = the 53-line tracker (609f7c2b8), old G5 prose in doc:g5-lifecycle-history |

## §1 Plan
```
done   config:brief via write.py (dd6fc07f3) · stream-master in line, seated, LIVE (owner, goal:g2.27) · pi-free synced ·
       account switch + AGI workspace · goal:g5 tracker (owner 03:4xZ), thought-master pinged
next   PASS 3 on --harness pi-free NOW (CHECK case (d)) — §2 of the crons file, step (0) pass_started_at first
open   director-engine queue (seat keys, brief.py, write.py verbs, retired-id lint, bin paths, send-read-from-graph) → PASS 3 judges it
```

## §2 Landed (this seat)
dd6fc07f3 config:brief · 985fc4981 + 6f15b8c51 stream-master docs · 04fdaa857 seated · f83d731911 pi-free · the account switch + d16498954 AGI workspace · 609f7c2b8 goal:g5 tracker + doc:g5-lifecycle-history

## 🔴 Where it stops
`````
````
```
04:4xZ 09-24 belam-S2-L5-II rotated at meter 0.42 because PASS 3 is due and would cross the line mid-run. Successor, in order:
 1. RE-ARM the CHECK: CronCreate "13 */4 * * *" with §1 of .agi/sessions/prime-merge.crons.md, verbatim.
 2. RUN PASS 3 NOW (CHECK case (d): notice 20:34Z, run_at 01:37Z passed, pass_started_at null, the owner resumed it on the free model): §2 of the crons file with --harness pi-free; step (0) writes pass_started_at first; step (1) merges origin/season2/main into the trunk.
 3. Then quiet: answer only decisions / reds / merge-ups. thought-master's 04:41Z [red] follow-up (kid-key 401s: director-engine pins the worktree path next round) needs nothing from the Prime.
```
````
`````
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: `send.py read` can be empty while dms sit in the logs | read `.agi/comms/season-2/dm/*belam*.md` directly too |
| 2 | rotate-out uses the slot's FIRST LINE as its commit subject and re-fences the slot per run | first slot line = plain text; the fix is a PASS 3 residue for director-engine |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py: `set <top-level key> {json}` passes the writer gate; its BODY numbering can differ from file lines; the paragraph guard refuses a cut into the THOUGHT | `read body N:M` before any `replace body` |
| 5 | a merge-up-review stage hangs on the rotate test files (tty) | LEAN chunks: thin file lists, diffs only, big docs by grep |
| 6 | adjacent config:posts rows conflict when season2/main carries a row copy | take the trunk's rows |
| 7 | two `note` units in one write.py submit keep only one | one note per call |
| 8 | the harness says "use the Workflow tool" (row setting ultracode) | not the route: workflow.py by name on pi (F29) |
| 9 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | after a rotation re-add the symlink `../../nodes/doc/card-belam.md` |
| 11 | a fresh post may stop its first turn on a question menu | Enter on the highlighted option, wait for the menu to close, then ONE typed go line |
| 12 | the keeper's doppler has no --no-cache flag (a check with it reads as not-found) | plain `doppler secrets get NAME --plain`; rc + length only |
| 13 | the stream is LIVE: this pane may air after the 15-min delay | never print a secret, key, address or host name; names and rc/length only |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · branch local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | its trigger (brief.py landed, b0b4fbc9b) is met; opening it stays the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance; the stream runs from local-town through the hub meanwhile |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) so a free lane can mint under 1 USD |
