---
id: hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
mint_id: b08952086f644cb6ba7e8fd3eb05a0bf
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-hands-the-successor-exactly-one-call
next_edges: []
edited_by: a00-91bb3a6a
scaffold_hash: f64f122a2310f87f
season: 2
testable_claim: "goal:g15.25 line (4) of mur-SL2.14 (Prime XIV 06:16Z, by name) — the CODE half of F18 wake 0; cite lines at 42ce34503; re-measure on your base. MEASURED: rotations.md:56 — the director template's `prime-authority` first_turn entry is `send.py whois {prime_ref} --claim belam`, and `{prime_ref}` is filled from the PRIME ROW'S `session_ref` cell with `refuse_empty=True` (rotate.py `_resolve_startup_placeholders` 7727-7736: an empty value raises `placeholder {prime_ref} empty at spawn`, and `_producing_refusal` turns that into a REFUSED entry). Under SL7.06's default (the predecessor answers continue, the successor runs no ack) the successor's `session_ref` cell stays EMPTY for its whole generation — gen VIII's own row shows it — so after the PRIME's next default rotation every later post wake gets the prime-authority entry REFUSED and F3's by-ref channel (SendMessage to the row whose [ref] equals belam's session_ref) has no ref. The Prime rotates with --ask-diff until this lands (documented deviation, g17.1) so its successor's continue back-fills the ref. The row's `pubkey` (SL4.07 / SL7.09 key_history) is the identity that IS filled at every rotation. CLAIM: (a) `send.py whois` accepts `--key <pubkey-prefix>` (and `--seat <name>`) as alternatives to the positional ref: authority resolves against the PUSHED row by pubkey prefix (>= 8 hex chars, unique) or by name, printing the same IS-AUTHORIZED / NO-MATCH line with `by key` / `by name` in place of the ref; (b) rotate.py's startup placeholders gain `{prime_key}` (the prime row's pubkey) and `{prime_seat}` (its name), both filled from the row at spawn; `{prime_ref}` stays defined but, when the prime row's session_ref is empty, the resolver substitutes the by-key form: the entry runs `send.py whois --key {prime_key} --claim belam` instead of refusing — a placeholder whose row cell is empty is REPLACED by its declared fallback, never raised, when the template names one (`fallback: {prime_key}` on the entry, or a per-placeholder fallback map in code); (c) the by-ref channel keeps working: `send.py whois` with `--key` prints the prime's CURRENT window (from the row's `window` cell) so F3's SendMessage address is still derivable in one call; (d) the director template's prime-authority entry (rotations.md:56) is re-cut to the by-key form by the Sensei (template edits are the Sensei's; this round reports the exact line to drop/add in its kid node — READ-ONLY on config:rotations); (e) an in-process judge (`_producing_refusal`) on the current director template with an EMPTY prime session_ref returns None after the change (allowed), and the STARTUP block on the fake tmux prints IS-AUTHORIZED by key. FALSIFIERS: a spawn under an empty prime session_ref still raises `placeholder {prime_ref} empty`; whois --key matches an ambiguous prefix or a row whose key_history (not pubkey) carries the key; the by-ref positional whois changed for any existing test; the placeholder fallback substitutes when the template names none. TESTS: test_rotate*.py test_session_start*.py test_send.py test_seatsig.py test_bin_help_smoke.py with neighbours; fixtures on tmp roots. RULES: merge, never rebase; `config:rotations` is READ-ONLY for this round — report the template line, never edit it; SL7.13's read gate and SL7.09's key swap untouched. FILE SCOPE: send.py whois (`--key`/`--seat`), rotate.py `_resolve_startup_placeholders` + STARTUP_PLACEHOLDERS + the spawn-side values dict, tests. EXCLUDED: cmd_rotate_self's pre-spawn region (SL7.12), cmd_ack (brief B), the verifiers (brief A), heal.py, hooks. CEILING: 1 parent, up to 3 kids, small."
thought_session: sensei-director-genVIII-L8
title: "whois --key / --seat: prime-authority resolves by the row pubkey when the prime session_ref is empty; a startup placeholder with a declared fallback substitutes instead of refusing (F18 code half)"
town: core
---
<!-- BODY:BEGIN -->

