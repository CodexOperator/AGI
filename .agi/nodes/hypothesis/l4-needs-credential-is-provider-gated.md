---
id: hypothesis:l4-needs-credential-is-provider-gated
mint_id: 89331de9413d40538028916cf8877e47
type: hypothesis
parents:
  - goal:g15
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter for the round's own tokens (of the $2 the Prime capped round 2 at; account read 09:10Z $11.89, floor $5.00); no suite run — the single test file only; nothing touches .env/Doppler/<keeper-dir>.
edited_by: thought-master
falsifier: The dry run still prints 'minting per spawn' for pi-local, or a real pi-local kid's env carries an OPENROUTER key, or the openrouter path stops minting, or test_adapters.py fails alone.
file_scope: extensions/agi/bin/adapters/pi_adapter.py (needs_credential only) · extensions/agi/tests/test_adapters.py (one test) · .agi/context/local-maxxing/gpu/kidA_round2_{dryrun.log,env_keys.log,provisioning_delta.txt} · this node + one kid experiment node. Nothing else.
scaffold_hash: 181b9cc6a20bc6ca
season: 2
testable_claim: With adapters/pi_adapter.py:316 needs_credential returning True only when the resolved provider is 'openrouter' (one line + one test in extensions/agi/tests/test_adapters.py), `dispatch.py --dry-run --harness pi-local --tier kid` prints no 'minting per spawn' line, a REAL kid spawned with --harness pi-local has no OPENROUTER_API_KEY in its environment (env keys logged, never values) and provisioning.py status shows no new engine-minted key for it, while --harness pi (provider openrouter) still mints exactly as before and test_adapters.py passes run alone.
tests: "ONE pi parent, ONE kid (Kid A of the GPU endpoint's round 2, re-homed here): the one-liner + its test; proof = the dry-run line, the real-kid env-keys log, the provisioning delta, test_adapters.py run ALONE; parent authors no experiment node, re-runs the dry-run itself as its probe."
title: "needs_credential is provider-gated: a pi-local spawn mints no OpenRouter key"
town: local-maxxing
---
# hypothesis:l4-needs-credential-is-provider-gated

## Measured lines
- Found by the merge-up review of the GPU endpoint round (mur-dcc0e0792 / wf_d7b3eb46-ef7, 2026-09-16): adapters/pi_adapter.py:316 `needs_credential` returns True unconditionally; dispatch.py:2427/2433 therefore mints and injects an OpenRouter key into EVERY pi spawn, including --harness pi-local whose provider row (local-town, cost 0) never names OpenRouter. The round's $0 proof held only for the hand-run argv (kidB_completion.log L9 `env -u OPENROUTER_API_KEY`).
- Prime decision 09:1xZ: fix in-loop as a g15 node from the thought-master's lane (owner rule: every bugfix/optimization finding is a g15 node), cap $2 for round 2.
- Mechanism already read by the reviewer: adapters/__init__.py L114-120 resolve('pi-local') -> adapter 'pi'; L232-233 namespace gate skips for provider != openrouter; dispatch.py L2040-2062 floor guards are provider-gated — needs_credential is the one ungated site.

## CLAIM
With adapters/pi_adapter.py:316 needs_credential returning True only when the resolved provider is 'openrouter' (one line + one test in extensions/agi/tests/test_adapters.py), `dispatch.py --dry-run --harness pi-local --tier kid` prints no 'minting per spawn' line, a REAL kid spawned with --harness pi-local has no OPENROUTER_API_KEY in its environment (env keys logged, never values) and provisioning.py status shows no new engine-minted key for it, while --harness pi (provider openrouter) still mints exactly as before and test_adapters.py passes run alone.

## FALSIFIERS
The dry run still prints 'minting per spawn' for pi-local, or a real pi-local kid's env carries an OPENROUTER key, or the openrouter path stops minting, or test_adapters.py fails alone.

## TESTS
ONE pi parent, ONE kid (Kid A of the GPU endpoint's round 2, re-homed here): the one-liner + its test; proof = the dry-run line, the real-kid env-keys log, the provisioning delta, test_adapters.py run ALONE; parent authors no experiment node, re-runs the dry-run itself as its probe.

## FILE SCOPE
extensions/agi/bin/adapters/pi_adapter.py (needs_credential only) · extensions/agi/tests/test_adapters.py (one test) · .agi/context/local-maxxing/gpu/kidA_round2_{dryrun.log,env_keys.log,provisioning_delta.txt} · this node + one kid experiment node. Nothing else.

## CEILING
$1 OpenRouter for the round's own tokens (of the $2 the Prime capped round 2 at; account read 09:10Z $11.89, floor $5.00); no suite run — the single test file only; nothing touches .env/Doppler/<keeper-dir>.

## Bridge
Proved -> hypothesis:gpu-local-town-openai-endpoint's Bridge becomes true: a burst of kids on --harness pi-local runs at $0 OpenRouter with no unused $5 keys minted; the WS adapter's GPU backend switch follows. Disproved -> the minting site is elsewhere too; name it.
What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-homed from the GPU endpoint round-2 brief (Kid A) to its own g15 node on the Prime ruling 09:1xZ; the finding came from the by-name review, not from a kid, which is why it is minted by the town master with the reviewer's file:line evidence as its measured lines.
<!-- THOUGHT:END -->
