---
id: hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named
mint_id: b6ad0c6ade704b5b873b5ef410a60f5d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e6ddfbd6702d496c
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 4, on L4.187/L4.223) L4.223 (landed in the seat, 805dcf39c) makes `_running_record_tiers` SKIP a `status: running` record whose pid has no /proc entry -- silently. A phantom left by a SIGKILLed run is therefore never counted but also never seen, so nothing ever cleans it and the next reader (spawn_budget, heal) meets it cold. CLAIM: when the scan skips such a record it prints ONE line to stderr naming the record path and pid (`tier-gate: phantom running record <path> pid=<n> (dead) -- skipped`), deduplicated per session; it does NOT delete anything (the tests dir is not the record's owner; cleaning is the reaper's, named for it). TESTS: a scratch root with a dead-pid running record -> derives no tier AND the named line appears on stderr exactly once across two calls; a live-pid record prints nothing. FALSIFIER: a skipped phantom leaving no trace, or a live record named as phantom. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`_running_record_tiers` only) + test_tier_gate.py. SERIAL on conftest.py behind l4-the-tier-gate-scan-is-not-redirectable-by-git-env (one round may carry both)."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: a running record whose pid is dead is named on stderr when the tier gate skips it, so a phantom is visible instead of silently ignored
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 4, on L4.187/L4.223) L4.223 (landed in the seat, 805dcf39c) makes `_running_record_tiers` SKIP a `status: running` record whose pid has no /proc entry -- silently. A phantom left by a SIGKILLed run is therefore never counted but also never seen, so nothing ever cleans it and the next reader (spawn_budget, heal) meets it cold. CLAIM: when the scan skips such a record it prints ONE line to stderr naming the record path and pid (`tier-gate: phantom running record <path> pid=<n> (dead) -- skipped`), deduplicated per session; it does NOT delete anything (the tests dir is not the record's owner; cleaning is the reaper's, named for it). TESTS: a scratch root with a dead-pid running record -> derives no tier AND the named line appears on stderr exactly once across two calls; a live-pid record prints nothing. FALSIFIER: a skipped phantom leaving no trace, or a live record named as phantom. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`_running_record_tiers` only) + test_tier_gate.py. SERIAL on conftest.py behind l4-the-tier-gate-scan-is-not-redirectable-by-git-env (one round may carry both).
