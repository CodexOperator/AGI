---
name: agi-goal
description: >
  Create, edit, renumber or retire an agi GOAL node, with the [goal] schema inline
  (fields, regexes, legal parents, fixed body order). Use whenever a post mints a
  goal or subgoal, decomposes a goal into subgoals, changes a goal's status/title,
  renumbers one, or reads one by id. goal:g4.18.2 (owner 2026-09-27: "goal creation
  would automatically include the schema in the skill").
---

# agi-goal — goals, with their schema

> **write.py is the OLD setup's node writer.** Quoting skill agi-node-write: "OLD SETUP ONLY (a post whose row has engine.v 4 edits node files with plain Write/Edit and agi-turn commits; owner 10-01 23:3xZ)". Every `write.py` command below is for a post on the old setup; a post whose row has engine.v 4 edits the node file directly. The routing in this skill is unchanged.

Source of truth: `.agi/context/schemas/[goal].md` (the schema) · `write.py` (the old setup's writer).
This skill is its manual; when the two disagree, the schema wins — fix this file.

## 1 · Mint a goal (one command)
```bash
python3 extensions/agi/bin/write.py create goal <gX.Y.Z> \
  --parent goal:<gX.Y> [--parent build:<id>] \
  --set goal_id=<GX.Y.Z> --set goal_kind=subgoal --set status=active \
  --set 'title=<GX.Y.Z>: <target end-state in one line>' \
  --body-file <body.md> --actor <post> --role <role>        # --dry-run first
python3 extensions/agi/bin/write.py goal:<id> 'read body 1:60'   # read it back by id
```
- `write.py` has NO goal-specific logic: `goal_id` + `goal_kind` arrive ONLY through `--set`.
  A goal minted without them (the slug alone) has no `goal_id` — fixing that later is a renumber.
- slug = lowercased `goal_id` (`G4.18.2` → `goal:g4.18.2`); `S4` → `goal:s4`.
- A write commits itself by exact path (message: the `write.commit_message` cell in `.agi/config.json`). Under a held suite lock it writes, prints `the write landed uncommitted` and the one commit-by-path line: run THAT line, nothing else (never `git add -A`; the grid cron is never the commit path). GOALS.md is retired (goal:g7.16.1.4.1): never recreate it.

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
Progress on a goal is never written on the goal or a card: one numbers-only line on the town board (skill agi-dispatch §5 "progress → board").

## 4 · Edit · retire · renumber
| op | how |
|---|---|
| edit a field | `write.py goal:<id> 'set status complete && thought <why this version>'` |
| add a note | `write.py goal:<id> 'note <sentence>'` — notes land where the HEAD's notes line says; goals are trackers (owner 09-24) |
| retire | `set status retired` + deprecate its seed node — NEVER delete, never `git rm`. NEVER while a child hypothesis is pending: place each child first (re-parent to the live goal it serves, or retire it too); a goal whose children PROVED it is `complete`, not retired (owner 04:4xZ 09-30, goal:s31) |
| renumber (owner 09-23) | keep `mint_id`; re-point EVERY frontmatter reference in the SAME commit; old → new in the moved node's THOUGHT; a retired id is never reused |
| decompose | one subgoal per leaf (§1), nest rather than widen; each is driven by a dispatched parent (skill `agi-dispatch`) and judged with `season.py judge <outcome> --against goal:<id>` |

Every version's why goes in the `THOUGHT` block (`thought <text>`, rewritten whole, never appended;
absent = empty, never fabricated). Mechanism-not-wording: (1) the instruction quoted, (2) what the machine
does at file:line, (3) the near miss, (4) the property that made a standing rule not apply.
A brief (hypothesis node) that returns from a gate: re-read the WHOLE node before a re-cut; never patch-on-patch (belam [rule] 10-08 08:4xZ, after E2's six cuts, RE8/RE9/RE11/RE12 were my own patches contradicting each other).

## 5 · Nested subgoals — how every role splits work (director template §Standing "nest", owner 09-21 01:5xZ + 09-23 10:2xZ)
```
goal:gX (assigned to you)
 ├─ sketch the LEAVES first: goal:gX.1 · gX.2 · …        each a full goal node (§1-§3), goal_kind=subgoal, ONE target end-state
 │    └─ too big for one round? split AGAIN: gX.1.1 · gX.1.2      nest rather than widen — never one fat sibling
 ├─ hypotheses hang UNDER A LEAF, never flat under a big goal     one hypothesis per round; its parent = the leaf it serves
 ├─ a residue big enough for its own round → a smaller goal LEAF under the goal that yielded it (then its hypothesis)
 └─ batch as resources allow; spawn parents ONLY against sketched leaves (skill agi-dispatch)
NEVER a new top-level goal (the Prime mints those, on the owner's word) · a loop your card names R&D needs no nesting (owner 09-23)
```
Next free id under a goal: the highest existing `goal_id` child + 1 (`git grep -h '^goal_id: GX\.' -- .agi/nodes/goal`). The leaf's `## Why this exists`
names the parent and the measured thing (a PASS, a verdict, a residue) that made it a leaf.

## 6 · Retired designations
g14 → `goal:g5` · g13 → none (read/write-path work: `goal:g4.19`) · g15 → g20 → `goal:g1`. A retired id in a live node, card, brief or dm is a bug.
