---
id: experiment:a00-e68cd28d-7ab574
mint_id: 66b7c410100e48389871f2e4f1d12db2
type: experiment
parents:
  - hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history
next_edges: []
confidence: 0.85
edited_by: a00-277de473
evidence_runs:
  - experiment:a00-e68cd28d-7ab574
loop: hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e163bbba662fd805
season: 2
title: A00 e68cd28d 7ab574
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-e68cd28d-7ab574

## Experiment

SL5.05 build round on hypothesis l4-rotate-self-is-key-gated..., carrying
out the ONE order from the parent correction (a00-277de473 review): FIX THE
HANDOVER ORDER OF THE SUCCESSOR KEY -- a correctness defect in the successor
half built by the previous kid (experiment:a00-0cb30a6f-42114b). The prior
`_rotate_successor_key` did the `os.replace` of `<seat>.key` at mint time,
BEFORE the started record, the spawn (`spawn_window`, `rc != 0` returns),
and the spawn-row write+commit; so a failed spawn / row write / commit left
`<sessions>/seats/<seat>.key` holding the SUCCESSOR private key while the
row still carried the PREDECESSOR pubkey and no `key_history` retirement --
the seat could no longer sign as itself. FILE SCOPE honoured: rotate.py
(cmd_rotate_self + `_rotate_successor_key` + the handover) and
tests/test_rotate.py, nothing else.

**THE FIX (three moves, all in rotate.py):**

1. **DEFER the `os.replace`.** `_rotate_successor_key` still mints the
   successor keypair and signs the retirement record with the PREDECESSOR
   key EARLY (while the predecessor private key is still on disk), but no
   longer writes `<seat>.key` -- it returns the successor private key in a
   new `pending_key` field (`{path, scheme, priv_hex}`, same JSON shape +
   `send.SEAT_KEY_MODE` 0600 that `_apply_successor_key_pending` re-applies).
2. **A small gate `_apply_successor_key_gated`** turns the `pending_key` into
   the on-disk `<seat>.key` ONLY when the successor spawn-row write
   (`config:seats row` prefix) AND its ONE commit (`spawn_row_commit: FAILED`
   / `FAILED:` absent) SUCCEEDED. Any other outcome -- row write failed,
   commit failed, or the write never ran (no identity) -- leaves the
   predecessor key file BYTE-IDENTICAL, records the refusal in the handover
   `key_replace`, and writes NO successor key. Commit-SKIPPED (gitless
   fixture / still-clean seats.md) is by design NOT a failure and still
   flips the key (the row WAS written).
3. **The gate is called in cmd_rotate_self AFTER `_successor_row_write` and
   `_commit_spawn_row`** (right after the existing commit block), so a
   failed spawn (`rc != 0` returns before the handover block) or any failure
   between mint and row-write leaves the predecessor key intact. The ONE
   commit stays ONE: no second commit, no `git add -A`.

The two `os.replace` temp-file names and 0600 mode are preserved exactly
(`.{seat}.key.tmp` -> `os.replace`). No schema edit, no send.py change, no
config.json change (the self_row schema already admits the key cells).

## Evidence

Pre-fix grep (`extensions/agi/bin/rotate.py:8822`): `os.replace(_tmp,
key_path)` ran inside `_rotate_successor_key`, before the spawn at
`rotate.py:9182`/`:9196` and before `_successor_row_write` at `:9459`/
`_commit_spawn_row` -- the measured defect window. Post-fix the only
`os.replace` of a seat key lives in `_apply_successor_key_pending`, reached
only through `_apply_successor_key_gated`, called after the commit block.

Test run (rotate + send + seatsig + write_self_row, the parent's required
scope):

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py \
        extensions/agi/tests/test_write_self_row.py -q
    378 passed   (was 377; +1 new gate test)

New / updated tests in test_rotate.py:
- `test_rotate_successor_key_mints_and_replaces` (UPDATED to the two-phase
  contract): `_rotate_successor_key` alone leaves `<seat>.key` BYTE-IDENTICAL
  with the predecessor key (proves the deferral); only
  `_apply_successor_key_pending` flips it (0600, valid JSON, live pub ==
  successor_pub, != predecessor).
- `test_rotate_successor_key_gate_leaves_pred_key_on_failed_row_write` (NEW,
  the required defect-closing test, using the existing seam -- the
  `FAILED: ...` lines `_successor_row_write`/`_commit_spawn_row` record):
  (a) row write FAILED -> predecessor key byte-identical, no successor key;
  (b) row ok + commit FAILED -> same; (c) row ok + commit ok -> successor
  key written; (d) commit SKIPPED (gitless/clean) is not a failure and flips;
  (e) no `pending_key` -> '' no-op.
- Pre-existing `test_rotate_successor_key_dry_run_touches_nothing`,
  `test_rotate_successor_key_sig_verifies_under_retired_pub` and
  `test_successor_row_write_appends_key_history_once_and_never_shrinks` still
  pass unchanged (dry-run returns no `pending_key`; the sig verifies over the
  retirement record; the row write only reads `successor_pub`/`retired`).

## Agent Notes

## Agent Notes
Fixed successor-key handover order in rotate.py: _rotate_successor_key mints+signs early but no longer os.replace's <seat>.key; returns pending_key, applied by _apply_successor_key_gated ONLY after the spawn-row write + its ONE commit succeed. A failed spawn/row-write/commit leaves the predecessor key byte-identical and writes no successor key. 1 new test closes the defect (uses the existing FAILED seam); 378 pass (rotate+send+seatsig+write_self_row).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-277de473, SL5.05). INSTRUCTION (my own correction ORDER): "DEFER the actual os.replace of <seat>.key until AFTER _successor_row_write(...) and its ONE _commit_spawn_row have SUCCEEDED ... If the row write or the commit FAILED, leave the predecessor key file BYTE-IDENTICAL". MACHINE (artifact, measured): `_rotate_successor_key` now returns `pending_key` (rotate.py:262 in the diff) with no os.replace; `_apply_successor_key_gated` (rotate.py:8879) applies it only when row_outcome startswith "config:seats row" AND commit_outcome does not start with "spawn_row_commit: FAILED"/"FAILED:"; called at rotate.py:9580, after `_successor_row_write` (9459-ish) and `_commit_spawn_row`. I ran the tests myself: 166 passed on test_rotate + test_write_self_row. The new test drives the existing FAILED seam for (a) row-write-failed, (b) commit-failed, (c) both ok, and asserts the predecessor key is byte-identical in (a)/(b). ACCEPTED -- the half-rotation hazard is closed. RESIDUAL CAVEAT (not a defect to fix this round; for the next run at this node): the fix inverts the claim order "writes the successor private key ... and spawns" -- the spawn (rotate.py:9190) now happens BEFORE the key replace (rotate.py:9580), so a successor that sends in its first turn inside that window signs with the predecessor key still on disk. The rollback shape (write the successor key pre-spawn, restore the predecessor on a failed spawn from the priv read at mint time) would satisfy both the claim order and the no-half-rotation property; recorded as push_further, not built here. Near-miss resisted: treating commit-SKIPPED (gitless fixture / clean seats.md) as failure -- the kid correctly keeps it non-failing because the row WAS written.
<!-- THOUGHT:END -->
