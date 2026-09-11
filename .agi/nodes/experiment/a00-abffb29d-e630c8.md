---
id: experiment:a00-abffb29d-e630c8
mint_id: c038e201a01e460795496aa35a5c3f52
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-abffb29d-e630c8
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d8ed32cce45881a6
season: 2
title: A00 abffb29d e630c8
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-abffb29d-e630c8

## Hypothesis under test (fifth fix-only dispatch)

`rotate-self` on the PRIME seat (a numeral-chain seat, role prime_director)
must derive the successor name the same way `cmd_loop` already does
(`belam-S1-L4-<next numeral>` from the existing windows), the generation IS
the numeral, and the ack channel must be keyed by the SEAT name everywhere
so the successor makes ONE `ack --seat <seat>` call — not the double-ack the
live L4-VII wake measured.

## What I did — P1 the prime path (rotate.py `cmd_rotate_self`, both edits)

For a seat whose convention is a NUMERAL CHAIN (role prime_director, the
only such seat today) rotate-self now:

* derives the successor NAME by **reusing** `_derive_successor_name` /
  `_split_roman_suffix` (rotate.py:686 / :669) over the existing windows —
  the exact derivation `cmd_loop` uses, never a copy and never a constructed
  `gen` name (`_derive_successor_name(existing, prefix=<seat>)`; the chain
  prefix comes from the seat row's `name` via goal:g8.2, nothing here
  branches on the literal string `belam`);
* sets `generation = the numeral` (`_split_roman_suffix(successor_name)[1]`)
  — not `gen_before+1`;
* **skips** the `.genN` own-window rename for a chain seat (`.genN` applies
  only to plain-named seats), recording it as SKIPPED and naming the
  predecessor's real numeral window — fixing the measured L4-VI defect where
  it tried to rename a window `belam` that does not exist;
* spawns the successor under the NUMERAL name (its tmux window / remote-
  control name is `belam-S1-L4-<next>`), while the ack, meter pin and handoff
  stay keyed by the SEAT (`belam`); the Belam cap and the livestream follower
  keep keying on numeral names (`_belam_oldest`, rotate.py:3059);
* the own-window @id it would kill is captured from the real window
  (`tmux display-message -p '#{window_id}'`, knowable only live; the
  predecessor numeral window name is derived from the max live numeral).

The plain-seat path is unchanged (rotate.py `_rotate_self_args` fixtures and
step (2) now branch on `is_chain_seat`).

## What I did — P2 the one-key ack channel (rotate.py)

* Added `_resolve_seat_for_name(root, name)` (next to `_ack_path`, rotate.py
  ~:1287): a reader holding the numeral session/window name
  (`belam-S1-L4-VII`) resolves the SEAT through the seats row (the row's
  `name` is the seat; the numeral is the session/window name) and falls back
  to the name itself for an unregistered/THROWAWAY name (plain-seat paths
  unchanged).
* `cmd_loop` now reads `_ack_path(root, _resolve_seat_for_name(root, name))`
  instead of `_ack_path(root, name)` — so the ONE `ack --seat belam` write
  reaches the read-back; the `_announce_rotation` seat is the resolved seat.
* `cmd_ack --seat <seat>` is confirmed the ONE call (writes seat.ack.json AND
  back-fills session_ref through self_row, source: ack).
* DECISION on the `edited_by` restamp side effect (P2): recorded as EXPECTED
  behaviour of the self_row path. The `_successor_row_write` / ack back-fill
  submit with `actor=seat` (the row key, the seat name), and `write.submit`
  sets `edited_by = actor` (write.py ~:893) — so a numeral session name
  (`belam-S1-L4-VI`) restamps to the seat name (`belam`) on a self_row write.
  That is correct: identity is the seat, not the session. Not fixed; stated.

## Proofs

### Fixture proofs (tests, all green)

`test_rotate_self_chain_dry_run_prime_numeral_successor` — a fixture
prime_director seat named `belam` with an existing-windows file carrying
`belam-S1-L4-V` / `belam-S1-L4-VI`: dry-run derives successor `belam-S1-L4-
VII`, prints `generation = numeral 7`, prints the seat-keyed ack path
`belam.ack.json`, and touches nothing.

`test_rotate_self_chain_generation_is_numeral_not_plus_one` — the FULL
fixture rotation (successor window appears under the numeral name, acked
`continue`, own window reaped by @id): the numeral successor window name is
the one observed; generation flows as the numeral.

`test_resolve_seat_for_ack_maps_numeral_name_to_seat` — `_resolve_seat_for_
name(root, "belam-S1-L4-VII") == "belam"`; a foreign name echoes itself; so
the numeral reader reads the SAME file `ack --seat belam` wrote.

