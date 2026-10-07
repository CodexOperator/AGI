---
id: goal:g7.16.1.11.14
mint_id: 5cbc2a6496694375a3cc854f214efa37
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.14
goal_kind: subgoal
origin: goal
scaffold_hash: 4401bbabd603fbca
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - design
  - g7.16.1.11
  - skills
  - load-matrix
title: "G7.16.1.11.14: skill deltas -- the skills an engine.v4 post loads describe the new system (boxes, lap, land, plain edits, agi-turn), by exclusion and delta, never by deleting a shared skill"
town: core
---
# goal:g7.16.1.11.14

## Why this exists
goal:g7.16.1.11: the owner's skills line (23:4xZ via belam 23:49Z, verbatim below) asked that the other skills reflect the way the new system works. The bundle splits it by author: AA1 = agi-send (doc:rse-aa1-boxes AA1.S), AA2 = the load-matrix exclusion of agi-node-write plus agi-rotate / agi-post / agi-goal deltas, AA3 = agi-master-gate / agi-merge-pass / agi-dispatch / agi-verify (AA3.7). The load matrix cannot be a deleted symlink: agi-turn's `add -A` would commit the deletion and the next land would remove the skill for EVERY post (all-is-one, measured).

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- An engine.v4 post's loaded skill set EXCLUDES agi-node-write (and any skill whose steps the new system automates) through a per-worktree sparse-checkout; skip-worktree paths are never staged as deletions; the committed .claude/skills links are untouched.
- Each delta is a DELTA, not a rewrite: what a v4 post does INSTEAD (box send/read/n instead of send.py; a plain node file + agi-turn instead of write.py; a land mail instead of the hand-gated merge-up; a child ROW instead of dispatch.py; grid.py by path, never --all); the old-setup text stays for belam, SM, DG3 and old TM until each moves.
- No skill step remains that a machine could do (nothing model-manual that could be automated): a step the new engine automates is deleted from the v4 text, not re-described.

## Invariants
- Skill text is changed when the bundle is BUILT, not before (AA1.S: 'the skill text itself changes when the bundle is built').
- A skill shared with the old setup is never edited in place for the old reader: the delta is additive or by load exclusion.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. In a v4 post's worktree `git status --porcelain | grep -c '^ D'` = 0 after agi-turn's `add -A`, and the loaded skill listing (the load matrix output) lacks agi-node-write.
2. Negative: `git grep -n 'write.py' -- <the v4 skill deltas>` returns zero hits outside a clearly marked old-setup note.

## Out of scope
goal:g7.16.1.11.11 / .12 / .13 (the systems the skills describe) · rewriting skills for the old setup.

## Agent Notes
Assigned to **director-general-1**.
