---
id: hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb
mint_id: e254388b44854fd2b475388d1b6c9249
type: hypothesis
parents:
  - goal:g1.25.2
next_edges: []
ceiling: 1.5 USD, <= 2 kids, pi parents
confidence: 0.75
edited_by: director-engine
scaffold_hash: db0577f192f1e56c
season: 2
testable_claim: "After the fix, every proposable entry in command:commands can place each OPTIONAL arg it declares -- as its CLI flag (e.g. `--back <back>`) or boolean switch, derived from the CLI's own argparse so drift fails a test -- so propose with any subset of declared args returns a complete argv; verbs that write the real crontab or systemd units, and owner-ops verbs like mesh-gw, are proposable: false with the reason recorded; no manifest purpose names a box detail (the anonymize guard runs over the whole manifest, purposes included); the duplicate test is removed and crons.py:show is labelled read; each proved by a committed test red on the pre-fix bytes, with test_commands*.py and test_graphweb.py green."
title: "the choice surface takes optional args and offers no operator verb (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb

# hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb

## Hypothesis

```
verified  director-engine 14:2xZ 09-23: commands.propose refuses 'grid.py:diff' with {back: 1} -- "cannot place arg 'back'; argv has no
          <back>" -- and 64 of 109 proposable entries refuse when every declared arg is filled (only optional ones fail to place)
```

## Agent Notes
assigned: director-engine (leaf goal:g1.25.2 of the jev choice surface); verified before minting.
