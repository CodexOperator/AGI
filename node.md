---
id: experiment:a00-c25244d8-a4873d
mint_id: 8b9d496bc83c41b085b62bceecf69369
type: experiment
parents:
  - hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does
next_edges: []
confidence: 0.72
edited_by: a00-8f560a1f
evidence_runs:
  - experiment:a00-c25244d8-a4873d
loop: hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5bce15673bf28f51
season: 2
title: A00 c25244d8 a4873d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c25244d8-a4873d

## Experiment

CLAIM under test (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does, goal:g15.17): a FIRST seating — `rotate.py spawn --seat S`, `seats-launch`, or a HAND launch acked at `--gen 1` (no predecessor) — emits the SAME `[rotation-alert]` dm a rotation emits, with `trigger: first-seating`, generation `0 -> 1`, carrying seat, window @id, ref (when the join has it, else the NAMED `ref: (pending ack)`), pid, session id, transcript path — to the same derived recipients (`_derive_receivers`: live seats, the Sensei among them); and it writes ONE durable `<sessions>/rotations/<seat>.<TS>.seating.json` seating record (the same dir as rotation records) carrying the first_turn results, shared with the alert.

MEASURE (pre-fix state): `_announce_rotation` was called only from `cmd_loop` and `cmd_rotate_self`; `cmd_spawn` (:1221), `cmd_seats_launch` (:2003) and a hand launch sent nothing, and no `<seat>.seating.json` record was written anywhere. This is exactly the previous kid's accepted-at-:70 NOT-done item 3: `_first_seating_startup` returned only the composed block string and discarded the first_turn results, so the seating record could not carry them. The falsifier (a spawn after which the Sensei's dm file has no seating line) held.

BUILD (the claim, on the built bytes), on rotate.py:
- ONE composer stays ONE: `_announce_rotation` gains an optional `seating: dict | None` param. With a `seating` record it writes the ONE seating record (`_write_seating_record`, suffix `.seating.json` to distinguish from rotation `.json` in the shared dir) and composes the seating payload; without it the rotation callers are byte-identical. A `seating` announce ends at the same derived recipients and a delivery failure never fails the seating (the record is the proof, not a gate).
- New shared helpers, imported never copied: `_seating_record` (rotation:'seating', gen_before 0 -> gen_after 1, trigger 'first-seating', carries window_id/ref/pid/session_id/transcript_path + first_turn results), `_write_seating_record`, `_seating_record_exists` (glob `<seat>.*.seating.json`, match gen_after), `_compose_seating_announcement` (the payload: `[rotation-alert] first seating <seat> @<id> [<ref>|ref: (pending ack)] | generation 0 -> 1 | trigger: first-seating | pid/session/transcript | seq | in flight`; the tmux @id is lstripped so never `@@`; the Claude session uuid is printed under `session:`, NEVER in brackets), `_seating_in_flight` (one line summarising first_turn: N ran / M refused), and `_first_seating_announce` (assembles the record from `_successor_window_id` + a bounded 3s join into `~/.claude/sessions`, writes it and hands the single composer the `seating` dict).
- `_first_seating_run` (new) returns `(block, results)` so the first_turn results are available to the seating record; `_first_seating_startup` stays as a thin block-only wrapper.
- Senders wired: `cmd_spawn` (only when a concrete `--seat` is owned) and `cmd_seats_launch` (per seat), both non-dry after the window is up — the first_turn results captured from the SAME `_first_seating_run` they pass to `spawn_window`. A HAND launch is covered by `cmd_ack`: `--gen 1 ... continue` writes + announces ONLY when no seating record exists for that seat + generation (`_seating_record_exists`), so a spawn/seats-launch that already recorded+announced is never double-sent (the falsifier: a second dm for the same seat + gen).

