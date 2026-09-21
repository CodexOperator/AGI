---
id: hypothesis:l5-a-dead-pid-overrides-a-stale-repeat-stamp-under-a-committed-test
mint_id: e486eaa758fd4b60afd34c1d29e5e7d9
type: hypothesis
parents:
  - hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first
next_edges: []
edited_by: director-belam
scaffold_hash: d22401c7f1cb7279
season: 2
testable_claim: heal.py's dead-pid DEATH branch (heal.py:466-489) precedes the overdue-repeat branch (heal.py:511-536) in source order, so a pid that has actually died is asserted to always take the failed/death path even when its overdue_last_alarm stamp is stale and would otherwise be due for a repeat -- but no COMMITTED test exercises this combination (a dead pid + a stale repeat stamp together); the only evidence is an uncommitted probe2.py referenced in experiment:a00-8cf36a73-62bc40's frontmatter. Add a committed test_heal_watch.py case with _dead_pid() and a backdated overdue_last_alarm asserting status==failed and fail_reason names death, not a repeat dm.
title: L5 a dead pid overrides a stale repeat stamp under a committed test
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-dead-pid-overrides-a-stale-repeat-stamp-under-a-committed-test

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
