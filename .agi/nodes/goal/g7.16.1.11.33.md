---
id: goal:g7.16.1.11.33
mint_id: afa6cfbd2d3d4337b3f107a7fd7ec0d5
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.33
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 040765d592efa731
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - env
  - box
  - g7.16.1.11
title: "G7.16.1.11.33: .env.example carries an AGI_BOX shape line, so a new box can name itself before crons.py and boxes.this_box refuse it"
town: core
---
# goal:g7.16.1.11.33

## Why this exists
goal:g7.16.1.11: crons.py refused every box-gated job on E until belam set AGI_BOX by hand (SM 19:4xZ 10-09, relaying belam): MAIN's .env carried no AGI_BOX, so `boxes.this_box` (boxes.py:160-179) found it neither in the environment nor in the box env file and REFUSED by design ("an unset AGI_BOX REFUSES", no `default_box` fallback; the error says "no AGI_BOX in the env and none in the box env file"). Nothing tells a new box's operator that the key exists: `.env.example` (49 lines, "THIS FILE IS THE SHAPE. IT HOLDS NO VALUES") names the provider credentials and carries no AGI_BOX line, and it is the file a new box is told to copy (`cp .env.example .env`).

## Target end-state
- `.env.example` carries the shape line COMMENTED (`# AGI_BOX=<box>`), with a comment saying what it is: the town name this box answers to (a box fact, not a credential), read by `boxes.this_box` and by crons.py's box gate, REFUSED when absent.
- OPEN FOR THE COUNCIL, not decided here: whether `AGI_BOX` also joins the config cell's `required_keys` so `envfile.py --check` (goal:g1.8) names a box that lacks it; the shape line alone is the first deliverable.

## Invariants
- `.env.example` still holds no value that works anywhere, and no ACTIVE `AGI_BOX=` line: extensions/agi/driver.sh:118-123 (`set -a; source "$AGI_ENV_FILE"`) exports every active assignment over any inherited AGI_BOX, so a copied `AGI_BOX=` (empty) would make `boxes.this_box` read an empty value and refuse on a box that had the variable set in its environment (SM 21:4xZ L3). The line ships commented; the copy fills it and uncomments it.
- `this_box` still refuses on an unset value: no default is added.

## Falsifier
The command that decides is the first backticked one (agi-frontier): it exits 0 only when the work is done.
1. `test -n "$(git grep -n -E '^# AGI_BOX=<box>$' -- .env.example)"` (0 hits today; it also exits 1 for `AGI_BOX=core-town`, a value that works on one box only, and for the active empty line, SM L4), AND item 2 below.
2. `test -z "$(git grep -n -E '^AGI_BOX=' -- .env.example)"` (no active line; 0 hits today and after) and `python3 extensions/agi/bin/envfile.py --check` still exits as it does today on a box whose .env has AGI_BOX (the new line adds no required key unless the council rules it in).

## Out of scope
Setting AGI_BOX on any box (belam set it on E by hand) · who may read .env (belam's) · the anonymize guard's secret class (goal:g7.16.1.11.30).

## RULE SM placement 19:4xZ 10-09, relaying belam (SM's relay text; the cites in it are SM's, boxes.py re-read above)
"(3) belam: .env.example lacks an AGI_BOX shape line. Add it in .29's round or as its own leaf (MAIN's .env had no AGI_BOX, so boxes.this_box -> '' and crons.py refused every box-gated job on E. belam set it by hand.)"

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 23:5xZ: RE-CUT 1 on SM's 21:4xZ return (L3, L4). Read by me at 4fc8a1dc26: driver.sh sources the env file under `set -a`, so an active empty `AGI_BOX=` copied from .env.example is exported over an inherited AGI_BOX and boxes.this_box then reads the empty value and refuses; so the shape ships COMMENTED (`# AGI_BOX=<box>`). Falsifier 1 pins that exact commented form (an `AGI_BOX=core-town` or an active empty line both leave it unsatisfied), item 2 pins the absence of an active line. Previous version: 10-09 07:0xZ (active empty line).
<!-- THOUGHT:END -->
