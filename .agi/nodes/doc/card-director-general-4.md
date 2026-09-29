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

## §0 State (00:0xZ 09-30) — gen 1; council RESUMED 23:4xZ (owner: "Restart council including DG5 stand up")
| | |
|---|---|
| post | director-general-4 · g7.16.1.6 FILL-IN (.6.2 writers) side by side with DG3's machinery + the leftovers lane |
| protocol | doc:council-loop (read its "council's lens" + Handoff) · goal:g7.16.1 · MAIN `<repo>` on local-maxxing/season2/main, CC Opus 5.5 high |
| split | FINAL in room directors 23:5xZ, agreed DG3 agi-6b · DG4 agi-47 · DG5 agi-c8 -- the room line is the source, this is a pointer |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | write.py · node_writer.py · loader.py · links.py · viewport.py (DG3) · rotate.py spawn/launch paths, dispatch.py, heal.py key path (DG5) |
| shared file | "[claim] <file>" in room directors before editing rotate.py / heal.py / dispatch.py / write.py; "[release] <file> <sha>" after the by-path commit |
| route up | to belam: merge-up · decision · rotation · red · rule only. Directors: SendMessage + room directors. Council: room council-loop |

## §1 Plan
```
WAIT  DG3 posts node_writer.commit_node(root, node_path) -> sha (CAS on refs/grid/<mint>) + refusal modes in room directors
S6.2  re-point every node-commit site onto commit_node, one site per commit:
        rotate.py commit sites incl. W1c (goal:g4.18.5.3: _ack_commit_seats · _publish_row_to_authority · _commit_spawn_row ·
          _commit_stops_row -> ONE _commit_posts_row; plan doc:card-director-general-3 §6) · rotate.py:9237 + :12177 grid commit --all
        cli.py 3 · season.py 2 · sensei.py 1 · send.py 1 · dashboard.py 1 -- measure each: a NODE write moves, a round/branch commit stays
S6.3  grid cron retired: crons.py:898 grid_sync line + grid.py:1831 cron -> ONE ~15-min snapshot job (cadence cell with DG3) · Falsifier 1
        measured 00:0xZ: the crontab carries the 5-min grid commit line TWICE (crons.py show lines 5 + 19)
LEFT  L2a(a) unify.py + verify_unified.py after DG3 BUILD1 (manifest.<key> row verb): files + 4 build nodes + 2 manifest rows, ONE commit
      L2a(b) publish-engine.sh + the g7.10 hook alarm (test the hook with the alarm removed first; it runs in EVERY session)
OPEN  L1b check_goal_lifecycle (council places) · belam [decision] g15/g26
```

## §2 Landed
- e1d710942 L1: 8 horizon parents over an active leaf -> active · walk 468 = 306 active / 77 horizon / 47 complete / 38 retired
- 259d75164 L2c: orphan THOUGHT END 6 -> 0
- 6a913d85d (+39 write.py commits) L2b: repo path 92 -> 10 live nodes (the 10 excluded by rule)
- room directors: the FINAL split (23:5xZ)

## 🔴 Where it stops
Waiting on DG3's commit_node signature in room directors. At wake: read room directors + council-loop, `send.py read director-general-4` once; if the signature is up, start S6.3's measurement-to-edit on crons.py (not shared) first.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 8 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock flaps; PASS B3 on the box | write.py leaves writes uncommitted while held; ONE test file per run |
| replace body anchor guard | a mid-paragraph range is refused; widen to paragraph bounds, never --force |
| `thought` verb | rewrites the FIRST column-0 THOUGHT pair: check for a fenced / second BEGIN first |
| config:commands | rows live in FRONTMATTER under `manifest:`; unset is top-level only until DG3's BUILD1 |
| crons.py show | prints the box's home log path -- never paste its output into a node, dm or room |
| council invariant | no parent/kid dispatch; every node through write.py; nothing deleted |

## §5 Verification
links.py links 5165 / 0 broken · orphan THOUGHT END 0 · repo path in live nodes 10 (excluded by rule)

## §6 BANKED
1. g15 retired over 32 active leaves, g26 over 1 -- sent to belam as [decision], rec re-parent to g1.
2. g6.49 active over 3/3 complete leaves -- no Falsifier on it or its leaves; completing it needs one written first.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The council resumed with a new lane: the directors (DG3/4/5 only) agreed the split themselves by SendMessage; after crossed amends on W1c, DG3's last text won (both DG3 and DG5 acked it), so rotate.py is split by function: its commit sites are DG4's, its spawn/launch paths DG5's.
<!-- THOUGHT:END -->
