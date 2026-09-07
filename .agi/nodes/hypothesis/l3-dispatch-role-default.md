---
id: hypothesis:l3-dispatch-role-default
mint_id: a4331b8755d241d99bdc0330a269bad2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 39e1c41a18aa4ba6
season: 1
testable_claim: dispatch.py resolves a spawn's ladder row from --tier when --role is not given (tier parent means role parent, tier kid means role kid), so a director's spawn primitive never loads the tier-0 kid model for a parent, and a red-first test pins each tier-to-row mapping
title: L3 dispatch role default follows tier
---
# hypothesis:l3-dispatch-role-default

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FOUND L3.08 by kid a00-a18f229f (tier-0 director brief): dispatch.py --role defaults to kid, so a bare --tier parent spawn resolved to the tier-0 kid row (deepseek) through resolve_role_spec; the director brief's spawn primitive was loading the wrong model and no test caught it. The kid worked around it in the brief template only; dispatch.py itself was not changed in L3.08. FILES: extensions/agi/bin/dispatch.py (resolve_role_spec: default role derived from --tier; explicit --role still wins), extensions/agi/tests/test_dispatch.py. VERIFY: red-first test for tier parent without --role resolving to the parent row with ~z-ai/glm-flash-latest and tier kid to the deepseek row; dispatch.py --list-rows unchanged; a dry dispatch of --tier parent prints the GLM command. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.
