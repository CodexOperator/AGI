---
id: experiment:a00-7fa2bf30-4e07ec
mint_id: 2669f2897f5d4ad392cc16c79f385a4f
type: experiment
parents:
  - hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
next_edges: []
confidence: 0.9
edited_by: a00-91bb3a6a
evidence_runs:
  - experiment:a00-7fa2bf30-4e07ec
loop: hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 290ec70f1613f001
season: 2
title: Live config prime-authority resolves by-key when prime session_ref empty
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-7fa2bf30-4e07ec

## Experiment

Closing the one softness the parent left in (e): `test_e` HARDCODED the
`prime-authority` template entry (label/cmd copied into the test) and stubbed
the seam with a monkeypatched subprocess.run, so the REAL `config:rotations`
node could drift into a shape the by-key mechanism does not cover and the
test would still pass. This round adds a LIVE-CONFIG test that reads the
actual node through the same loader rotate.py uses and asserts the RESOLVED
SHAPE, not the producing path.

Added `test_e_live_prime_authority_entry_resolves_by_key_from_the_live_node`
to `extensions/agi/tests/test_rotate_startup.py`:

1. Locates the graph root as `parents[3]/.agi` (the checkout under test) and
   `rotate._load_templates(graph)` from the REAL `nodes/.geometry/
   rotations.md` -- the exact loader and path rotate.py resolves.
2. Pulls the REAL `prime-authority` first_turn entry from BOTH the
   `director` template and its `prime_director` mirror.
3. Builds the fully-filled canonical values map with
   `rotate._first_turn_values` (so the prime row's REAL pubkey is used) and
   forces `prime_ref=""` -- the SL7.06 default where the prime row's
   session_ref is empty.
4. Asserts the entry resolves WITHOUT a refusal (no ValueError), its
   resolved command is the by-key form (`--key <pubkey>`), `{prime_ref}` /
   `{prime_key}` are gone, and `rotate._producing_refusal(resolved) is
   None`. Asserts the RESOLVED SHAPE only, so a future re-cut to
   `--key {prime_key}` still passes.

Skips (not fails) only when the live rotations node or the requested
`director`/`prime_director` template is genuinely ABSENT, so the hermetic
suite stays runnable off-repo; a PRESENT node that fails to resolve is a
live-drift finding, surfaced as a test failure naming the live cmd line.

## Evidence

`config:rotations` was NOT edited (parent instruction). The code map
`_STARTUP_FALLBACKS = {"prime_ref": "--key {prime_key}"}` in rotate.py was
already in place from the prior kid; no rotate.py change was needed.

EXACT LIVE LINE READ from the node (`rotate._load_templates` on the real
rotations.md) -- BOTH the `director` template and its `prime_director`
mirror still declare:

    python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam

(the `{prime_ref}` form is unchanged; the by-key resolution comes from the
per-placeholder code map, not a template edit -- exactly the case the parent
flagged as uncovered).

REAL prime row pubkey read from the live seats registry (via
`_first_turn_values`) with `prime_ref` forced empty:

    b82e1378b698462ee680a6b7c5cce7abd65e6059459b124f1139babb9e2e97c8

RESOLVED (both templates, identical):

    python3 extensions/agi/bin/send.py whois --key \
    b82e1378b698462ee680a6b7c5cce7abd65e6059459b124f1139babb9e2e97c8 \
    --claim belam

`_producing_refusal(resolved) is None` -- the resolved by-key whois form
passes the startup producing allowlist.

Suite (named files only):

    test_rotate_startup.py -k live_prime_authority : 1 passed
    test_rotate_startup test_send test_rotate_templates test_rotate_next : 373 passed
    test_seatsig test_bin_help_smoke : 74 passed, 3 skipped

Also observed (pre-existing, unrelated): a `config:seats is deprecated; use
config:posts` fallback notice fires from `_first_turn_values`, and the
tier-gate logs a phantom dead running record -- both harmless to this run.

## Agent Notes
LIVE-CONFIG test closes test_e softness: real config:rotations director+prime_director prime-authority (whois {prime_ref} --claim belam) resolves by-key no refusal with prime_ref empty; asserts resolved SHAPE only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-91bb3a6a, SL7.16). ACCEPTED, closes the round. Added test_e_live_prime_authority_entry_resolves_by_key_from_the_live_node, which loads the REAL config:rotations through rotate._load_templates, takes the prime-authority entry from both the director template and its prime_director mirror, builds values from _first_turn_values with prime_ref forced empty, and asserts the RESOLVED SHAPE (by-key whois, no refusal, allowlist clean) rather than the producing path. Parent ran it: both templates still declare 'whois {prime_ref} --claim belam' and both resolve to 'whois --key b82e1378... --claim belam'; 451 passed, 3 skipped across the named set. config:rotations stayed READ-ONLY, per the round. This is the evidence the claim's (e) needed: the by-key transition is proven on the live node bytes, not on a copied line.
<!-- THOUGHT:END -->

PARENT VERDICT (a00-91bb3a6a, SL7.16): ROUND ACCEPTED as inconclusive_lean_proved:90. Three kids built the F18 code half on this branch. send.py whois resolves by --key (pubkey prefix, >=8 hex, unique, pubkey never key_history) and --seat, printing by key / by name and the row window. rotate.py fills {prime_key}/{prime_seat} from the prime row even when session_ref is empty, and _STARTUP_FALLBACKS maps an empty {prime_ref} to the whole by-key fragment, so the CURRENT template resolves prime authority by key instead of refusing. _producing_refusal is None on the current live entry, and the composed STARTUP block shows IS-AUTHORIZED by key. 451 passed / 3 skipped on the named set. NOT PROVED (why not 'proved'): the compose-level IS-AUTHORIZED line ran with the whois subprocess stubbed; the real rotate-spawns-send seam is asserted as argv shape only, and three kid verdicts are self-cited. OPEN FOR THE SENSEI: the template re-cut (rotations.md:57 and the prime_director mirror at :98) is now OPTIONAL, since the code map makes the current line resolve by key -- the round reports the line but config:rotations stayed READ-ONLY.
