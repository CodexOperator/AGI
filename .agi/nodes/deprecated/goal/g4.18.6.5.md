---
id: goal:g4.18.6.5
mint_id: d0c62157206843e7a5cf7bcab0c13363
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.5
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 2c36915012372854
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.5: no link ever needs re-pointing -- the renumber re-point rule retires from CLAUDE.md and the agi-goal skill, a retire with a live referrer is handled, the whole walk stays off the write path (row W2e; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.5

## Why this exists
goal:g4.18.6 bullet 4 + the goal:g7.16.1.4 W2 coupling. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): the rule lives at CLAUDE.md:107 and skills/agi-goal/SKILL.md:68 ('re-point EVERY frontmatter reference', upper case: the bundle's case-sensitive falsifier grep misses it) and :4/:7 name renumbering. Bullet 4 does NOT hold yet: every create walks all node files; that walk is goal:g4.18.6.2.2's. goal:g4.18.6 itself carries a doubled `# goal:` H1 and a title stored WITH its quotes.

## Target end-state
- CLAUDE.md:107's re-point clause and the agi-goal renumber row say what a renumber is once links are mint ids (the address changes, nothing is re-pointed); a retire of a node with a live referrer is refused or leaves the referrer resolving (goal:g4.18.6 Falsifier 1, second half).
- Hygiene: goal:g4.18.6's doubled H1 and quoted title are fixed by the row that edits it. Text only: no hypothesis.

## Invariants
- No link breaks on a renumber, move or retire.

## Falsifier
1. A committed test: a retire of a node with a live referrer is refused or the referrer still resolves.
2. Negative: `git grep -n -i 're-point every' -- CLAUDE.md skills` prints 0 (case-INSENSITIVE).

## Out of scope
goal:g4.18.6.4 (lands first)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29). The falsifier is case-insensitive on purpose: the bundle's grep would pass with SKILL.md:68 still teaching the rule.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
