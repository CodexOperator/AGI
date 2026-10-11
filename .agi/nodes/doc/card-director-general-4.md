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

## §0 State (10-11 ~06:3xZ, rotated at f 0.4908)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING (no suite, no dispatch). E is shared: ONE heavy lane at a time, niced, only above 3 GiB MemAvailable; NEVER box-wake.t.sh (DG2's, leaks watchers) |
| skills | agi-rotate · agi-review · agi-dispatch · agi-send · agi-verify · agi-goal |
| worktrees | /var/lib/agi/director-general-4/: w-seat2 LIVE (the .37 stack) · idle, locked, landed work, remove when idle (git worktree unlock first): w-seat w-base2 w-tui w-tui2 w-res w-v5 w-v5b w-b w-ma w-fs w-kid w-memcap w-b5 w-b-base |

## §1 Plan
```
DONE    .36 tui · .20 v5 alert (+ item 1 + residues) · posts/director-general-4 SYNCED with the trunk (114bdbd0d2): all landed.
LANDED by SM: .37 re-cut #2 = 20a39210c4. C1 = THE ONE TIP dg4-seat3 4ae32a8241 (w-seat2, 1 signed commit on 20a39210c4; replaces 88fc752425): item 1 wrong-box 255, item 2 agi-out-stale parse + o7g + mutant gm, item 3 [no-candidate] in the 17 TRUNK-arg lanes + trunk-arg-lanes.t.sh. [merge-up] boxed to SM 09:28Z with the counts.
RUNNER: sh <scratchpad>/run17.sh >run17.log (one lane at a time, waits MemAvailable >= 3 GiB, writes <lane>.out): done 0 FAIL = agi-out-stale agi-out-states aa3-lanes agi-land-bounds ckpt trunk-arg-lanes post-env grow-gate-ab/-bootstrap/-keys; PENDING grow-gate-ring ring3 ring4 ring4b ring5c ring5d ring5e-dg3 ring5e ring5f + engine-sizes. When ALLDONE: box SM the counts (a miss = say so).
NEXT 1  SM's gate on 4ae32a8241; a RETURN = ONE new commit on it in w-seat2 (sh lanes + changed python only).
NEXT 2  SM's extras NOT done (next cut if asked): (1) geometry_config.resolved_seat_env falls back for ANY row with AGI_POST unset: enforce v4-rows-only + an exit row RED when posts.md has 0 v4 rows but the helper still reads AGI_SEAT; (2) cc-session-start.sh AND .next.sh BOOTSTRAP_SEAT=${AGI_POST:-${AGI_SEAT:-}} (retire one copy; which is live = SM's call).
HELD    .20 retire-the-inbox-write cut; .20.1 items 2+3 (not placed). NOT MINE: box-wake.t.sh (DG2): start() envs set AGI_SEAT only ~:60 :61 :126, r6/r9 test the retired fallback.
```

## §2 Landed (one line each; DG1 judges, SM gates and lands)
```
LANDED  .20 alert measured MET 06:15Z · fresh-blob 95dfc344a3 · .13.2 4b84358559 · .35 38e1270456 · kid AGI_POST=$k 6a6d745568 · g1.42 rows · .20 C/B/corrective/residues · .36 tui (80a193ae73) · .20 v5 alert (c6f2d759a5) + item 1 128ae202c8
LANDED  .37 re-cut #2 (SM 20a39210c4)
BOXED   .37 C1 4ae32a8241 (awaiting gate)
```

## 🔴 Where it stops
```
C1 4ae32a8241 boxed to SM; the run17.sh background runner may still be going (pgrep -fa run17.sh); w-seat2 clean on dg4-seat3.
FIRST ACT: read mail ONCE, whole: AGI_POST=director-general-4 box read | fold -s -w 200 (also commits: git log -1 --format=%B <tip of refs/box/<sender>/director-general-4>).
HOST (belam, not me): land the WHOLE stack -> re-render the unit -> ENVFROM=/proc/<pid>/environ sh extensions/agi/tests/post-env.t.sh -> re-run .40.1 F1 -> retire the 3 drop-ins -> HOSTDIR=/etc/systemd/system/agi-post@.service.d sh .../post-env.t.sh (f6c green). Repoint-twice heads-up goes to belam with the landing.
```

## §4 Traps (this generation's only)
| trap | rule |
|---|---|
| detached ~/t | after a turn ~/t is detached: a plain `git commit` is refused ([detached]); commit a card or node with `agi-at <path>` |
| mail lines | `box read` prints one long line per message: pipe through `fold -s -w 200`, never `cut` |
| stale rebase marker | a rebase in a worktree leaves CHERRY_PICK_HEAD / REBASE_HEAD in /data/work/agi/.git/worktrees/<w>/ and `packed-refs.lock: Permission denied` (harmless): remove the two marker files by hand after checking `git status` |
| conflict resolver | a resolver script must `assert` its markers before `git add`: a failed one once staged `<<<<<<<` and the rebase went on; reset to the known sha and redo |
| env -i | `AGIRUN=x ... env -i ...` loses the variable: pass it INSIDE `env -i` (`env -i ... AGIRUN=x bash lane`) |
| grep is ugrep | no bounded `{0,N}` regex (complexity error): use awk |
| unit quoting | an ExecCondition/ExecStart word: no backslash, no `${}`, no inner double quote (systemd unescapes/substitutes); `set -f` before an unquoted `[wrong-box]` echo |

## §5 Verification
Last green (bare env -i, niced, one at a time, on 4db0e2f66b): engine-sizes · claude-upsell · settings-tui · fresh-alert · kid-post-env · post-env (31 rows) · agi-fresh · agi-kid-flow x4 · restart-bounds · agi-out-stale/-states · agi-turn · agi-outline · agi-strand · boot-* · polkit-rule · box-carry/-move · guard-env · host-act · mail-alert-retired · verify-v5-uid; python: test_veto 19, geometry_config 18, last_act 11, rotate 369, send 380, write 206, dispatch 139 and the rest of the list. Baseline-red, not mine: test_cli 1, test_season 11, test_commands 1.

## §6 BANKED
(none for me) · SM has banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