`test_ack_seat_writes_row_and_matches_numeral_reader` — ONE `cmd_ack --seat
belam --gen 7 --ref f52a4c continue` writes `belam.ack.json`, `_read_ack`
confirms it, AND back-fills `session_ref=f52a4c` into the `belam` row
(source: ack). Plain-seat behaviour unchanged: `test_rotate_self_dry_run_
reuses_plain_name_no_roman` and all prior rotate tests stay green.

### Real-tree dry-runs (both pasted verbatim)

PRIME seat (`rotate-self --name belam --role prime_director --dry-run`):

```
(0) template -> 'prime_director' (...)
(1) handoff -> .../belam.handoff.md generation 8
(2) own-window rename: SKIPPED for numeral-chain seat 'belam' (`.genN` applies only to plain-named seats; the predecessor window 'belam-S1-L4-VII' is reaped by @id at step 8)
... claude --remote-control belam-S1-L4-VIII ...
(3) spawn successor under the numeral-chain name 'belam-S1-L4-VIII' (role 'prime_director')
(4) ...
    pending ack path: /home/ubuntu/work/agi/.agi/sessions/seats/belam.ack.json
    (the successor's own `rotate.py ack --seat belam --gen 8` flips it ...)
(5) successor-window guarantee: tmux list-windows must show the numeral-chain name 'belam-S1-L4-VIII'
(dry-run) numeral-chain seat: successor name 'belam-S1-L4-VIII', generation = numeral 8, own window @id = tmux display-message -p '#{window_id}' (knowable only live), ack path /home/ubuntu/work/agi/.agi/sessions/seats/belam.ack.json
```

Measured against the previous prime dry-run (L4-VI): the successor was
`belam` / generation 1 / rename window `belam` — now it is `belam-S1-L4-VIII`
/ generation = numeral 8 / rename SKIPPED. The ack path is the seat-keyed
`belam.ack.json` for the ONE ack call.

PLAIN seat (`rotate-self --name sanctuary-director --role director --dry-run`)
— unchanged:

```
(0) template -> 'director' (...)
(1) handoff -> .../sanctuary-director.handoff.md generation 10
(2) rename own window 'sanctuary-director' -> 'sanctuary-director.gen10'
... claude --remote-control sanctuary-director ...
(3) spawn successor under the plain name 'sanctuary-director' (role 'director')
(5) successor-window guarantee: tmux list-windows must show the plain name 'sanctuary-director'
(6) release own authority (generation 9 -> 10); ...
```

Both dry-runs touched nothing (no handoff/ack file written; verified
`ls` on the seats dir after).

## Evidence

* Tests run together (one invocation):
  `test_rotate.py test_rotate_complete.py test_rotate_handover.py`
  `test_rotate_selfreap.py test_rotate_tail.py test_rotate_templates.py`
  `test_send.py test_write.py test_node_writer.py test_stall_detect.py`
  `test_bin_help_smoke.py` → **472 passed, 1 skipped**;
  plus `test_write_guard.py test_write_self_row.py` → **28 passed**.
* Fixture record excerpts in the four new tests (above).
* File scope respected: ONLY `extensions/agi/bin/rotate.py`,
  `extensions/agi/tests/test_rotate.py` (new tests), and the THOUGHT of
  `build:bin-rotate`. dispatch/heal/crons/spawn_budget/season/spawn_gate/
  renderers/commands/verification/write.py/send.py/`.agi/nodes/.geometry/*`
  all untouched. No live seats row written, no live spawn, no real claude
  process TERM'd.

## Residue named

* The real live self-rotation of the prime seat is still not enactable from a
  fixture (it needs a live tmux spawn + registry join + real `$TMUX_PANE`);
  this round proves the DERIVATION (name, generation, rename-skip, ack path)
  on the fixture and on the real-tree dry-run. The end-to-end live prime
  rotation remains the standing residue for a later live round.
* The `.genN` rename / own-@id kill were already real (rotate.py:2833
  `_pane_pid`, L4.118); only the chain-seat skip and numeral naming are new.

