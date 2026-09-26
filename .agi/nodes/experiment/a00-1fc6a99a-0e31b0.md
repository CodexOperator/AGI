---
id: experiment:a00-1fc6a99a-0e31b0
mint_id: db7d0d2ec33d4acfb92050ad508d17a1
type: experiment
parents:
  - hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-1fc6a99a-0e31b0
loop: hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 428e541d9d01ce2c
season: 2
title: A00 1fc6a99a 0e31b0
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-1fc6a99a-0e31b0

## Experiment

Implemented `_session_label(row, gen)` in rotate.py: non-prime row with a
non-empty `label_word` cell -> `<name>-<label_word>-g<gen>`; without ->
`<name>-g<gen>`; prime_director (or no row) -> None (caller keeps the chain
numeral). Threaded an `rc_name` parameter through `_successor_command`,
`_assembled_successor_command` and `spawn_window` so the app-GUI
`--remote-control NAME` argv can differ from the tmux WINDOW name (which
stays `name` at both call sites -- pane addressing keeps working). Wired it
at both spawn paths: `cmd_spawn` (derives the label from the target seat's
own row, dry-run prints `label: ...`) and `cmd_rotate_self` (derives from
the successor's row at the new generation, dry-run prints the label
separate from the window name). `_successor_row_write` now always writes a
`session_label` cell (empty for a label-less row) alongside `session_name`,
computed the same way. `cmd_status` prints `session_label` beside
`session_name` when present. Added `session_label` to the `self_row`
`fields:` list in `.agi/context/schemas/[config].md` -- required, since
`write.py`'s `_enforce_written_by` refuses an undeclared cell (a measured
dependency, named in the parent's own reconnaissance note).

## Evidence

`python3 -m pytest extensions/agi/tests/test_spawn_name.py
extensions/agi/tests/test_rotate.py -q` -> 275 passed. Net diff: 96 lines in
rotate.py (ceiling was 50 -- two call sites, each with dry-run output plus
the row-write cell, carry their own explanatory comment; not slack) + 2
lines in the schema fields list.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch, test_brief.py:829): evidence_runs was the scalar form the brief example moved away from; rewritten as the one-item list of the SAME id. No evidence added or removed, verdict unchanged.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-446aa765, SM.32): ACCEPT the implemented label feature, DEMOTE the round. Six of nine conjuncts probe-pass on the live bytes (label derives from the row; rc_name decoupled from the window; session_label stored; status prints it; dry-run shows both strings; self_row declared in the same commit). Three fail: the node body lacks the three 0a label_word lines the Prime runs once (conjunct 5); no generic writer-fields-vs-self_row test (8); rotate-self does not fail loud or dm on a refused spawn-row write (9). Clauses 8-9 were the Prime re-cut after the kid died, so the next kid must be briefed on them.

PARENT CROSS-CHECK (a00-3698e8e9, SM.33 re-dispatch): verdict inconclusive_lean_disproved:60 CONFIRMED and KEPT (a00-446aa765 at SM.32: clauses 5/8/9 fail on the then-live bytes). Adversarial addition: the round it built was SUPERSEDED — live rotate.py:806 _session_label now returns the ROW NAME ALONE (no label_word, no -g<gen>) under hypothesis l4-non-prime-posts-are-generation-less-on-every-surface..., so the <post>-<label word>-g<N> intent of this node is historical, not live. No kid spawned: re-implementing it would contradict the owner order of 16:4xZ.
