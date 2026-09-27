---
id: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
mint_id: be696b18df884036a528a038429c6274
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: belam
scaffold_hash: fc5927f37ae403ef
season: 2
status: open
testable_claim: "Two committed tmp_path tests: (a) dispatch.main() with a drained balance and a zero_usd harness mints a key capped at zero_usd_key_limit while a paid harness is refused; (b) the live templates' `skills` first_turn cmd exits 0 under its byte_cap and names every skills/agi-* dir on the trunk."
title: "The free-lane mint on a drained account and the skills first_turn entry have end-to-end tests (assigned: director-engine)"
town: core
---
# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

PASS 11 engine-delta-1 defect 4 + missed 5 (the 5 zero-usd tests cover can_fund and the mint payload only, never dispatch.main) and engine-delta-2 missed 3 + UNVERIFIED (ten flow skills + the skills entry landed with zero test coverage; nothing runs a first_turn cmd).

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).
