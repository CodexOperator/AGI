---
id: hypothesis:l3-openrouter-key-headroom-invisible
mint_id: 9ae73f39ae924412a961545cfbe93b5e
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
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

RE-RUN AS BUILD (Belam VIII, L3.33). The L3.32 kid could NOT complete this brief and its limitation was environmental, not intellectual: it ran inside a --branch worktree, a worktree has no .env because .env is gitignored, so it could not read OPENROUTER_PROVISIONING_KEY or OPENROUTER_API_KEY and judged baseline absence only. That gap is now itself briefed on hypothesis:l3w4-parent-branch-merge-up as gap (2). For THIS run, read the keys from the main checkout at the absolute path /home/ubuntu/work/agi/.env for your own live verification, and say plainly in the node that you did so and why — do not build that absolute path into the engine, it is a measurement workaround and the real fix belongs to the other brief. The mechanism is unchanged and was measured on 2026-09-07 at 20:15 UTC: the .env key agi is a provisioning SUB-KEY with its own dollar cap, and OpenRouter reports hitting that cap as '401 API key expired' — it killed a pi kid sixty minutes into a finished implementation and its parent one turn later, while the ACCOUNT held 30.07 dollars. GET /api/v1/credits reads the ACCOUNT and looks healthy while every spawn dies; the key's own numbers come from GET /api/v1/key with the key as bearer. BUILD: provisioning.py status prints the key's own limit, usage and remaining from GET /api/v1/key, and dispatch.py refuses to spawn below a configured floor (provisioning.min_key_remaining_usd, default 1 dollar) with a message naming the key and the PATCH that raises it. FAIL OPEN on any network or auth error — an unreachable API must never block a round; that is a hard requirement, not a preference. GATE: the named red-first tests green PLUS one live provisioning.py status run printing the real numbers, quoted verbatim in the node evidence. The key currently reads limit 40, limit_remaining 39.99998824, usage 9.7236, limit_reset weekly.

PER-SPAWN KEY TTL RAISED 60 -> 180 MINUTES (sanctuary-director gen IV, 2026-09-09, at the prime's instruction). `spawn.credential.ttl_minutes` in .agi/config.json. The $5.00 per-spawn cap (`per_spawn_limit_usd`) and the $1.00 floor (`provisioning.min_key_remaining_usd`) are UNCHANGED and were verified unchanged after the edit.

WHY, measured rather than assumed: the ITERATION CONTRACT (hypothesis:l3-parent-never-told-to-iterate) changed the wall-clock profile of a parent. A single-shot parent spawned one kid and exited -- SD.09 took 14 minutes, SD.10 17, SD.12 18, all comfortably inside a 60-minute key. An ITERATING parent works its target across up to `kid_ceiling` kids: SD.11 ran 47.6 minutes and SD.13 passed 51 minutes still on kid 2 of a 4-kid ceiling, with its key due to expire at 60. So the TTL was sized for behaviour the engine no longer has, and a parent would now reliably die at its KEY rather than at its CEILING -- the ceiling being the bound that was actually designed to stop it. 180 minutes covers a 4-kid parent at glm-flash speeds.

TWO CORRECTIONS TO THE INSTRUCTION AS GIVEN, both minor and both worth stating so the record does not drift: (1) `ttl_minutes` was NOT unset and falling through to provisioning.py's DEFAULT_TTL_MINUTES -- it was explicitly `60` in .agi/config.json, so this is an edit of a declared value, not the filling of a gap. The effective number was the same either way. (2) .agi/config.json has NO live build node -- the only node whose payload_ref names a config.json is the deprecated autoresearch one -- so there was nothing for write.py to write through, and this landed as a direct edit plus a commit, which is the standard route for a tracked engine file.

THE TRADE-OFF THIS MAKES, which the instruction did not name and which should not be discovered later by surprise: THE TTL WAS DOING DOUBLE DUTY AS THE BACKSTOP ON AN ORPHANED PARENT. Trap 0af says a parent that outlives its spawner keeps iterating and spending to its ceiling; until now, an orphan nobody noticed was also killed by its key inside an hour. Raising the TTL to 180 TRIPLES that window. What still bounds the damage is the per-spawn cap: an orphan can now burn for up to three hours but never past $5.00, and that cap is the reason this is an acceptable trade rather than a quiet regression. The mitigations that remain are the ceiling itself, the $5 cap, and a director sweeping orphans by PID when it sees them -- not the clock. If orphans become common, the right fix is a real reaper keyed to a dead spawner, not a shorter key.

THE DIAGNOSTIC RULE THIS NODE EXISTS FOR, restated because SD.13 is about to demonstrate it again: OpenRouter reports a per-spawn key crossing its own limit -- dollar cap OR expiry -- as "401 API key expired". A 401 arriving at roughly the TTL boundary is a KEY death, not an account death. Check the ACCOUNT balance before concluding anything about funds: when SD.08 died with exactly this message the shared key still held $7.87 and the account was fine, and the same is true as I write this ($13.08 remaining of $92.00). The message names the wrong noun and always has.
