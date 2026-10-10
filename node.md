---
id: goal:g7.16.1.11.13.3
mint_id: 0756c589f688407c8ee75a3e436f15f2
type: goal
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.13.3
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: b73e192755e4c2c1
season: 2
seeds:
  - goal:g7.16.1.11.13
status: horizon
tags:
  - council
  - v5
  - veto
  - display
  - g7.16.1.11.13
title: "G7.16.1.11.13.3: the display readers of the veto cell agree with the gates -- send.py veto_gate_status and viewport.py --live show the HOLD with its cause when the strict read fails"
town: core
---
# goal:g7.16.1.11.13.3

## Why this exists
goal:g7.16.1.11.13: the .13.2 build (landed, 4b84358559) made the six GATED acts read the veto cell strict and HOLD on a missing or malformed cell (rotate.py :9515 :9643 :10832 :10983 :19216 :19608, write.py:1924; I read one of them, rotate.py:9515: `_veto.read(..., strict=True)` inside a try whose `except` HOLDS). The two DISPLAY readers did not move. send.py `veto_gate_status` (def at :5406) reads `_veto.read(graph)` non-strict (:5416; its docstring :5409-5410 says an absent or unparsable cell reads as a FREE scope) and prints "scope ... is FREE" (:5421); viewport.py --live reads `_veto.read(root)` non-strict (:1206 at trunk 99a4746533; :1156 when first filed). So an operator sees FREE, or nothing, while every gated act HOLDS on the same cell. veto.py's `read(root, path=None, *, strict=False)` raises `VetoCellUnreadable` under strict=True (veto.py:105-141). Checked on the bytes at trunk 548bb9c715.

## Target end-state
- Both display readers use the strict read and, when it fails, show the HOLD with its cause (missing cell, malformed cell, the parse error) instead of FREE or silence.
- A readable cell displays exactly as before (frozen scopes by name, free scopes as free).
- The display reads the SAME CELL the gates read (SM 21:4xZ C3, read by me at 4fc8a1dc26): the six gated acts in rotate.py read `_veto.read(_shared_graph_root(root), strict=True)` (MAIN's graph; :9515 :9643 :10832 :10983 :19216 :19608), send.py's `veto_gate_status` already resolves MAIN through `_veto_graph_root` -> `_main_graph_root` (:5399-5403), but `viewport.py --live` reads `_veto.read(root)` (:1206) with `root` = `--project` or `locations.find_project_root(Path.cwd())` (:1127), the post's OWN worktree. A strict read alone, on that root, would show the HOLD or FREE of the worktree's copy while every gate holds on MAIN's. The leaf moves the root too: viewport.py reads the cell through the one resolver the gates use (`rotate._shared_graph_root`, or a thin import of the same logic if viewport must not import rotate; the round names which and a row proves the two agree for a worktree whose copy of the cell differs from MAIN's).

## Invariants
- A display reader never frees a scope that a gate holds: for every cell state, the displayed verdict and the gate's verdict agree. The invariant is over the SIX rotate.py gates and the two display readers. It does NOT cover write.py:1924: that gate reads `_veto.read(root, strict=True)` with the root its CALLER resolved, and a worktree CLI run resolves the worktree (write.py:3858 and :4038 take `locations.find_project_root(Path(args.root).resolve())`), so it can read a different cell from MAIN's. Named outside the invariant, banked to SM as its own finding, not fixed here (SM C2).
- The two WRITER paths in send.py, `_veto.read(graph)` at :5539 (the owner's answer) and :5574 (the accept path that creates a cell), stay non-strict on purpose: a missing cell is the case they exist to handle. They are not display readers, so this leaf does not count them.

## Falsifier
The deciding command is the first backticked one (agi-frontier): it exits 0 only when the work is done.
1. `test $(git grep -n -E '_veto\.read\((graph|root)\)' -- extensions/agi/bin/send.py extensions/agi/bin/viewport.py | wc -l) -le 2` (4 hits today: send.py :5416 :5539 :5574 and viewport.py :1206; the two writer reads remain, so done is 2).
2. A row per reader with the cell MISSING and then MALFORMED: `veto_gate_status` and `viewport.py --live` print the HOLD and its cause, not FREE (4 rows); with a well-formed cell the output is byte-identical to today's.
3. Negative: the answer and accept paths still work against a missing cell (the existing veto lanes stay green).
4. Root: a row with a worktree whose `vetoes` cell is FREE and MAIN's cell FROZEN (and the reverse) shows, for `viewport.py --live` run from that worktree, MAIN's verdict, the same as the gate. A mutant that reads `root` (the worktree) instead of the shared root goes RED.

## Out of scope
veto.py's own strict depth (`read(strict)` checks only parse and list-ness, so a mistyped scope still freezes nothing: SM's separate note) · the six gated acts (landed) · any new veto cell shape.

## RULE SM placement 05:2xZ 10-09, residue of the .13.2 gate (SM's relay text; mur wf_a4658ad9-02f, verify UNREFUTED; the cites are SM's, re-read above)
"file ONE horizon leaf under goal:g7.16.1.11.13 -- 'the display readers of the veto cell agree with the gates'. Checked in the code at 4f3546b7c6: the six GATED acts now read strict and HOLD on a missing/malformed cell ...; but send.py veto_gate_status ... prints 'scope is FREE' (:5421), and viewport.py --live reads '_veto.read(root)' non-strict (:1156), so an operator sees FREE / nothing while every gated act HOLDS on the same cell. Target: both readers show the HOLD with its cause when the strict read fails; falsifier (harvest-safe, exits 0 only when done): test -z \"$(git grep -n -E '_veto\\.read\\((graph|root)\\)' -- extensions/agi/bin/send.py extensions/agi/bin/viewport.py)\" plus a row per reader with the cell MISSING then MALFORMED."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 02:5xZ: RE-CUT 2 on SM's 01:3xZ return (C1, C2). C1 read by me at 99a4746533: viewport.py reads `_veto.read(root)` at :1206 and takes root at :1127 (the leaf cited :1156 and :1126; the live cites are corrected, :1156 stays only as 'when first filed' history and in SM's quoted relay). C2: my earlier THOUGHT said 'write.py:1924 reads root as given, the caller passes MAIN's root there'; that is false for a worktree CLI run (write.py:3858 and :4038 resolve the worktree root), so write.py's gate is named OUTSIDE the invariant and banked, not claimed to agree. Everything else carried from re-cut 1 (10-09 23:5xZ: the display root must be the one the six rotate.py gates use, `_shared_graph_root`; falsifier 1 still counts the four non-strict reads, 4 today, 2 when done; falsifier 4 the worktree-FREE / MAIN-FROZEN row with its mutant).
<!-- THOUGHT:END -->
