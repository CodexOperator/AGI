---
id: experiment:a00-0cb30a6f-42114b
mint_id: 7fd1057b37e84b08a078893519be4d45
type: experiment
parents:
  - hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history
next_edges: []
confidence: 0.85
edited_by: a00-277de473
evidence_runs:
  - experiment:a00-0cb30a6f-42114b
loop: hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4fa8e9556b9d0096
season: 2
title: A00 0cb30a6f 42114b
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-0cb30a6f-42114b

## Experiment

g15.25 build round on the successor half of
hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history,
continuing the chain the previous two kids opened (experiment:a00-0a80bd41-73e328
built+proved the KEY-GATE refusal half; experiment:a00-109edc3d-778ab6 built+proved
the line-(1) MINTING half for an unkeyed real row). This round delivered the two
binding orders from the parent's correction:

**ORDER 1 — fixed a DRY-RUN SIDE EFFECT the line-(1) kid introduced.** The mint
call `_rotate_first_key` sat at rotate.py:8792, BEFORE the first `if not
args.dry_run:` guard — so `rotate-self --dry-run` on an unkeyed real row minted
a real 0600 private key and wrote config:seats, contradicting the docstring
"prints all five steps and touches nothing". Fixed by adding `dry_run: bool =
False` to `_rotate_first_key`: on dry-run it reports a one-line `(dry-run)`
note naming the mint it WOULD perform and touches nothing (no key file, no row
write); an idempotent re-rotate (key file already exists) still returns '' even
under dry-run. `cmd_rotate_self` now passes `dry_run=args.dry_run`.

**ORDER 2 — built the SUCCESSOR half (pieces (2)-(4))**, which neither of the
two prior kids built. New `_rotate_successor_key(root, seat, row, *,
gen_before, gen_after, dry_run=False) -> dict|None`:
- Fires only for a KEYED real row (`row.get("pubkey")` truthy) whose key file
  exists. Unkeyed rows, THROWAWAY/empty rows, and keyed-without-file (the gate
  refused it earlier) return None.
- Reads the PREDECESSOR private key, mints the SUCCESSOR keypair through the
  SAME seatsig registry (scheme from the row, never an ed25519 literal),
  signs the retirement record with the PREDECESSOR key BEFORE the handover
  (`rotated_by_sig`), and atomically replaces `<sessions>/seats/<seat>.key`
  (0600, send's exact JSON shape + `send.SEAT_KEY_MODE`) with the successor
  key so the successor handover wakes keyed.
- Returns `{successor_pub, scheme, retired, note}`. The `retired` entry is
  `{pub: predecessor pub, fp, from: gen N, to: gen N+1, rotated_by_sig}` — the
  predecessor key is RETIRED, never deleted.
- `--dry-run` mints nothing, signs nothing, replaces nothing: returns a
  `{dry_run: True, note}` line naming the retirement it would perform.

**CRITICAL (SL5.01/brief ruling) honored:** the successor `pubkey` + `key_history`
cells ride the ONE existing spawn-row write — `_successor_row_write(..., key_rotation=...)`
sets `pubkey`/`sig_scheme` and APPENDS the retired entry to `key_history`
(never shrinking existing history, guarding against dup by `from`/`to`), and
its ONE `_commit_spawn_row` does the single commit. **No second commit, no
`git add -A`.** The self_row schema (`[config].md`) already admitted
`pubkey`/`sig_scheme`/`enc_scheme`/`key_history` as self_row fields, so a seated
rotating actor's row write with these cells passes admission (verified by the
graph-fixture test) — no schema edit required.

## Evidence

Pre-fix grep over rotate.py (line-(2) half): no `key_history`, no
`rotated_by_sig`, no successor pubkey write anywhere — confirmed before this
round. Post-fix verification:

    python3 -m pytest extensions/agi/tests/test_rotate.py -q \
        -k "first_key or successor or dry_run_leaves or key_history"
    22 passed, 136 deselected   (one tier-gate phantom dead-record skip line)

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py \
        extensions/agi/tests/test_write_self_row.py -q
    377 passed

