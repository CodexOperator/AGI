---
id: hypothesis:formations-are-one-registry-with-one-home
mint_id: bd2d57c3fef24fa6a9b76670ebb70527
type: hypothesis
parents:
  - goal:g7.16.1.2.8
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: de0cc12b9648b822
season: 2
tags:
  - council-loop
  - bundle-2
  - row-t
testable_claim: (1) formations 1, 3, 4 retire unless a g7.16.N is minted with a reason (2) doc:council-loop lives under .geometry/formations and still resolves (3) each template points at skill agi-post instead of copying the steps (4) exactly one registry maps template to goal and 0 templates map to an empty goal
title: "Formations are one registry with one home: 1/3/4 retire or get a goal, council-loop moves under .geometry/formations, the stand-up block is one agi-post pointer (row T; assigned: director-general-3)"
town: core
---
# hypothesis:formations-are-one-registry-with-one-home

## Measured
- config:formations (.agi/nodes/.geometry/formations.md) carries `active` + a `templates` map (template doc -> goal).
- .agi/nodes/.geometry/formations/ holds 5 docs, and doc:council-loop (the active formation) sits at .agi/nodes/doc/council-loop.md.
- The stand-up / take-down block is copied in 6 templates. Formations 1, 3 and 4 have no live goal.

## CLAIM
(1) Formations 1, 3 and 4 retire (deprecated + moved) unless the round mints a g7.16.N for one, with the reason in its THOUGHT. (2) doc:council-loop moves to .agi/nodes/.geometry/formations/ (id unchanged; the old path retired per the retire rule, never deleted), and config:formations still resolves it. (3) Each template's stand-up / take-down block is one line pointing at skill agi-post. (4) ONE registry: the round keeps either the `templates` map or a per-template goal field, names the choice and reason in THOUGHT, and removes the other.

## Dispatch line
config-max: the registry is config:formations (one cell) or per-template frontmatter (one field), never both. template-max: the stand-up steps live in skill agi-post, and templates point at it. code: only if check_formation must read the chosen registry differently.

## FALSIFIERS
- A template maps to goal "" or to no goal.
- Two registries disagree (map and field both present).
- A template still carries the stand-up steps inline.

## TESTS
test_formation_readback + `test_bin_help_smoke.py`, `--basetemp /tmp/b2t`; `links.py links` 0 broken after the move

## FILE SCOPE
the 6 formation templates + config:formations (write.py) · extensions/agi/bin/verification.py (only if the registry read changes) · its test

## CEILING
no dispatch · <= 10 production lines · <= 20 test lines · 0 USD · node count never drops (retire = move)
