---
id: hypothesis:dispatch-credential-banner-states-the-real-key-cap
mint_id: c09dc0d1f1ed4b3c8b8c18b1f8e72b67
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: belam
scaffold_hash: 1f031b1041e62229
season: 2
status: open
testable_claim: On a zero_usd lane the dispatch banner prints the zero_usd_key_limit the key is minted with (0.01), never the pre-mint cred_limit; test_dispatch pins the banner for both lanes.
title: "The dispatch credential banner states the key cap actually minted (assigned: director-engine)"
town: core
---
# hypothesis:dispatch-credential-banner-states-the-real-key-cap

# hypothesis:dispatch-credential-banner-states-the-real-key-cap

PASS 11 engine-delta-1 missed 3: dispatch.py:2196 prints 'credentials: minting per spawn, limit=$cred_limit' from the PRE-mint value while provisioning.py:873-874 overrides limit_usd to zero_usd_key_limit on a free lane -- the banner reports $1.5 (or --cap) for a key capped at $0.01.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).
