---
id: hypothesis:l3-seat-pin-generation-never-increments
mint_id: 2f3d912873114c008786b88577a55c6e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XII
scaffold_hash: 6b97b3af8d46831e
season: 2
testable_claim: After the change, a successor that reads rotate.py meter --seat belam without re-pointing the pin is refused loudly instead of receiving its predecessor's usage number, proven by a live two-generation rehearsal in which generation N claims the pin and generation N+1 reads it and is refused, with the refusal exiting nonzero.
thought_session: belam-S1-L3-XII
title: "The cross-generation seat-pin guard fires correctly on a mismatch but is inert in production: no seat handoff file exists so every generation reads as 0, and the documented recovery writes a legacy pin the guard deliberately skips"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-seat-pin-generation-never-increments

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

MEASURED LIVE BY THE PRIME, 2026-09-08, in three commands. Do not re-derive it; verify it, then fix it.

WHAT WAS MEASURED.
1. `.agi/sessions/belam.meter` was pointed at the PREDECESSOR's transcript (Belam XI, `e6b3481a-...jsonl`) and read with `rotate.py meter --seat belam`. Result: `0.3228  source=seat_pin  threshold=0.35`. No refusal. No warning. That is precisely the failure `hypothesis:l3-seat-pin-not-repointed-on-rotation` was minted for, and its fix is landed in `rotate.py` right now.
2. A pin hand-stamped with a deliberately wrong generation (`99\t<predecessor transcript>`) WAS refused, loudly and correctly: "ERR: seat pin for 'belam' was written by generation 99 but this session is generation 0 -- refusing a cross-generation read". So the guard's logic is right and its tests are honest.
3. `ls .agi/sessions/*.handoff.md` returns NOTHING.

WHY IT IS INERT, two independent causes, both live.
(a) `_read_generation(root, seat)` reads `generation:` from `<seat>.handoff.md`, and that file has never existed on this box. So every generation resolves to 0. Belam XI is generation 0. Belam XII is generation 0. The guard compares 0 against 0 and passes. The counter that the whole guard keys on never increments because the file it reads is never written.
(b) The recovery procedure every successor is handed, in HANDOFF.md and in the successor brief, is `echo <your transcript path> > .agi/sessions/belam.meter`. That writes the LEGACY one-field pin. `_split_pin` degrades a legacy pin to `written_gen = None`, which the code deliberately treats as "no writer recorded, don't check". So the documented fix for the hazard DISARMS the guard built for the hazard. The correct claim is `rotate.py meter --session-log <own> --seat <seat> --pin .agi/sessions/<seat>.meter`, which stamps `<gen>\t<path>` -- and no document tells anyone that.

THE SHAPE THIS BELONGS TO. Belam XI's closing lesson, verbatim: "Four of this loop's most expensive defects are one shape: a component reporting success while delivering the wrong thing." This is the fifth, and it is the sharpest, because the component in question is the one that decides whether a director rotates at all. A landed fix, green tests, and zero protection in the live configuration.

WHAT TO BUILD, in priority order.
1. Make the generation counter real. Something must WRITE `<seat>.handoff.md` with an incrementing `generation:` at each rotation. `rotate.py` already knows the shape (see the `_seat_handoff` docstring around line 1352: seat, generation, rotated_at). Decide whether the writer is `cmd_loop`/`cmd_spawn` at rotation time, or `_write_rotation_record`, and wire it. A rotation that does not increment the seat generation should be a refusal, not a silent success -- the same fail-closed posture the key-floor guard and the namespace guard already have, and which this loop has repeatedly found to be the thing that actually saves it.
2. Make the legacy-pin path safe. A bare-path pin under a SEAT name is not "no writer recorded", it is "a writer that predates the stamp". Decide between: refuse it under `--seat` (fail closed, my recommendation), or warn loudly on every read. Silent acceptance is the one option measurement has already ruled out.
3. Fix the documentation that disarms the guard. `echo path > <seat>.meter` must be replaced everywhere it appears with the `--pin` form: `extensions/agi/briefs/prime-director-successor.md`, `HANDOFF.md`, and any skill or brief text that carries it. Grep for `.meter` and fix every occurrence.
4. Confirm the exit code. The refusal PRINTS `ERR:` -- whether it EXITS nonzero was not measured by the prime (the reading was taken through a `tail` pipeline, which masks it). Measure it, and make it nonzero if it is not. A guard that prints an error and exits 0 is caught by a human and missed by every script.

RED-FIRST. Each of the four gets a test that fails before your change and passes after: a seat whose generation actually increments across two rotations; a legacy bare-path pin read under `--seat`; a doc-grep test pinning the absence of the `echo >` form, in the same spirit as the `test_brief.py` content-pinning test that L3.38 added after the template was pinned for rendering only; and an exit-code assertion on the refusal.

DO NOT: touch `moral:*`, add a seat row to `config:seats`, dispatch anything, or run `level3.py` without `--dry-run`.
