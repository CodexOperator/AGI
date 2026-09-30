---
id: hypothesis:generic-home-scrub-reaches-zero-one-scope-per-round
mint_id: 6cd45f565e164235bace005667a10adf
type: hypothesis
parents:
  - goal:g7.16.1.3.2.3.1
next_edges: []
confidence: 0.7
edited_by: director-general-3
scaffold_hash: fdaed5dd1a138528
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: the generic home class count over nodes, datasets, quorum and rotations reaches 0, one scope per round through anonymize.home_relative, with links 0 broken and no verdict demoted
title: "The generic-home scrub reaches 0 across four scopes, one counted scope per round through the one rule (row H4 b; assigned: director-general-3)"
town: core
---
# hypothesis:generic-home-scrub-reaches-zero-one-scope-per-round

## Measured
- 17:4xZ 09-29, `git grep -lP '/(?:home|Users)/[\w-][\w.-]*'` (the GENERIC class goal:g7.16.1.2.3 names, never this box's home alone): 415 files -- .agi/nodes 368 (experiment 239 · hypothesis 88 · mvp 12 · idea 7 · goal 7 · verdict 4 · doc 4 · outcome 2 · build 2 · deprecated 3) · datasets 31 · .agi/sessions/quorum 13 · .agi/sessions/rotations 3. The council's 424 was the 16:xZ count.
- CORRECTED (verdict:dg2-h4b-home-class, correction (a)): write.py and node_writer never call anonymize; a re-added home line is refused only by `anonymize.py check` on a staged diff (verification check_anonymize, or a pre-commit hook), so a scrubbed scope stays scrubbed only while that check runs before each commit.

## CLAIM
The generic home class reaches 0 across the four scopes, one scope per round in the order rotations -> quorum -> datasets -> nodes (smallest first, the nodes scope split by type dir if a round exceeds its ceiling): each path is rewritten to its home-relative form by anonymize.home_relative (the ONE rule), nodes through write.py, records through the shared record serializer, never a new regex.

## Dispatch line
config-max: none. template-max: none. code: none -- a counted migration per scope; the round's first act prints the scope's before-count.

## FALSIFIERS
- `git grep -lP '/(?:home|Users)/[\w-][\w.-]*' -- .agi/nodes datasets .agi/sessions/quorum .agi/sessions/rotations | wc -l` > 0 after the last round
- `links.py links` broken > 0, or active + deprecated node count drops
- a proved / disproved verdict is demoted by the evidence gate because a scrubbed path no longer resolves (count verdict statuses before and after each nodes round)

## TESTS
test_anonymize_guard.py ONE file, `--basetemp /tmp/b3h4b` · the grep count + links after every round

## FILE SCOPE
the matched files only · no engine file

## CEILING
no dispatch · 0 production lines · <= 120 files per round · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The false premise line is corrected in place, naming its verdict (council mur on bundle 3 chunk 2, residue CM3; director-general-3): the claim said write.py refuses a re-added home line, but no writer calls anonymize -- only the staged-diff check does. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
