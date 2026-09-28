---
id: goal:g4.18.1.1
mint_id: c8fee9866a2b4beeb029518717f6c5ce
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G4.18.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e9cbfa3ece525da7
season: 2
seeds: []
status: active
tags:
  - engine
  - write
title: "G4.18.1.1: one row validator + an answers file -- a mint is rows checked against the type schema, stamped from the calling post, no shell-quoted values"
town: core
---
# goal:g4.18.1.1

# goal:g4.18.1.1

## OWNER 2026-09-26 ~23:2xZ, verbatim (the fragment this leaf carries; the whole quote is on goal:g4.18.1)
"Each row filled out and format checked." / "The mint uses the calling posts info to stamp info appropriately."

## Why this exists
goal:g4.18.1 -- the one mint route needs ONE validator both of its front doors call; today a mint is a single `write.py create` argv whose `--set` k=v pairs are checked only by the spawn gate at the end, so a wrong row is found after the whole command is typed, and a quote or backtick in any value breaks the shell line (the predecessor dropped an owner quote's apostrophes to get it through).

## Target end-state
- A mint can be described as an ANSWERS FILE (one row per field: frontmatter fields, parents, body, payload) and minted with one `write.py` call that reads it; no value ever passes through a shell-quoted argv.
- Every row is validated against `.agi/context/schemas/[<type>].md` (required, regex, types, legal parents) by ONE function, row by row, and a refusal names the row and the rule.
- Rows the calling post does not choose (actor, role, town, season, thought_session) are stamped from the caller's `config:posts` row, never typed.

## Invariants
- The same validator backs the answers file AND the captive flow (goal:g4.18.1.2); no second copy of a schema rule in code.
- A refused mint writes nothing (the spawn gate's contract holds).

## Falsifier
1. An answers file carrying an owner quote with an apostrophe, a backtick and `$(` mints byte-identically (`write.py ... read body` round-trip), exit 0.
2. Negative: an answers file with one bad row exits non-zero naming that row, and `git status` shows no new node.

## Out of scope
goal:g4.18.1.2 (captive flow) · goal:g4.18.1.3 (storage picker) · goal:g4.18.1.4 (location row) · goal:g4.18.1.5 (new version) · goal:g4.18.2 (skills)

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted by director-engine as one of five nested leaves of goal:g4.18.1 (standing: nest an ASSIGNED goal into sketched leaves before any parent is spawned). The split follows the owner quote on goal:g4.18.1 and the refinements (a) (b) (c) read there; refinement (d) per-function skills is goal:g4.18.2 and is not repeated; (e) role-template text goes up through the master as template lines. confidence/origin/seeds/tags were set after the create because the agi-goal skill mint command omits them while [goal].md requires them.
<!-- THOUGHT:END -->
