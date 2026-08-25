---
confidence: 1.0
goal_id: G7.1
goal_kind: subgoal
id: "goal:g7.1"
mint_id: 3feb9ce4e95341bb96ecc424bc5b7421
origin: goals-doc
parents:
  - goal:g7
seeds:
  - exp:integrity-detection-r1
status: active
tags:
  - goal
  - subgoal
title: "G7.1: Referential integrity on every parent reference"
type: goal
---

L15 validates `goal:`-prefixed parents only. Everything else dangles silently,
and on this corpus 60.3% of parent references did — a `hypothesis:` vs `hyp:`
prefix mismatch that quietly disconnected most of the `spawns` graph the
attractiveness ranking is computed over. Nothing warned, and the ranking was
read as authoritative for months.

Extend the existing check to all parent references: warn by default, `--strict`
to fail. The mechanism exists; only its scope is wrong. Owns TODO **H4d**.
