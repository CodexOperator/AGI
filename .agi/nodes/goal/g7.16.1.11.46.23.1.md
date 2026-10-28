---
id: goal:g7.16.1.11.46.23.1
mint_id: 211152233c39485b992924586b502b85
type: goal
parents:
  - goal:g7.16.1.11.46.23
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.46.23.1
goal_kind: subgoal
origin: goal
seeds: []
tags:
  - V8a
  - verify-land
season: 3
status: active
title: "G7.16.1.11.46.23.1: verify-land admits a ruled code delete ONLY by path from a BASE-read land.deletes_admitted cell (sets, not counts), with rename detection pinned (-M) and a node delete never admitted"
town: local-maxxing
---
# goal:g7.16.1.11.46.23.1

## Why this exists
goal:g7.16.1.11.46.23 (V8a, the R-land / verify-land land checks): L154 (director-general-3's seat_status.py retire, owner ruling (3), council GO 3/3 09:45:46Z 10-26) carried ONE code delete, extensions/agi/bin/seat_status.py, and the installed verify-land held it (`verify-land: HOLD (D)`; its line 18 holds ANY D with no knob). The council landed it as a one-off on that hold (alive gen 21 [decision] 09:55:09Z 10-26, 3/3: all-is-one 09:51:35Z + 09:53:15Z, self-perpetuating 09:51:33Z + 09:54:06Z) and made the general case THIS leaf, so the next ruled code delete needs no one-off. Measured on L154's range: `git diff --name-status` gives D 1 by default and D 4 with `-c diff.renames=false` (both retired build nodes + the ported test), so today's count depends on the lander's git config.

## Target end-state
- verify-land admits a D only for a path listed in .agi/config.json `land.deletes_admitted: [{path, ruling}]`, read from BASE (`git cat-file blob BASE:.agi/config.json`), never from TIP. The cell sits on land.rules_paths, so adding an entry is itself an earlier wrapped, belam-signed land.
- SETS, not counts: every D path must be in the cell by path; one admitted path never covers another deleted path. Readings: `D admitted: <path> (<ruling>)` per admitted path; `admitted but not deleted: <path>` for a stale entry (a reading, not a hold). Each entry is removed after its land.
- Rename detection is PINNED: `git diff -M --name-status` in the installed verify-land's D line AND in extensions/agi/guard/verify-land.sh (the copy the re-pin installs), so the D set does not depend on diff.renames.
- A D under .agi/nodes/ is NEVER admitted, listed or not (retire, never delete: a retire is an R into deprecated/).

## Invariants
- A range cannot admit its own delete (the cell is read from BASE).
- Every check still runs to the verdict; an admitted D adds a reading, never removes another hold.
- Until this lands, a ruled D lands only as a council-named one-off on the [landed] (the L154 shape).

## Falsifier
1. extensions/agi/tests/verify-land.t.sh rows, each RED under its mutant: the cell read from TIP (a tip listing its own delete) -> HOLD; an unlisted D -> HOLD; path a/ listed, b/ deleted -> HOLD; diff.renames=false in the env -> the SAME D set as the default; a listed node D (under .agi/nodes/) -> HOLD; a listed code D at BASE -> OK with `D admitted: <path> (<ruling>)`.
2. negative: `git grep -n 'name-status' -- extensions/agi/guard/verify-land.sh` shows no D-reading diff without `-M`.

## Out of scope
goal:g7.16.1.11.46.23's other rows; the R-land mode flip (the council's, after a lap); any change to what counts as a RULES path (land.rules_paths, landed in L150).

## Agent Notes
Assigned to **belam**.
