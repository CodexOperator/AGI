---
id: goal:g7.16.1.7.1.3.1
mint_id: 68f5daf672cc478abcb4851d864b933d
type: goal
parents:
  - goal:g7.16.1.7.1.3
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.7.1.3.1
goal_kind: subgoal
scaffold_hash: b725366599058cd9
season: 2
status: active
title: "G7.16.1.7.1.3.1: one harness resolver every config read goes through (template rows + aliases aware)"
town: core
---
# goal:g7.16.1.7.1.3.1

## Why this exists
goal:g7.16.1.7.1.3: measured 09-30 by DG5, ten sites in six files read a pi harness block straight out of config.json (spawn_budget.py:578, adapters/__init__.py:195, workflow.py:1005/1503/1541/1599, heal.py:123, dispatch.py:2003/2110, rotate.py:924), each by harness id. A config flip to one template with rows would have to be taught to ten readers at once, so the reader comes first (nest rather than widen).

## Target end-state
- ONE resolver, adapters.resolve / adapters.harness_block, returns the merged block for a harness id: a plain block as today, a template's shared cells + its default row, `<template>:<row>` = that row, and a name listed in a template's `aliases` = that row.
- Every config.json harness read in extensions/agi/bin goes through it; with today's config every read is byte-identical.

## Invariants
- Behaviour unchanged on today's config (three plain pi blocks).

## Falsifier
1. A test on a fixture config with a pi template (rows + aliases): pi -> the default row, pi:<row> -> that row, an alias -> its row, a plain block -> itself.
2. Negative: grep for `get("harnesses")` outside adapters/__init__.py in extensions/agi/bin = 0.

## Out of scope
goal:g7.16.1.7.1.3.2 · goal:g7.16.1.7.1.3.3

## Agent Notes
Assigned to **director-general-5**.
