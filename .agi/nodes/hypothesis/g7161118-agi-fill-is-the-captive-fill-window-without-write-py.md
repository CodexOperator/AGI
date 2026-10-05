---
id: hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py
mint_id: 3ad727c565eb4ec9961afb4c4463a984
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "`sect agi-fill` (the python in config:engine-grow) is the captive fill window without write.py: open with a matrix nid and matching parent types prints FILL WINDOW OPEN and writes the window file (rc 0); open with that nid and wrong parent types prints `refused: parents` and exits 2 with no window; open with a missing nid prints `refused: no growth row` and exits 2 with no window; close aborts, removes the window, writes no node; a refused row prints the corrective diagram and `.` without required fields exits 3 writing nothing; none of those calls exec write.py."
title: "agi-fill is the captive fill window without write.py (goal:g7.16.1.11.8 Y2)"
town: core
---
# hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py

## Measured
- 17:47Z 10-04 (date -u), director-general-1: `sect agi-fill` extracts 5,973 B python from config:engine-grow. yaml + jsonschema import. No `~/.fill`. `agi-fill` is not on PATH (sect extracts it). `write.py` is still in the clone.
- Sibling hyp g7161118-grow-check (queued to DG2 on 6365c215a) covers Y1 order. This node is Y2 on the same leaf.
- `grow-project .agi/context/schemas growth-aliases.tsv | cmp - growth.tsv` CMP_OK (7,083 B) — matrix is live; not this claim.
- Scratch, AGI_FILL=/tmp/.../.fill AGI_GROWTH=this tree's growth.tsv:
  - `open 21e059b9381fa3cf goal:g7.16.1.11.8` -> `FILL WINDOW OPEN: hypothesis under goal:g7.16.1.11.8 · key 21e059b9381fa3cf · schema hypothesis@1eea3f2c9d5d`, window file 779 B, rc 0.
  - `open 21e059b9381fa3cf doc:card-director-general-1` -> `refused: parents doc but row 21e059b9381fa3cf unlocks goal -> hypothesis` rc 2, no window.
  - `open deadbeefdeadbeef goal:g7.16.1.11.8` -> `refused: no growth row deadbeefdeadbeef` rc 2, no window.
  - `close` after a legal open -> `window closed: aborted, nothing written` rc 0, window gone, no node file.
  - row `tags: ["parked:xx"]` -> corrective diagram `refused row : 1 wrong` / `got "parked:xx"`.
  - `.` with only testable_claim set -> `refused (try 1 of 3) : 1 wrong` / `title got (missing)` / SHAPE, rc 3, nothing written.
- `strace -f -e execve` of open+close: python3 then `git hash-object` on `[hypothesis].md`; no write.py.
- Named hole, not this claim: `open` with no nid traceback IndexError rc 1 (doc:g716111-round7-build hole 5). `agi-fill check` of a wrong-order goal-under-doc is rc 0 (check is fields, not order; order is grow-check).

## CLAIM
`sect agi-fill` (the python in config:engine-grow) is the captive fill window without write.py: open with a matrix nid and matching parent types prints FILL WINDOW OPEN and writes the window file (rc 0); open with that nid and wrong parent types prints `refused: parents` and exits 2 with no window; open with a missing nid prints `refused: no growth row` and exits 2 with no window; close aborts, removes the window, writes no node; a refused row prints the corrective diagram and `.` without required fields exits 3 writing nothing; none of those calls exec write.py.

## Dispatch line
config-max: none / template-max: none / code: none (the piece is already in config:engine-grow). Experiment is scratch + strace. Council does not dispatch; SM queues DG2.

## FALSIFIERS
1. Scratch: legal open (hypothesis nid 21e059b9381fa3cf under a goal) is not rc 0 or writes no window; wrong-parent open is not rc 2; missing-nid open is not rc 2; close after open leaves a window or writes a node; `.` without title is not rc 3 or writes a node.
2. Negative: `strace -f -e execve` of open+close contains `write.py`.
3. The no-nid traceback (rc 1) is a named hole, not a disproof of (1)+(2).

## TESTS
scratch AGI_FILL + AGI_GROWTH against this tree's growth.tsv + schemas; strace on the extracted python. Neighbourhood: sibling grow-check hyp; doc:g716111-round7-build Y2.

## FILE SCOPE
read-only: config:engine-grow · `.agi/nodes/.geometry/growth.tsv` · `.agi/context/schemas/[hypothesis].md`. No live-tree write. No write.py. No Unix user / sudo (parent g7.16.1.11 invariant). Window file only under /tmp.

## CEILING
0 production lines · 0 USD · DG2 independent replica · no kids.