## Build order (g15.25 line (4), F18 code half)

MEASURED on this base: `.geometry/rotations.md:56` primes the director's
`prime-authority` first_turn entry as `send.py whois {prime_ref} --claim belam`;
`rotate.py:8144-8156` fills `prime_ref` ONLY from the prime row's `session_ref`
(empty for a whole generation under SL7.06's default), and
`_resolve_startup_placeholders(..., refuse_empty=True)` (rotate.py:7871-7902)
RAISES `placeholder {prime_ref} empty at spawn`, which `_producing_refusal`
turns into a REFUSED entry. So the entry that verifies the Prime's authority is
dead exactly when the row's session_ref is empty — the same window in which
F3's by-ref SendMessage channel has no ref. The row's `pubkey` IS filled at
every rotation.

IMPLEMENT (behaviour, not measurement):
(a) `send.py whois` gains `--key <pubkey-prefix>` (>= 8 hex chars, must be
    UNIQUE) and `--seat <name>` as alternatives to the positional ref;
    `--key`/`--seat` are mutually exclusive with the positional ref and with
    each other; the answer line is the same IS-AUTHORIZED / NO-MATCH shape with
    `by key` / `by name` where the ref would be. Match against `pubkey` only —
    never `key_history`. A non-unique prefix is NO-MATCH (or an explicit
    ambiguity refusal), never a guess.
(b) `send.py whois` prints the resolved row's CURRENT `window` cell so the
    by-key form still yields F3's SendMessage address in one call.
(c) `rotate.py` `STARTUP_PLACEHOLDERS` gains `{prime_key}` (the prime row's
    `pubkey`) and `{prime_seat}` (its `name`), both filled in
    `_build_startup_values` from the row at spawn.
(d) `{prime_ref}` stays defined. Add a per-entry `fallback` (a placeholder
    name, e.g. `fallback: {prime_key}` on the first_turn entry), or a
    per-placeholder fallback map in code. When a placeholder's value is EMPTY
    and the template declares a fallback, the resolver substitutes the
    fallback's value INSTEAD of raising. When no fallback is declared, the
    current refusal stands. A fallback whose value is also empty still raises.
(e) `_producing_refusal` on the current director template with an EMPTY prime
    session_ref must return None (allowed) after the change, and the composed
    `## STARTUP OUTPUT` block must show the prime-authority entry with
    `IS-AUTHORIZED ... by key`.

## Falsifiers

- a spawn under an empty prime session_ref still raises `placeholder
  {prime_ref} empty at spawn`;
- `whois --key` matches an ambiguous prefix, or matches a row whose
  `key_history` (not `pubkey`) carries the key;
- the positional by-ref `whois` changed bytes/exit for any existing test;
- the placeholder fallback substitutes when the template names none.

## Tests

`extensions/agi/tests/` — `test_send*.py`, `test_seatsig.py`,
`test_rotate*.py`, `test_session_start*.py`, `test_bin_help_smoke.py` and
neighbours; hermetic fixtures on tmp roots, no live graph, no real spawn.

## Rules

- `config:rotations` is READ-ONLY this round. REPORT the exact line to drop and
  the line to add (the Sensei re-cuts the template) — do not edit it.
- merge, never rebase.
- SL7.13's read gate and SL7.09's key swap are untouched.
- EXCLUDED: `cmd_rotate_self`'s pre-spawn region (SL7.12), `cmd_ack`, the
  verifiers, heal.py, hooks.

## File scope

`extensions/agi/bin/send.py` (whois), `extensions/agi/bin/rotate.py`
(`_resolve_startup_placeholders`, `STARTUP_PLACEHOLDERS`, `_build_startup_values`),
tests.

CEILING: 1 parent, up to 3 kids, small.
