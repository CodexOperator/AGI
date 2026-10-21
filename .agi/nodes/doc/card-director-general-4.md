---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board. CARRIED CARD for the G6 move: the new session starts from this file.

## §0 State (10-21 22:3xZ, carried)
| | |
|---|---|
| post | director-general-4 (builder under sanctuary-master = SM). At G6 I become director-general-2 (same agent, uid stays mine, old key retired, fresh key minted at first start, NEW Claude session). The role of the new row is whatever SM's brief and the posts.md row say: read both before acting |
| matrix now | goals post = director-goals-1 (was DG1, G3) · science post = director-science-1 (was DG2, G4) · director-general-1 = the ex-DG3, builder/media (G5; the old name director-general-1 for the goals post is gone) · director-general-3 has no live row until G7 (ex-DG5) · until G6 a send to director-general-2 is off-matrix. Mail only names with a live row |
| running | NOTHING: no suite, runner, dispatch, build, review, council round. No session cron. Quiet rule: never box belam, only SM, one message per finished thing ([red] and blocking owner asks excepted) |
| skills | agi-rotate · agi-send · agi-verify · agi-goal · agi-post (+ agi-review / agi-dispatch only if SM dispatches) |
| worktrees | /var/lib/agi/director-general-4/t (detached = posts/director-general-4) only is live. Old locked w-* (boardlog pins ownrow fixrunner capsule2 capsule3 board3 close2 close3) are ON the trunk; w-board2 dbbfb2e2a6, w-capsule a0a86ef159, w-roll 4113ada851 are SUPERSEDED history (clean). Nothing in them is owed; remove by path only if asked. w-s1/w-s2 released |
| scratch | pytest --basetemp, TMPDIR, lane temp, gate trees: ONLY /data/work/gate-director-general-4 (700, my uid; the dir name follows the uid owner, check after the move); home and /tmp are on the ROOT disk. One heavy lane at a time, niced, only above 3 GiB MemAvailable |

## §1 Plan
```
OPEN TIPS: NONE. Every tip of mine is on the trunk (core/season3/main 0aa49b525f at 22:3xZ; checked with merge-base --is-ancestor).
  g5.4.1 S1 = L33 50d5ce0673 (tip dg4-s1 c6b536bcc8) · S2 = L50 7696f541dc (tip dg4-s2 94af29d0d8) · S2 follow-up = L51 (tip dg4-s2f f773ecba96, on the trunk). Branch refs kept as history.
NOT PLACED, DO NOT START: g5.4.1 S3 = (P5) the rollover-skill line, the agi-season-report skill the owner asked for 10-16, the season-3 backfill. SM sends it as its own [design] when it is wanted. Season 3 report exists as template + facts reader + render + doc node (season_report.py facts|refresh-facts|render; template extensions/agi/templates/season_report/report.html; fixtures extensions/agi/tests/fixtures/season_report/; tests test_season_report.py).
NEXT 1: tell SM move-ready (card sha + "open tips none"), then WAIT for SM's per-post GO for G6. Nothing moves before it.
NEXT 2 (after the GO and the new session): read box, check `git rev-parse core/season3/main`, and answer only what SM places. First check the credential helper before any push: git config --global --get-all credential.https://github.com.helper (trap 114); no push is planned.
```

## §2 Landed (one line each; SM gates and lands, belam merges up)
```
10-21  L33 50d5ce0673 S1 (template + facts reader) · L50 7696f541dc S2 (refresh-facts, render, doc node P3/P4) · L51 f773ecba96 S2 follow-up (event = commit recomputed or exact re-runnable read; every box value prints a dagger + legend)
10-15  SEASON 3 ROLLED (apply rc 0 by belam 06:21-06:24Z); live trunk core/season3/main; landings only through SM (LAND_TRUNK=refs/heads/core/season3/main)
before: .42 E + fix-forwards, .44.1-.6 capsule, runner-uid pin, boardlog, pins, close2/close3, rollover stack 20 (all on the trunk)
SHUFFLE (goal:g7.16.1.11.45, owner GO 10-21 14:45Z, council 3/3): G3 L52 ba8faaad3a DG1->director-goals-1 · G4 L55 8a9d18ec9c DG2->director-science-1 · G5 L57 69e36d2286 DG3->director-general-1 · NEXT G6 me DG4->DG2 · G7 DG5->DG3
```

## 🔴 Where it stops
```
Waiting for: (1) SM's per-post GO for G6. (2) Nothing else is owed by me.
Rename "design B": uid stays mine; old key retired; fresh key at first start under the new name; the moved home starts a NEW Claude session, so THIS CARD is the resume path. Card doc node keeps its mint id (doc:card-director-general-4 may be renamed by SM's rows; follow the quorum link).
FIRST ACT on resume: AGI_POST=<my post name now> box read | fold -s -w 200 ; send only with a stdin heredoc (an arg-only send arrives EMPTY). A RETURN on a cut = ONE new signed commit ON the sent sha in the matching worktree; `agi-at <path>` ONLY in the main checkout.
```

## §4 Traps (inherited 4 already moved to skills; the rest here move at the next rotation, SM may name their homes)
| trap | rule |
|---|---|
| mail (owner 10-11) | NEVER box belam; to SM one message per finished thing, no [ack]/[thanks]/[landed]; only [red] or a BLOCKING owner-ruling ask at once |
| the sha in a box message | `git rev-parse HEAD` FIRST, then compose the heredoc with it inline |
| home literals | belam's guard knows EVERY seat's home: grep the added lines AND the message for /var/lib/agi/<name>, /home/, /data/home; a crons row writes `~/...` |
| new CLI verb | a subparser in a bin needs a commands.md entry (manifest: or excluded: + reason): run test_commands_manifest.py before sending |
| scanned sites | a new update-ref / commit-tree / mktree / hash-object -w / fetch moves test_grid_writers pins: run it before sending |
| old trunk spelling | `local-maxxing/season2/main` may be spelled only in test_season_rollover_global.py (box-move-refs lane) |
| tests | pin the runner uid (never assert on the uid running pytest); every row has a one-edit mutant that must go RED |
| shell | no broad `pkill -f` / `pgrep -f` (killed my shell); `sleep N` then another command is blocked, use an until loop; cwd resets, use absolute paths |

## §5 Verification
Last green (season_report): test_season_report suite on the L51 tip; test_commands_manifest (`_OUTSIDE_CLIS` names facts, refresh-facts, render) · test_grid_writers · test_anonymize_guard · test_boxkit_templates in the S2 gate lanes. Re-run before any new cut, bare env, niced, one at a time.

## §6 BANKED
- S3 shape (P5 + skill + backfill) and the song question (owner said generate each time; no generator exists) wait for SM's [design].
- `capsule move` is box-move.sh's caller work, not a verb (council); the capsule residues (custom cron `log:` outside `~/logs/` neither capped nor mkdir'd; `in` transports refs/grid verbatim) are named, not fixed.
- A machine identity in the box ring (heal / memory-alarm senders) is banked with belam for S3: the owner's call.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
