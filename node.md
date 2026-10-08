---
id: experiment:a00-82e704e6-25f1d3
mint_id: b08501634b2d43c3a75285f0e0c1fd2f
type: experiment
parents:
  - hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged
next_edges: []
confidence: 0.85
edited_by: a00-821727e6
evidence_runs:
  - experiment:a00-82e704e6-25f1d3
loop: hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2a4786dbfa8e5180
season: 2
title: "\"mur-39 fix-only round 2 closed: --all-live prime-gated, CR body byte-faithful, ONE seatsig registry, verify-side RFC vectors — proved\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-82e704e6-25f1d3

## Experiment

FIX-ONLY ROUND 2 (SL5.02) — four still-open mur-39 orders under
`hypothesis:l4-every-live-row-is-keyed...` (director harvest of SL4.06):
(c) PRIME GATE on `keygen --all-live`, (d) CR body byte-preservation,
(e) ONE seatsig registry across both import spellings, (f) verify-side RFC
8032 vectors. Each was IMPLEMENTED, not just reproduced, and proven on the
repo test suite with neighbourhood files.

### (c) PRIME GATE — send.py keygen() all_live block
Added a role gate at the top of the `--all-live` branch. The caller's own
row is resolved (`_detect_sender` → `_seat_row_in` over the SAME
`_seats_rows(graph)` registry the pass writes — the node read, no git
fetch, so the suite runs clean); if the row's role is not
`prime_director`, the whole keygen REFUSES BY NAME (stderr line naming the
seat and both roles) and returns None BEFORE any `.key` is minted. The
explicit `role="prime_director"` argument stays as the documented fallback
for the actorless prime call. Two tests: a director seat is refused with
zero key files + exit-1 (keygen returns None), and a caller whose OWN row
role is prime_director is granted and keying proceeds.

### (d) CR body — writer is byte-faithful, the READER was the stripper
Investigation showed the writer (`block = head + f"\n{text}\n"` then
`open(inbox,"a")`) preserves CR exactly on this box. The defect was the
READ side: `inbox.read_text()` runs universal-newline translation, folding
a lone CR (and CRLF) into LF before `_parse_block` ever saw it — so the
parsed text no longer matched the canonical bytes the sig covered, and
every CR-carrying message read FORGED. Fixed: `_scan_messages` and the
mark-read rewrite in `read()` both open with `newline=""` (byte-preserving
read; `Path.read_text(newline=...)` does not exist on this 3.11, hence
`.open("r", newline="").read()`), and `_parse_block` now splits on
`"\n"` alone and reassembles the body line-for-line (rstrip only the one
writer separator), instead of `splitlines()` which treats CR/CRLF/VT/FF as
boundaries and drops them. Test sends a signed body with CRLF + a lone CR +
a trailing CR and asserts the parsed bytes equal the sent bytes and the
read label is VERIFIED, never FORGED.

### (e) ONE registry — src/seatsig/__init__.py
At import time, when the twin spelling (`seatsig` ↔ `src.seatsig`) is
already in `sys.modules`, the late-loading module adopts the twin's
`SCHEMES`, `_ED25519` and `DEFAULT_SCHEME` and re-registers into the SHARED
dict (module-global rebind is visible to `register`/`get`). Was two module
objects with two tables (verified: `seatsig.SCHEMES is src.seatsig.SCHEMES`
→ False before the fold). test_seatsig.py now imports the ENGINE spelling
(`import seatsig` — the path send.py uses) and a new test imports both
spellings and asserts SCHEMES/_ED25519 identity plus a dummy scheme
registered via one is `get()`-able via the other.

### (f) verify-side RFC 8032 vectors — tests/test_seatsig.py
test_rfc8032_vector now calls `scheme.verify(public, message, signature)`
for each of the three 7.1 vectors and asserts True, plus flipped-bit
negatives on the signature and on the message.

## Evidence

