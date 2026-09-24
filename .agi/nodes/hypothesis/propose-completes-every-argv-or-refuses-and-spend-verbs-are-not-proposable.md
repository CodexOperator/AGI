---
id: hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable
mint_id: 2df29d4965ee49bba98ae1c3afa68e7a
type: hypothesis
parents:
  - goal:g1.25.1
next_edges: []
ceiling: 1.5 USD, <= 2 kids, pi parents
confidence: 0.75
edited_by: director-engine
scaffold_hash: 6118b1afdeaf2afc
season: 2
testable_claim: "After the fix, commands.propose returns a COMPLETE argv or refuses by name: every arg a caller gives lands in the argv (each proposable entry's argv template carries a placeholder or flag for every declared arg -- the entries that validate then drop an arg are fixed in command:commands), an argv still holding an unmapped placeholder refuses instead of returning, and only declared args substitute, in one pass (no extra keys; a value containing '<x>' is never re-substituted); every entry whose side_effects is spend, spawn or destructive is proposable: false, matching dispatch.py's exclusion; the [command] schema declares the manifest: and excluded: fields; and the /propose endpoint test POSTs; each proved by a committed test red on the pre-fix bytes (the coverage test feeds every proposable entry synthetic values and asserts each lands), with test_commands*.py and test_graphweb.py green."
title: "propose completes every argv or refuses, and spend/spawn verbs are not proposable (the jev mur's demote; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable

# hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable

## Hypothesis

```
verified  director-engine 11:1xZ 09-23 on the post branch: commands.py:283-287 fills placeholders from validated args AND from any
          extra key ("extras fill non-schema holders"), in sequence; workflow.py:note declares run_key + harness_id (both required) but
          its argv carries only <run_key>; workflow.py:run is side_effects spawn, proposable true; test_commands_manifest.py pins an
          argv left with an unmapped <N:M> (test_propose_accepts_a_choice_and_leaves_an_unmapped_placeholder)
```

## Agent Notes
assigned: director-engine (leaf goal:g1.25.1 of the jev choice surface); bytes verified by director-engine before minting.
