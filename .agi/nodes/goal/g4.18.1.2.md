---
id: goal:g4.18.1.2
mint_id: 40ce30b7bd5f4d478da2876dfe965660
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G4.18.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: f6fdabd3064e2539
season: 2
seeds: []
status: active
tags:
  - engine
  - write
title: "G4.18.1.2: the captive mint flow -- a draft filled one row per call, each row checked by the one validator, no interactive stdin"
town: core
---
# goal:g4.18.1.2

# goal:g4.18.1.2

## OWNER 2026-09-26 ~23:2xZ, verbatim (fragment; whole quote on goal:g4.18.1)
"Why can't minting just use the write function one step at a time as a captive flow the models follow? Each row filled out and format checked." / "recommending doing it manually one at a time to avoid backtick and quote confusion errors"

## Why this exists
goal:g4.18.1 -- swarm parents struggled with node creation (goal:g4.18.1 Evidence 09-26); a model composing one long `create` argv makes quoting errors a row-by-row flow cannot make.

## Target end-state
- A post mints by a DRAFT: one command opens it for a type, then one command per row fills and checks that row (goal:g4.18.1.1's validator), and a final command mints it; each step prints the next row to fill and its legal values.
- The flow needs no interactive stdin (panes have no operator): every step is a separate, resumable call over the draft file.
- The draft IS an answers file: a finished draft and a hand-written answers file mint through the same code.

## Invariants
- No row value is ever taken from a shell-quoted argv position that the model must escape; a value can come from a file or stdin.
- An abandoned draft mints nothing and blocks nothing.

## Falsifier
1. A scripted run of the step commands mints a hypothesis whose bytes equal the same mint made from an answers file, exit 0.
2. Negative: a step that fills a row with a value its schema regex refuses exits non-zero and the draft is unchanged.

## Out of scope
goal:g4.18.1.1 · goal:g4.18.1.3 · goal:g4.18.1.4 · goal:g4.18.1.5

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted by director-engine as one of five nested leaves of goal:g4.18.1 (standing: nest an ASSIGNED goal into sketched leaves before any parent is spawned). The split follows the owner quote on goal:g4.18.1 and the refinements (a) (b) (c) read there; refinement (d) per-function skills is goal:g4.18.2 and is not repeated; (e) role-template text goes up through the master as template lines. confidence/origin/seeds/tags were set after the create because the agi-goal skill mint command omits them while [goal].md requires them.
<!-- THOUGHT:END -->
