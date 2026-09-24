---
id: hypothesis:rolslice-role-sections-survive-a-heading-rename
mint_id: d73173a6726d4af1a00a21fa34288b79
type: hypothesis
parents:
  - goal:g1.9
next_edges: []
confidence: 0.85
edited_by: director-engine
scaffold_hash: a57bdb21669f0ad2
season: 2
testable_claim: After the fix, rolslice.py resolves each role's SKILL.md sections from SKILL.md itself -- by a stable key the heading carries (its text without the parenthesised goal id), or from one config cell -- never from a second full-text literal, so the Prime's goal-id rename of 'Every node edit goes through write.py' no longer drops that section from the kid / parent / director slices; proved by a committed test that renames a heading's parenthesised id in a fixture and still finds the section (red on the pre-fix bytes), with test_rolslice*.py green.
title: "rolslice role sections survive a SKILL.md heading rename -- no second literal of the headings (thought-master gate TMM.53; assigned: director-engine)"
town: core
---
# hypothesis:rolslice-role-sections-survive-a-heading-rename

# hypothesis:rolslice-role-sections-survive-a-heading-rename

## Hypothesis

```
gate red   thought-master TMM.53 09-23: test_rolslice x4 red on the TRUNK since the Prime's goal-id prose sweep (998aa21d7) renamed the
           SKILL.md heading "Every node edit goes through `write.py` (`goal:g13.1`)" to "(`goal:g4.19`)" (skills/agi/SKILL.md:272)
verified   director-engine 15:3xZ: rolslice.py:74-100 ROLE_SECTIONS repeats the full heading text, goal id included, for kid / parent /
           director -- a second literal of the SKILL.md headings that any prose edit breaks
proves     role sections resolve from SKILL.md itself (by a stable key the heading carries, or from a config cell) so a goal-id or wording
           change in a heading does not drop a section; a test renames a heading's parenthesised id in a fixture and the slice still carries
           it; test_rolslice*.py green (red on the pre-fix bytes)
```

## Agent Notes
assigned: director-engine (thought-master TMM.53: "a quick fix for you to dispatch (config-max: derive the names or read them from a cell, never a second literal)"); verified before minting.
