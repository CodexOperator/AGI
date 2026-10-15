---
id: experiment:a00-092dc9fa-b84bb2
mint_id: a1dd0955c3234de2afa7edfb1cf4b835
type: experiment
parents:
  - hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged
next_edges: []
confidence: 0.8
edited_by: a00-7a73752f
evidence_runs:
  - experiment:a00-092dc9fa-b84bb2
loop: hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0512bdd78358340d
season: 2
title: keygen (1) writes the row and is LIVE-keyed; (5) schema declares the cells — kid 1 slice built and proven
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-092dc9fa-b84bb2

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.


# experiment:a00-092dc9fa-b84bb2

## Experiment

Kid 1 of 2 under the parent — items **(1) keygen writes the row + keys every
live row** and **(5) schema cells**. Items (2)(3)(4) (env v1, enc registry
hook, key_history handling, whois verify/RETIRED label) belong to kid 2 and
were NOT touched.

**Before (measured):** `keygen` (send.py 211-241) minted
`<sessions>/seats/<seat>.key` (0600), printed `pubkey:`/`sig_scheme:`, and
wrote **no** row cell — zero live rows carried pubkey, every message read
UNSIGNED. Schema `[config].md` self_row.fields = `[session_ref, session_id,
generation, window, pid]` — no signing cells.

**Implemented:**
- `keygen(root, seat, scheme="ed25519", all_live=False, actor="", role="")`
  mints the 0600 key, then writes `pubkey`, `sig_scheme`, `enc_scheme: none`
  via `write.submit` (the sanctioned writer) into the seat's OWN row under
  the self-row carve-out. A `.key` file that already exists is REFUSED by
  name (non-zero exit, message names seat + key path) — never overwritten.
  Private seed never printed/logged/written outside `sessions/`.
- `keygen --all-live` (CLI flag) keys every LIVE row (live `pid`/`session_id`)
  lacking a pubkey, skips keyed rows, prints one line per live row. The prime
  is the registry-wide writer the schema admits (`written_by: [owner,
  prime_director]`); a seated non-prime falls under the self-row rule and can
  only write its own row. Row write failures are graceful (never abort the
  mint; note on stderr).
- (5) `[config].md` seats list now declares `pubkey`, `sig_scheme`,
  `enc_scheme`, `key_history`, and all four are `self_row.fields` so a row
  write carrying them passes the write guard.

## Evidence

Run: `pytest test_send.py test_seatsig.py test_bin_help_smoke.py test_write.py
test_write_guard.py test_write_self_row.py test_write_master_sensei.py` →
**393 passed, 2 skipped** (183 pre-existing send tests still green). New
tests: `test_keygen_refuses_to_overwrite_existing_key`,
`test_keygen_writes_own_row_cells_through_write_submit`,
`test_keygen_all_live_keys_live_rows_only_and_skips_keyed`,
`test_seated_writer_may_write_own_signing_cells`,
`test_seated_writer_own_signing_cells_still_refuse_other_rows`.

LIVE CLI smoke on tmp root `/tmp/smoke` (3 live + belam, one dead s3, one
keyed s4):
```
keyed s1 ... / keyed s2 ... / keyed belam ... / skipped s4 (already keyed)   EXIT=0
```
config rows after: s1/s2/belam carry pubkey+sig_scheme el25519+enc_scheme
none; s3 (dead) got NO pubkey and no key file; s4 cell untouched. Second
`--all-live` skips all. `keygen --seat s1` on an existing key → `REFUSED: s1's
key <path> already exists; not overwriting`, EXIT=1, key bytes unchanged.

## Verdict

The (1)+(5) slice is built on the shipped bytes and proven by unit tests plus
a live CLI smoke. Not `proved`/`disproved` here — the experiment node is my
own running record; the parent hypothesis's full claim awaits kid 2.

## Agent Notes
Kid 1 slice: item (1) keygen now writes own-row cells (pubkey/sig_scheme/enc_scheme:none) via write.submit self-row carve-out; --all-live keys live rows (pid/session_id) lacking pubkey, skips keyed/dead; existing .key refused by name, never overwritten; env v1/RETIRED/hook/enc impl are kid 2. item (5) [config].md declares pubkey/sig_scheme/enc_scheme/key_history in the seats list AND self_row.fields so the write guard passes. 393 pass + live CLI smoke on tmp root (3 live keyed, dead untouched, keyed skipped, second keygen refuses, bytes unchanged).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-7a73752f): kid 1 claimed (1)+(5) built and proved. I read the artifact, not the report: send.py `_mint_seat_key` refuses when the .key exists, `keygen` writes pubkey/sig_scheme/enc_scheme through `_row_write_submit`->write.submit self-row, `--all-live` filters `_live_row` (pid or session_id) and skips keyed; [config].md declares the four cells in the seats list AND self_row.fields. I independently re-ran the two test batches (257 passed + 136 passed = 393, matching the node) and confirmed the new test names exist (test_send.py:3848/3859/3880, test_write_self_row.py:145/161). Verdict `proved` for the (1)+(5) slice stands. Weakness: the node body still carries the empty scaffold placeholder sections above the real content, and the claim that a non-prime actor degrades gracefully on --all-live is asserted, not proven — the smoke used a tmp root whose write guard is permissive.
<!-- THOUGHT:END -->
