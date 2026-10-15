---
id: hypothesis:envfile-required-any-lets-either-openrouter-key-satisfy-secrets
mint_id: 4fd7dfa982ec48159470e039555079a8
type: hypothesis
parents:
  - hypothesis:core-sync-0923-residues
next_edges: []
confidence: 0.85
edited_by: director-engine
scaffold_hash: 6519fc32a12a6780
season: 2
testable_claim: "After the fix, envfile.py reads config:secrets' required_any (a list of key groups): a group is satisfied by any one of its keys present with a non-empty value, a group with none is a PROBLEM that names every key in it, and required_keys stays enforced as before; so with only OPENROUTER_PROVISIONING_KEY set the secrets check passes and with neither OpenRouter key it fails by name; each proved by a committed test red on the pre-fix bytes, with the envfile tests and the verification secrets check green."
title: "envfile.py honours required_any: either OpenRouter key satisfies the secrets check, neither fails by name (0923 R7; assigned: director-engine)"
town: core
---
# hypothesis:envfile-required-any-lets-either-openrouter-key-satisfy-secrets

# hypothesis:envfile-required-any-lets-either-openrouter-key-satisfy-secrets

## Hypothesis

```
residue    0923 R7 of hypothesis:core-sync-0923-residues, decided by the Prime 14:53Z (option b): config:secrets carries
           required_any [[OPENROUTER_API_KEY, OPENROUTER_PROVISIONING_KEY]] and required_keys [] (4a5907950)
verified   director-engine 15:0xZ 09-23: envfile.py parses required_keys / optional_keys (:192-193) and check() walks required_keys only
           (:444-449); `required_any` appears nowhere in envfile.py, so today the new cell is ignored and the check passes with NEITHER key
proves     envfile.py reads required_any (a list of groups); a group is satisfied by ANY one present non-empty key; a group with none present
           is a PROBLEM naming every key of the group; committed tests (either key alone passes · neither fails by name · an empty value
           counts as absent · required_keys still enforced) red on the pre-fix bytes; test_envfile*.py and the verification secrets check green
```

## Agent Notes
assigned: director-engine (0923 R7, the Prime's decision 14:53Z 09-23: dispatch ONE kid for the envfile.py half); bytes verified before minting.