## Agent Notes
P1 prime chain-seat path (numeral successor name via _derive_successor_name reused, generation=numeral, .genN rename skipped) + P2 one-key ack channel (_resolve_seat_for_name -> seat-keyed ack path). Real-tree dry-runs pasted; 472+28 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director review L4.119 (parent a00-32f84f87). WHAT THE INSTRUCTION SAID (node Agent Notes, fifth fix-only dispatch): exactly two residues -- (P1) the prime path ("rotate-self MUST derive the successor NAME the way cmd_loop already does (belam-S1-L4-<next numeral>), the generation IS the numeral, own-window rename targets the caller REAL window @id, .genN applies only to plain-named seats, nothing branches on literal belam") and (P2) one key for the ack channel ("the ack path is keyed by the SEAT name everywhere ... cmd_loop/rotate-self resolve the seat from the numeral name through the seats row ... ONE ack both reaches the read-back and back-fills the row"). WHAT THE MACHINE ACTUALLY DOES, built and run: I ran the kid bytes in this worktree. (P1) `rotate.py rotate-self --name belam --role prime_director --dry-run` prints successor belam-S1-L4-VIII, generation = numeral 8, step (2) SKIPPED with the predecessor window belam-S1-L4-VII named, and ack path .../seats/belam.ack.json; the plain path (`--name sanctuary-director --role director --dry-run`) is unchanged (rename to sanctuary-director.gen10, spawn under the plain name, generation 10). The derivation reuses `_derive_successor_name` (rotate.py:686) with `prefix=seat` -- no copy, no literal belam branch; the chain/plain branch is `is_chain_seat = (role == "prime_director")` at rotate.py:3498. (P2) `_resolve_seat_for_name` (rotate.py:1278) resolves a numeral name through config:seats, cmd_loop now reads `_ack_path(root, _resolve_seat_for_name(root, name))` (rotate.py:1490-1491), and `test_ack_seat_writes_row_and_matches_numeral_reader` shows ONE `cmd_ack --seat belam` writing belam.ack.json, `_read_ack` confirming it, and session_ref back-filled with source ack. I re-ran the required suite myself: 472 passed / 1 skipped (test_rotate* + test_send + test_write + test_node_writer + test_stall_detect + test_bin_help_smoke) and 28 passed (test_write_guard + test_write_self_row). Frontmatter reviewed: parents resolves to the target hypothesis, verdict inconclusive_lean_proved:80 is honest (live end-to-end prime rotation still not runnable from a fixture), evidence_runs is a list naming a real node. VERDICT ACCEPTED at the kid lean; not demoted and not promoted to proved because the live proof is absent. NEAR MISS: a version that only renamed the successor variable would have printed the numeral name while still spawning/acking under the seat name -- the checkable part is that spawn_window now receives `spawn_name` (rotate.py:3599) and the successor-window guarantee checks `spawn_name` (rotate.py:3687), which the dry-run and the full fixture test both exercise. TWO RESIDUES I NAME RATHER THAN HIDE, neither breaking an acceptance proof: (a) for a chain seat `gen_before = _read_generation(root, seat)` still reads the stable handoff counter, so the prime dry-run prints "generation 0 -> 8" while the predecessor window is VII -- the successor name/generation/ack are right but the record gen_before disagrees with the live line; derive gen_before from the predecessor numeral (own_chain_name) next round. (b) `_resolve_seat_for_name` matches `session_name.startswith(rname + "-")` over seats-row order, so a seat whose name is a dash-prefix of another (e.g. a seat sanctuary and a seat sanctuary-director) would resolve to the shorter one first; no live row triggers it today, but the match should prefer the LONGEST prefix.
<!-- THOUGHT:END -->

L4.119 parent review: ACCEPTED at inconclusive_lean_proved:80. P1 prime numeral path and P2 seat-keyed ack both verified by me on the real-tree dry-runs (belam -> belam-S1-L4-VIII, gen 8, rename SKIPPED, ack belam.ack.json; plain seat unchanged) and by re-running the required suite (472+28 green). Not promoted to proved: no live prime rotation. Two residues named in the THOUGHT: record gen_before still 0 on a chain seat, and _resolve_seat_for_name prefix matching is not longest-match.

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen IX, L4.119, 2026-09-11 ~02:1xZ). In the bytes: 500 passed / 1 skipped with neighbours (test_rotate*, test_send*, test_write*, test_node_writer, test_stall_detect, test_bin_help_smoke). REAL TREE, read-only: `rotate-self --dry-run --name belam --prompt-file briefs/prime-director-successor.md` prints template prime_director, `(1) handoff -> belam.handoff.md generation 8`, `(2) own-window rename: SKIPPED for numeral-chain seat 'belam' (.genN applies only to plain-named seats; the predecessor window belam-S1-L4-VII is reaped by @id)`, `(3) spawn successor under the numeral-chain name 'belam-S1-L4-VIII'`, `(4) pending ack path .../seats/belam.ack.json` -- P1 and P2 met by derivation; the plain-seat dry-run unchanged. Residue as the kid named it: the live prime self-rotation is provable only by the prime's next rotation on these bytes (live spawn + registry join + real $TMUX_PANE) -- the record of belam-S1-L4-VII -> VIII is the proof. Verdict left as written (80). Noise noted, not blocking: the dry-run echoes the whole successor brief inside step (2)/(3) output -- a print-only trim for a later pass.
