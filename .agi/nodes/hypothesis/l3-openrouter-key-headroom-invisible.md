---
id: hypothesis:l3-openrouter-key-headroom-invisible
mint_id: 9ae73f39ae924412a961545cfbe93b5e
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: c1164fe30bb8d852
season: 2
testable_claim: provisioning.py status prints the .env key's own limit, usage and remaining from GET /api/v1/key, and dispatch.py refuses to spawn with a named error when remaining is below a configured floor, proved by a test that fakes a near-exhausted key and asserts the refusal plus one live status run showing the real numbers.
thought_session: 7af11157
title: Surface the OpenRouter sub-key headroom before it kills a round
---
<!-- BODY:BEGIN -->
# hypothesis:l3-openrouter-key-headroom-invisible

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM: the one number that can kill every pi agent in the graph is invisible to the loop's own telemetry, and it should be a one-line refusal instead of a silent 60-minute death.

WHY: measured in L3.29 on 2026-09-07. The OpenRouter key in .env is a provisioning SUB-KEY carrying its own dollar cap. It stood at limit 10, usage 9.7236, and OpenRouter reports crossing that cap as "401 API key expired" - wording that points at an expiry and sends a reader looking at the wrong thing. It killed the p-quorum parent AND its kid, the kid 60 minutes in with its whole brief implemented and not one line of its node written. Meanwhile curl /api/v1/credits read the ACCOUNT at 30.07 dollars and looked perfectly healthy, and provisioning.py status printed "available keys_visible=1 engine_minted=0" and said nothing about dollars at all.

FILES:
extensions/agi/bin/provisioning.py :: status - add the key read and the printed row
extensions/agi/bin/dispatch.py :: the pre-flight before a spawn takes a budget slot
extensions/agi/tests/test_provisioning.py :: fake a near-exhausted key
.agi/config.json :: the floor, defaulted, overridable per project

DESIGN: status calls GET https://openrouter.ai/api/v1/key with OPENROUTER_API_KEY and prints limit, usage and remaining beside what it prints today; a key with no limit prints unlimited rather than failing. dispatch.py checks remaining against a floor (suggest 1.00 USD, config key provisioning.min_key_remaining_usd) and refuses with a message naming the key label, the remaining amount and the PATCH command that raises it. The check is fail-open on a network error - an unreachable API must never block a round - and is skipped for a non-openrouter harness.

TESTS red-first: test_status_prints_key_limit_usage_remaining, test_status_says_unlimited_when_no_limit, test_dispatch_refuses_below_floor_naming_the_key, test_dispatch_spawns_when_remaining_above_floor, test_check_fails_open_on_network_error.

GATE: a parent must see the five tests green AND one live provisioning.py status run printing the real numbers for the key in .env.

NOT IN SCOPE: per-spawn key minting is goal:g1.11's older slice and stays as it is; the failure ledger's died category (l3w4-agent-failure-ledger) should gain a session-limit-style row for this class but that belongs to its own brief.

SOURCE: HANDOFF section 6 items 33 and 34 and trap 0o, all from the L3.29 measurement. The 10-to-40 raise was a prime judgement call, not an owner decision - this brief is what makes the next one unnecessary.
