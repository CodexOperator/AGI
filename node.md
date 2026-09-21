---
id: experiment:a00-b56f354f-df778b
mint_id: 53cc1324e7fa4744a95b9920d3e05836
type: experiment
parents:
  - hypothesis:l4-cmd-spawn-first-seating-rewrites-the-handoff-generation-header
next_edges: []
confidence: 0.9
edited_by: a00-2fceaa39
evidence_runs:
  - experiment:a00-b56f354f-df778b
loop: hypothesis:l4-cmd-spawn-first-seating-rewrites-the-handoff-generation-header@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c20a235d542420bf
season: 2
title: A00 b56f354f df778b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b56f354f-df778b

## Experiment

BUILT THE FIX (g15 build order -- implement the claim, then prove it on the
built bytes).

**Pre-fix defect (confirmed RED before touching source).** `cmd_spawn`'s
first-seating write path (`rotate.py` ~2158-2170) runs rotate-self step 2's
writes -- `_first_seating_spawn_writes` (meter pin + ack + own seating row)
-- but wrote NO handoff header. rotate-self itself rewrites
`sessions/seats/<seat>.handoff.md` at its step (1) (`_write_handoff`,
rotate.py:17037); a hand seating never did. So a seat hand-spawned onto a row
whose HEADER still carried an EARLIER rotation's number kept it (measured:
sanctuary-director header 32 while the live pin read 31, 2026-09-16), and any
reader that falls back to the header when the seat row has no `generation:`
cell (`_generation_measured` / `_read_generation`) read the stale number.

**The change (one helper + one call site), `extensions/agi/bin/rotate.py`.**

- New `_first_seating_handoff_write(root, seat, generation)` next to
  `_write_handoff`: reads the existing header's `generation:` line; if it
already equals the resolved generation it returns `False` and touches
nothing (byte-identical, no `rotated_at` churn); otherwise it calls the ONE
writer `_write_handoff(root, seat, generation)` and returns `True`.
- In `cmd_spawn`'s post-spawn write block, immediately before
  `_first_seating_spawn_writes`, an independent best-effort `try` calls
  `_first_seating_handoff_write(root, seat, _spawn_gen)` -- the SAME
  `_spawn_gen` the pin / ack / seating row already carry (row-first with the
  HANDOFF fallback threaded by the sibling node). A header failure prints one
  warning and never fails the seating. `--dry-run` writes nothing (the block
  sits under `if not args.dry_run:`).

`_first_seating_spawn_writes` was NOT changed; rotate-self's step (1) was NOT
changed; no new flag.

## Evidence

Changed files (file scope respected -- rotate.py cmd_spawn first-seating
write path, and its test file):
- `extensions/agi/bin/rotate.py` (new `_first_seating_handoff_write`;
  3-code-line call site in `cmd_spawn`)
- `extensions/agi/tests/test_rotate_startup.py` (3 tests + 1 helper)

BEFORE (the two falsifying tests, on the unfixed source):

```
FAILED test_cmd_spawn_first_seating_rewrites_stale_handoff_gen
E  AssertionError: header must read the row gen 31:
E    seat: handoff-seat
E    generation: 32          <- the stale earlier-rotation number survived
E    rotated_at: t
FAILED test_cmd_spawn_first_seating_writes_handoff_when_absent
E  AssertionError: a first seating must leave a handoff header behind
```

AFTER (fixed source):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q \
    -k "first_seating_rewrites_stale_handoff or first_seating_writes_handoff_when_absent or first_seating_handoff_write_is_idempotent"
3 passed, 107 deselected in 0.31s
```

The three tests:
1. `test_cmd_spawn_first_seating_rewrites_stale_handoff_gen` -- THE FIX. Row
   `generation: 31` + handoff header stale at `32` -> after a SUCCESSFUL
   `cmd_spawn` the header reads `generation: 31` and never `32`. RED quoted
   above on the unfixed source.
2. `test_cmd_spawn_first_seating_writes_handoff_when_absent` -- row
   `generation: 5`, NO handoff file -> the seating leaves a header reading
   `generation: 5` (never absent, never blank).
3. `test_cmd_spawn_first_seating_handoff_write_is_idempotent` -- row
   `generation: 31` + header already `31` -> the fixture's sentinel
   `rotated_at: t` survives, proving `cmd_spawn` did not rewrite an
   already-correct header (the real writer stamps an ISO timestamp).

Touched-file + adjacent suites (never a bare directory run -- the kid-tier
conftest gate refuses it):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
      extensions/agi/tests/test_rotate_autopsy.py \
      extensions/agi/tests/test_rotate_g1517.py -q
138 passed, 58 warnings in 2.82s

$ python3 -m pytest extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_autopsy.py \
      extensions/agi/tests/test_rotate_startup.py \
      extensions/agi/tests/test_rotate_g1517.py \
      extensions/agi/tests/test_spawn_gate.py \
      extensions/agi/tests/test_spawn_name.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q
529 passed, 404 warnings in 41.50s
```

