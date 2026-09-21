---
id: experiment:a00-4711d0aa-8b1185
mint_id: aa7d007ea5724ad9bb26032f56724323
type: experiment
parents:
  - hypothesis:l4-the-prime-successor-window-name-derives-from-the-season-and-loop-cells-never-copies-the-predecessor-prefix-and-the-chain-reaps-by-seniority-across-prefixes
next_edges: []
confidence: 0.85
edited_by: a00-4711d0aa
evidence_runs:
  - experiment:a00-4711d0aa-8b1185
line_ceiling: 40
loop: hypothesis:l4-the-prime-successor-window-name-derives-from-the-season-and-loop-cells-never-copies-the-predecessor-prefix-and-the-chain-reaps-by-seniority-across-prefixes@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 59
profile: balanced
role: kid
scaffold_hash: 4b51ef7b32d8b1cd
season: 2
title: "SM.107 built: prime window name derives S/L from live ladder cells, reap sorts by seniority across prefixes"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-4711d0aa-8b1185

## Experiment

SM.107 — a g15 BUILD round (owner 09-18 05:2xZ; measured pre-fix state
reproduced first, then the claim implemented and proved on the built bytes).

### Pre-fix state (measured)
- `rotate.py` step 3 (the `is_chain_seat` branch of `cmd_rotate_self`, ~L18459)
derived the successor with `_derive_successor_name(_existing_for_chain,
prefix=seat)`, which COPIES the predecessor window's prefix: `belam-S1-L4-XXXI`
-> `belam-S1-L4-XXXII`. Live tmux showed `belam-S1-L4-XXVII..XXXI` while the
ladder read `current_season: 2` and the L5 plan was the active loop.
- `_split_roman_suffix` increments the numeral only; the S/L token was never
read from a cell.
- `_belam_oldest` sorted the five-window chain by NUMERAL ONLY, so after a
token change `belam-S2-L5-I` (numeral 1) would be reaped while `belam-S1-L4-V`
stayed — the newest window reaped.
- `config:rotations` after_join `belam-chain` grepped the literal
`belam-S1`; 11 test files carried `belam-S1` strings (most as fixture keys).

### Built
- `rotate.py`: `_chain_token(name)` (one reader of the `-S<season>-L<loop>`
token), `prime_window_name(root, predecessor, prefix)` (season from ladder
`current_season`, loop from ladder `current_loop`; numeral continues only when
the predecessor's token MATCHES, else restarts at I; falls back to the
predecessor's token when the ladder has no cells so a pre-cell fixture root is
byte-identical), and `_window_seniority` (reap key `(token, numeral)`,
oldest-first). Step 3 now calls `prime_window_name(root, own_chain_name,
prefix=seat)`; `_belam_oldest` sorts with `_window_seniority`.
- `.agi/nodes/.geometry/ladder.md`: added the missing `current_loop: 5` cell.
- `.agi/context/schemas/[ladder].md`: declared the `current_loop` field.
- `.agi/nodes/.geometry/rotations.md`: after_join `belam-chain` now
`grep -E 'belam-S[0-9]+-L[0-9]+'` (passes the producing/filter judge: measured
refusal `None` through `_resolve_startup_placeholders` + `_producing_refusal`).
- New `extensions/agi/tests/test_prime_window_name.py`: 6 tests — restart on
token change, continue on same token, fallback without cells, the LIVE node's
grep pattern matches both prefixes and no literal `grep belam-S1`, reap across
prefixes reaps `belam-S1-L4-XXIX` not `belam-S2-L5-II`, and an END-TO-END
rotate-self step 3 with season 2 / loop 5 spawning `belam-S2-L5-I`.

### Test evidence
`python3 -m pytest extensions/agi/tests/test_prime_window_name.py
.../test_rotate.py .../test_rotate_handover.py .../test_spawn_name.py
.../test_heal_watch.py .../test_rotate_selfreap.py .../test_heal_seats.py
.../test_heal_pin_reap.py -q` — all green (378 passed in test_rotate + the
new file; 130 passed in the heal/selfreap set).

## Evidence

Production lines measured with `git diff --numstat` (added column):
`extensions/agi/bin/rotate.py` 53, `[ladder].md` 4, `ladder.md` 1,
`rotations.md` 1 = **59 added / 5 deleted**, ceiling 40 (1.5x — under the 2x
re-brief line, recorded in frontmatter). Test file excluded.

Agent Notes: see the hypothesis node's brief (SM.107).

## Agent Notes
SM.107 built: prime_window_name reads season from ladder current_season and loop from the new current_loop cell, restarts numeral at I on a token change; step 3 of rotate-self calls it; _belam_oldest sorts by (token, numeral) so a token change reaps the oldest prefix; after_join belam-chain greps belam-S[0-9]+-L[0-9]+; 6 tests in test_prime_window_name.py incl. end-to-end rotate-self spawn of belam-S2-L5-I, plus green test_rotate/test_rotate_handover/test_spawn_name/heal set. 59 production lines (1.5x ceiling 40).
