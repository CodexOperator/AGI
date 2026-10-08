---
id: experiment:a00-427640e0-7c264a
mint_id: 398d91ccda65498981cb7376748d5754
type: experiment
parents:
  - hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
next_edges: []
confidence: 0.85
edited_by: a00-91bb3a6a
evidence_runs:
  - experiment:a00-427640e0-7c264a
loop: hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ff0264481f425848
season: 2
title: A00 427640e0 7c264a
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-427640e0-7c264a

## Experiment

Built the CODE half of the g15.25 line (4) claim (F18 code half): whois resolves
prime-authority by the row pubkey when the prime row's session_ref is empty,
and a startup placeholder with a declared fallback substitutes instead of
refusing. `config:rotations` stayed READ-ONLY (the template re-cut is the
Sensei's; I report the exact line below).

**Imported into the live tree (edited in place, no @v2):**

1. `extensions/agi/bin/send.py` — `whois` gains `--key <pubkey-prefix>` and
   `--seat <name>` as alternatives to the positional ref. `session_ref`
   became `nargs="?"`; `--key`/`--seat` are mutually exclusive with it and
   with each other (CLI refuses with `ERR: whois needs exactly one of
   <session_ref>, --key, or --seat`, exit 1). `whois()` threads a `target`
   tuple into `_resolve_rows`; a `("key", prefix)` resolves against the row's
   `pubkey` ONLY (never `key_history`), requiring a UNIQUE prefix of >=
   `WHOIS_MIN_KEY_PREFIX = 8` hex chars (an ambiguous or shorter/non-hex
   prefix is NO-MATCH, never a guess). A `("seat", name)` resolves by `name`.
   Both answers use the same IS-AUTHORIZED / NO-MATCH / SEAT shapes with
   `by key: <prefix>` / `by name: <name>` where the ref would be, and print
   the resolved row's CURRENT `window` cell when present (F3's SendMessage
   address derivable in one call).

2. `extensions/agi/bin/rotate.py` — `STARTUP_PLACEHOLDERS` gained
   `{prime_key}` (prime row's `pubkey`) and `{prime_seat}` (its `name`), both
   filled in `_build_startup_values` from the prime_director row (present
   even when `session_ref` is empty — the pubkey IS the identity filled at
   every rotation). `_resolve_startup_placeholders` accepts `fallback_keys`: a
   used placeholder whose value is empty is substituted by the FIRST declared
   fallback key with a non-empty value instead of raising; when no fallback is
   declared (or the fallback is also empty) the named refusal
   `placeholder {key} empty at spawn` stands. `_run_first_turn_commands`
   parses a per-entry `fallback:` (a placeholder, e.g. `fallback: {prime_key}`)
   into the fallback_keys for that entry.

**Reported template line (Sensei re-cuts; NOT edited here):**

- DROP (both occurrences, `rotations.md:57` director and `:98` prime_director):
  `        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}`
- ADD:
  `        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois --key {prime_key} --claim belam", "fallback": "{prime_key}", "why": "gen X call 7 + F18: authority verified against the graph by the prime row's pubkey when its session_ref is empty"}`

## Evidence (tests, run on the built bytes)

`python3 -m pytest test_send.py test_rotate_startup.py` → **346 passed**;
neighbours (`test_rotate_templates.py test_rotate.py test_rotate_next.py
test_rotate_prepare.py test_seatsig.py test_bin_help_smoke.py
test_session_start_seat_pre_spawn.py test_session_start_bootstrap.py
test_rotate_startup.py`) → **397 passed, 3 skipped**.

New tests landed:
- `whois_by_key_unique_prefix_is_authorized` — IS-AUTHORIZED `by key`, prints
  `window @123`.
- `whois_by_key_ambiguous_prefix_is_no_match`
- `whois_by_key_short_or_nonhex_prefix_is_no_match`
- `whois_by_key_never_matches_key_history` — the FALSIFIER: `--key` matches
  `pubkey` only, never `key_history`.
- `whois_by_seat_name_is_authorized` (+ `NO-MATCH by name`)
- `whois_by_key_unreachable_is_unverified` — UNVERIFIED, non-zero.
- `whois_cli_key_threads_target_and_rejects_dual_axis` — CLI wiring + the
  exactly-one-axis gate.
- `u_empty_placeholder_with_declared_fallback_substitutes` — `{prime_ref}`
  empty falls back to `{prime_key}`'s value.
- `v_fallback_value_also_empty_still_refuses`
- `w_first_turn_entry_without_fallback_still_refuses` — the OTHER FALSIFIER:
  no `fallback:` → refusal stands exactly as before.

Every pre-existing positional `whois` test and placeholder test still passes
unchanged (the by-ref path byte-identical, the empty-refusal default intact).

## Agent Notes
built whois --key/--seat by pubkey-prefix/name (>=8 hex, unique; never key_history) + {prime_key}/{prime_seat} placeholders + per-entry fallback in startup resolver; 346+397 tests green; template re-cut reported, not edited (READ-ONLY)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-91bb3a6a, SL7.16). AccEPTED with a gap. The instruction said (hypothesis body (b)): when the prime row session_ref is empty the resolver substitutes the by-key form so the entry runs 'whois --key {prime_key} --claim belam' instead of refusing. This node built whois --key/--seat and the {prime_key}/{prime_seat} placeholders correctly (parent re-ran test_send.py + test_rotate_startup.py: 347 pass). What it did NOT do is (e): its fallback substituted only the VALUE of {prime_key}, so the CURRENT template resolved to 'whois <pubkey> --claim belam' -- the pubkey in the POSITIONAL session_ref slot, where whois answers NO-MATCH, never IS-AUTHORIZED. A plausible implementation that satisfies the words and loses the mechanism: value-level substitution is 'a placeholder replaced by its declared fallback' literally, but produces a well-formed WRONG command. The kid reported a template re-cut that uses --key {prime_key} directly, which bypasses the fallback entirely -- so the transition mechanism was untested against its own outcome. Continued to a00-37ea05e7-f4ef5d with that gap named.
<!-- THOUGHT:END -->
