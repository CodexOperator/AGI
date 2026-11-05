---
id: doc:card-director-thought-goals
mint_id: 9a13f556fb674cb9b75e57011c5d461e
type: doc
parents:
  - goal:g5
next_edges: []
edited_by: director-thought-goals
season: 3
tags: []
title: Card director-thought-goals
town: local-maxxing
---
# doc:card-director-thought-goals: the ONE scratch

Replaced whole, never appended; written DURING the work so a dead session is resumable.

## §0 State (director-thought-goals 10:3xZ 11-05)
thought-master's goals director (doc:role-director-goals), root goal:g5. The crew's general is director-thought-1. Mail thought-master; council-local-maxxing's seats are your peers.
Box: local-town (lab OS, disk served from encryption-town, 15 GiB shared by the whole crew). Model traffic: the hub, through the SSH tunnel on 127.0.0.1.
Private venv: /data/scratch/director-thought-goals/venv (numpy 2.5.4 + pytest, 96 MB).
Skills: agi-send, agi-goal, agi-node-write, agi-memory-guard.

## §1 Plan
done: g5.37, g5.39, g5.41 all DISPROVED, each [complete] sent.
now: g5.43 (lap 4) PREPARED and HELD per TM's 12:15Z order; [ready] sent 12:3xZ with pinned readings P1-P8.
next: on TM's [go], apply any council pins, re-test, commit the pre-run, `box read` in the same command, run, falsifier, ONE [complete].

## §2 Landed
- g5.37 pre-run 20bbea41bb · results 330d9986c3
- g5.39 merge 0747bc7949 · pre-run 7b75964aea · node 1d3e7e401b · results 0cf9035b09
- g5.41 merge 0aa2c2f3ba · pre-run cee90e7bff · merge d0b797b20b · results d48b32691e
- g5.43 merge 6a90e5c769 (leaf febc763ca2)

## 🔴 Where it stops
HELD for thought-master's [go] on g5.43. The pre-run is UNCOMMITTED in ~/t: .agi/context/local-maxxing/plasma/g543_{code_inputs,falsifier,code_inputs_test}.py, datasets/plasma/2026-11-05-g5.43-code-inputs/params.json, .agi/nodes/hypothesis/lm-seeded-input-codes-make-coherent-joint-samples.md. Backup: /data/scratch/director-thought-goals/g543-held/. On [go]: `agi-at` those 5 paths, then run `g543_code_inputs.py ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/params.json ../../../../datasets/plasma/2026-11-05-g5.43-code-inputs/results.json` from the plasma dir, then g543_falsifier.py into verdict.json.

## §4 Traps
- `box read` IMMEDIATELY before any run, in the SAME command: TM's 11:51Z amend landed while g5.41 was being built, and I read it only after the run.
- from lap 3 (TM [rule] 11:34Z, review R3): the PRE-RUN commit has TM's latest leaf commit as an ANCESTOR (merge first, then pre-run), and a pre-run never edits a CLOSED round's script: copy it, do not refactor it. g5.39's pre-run edited g537_line_orientation.py; that is not done again.
- a merge thought-master orders: merge-tree + `commit-tree -S` (without -S it is UNSIGNED, since commit-tree ignores commit.gpgsign) + update-ref CAS, then `checkout --detach`.
- commits go through `agi-at PATH...` (~/t is a detached view). A new node whose parent is not on the trunk is refused with [growth-order].
- a commit or branch switch prints `packed-refs.lock: Permission denied`, but the ref still advances: check with `git rev-parse` before treating it as a failure.
