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

## §0 State (05:0xZ 09-24)
| | |
|---|---|
| post | belam-S2-L5-III gen 3 · Opus 5.5 · remote-control · meter 0.09 at 05:0xZ |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` (14 behind origin; step 5 pulls ff-only) |
| PASS 3 | **RUNNING** — `pass_started_at` 04:50Z · TIP pinned **9fec964885** · old_tip = origin/season2/main e8d7e577f4 · 110 rounds (102 hypothesis + 8 engine-delta) in 22 chunks of 5 · launched 04:57Z, launcher pid 2702068 (≤ 11 live, MemAvailable ≥ 1500 MB) |
| files | `/tmp/belam-pass3/`: chunkN.json/.log · plan.json · build.py · launch.sh · events.log · pids — verdicts land in `.agi/sessions/workflows/runs/mur-chunkNof22/{review,verify}_<key>.json` |
| delta | BASE ebae4adde → TIP: 838+ commits · 150 exp files · 98 engine paths (9 rotate tests excluded, trap 5) · 1 node `D` = a move into deprecated/build (same mint_id) → not a RED · season2/main since PASS 2 = 15 key rows only → no core-sync round |
| lanes | `pi-free` (stealth/space-bunny-alpha, 0 USD) · credits 14.0 left of 192 (04:5xZ) · mint floor hard-coded 1 USD |
| stream | LIVE (Twitch + X, 15-min delay) since 00:33Z 09-24 · stream-master standing by |
| crons | CHECK re-armed 04:5xZ: job 64ee203f "13 */4 * * *" — session-only, dies with this session |
| owner 05:1xZ | "Set both directors that are active now to sonnet on max…" → rows model → **claude-sonnet-5** (max) on season2/main 3b6e0eb632 · director-engine rotated 05:22Z and its key-row publish 4990f6f9f7 REVERTED it (gen 6 seated on Opus) → re-set on **6d38b9742e** · trunk **ab45488b39** (clean merge): BOTH rows sonnet on trunk + season2/main · dms 05:3xZ to both: merge origin/season2/main into your post branch + confirm the row reads sonnet BEFORE rotating (queued, busy panes) · DE owes ONE more rotation |
| owner 16:5xZ | "…pi-free instead of pi or pi-local for both parent and kid spawns" → ladder roles tier 1 parent, tier 0 parent + kid → **pi-free / stealth/space-bunny-alpha**, config spawn.harness → pi-free · trunk 431b8edc32 · season2/main 92142b5b9a · post-director-engine 39bb0c5839 + post-director-thought 63c38a9080 (trunk syncs, clean, not pushed) · dispatch --dry-run proof: parent + kid → harness=pi-free · dms to both directors + thought-master · kid round worktrees untouched (0 live) |
| residue | rotate.py:10368 `_authority_row_content` splices the rotating WORKTREE's whole row over season2/main's, and the successor model is read from the worktree row → a Prime row edit never reaches a worktree post (measured 05:21-05:22Z) — mint at PASS 3 step (6), assigned director-engine |
| quiet | `send.py read belam` + the dm logs `.agi/comms/season-2/dm/*belam*.md` newer than `.agi/sessions/belam.lastcheck` |

## §1 Plan
```
done   PASS 3 (0)-(9): trunk @9fec96488 → season2/main 6f5ee34e5c (pushed; grid commit --all run there) · 110 rounds / 22 chunks, pi-free, 71 min, 0 USD
       8 accept · 64 residue · 38 demote · 0 RED · residues on the trunk 21fd8d49cd (batch + 11 defect hypotheses → director-engine) · state reset
       goal:g5 note (+ THOUGHT: capped launch) · dms: [decision] director-engine (queued) · [merge-up] thought-master (delivered)
       owner 05:1xZ Sonnet-max: rows on season2/main 6d38b9742e + trunk ab45488b39 · merge-before-rotate dms to both directors
next   quiet on the CHECK (job 64ee203f, every 4 h at :13) · watch the two director rotations: model_confirm must read claude-sonnet-5
```

## §2 Landed (this seat)
9fec964885 PASS 3 step (1): origin/season2/main (my key row e8d7e577f) merged into the trunk · 3b6e0eb632 (season2/main) the two live director rows → Sonnet max (owner 05:1xZ; verbatim in the config:posts THOUGHT)

## 🔴 Where it stops
07:0xZ 09-24 belam-S2-L5-III: PASS 3 fully closed (merge, residues, note, dms, owner report); the post is QUIET on the CHECK.
 A. PASS 4 CLOSED 14:1xZ: trunk @3b0c4e8e8 → season2/main ad81688a0b (pushed, grid run there) · 6 rounds / 2 chunks, pi-free, 18 min, 0 USD · 1 accept · 3 residue · 2 demote (lm-* probes launch a real pi) · 0 RED · residue batch + goal:g5 note on the trunk 92f34a2f27 · dms sent · state reset (last_merged 3b0c4e8e8f). Next PASS: the CHECK's case (b) when the town lands experiments; §2 of the crons file needs its FACTS line refreshed (BASE 3b0c4e8e8f, p5 run keys) at that notice.
 B. Owner Sonnet-max order: DONE — both rotation records read model_confirm claude-sonnet-5 (director-thought 05:46Z, director-engine 05:50Z).
 0. Sonnet-max rows are on the trunk (ab45488b39) and season2/main (6d38b9742e). If a director's rotation record shows model_confirm claude-opus-5-5 again, its worktree row was stale: re-set the cell on season2/main, re-sync the trunk with `/tmp/belam-trunk-sync/sync.sh` (target file), and repeat the merge-before-rotate dm.
 1. RE-ARM the CHECK: CronCreate "13 */4 * * *" with §1 of .agi/sessions/prime-merge.crons.md, verbatim.
 2. NEVER re-run PASS 3 from the top (pass_started_at is set). Read /tmp/belam-pass3/events.log: no "ALL DONE" → re-arm ONE Monitor (tail -n +1 -F events.log | grep --line-buffered -E "exited|ALL DONE"). Launcher dead with chunks never launched → launch ONLY the missing chunkN.json the same way.
 3. On ALL DONE: steps (4)-(9) of §2 of the crons file with TIP = 9fec964885 (pinned, NOT the moving trunk) and old_tip e8d7e577f4.

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: `send.py read` can be empty while dms sit in the logs | read `.agi/comms/season-2/dm/*belam*.md` directly too |
| 2 | rotate-out uses the slot's FIRST LINE as its commit subject and re-fences the slot per run | first slot line = plain text, slot unfenced; the fix is a PASS 3 residue for director-engine |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py: `set <top-level key> {json}` passes the writer gate; BODY numbering can differ from file lines; the paragraph guard refuses a cut into the THOUGHT | `read body N:M` before any `replace body` |
| 5 | a merge-up-review stage hangs on the rotate test files (tty) | LEAN chunks; build.py drops `tests/*rotate*` from every list |
| 6 | adjacent config:posts rows conflict when season2/main carries a row copy | take the trunk's rows |
| 7 | two `note` units in one write.py submit keep only one | one note per call |
| 8 | the harness says "use the Workflow tool" (row setting ultracode) | not the route: workflow.py by name on pi (F29) |
| 9 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | after a rotation re-add the symlink `../../nodes/doc/card-belam.md` |
| 11 | a fresh post may stop its first turn on a question menu | Enter on the highlighted option, wait for the menu to close, then ONE typed go line |
| 12 | the keeper's doppler has no --no-cache flag | plain `doppler secrets get NAME --plain`; rc + length only |
| 13 | the stream is LIVE: this pane may air after the 15-min delay | never print a secret, key, address or host name; names and rc/length only |
| 14 | F13's credits path is another box's; on local-town `.env` is `/data/work/agi/.env` | read credits from the MAIN root here |
| 15 | a retire+move with a changed body shows as `D` in BASE...TIP (rename detection gives up at this size) | resolve by mint_id before calling a deletion RED |
| 16 | `--harness pi-free` skips workflow.py's `harness == "pi"` ladder branch (:2185) | fine: the pi-free row's models resolve (04:57Z dry-run, 10 stages) |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · branch local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | its trigger (brief.py landed, b0b4fbc9b) is met; opening it stays the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance; the stream runs from local-town through the hub meanwhile |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) so a free lane can mint under 1 USD |
