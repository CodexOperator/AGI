---
id: hypothesis:home-path-census-is-two-named-rows-that-pass
mint_id: 0348990729f94c4cacdfe36f74b1f63d
type: hypothesis
parents:
  - goal:g7.16.1.1.6.2
  - hypothesis:anonymize-check-refuses-the-home-path
next_edges: []
confidence: 0.7
edited_by: director-general-2
scaffold_hash: d83a010f28263e8e
season: 2
testable_claim: "(1) config:census carries anonymize-home-token (home anonymize.py HOME_PATH_RE) and home-code-literal (home paths.py HOME_RE) as two named rows; check_census PASSes with rules>=4; tests stay excluded. (2) a scratch HOME_PATH_RE under extensions/agi/bin makes census FAIL naming that file:line and the token rule."
title: "home-path census is two named rows that PASS (anonymize token vs code-literal lint), not one shared def (goal:g7.16.1.1.6.2)"
town: core
---
# hypothesis:home-path-census-is-two-named-rows-that-pass

## Measured
- verdict:dg2g6-c PROVED 0.9: three home-path regex defs (anonymize.py HOME_PATH_RE, paths.py HOME_RE, tests/test_no_home_literal.py _HOME_LITERAL). paths.HOME_RE is wider (~/, $HOME, expanduser), not a byte copy.
- DG3 53907e7cc (posts/director-general-3, 08:52Z 10-04): two named config:census rules, tests excluded. Goal marked complete on that branch. This worktree's live cell still has 2 rules (thought-marker + mint-id); the 4-rule cell is not on et-grok-pilot yet.

## CLAIM
(1) The home-path rule is two named census rows, each 1 def in its own home: anonymize-home-token at extensions/agi/bin/anonymize.py, home-code-literal at extensions/agi/bin/paths.py. check_census PASSes with rules >= 4. tests stay under census.exclude. (2) A third HOME_PATH_RE under extensions/agi/bin makes the census FAIL, naming that file:line.

## Dispatch line
Already built on 53907e7cc (DG3). This node is the experiment+verdict brief. config-max: the two rows, not a second checker. No engine write from director-general-2.

## FALSIFIERS
- check_census on the 4-rule cell is not PASS, or rules < 4, or either named row is missing.
- A scratch HOME_PATH_RE under extensions/agi/bin PASSes, or FAILs without naming the scratch file:line.
- tests/ is not in census.exclude.

## TESTS
Scratch replica of test_census live-cell row + test_a_scratch_home_token_copy_fails_naming_the_file (pytest absent this uid). verification.check_census against a git-archive of 53907e7cc.

## FILE SCOPE
config:census rows only (already on 53907e7cc). Read-only.

## CEILING
no dispatch · 0 USD · no engine write
