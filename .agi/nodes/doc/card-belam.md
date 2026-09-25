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

## §0 State (02:1xZ 09-25)
| | |
|---|---|
| post | belam-S2-L5-V gen 5 · seated 00:44Z 09-25 · Opus 5.5 · meter ~0.20 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC |
| PASS 5 | RUNNING since 02:02Z (state `pass_started_at`) · trunk synced 5b7d503fa7 (season2/main ee13b9564a merged in, clean) · PIN TIP 5b7d503fa7 · OS ee13b9564a · BASE 3b0c4e8e8f → 449 commits · 39 exp · 18 rounds (15 hyp + 3 engine-delta) · 4 chunks (5/5/4/4) on pi-free, launched 02:02-02:05Z · Monitor bqugxyvyu on `/tmp/belam-pass5/events.log` |
| directors | director-engine + director-thought, claude-sonnet-5 max · `doc:unified-director-brief` §1: ONE parent per round, `--tier parent --role parent --ladder-tier 0` |
| stream | LIVE on Twitch + X · PAUSED by stream-master's `brb` ~02:04Z (its `pgrep -a` printed relay keys into its own tool output; never the capture) · `back` = the owner's · relay target delay 15m00s (owner: ~2 min) · `brb` for every post (`~/.local/bin/brb`) · `panic` the owner's (`/usr/local/bin/panic`, TM 02:0xZ) |
| dms | [owner] brb notice → TM/DE/DT/SM · in: TM [owner] 02:03Z (panic on PATH; `back` granted to TM for its own brb) · SM [red] 02:04Z → answered [decision] hold |
| lanes | credits 13.75 (01:59Z) · parents + kids pi-free · mint floor 1 USD |
| crons | CHECK 4f4c68c7 "13 */4 * * *" (next 04:13Z) · PASS 5 one-shot 7f0c852a fired 01:59Z (consumed) · retired belam panes hold no crons (gen 4 cancelled 7ce06676) · SESSION-ONLY |

## §1 Plan
```
done   seated · crons re-armed · quorum re-linked · owner stream line: [owner] dm x4, ~/.local/bin/brb, doc:unified-head
       line E (+ relay-argv clause after SM's red) · PASS 5 steps (0)-(3)
next   PASS 5 (4)-(9) at ALL DONE · then the OWNER'S JEV ASK: did the Jev existing-tools exploratory run happen
       (thought-master, g5.24.3; PASS round lm-jev-cua-off-the-shelf-survey-* in chunk 4) + any Jev in today's
       trove survey -> did it yield results -> owner report
open   round-mur ROUTED to director-engine as a WORKFLOW (behind g1.25) · residues with director-engine · §6
```

## §2 Landed (this seat)
f6dd6dad92 card at seating + quorum re-link · 5b7d503fa7 trunk sync (season2/main key row, clean) · HEAD stream line + card (this commit)

## 🔴 Where it stops
```
02:1xZ 09-25 belam-S2-L5-V: PASS 5 running (4 chunks on pi-free); stream held by stream-master's brb, back is the owner's.
 1. At ALL DONE in /tmp/belam-pass5/events.log: python3 /tmp/belam-pass5/verdicts.py (-v for every round) = step (4).
 2. Step (5) in .agi/worktrees/prime-root: pull --ff-only, merge-tree preview, merge --no-ff 5b7d503fa7, verify, push, grid commit --all (background).
 3. Steps (6)-(9) as section 2 of .agi/sessions/prime-merge.crons.md; then the owner's Jev ask (§1 next).
 4. A successor at wake: RE-ARM the CHECK (§1 verbatim); pass_started_at is SET, so resume PASS 5 from /tmp/belam-pass5 (runs mur-p5chunk*), never relaunch; re-link the quorum (trap 10); write this card whole.
```
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the logs too when a post says it wrote |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text (defect minted) |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py body numbering can differ from file lines | `sub <old> => <new>` (literal); never ` && ` inside a unit |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py via sync.sh: temp index + ff-only, never a conflicted MAIN |
| 7 | two `note` units in one submit keep one; a body writer cannot share a submit with `thought` | one body writer per submit, `thought` alone |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi / pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | diff vs the doc node, `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit both by exact path |
| 11 | a Prime row edit on season2/main is reverted by that post's next key-row publish | the post merges origin/season2/main and confirms the cell (defect minted) |
| 12 | `cd` moves the session's working directory | absolute paths, `git -C`, subshells |
| 13 | the stream is LIVE | never print a secret, key, address or host name; one shows → `brb` |
| 14 | `.env` on local-town is `/data/work/agi/.env` | read credits from the MAIN root |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 16 | background writes of many nodes outlast the 120 s Bash timeout | pass a timeout |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 18 | at rotation a director reads HEAD + card, never the template | rules in doc:unified-director-brief; cards carry overrides only |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 20 | asking the owner for a go on a design the owner raised | decide, route, report · a workflow needs no hypothesis |
| 21 | a write.py sub whose OLD text holds the arrow token writes garbage | assert it absent; else replace the paragraph |
| 22 | a RETIRED pane's hook captured this LIVE card + spawned rotate-self --force for the seat (gen 4 01:59Z, its own f=0.4794; refused: behind 1) | rewrite the card whole; a retired pane cancels its own crons (gen 4 did) |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys (SM 02:04Z) | never print a process argv broadly; `pgrep -c` / `-x` only |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| stream `back` after stream-master's brb (02:04Z) | the owner's; keys never reached the capture per SM |
| Twitch/X stream keys passed through a model context (SM 02:04Z) | rotate them at leisure |
| retired belam panes I-IV + agi-98 still alive (a numeral-chain window is not reaped) | reap, or keep for the stream -- the owner's call; none holds a cron |
| global git identity on this box (box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | trigger met (brief.py b0b4fbc9b); opening it is the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
| thought-master beyond the director docs (goal moves / config) | config:* stays prime/owner-only; a scoped grant is a director-engine round |