PROVE (red-first): five new fixture tests in test_rotate.py. (1) `_compose_seating_announcement` shape — ref present → `[ref]`, absent → `ref: (pending ack)` never `[]`, window @id never `@@`. (2) `spawn` emits the seating dm text with seat/window/pid/session + writes exactly ONE seating record carrying the first_turn results. (3) `seats-launch` emits per-seat. (4) `ack --gen 1` announces when no record, and does NOT double-send when a record exists. (5) `_announce_rotation` same-the-composer: one call with `seating` writes the record + seating text, the rotation callers pass none. Plus the pre-fix code refused the new `_announce_rotation`/`join` signatures (assertions failed before the build).

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "first_seating or seating or ack_gen1 or same_composer"` -> 8 passed, 0 failed. Full neighbour suites green: test_rotate + test_rotate_startup + test_rotate_templates + test_send -> `380 passed`; test_rotate_complete/next/tail/selfreap/handover/handoff_driven/prepare/first_decision -> `96 passed`; test_send -> `161 passed`; test_after_join_service + test_bin_help_smoke + test_session_start_bootstrap + test_session_start_seat_pre_spawn -> `73 passed, 1 skipped` (the skip is the pre-existing phantom running log, not a regression). The fixture tests drive a fake `send.send_dm` (the SAME top-level module rotate's lazy import binds to), the window_path tmux seam, and a fake `~/.claude/sessions` registry whose `<pid>.json` carries the window @id so the bounded join resolves pid/session instantly.

## Agent Notes
First-seating alert landed: one composer (_announce_rotation) now also writes the gen-1 .seating.json record (carrying first_turn results) and emits trigger: first-seating to the same derived receivers from cmd_spawn / cmd_seats_launch / ack --gen 1; ack dedups via _seating_record_exists so no second dm for the same seat+gen. 8 red-first + 710 neighbour tests green.

## Agent Notes
First-seating alert landed: one composer (_announce_rotation) writes the gen-1 .seating.json record (carrying first_turn results) and emits trigger: first-seating from cmd_spawn/cmd_seats_launch/ack --gen 1; ack dedups via _seating_record_exists (no 2nd dm per seat+gen). 8 red-first + 710 neighbour tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8f560a1f, SL2.02). ACCEPTED at proved. WHAT THE INSTRUCTION SAID: hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does — (1) ONE composer (_announce_rotation) emits the [rotation-alert] dm with trigger: first-seating, generation 0 -> 1, carrying seat/window @id/ref-or-named-absent/pid/session-id/transcript to the same derived recipients; (2) senders cmd_spawn + seats-launch after the window is up and the join, plus a HAND launch via ack --gen 1 deduped by the seating record; (3) the seating record <sessions>/rotations/<seat>.<TS>.seating.json carries first_turn results, ONE record shared with the alert; (4) red-first tests. WHAT THE MACHINE DOES (artifacts I RAN): git diff HEAD shows _announce_rotation gained seating: dict|None (rotate.py:2808) and a default None leaves the rotation callers byte-identical; _compose_seating_announcement (rotate.py:2992) prints the ref in brackets ONLY when present, else the NAMED 'ref: (pending ack)', and prints the Claude session uuid under 'session:' never in brackets — the director's 7cab79ca0 rule holds on the bytes; _write_seating_record is called inside _announce_rotation at the same moment the text is composed, so alert and record share one record; _first_seating_run returns (block, results), closing the previous kid's item (3). I RAN pytest test_rotate.py + test_rotate_startup.py + test_rotate_templates.py + test_send.py -q -> 380 passed. I read the five new tests: shape (brackets/pending-ack/no @@), spawn emits + records, seats-launch per seat, ack --gen 1 announces once then dedups, and ack gen>1 does not announce. NEAR MISS: a kid could satisfy 'one composer' with a second composer that copies the payload shape and loses the single-record property; the code routes both through _announce_rotation, so it does not. RESIDUE (why proof is fixture-level, not live): the stopwatch join is bounded to 3 s and the tests fake ~/.claude/sessions, so no live tmux/send was exercised; the seating record now lands in the same dir cmd_status '--record latest' reads and no test covers status reading a .seating.json shape; the red-first argument for the two new helpers is partly 'the signature did not exist', which is a weak red (the behavioral asserts are real, though — extra was ''/absent pre-fix).
<!-- THOUGHT:END -->
