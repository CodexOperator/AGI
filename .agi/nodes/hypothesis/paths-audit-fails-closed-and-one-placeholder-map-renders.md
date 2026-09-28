---
id: hypothesis:paths-audit-fails-closed-and-one-placeholder-map-renders
mint_id: af76bc51faca47319056684ae50eb724
type: hypothesis
parents:
  - goal:g15.29.4
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: c027a2d889050c71
season: 2
testable_claim: After the fix, the paths audit refuses (non-zero, naming the missing schema) when .agi/context/schemas/[box].md is absent or declares no box cells instead of passing with an empty cell set, and a committed test covers that absent-schema layout again; boxes.resolve_placeholders refuses a schema that declares no `placeholders:` map instead of substituting nothing; and crons.py's placeholder rendering (crons.py ~478, its own four-token list) goes through boxes.resolve_placeholders so ONE schema-declared map renders every placeholder, with the crontab rendered for the live crons node byte-identical before and after; each proved by a committed test red on the pre-fix bytes, test_paths_audit.py and test_crons.py green.
title: "The paths audit fails closed and one placeholder map renders (assigned: director-engine)"
town: core
---
# hypothesis:paths-audit-fails-closed-and-one-placeholder-map-renders

# hypothesis:paths-audit-fails-closed-and-one-placeholder-map-renders

## Hypothesis

After the fix, the paths audit refuses (non-zero, naming the missing schema) when .agi/context/schemas/[box].md is absent or declares no box cells instead of passing with an empty cell set, and a committed test covers that absent-schema layout again; boxes.resolve_placeholders refuses a schema that declares no `placeholders:` map instead of substituting nothing; and crons.py's placeholder rendering (crons.py ~478, its own four-token list) goes through boxes.resolve_placeholders so ONE schema-declared map renders every placeholder, with the crontab rendered for the live crons node byte-identical before and after; each proved by a committed test red on the pre-fix bytes, test_paths_audit.py and test_crons.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.4; source R-EF27 D1 D2 + M1 (resolve_placeholders has no production caller) M3 (placeholders fail open)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
