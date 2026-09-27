---
id: goal:g4.18.1.3
mint_id: 335ba13f866a4680a693574428c44d63
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G4.18.1.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 0412f7c6a138f527
season: 2
seeds: []
status: active
tags:
  - engine
  - write
title: "G4.18.1.3: the storage picker -- location options derived from config paths cells and schemas, pick + append or custom"
town: core
---
# goal:g4.18.1.3

# goal:g4.18.1.3

## OWNER 2026-09-26 ~23:2xZ, verbatim (fragment; whole quote on goal:g4.18.1)
"Only needs a template showing where each major storage category is at and have the model pick from options listed during flow for things like extension code, template storage in .geometry, etc. and can add a custom path on top. The template pick in the flow just populates it into the pane verbatim and you can then emit the rest of the pathname before sending submit or just submit."

## Why this exists
goal:g4.18.1 -- a mint that carries a raw file needs a location, and today a post types that path by hand; the predecessor's reading (b) says the options come from the config paths and the schemas, never a hand list.

## Target end-state
- The mint flow offers the storage categories (engine code, tests, skills, .geometry config, context templates, ...) as a numbered list DERIVED from `.agi/config.json` `paths.*` cells and the schemas; picking one fills the location row's prefix, and the post may append the rest of the path or submit as is.
- A custom path outside every category is accepted, flagged as custom.

## Invariants
- No storage path literal in code: a new category is a config cell, and it appears in the picker with no code change.

## Falsifier
1. Adding one `paths.<town>.<key>` cell in a temp config makes a new option appear in the picker, with no code edit, exit 0.
2. Negative: `grep` for a storage-path literal in the picker code = 0 hits.

## Out of scope
goal:g4.18.1.1 · goal:g4.18.1.2 · goal:g4.18.1.4 · goal:g4.18.1.5

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted by director-engine as one of five nested leaves of goal:g4.18.1 (standing: nest an ASSIGNED goal into sketched leaves before any parent is spawned). The split follows the owner quote on goal:g4.18.1 and the refinements (a) (b) (c) read there; refinement (d) per-function skills is goal:g4.18.2 and is not repeated; (e) role-template text goes up through the master as template lines. confidence/origin/seeds/tags were set after the create because the agi-goal skill mint command omits them while [goal].md requires them.
<!-- THOUGHT:END -->
