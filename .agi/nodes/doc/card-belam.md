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
thought_session: belam-S2-L5-IV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

## §0 State (21:1xZ 09-24)
| | |
|---|---|
| post | belam-S2-L5-IV gen 4 · seated 20:06Z (clean seam) · Opus 5.5 · remote-control · meter ~0.29 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN and lands there: exact-path commits only) · prime-root = `season2/main` · box tz UTC |
| merge | PASS 3 → 6f5ee34e5c · PASS 4 → ad81688a0b (14:08Z) · state file: last_merged 3b0c4e8e8f, notice/run_at/pass_started_at null · trunk `.geometry` current 21:0xZ (1724e43da4 reached it via thought-master's 4905c6d0bf) |
| directors | director-engine + director-thought, claude-sonnet-5 max · rule now in `doc:unified-director-brief` §1 DISPATCH: ONE parent per round, `--tier parent --role parent --ladder-tier 0`, no `--harness` (pi-free by the ladder), never `--tier kid` · spawns 0/30 at 21:1xZ (DH.295/296 bare kids finished) |
| dms 09-24 | 20:5xZ rule ping: DE delivered · DT undelivered-yet (sweep) · TM delivered (acted: 36cce7af91 retired `doc:lm-director-brief-customizations`) · 21:0xZ DE commands steer + TM Jev survey: undelivered-yet (panes busy) · inbox empty 21:1xZ |
| lanes | parents + kids on pi-free (stealth/space-bunny-alpha) · credits 13.94 (13:47Z) · mint floor 1 USD |
| stream | LIVE on Twitch + X since 00:33Z 09-24 (15-min delay) |
| crons | CHECK job 7ce06676, "13 */4 * * *" recurring, §1 of `.agi/sessions/prime-merge.crons.md` verbatim · SESSION-ONLY, dies with this session |

## §1 Plan
```
done   seated: CHECK re-armed · quorum re-linked · card
       owner 20:1xZ-20:4xZ (verbatim in doc:l5-owner-decisions): raw DMs read -- thought-master never asked the Prime; it authorised
       direct kids 05:19Z (TMM.107) and lifted them 17:02Z on the two CARDS only · the parent/kid rule + thought-master's co-ownership
       of the director docs in doc:unified-director-brief · director cards = graph entities (doc:card-director-engine / -thought)
       · goal:g1.25 reshaped: action registry, commands.py = query + parse layer · Jev survey ordered to thought-master (g5.24.3)
       · config:rotations startup pass (prime 13->10, director 9->8, F32 = no Claude subagents) · trunk .geometry current
next   the next CHECK: live leases tier=parent only (a new bare kid = [red] to thought-master) · the four dms landed
       (send.py status <seat>; else send.py wake) · each director re-links its card to doc:card-<post> at its next card write
open   residues with director-engine (pass3 batch + 11 defect hypotheses; pass4 batch) · §6
```

## §2 Landed (this seat)
e05d2ef5f2 card at seating · 004ddcf49a director rule + thought-master authority + card entities + owner verbatim · 68074ee7ab goal:g1.25 steer + GOALS.md · 6f855070e8 startup pass

## 🔴 Where it stops
21:1xZ 09-24 belam-S2-L5-IV: the owner's 20:1xZ-20:4xZ orders applied and committed; quiet on the CHECK.
 1. Next CHECK fire: run §1 of .agi/sessions/prime-merge.crons.md as written, plus: spawn_budget.py status shows tier=parent leases only; send.py status director-engine / director-thought / thought-master shows the 09-24 dms read.
 2. Otherwise quiet: answer only decisions / reds / merge-ups and the owner.
 3. A PASS reuses /tmp/belam-pass4/ (build.py, launch.sh, verdicts.py) and /tmp/belam-trunk-sync/: copy, retarget BASE / TIP / OS and the run-key prefix, as PASS 4 did.
 4. A successor at wake: RE-ARM the CHECK (CronCreate "13 */4 * * *", §1 verbatim), re-link the quorum symlink (trap 10), write this card whole.

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | read `send.py read belam`; the logs too when a post says it wrote |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject and re-fences the slot per run | first slot line = plain text; defect minted (hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced) |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py body numbering can differ from file lines | `sub <old> => <new>` (literal, several per submit) beats line ranges; never ` && ` inside a unit's text |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py: trunk rows + the Prime's cells, pubkeys must agree; temp index + ff-only, never a conflicted MAIN |
| 7 | two `note` units in one submit keep only one; a body writer cannot share a submit with `thought` | one body writer per submit, `thought` alone |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi / pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | diff the flat file vs the doc node (rotate adds only a fence level), then `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`; commit both by exact path |
| 11 | a Prime row edit on season2/main is reverted by that post's next key-row publish (rotate.py:10368) | before a post rotates on a new row cell, it merges origin/season2/main and confirms the cell (defect minted) |
| 12 | `cd` moves the session's working directory (hit again 09-24: a `cd` into comms/dm) | absolute paths, `git -C`, subshells |
| 13 | the stream is LIVE (15-min delay) | never print a secret, key, address or host name |
| 14 | `.env` on local-town is `/data/work/agi/.env` (F13 names another box) | read credits from the MAIN root |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 16 | background writes of many nodes outlast the 120 s Bash timeout | pass a timeout, or expect the task to move to the background |
| 17 | the Agent tool for graph recon (the Prime spawned one 20:2xZ 09-24) | NEVER -- no Claude subagents, ever (owner 20:3xZ, F32); read the graph yourself |
| 18 | at rotation a director reads HEAD + card, never the template (until brief.py lands) | rules go in doc:unified-director-brief; cards (doc:card-<post>) carry overrides only |
| 19 | every rotation's key row lands on season2/main and leaves the trunk's `.geometry` behind: rotate-self refuses (rotate.py `_geometry_resolution_root`) | after a rotation: `git rev-list --count HEAD..origin/season2/main -- .agi/nodes/.geometry` = 0, else merge it (merge-tree preview first) |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · branch local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | its trigger (brief.py landed, b0b4fbc9b) is met; opening it stays the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance; the stream runs from local-town through the hub meanwhile |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) so a free lane can mint under 1 USD |
| thought-master beyond the director docs (goal moves / renumbers / config) | director docs + cards GRANTED (owner 20:1xZ 09-24; doc:unified-director-brief line 21); config:* stays prime/owner-only (write.py:1701, [config].md:3) -- a scoped actor_rows grant is a director-engine round if the owner wants more |
