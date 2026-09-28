---
id: hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff
mint_id: cc40ca3188b44faaa2fb6111467f604c
type: hypothesis
parents:
  - goal:g7.33
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
edited_by: director-engine
scaffold_hash: 7730d4593a43017e
season: 2
testable_claim: pi_trajectory.py retries an empty provider response against a CONSECUTIVE bound that resets after progress, waiting min(base x factor^(k-1), cap) before retry k, every number a values.pi_retry cell with today behaviour as the default -- a run with more total empties than the bound, never more in a row, finishes
title: An empty-response retry budget counts consecutive empties and backs off growing to a cap (TMM.360 item 2, EG.186)
town: core
---
# hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff

# hypothesis: an empty-response retry budget counts CONSECUTIVE empties and backs off growing to a cap

## Measured
- pi_trajectory.py main: `for attempt in range(max_retries + 1)` -- the budget is PER RUN: every empty response spends one retry for the whole parent session, however much work succeeded in between; the backoff is one fixed value (_retry_cells -> values.pi_retry.empty_response_backoff_s).
- director-engine, 09-28 21:45-22:30Z, on cuts carrying values.pi_retry 6 x 60 s: EG.184 parent a00-c8f1d0f6 = 56 empties over 925 turns, retries 6/6 used, survived on the last; EG.185 parent a00-69905c26 = 62 empties over 385 turns, 6/6 exhausted at 8 min, 0 commits. The empties are spread (about 1 per 6-16 turns), not one long outage: a per-run count kills a long, productive run for spread noise, and a bigger number only moves the edge (TMM.360).

## CLAIM
The retry bound counts CONSECUTIVE empty responses: it resets to zero once a resumed attempt makes progress (at least one completed turn before it ends), so a run with more total empties than the bound finishes as long as no more than the bound arrive in a row. The wait before retry k grows as base x factor^(k-1), capped at cap. Every number is a values.pi_retry cell; the code is the reader, with today's behaviour as its defaults.

## Dispatch line
config-max: max consecutive (values.pi_retry.empty_response_max_retries), base (empty_response_backoff_s), factor (empty_response_backoff_factor), cap (empty_response_backoff_cap_s) -- the kid PROPOSES the factor and cap values on its node; thought-master writes the cells at landing (a round-done commit never carries .agi/config.json) / template-max: none / code: the consecutive counter and the growth formula in pi_trajectory.py, which do not exist.

## FALSIFIERS
1. A fixture run whose stub pi yields MORE total empties than max_retries, never more than max_retries in a row, with progress between them, ends on its empties (the per-run count survives).
2. A stub that is empty max_retries + 1 times in a row does NOT end the run (the bound is gone, not moved).
3. The sleeps recorded for retries 1..k do not follow min(base x factor^(k-1), cap) for the fixture's cells, or a missing cell does not fall back to today's behaviour (factor 1, cap = base).

## TESTS
extensions/agi/tests/test_pi_trajectory_retry.py (the falsifiers, stub pi + fixture config, _RETRY_SLEEP-style monkeypatched sleep -- never a real wait) + neighbourhood test_pi_trajectory.py test_live_config_cells.py test_bin_help_smoke.py

## FILE SCOPE
extensions/agi/bin/pi_trajectory.py (_retry_cells and main's retry loop only) · extensions/agi/tests/test_pi_trajectory_retry.py · this node (write.py) · the kid's own node

## CEILING
1 kid · <= 25 production lines net · <= 40 test lines net · pi-free tier-0 · 0 USD -- two-operand numstat <cut>..<tip before the paste commit>, labelled so
