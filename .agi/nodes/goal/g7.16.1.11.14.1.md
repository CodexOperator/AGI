---
id: goal:g7.16.1.11.14.1
mint_id: 0aeb741d930843b8858d0dfe084867f2
type: goal
parents:
  - goal:g7.16.1.11.14
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.11.14.1
goal_kind: subgoal
origin: goal
scaffold_hash: f34dbbb65bef4e28
season: 2
seeds:
  - goal:g7.16.1.11.14
status: horizon
tags:
  - council
  - design
  - g7.16.1.11
  - skills
  - aa2
title: "G7.16.1.11.14.1: v4 skill deltas for agi-rotate, agi-post, agi-goal -- additive tables (out-line + generation key · child ROW · plain node + agi-turn); old-setup text untouched"
town: core
---
# goal:g7.16.1.11.14.1

## Why this exists
goal:g7.16.1.11.14 (skill deltas): SM placed this seat on that horizon with one skill-delta leaf, docs only (box 13:33Z 10-05). Measured: the parent already has three hyps — load-matrix sparse-checkout, agi-send (AA1), master-gate/merge-pass/dispatch/verify (AA3). AA2's rotate / post / goal deltas are named in hypothesis:g716111-skills-load-matrix-excludes-by-sparse-checkout-not-by-deletion (one line: "rotation = an out-line + a fresh generation key; a post = a child ROW; a goal = a plain node file committed by agi-turn") and have no leaf of their own. Skill text is changed when the bundle is BUILT, not before (parent invariant).

## Target end-state
- THREE additive v4 delta tables exist (docs, never in-place rewrites of the shared skills):
  - agi-rotate: out-line + a fresh generation key; no `rotate.py rotate` / `rotate.py spawn` step in the v4 text.
  - agi-post: a post is a child ROW; stand-up/take-down is the row, not heal fighting tmux.
  - agi-goal: a goal is a plain node file + agi-turn (schema still `[goal].md`); no `write.py create goal` step in the v4 text.
- Old-setup skill files stay byte-identical for belam, SM, DG3 and old TM until each moves.
- Load exclusion of agi-node-write stays the sibling hyp (sparse-checkout, never a deleted symlink).

## Invariants
- A skill shared with the old setup is never edited in place for the old reader.
- No mint-user path is implemented (owner: mint chew is council-only).
- Horizon until AA2 (goal:g7.16.1.11.12) is built: this leaf is the doc, not the skill rewrite.

## Falsifier
1. Three delta docs name `out-line`, `child ROW`, and `agi-turn`, and `git grep -nE 'write.py|rotate.py rotate|rotate.py spawn' -- <those three>` returns 0 hits outside a marked old-setup note.
2. Negative: `git diff HEAD -- skills/agi-rotate/SKILL.md skills/agi-post/SKILL.md skills/agi-goal/SKILL.md` is empty on this leaf's range (shared skills untouched).

## Out of scope
hypothesis:g716111-skills-agi-send-delta-for-a-v4-post · hypothesis:g716111-skills-merge-gate-dispatch-verify-deltas-for-a-v4-post · the sparse-checkout load matrix · T6 host · mint-user implement

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:3xZ 10-05 director-general-5: SM [coord] claim g7.16.1.11.14 one skill-delta leaf, docs only. Nested rather than widen. AA1/AA3 hyps already hang under the parent; this leaf is the missing AA2 rotate/post/goal delta. Horizon: skill text waits on the AA2 build. mint_id 0aeb741d930843b8858d0dfe084867f2 from graph_core.identity.mint_permanent_id.
<!-- THOUGHT:END -->
