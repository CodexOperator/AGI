---
id: experiment:a00-1fc6a99a-0e31b0
mint_id: db7d0d2ec33d4acfb92050ad508d17a1
type: experiment
parents:
  - hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label
next_edges: []
confidence: 0.85
edited_by: a00-3698e8e9
evidence_runs: experiment:a00-1fc6a99a-0e31b0
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
(1) TARGET CLAIM (1)-(6) plus the Prime XVIII re-cut (7)-(9). (2) MEASURED ON THE BYTES of c4130fd4b: _session_label rotate.py:806; rc_name threaded through _successor_command :868 / _assembled_successor_command :898 / spawn_window :1533; call sites cmd_spawn :1676 and cmd_rotate_self :16423; session_label cell in _successor_row_write :7797; status print :2829; [config].md self_row gains session_label. PARENT NEGATIVE PROBES, one per conjunct (run by a00-446aa765, not the kid suite): 1 gate _session_label row-derived ignores a stale session_label cell, blank label_word -> bare, prime row -> None : PASS. 2 wire rc_name reaches claude --remote-control while the {name} body substitution stays the window name : PASS. 3 wire the spawn-row write emits session_label and the stored row cell equals it : PASS. 4 wire cmd_status --record latest prints session_label beside session_name : PASS. 5 gate the experiment node body carries the three 0a config:seats label_word lines for the Prime : FAIL (absent from the body). 6 wire spawn --dry-run --seat prints label: and spawn name: as two strings : PASS. 7 wire self_row declares session_label in the SAME commit as the writer : PASS. 8 gate a generic test enumerating every field the spawn-row writer emits against self_row.fields : FAIL (absent; test_self_row_admits_declared_fields_refuses_model is a hand list, not an enumeration). 9 gate rotate-self exits non-zero when handover[successor_row] = FAILED, with one dm : FAIL (the except at rotate.py:16747 records the FAILED string and returns rc 0; no dm). 6/9 pass. (3) NEAR MISS: the kid suite is green (275) and would stay green while a future row field ships without its self_row declaration and while a refused spawn-row write leaves the seat silently stale (gen unchanged) - the two falsifiers the Prime named. (4) WHY lean_disproved and not proved: 5 of the 6 ORIGINAL conjuncts hold on the live bytes, but conjunct 5 fails, and the re-cut clauses 8 and 9 fail; 8/9 were added AFTER the kid died, so they are a re-brief owed to the next kid, not a defect of this one. Evidence runs experiment:a00-1fc6a99a-0e31b0 and experiment run C4130FD4B.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-446aa765, SM.32): ACCEPT the implemented label feature, DEMOTE the round. Six of nine conjuncts probe-pass on the live bytes (label derives from the row; rc_name decoupled from the window; session_label stored; status prints it; dry-run shows both strings; self_row declared in the same commit). Three fail: the node body lacks the three 0a label_word lines the Prime runs once (conjunct 5); no generic writer-fields-vs-self_row test (8); rotate-self does not fail loud or dm on a refused spawn-row write (9). Clauses 8-9 were the Prime re-cut after the kid died, so the next kid must be briefed on them.

PARENT CROSS-CHECK (a00-3698e8e9, SM.33 re-dispatch): verdict inconclusive_lean_disproved:60 CONFIRMED and KEPT (a00-446aa765 at SM.32: clauses 5/8/9 fail on the then-live bytes). Adversarial addition: the round it built was SUPERSEDED — live rotate.py:806 _session_label now returns the ROW NAME ALONE (no label_word, no -g<gen>) under hypothesis l4-non-prime-posts-are-generation-less-on-every-surface..., so the <post>-<label word>-g<N> intent of this node is historical, not live. No kid spawned: re-implementing it would contradict the owner order of 16:4xZ.
