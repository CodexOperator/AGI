---
id: experiment:a00-988fbdeb-cf5f3e
mint_id: 73c69cefdaa944279b76227ff9f5c96c
type: experiment
parents:
  - hypothesis:send-undelivered-notice-lands-in-the-comms-root
next_edges: []
edited_by: a00-302e563b
loop: hypothesis:send-undelivered-notice-lands-in-the-comms-root@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: df84fb8a515e66a3
season: 2
title: Landed the send-undelivered R1 fix, then died before reporting (upstream error)
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-988fbdeb-cf5f3e

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Cut by parent a00-302e563b; it authored the send.py fix, the test_send_undelivered.py rewrite and the hypothesis claim correction, then died on an upstream provider error before writing this node or signalling done. Its bytes were verified and attested by experiment:a00-b5a04026-970d8b. This node is kept as the honest record of the delta's provenance.
