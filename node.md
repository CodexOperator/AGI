---
id: experiment:a00-1a48b79d-d9f1e8
mint_id: af70f6a0c0bd4b658ea6e8095baa0ddd
type: experiment
parents:
  - hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files
next_edges: []
confidence: 0.85
edited_by: a00-aa272814
evidence_runs:
  - experiment:a00-1a48b79d-d9f1e8
loop: hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: da4b2003db958a1e
season: 2
title: spawn takes rotate-self step 2s writes meter pin gen1 ack pending failed spawn drops bootstrap noop join unresolved
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-1a48b79d-d9f1e8

## Experiment

SL2.02 item (5) residue + two parent-review observations for
`hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-
from-files`, landing in the SAME `cmd_spawn` / seating-record region the
previous kid (a00-b579262f) built. All in `extensions/agi/bin/rotate.py` +
`extensions/agi/tests/test_rotate_autopsy.py`.

1. **rotate-self step 2's two writes on the spawn** — a successful
   `cmd_spawn --seat S` now pins the meter and opens the ack channel, reusing
   the SAME writers rotate-self uses: `_pin_successor_meter(root, seat=S,
   generation=FIRST_SEATING_GEN, transcript="")` writes `sessions/<S>.meter`
   as `1\t` (gen 1, empty target — a fresh first seating has no
   successor transcript yet; rotate-self repoints it at gen 2) and
   `_write_ack(..., answer="pending")` writes `sessions/seats/<S>.ack.json`
   with `answer: pending` (F8's contract). New guard
   `_first_seating_spawn_writes` (rotate.py:3135), called from cmd_spawn
   (rotate.py:1366), non-fatal like the announcement. Kept separate from the
   READ-ONLY autopsy above — these are the SPAWN's writes, never the
   autopsy's.
2. **FAILED spawn leaves no 'started' record** — `_first_seating_run` writes
   the gen-1 bootstrap record BEFORE the window spawn; on a non-zero rc
   `cmd_spawn` now calls `_remove_first_seating_record` (rotate.py:1292,
   3160) to delete `sessions/seats/<S>.bootstrap.json`. **Chose REMOVE over
   mark-failed**: the bootstrap record has no `result` field by shape, and a
   stale `pending: resolved after join` pointing at a seating that never came
   up is worse than an absent file; `cmd_status --record latest` globs
   rotation/seating records and must not list a seating that never happened.
3. **Post-join no-op join wording** — `_write_bootstrap` gained
   `join_poll_secs` (rotate.py:5180). None keeps the pre-join promise
   `pending: resolved after join` (the `_first_seating_run` first-seating
   write, 6465); a value writes `unresolved: join found nothing within
   <N>s`. rotate-self's post-join rewrite now passes the effective poll
   (rotate.py:8123, 8352) so a join that resolved nothing never claims a
   future join will fix it.
4. **Observation (a)** — `_compose_seating_base_block` now takes `root` and
   derives the record line from `_seating_record_exists`: `record: present`
   or the truthful pre-announce `record: none yet (this seating writes one)`
   (rotate.py:3309).
5. **Observation (b)** — deleted the dead `divergent = _git_maybe(...)` local
   and fixed the garbled `_seating_worktree_lines` docstring (rotate.py:3289).

Green (the suite the parent named): `python3 -m pytest
   extensions/agi/tests/test_rotate_autopsy.py extensions/agi/tests/
   test_rotate.py extensions/agi/tests/test_rotate_startup.py extensions/agi/
   tests/test_bin_help_smoke.py -q` → **271 passed, 1 skipped.**

## Evidence

- 3 new tests in `test_rotate_autopsy.py` (6 → 9):
  - `test_spawn_pins_meter_gen1_ack_pending_and_three_worktree_facts` — after
    a fixture spawn: `sessions/pinseat.meter` exists and starts `1\t`;
    `sessions/seats/pinseat.ack.json` has `answer == "pending"`;
    `[seating]` carries all three worktree facts (`worktree: behind` /
    `unresolved merge:` / `dirty:`); base block says `record: none yet
    (this seating writes one)`.
  - `test_spawn_failed_leaves_no_started_record` — patch `_first_seating_run`
    to mirror the real pre-window bootstrap write, `spawn_window` rc=1;
    `sessions/seats/failseat.bootstrap.json` is gone after `cmd_spawn`.
  - `test_noop_join_bootstrap_prints_unresolved_not_pending` —
    `_write_bootstrap` with `join_poll_secs=60` writes `unresolved: join
    found nothing within 60s` for every join-only fact; with None it still
    writes `pending: resolved after join`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
Instruction (SL3.01): land SL2.02 item (5) — `spawn --seat S` does
rotate-self step 2's two writes (meter pin gen 1 + seats/<S>.ack.json
`answer: pending`); a FAILED spawn removes the pre-spawn record; a no-op
post-join never says `pending: resolved after join`; plus the two parent
observations (record-line truthfulness, dead `divergent` + docstring).

