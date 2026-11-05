---
id: goal:g7.16.1.11.46.5
mint_id: 72c9b06b6ba341c498f4f2bf6a7bc1eb
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.5
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M4
season: 3
status: complete
title: "G7.16.1.11.46.5: M4 -- the board shows intake: <post>=open/placed/red per post per lap, computed from the cards by the one metrics_line writer, and one TRAJECTORY line per ingested throw"
town: local-maxxing
---
# goal:g7.16.1.11.46.5

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §39 (after ingestion, the board) and §34.4. metrics_line is ONE cell rewritten by the graph-metrics cron as belam (crons.md: board_job.py --job metrics_cell -> metrics_cell.py; tests/graph-metrics.t.sh D): a second writer would be clobbered every hour, so the intake segment comes from that writer. Doc sections implemented: §39 (board, TRAJECTORY), §34.4 (numbers on the board) (doc:brainstorm-unify is reference, never placement).

## Target end-state
- metrics_line on town:local-maxxing carries `| intake: <post>=<open>/<placed>/<red>[/?<unknown>] …` for every post with a card §7, read from the cards on the trunk; red = an open row older than one lap; `?<unknown>` = open rows with no lap (age unknown, never red).
- The TRAJECTORY section carries one line per ingested throw; the first is "10-23 brainstorm (doc:brainstorm-unify) atoms=62 placed=<k> → <leaf ids>", updated as rows close.

## Invariants
- No post writes the intake numbers by hand; the cron is the one writer.

## Falsifier
1. `sh extensions/agi/tests/graph-metrics.t.sh` exits 0 with new lanes: the intake segment equals a scratch card's counts; a §7 count change changes the next cell (mutant: a cron that skips the cards reads RED).
2. Live: `grep -c '^metrics_line: .*| intake: .*belam=' .agi/nodes/town/local-maxxing.md` ≥ 1 and `grep -c 'atoms=62 placed=' .agi/nodes/town/local-maxxing.md` ≥ 1.
3. Negative: `git grep -l 'set metrics_line' -- extensions skills ':!extensions/agi/tests'` prints nothing (the one writer stays extensions/agi/bin/metrics_cell.py via board_job.py --job metrics_cell, which writes the cell by name; true at 2ef3c2f6d6).

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-24 (CLOSE; standing close form) falsifiers RE-RUN as written at trunk 075054d326 (L90 = 89a1dd7589, the 05:23Z board cell on the trunk): F1 `sh extensions/agi/tests/graph-metrics.t.sh` 0 FAIL (new lanes m4a-m4d, the Z1/Z2 lanes m4z1 m4z2, the T1/T2/T2b lanes m4t1 m4t1b m4t2 m4t2b m4t2c; mutants m4m m4t2m m4t2bm RED). F2 live: `grep -c "^metrics_line: .*| intake: .*belam=" .agi/nodes/town/local-maxxing.md` prints 1 and `grep -c "atoms=62 placed=" ...` prints 1 (the cell reads `| trajectory: 10-23 brainstorm (doc:brainstorm-unify) atoms=62 placed=8 -> ...` then `| intake: belam=55/9/0`). F3 negative: `git grep -l "set metrics_line" -- extensions skills ":!extensions/agi/tests"` prints nothing. Council wording (Target "carries") landed with L90; the Falsifier text is unchanged.
<!-- THOUGHT:END -->
