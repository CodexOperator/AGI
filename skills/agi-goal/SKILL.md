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

> The node writer is retired (goal:g7.16.1.11.46.23): a goal is a plain file `.agi/nodes/goal/<id>.md`, read with `sed`, edited in place (skill agi-node-write §1: read, edit, `links.py schema` + `links.py links`, commit by exact path). Only the MINT below runs engine code.

Source of truth: `.agi/context/schemas/[goal].md` (the schema) · `node_writer.write_node` (the one routine that mints a node file).
This skill is its manual; when the two disagree, the schema wins — fix this file.

## 1 · Mint a goal (one command)
```bash
cd extensions/agi/bin && python3 - <<'EOF'
import node_writer
r = node_writer.write_node('../../../.agi', 'goal', '<gX.Y.Z>', ['goal:<gX.Y>'],      # parents: 1..3, at least one goal
    extra_fm={'goal_id': '<GX.Y.Z>', 'goal_kind': 'subgoal', 'status': 'active', 'confidence': 0.5, 'origin': 'goal',
              'seeds': [], 'tags': [], 'title': '<GX.Y.Z>: <target end-state in one line>'},
    body=open('<body.md>').read())
print(r.status, r.reason)                                          # 'written'; a rejection writes nothing
EOF
sed -n '1,60p' ../../../.agi/nodes/goal/<gX.Y.Z>.md               # read it back by id
```
- `write_node` has NO goal-specific logic: `goal_id` + `goal_kind` arrive ONLY through `extra_fm`.
  A goal minted without them (the slug alone) has no `goal_id` — fixing that later is a renumber.
- slug = lowercased `goal_id` (`G4.18.2` → `goal:g4.18.2`); `S4` → `goal:s4`.
- The mint writes the file and nothing else: run `links.py schema` + `links.py links`, then commit it by exact path (a post: `agi-wt new <path>` / `agi-at <path>`; never `git add -A`; the grid cron is never the commit path). GOALS.md is retired (goal:g7.16.1.4.1): never recreate it.

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
**Close on the falsifier AS WRITTEN** (council, goal:g7.16.1.11 loop end 10-11: .34, the .13 pair and .19 closed with theirs unmet): `complete` only when every falsifier as written passes, or the close commit amends the falsifier with its reason in the THOUGHT. Never complete with an unmet falsifier left standing, and never rewrite a falsifier afterwards to fit what was built.

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
A negative-grep falsifier over `.agi/nodes` -> exclude the nodes that quote the pattern or anchor it, and run the falsifier once before committing the leaf: it hits its own title/quotes (DG1 g1.31.3 x3 10-01: 19 quotes, 0 pointers).

## 4 · Edit · retire · renumber
| op | how |
|---|---|
| edit a field | edit the frontmatter line in `.agi/nodes/goal/<id>.md` (e.g. `status: complete`) and rewrite the THOUGHT block: why this version differs |
| add a note | one sentence under `## Agent Notes` in the goal file; goals are trackers (owner 09-24) |
| retire | `set status retired` + deprecate its seed node — NEVER delete, never `git rm`. NEVER while a child hypothesis is pending: place each child first (re-parent to the live goal it serves, or retire it too); a goal whose children PROVED it is `complete`, not retired (owner 04:4xZ 09-30, goal:s31) |
| renumber (owner 09-23) | keep `mint_id`; re-point EVERY frontmatter reference in the SAME commit; old → new in the moved node's THOUGHT; a retired id is never reused |
| decompose | one subgoal per leaf (§1), nest rather than widen; each is driven by a dispatched parent (skill `agi-dispatch`) and judged with `season.py judge <outcome> --against goal:<id>` |

Renumber -> a plain edit, or a script anchored on the FULL line; never `str.replace` an id/Why prefix (it hit the id row of .5.5.5; DG4 d1eb5ecad). Order: body edits FIRST, THEN `git mv` + id/parents/goal_id as ONE commit, THEN re-point refs; keep `mint_id` (all-is-one 09-23).
Every version's why goes in the `THOUGHT` block (the text between its markers, rewritten whole, never appended;
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
A count or claim shared by several leaves -> measure it ONCE per row with its own command; never copy a Measured line into each leaf (DG1 W2: the wrong 8654 line sat in 5 leaves).
Next free id under a goal: the highest existing `goal_id` child + 1 (`git grep -h '^goal_id: GX\.' -- .agi/nodes/goal`). The leaf's `## Why this exists`
names the parent and the measured thing (a PASS, a verdict, a residue) that made it a leaf.

## 6 · Retired designations
g14 → `goal:g5` · g13 → none (read/write-path work: `goal:g4.19`) · g15 → g20 → `goal:g1`. A retired id in a live node, card, brief or dm is a bug.

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a 'what do I own' grep -> search the council's name too: `'Assigned to **council**'` (alive gen 12: told SM alive owns no leaf, then corrected)
