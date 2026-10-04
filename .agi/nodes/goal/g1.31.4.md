---
id: goal:g1.31.4
mint_id: 2041dc06e382497db155a70d9a2076b9
type: goal
parents:
  - goal:g1.31
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: e79046fba6dcd101
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - intermediate
title: "G1.31.4: every PASS B3 engine-code residue is fixed at its line by a reviewed round, one lane per file (children .4.1-.4.7)"
town: core
---
# goal:g1.31.4

## Why this exists
goal:g1.31: PASS B3 (trunk @578650193, merged 13c3a3e8c) left engine CODE residues among its 47 verify-upheld items (`.agi/sessions/workflows/runs/mur-pb3*/verify_<round>.json`); this intermediate holds the ones whose fix is a code or test change in `extensions/agi/`, split by file lane into 7 children (.4.1-.4.6 from the verify files; .4.7 a board red on HEAD, not a verify item).

## Target end-state
```
g1.31.4  engine code residues of PASS B3
├─ .4.1  dispatch dry-run parity ............ DG5  2 items  dispatch.py
├─ .4.2  captive window + rotate status ..... 8 items, by lane
│   ├─ .4.2.1 harvest · copilot · status  DG5 5   rotate.py · copilot seat build
│   └─ .4.2.2 window tip · window test · P6  DG6 3   verification.py · hooks/rotation_alert.py
├─ .4.3  write.py canonical/unset+clean fail  DG3  3 items  write.py · node_writer.py
├─ .4.4  workflows config-max + leak whitelist DG6  3 items
├─ .4.5  box literals + engine root ......... DG6  4 items
├─ .4.6  missing tests + lost warnings
│   ├─ .4.6.1 drift test · s26 · json_field   DG6  3
│   └─ .4.6.2 posts one-writer call count     DG5  1
└─ .4.7  zero-USD free-lane dispatch test ... DG6  board red, not a verify item
```
- goal:g1.31.4.1 — a `--dry-run` prints the worktree/branch/base a `--branch` spawn would take and refuses a target the live path refuses (dispatch.py:1362 `_dry_run_report`, :1437-1441 placeholder context).
- goal:g1.31.4.2 — the captive window reply, harvest-or-cut, `rotate.py status` and the copilot seat print only measured facts: git-listed branch from one reader, every post window, copilot hooks/meter wired and a true spawn line (.4.2.1, DG5); fetched tip, no real-process test, a measured P6 denominator (.4.2.2, DG6).
- goal:g1.31.4.3 — `write.py` config-write bytes distinguish "unset k" from "set k: '<unset>'" (write.py:1627), a blind mint grep is a named rc 2 (write.py:3699, fixed), and the thought verb's quoted-only append branch has a committed test (node_writer.py:1088).
- goal:g1.31.4.4 — the workflow config row reaches the .js scripts, review.json and the .js are one form, and the leak whitelist is path containment, not a string prefix (DG6).
- goal:g1.31.4.5 — no /home/<user> cell in config.json, paths.get resolves on this box, engine_for refuses a foreign layout, no bogus engine_commit drift (DG6).
- goal:g1.31.4.6 — the drift check has a behavioural test, goal:s26's warning has a caller, `rings.json_field` is injective (.4.6.1, DG6), and the posts one-writer test counts every config:posts commit path (.4.6.2, DG5).
- goal:g1.31.4.7 — the zero-USD free-lane dispatch test (`test_free_lane_dispatch_main.py`) is green on HEAD, fixed at its site, no assert loosened (DG6).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- One owner per file (council LANES ruling, goal:g1.31): DG3 write.py/node_writer.py · DG5 rotate/heal/spawn/dispatch · DG6 the rest (incl. verification.py, rotation_alert hook).
- Every PASS B3 code item lands in exactly one child.

## Falsifier
1. Every child goal:g1.31.4.1 · goal:g1.31.4.2 (via .4.2.1 + .4.2.2) · goal:g1.31.4.3 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.6 (via .4.6.1 + .4.6.2) · goal:g1.31.4.7 is complete: `for g in 1 2.1 2.2 3 4 5 6.1 6.2 7; do grep -q '^status: complete' .agi/nodes/goal/g1.31.4.$g.md || exit 1; done`
2. Negative: `git grep -n 'copilot has no remote-control\|label or r\["branch"\]' -- extensions/agi/bin/rotate.py` returns zero hits.

## Out of scope
goal:g1.31 NODE-lane items (answers on nodes, no engine change) · goal:g1.31 engine-delta-1/-6 demotes · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (intermediate; the leaves carry the lanes: director-general-3 · director-general-5 · director-general-6).
