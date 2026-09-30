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

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (02:4xZ 09-30) — rotating at f≈0.43 after goal:g7.16.1.5.3 landed
| | |
|---|---|
| post | director-general-4 · FIRST PRIORITY (belam 02:xZ, owner verbatim on the goal): goal:g7.16.1.5.3 worktree cleanup · then g7.16.1.6 fill-in · leftovers lane |
| protocol | doc:council-loop · MAIN `<repo>` on local-maxxing/season2/main (working files on the RAM disk since 01:41Z; .git + .agi/worktrees on disk) · CC Opus 5.5 high |
| messaging | owner verbatim: "use internal messaging only for everything and full guarantee until bundles land" -- SendMessage by session name (ListAgents) ONLY; NO send.py, NO rooms. Prime = agi-c2 (re-check: names change at every restart) |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | write.py · node_writer.py · loader.py · links.py · viewport.py (DG3) · rotate.py, dispatch.py launch, heal.py key path (DG5) |
| peers | DG5 = tmux window director-general-5 (row window @10 at 02:2xZ; session name changes on restart); DG3 at @8 |

## §1 Plan
```
g7.16.1.5.3  BUILT 873fec43f -- heal sweep ARCHIVES then prunes (refs/archive/worktrees/<name>, dirty -> <name>-dirty via a throwaway
             index; --force only behind verified refs; pass deferred under mem/io PSI; <= reaper.worktree_archive_per_pass per pass)
   OPEN a) takes effect when heal's watch RESTARTS -- a Prime/owner act on the live box; ~1015 trees / 25 per pass ~ 40 passes
        b) the census row for sweep liveness (the goal's "a row of the census") -- not built
        c) Falsifier 2 after the restart: 0 "[sweep] refused ...: unmerged" lines in heal's log; Falsifier 1: git worktree list -> live rounds
        d) DG5 [release] of heal.py not delivered (its session renamed) -- the commit message carries it; tell DG5 by window name
   NEVER du/find over .agi/worktrees (io storm) -- git worktree list
g7.16.1.6    WAIT: council places .6 -> DG1 leaf -> DG3 builds commit_node(root, node_path, content=None, *, payload=None, prefix)
             DG4 then: send.py:796 keygen onto commit_node; crons.py:898 grid_sync + grid.py cron -> ONE ~15-min snapshot job
OPEN         DG2 verdict on hypothesis:node-type-schemas-name-a-thought-reader-that-exists (0d2ace8b8; F1 pointer L1.05 vs g7.16.1.4.1)
             DG1: drop goal:g7.16.1.4.1 Falsifier-2 exclusions; g7.16.1.4.1.1 complete? (both sent by send.py inbox -- re-send by SendMessage)
             council: L1b check_goal_lifecycle placement · walk mismatches in bundle trees (g4.18.5.1 · g7.16.1.1 · .1.2 · .1.7 · g6.49)
```

## §2 Landed
- e1d710942 L1 goal markers · 259d75164 L2c THOUGHT END · 6a913d85d L2b repo-path scrub (82 nodes)
- b8d232fc6 + de5507a17 L2a: unify.py / verify_unified.py / publish-engine.sh retired (SM clean: 393992bbf, 481ecfde6 test_push_gap.py)
- 0d2ace8b8 schema "Readers strip it" bullets · f27b84d7f fe2e775e6 989782c9d cec3b9af5 g15/g26 (belam decision a)
- census (read-only) eeccfbaa1 bypass: 303 legacy parent-rule violations, 0 provably bypass-minted
- 8d053818e heal's resume posts-row write committed alone before the ack
- 873fec43f goal:g7.16.1.5.3 archive-then-prune sweep (heal_sweep 28 · heal_watch 88 · heal 23 · help 70+8s)

## 🔴 Where it stops
g7.16.1.5.3 built at 873fec43f, awaiting heal's watch restart by the Prime; next: re-send DG1/DG2 notes by SendMessage, then the census row (b).
Next command at wake: ListAgents, then SendMessage to agi-c2 asking whether heal's watch restarted; if yes, `tail -200` heal's log for "[sweep] archived" / "deferred" lines.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared | commit by exact path; `git diff` EVERY file for foreign hunks first (b8d232fc6 swept DG3's hunk) |
| verify-suite.lock | a guard that PRINTS but does not stop is no guard (de5507a17): `if lock; then stop; fi` |
| tests + box PSI | heal sweep tests stub `_sweep_pressure_ok` (autouse): the real box io PSI would defer every pass |
| row verb | `row manifest.<key> <file>` (empty = remove); manifest keys keep the YAML colon, cadences do not |
| crons.py apply runs from MAIN every 5 min | change config and code in the order valid under BOTH |
| heal's ack instruction | `--gen` is refused for non-prime posts: `rotate.py ack --post director-general-4 --session <id> --ref <ref> continue` |

## §5 Verification
links 5270 / 0 broken · grid 0 errors · heal tests above

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Rotation card: after the reboot the owner made worktree cleanup first priority and it landed (873fec43f); what is left needs the Prime's heal restart, so the successor starts from its evidence.
<!-- THOUGHT:END -->
