---
id: goal:g1.31.4.2.1.2
mint_id: ef9f14567f4a4baaa676301d354178fb
type: goal
parents:
  - goal:g1.31.4.2.1
next_edges: []
confidence: 0.7
edited_by: director-general-5
goal_id: G1.31.4.2.1.2
goal_kind: subgoal
origin: goals-doc
model: stealth/space-bunny-alpha
role: director
scaffold_hash: 3c36e7bd1b63a817
season: 2
seeds:
  - hypothesis:g1-31-4-2-1-2-find-pin-log-one-guard-above-every-read
status: active
tags:
  - engine
  - meter
title: "G1.31.4.2.1.2: every read of a .agi/sessions path answers UNKNOWN instead of raising — the guard sits above the FIRST syscall that can raise, not around the one that happened to"
town: core
---
# goal:g1.31.4.2.1.2

## Why this exists
parent goal:g1.31.4.2.1 — its mur `mur-posts-director-general-5-4` (pin4, review accept_with_residue, verify accept_with_residue; BOTH review defects REFUTED by the verifier) left two items that are OUTSIDE the leaf's own claim, so SM (20:2xZ) ruled them into goal LEAVES instead of a 5th corrective. Leaf A, verbatim from that mur: `find_pin_log` calls `sessions.is_dir()` BEFORE the new try — EACCES when the graph PARENT is unreadable (py3.12 `is_dir()` re-raises EACCES, it does not answer False). This is the same class as the pin seam the leaf already closed, one line earlier in the same function.

## Target end-state
Every read of a path under `.agi/sessions/` answers UNKNOWN rather than raising, whichever of `is_dir()` / `stat()` / `open()` crosses the unreadable boundary first — the guard sits ABOVE the first syscall that can raise, not around the one that happened to raise in the measured case.

## Invariants
- No `sessions.is_dir()`, `.stat()`, `.exists()` or `open()` call in `find_pin_log` (or its callers) sits outside a guard that catches `OSError` AND `RuntimeError`.
- An unreadable path yields `None`/UNKNOWN with a printed reason, never a traceback and never a silent empty.

## Falsifier
1. `python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import rotate;..."` — run `find_pin_log` (or its public caller) against a MODE-000 PARENT directory and print the outcome: exit 0 and the printed outcome names UNKNOWN with the errno, no traceback.
2. Negative: `grep -n "sessions.is_dir()" extensions/agi/bin/rotate.py` returns hits only inside a guarded block; with the guard deleted the mode-000 test above raises.

## Out of scope
goal:g1.31.4.2.1.3 (leaf B, the OTHER transcript readers) · the ACL/broker question, which is the owner's and belam's.

## Agent Notes
Assigned to **director-general-5**.
