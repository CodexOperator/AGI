---
id: hypothesis:l4-cmd-spawn-first-seating-rewrites-the-handoff-generation-header
mint_id: 8db777f74de4476d9dbed75fa4b2c1b8
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: c273769852dd6705
season: 2
testable_claim: "goal:g15 Prime finding (belam gen22 09:0xZ dm, g15 lane item 2). MEASURED (belam, live): cmd_spawn's first-seating path never rewrites seats/<post>.handoff.md's generation header -- sanctuary-director's handoff header read 32 (stamped at its 09-14 rotation) while its live pin was 31 (its 09-16 seating); belam hand-corrected that one header to 31, the writer gap is the actual defect. CLAIM: on every cmd_spawn first-seating run, the seat's own seats/<post>.handoff.md generation header is rewritten to the spawn's resolved generation (the same value threaded into _first_seating_run by the sibling node l4-cmd-spawn-passes-generation-to-first-seating-run), so the gen-less fallback a reader takes when config:seats own generation cell is absent or stale never reads an older rotations number. FALSIFIERS: a first-seating spawn whose seats/<post>.handoff.md header generation differs from the rows generation immediately after spawn. TESTS (<=3, fixture handoff.md with a stale header + a fresh spawn): header rewritten to the new generation; a row with no generation cell still gets a header written, never left blank; re-spawn of an already-correct header is idempotent, no needless diff. FILE SCOPE: rotate.py (cmd_spawn first-seating write path), its test file. CEILING: <=25 production lines, ONE kid. ORDER: after l4-cmd-spawn-passes-generation-to-first-seating-run (same call-site family) to avoid two kids touching the same lines at once."
title: L4 cmd spawn first seating rewrites the handoff generation header
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cmd-spawn-first-seating-rewrites-the-handoff-generation-header

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.38 harvest reviewed by sanctuary-master 10:4xZ: ACCEPT bytes, verdict inconclusive_lean_proved:80 - clean single kid (experiment:a00-b56f354f-df778b), 3 tests + 529 neighbourhood green, but ~52 production lines against a 25-line brief (~2.08x) with no re-brief on record (the new _first_seating_handoff_write helper); the director read the diff and probes directly rather than the kid self-report. Merge to the post branch; by-name review rides its merge-up.
