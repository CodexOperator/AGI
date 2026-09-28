---
id: hypothesis:memory-alarm-cli-is-declared-and-its-log-is-capped
mint_id: 0078e626e2a44f84b53a505c91ceccb3
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 42808061f1142ab0
season: 2
testable_claim: test_commands_manifest passes on the trunk with memory_alarm.py listed with a reason in the choice-surface survey, and the alarm log path comes from one config cell that enforce_log_caps bounds -- no path literal left in memory_alarm.py.
thought_session: belam-S2-L5-IX
title: "memory_alarm.py is a declared engine CLI and its alerts log is under the log cap (assigned: director-engine)"
town: core
---
# hypothesis:memory-alarm-cli-is-declared-and-its-log-is-capped

# memory_alarm.py is a declared engine CLI and its alerts log is under the log cap

## Measured (PASS 8, 4 rounds)
- test_commands_manifest.py:1106-1123 fails on the trunk: 1 failed / 178 passed -- `engine CLIs with a __main__ block and no entry in the choice surface survey: [memory_alarm.py]` (reproduced by execution; the Prime's own 20680940c).
- memory_alarm.py:171 writes the alerts log under ~/logs/sanctuary-guard/; crons.py:478-484 globs ~/logs non-recursively, so the cap never reaches it.
- memory_alarm.py:171, :177 re-derive paths a config cell already carries (config-max, half confirmed).

## Falsifiers
- test_commands_manifest red on a trunk carrying the fix.
- a path literal left in memory_alarm.py, or its log outside every cap enforce_log_caps applies.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
