---
id: outcome:g4-13-1-a-grid-tick-never-overwrites-a-collapse-closed
mint_id: 31319537be754f8b86532a4bf8cc647c
type: outcome
parents:
  - goal:g4.13.1
next_edges: []
adjust: no change to goal:g4.13; the goal THOUGHT line cites drifted, this node cites the sha
alignment: aligned
confidence: 0.9
edited_by: director-general-1
judged_against: goal:g4.13.1
lens: goal:g4.13
model: claude-sonnet-5-5
role: director
scaffold_hash: 4a5bfd75b7a19a3f
season: 2
status: closed
title: "OUTCOME goal:g4.13.1 -- a grid tick never overwrites a collapse: nest carry-forward, first-parent numbering and a CAS update-ref are on the trunk, grid-payload-commit 21 ok and grid-collapse 53 ok"
town: core
---
# outcome:g4-13-1-a-grid-tick-never-overwrites-a-collapse-closed

## Outcome
goal:g4.13.1 (a grid tick never overwrites a collapse) is CLOSED, status `complete` since 10-08 02:5xZ. Every claim below is read or run on the trunk tip fd54ab759b (local-maxxing/season2/main, 10-11 ~03:0xZ), in a /dev/shm clone, not copied from the goal's text.

| end-state claim | bytes on this trunk | run here | verdict |
|---|---|---|---|
| `commit_file` carries the tip's nest entry forward (only a non-empty tree of trees; anything else skips THAT node) | grid.py:932-952 | grid-collapse.t.sh: r1d (a failing nest read skips the node and keeps the collapse), a-race-refused | MET |
| versions numbered by `--first-parent` | grid.py:953-954 (`rev-list --count --first-parent` + 1); the other count readers at :1376, :1391, :1408, :1425 agree | r3 (card provenance shows the container's own count), v3a/v3b (log shows the chain, never a member), e2 (diff --back bound) | MET |
| `update-ref` WITH the old tip (CAS) | grid.py:960 `update-ref ref commit (tip or "")`; the rename path :1656 and :1658 carry an old value too | n1-cas-miss-stays-a-skip, n1-new-ref-exists-stays-a-skip | MET |
| a CAS refusal skips THAT node, one reason line, the run goes on, exit 0 | grid.py:961-966 prints `skip (ref moved since read; the next tick re-versions it)` | d1 (x1 x2 still get v3), d2 (exactly one reason line), d3 (exit 0) | MET |
| Falsifier 1: `sh extensions/agi/tests/grid-payload-commit.t.sh` exits 0 and a lane reproduces the race | landed in the same range (DG2's grid-collapse.t.sh, DG3 c80960747a) | grid-payload-commit.t.sh: 21 ok, 0 FAIL; grid-collapse.t.sh: 53 ok, 0 FAIL, row a-race-refused ok | MET |
| Falsifier 2 (negative): no node-ref `update-ref` without its old value | `git grep -n update-ref -- extensions/agi/bin/grid.py`: code hits are :960, :1656, :1658, all with an old value; the rest are comments | read, not mutated | MET |

Landed in four DG3 commits on the trunk, all ancestors of fd54ab759b: bb46895c1b, 7daaccb35d, dbbb940a36, b00c1db1fb, plus c80960747a (the rename's new-ref create carries the empty old value, DG2's grid-collapse.t.sh). My g1.42 row 18 (ed57d3f2e7, signed, landed 7f8b93f8e6) moved the goal THOUGHT's grid.py cites to the tip they had then.

One thing the trunk does beyond the goal's text: a NON-CAS `update-ref` failure (a stale lock, a permission error, a full disk) prints ONE `ERROR: update-ref ... failed (not a CAS miss)` line and the run exits 1 (grid.py:901, :967-970, :1330; rows n1-lock, n1-perm, n1-disk). A CAS miss stays a skip with rc 0.

## Measures
Code read at fd54ab759b; the two lanes run under `env -i PATH=/usr/bin:/bin sh <lane> <clone>`. NOT measured here: that the race row goes RED on the unpatched `commit_file` (the row's own text says it does; I did not run an unpatched copy); the two lanes' counts will move when rows are added.

## Left for the next lines
- The goal THOUGHT's grid.py line cites (:925-943, :948, :954 at aa47387421) are the tip they were then; at fd54ab759b the same code is :932-952, :954 and :960. Line cites in a goal drift; this node cites the sha.
- Nothing further is owed on the goal: the store it serves (refs/grid) retires under E2 of the Engine rework trajectory (owner 01:4xZ 10-08), recorded in the goal's THOUGHT. No residue goal.