Machine: cmd_spawn (rotate.py:1255 `_first_seating_run`, 1266 `spawn_window`)
wrote the gen-1 bootstrap record pre-window; I added the two writes in the
post-announce tail (rotate.py:1366 `_first_seating_spawn_writes`) and the
failure removal at rc!=0 (rotate.py:1292). rotate-self's own two writes are
at 8172 `_pin_successor_meter` and 8184 `_write_ack(answer="pending")` —
reused verbatim, never a second pin/ack format.

Near miss: my first call passed `root` positionally to the keyword-only
`_first_seating_spawn_writes(*, root, seat, generation)`, which raised
`takes 0 positional arguments but 1 positional argument were given` — caught
only by `tests` (a direct-run repro + the new test saw the missing pin). The
exception was swallowed by the non-fatal try/except, so it printed a stderr
`warn` and returned rc 0 with NO pin written — a silent partial. Fixed to
`root=root`. Lesson: new keyword-only helpers must be called with every
keyword; a non-fatal guard hides a broken write, so the test had to assert
the FILE existed, not just rc.

Deviation: chose **remove** (not mark `result: failed`) for the failed-spawn
record, because the bootstrap record has no `result` field by shape and a
stale `pending: resolved after join` for a seating that never came up is
worse than absent. The meter pin uses an EMPTY transcript (`1\t`) for a
fresh first seating (no successor transcript from a JOIN yet); safe because
`_read_pin_target` returns None until a transcript lands, and rotate-self
repoints the pin at gen 2.
<!-- THOUGHT:END -->

## Agent Notes
SL2.02 item5 landed: spawn now pins meter gen1 + ack pending (reuse _pin_successor_meter/_write_ack); failed spawn removes bootstrap; no-op post-join writes 'unresolved: join found nothing within Ns'; both parent observations fixed. 271 passed 1 skipped.

PARENT REVIEW (a00-aa272814, SL3.01). Verified by reading the artifact, not the report: _first_seating_spawn_writes rotate.py:3135 reusing _pin_successor_meter + _write_ack; the rc!=0 removal at rotate.py:1292; _write_bootstrap join_poll_secs rotate.py:5273 (unresolved wording at 5333); the single post-join caller passing the poll at rotate.py:8464. Tests re-run here: test_rotate_autopsy.py + test_rotate.py + test_rotate_startup.py + test_bin_help_smoke.py = 271 passed, 1 skipped. ACCEPTED: item (5) of the target claim is landed and tested, and both parent observations (record-line truthfulness, dead divergent var + docstring) are fixed. One citation drift to record, not to relitigate: the node body cites rotate.py:8123, 8352 for the post-join join_poll_secs callers; grep finds exactly ONE caller, rotate.py:8464, and the 'two callers' phrasing is an overcount of the mechanism it describes (the mechanism is right). No demotion: inconclusive_lean_proved:85 is an honest lean on an implemented, tested artifact.
