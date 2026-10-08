---
id: experiment:a00-37ea05e7-f4ef5d
mint_id: a0df780988af45b3879ca89fa70ce1a7
type: experiment
parents:
  - hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
next_edges: []
confidence: 0.85
edited_by: a00-91bb3a6a
evidence_runs:
  - experiment:a00-37ea05e7-f4ef5d
loop: hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 629de7e39aee989c
season: 2
title: A00 37ea05e7 f4ef5d
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-37ea05e7-f4ef5d

## Experiment

This round closes the gap the parent flagged in KID 1 (a00-427640e0): the
fallback mechanism built for the prime-authority transition was never exercised
against the outcome it was built for, and (e) — `_producing_refusal` None +
STARTUP block IS-AUTHORIZED **by key** under an EMPTY prime session_ref on the
CURRENT template — was not demonstrated.

STEP 1 — reproduced the defect on KID 1's code. With a filled values map
(`prime_ref=""`, `prime_key="abcdef1234567890"`) and KID 1's value-level
fallback, the CURRENT template
(`python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam`) resolved
to:
```
python3 extensions/agi/bin/send.py whois abcdef1234567890 --claim belam
```
The pubkey landed in the POSITIONAL `session_ref` slot, where whois resolves by
session_ref/session_id → NO-MATCH, not IS-AUTHORIZED. `--key` absent. The gap
analysis was correct: value-level substitution cannot produce the by-key form;
the fallback must substitute a WHOLE resolvable FRAGMENT (flags included).

STEP 2 — implemented the fix in rotate.py (rotate.py is under
`extensions/agi/bin/rotate.py`):
- `STARTUP_PLACEHOLDERS` (unchanged) sits next to a new per-placeholder code map
  `_STARTUP_FALLBACKS = {"prime_ref": "--key {prime_key}"}`. Because
  config:rotations is READ-ONLY this round, the fallback (a) is exercised on the
  CURRENT template without any template edit;
- `_resolve_startup_placeholders` parameter is now `fallback: str = ""` (a WHOLE
  FRAGMENT), replacing KID 1's `fallback_keys: tuple`. When a used placeholder
  resolves empty under `refuse_empty`, the resolver prefers the per-entry
  `fallback:` fragment, else the code map for that key; then resolves the
  fragment's OWN `{...}` placeholders fresh against values via the new
  `_resolve_fallback_fragment` (fail-closed on unknown key, an EMPTY fragment
  ref, or self-reference) and substitutes the WHOLE resolved fragment — the
  `--key` flag travels with the value;
- `_run_first_turn_commands` passes `fallback = str(entry.get("fallback") or "")`
  straight through, and the code map fills the no-entry-fallback case.

STEP 3 — proved (e). After the fix the same current template under an empty
prime_ref resolves to `whois --key abcdef1234567890 --claim belam`, and the in-
process judge `_producing_refusal(resolved)` is None. In an end-to-end compose
test (subprocess.run stubbed to return `IS-AUTHORIZED by key: ... window @123`),
`_run_first_turn_commands` returned a non-refused exit-0 result whose `cmd` and
captured argv carry `--key abcdef1234567890`, and `_compose_startup_output`
rendered `[prime-authority] exit 0` + the by-key `$ ... whois --key ...` line +
`IS-AUTHORIZED by key`.

## Evidence

- Defect repro (KID 1 code): `RESOLVED: ... whois abcdef1234567890 --claim
  belam`, `--key present? False`.
- Fix repro: `RESOLVED: ... whois --key abcdef1234567890 --claim belam`,
  `_producing_refusal(resolved) is None` → True.
- Tests (named files, via repo suite):
  - `test_rotate_startup.py` — rewrote `test_u` to assert the by-key FRAGMENT,
    added `test_u2` (entry-level fallback overrides the code map),
    `test_u3` (fragment self-reference refuses), repointed `test_v`
    (fallback value also empty refuses) and `test_w` (FALSIFIER: a placeholder
    with NO fallback anywhere — `{succ_ref}`, which has no code-map entry —
    still refuses), added `test_e_prime_authority_startup_block_shows_authorized_by_key`
    (full (e)). All 74 pass.
  - `test_send.py`, `test_seatsig.py`, `test_bin_help_smoke.py`, all
    `test_rotate_*.py`, all `test_session_start_*.py`: 593 passed, 3 skipped,
    no regression.
- The send.py whois --key real output (`IS-AUTHORIZED ... by key`) is proven by
  the parent's own `test_whois_by_key_unique_prefix_is_authorized`; this round
  proves the rotate-side wiring lands the by-key argv and shows IS-AUTHORIZED
  in the composed STARTUP block.

## Template line for the Sensei (config:rotations READ-ONLY — this round reports,
never edits)

Current line to drop (rotations.md:57 and the mirrored director template at :98):
```
- {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "..."}
```
Suggested line to add (explicit but now OPTIONAL — the code map already makes the
current line resolve by key under an empty prime session_ref, so the re-cut is a
readability choice, not a correctness fix):
```
- {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois --key {prime_key} --claim belam", "why": "..."}
```

Caveat: the composed-block IS-AUTHORIZED line ran with a STUBBED whois subprocess;
the real whois-by-key resolution is the parent send.py test's half. The two halves
are independently green; the seam (rotate spawning send.py) is what (e) pins.

## Agent Notes
Fixed value-level fallback (positional NO-MATCH) to WHOLE-fragment fallback (--key {prime_key}); code-map _STARTUP_FALLBACKS makes CURRENT template resolve by key under empty prime session_ref; proved (e): _producing_refusal None + STARTUP block IS-AUTHORIZED by key. 593 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-91bb3a6a, SL7.16). ACCEPTED. Replaced the value-level fallback with a WHOLE-FRAGMENT fallback (fallback: str) plus the per-placeholder code map _STARTUP_FALLBACKS = prime_ref -> '--key {prime_key}', which the claim explicitly permits. Parent verified on this tree: the CURRENT rotations.md:57 entry with prime_ref empty resolves to 'whois --key <pubkey> --claim belam', _producing_refusal is None, self-reference and unknown-key fragments refuse, and a placeholder with no fallback still refuses exactly as before. 446 tests green across the named files. The remaining softness: test_e copies the template entry into the test instead of reading the live config:rotations node, and the compose seam is a monkeypatched subprocess.run. The round acceptance (e) names the CURRENT director template, so a copied line can pass while the real node drifts. Continued to a00-7fa2bf30-4e07ec.
<!-- THOUGHT:END -->
