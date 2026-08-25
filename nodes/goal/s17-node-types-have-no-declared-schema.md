---
confidence: 1.0
goal_id: S17
goal_kind: short-term
heading_level: 2
id: "goal:s17"
mint_id: 46b7d8f76a8742bf9aafa5a82ad8cca3
order: 64
origin: goals-doc
seeds:
  - idea:schema-declared-spawn-gate
status: active
tags:
  - goal
  - root
  - short-term
title: "S17: Node types have no declared schema, so a spawn is never checked"
type: goal
---

**Seven node types are in daily use and `context/schemas/` declares six of
them — and the overlap is not what you would guess.** Active (bracketed, per
`schema_registry/loader.py`: `[name].md` is active, `name.md` is inactive):
`experiment`, `hypothesis`, `idea`, `mvp`, `outcome`, `task`. Absent entirely:
**`verdict`** — the type the evidence gate exists to police — plus `goal`,
`level3`, `bigger_outcome` and `app_purpose`. `agent_session.md` sits
unbracketed and therefore inactive.

So the most consequential node type in the graph has no declared shape, and
nothing anywhere checks a node against a schema at write time.

**What has to exist, and it is three separate things:**

1. **Schemas for the missing types**, and a review of the ones that exist. The
   two new ones are structural rather than content-bearing and belong to the
   graph's own geometry (`.geometry`, **G10.2**):
   - **`config`** — where things are on the filesystem: the graph repo, the
     assembled code repo, the payload checkout. Today those are constants
     scattered across `find-root.sh`, `level3.py`'s `DEFAULT_ENGINE_ROOT` and
     `grid.py`'s `default_engine_root()`, which is three definitions of one
     fact.
   - **`shape`** — what shape the grid ref system takes, which node types may
     parent which, and the maximum number of parents any node may declare.
     This is the graph describing its own geometry rather than a reader
     inferring it.

2. **A spawn rule table, derived from the corpus rather than invented.**
   Measured 2026-08-25 across 767 nodes — observed parent types and the
   maximum parent count actually used:

   | type | n | max parents | parent types seen |
   |---|---|---|---|
   | `level3` | 185 | 2 | idea, goal |
   | `hypothesis` | 105 | 2 | idea, goal, experiment, hypothesis |
   | `task` | 91 | 1 | hypothesis |
   | `verdict` | 83 | 2 | experiment, verdict, hypothesis |
   | `experiment` | 75 | 2 | hypothesis, verdict, goal, task, idea, experiment, level3 |
   | `goal` | 73 | 1 | goal |
   | `idea` | 71 | 1 | goal |
   | `mvp` | 26 | 2 | verdict, goal, experiment, hypothesis |
   | `outcome` | 19 | 2 | mvp, verdict |
   | `bigger_outcome` | 17 | 2 | outcome, mvp |
   | `app_purpose` | 15 | 2 | bigger_outcome, outcome |

   **Exactly three types may be parentless: G-goal, S-goal, and `idea`.**
   Everything else must declare at least one parent. Note what that implies
   about the corpus as it stands: 24 hypotheses, 21 verdicts, 4 experiments and
   2 level-3 nodes are parentless today. **They are a report, not a purge** —
   G7's first invariant is that node count never drops, and G7.1 already
   established the policy that a bad reference is fixed or dropped, never the
   node.

3. **Feedback on every spawn, approved *and* rejected.** A validator that only
   speaks up on failure teaches nothing; an agent cannot tell "accepted" from
   "not checked". Both paths report, naming the rule that was applied.

**The design constraint that decides how this is built:** this is a code
control replacing a prose one, which is what the design ethic demands — "no
prose-only controls where a code control is possible". The schema is data
(`context/schemas/`), the check is code, and the check runs on the writer path
the way `evidence_gate.py` already does for verdicts, not as a linter someone
remembers to run.

Falsifier: attempt to write a `verdict` with no parent and a `task` with three
parents. Both must be rejected with a message naming the rule and the schema
file. Attempt a legal spawn and get an explicit approval line. If any of the
three is silent, this is not done.