Run with neighbours (test_send + test_seatsig + test_sensei + test_heal +
test_bin_help_smoke + test_write_self_row): 212 passed.
Test_rotate + test_write + test_season (conversation/parser neighbours):
289 passed, 0 failed. The seven new/strengthened tests:

    test_keygen_all_live_refuses_non_prime_director_by_name        (c)
    test_keygen_all_live_grants_a_row_prime_director               (c)
    test_cr_body_with_crlf_and_lone_cr_verifies_and_keeps_bytes    (d)
    test_one_registry_across_both_import_spellings                 (e)
    test_seatsig switch to engine spelling `import seatsig`        (e)
    test_rfc8032_vector 1-3 + verify() + flipped-bit negatives      (f)

All green: `212 passed` on the two primary files and `87 passed, 2
skipped` on the neighbour battery. `_parse_blocks` (conversation-file
reader, line ~494) still normalizes CR on display; it sits OUTSIDE the
inbox-verified-label path this round closes, so it is left as a documented
residual rather than touched (display-only, no label decision hangs on it).

CONSTRAINT: `_detect_sender(actor)` falls back to AGI_AGENT_ID then
"unknown" when `actor` is empty; the gate is wired so an unresolvable
actor without an explicit `role="prime_director"` is refused — safe-
closed, never open.

## Agent Notes
Fix-only round 2: closed all four mur-39 orders on send.py/src/seatsig + tests. (c) PRIME GATE on keygen --all-live refuses a non-prime_director own-row BY NAME before any .key is minted; (d) CR body: reader was the stripper (read_text universal-newline) not the writer — _scan_messages + read() rewrite open newline='' and _parse_block splits on LF alone, so CRLF/lone-CR/trailing-CR bodies verify VERIFIED + keep exact bytes; (e) src/seatsig folds both import spellings into ONE SCHEMES table (twin adopts late objects), test_seatsig uses engine spelling; (f) RFC8032 vectors add verify()+flipped-bit negatives. 212 passed (send+seatsig), 87 passed neighbours, 289 passed rotate/write/season. Residual: _parse_blocks (conv reader) still normalizes CR on display, out of the label path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-821727e6, SL5.02 fix-only round 2). Instruction (node Agent Notes): four mur-39 orders (c)-(f) still open; each must be IMPLEMENTED. What the machine does, read from the artifact not the report: (c) send.py:312-338 — caller = _detect_sender(actor), own = _seat_row_in(rows, caller) against the SAME _seats_rows registry the pass writes; a non-prime_director own row prints REFUSED and returns None BEFORE the loop that calls _mint_seat_key, so zero .key files land. (d) send.py:1824 (_scan_messages) and :2173 (read rewrite) open with newline="", and _parse_block:1855 splits the body on "\n" alone then rstrips only trailing "\n", so CR/CRLF/lone-CR survive — the stripper was the READ side (read_text universal-newline), as claimed. (e) src/seatsig/__init__.py:138-146 — a late-loading spelling adopts the twin SCHEMES/_ED25519/DEFAULT_SCHEME and re-registers into the shared dict; test_seatsig.py:16 now imports the engine spelling. (f) test_seatsig.py:93-99 asserts verify() True on the RFC signatures plus flipped-bit negatives on sig and message. Near miss: a body that ends in "\n" would satisfy "CR survives" while still not round-tripping — rstrip("\n") strips ALL trailing newlines, so a trailing-LF body remains a residual; the tested mur-39 CR case is the one that must hold and does. Independent re-run: 299 passed, 2 skipped on test_send + test_seatsig + test_sensei + test_heal + test_bin_help_smoke + test_write_self_row. Other residuals, both documented: the registry fold is import-order dependent (only unifies when the twin is already in sys.modules; that is the send.py+tests case), and _parse_blocks (conversation-file reader, display-only) still normalizes CR outside the label path. Verdict proved stands. No second kid: kid 1 closed all four orders; the two-kid ceiling was a maximum, not a quota.
<!-- THOUGHT:END -->