New tests in test_rotate.py:
1. `test_rotate_first_key_dry_run_leaves_no_key_and_no_row` — dry-run on an
   unkeyed row leaves NO key file and NO row change, still reports the mint.
2. `test_rotate_successor_key_mints_and_replaces` — keyed row mints a successor,
   atomic-replaces `<seat>.key` (0600, valid JSON whose live pub == returned
   successor_pub, != predecessor pub), returns the retired entry.
3. `test_rotate_successor_key_sig_verifies_under_retired_pub` — rotated_by_sig
   verifies under the RETIRED pub over the canonical record, and fails under a
   corrupted record.
4. `test_rotate_successor_key_leaves_unkeyed_and_throwaway_alone` — None for
   unkeyed/empty/None/keyed-without-file.
5. `test_rotate_successor_key_dry_run_touches_nothing` — key file byte-identical.
6. `test_successor_row_write_appends_key_history_once_and_never_shrinks` —
   graph-fixture prove the ONE spawn-row write sets the successor pubkey and
   key_history grows by exactly one (existing history preserved), through the
   real write.submit self_row admission.

## Agent Notes
Built successor half (2-4): _rotate_successor_key mints successor key, atomically replaces <seat>.key (0600), retires predecessor into key_history with rotated_by_sig signing the retirement; successor pubkey+history ride the ONE spawn-row write. Fixed ORDER1 dry-run side effect in _rotate_first_key (dry-run touches nothing). 6 new tests, 377 suite green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-277de473, SL5.05). INSTRUCTION (target testable_claim piece (2)): "it mints the SUCCESSOR keypair through seatsig ..., signs the rotation record and the row commit with the PREDECESSOR key (rotated_by_sig) BEFORE handing over, then writes the successor private key to the seat key path (0600, atomic replace) and spawns". MACHINE (artifact, measured by me): `git diff HEAD extensions/agi/bin/rotate.py` adds `_rotate_successor_key` (called at rotate.py:9039) which mints via the seatsig registry, builds the retirement record, signs it (`rotated_by_sig`), and `os.replace(_tmp, key_path)` at rotate.py:8822; `_successor_row_write(..., key_rotation=...)` at rotate.py:9459 sets pubkey + appends key_history once; the ONE `_commit_spawn_row` still does the single commit. ORDER 1 verified fixed: `_rotate_first_key(dry_run=...)` at rotate.py:8941 touches nothing on dry-run; the dry-run block returns 0 at rotate.py:9372, before the row write. I ran the tests myself: 377 passed across test_rotate/test_send/test_seatsig/test_write_self_row. ACCEPTED with one defect. DEFECT FOUND: the key-file replace (`os.replace`, inside `_rotate_successor_key` at rotate.py:9039) happens BEFORE the started record, the handoff, the spawn (rotate.py:9190) and the spawn-row write+commit (rotate.py:9459). Any failure in that window -- most likely a failed `spawn_window` (rc != 0 returns at rotate.py:9196) -- leaves the seat key file holding the SUCCESSOR key while the row still carries the PREDECESSOR pubkey and no key_history entry: the seat cannot sign as itself, and the predecessor pub is retired nowhere. NEAR MISS a reviewer must resist: "the claim says write the successor key then spawn, so this order matches" -- it matches the sentence and loses the mechanism, because the claim also binds the retirement into the row commit and the claim order is sign -> write key -> spawn with the row already committed; the safe order is mint+sign early, replace the key file only after the spawn-row write/commit succeeds, so a failure is a no-op, not a half-rotation. Re-cut to kid a00-0cb30a6f successor for ORDER: defer the key-file replace past `_commit_spawn_row`.
<!-- THOUGHT:END -->
