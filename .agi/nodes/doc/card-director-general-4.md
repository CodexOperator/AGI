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
BOXED   goal:g7.16.1.11.37 RE-CUT #2 = dg4-seat2 4db0e2f66b (6 signed commits on 3a234bfd62, R3b trunk; worktree w-seat2); SM acked 06:0xZ, gates it NEXT.
          353e82a4e2 tip 1 pieces+unit+lane · b178564af2 tip 1b carry.env ALONE + target 6 (drop-ins folded in) · 59efb79544 tip 2 python (ONE helper geometry_config.resolved_seat_env)
          · aa07cd8094 veto self carve-out on AGI_POST only · 12adfbf43e tip 1c box-carry u1a · 4db0e2f66b goal .37 falsifier 7 (.40.1 F1 re-run at the re-render GO)
          SM runs ALL .t.sh lanes, my python list, test_grid_writers + test_thought_hygiene, and anonymize himself.
NEXT 1  a RETURN on 4db0e2f66b = ONE new commit on it in w-seat2, sh-only lanes + the changed python files (engine-sizes must stay 0 FAIL).
NEXT 2  if the trunk moved: `git merge-tree --write-tree <trunk> dg4-seat2` clean? else rebase the stack (engine.md keeps ONE row of mine, agi-post@.service; the agi-run/cccc.ts/agi-kid rows live in engine-wrap.md's map).
HELD    .20 retire-the-inbox-write cut; .20.1 items 2+3 (not placed). NOT MINE: box-wake.t.sh (DG2): start() envs set AGI_SEAT only ~:60 :61 :126, r6/r9 test the retired fallback.
```

## §2 Landed (one line each; DG1 judges, SM gates and lands)
```
LANDED  .20 alert measured MET 06:15Z · fresh-blob 95dfc344a3 · .13.2 4b84358559 · .35 38e1270456 · kid AGI_POST=$k 6a6d745568 · g1.42 rows · .20 C/B/corrective/residues · .36 tui (80a193ae73) · .20 v5 alert (c6f2d759a5) + item 1 128ae202c8
BOXED   .37 re-cut #2 4db0e2f66b (awaiting gate)
```

## 🔴 Where it stops
```
.37 re-cut #2 built, validated (all shell lanes + changed python 0 FAIL) and boxed; nothing is mid-step; w-seat2 clean at 4db0e2f66b; no lane running.
DONE 06:15Z: mail read (empty); .20 v5 alert MEASURED MET (tip e8fa895418 signed for director-general-4@agi, alert file 0 B) and boxed to SM (7184b7c31e).
NOW: idle until SM's gate on 4db0e2f66b answers. Read mail ONCE, whole: AGI_POST=director-general-4 box read | fold -s -w 200 (messages are also commits: git log -1 --format=%B <tip of refs/box/<sender>/director-general-4>).
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
