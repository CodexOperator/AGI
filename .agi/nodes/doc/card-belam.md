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
thought_session: belam-S2-L5-I
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`, five-axis map) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines with frontmatter; rules live in role docs, never here.

## §0 State (20:1xZ 09-23)
| | |
|---|---|
| post | belam-S2-L5-I gen 2 → ROTATING at meter 0.92 (hook) · Opus 5.5 · remote-control |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` |
| season2/main | @a99b128b0 (PASS 2 merge 4c35ff60f + the thought-master key row) · state `.agi/sessions/prime-merge.state.json`: last merged trunk ebae4adde, no notice pending |
| quiet | belam row = quiet (owner): `send.py read` shows nothing — read the dm logs `.agi/comms/season-2/dm/*belam*.md` newer than `.agi/sessions/belam.lastcheck` |
| crons | SESSION-ONLY: CHECK every 4 h "13 */4 * * *" (spec §1 of `.agi/sessions/prime-merge.crons.md`) · persisted `prime_merge 13 */4` inert until prime_merge.py |
| spend | floor -50 (owner) · per-key cap 1 USD kept (owner) · key TTL 300 min · TypeSafe 2 × 5 USD keys in MAIN .env (forwarded to pi kids) · 42.69 USD at 11:41Z |
| nodes | links 0 · goals byte-identical · active 3753 (season2/main) |

## §1 Plan
```
done   doc unification: HEAD (doc:unified-head) · templates director/master/Prime · this card as a doc node · goal + hypothesis
       formats in their schemas · review-in-place in the director template · retired ids out (g14 → g5) · PASS 2 (21 rounds, 0 red)
open   director-engine queue: seat-key round FIRST → brief.py (merge-up @fe5647b83 ruled land-all at thought-master's gate) →
       write.py sub → retired-id lint → harness bin paths → send-read-from-graph → PASS 2 residue batch + 2 defect rounds
Prime  (a) when the brief.py merge-up lands on the trunk: rewrite config:brief's brief cell through write.py as prime_director,
           same values (the sanctioned write the EF.19 demote asks for)
       (b) after ANY rotation on this box: republish that post's re-keyed row on season2/main (as a99b128b0) until the key round lands
       (c) next merge pass only when experiment files land (CHECK arms it; chunk reviews LEAN)
```

## §2 Landed (09-23)
1e6ca0056 HEAD · 52d046afd templates + card node · 3e4307050 goal format · 53b3ae955 hypothesis format · 4adaa1f01 review-in-place · 4c35ff60f (season2/main) PASS 2 · 1ed2eda83 g5 dedup · 7a0227ac7 rules in role docs only

## 🔴 Where it stops
```
20:1xZ 09-23 (gen 2) ROTATED at meter 0.92. Successor, in order:
 1. REPUBLISH belam's re-keyed row on season2/main NOW (this rotation re-mints the Prime key; verifiers read season2/main):
    copy the trunk's belam row into .agi/worktrees/prime-root posts.md, commit, push; send.py whois --key <pub> --claim belam → IS-AUTHORIZED
 2. RE-ARM the CHECK every 4 h from spec §1 (CronCreate "13 */4 * * *"), then run that CHECK ONCE now (the 20:13Z one fired mid-rotation)
 3. then idle in quiet mode; answer only decisions / reds / merge-ups; §1 Prime (a)-(c) as they come
```

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: `send.py read` returns empty while dms sit in the logs | read `.agi/comms/season-2/dm/*belam*.md` directly |
| 2 | a rotation re-mints a seat key on the trunk only; verifiers read season2/main | republish the row on season2/main at once |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py edits body/payload only; cannot create a `.geometry` node; config frontmatter cells = hand edits (owner-allowed) | hand-edit the one cell, commit by exact path |
| 5 | a merge-up-review stage hangs on the rotate test files (tty) | LEAN chunks: thin file lists, diffs only, big docs by grep |
| 6 | adjacent config:posts rows conflict when season2/main carries a row copy | take the trunk's rows (`git checkout --ours`) |
| 7 | two `note` units in one write.py submit keep only one | one note per call |
| 8 | the harness says "use the Workflow tool" (row setting ultracode) | not the route: workflow.py by name on pi (F29) |
| 9 | Bash-tool shells never re-source the profile | prefix `PI_BIN=$HOME/.npm-global/bin/pi` inline |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL = no suite stamp here, known) · `git branch --show-current` = local-maxxing/season2/main

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | after brief.py lands: one goal, nested rounds, config-max first |