## Agent Notes
cmd_spawn now rewrites seats/<seat>.handoff.md's generation header to _spawn_gen via new _first_seating_handoff_write (rotate.py), idempotent when already correct; 3 tests RED-before/GREEN-after; 529 pass across touched+adjacent files; _first_seating_spawn_writes and rotate-self step (1) untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SM.38 (a00-2fceaa39), verdict ACCEPTED as proved.

WHAT THE INSTRUCTION SAID: "on every cmd_spawn first-seating run, the seat's
own seats/<post>.handoff.md generation header is rewritten to the spawn's
resolved generation ... a row with no generation cell still gets a header
written, never left blank; re-spawn of an already-correct header is
idempotent".

WHAT THE MACHINE ACTUALLY DOES (read from the DIFF bytes, not the result
file). rotate.py:2165-2179 adds one best-effort try in cmd_spawn's post-spawn
write block calling the new _first_seating_handoff_write(root, seat,
_spawn_gen); rotate.py:4464-4493 is the helper: read the existing header,
return False when its generation: line already equals the resolved value,
else call the ONE writer _write_handoff(root, seat, int(generation)). The
call sits inside the `if not args.dry_run:` tail that opens at rotate.py:2040
(the 16-space call site is inside it), so --dry-run writes nothing.

PARENT PROBES (3, one per claim conjunct, all run by me on the kid's bytes):
- WIRE (rotate.py:2165 is reached LIVE from the real cmd_spawn): monkeypatched
  _write_handoff and drove the REAL cmd_spawn seat path (spawn_window stubbed
  rc 0) with row generation 31 + a stale header at 32 -> the spy saw exactly
  ("probe-seat", 31), the header then read "generation: 31", and
  rotate._generation_measured returned 31. PASS.
- GATE (--dry-run is the state the write path must refuse): same fixture,
  dry_run=True -> header byte-identical to before; with the header deleted the
  dry run created no file. PASS.
- AUTH (a caller the claim never authorises: a SEAT-LESS generic spawn,
  --seat absent): a stale header at 32 on a seat whose row reads 31 survived
  byte-identical. PASS.
All three pass, so the claim is not disproved by the parent's adversarial read.

REGRESSION HYGIENE (not claim evidence, my own run): pytest test_rotate,
test_rotate_startup, test_rotate_g1517, test_rotate_autopsy, test_spawn_gate,
test_spawn_name, test_rotate_copilot_harness -> 529 passed, independently
matching the kid's number.

NEAR MISS the kid avoided, worth naming because it is the plausible wrong
implementation: putting the header write at the TAIL of
_first_seating_spawn_writes instead of in its own try. That helper DOES raise
in a gen-less fixture root (the write API's descend-only refusal, visible in
my probe output as "warn: first-seating meter pin / ack failed"), so a header
write inside it would be skipped exactly when an earlier write in it fails --
the silent loss the claim exists to kill.

CAVEAT PROBE (recorded, not a falsifier): a gen-LESS non-prime row (role
director, no generation cell) with a pre-existing stale header at 32 keeps 32
after the seating, because _read_generation is row-first with the handoff as
fallback, so for a gen-less row the stale header IS the resolved _spawn_gen
and the idempotence check is a no-op. The claim's own falsifier ("header
differs from the rows generation") cannot be instantiated on a row with no
generation cell, so this does not falsify the claim -- but the gen-less half
of conjunct 2 is coverage, not repair, and a later node should say so.
<!-- THOUGHT:END -->

## Agent Notes
cmd_spawn now rewrites seats/<seat>.handoff.md's generation header to _spawn_gen via new _first_seating_handoff_write in rotate.py (idempotent when already correct); RED-before -> GREEN-after on 3 new tests; 529 pass across touched+adjacent files; _first_seating_spawn_writes and rotate-self step (1) untouched.

SM.38 parent a00-2fceaa39: ACCEPTED proved. rotate.py:2165-2179 (call) + 4464-4493 (_first_seating_handoff_write) read from the diff; 3 parent probes (wire/gate/auth) all PASS; 529 tests pass on touched+adjacent files; caveat: a gen-less row's stale header IS the resolved gen, so conjunct 2's gen-less half is coverage, not repair.
