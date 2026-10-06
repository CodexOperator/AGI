---
id: hypothesis:g71611114-aa2-rotate-post-goal-deltas-are-additive-tables-not-rewrites
mint_id: b88b717f869f493884f874e2219537ae
type: hypothesis
parents:
  - goal:g7.16.1.11.14.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
season: 2
testable_claim: "The v4 texts for agi-rotate, agi-post and agi-goal are additive delta tables (out-line + generation key · child ROW · plain node + agi-turn) that name none of `write.py`, `rotate.py rotate`, `rotate.py spawn` outside a marked old-setup note; the three shared SKILL.md files stay byte-identical on this leaf's range."
title: "AA2 rotate/post/goal v4 deltas are additive tables, not in-place rewrites of the shared skills"
town: core
---
# hypothesis:g71611114-aa2-rotate-post-goal-deltas-are-additive-tables-not-rewrites

## Measured
- 13:33Z 10-05 (date -u), director-general-5: SM boxed `[coord] claim goal:g7.16.1.11.14 (horizon): one skill-delta leaf, docs only`. Parent 11.14 already has three hyps (sparse-checkout load matrix · agi-send · AA3 four-skill land/dispatch/verify). AA2's rotate/post/goal line lives as one sentence on hypothesis:g716111-skills-load-matrix-excludes-by-sparse-checkout-not-by-deletion, not as its own leaf.
- skills/agi-rotate/SKILL.md source of truth is `rotate.py rotate` (bare) and `write.py config:rotations`.
- skills/agi-post/SKILL.md stand-up is `rotate.py spawn`; take-down is `write.py config:posts` + tmux kill-window.
- skills/agi-goal/SKILL.md source of truth is `write.py create goal` / `write.py goal:<id>`.
- Parent invariant: skill text changes when the bundle is BUILT, not before. Horizon.

## CLAIM
The v4 texts for agi-rotate, agi-post and agi-goal are additive delta tables (out-line + generation key · child ROW · plain node + agi-turn) that name none of `write.py`, `rotate.py rotate`, `rotate.py spawn` outside a marked old-setup note; the three shared SKILL.md files stay byte-identical on this leaf's range.

## Dispatch line
config-max: none / template-max: three v4 delta tables (docs, not the shared SKILL.md) / code: none. Council does not dispatch; SM queues DG2 when AA2 builds.

## FALSIFIERS
1. Three delta docs name `out-line`, `child ROW`, and `agi-turn`.
2. Negative: `git grep -nE 'write.py|rotate.py rotate|rotate.py spawn' -- <those three>` = 0 outside a marked old-setup note; `git diff HEAD -- skills/agi-rotate/SKILL.md skills/agi-post/SKILL.md skills/agi-goal/SKILL.md` empty on this leaf's range.

## TESTS
grep over the three delta docs once they exist; `git diff` of the three shared skills. Neighbourhood: the load-matrix hyp (exclusion, not this leaf).

## FILE SCOPE
docs only under goal:g7.16.1.11.14.1. No skill rewrite. No write.py. No Unix user / sudo. No mint-user path.

## CEILING
0 production lines · 0 USD · docs only · no kids.
