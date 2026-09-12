---
id: hypothesis:l4-cmd-spawn-initialises-rowgen-display-cmd-resolves-by-key-presence-and-preserve-swept-latches-never-inherits-a-stale-sweep
mint_id: e8afb91951344e159dd9e01db4510365
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: fb0edec51fd8a836
season: 2
testable_claim: "goal:g15 FIX-ONLY (mur-SL2.25 residue lines (d) + (h) + (i), Prime XVII 20:5xZ — three one-function fixes bundled). MEASURED by the Prime on ffcfa4e2f, re-locate on post tip 1d07f3521: (d) SL7.79 — a seat-less, non-dry cmd_spawn inside a project root raises UnboundLocalError on _rowgen (rotate.py:1697-1699 assign _rowgen only inside the seat branch; :1769 reads it unconditionally); (h) SL7.95 — sensei.py _display_cmd resolves the column by TRUTHINESS, so {'command': ''} falls through to the json fragment '{\"command\":\"\"}' instead of '-', and its docstring still describes the pre-fix behaviour; (i) SL7.83 — rotate.py _preserve_swept_latches (:3452) inherits a stale swept_latches key from a PRE-EXISTING record file at the path (a re-run on an old record carries the old sweep list forward as if measured now). CLAIM: (d) _rowgen is initialised None before the branch and the seat-less path reads a named fallback (FIRST_SEATING_GEN or the explicit --gen), no exception; a test drives cmd_spawn seat-less non-dry with the spawn seam faked; (h) _display_cmd resolves by KEY PRESENCE with a string value — an empty string command prints '-' (empty input prints '-', an explicit empty command prints '-'), docstring rewritten to the live order; (i) _preserve_swept_latches copies swept_latches from the existing file ONLY when the in-memory record has no sweep of its own for THIS run (a sweep performed now always wins; an inherited list is marked inherited: true). FALSIFIERS: an UnboundLocalError path reachable; a json fragment for an empty command; an inherited sweep list presented as measured. TESTS (append; <= 4): test_rotate_startup.py (d); test_sensei.py (h) two cases; test_rotate_latch_sweep.py (i). FILE SCOPE: rotate.py — the _rowgen initialisation in cmd_spawn + _preserve_swept_latches; sensei.py — _display_cmd; the three test files. EXCLUDED: everything else in rotate.py (after_join, closeout, cmd_ack, cmd_meter), sensei.py's other subcommands. CEILING: <= 25 lines + <= 4 tests; rotate + send nbhds green."
thought_session: sensei-director-genXVII-L17
title: "three one-function fixes (d)(h)(i): cmd_spawn initialises _rowgen before the seat branch (no UnboundLocalError seat-less), sensei.py _display_cmd resolves by key presence ('' prints '-'), _preserve_swept_latches never presents an inherited sweep list as measured"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cmd-spawn-initialises-rowgen-display-cmd-resolves-by-key-presence-and-preserve-swept-latches-never-inherits-a-stale-sweep

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
