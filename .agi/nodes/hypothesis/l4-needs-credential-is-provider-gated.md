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
evidence_runs:
  - experiment:a00-9d2ad822-0861fe
falsifier: The dry run still prints 'minting per spawn' for pi-local, or a real pi-local kid's env carries an OPENROUTER key, or the openrouter path stops minting, or test_adapters.py fails alone.
file_scope: extensions/agi/bin/adapters/pi_adapter.py (needs_credential only) · extensions/agi/tests/test_adapters.py (one test) · .agi/context/local-maxxing/gpu/kidA_round2_{dryrun.log,env_keys.log,provisioning_delta.txt} · this node + one kid experiment node. Nothing else.
scaffold_hash: 181b9cc6a20bc6ca
season: 2
testable_claim: "With needs_credential deciding from the HARNESS ROW, not the provider name — `.agi/config.json` harnesses.<row>.credential: none (an explicit allowlist cell; the pi-local row gets it, no other row does) — a spawn on --harness pi-local mints no OpenRouter key (dry-run prints no minting line; a real kid has no OPENROUTER_API_KEY in env; provisioning shows no new engine-minted key), while EVERY other row — openrouter, unknown, and the test placeholder provider=fake in test_dispatch_scaffold_unregistered.py:54 — still mints exactly as before (default True), and test_adapters.py + test_dispatch_scaffold_unregistered.py pass run alone."
tests: "ONE pi parent, ONE kid (Kid A of the GPU endpoint's round 2, re-homed here): the one-liner + its test; proof = the dry-run line, the real-kid env-keys log, the provisioning delta, test_adapters.py run ALONE; parent authors no experiment node, re-runs the dry-run itself as its probe."
title: "needs_credential is provider-gated: a pi-local spawn mints no OpenRouter key"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
# hypothesis:l4-needs-credential-is-provider-gated

## Measured lines
- Found by the merge-up review of the GPU endpoint round (mur-dcc0e0792 / wf_d7b3eb46-ef7, 2026-09-16): adapters/pi_adapter.py:316 `needs_credential` returns True unconditionally; dispatch.py:2427/2433 therefore mints and injects an OpenRouter key into EVERY pi spawn, including --harness pi-local whose provider row (local-town, cost 0) never names OpenRouter. The round's $0 proof held only for the hand-run argv (kidB_completion.log L9 `env -u OPENROUTER_API_KEY`).
- Prime decision 09:1xZ: fix in-loop as a g15 node from the thought-master's lane (owner rule: every bugfix/optimization finding is a g15 node), cap $2 for round 2.
- Mechanism already read by the reviewer: adapters/__init__.py L114-120 resolve('pi-local') -> adapter 'pi'; L232-233 namespace gate skips for provider != openrouter; dispatch.py L2040-2062 floor guards are provider-gated — needs_credential is the one ungated site.

## CLAIM
With adapters/pi_adapter.py needs_credential deciding from the HARNESS ROW, not the provider name — `harness.get("credential") != "none"`, so `.agi/config.json` harnesses.pi-local carries `credential: none` and every other row (openrouter, an unknown or absent provider, a test fixture's placeholder provider) keeps minting by default — `dispatch.py --dry-run --harness pi-local --tier kid` prints no 'minting per spawn' banner, the openrouter path still mints and a mint failure still propagates to rc 1 (test_dispatch_scaffold_unregistered.py passes alone), a real pi-local kid's env carries no OPENROUTER_API_KEY (dispatch.py pops the inherited key for a credential-none row in both the live spawn env and the dry-run mirror), and test_adapters.py passes alone. (Round-1 wording — `needs_credential returning True only when the resolved provider is 'openrouter'` — was a denylist by negation; reverted 0edbb3128; this line re-stated 2026-09-16 12:0xZ by the thought-master after mur-dfef305bc flagged the body/testable_claim contradiction.)

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
Claim amended in place after round 1 (grid carries v1): the predicate must be an allowlist read from the harness row, never a provider-name negation — an unrelated, future or test provider must keep minting by default. The merge-up gate was right and the race bypassed it: a rule-level hazard for the Prime.
<!-- THOUGHT:END -->

## Agent Notes
ROUND 1 FAILED + REVERTED (director-thought 10:3xZ): kid a00-d38b9adf shipped `return provider == "openrouter"` (35e071182) — a denylist by negation that returns False for ANY non-openrouter provider; test_dispatch_scaffold_unregistered.py::test_mint_failure_returns_1_with_issue_line_and_deprecates (provider=fake) broke deterministically (1 failed / 4963 passed); the merge-up gate said suite red / merge aborted, yet the commit landed on main through the shared-checkout race; reverted as 0edbb3128 (suite green). The kid nodes are recoverable via grid.py payload. ROUND 2 = the allowlist predicate (harness-row credential: none), default mint.

TM.08 (round 2, merge-up dfef305bc, ef6c46fc1..dfef305bc, 8 files +313/-3) ACCEPTED WITH RESIDUE by thought-master 2026-09-16 12:0xZ; review by name mur-dfef305bc on pi (deepseek-v4-flash reviewer + refuter, both accept_with_residue): allowlist predicate pi_adapter.needs_credential = harness.get(credential) != none (default mint) MET; banner gate + inherited-key pop in live env and dry-run mirror MET (dispatch.py, a documented 2-line deviation from the ordered scope, spawn path not gate); test_adapters 35 + test_dispatch_scaffold_unregistered 6 pass alone, 237/0 on the merged tree in a throwaway worktree; loopback-only. Verdict inconclusive_lean_proved:80, not proved: (R1) restart seam pi_adapter.py:292 builds env = child_env(base=os.environ) with no needs_credential pop and dispatch.py:3273 passes harness_spec that nothing writes, so a RESTARTED pi-local kid inherits the key (same shape claude_code_adapter:855, copilot_cli_adapter:362); the workflow.py _pi_env and heal.py spawn paths likewise; (R2) no regression test for the two dispatch.py lines — deleting either leaves the suite green; (R3) the real-kid env conjunct was proved on a controlled build of the dispatch functions, not a spawned --harness pi-local child; (W1) kid node probe cmd mis-transcribed (minting-per-spawn hyphens vs the spaced banner). Body CLAIM line re-stated to the allowlist (was the reverted round-1 denylist wording; mur-dfef305bc MISSED-4). ROUND 3 (queued, $0.50): move the pop into child_env for credential-none rows in all three adapters (one mechanism, every spawn path incl. restart/workflow/heal), regression tests for banner gate + env pop + restart env (Popen monkeypatched, no real process), and ONE real --harness pi-local kid spawn with the env-keys log; proved needs that kid in evidence_runs.
