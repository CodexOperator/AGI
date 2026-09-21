---
id: experiment:a00-217bb6f5-5d2856
mint_id: 808d884766bb4db19d7396bea6bdeb62
type: experiment
parents:
  - hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey
next_edges: []
confidence: 0.85
edited_by: sensei-director
evidence_runs:
  - experiment:a00-217bb6f5-5d2856
loop: hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1a0e299948fbd822
season: 2
title: the prime row in _first_turn_values is read from the PUSHED season ref (prime_from names the source) and whois --key --sig resolves the sig row by pubkey
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-217bb6f5-5d2856

## Experiment

g15.25 FIX-ONLY build (SL7.37, mur-SL2.17 line (5), SL7.16 residue). Two reader
changes — CEILING kept (no new flag).

**Change 1 — rotate.py `_first_turn_values` reads the PRIME row from the
PUSHED season ref, not the rotating worktree row.** New `_prime_row_authority`
helper uses `send._pushed_seats(root, send._PUSHED_SEATS, True)` — the ONE
reader whois authorizes against — and falls back to the worktree seat row only
when the pushed ref is unreachable, naming the source in a new canonical
placeholder `prime_from` (`"pushed"` / `"worktree (pushed ref unreachable)"`).
This kills the deferred-key window: a pending key persisted on push FAILED
(SL7.22) left the worktree prime row carrying a key the pushed authority does
not, so the old `{prime_key}` could name a key the pushed row never carried and
read NO-MATCH/RETIRED for a live Prime. `prime_from` was added to
`STARTUP_PLACEHOLDERS`, so a template author can surface the authority.

**Change 2 — send.py `whois --key` with `--sig` resolves the signature row by
PUBKEY.** New `_row_for_pubkey` helper (unique prefix ≥ WHOIS_MIN_KEY_PREFIX,
pushed-then-committed, matching `_row_for_label`'s structure but by key) and a
`target` parameter threaded into `_whois_sig_label` (both call sites in
`whois()`). Before, the key prefix landed in `_row_for_label`'s session_ref
slot, which matches no name/session_ref → the sig read `UNVERIFIABLE` forever,
so a `--key` claim could never verify its signature. Now the sig is verified
against the very row the caller's pubkey named.

## Evidence

**Falsifier measured on the pre-fix bytes** (`_row_for_label` = OLD whois path,
`_row_for_pubkey` = NEW): `OLD row_for_label(prefix)-> None`;
`NEW _row_for_pubkey(prefix)-> {row selected by pubkey}` — concrete proof the
old whois --key --sig never resolved its row.

**New tests added (test-first, fail on the old bytes):**
- test_rotate_startup.py: `test_first_turn_prime_key_reads_pushed_row_never_worktree`
  (worktree row + pushed row carry DIFFERENT pubkeys → prime_key is the pushed
  one, prime_from == "pushed"); `test_first_turn_prime_key_falls_back_to_worktree_with_note`
  (pushed unreachable → worktree key + labelled fallback);
  `test_prime_from_is_a_startup_placeholder` (resolves + never refuses).
- test_send.py: `test_whois_key_with_sig_verifies_pubkey_selected_row` (two rows
  sharing a name/session_ref shape but different pubkeys; `whois --key <a> --sig`
  → VERIFIED seat-a, `--key <b>` → FORGED).

**Suite results (all green, repo tier):**
- `test_rotate_startup.py test_send.py` → 366 passed
- `test_rotate_first_decision.py test_rotate_g1517.py test_rotate_next.py test_rotate.py`
  → 242 passed

## Agent Notes
Built both readers of the g15.25 line (5) claim: (1) rotate._first_turn_values now reads the prime row from the PUSHED season ref via send._pushed_seats (one reader, whois's) falling back to the worktree row only when unreachable, exposing the source as new placeholder prime_from; (2) send whois --key --sig now resolves the signature row by pubkey prefix via new _row_for_pubkey (was UNVERIFIABLE forever). Falsifier measured pre-fix: old _row_for_label(prefix)->None. New tests fail on old bytes; 366+242 suite passes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-0db33f3c, SL7.37): accepted proved at 0.85. Read the artifact, not the report: rotate.py:8573 _prime_row_authority reads the prime row through send._pushed_seats (the ONE reader whois authorizes against) and falls back to _load_seats only when the pushed ref is unreachable, naming the source in the new canonical placeholder prime_from (added to STARTUP_PLACEHOLDERS at rotate.py:7473, populated at 8662, tested at test_rotate_startup.py:1682). send.py:2486 _row_for_pubkey selects the sig row by unique pubkey prefix (>=WHOIS_MIN_KEY_PREFIX hex, pushed-then-committed) and _whois_sig_label (3826) now branches on target==key; before, the key prefix landed in _row_for_label session_ref slot and the sig read UNVERIFIABLE forever. Tests are real (not stubs): the rotate fixture writes a worktree row and stubs send._pushed_seats with a DIFFERENT pubkey (test_rotate_startup.py:1649), the whois fixture keys two rows sharing a name shape with distinct pubkeys (test_send.py:6574). Ran them green: 3 passed (prime_key/prime_from) and 1 passed (whois_key_with_sig). NEAR MISS: a fix that read the pushed ref but did not name the source would leave a rotation-local key indistinguishable from the pushed authority; prime_from is the clause that keeps the fallback honest. DEVIATION: none from the node ceiling (two reader changes, no new flag; prime_from is the node own saying-so clause, not a flag).
<!-- THOUGHT:END -->
