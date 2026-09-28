---
id: hypothesis:the-last-engine-clis-join-the-choice-surface
mint_id: 9f791610d2e64b278c149e3ec4f74e67
type: hypothesis
parents:
  - goal:g1.25.4
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 23409932549abea9
season: 2
testable_claim: "After the round, command:commands covers all 70 engine CLIs: each of the last 35 has every verb declared (typed args, placement data, side_effects, proposable) or excluded by name with a reason (library debug entries, destructive / live-seat / owner-ops verbs); the coverage and drift tests include them and stay green; propose still imports and executes nothing; the manifest stays deterministic with no absolute path or box value."
title: "the last engine CLIs join the choice surface: all 70 covered (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-last-engine-clis-join-the-choice-surface

# hypothesis:the-last-engine-clis-join-the-choice-surface

## Hypothesis

```
set        backfill-mint-ids.py boxes.py branches.py briefing.py completion.py dashboard.py decompose-engine.py derive-commands.py drift_check.py failures.py frontier.py geometry_config.py glitch_master.py graphweb.py grid_coverage_check.py inject.py lm_bench.py mail_alert.py mem_cap.py migrate_channel.py payload_boundary.py pi_edit_forgiveness.py pi_trajectory.py plan_master.py reconciler.py rolslice.py seat_status.py spawn_gate.py stall_detect.py success_metrics.py telemetry_rollup.py towns.py verify_unified.py ws_raw.py ws_raw_client.py
proves     the coverage test lists all 70 engine CLIs and stays green: every verb declared or excluded by name with a reason; the drift test
           covers the new entries; propose imports / executes nothing; the manifest stays deterministic with no absolute path or box value
```

## Agent Notes
assigned: director-engine (goal:g1.25, the owner's cli-maxxing; survey batch 3 of 3); measured before minting.
