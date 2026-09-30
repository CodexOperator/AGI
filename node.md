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

## §0 State (00:3xZ 09-30) — gen 1; council RESUMED 23:4xZ (owner: "Restart council including DG5 stand up")
| | |
|---|---|
| post | director-general-4 · g7.16.1.6 FILL-IN (.6.2 writers) side by side with DG3's machinery + the leftovers lane |
| protocol | doc:council-loop (read its "council's lens" + Handoff) · goal:g7.16.1 · MAIN `<repo>` on local-maxxing/season2/main, CC Opus 5.5 high |
| split | FINAL in room directors 23:5xZ, agreed DG3 agi-6b · DG4 agi-47 · DG5 agi-c8 -- the room line is the source, this is a pointer |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | write.py · node_writer.py · loader.py · links.py · viewport.py (DG3) · rotate.py WHOLLY incl. W1c + its commit sites, dispatch.py launch, heal.py key path (DG5) |
| shared file | "[claim] <file>" in room directors before editing heal.py / dispatch.py / write.py; "[release] <file> <sha>" after the by-path commit |
| route up | to belam: merge-up · decision · rotation · red · rule only. Directors: SendMessage + room directors. Council: room council-loop |

## §1 Plan
```
WAIT  commit_node(root, node_path, content=None, *, payload=None, prefix) is POSTED in room directors (00:0xZ) but built only after the council places g7.16.1.6 and DG1 mints its leaf: council -> DG1 -> DG3 -> DG4
S6.2  re-point every NON-rotate node-commit site onto commit_node, one site per commit:
        MEASURED 00:0xZ: of 8 non-rotate commit sites ONE is a node write -- send.py:796 keygen --all-live (config:posts via a temp
        index; told DG3: commit_node must take content); cli.py x3 · season.py x2 · sensei.py x1 stay (round / merge / sessions), dashboard.py:631 no commit
        (rotate.py's commit sites, W1c and its :9237/:12177 grid commit --all calls are DG5's)
S6.3  grid cron retired: crons.py:898 grid_sync line + grid.py:1831 cron -> ONE ~15-min snapshot job (cadence cell with DG3) · Falsifier 1
        measured 00:0xZ: the crontab carries the 5-min grid commit line TWICE (crons.py show lines 5 + 19)
LEFT  L2a(a) DONE b8d232fc6 (+ rows 4b2d2d2d1, 9b671709a)
            L2a(b) DONE de5507a17 (goal:g7.16.1.4.1.1 met for all three tools; its status is DG1/council) -- publish-engine.sh + g7.10 hook alarm (both hook copies, tested first) + grid.py cron --publish-engine +
        crons.py publish_engine job (KNOWN_JOBS, _require_dir) + config:crons cadence (removed BEFORE the code) + commands grid.py:cron
        row (20097eada) + metrics.py PUBLISH_STATE_PATH + test_publish_alarm.py + 2 build nodes -> ONE by-path commit after the pass
OPEN  L1b check_goal_lifecycle (council places) · belam [decision] g15/g26
```

## §2 Landed
- e1d710942 L1: 8 horizon parents over an active leaf -> active · walk 468 = 306 active / 77 horizon / 47 complete / 38 retired
- 259d75164 L2c: orphan THOUGHT END 6 -> 0
- 6a913d85d (+39 write.py commits) L2b: repo path 92 -> 10 live nodes (the 10 excluded by rule)
- b8d232fc6 L2a(a): unify.py + verify_unified.py retired whole (rows first, via DG3 BUILD1) -- SM ACCEPT wf_40b19c77-7f2; note closed 393992bbf
- de5507a17 L2a(b): publish-engine.sh retired -- SM accept_with_residue wf_35fe675a-d5b; residue 116 (section 6 = the only push-gap coverage) closed 481ecfde6, SM verified CLEAN (test_push_gap.py 26p + build:tests-test-push-gap); F2 exclusions on goal:g7.16.1.4.1 routed to DG1 inbox
- 0d2ace8b8 hypothesis:node-type-schemas-name-a-thought-reader-that-exists (DG2 fork via DG3): 16 schema bullets one text, reader test globs schemas (19p, negative red); +2 disclosed lines; F1 pointer wording (L1.05 vs g7.16.1.4.1) with DG2 inbox
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
| foreign hunks | `git diff` EVERY file before a by-path commit: b8d232fc6 swept DG3's uncommitted guard edit (DG3 counted it landed) |
| row verb | `row manifest.<key> <file>` (empty file = remove); manifest keys keep their YAML colon (`unify.py:`), cadences do not |
| crons.py apply runs from MAIN every 5 min | change config:crons and crons.py in the order that is valid under BOTH: remove from the node first |
| crons.py show | prints the box's home log path -- never paste its output into a node, dm or room |
| council invariant | no parent/kid dispatch; every node through write.py; nothing deleted |

## §5 Verification
links.py links 5165 / 0 broken · orphan THOUGHT END 0 · repo path in live nodes 10 (excluded by rule)

## §6 BANKED
1. g15 retired over 32 active leaves, g26 over 1 -- sent to belam as [decision], rec re-parent to g1.
2. g6.49 active over 3/3 complete leaves -- no Falsifier on it or its leaves; completing it needs one written first.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L2a(a) landed on DG3's BUILD1 and L2a(b) went into its test pass; the version adds three traps paid for tonight (a swept foreign hunk, the row verb's key grammar, the config-before-code order a live 5-min cron forces).
<!-- THOUGHT:END -->
