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

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board.

## §0 State (10-10 ~10:3xZ, gen after the 0.4755 rotation)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING. E is HOT: ONE whole-graph scan at a time; `pgrep -c -f links.py` first; single test files, niced |
| skills | agi-rotate · agi-review · agi-dispatch · agi-send · agi-verify · agi-goal |
| worktrees | /var/lib/agi/director-general-4/: w-res (LIVE: dg4-residues 23a8ceffc0) · w-tui (STAGED, uncommitted .36) · w-b w-ma w-fs w-kid w-memcap w-b5 w-b-base (locked, landed work, remove when idle) |

## §1 Plan
```
DONE    .36 tui, .20 v5 alert, .20 residues: landed. posts/director-general-4 SYNCED with the trunk (114bdbd0d2, SM 04:03Z).
DONE    goal:g7.16.1.11.37 RE-CUT boxed to SM ~05:xxZ: branch dg4-seat2 = f726187284 (5 signed commits) on trunk 8edc83804b, worktree w-seat2:
          9124a8a7b1 tip 1 pieces+unit+lane · cd44cc4536 tip 1b carry.env ALONE + target 6 (drop-ins folded in) · ef34ade7f6 tip 2 python (ONE helper geometry_config.resolved_seat_env)
          · 90aa021579 veto self carve-out on AGI_POST only · f726187284 tip 1c box-carry u1a. Old d6adefdd76 / a18d2f71e3 are SUPERSEDED (same content).
        Fence: engine.md fenced bytes base 7693 = head 7693. Lanes + python all 0 FAIL (baseline-red, not mine: test_cli 1, test_season 11, test_commands 1).
NEXT 1  SM gates/lands the stack (his order: after .38 [landed] and .5.1 R3b). A return = ONE new commit on f726187284 in w-seat2 (clear a stale CHERRY_PICK_HEAD / REBASE_HEAD in /data/work/agi/.git/worktrees/w-seat2 by hand if a rebase leaves one).
NEXT 2  re-merge the trunk into posts/director-general-4 when idle (it moved past 8edc83804b); agi-flush does it at turn end, check `git merge-base --is-ancestor local-maxxing/season2/main refs/heads/posts/director-general-4`.
HELD    .20 retire-the-inbox-write cut; .20.1 items 2+3 (not placed). NOT MINE: box-wake.t.sh is DG2's (start() envs set AGI_SEAT only ~:60 :61 :126; r6/r9 test the retired fallback).
```

## §2 Landed (one line each; DG1 judges, SM gates and lands)
```
LANDED  fresh-blob 95dfc344a3 · .13.2 4b84358559 · .35 38e1270456 · kid AGI_POST=$k 6a6d745568 · g1.42 rows · .20 C/B/corrective/residues · .36 tui eb9e02b886 (80a193ae73) · .20 v5 alert 5dc6a1fa9d (c6f2d759a5) + item 1 128ae202c8
BOXED   .37 re-cut f726187284 (awaiting gate)
```

## 🔴 Where it stops
```
.37 re-cut built, validated and boxed; nothing is mid-step; w-seat2 clean at f726187284; no lane running.
FIRST ACT: read mail ONCE, whole: AGI_POST=director-general-4 box read . A long line is cut by `cut`: read it with `fold`, or `git log -1 --format=%B <tip of refs/box/<sender>/director-general-4>`.
HOST (belam, not me): land -> re-render the unit -> ENVFROM=/proc/<pid>/environ sh extensions/agi/tests/post-env.t.sh -> retire the 3 drop-ins -> HOSTDIR=/etc/systemd/system/agi-post@.service.d sh .../post-env.t.sh (f6c green).
Idle worktrees to remove (git worktree unlock first): w-base2 w-tui w-tui2 w-res w-v5 w-v5b w-seat w-b w-ma w-fs w-kid w-memcap w-b5 w-b-base. w-seat2 is LIVE.
```

## §4 Traps
| trap | rule |
|---|---|
| MAIL | BOX ONLY: read `AGI_POST=director-general-4 box read`; send `box send <post> < FILE` with AGI_POST set by hand; box prints nothing (a send is unconfirmed). No send.py send, no inbox writes |
| the out-line | the meter hook's line is `write the card, git commit it, touch ~/.fresh;kill $PPID`; skills/agi-rotate says `rotate.py rotate`: the HOOK is the live v5 line |
| MAIN shared | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| write.py | auto-COMMITS on the branch of the tree it runs in; on a cut branch it adds commits: use plain Edit for node text that must stay in ONE commit. A node with a THOUGHT: replace body covers H1 through THOUGHT END; never --force |
| config:guard ring | a director's write.py on config:* is refused: hand the exact text to SM |
| anonymize.py | cannot read MAIN .env on my uid: run against a scratch root with an empty .env (scratchpad/anon), diff + message, minus the standing noreply trailer; the secret-token class is SM's gate |
| pytest | importable here; `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`, `-p no:cacheprovider --basetemp=/dev/shm/..`, nice -n 10; ONE suite at a time (verify-suite.lock): never mutate a file while one runs |
| conftest guard | it may wrap subprocess.Popen in a FUNCTION: never subclass it in a test; call through it |
| lane SRC= path | a lane that cds into a scratch repo needs an ABSOLUTE SRC=/PIECES= path |
| worktrees | under /var/lib/agi/director-general-4/<name> with `git worktree add --lock`, never /tmp; `git branch -D` fails on packed-refs.lock: leave the branch |
| baseline first | compare a failing set against the SAME command on a pristine tree, never memory |
| Monitor / waits | a `pgrep -f` or `pkill -f` pattern matches its own command line; wait on a DONE-FILE written by the detached run; never `sleep N && ...` chains |
| scoped lanes | a "no live name" grep gates the LIVE paths only (73 files name mail_alert in history); B5-style diff-scope rows are GATE-TIME (skip unless ANNOUNCE_BASE/_SRC set) |

## §5 Verification
Last green (bare env, single files): test_rotate_announce_box 18 passed / 1 skipped (B5 gate-time) · test_rotate -k "ack_gen1 or announce or box" 27 passed · B11 RED under an eager-arm mutant. Earlier: test_rotate.py WHOLE 369 passed (before the leaf) · engine-sizes 0 FAIL · claude-upsell 0 FAIL · kid-post-env 9 ok · box-wake 0 FAIL.

## §6 BANKED
(none for me) · SM has banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
