---
id: outcome:g7-16-1-11-13-3-the-veto-display-readers-agree-with-the-gates-closed
mint_id: e802138a02084b5cb84eeada2e7f4d7e
type: outcome
parents:
  - goal:g7.16.1.11.13.3
next_edges: []
adjust: no change to goal:g7.16.1.11.13; three named residuals stay open (interactive viewport --live, write.py:1924, veto.py strict depth)
alignment: aligned
confidence: 0.85
edited_by: director-general-5
judged_against: goal:g7.16.1.11.13.3
lens: goal:g7.16.1.11.13
model: claude-sonnet-5-5
role: director
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.11.13.3 -- the veto display readers agree with the gates: send.py veto_gate_status and viewport.py --live read the cell strict from MAIN and show the HOLD with its cause, 42 passed on the trunk, the interactive TTY view still shows neither"
town: core
---
# outcome:g7-16-1-11-13-3-the-veto-display-readers-agree-with-the-gates-closed

## Outcome
goal:g7.16.1.11.13.3 (the two DISPLAY readers of the veto cell must agree with the six gated acts, which already read strict and HOLD) is CLOSED, `complete` since 10-10 ~10:2xZ. Every claim below was re-read at the trunk tip 6185e6c14a (10-11 ~03:3xZ), read-only, in a fresh worktree off that tip; no whole-graph scan was run.

| falsifier | bytes / run on this trunk | verdict |
|---|---|---|
| F1: at most 2 non-strict `_veto.read(graph\|root)` hits in send.py + viewport.py | `git grep -n -E '_veto\.read\((graph\|root)\)' -- extensions/agi/bin/send.py extensions/agi/bin/viewport.py` -> 2 hits, send.py:5541 and :5576, the two WRITER paths (the owner's answer, the accept path that creates a cell) that stay non-strict on purpose | MET |
| F2: a row per reader, cell MISSING then MALFORMED, prints the HOLD and its cause, not FREE | send.py:5416 `_veto.read(graph, strict=True)`; any failure of it returns `HOLD scope=...: <cause>` (`except Exception`, f032805d7e widened it from VetoCellUnreadable); a seatsig import failure is also a HOLD (send.py:5414). viewport.py:1211 reads strict and appends `HOLD veto cell: <cause>` (:1214), with a bare `except Exception` fallback that is also a HOLD (:1221). `pytest extensions/agi/tests/test_veto_display_strict.py extensions/agi/tests/test_veto.py`: 42 passed (38 at landing; 4 rows were added to these files since) | MET |
| F3: the answer and accept paths still work against a missing cell | the two writer reads are the non-strict hits above; the veto lanes in test_veto.py are in the 42 passed | MET |
| F4: the display reads the SAME cell the gates read (MAIN's, not the worktree's) | viewport.py:1207-1209 resolves `locations.git_common_root(...)` then the project root of that, the root the gates use; send.py goes through `_veto_graph_root`. The worktree-vs-MAIN rows (d2/d4) are in the 42 passed | MET |
| Invariant: a display reader never frees a scope a gate holds, over the six rotate.py gates and the two display readers | follows from F2 + F4 for those eight readers; write.py:1924 is OUTSIDE it (below) | MET for the stated eight |

Mutants were run by sanctuary-master at the gate, not repeated here: the worktree root instead of the shared root 3 RED, the import arm answering "free" 2 RED, send non-strict 3 RED, viewport silence 2 RED. I ran the d-rows green on the final form (the 42 passed above).

Landings (all ancestors of 6185e6c14a, all signed `G`): DG2's rows cee5bfb35c, 3470998e5a and f26dbe8509 (written first); my build 6eaeeb6bf7 and 07855f4f1f; sanctuary-master's landing 53a26cfe96; my follow-up f032805d7e (the Exception widening, on DG2's d7 rows); my close d1e7417eea (status complete + THOUGHT). The goal's six gated acts landed earlier as 4b84358559.

## Measures
git grep, file reads and pytest in a clone at the tip; no timing or box reading is claimed. The 42 passed are the two named test files only, not the full suite.

## Left for the next lines
- OPEN, named, not fixed: the TTY-interactive `viewport --live` returns into `interactive(...)` at viewport.py:1230 before the status line is built, so it shows neither a HOLD nor a GATE-FROZEN; the piped `--emit` views do. A leaf if the owner wants the live pane to carry it.
- OPEN, named, banked to sanctuary-master as C2: write.py:1924 reads `_veto.read(root, strict=True)` with the root its caller resolved, and a worktree CLI run resolves the worktree, so it can read a different cell from MAIN's. It is outside this goal's invariant; no goal is minted for it here.
- OPEN, out of this goal by its own text: veto.py's strict depth (`read(strict)` checks parse and list-ness only, so a mistyped scope still freezes nothing).
