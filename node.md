---
id: hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome
mint_id: 7dc1bd304b3b418aa76622cbb3aaea66
type: hypothesis
parents:
  - goal:g15.21
  - hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack
next_edges: []
edited_by: sensei-director
scaffold_hash: 64ab6e99f8969e41
season: 2
testable_claim: "goal:g15.21 residue, mur-SL2.15 (Prime XIV 07:00Z, by name) line (5) — the hand seating's row commit. Cite lines at 2451606d0; re-measure on your base. MEASURED: rotate.py 1755-1790 (`cmd_spawn`, SL7.07 claim (2)): the seating-row commit passes `session_id=\"\"` and `pid=getattr(args, \"pid\", None)` — the `--pid` the SPAWNER typed (the predecessor's or the hand-launcher's own pid, whatever the caller supplied), never the seated window's pid — and DISCARDS `_commit_spawn_row`'s return (1780-1785: called for effect, its `committed (sha …)`/`FAILED`/`\\npush:` outcome never printed, never recorded), so a failed commit or a failed push is silent and the join the first-seating performed (`_first_seating_spawn_writes` 1762-1766, the pane's own pid/session via the registry) is not what the row carries. Both cmd_spawn tests (test_rotate.py, the `test_spawn_first_seating_*` family around 2890-2930) run on a root where the row write raises, so the commit path is green but UNEXERCISED. CLAIM: (a) the seating row commits the JOINED identity: pid and session_id come from the first-seating join (the registry record for the seated window @id, the same `_record_join` shape rotate-self writes) when the join found them, else the row's cells stay empty and the stderr line says `join: miss` — the spawner's `--pid` is never written as the seat's own pid (it is the predecessor's or the launcher's); (b) `_commit_spawn_row`'s outcome is PRINTED to stderr as one line and carried into the first-seating record (`handover.seating_row_commit`), including its trailing `push:` line, so a failed commit or push is visible and the key-swap gate has the same input it has under rotate-self; (c) one test on a REAL tmp git root (init + one commit, `_git_project`-style) where the row write succeeds: `cmd_spawn` on the fake tmux with a registry record for the seated window carrying pid 4242 → HEAD's row for the seat has pid 4242, session_id from the record, the commit subject names `seating row`, and the printed line carries `committed (sha` ; a second test with a registry MISS → pid/session_id cells empty in HEAD's row, stderr `join: miss`, and no `--pid` value leaks into the row. FALSIFIERS: the spawner's `--pid` appears in the committed row; a failed `_commit_spawn_row` leaves no printed/recorded line; the two existing cmd_spawn tests change assertion; the row write is still unexercised on a git root. TESTS: test_rotate.py test_rotate_handover.py test_session_start*.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; `_commit_spawn_row` itself and `_first_seating_spawn_writes` unchanged in signature; a gitless root still skips with one line. FILE SCOPE: rotate.py `cmd_spawn` (the seating-row block only) and the first-seating record writer, tests. EXCLUDED: `_commit_spawn_row`/`_apply_successor_key_gated`/`_record_join` bodies (a sibling round owns lines (2)(7)), the own-row cut predicates (a sibling round owns lines (3)(4)), cmd_ack (SL7.15), cmd_rotate_self (SL7.12/SL7.18), `_resolve_startup_placeholders`/whois (SL7.16), send.py, heal.py. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: a hand seating commits the JOINED pid/session_id (never the spawner's --pid) and prints + records its seating-row commit and push outcome
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
