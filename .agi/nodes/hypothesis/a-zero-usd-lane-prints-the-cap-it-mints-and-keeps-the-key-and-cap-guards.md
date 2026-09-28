---
id: hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards
mint_id: 6bc640058a4d49d5b89998561ea402df
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: a00-475427c2
scaffold_hash: 99eefc8ec1496ca4
season: 2
testable_claim: "On a zero_usd lane the banner prints the zero_usd_key_limit_usd cap; check_runtime_key_usable and the --cap guard run for every openrouter lane; only the key and account floors are skipped (assigned: director-engine)"
title: A zero-USD lane prints the cap it mints and keeps the runtime-key and cap guards
town: core
---
# hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards

## Measured
TMM.298 (thought-master 13:31Z 09-27, gating 6f9b9a1d9 = trunk 91ae33672), two residues of the zero-USD mint fix:
(1) dispatch.py:2196 prints `credentials: minting per spawn, limit=$<cred_limit>` (1.0) while a zero_usd lane mints a key capped at provisioning.zero_usd_key_limit_usd (0.01; measured: every DH.533-536 key reads limit=0.01).
(2) dispatch.py:2349-2350 -- the outer `if provider == openrouter and zero_usd is not True` skips check_runtime_key_usable AND the --cap guard for zero_usd lanes; only the key floor and the account floor were ordered exempt (TMM.296 point (d)).

## CLAIM
On a zero_usd lane the credentials banner prints the cap actually minted (the zero_usd_key_limit_usd cell); check_runtime_key_usable and the --cap guard run for every openrouter lane; ONLY check_key_floor and check_account_floor are skipped for a zero_usd lane; paid lanes are byte-for-byte unchanged in behaviour.

## Dispatch line
config-max: none new (read provisioning.zero_usd_key_limit_usd, already a cell) / template-max: none / code: the banner's value + the gate split in dispatch.py.

## FALSIFIERS
- a zero_usd dry-run prints limit=$1.0;
- a zero_usd dispatch with a dead runtime key and provisioning ABSENT passes the pre-flight;
- a zero_usd `--cap 0` is not refused;
- a paid-lane test in test_dispatch.py changes outcome.

## TESTS
extensions/agi/tests/test_zero_usd_mint_floor.py (extend: banner value, runtime-key gate, --cap guard on a zero_usd lane) + neighbourhood test_cli.py test_heal_watch.py test_dispatch.py test_bin_help_smoke.py once. timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE. NEVER a real mint: every provisioning call stubbed.

## OPEN (EG.51, experiment:a00-b100d6b9-3307de; the ONE source for conjunct 2 since EG.71, experiment:a00-475427c2-e0ffb1)
No verdict on this node yet; a00-8d4fc327 holds proved, a00-6273b184 holds inconclusive_lean_proved:60. `cli._claim_conjunct_numbers` counts the Measured residues (1) (2) as the conjuncts [1, 2]. The gate (cli.py:1209-1232 at 5a0e89753) reads probes from `--probes` or the agent record, never from a node's frontmatter. The only probe dicts (a00-6273b184 frontmatter) are labelled [1, 4] (DH.608 item numbers), so a tier-parent proved here is refused for uncovered conjunct 2 until a probe labelled 2 is passed. Probe 2 (the gate split) fits Measured (2); probe 1 (the ladder settings cell) fits neither residue.

## FILE SCOPE
extensions/agi/bin/dispatch.py (the banner line + the openrouter gate block only) · extensions/agi/tests/test_zero_usd_mint_floor.py · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines net · <= 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
