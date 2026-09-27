---
id: doc:draft-skills-first-turn
mint_id: 815cbacff5b441f7a832a6841135930a
type: doc
parents:
  - goal:g4.18.2
next_edges: []
edited_by: director-engine
scaffold_hash: 7fef1ea3005738bd
season: 2
title: "doc:draft-skills-first-turn -- DRAFT config:rotations entry: the skill index on every rotated seat's first turn by template edit only (handed to the owner)"
town: local-maxxing
---
# doc:draft-skills-first-turn

`config:rotations` DRAFT (director-engine, 2026-09-27): the skill index on every rotated seat's first turn, by TEMPLATE EDIT ONLY. Handed to the owner, who informs thought-master; a director never writes config:rotations.

## Answer
```
YES, for every ROTATED seat, on any harness   the template's first_turn output is plain text appended to the successor's first input
NO, for dispatched parents / kids            their first turn is the dispatch brief (config:brief), not config:rotations -- BANKED: config:brief extras.parent (L4.110 ring-gate)
```

## Measured
| check | result |
|---|---|
| startup gate `rotate._producing_refusal` (F12) on the chained cmd | `None` = admitted |
| shell readers (grep, git grep, head, sed, awk, ls, cat, git show / ls-files) | all REFUSED by the same gate |
| run | rc 0 · 4294 bytes · 0.87 s (first_turn_timeout_s 120) |
| byte cap | per entry (rotate.py:13573-13577: an entry-level `byte_cap` wins) -> 5000 here; the template caps (8000 / 40000) are untouched |
| templates | exactly two: `director` (every director + master seat) and `prime_director` |

## The edit -- ONE line, appended to BOTH lists
- `templates.director.startup.first_turn`: after the `send-verbs` entry
- `templates.prime_director.startup.first_turn`: after the `landed-since-stamp` entry

```
        - {"label": "skills", "byte_cap": 5000, "cmd": "python3 extensions/agi/bin/write.py build:skills-agi-corrective-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-dispatch-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-goal-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-merge-pass-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-node-write-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-rotate-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-send-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-verify-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-SKILL.md 'read payload 2:12'", "why": "OWNER 2026-09-27 05:4xZ (director-engine pane): 'Can template edits only add the skill index in there for any harness on first turn?' -- each skills/*/SKILL.md name + description, read from the file itself through its build node (write.py read payload), never a copy; one clause per skill until the TMM.284 emitter replaces the chain with one call"}
```

## Limits (why TMM.284's emitter still earns its place)
| limit | effect | who fixes |
|---|---|---|
| one clause per skill | a NEW skill needs one clause added here | the TMM.284 emitter (skills/*/SKILL.md globbed, no edit) |
| line range pinned per file (`2:<closing --- - 1>`) | a description that grows or shrinks drifts the range | same emitter |
| `build:skills-agi-corrective-SKILL.md` exists only on the director-engine post branch | its clause prints one ERR line until that merge-up lands on the trunk | drop that clause, or land after the merge-up |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. (1) Owner 05:4xZ in the DE pane: "Can template edits only add the skill index in there for any harness on first turn? If so do the template edits as drafts and hand those off I will inform TM". (2) Every shell reader is refused by the startup gate (measured); write.py read payload through each skill build node is admitted, so the text is read from the SKILL.md itself, never copied. (3) Near miss: a single glob reader would need a new producer -- that is TMM.284, code, a kid round. (4) The line was proven by inserting it into a scratch copy of config:rotations: both templates parse (9 and 10 entries) and the entry runs rc 0, 4294 bytes.
<!-- THOUGHT:END -->
