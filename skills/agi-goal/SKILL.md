---
name: agi-goal
description: >
  Create, edit, renumber or retire an agi GOAL node, with the [goal] schema inline
  (fields, regexes, legal parents, fixed body order). Use whenever a post mints a
  goal or subgoal, decomposes a goal into subgoals, changes a goal's status/title,
  renumbers one, or checks GOALS.md. goal:g4.18.2 (owner 2026-09-27: "goal creation
  would automatically include the schema in the skill").
---

# agi-goal — goals, with their schema

Source of truth: `.agi/context/schemas/[goal].md` (the schema) · `write.py` (the only writer).
This skill is its manual; when the two disagree, the schema wins — fix this file.

## 1 · Mint a goal (one command)
```bash
python3 extensions/agi/bin/write.py create goal <gX.Y.Z> \
  --parent goal:<gX.Y> [--parent build:<id>] \
  --set goal_id=<GX.Y.Z> --set goal_kind=subgoal --set status=active \
  --set 'title=<GX.Y.Z>: <target end-state in one line>' \
  --body-file <body.md> --actor <post> --role <role>        # --dry-run first
python3 extensions/agi/bin/snapshot-goals.py --render       # GOALS.md is DERIVED
python3 extensions/agi/bin/snapshot-goals.py --render --check   # exit 0 = byte-identical
```
- `write.py` has NO goal-specific logic: `goal_id` + `goal_kind` arrive ONLY through `--set`.
  A goal minted without them (the slug alone) has no `goal_id` — fixing that later is a renumber.
- slug = lowercased `goal_id` (`G4.18.2` → `goal:g4.18.2`); `S4` → `goal:s4`.
- Commit the node + `GOALS.md` by exact path. Never hand-edit `GOALS.md`: the next render erases it.

## 2 · The schema (as at 2026-09-27)
```
required : id type mint_id title goal_id goal_kind status origin seeds confidence tags
regex    : goal_id   ^[GS]\d+(\.\d+)*$
           goal_kind ^(long-term|perpetual|short-term|subgoal)$     long-term = legacy perpetual
           status    ^(active|horizon|retired|phasing-out|complete)$  phasing-out = legacy retired
types    : seeds list · tags list · confidence float
round_commit: false  — a round's `cli.py done` never sweeps a goal node
```
| goal_kind | allowed parents | min..max | rule |
|---|---|---|---|
| perpetual / long-term | build, goal, vision | 1..2 | a NEW one hangs under a vision or goal (G1/g15/g16 roots grandfathered) |
| short-term | build, goal | 1..2 | |
| subgoal | build, goal | 1..3 | at least ONE goal parent (`min_parents_by_type`) |

`retired` ≠ `complete`: complete = achieved (keeps scoring); retired = stopped making sense (leaves the score, stays in the graph).

## 3 · The body — fixed order (owner 09-23, goal:g5; a merge-up reviewer checks it)
```
# goal:gX.Y
## Why this exists      one paragraph PER PARENT EDGE: the parent + what it measured that made it a parent
## Target end-state     world-after claims, not tasks
## Invariants           always-true, or the graph is wrong
## Falsifier            1. a CLI/grep that exits 0 only when done  2. a negative: forbidden path, zero hits
## Out of scope         sibling goal:… ids
## Agent Notes          "Assigned to **<post>**." and nothing else
```
Owner words are copied VERBATIM into the body (a `## OWNER <date> <time>, verbatim` section) — the node is
where owner verbatim lives, never a card. Framing: a target end-state, never "finish today or failed".

## 4 · Edit · retire · renumber
| op | how |
|---|---|
| edit a field | `write.py goal:<id> 'set status complete && thought <why this version>'` |
| add a note | `write.py goal:<id> 'note <sentence>'` — notes land where the HEAD's notes line says; goals are trackers (owner 09-24) |
| retire | `set status retired` + deprecate its seed node — NEVER delete, never `git rm` |
| renumber (owner 09-23) | keep `mint_id`; re-point EVERY frontmatter reference in the SAME commit; old → new in the moved node's THOUGHT; a retired id is never reused |
| decompose | one subgoal per leaf (§1), nest rather than widen; each is driven by a dispatched parent (skill `agi-dispatch`) and judged with `season.py judge <outcome> --against goal:<id>` |

Every version's why goes in the `THOUGHT` block (`thought <text>`, rewritten whole, never appended;
absent = empty, never fabricated). Mechanism-not-wording: (1) the instruction quoted, (2) what the machine
does at file:line, (3) the near miss, (4) the property that made a standing rule not apply.

## 5 · Retired designations
g14 → `goal:g5` · g13 → none (read/write-path work: `goal:g4.19`) · g15 → g20 → `goal:g1`. A retired id in a live node, card, brief or dm is a bug.
