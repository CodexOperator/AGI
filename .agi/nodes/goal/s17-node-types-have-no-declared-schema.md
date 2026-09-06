---
id: goal:s17
mint_id: 46b7d8f76a8742bf9aafa5a82ad8cca3
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S17
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds:
  - idea:schema-declared-spawn-gate
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S17: Node types have no declared schema, so a spawn is never checked"
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

**Writer coverage closed 2026-08-26. Still active for the corpus half.**
`verdict:spawn-gate-lands-on-writer-path` recorded the gate reaching 2 of ~6
writers, with `dispatch.py` carrying a *duplicated, un-gated copy* of the whole
scaffold routine — its own type tuple, its own body prompts, its own
`write_text()`. It was deleted rather than gated: `bin/node_writer.py` is now
the only routine that creates a node file, and all four spawn writers
(`cli.py scaffold`, `cli.py done`, `post_wire.py`, `dispatch.py`) reach it the
same way. Gating the copy would have left two gated routines to drift apart,
which is the one-fact-many-definitions defect this goal names rather than the
fix for it.

Four defects fell out of the merge that the duplication had been hiding: every
big-zoom scaffold was an illegal parentless `hypothesis` (now an `idea`, one of
the three parentless-legal shapes); `post_wire.py`'s fallback verdict minted no
`mint_id` and named its file after the *parent's* slug while its `id:` used the
agent id; and dispatch.py's re-scaffold branch compared bodies against a string
it never equalled, so it was dead code. The hyphen generator is gone with it —
the 2 `bigger-outcome` and 2 `app-purpose` nodes were renamed the same day
(file, `id:` and `type:`, mint ids preserved, 5 inbound edges rewritten), so the
corpus is now underscore-only.

**Surveyed against all 781 nodes afterwards: three of those four had written
nothing.** Zero nodes with a null parent entry, zero without a `mint_id`, zero
with unparseable frontmatter. They were latent — reachable but not yet reached.

**The fourth was live, and it was the read side of the same defect.** The
fallback verdict's filename bug was the visible edge of `cli.py`'s and
`post_wire.py`'s two disagreeing copies of "id → file". `post_wire`'s could not
resolve **417 of 781 ids**; `cli`'s missed 147 (every id on an abbreviated
`exp:`/`hyp:` prefix); 270 were resolvable by one and not the other. That one
mattered because post_wire's "not found" branch does not report — it *creates a
verdict node*, so an unresolved id minted a duplicate instead of updating its
target, on the writer whose job is updating verdicts. `node_writer` now holds
the one lookup beside the one write; both readers resolve all 781 and agree.

**What keeps this goal active:** the corpus half is untouched by design — 53
nodes violate `min_parents` and 3 carry no `type:` at all. The three
*generators* (`snapshot-goals.py`, `snapshot-build-site.py`, `level3.py`) are
still un-gated, still deliberately: they re-derive a whole node population from
an input file rather than spawning, and a generator that trips the gate is a
generator bug that H0i says should be reported, not failed on.

## 2026-08-27: the grammar grew a per-kind floor, and the corpus half shrank

`spawn:` gained **`min_parents_by_type`** — a mapping of parent type to a
minimum count of parents *of that kind*. `min_parents` counts parents; this
counts what they are. Two outcomes and "one verdict plus one outcome" are the
same arity and different shapes, and only the second is convergence; arity
alone cannot say so. Four unsatisfiable forms are **schema errors that leave
the type unverified**, not runtime rejections — a rule no node could ever pass
would reject its whole type forever, which is louder than the missing rule it
replaced.

`[shape].md` also gained `edge_fields`, classifying each edge as lineage,
scheduling, provenance or proposal. **Parsed, not yet enforced** — recorded as
a residual in that file rather than claimed.

**The corpus half moved for the first time, and not by editing the corpus.**
21 nodes that looked parentless to the gate were in fact naming a real parent
under a key no gate reads (`parent_hypothesis` 10, `parent_idea` 9, `parent`
4). Those edges were *written down*, so moving them into `parents:` was repair
rather than the edge-invention G7.1 forbids:

    min_parents violations   91 -> 70
    nodes with no `type:`     3 -> 0
    dangling references      15 -> 0

**What still keeps this goal active:** 70 `min_parents` violations remain and
are untouched by design, plus 36 nodes that violate the three new PRESCRIPTIVE
schemas (`[bigger_outcome].md`, `[overview].md`, `[vision].md`) — those state
what should be rather than what is, and the corpus is expected to fail them
until it is written up to them. The three generators remain un-gated for the
reason above. One type is still **unverified**: `doc`, which has no
`[doc].md` at all — one node, `doc:goals-preamble`, and it is the file that
renders GOALS.md's preamble.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep. Node types have declared schemas —
16 files under `context/schemas/`, each owning its own `spawn:` block — and
`spawn_gate.check_spawn` enforces them on every writer path through the one
routine, `node_writer.write_node`.

Proven live the same day rather than assumed: `goal:s22` changed two schemas'
`allowed_parents` and the gate immediately began rejecting `goal -> mvp` and
`goal -> experiment` at exit 2 while still approving `goal -> hypothesis` and
`goal -> cron`. A schema edit changed what agents may write, with no code
change — which is the thing this goal asked for.
<!-- THOUGHT:END -->