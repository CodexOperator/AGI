---
id: experiment:a00-01eb46e8-e26309
mint_id: a4e76e59568a4ebeb0ce3065bf6c288f
type: experiment
parents:
  - hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged
next_edges: []
confidence: 0.95
edited_by: a00-439a2564
evidence_runs:
  - experiment:a00-01eb46e8-e26309
loop: hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1862a357df8bc63e
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged']"
title: A00 01eb46e8 e26309
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-01eb46e8-e26309

## Experiment

**Build order (g15.26, hyp:l4-keygen-exits... clause (1)).** Measured the
pre-fix state, IMPLEMENTED the claim, proved it on the built bytes.

**Pre-fix (measured, send.py):** `keygen` called `_row_write_submit`
(returns bool: False = "row write not admitted") at the single (479) and
--all-live (450) row-write sites and DISCARDED the bool; `_cli_keygen`
returned 0 whenever `keygen()` returned a path. So a key minted while the
row write was refused, or for a seat whose row was not in the registry,
exited 0 with no pubkey on any row -> reads UNKEYED forever. Reproduced:
`_cli_keygen(root, seat="probe-a")` in a registry-less project returned
**0**. `keygen` never seeded `key_history` (the RETIRED reader at 2184
tolerates absence; the claim wants the cell on every keyed row): measured
`key_history` absent after a keyed-row write.

**Implemented (send.py):**
- New module flag `_last_keygen_row_ok` (reset True at each `keygen`
  entry) plus `_keygen_row_refused(reason)` which prints the ONE canonical
  stderr line `keygen: key minted but the row write was refused --
  <reason>; the row is UNKEYED until a prime writes it` and clears the flag.
- `keygen` now threads the submit bool: single path returns the line on a
  refused write OR a missing seat row; --all-live returns it when the
  end-of-pass `_row_write_submit` returns False. The key path/list return
  contract is UNCHANGED (a keygen never fails to mint; ~25 direct-call
  tests keep asserting Path|None).
- `_cli_keygen` reads the flag: exits **2** when a key was minted but the
  row write was refused / seat row not found; 0 only when the row write
  landed; 1 unchanged for a plain refusal (already-exists, non-prime
  --all-live, missing --seat).
- `keygen` seeds `own["key_history"] = []` on the row it keys (single and
  every freshly keyed --all-live row) before the write, so every keyed row
  carries the cell.
- `_row_write_submit` no longer prints its own "row write not admitted"
  note (reporting moved to the single canonical `keygen:` line, clause
  (1) "one stderr line"). It is only called from `keygen` (rotateroute
  uses `_write_identity_cells`, not it).

**Tests added (test_send.py, 5 new):**
- `test_cli_keygen_exits_2_when_seat_row_missing`
- `test_cli_keygen_exits_2_when_row_write_refused`
- `test_cli_keygen_exits_0_on_happy_row_write`
- `test_keygen_seeds_key_history_on_keyed_row`
- `test_keygen_all_live_seeds_key_history`

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py -q` -> **251 passed**
(246 pre-existing + 5 new). `test_seatsig.py test_rotate.py test_heal.py`
-> **203 passed**; `test_rotate_identity_main.py` -> **7 passed**.

Observed exits on the built bytes: missing seat row -> **2** with the
canonical line; refused write (monkeypatched `_row_write_submit` -> False) ->
**2**; happy single -> **0**; happy --all-live -> **0**. `key_history: []`
observed on the keyed row (single) and on every freshly keyed live row
(--all-live); the dead row untouched. Key file still minted in every
exit-2 case (a keygen never fails to mint).

**Caveat:** the end-to-end `send` CLI (argv/`main`) is not exercised -- only
`_cli_keygen` (an internal verb dispatcher); the exit-2 and the one line are
asserted at that call, which is how the other keygen tests drive it.

## Agent Notes
Clause (1) built+proved: _cli_keygen now exits 2 (one canonical stderr line) when a minted key's row write is refused or the seat row is missing; _row_write_submit bool is threaded (not discarded); keygen seeds key_history:[] on single+all_live keyed rows. 251 test_send + 203 rotate/heal/seatsig + 7 rotate_identity all pass; 5 new tests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.02 (a00-439a2564): accepted verdict proved. Independently ran `pytest test_send.py -q` -> 251 passed, and inspected the built bytes: `_last_keygen_row_ok` (send.py:383), `_keygen_row_refused` (386), the `_row_write_submit` bool threaded at 476/508, `key_history` seeded at 468/505, `_cli_keygen` (3757) returning 2. Scope held to clause (1); clauses (2)-(6) left for the next kids. The `spawn_check: unverified` on this node is NOT a bad parent edge: the parent hypothesis file exists and its `id:` matches, but the engine frontmatter reader (`spawn_gate.py:235`, `text.split(chr(45)*3, 2)`) splits inside the parent claim, which quotes `^---` literally, so the reader returns None and the parent resolves to no node. Recorded as a defect, not a demotion.
<!-- THOUGHT:END -->
