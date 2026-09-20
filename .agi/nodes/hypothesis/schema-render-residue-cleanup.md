---
id: hypothesis:schema-render-residue-cleanup
mint_id: 46d9c18a085247969d0eb7d1106395c5
type: hypothesis
parents:
  - goal:g17.14
next_edges: []
edited_by: a00-9ae9e1e9
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: parent
scaffold_hash: 1769dd139cc3ce9b
season: 2
testable_claim: The g17.14 subgoal goal nodes carry heading_level 3 and snapshot-goals.py --render --check exits 0 on the corrected tip.
title: Schema render residue cleanup
town: core
---
# hypothesis:schema-render-residue-cleanup

## Testable claim

On the corrected tip, `goal:g17.14.1`, `goal:g17.14.2` and `goal:g17.14.3` each carry `heading_level: 3`, and `snapshot-goals.py --render --check` exits 0. The g17.14-referenced decisive hypotheses carry no self-citing `evidence_runs`; any hypothesis the residue names that is absent from this checkout is moot, never silently backfilled.

## What would prove it

`snapshot-goals.py --render --check` exits 0 after the heading_level writes and the derived GOALS.md re-render; the schema scan reports zero nodes missing a required field on the g17.14 line.

## What would disprove it

The render gate still errors with "has no heading_level"; or `--render --check` exits non-zero with a derived/node mismatch; or a g17.14-referenced hypothesis self-cites its own id in `evidence_runs`.

## Agent Notes
Residue-4 disposition on this checkout: heading_level backfilled on goal:g17.14.1/.2/.3 and the derived GOALS.md re-rendered so snapshot-goals.py --render --check exits 0 (189 goals byte-identical). The residue clauses naming hypotheses a00-8e139c40-f77c9b / a00-da41e117-c79b5e (testable_claim) and a00-bfd0d94a / a00-debf9c6e (self-citing evidence_runs) are MOOT here: those nodes exist only on the helper-grok line (base 1bbbc911), not on core/season2/main, which this worktree was cut from. Bin path: the grok-bot binary path is NOT verified and no install is invented; if a seating row names harness grok-bot, its bin must be validated by a soft existence check at resolve time, never assumed present (Belam stub practice).
