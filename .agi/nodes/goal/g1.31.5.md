---
id: goal:g1.31.5
mint_id: 8e5a6d5782ff45d184144cee2555c869
type: goal
parents:
  - goal:g1.31
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: f594a226df0db7f4
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - intermediate
title: "G1.31.5: every REAL PASS B3 missed row (58, triaged of 147) is fixed at its line or answered on its node, 14 leaves; DUP/FIXED/FALSE/OWNER disposed"
town: core
---
# goal:g1.31.5

## Why this exists
goal:g1.31: each of PASS B3's 40 verify files (`.agi/sessions/workflows/runs/mur-pb3*/verify_<round>.json`, gitignored, on the Prime's box) carries a `missed` array: 147 reviewer-found rows in all, beside the 47 upheld items that goal:g1.31.1-.4 hold. No row was adversarially verified, so every row was triaged against HEAD 7ca035b18 (triage table `/tmp/dg6/missed/triage.json`: verdict · lane · cluster · severity · cite per row) and the REAL ones were re-cited at d4b7ead17. 59 rows were REAL. On re-check the NODE drafter moved n142 to DUP (same node and line as goal:g1.31.3.1.1 #46), so this node holds 58 REAL rows in 14 leaves.
```
verdict    REAL 58 · FALSE 55 · DUP 24 · FIXED 6 · OWNER 4        (=147; n142 REAL -> DUP)
REAL/lane  NODE 33 · DG6 16 · DG5 6 · DG3 2 · DG4 1
REAL/sev   red 3 · residue 25 · nit 30
```

## Target end-state
```
g1.31.5  PASS B3 missed rows: 58 REAL, 14 leaves
├─ .5.1  RED: reds first, one leaf per lane and cluster
│   ├─ .5.1.1  DG6  1  n19            agent-git hook fails closed on a failed diff
│   ├─ .5.1.2  DG6  2  n112 n88       email class + forward scrub; skills/ in guard scope
│   └─ .5.1.3  DG4  1  n83            _commit_write never commits a same-path hand edit
├─ .5.2  DG3  2  n60 n84              one posts parser in the guard test; one parked:<goal> spelling
├─ .5.3  DG5  6  n33 129 130 139 76 107   rotate.py + heal.py
├─ .5.4  DG6 engine residues
│   ├─ .5.4.1  6  n17 74 21 66 146 147   config-max literals
│   ├─ .5.4.2  4  n47 56 73 108          tests/
│   └─ .5.4.3  3  n2 75 104              one-source + probe
└─ .5.5  NODE answers (write.py only), 33 rows, 6 leaves .5.5.1-.5.5.6
```
- goal:g1.31.5.1: the 3 reds are closed. The agent-git hook refuses when `git diff --cached` fails (.5.1.1). No tracked node carries an email address and `anonymize.py` has an email class (.5.1.2). A write.py commit never carries a hand edit it did not make (.5.1.3).
- goal:g1.31.5.2: `test_write_self_row.py` parses through the one line-anchored parser, and the `parked:<goal>` tag is built in one place (`rotation_record.py`).
- goal:g1.31.5.3: in rotate.py and heal.py the announce sees every post session, the cut line, prompt, worktree path and model defaults come from cells, the heal comments name the real mechanism, and the 3 strict-xfail placeholders are green for real.
- goal:g1.31.5.4: the grid lock, deprecated dirname, scope deny-list, drafting note and ifeval paths are config cells. Dead test code is gone, the leak guard has its own tests, and no test reads the live checkout. The drift rule has one source, `brief._strip_thought` is pinned by a test, and the copilot flags are probed.
- goal:g1.31.5.5: 33 node rows are answered on their nodes through `write.py`: scrub THOUGHTs, scrub damage, scaffolds, stale cites, verdict roll-ups, goal shapes.
- DUP 24 add no leaf. Each row goes onto its goal:g1.31.1-.4 leaf as evidence: g1.31.1.1 n71 · g1.31.1.2 n69 n91 · g1.31.2 n86 n87 · g1.31.3.1.1 n142 · g1.31.3.1.2 n92 n105 n126 · g1.31.3.2 n120 n133 n134 · g1.31.4.1 n26 · g1.31.4.2.1 n131 n136 · g1.31.4.4 n64 n65 n67 n85 · g1.31.4.5 n44 n45 n110 · g1.31.4.6.1 n123 n124.
- FIXED 6 (n23 27 41 72 79 111) and FALSE 55 add no leaf. Each row's evidence or reason is in the triage table.
- OWNER 4 (n6 `<repo>` placeholder vocabulary · n22 + n109 scrub restamped `edited_by` · n144 are user names in the guard's scope) are banked in director-general-6's card §6 BANKED, never leaves.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Every REAL row lands in exactly one leaf: 58 = 1+2+1 + 2 + 6 + 6+4+3 + 33.
- One owner per file, and per function where a region is granted (SM 09-30: `write.py _commit_write` is DG4's).
- A node is edited only through `write.py`. A node is retired, never deleted. History is never rewritten here: a leak is scrubbed forward, and any history rewrite is the owner's call, routed to the Prime.

## Falsifier
1. Every child is complete: `for g in 1.1 1.2 1.3 2 3 4.1 4.2 4.3 5.1 5.2 5.3 5.4 5.5 5.6; do grep -q '^status: complete' .agi/nodes/goal/g1.31.5.$g.md || exit 1; done`
2. Negative: `git grep -nE '[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}' -- .agi/nodes/experiment/a00-75e7c869-24b9f0.md .agi/nodes/experiment/a01-4a4d8f92-b02a7a.md .agi/nodes/experiment/a01-9bc63860-d97453.md .agi/nodes/experiment/a00-9f8f7f3e-99d092.md` returns zero hits (8 lines at HEAD d4b7ead17).

## Out of scope
goal:g1.31.1 · goal:g1.31.2 · goal:g1.31.3 · goal:g1.31.4 (the 47 upheld items; DUP rows only add evidence there) · the 55 FALSE and 6 FIXED rows · the 4 OWNER rows (banked) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (intermediate; the leaves carry the lanes: director-general-3 · director-general-4 · director-general-5 · director-general-6).
