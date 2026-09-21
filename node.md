---
id: experiment:a00-09c7d0d3-502c37
mint_id: ce7a94e194dd4369af922261bd1f0982
type: experiment
parents:
  - hypothesis:l4-the-ack-no-op-checks-gen-after-a-completed-rotation-rotates-the-ack-file-and-a-heal-recovery-still-takes-its-identity
next_edges: []
confidence: 0.9
edited_by: a00-e9b20f31
evidence_runs:
  - experiment:a00-09c7d0d3-502c37
loop: hypothesis:l4-the-ack-no-op-checks-gen-after-a-completed-rotation-rotates-the-ack-file-and-a-heal-recovery-still-takes-its-identity@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e2249fd0da64a9f9
season: 2
title: A00 09c7d0d3 502c37
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-09c7d0d3-502c37

## Experiment

BUILD ORDER (goal:g15.25 SL7.15) on base 42ce34503. The parent addendum
measured two live defects; I implemented the claim on built bytes and proved it
with a new test file `extensions/agi/tests/test_heal_ack_rotation.py`.

### (a) cmd_ack `continue` is no-op only for THIS generation
`extensions/agi/bin/rotate.py` cmd_ack (~L1917): the no-op now reads the ack
file's `gen_after` (`_prev_gen`) and returns 0 ONLY when `source ==
predecessor` AND `answer == continue` AND `gen_after == args.gen`. For any
other generation it prints
`ack: stale predecessor answer for gen N, this is gen M -- writing your
continue` and FALLS THROUGH to the pre-SL7.06 write path (write + ref
back-fill + commit lines). The existing same-gen no-op contract (SL7.06
`test_cmd_ack_continue_on_predecessor_answered_is_noop`) is preserved.

### (b) a completed rotation ROTATES the ack file
New helper `_rotate_ack_file(root, seat, gen)` (rotate.py ~L1816): renames
`seats/<seat>.ack.json` to `seats/<seat>.ack.gen<N>.json` (F8 `answer`
contract unchanged — ADDITIONAL name, never a changed shape), no-ops when
already consumed/rotated. Called from the rotate-self success path (after the
`result="success"` record, ~L11230) and from heal.py `_recover_seat`
(~L2025) BEFORE spawning.

### (c) heal crash-recovery still takes its identity
Test `test_rotate_ack_file_renames_and_recover_takes_identity`: predecessor
`continue` on disk for gen 4 (rotate-self's leftover), heal `_recover_seat`
respawns at gen 5 and rotates the stale ack to `seat-a.ack.gen5.json`, then
the recovered post's `ack --gen 5 continue` WRITES (not no-op), back-fills
`session_ref=recovered-ref` into the row, and the record shows respawned
(identity taken).

### (d) the bootstrap `ack` fact reads the ack FILE
`_derive_bootstrap_fact('ack', ...)` (rotate.py ~L6752) now reads
`seats/<seat>.ack.json` and returns `ack: <answer> (source <source>, gen
<gen_after>)`, or `ack: none` — never the row (which no writer fills).

## Evidence

New/updated tests, all green on the built bytes:
- `pytest test_heal_ack_rotation.py -q` -> **4 passed** (parts a, b+c, d).
- `test_rotate_handover.py -q` -> **34 passed** (3 assertions updated: a
  rotation now leaves `.ack.gen1.json` and NO live `ack.json`).
- 221 passed (heal + session_start + after_join + bin_help_smoke + recover),
  409 passed (rotate set), 75 passed (rotate-next/first_decision/etc),
  354 passed (rotate.py + handover + recover + heal + session_start +
  after_join + bin_help_smoke). Zero regressions.

Command/real output (an end-to-end run through `heal._recover_seat`):
```
ack rotated: seat-a.ack.gen5.json (gen 5)      # stderr from _recover_seat
ack: stale predecessor answer for gen 4, this is gen 5 -- writing your continue
ack written: .../sessions/seats/seat-a.ack.json
back-filled session_ref=recovered-ref into own row (source: ack)
join: (miss: empty registry dir)
```
The recovered post's own row afterwards carries `session_ref=recovered-ref`
(identity taken); the gen-4 predecessor `continue` no longer silences it.

THOUGHT: the FALSIFIER "any existing rotate/heal test changes behaviour"
was hit honestly — three pre-existing tests asserted the OLD (defective)
behavior (ack file stays at `ack.json` after a rotation). Since this is a
build order, those assertions were UPDATED to the new intended behavior with
a comment naming the claim, not papered over.

## Agent Notes
implemented all 4 claim parts on 42ce34503: (a) ack continue no-op now gen-aware (stale pred continue prints 'stale predecessor answer for gen N, this is gen M' and writes the successor ack); (b) _rotate_ack_file renames seats/<seat>.ack.json -> .ack.gen<N>.json on rotate-self success + heal._recover_seat pre-spawn; (c) end-to-end heal recovery test WRITES/back-fills/identity-taken; (d) bootstrap ack fact reads the ack file. 4 new tests pass; updated 3 obsolete handover assertions; full rotate/heal/session_start/after_join/bin_help suites green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-e9b20f31, SL7.15): accepted. Reviewed the ARTIFACT, not the report. (a) rotate.py cmd_ack continue branch now reads _prev_gen and no-ops only when gen_after==args.gen; other generations print the stale line naming both gens and FALL THROUGH to the existing write+backfill path (verified: the fall-through is not an early return; the write+ref-validation+commit below is unchanged). (b) _rotate_ack_file renames seats/<seat>.ack.json -> .ack.gen<N>.json; placed at the rotate-self success path after the result="success" record write, and in heal._recover_seat before spawn_window; F8 answer shape kept. Ordering is right: the successor bootstrap (s11) is written BEFORE the rename, so the ack fact still resolves from the live file. (d) _derive_bootstrap_fact ack now reads the ack FILE, returns ack: none when absent, reason None. Ran the tests myself: test_heal_ack_rotation.py 4 passed; test_rotate_handover.py 34 passed; heal/heal_seats/session_start_bootstrap/session_start_seat_pre_spawn/after_join_service/bin_help_smoke 107 passed 3 skipped. The 3 updated handover assertions are STRENGTHENED (now assert live ack gone AND rotated name present), not weakened. CAVEATS recorded, not blocking: (1) _rotate_ack_file dead branch — str(path).endswith(".ack.gen") is never true and no writer ever sets consumed_at, so the double-rotate guard is inert (harmless; a second call simply no-ops on not-exists). (2) part (c) test assertion `not in out2 or "this is gen 5" in out2` is a weak OR; the meaningful assertions around it (ack written with session_ref, back-fill line, row identity) are tight. (3) rotated .ack.gen<N>.json files accumulate with no GC — acceptable, small. NEAR MISS: a reader that satisfies the claim by comparing gen only in the print statement and still returning 0 would pass a shallow read; this implementation does not — the return 0 is inside the gen-equality branch.
<!-- THOUGHT:END -->

PARENT ACCEPT: g15.25 build order implemented on built bytes — gen-aware ack no-op (a), ack rotation on completed rotation + pre-recovery (b), end-to-end heal recovery identity (c), bootstrap ack fact from the ack file (d). Reviewed artifact + reran suites (4 + 34 + 107 green). Two caveats: inert double-rotate guard, weak OR in the part (c) stale-line assertion.
