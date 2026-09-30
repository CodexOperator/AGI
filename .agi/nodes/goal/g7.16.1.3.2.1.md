---
id: goal:g7.16.1.3.2.1
mint_id: 2d43ab50f2154f86bb6cc75d82ca706d
type: goal
parents:
  - goal:g7.16.1.3.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: ba0763f2a14ae1d7
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.1: rotation-record dump/resolve and parked_carriers live in ONE shared module that rotate, heal, sensei, write and verification import by public name; heal never swallows ImportError on a record write (row H4 part 1; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.1

## Why this exists
goal:g7.16.1.3.2 (row H4), part 1. Bundle 1-2 rounds left the rotation record's I/O as private functions in rotate.py (`_dump_record`, `_resolve_record_path`) that other modules reach into, and verification.py's `parked_carriers` is imported by write.py for the set-active drop, so write.py imports the verifier. Measured 17:2xZ 09-29: write.py:2369 `import verification` (for `verification.parked_carriers`) · heal.py:872 and :1031 call `_rot._dump_record` · sensei.py:576-591 call `rotate._resolve_record_path` (4 sites) · heal's record write sits in `except (OSError, ImportError)` ("never raises"), so a missing module silently skips the record.

## Target end-state
- ONE small shared module holds the record dump/resolve and parked_carriers. rotate, heal, sensei, write and verification import it by public name.
- heal never swallows ImportError on a rotation-record write: a missing module fails loudly.

## Invariants
- Rotation records write and resolve byte-identically before and after the move.

## Falsifier
1. `git grep -nE '\._(dump_record|resolve_record_path)\b|from rotate import _' -- extensions/agi/bin` prints only the shared module's own definitions (the bundle goal's `rotate\._` form misses heal.py:872 and :1031, which call `_rot._dump_record` through an alias; measured 17:4xZ), and `git grep -n 'import verification' -- extensions/agi/bin/write.py` prints 0.
2. Negative: heal.py's record-write paths catch OSError only: `git grep -n 'except (OSError, ImportError)' -- extensions/agi/bin/heal.py` prints 0 on those paths.

## Out of scope
goal:g7.16.1.3.2.2 · goal:g7.16.1.3.2.3

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 3, stage 1, 17:2xZ 09-29) from goal:g7.16.1.3 row H4. Re-measured after the crash re-seat (17:4xZ): Falsifier 1 widened to any `._dump_record` / `._resolve_record_path` attribute reach, because heal.py imports rotate as `_rot` (heal.py:872, :1031) and the `rotate\._` grep printed 0 while two cross-module private calls stood. Today's reach: sensei.py 6 sites, heal.py 2, rotate.py's own 11.
<!-- THOUGHT:END -->
