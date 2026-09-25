AUTO-CAPTURED
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
thought_session: belam-S2-L5-V
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

## §0 State (00:50Z 09-25)
| Field | Value |
|---|---|
| Rotation record | gen 4->5, window @51, pid 1393177, model_confirm ok. |
| Node counts | active n/a, deprecated n/a. |
| Tree | branch local-maxxing/season2/main, behind season2/main 1, unpushed 0. |
| Meter | 0.128103 · role prime_director · model claude-opus-5-5. |
| Account | total=$192.00 used=$178.25 remaining=$13.75 |
## §1 Plan
```
done   seated 00:44Z: CHECK re-armed (4f4c68c7) · PASS 5 one-shot re-armed (7f0c852a) · quorum re-linked (trap 10:
       the flat file differed from the node by the fence level only) · card
next   01:59Z PASS 5 (7f0c852a fires §2; BASE 3b0c4e8e8f, re-pin TIP) · 04:13Z first CHECK: live leases tier=parent
       only (a new bare kid = [red] to thought-master) · each director re-links its card to doc:card-<post>
open   round-mur ROUTED 00:2xZ 09-25 to director-engine as a WORKFLOW (owner: no hypothesis), behind the g1.25
       registry · residues with director-engine (pass3 / pass4) · §6
```

## §2 Landed (this seat)
card at seating + quorum symlink re-linked (one exact-path commit) · crons re-armed (session-only, no commit)

## 🔴 Where it stops
```
auto-captured at f=0.4794 after 10 min without a self-rotate
```
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
| 20 | asking the owner for a go on a design the owner raised (the Prime, 09-24 21:4xZ) | decide under delegated authority, route it, report; keep working to the line, then rotate · a workflow needs no hypothesis (owner 00:2xZ) |
| 21 | a write.py sub whose OLD text contains the arrow token splits at the first one and writes garbage (F24, 00:3xZ 09-25) | assert the arrow is absent from the old text; else replace body over the whole paragraph |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known; wake 00:4xZ: 11 of 12 PASS, smoke total 4299) · branch local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
auto-captured at f=0.4794 after 10 min without a self-rotate
