---
id: hypothesis:every-secrets-reader-honours-required-any
mint_id: 1ae38986a29b448d9fe7847ff63c9f98
type: hypothesis
parents:
  - goal:g15.29.3
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 0234d96f88baf734
season: 2
testable_claim: After the fix, anonymize.py _secret_tokens (anonymize.py:28) collects the env values of every key a secrets node names under required_any as well as required/optional/forbidden keys, so a key declared only under required_any is in the physical-token denylist; envfile.py refuses a malformed required_any entry by name instead of dropping it (envfile.py:199 isinstance filter); the [config] schema declares required_any beside its three sibling env fields; and the test named for the required_any interaction (test_envfile.py ~775) declares a group; each proved by a committed test red on the pre-fix bytes, the anonymize test driving the real _secret_tokens against a fixture secrets node and fixture values only, test_envfile.py and test_anonymize_guard.py green.
title: "Every secrets reader honours required_any (assigned: director-engine)"
town: core
---
# hypothesis:every-secrets-reader-honours-required-any

# hypothesis:every-secrets-reader-honours-required-any

## Hypothesis

After the fix, anonymize.py _secret_tokens (anonymize.py:28) collects the env values of every key a secrets node names under required_any as well as required/optional/forbidden keys, so a key declared only under required_any is in the physical-token denylist; envfile.py refuses a malformed required_any entry by name instead of dropping it (envfile.py:199 isinstance filter); the [config] schema declares required_any beside its three sibling env fields; and the test named for the required_any interaction (test_envfile.py ~775) declares a group; each proved by a committed test red on the pre-fix bytes, the anonymize test driving the real _secret_tokens against a fixture secrets node and fixture values only, test_envfile.py and test_anonymize_guard.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.3; source R-EF43 D1 D2 D3 + M1 (anonymize._secret_tokens never reads required_any: the live OPENROUTER_API_KEY value is outside the SM.122 guard)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
