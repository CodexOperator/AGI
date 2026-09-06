---
id: goal:s31
mint_id: 8b21d5fc9e3a4c07af6d1e94b70c2f38
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S31
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S31: A scaffolded node ships schema-invalid, and the brief forbids the kid from fixing it"
---
**Found by a parent, in its `struggles:` line, on the 2026-09-02 iteration-103
run. Fifth time this session that field beat the review it came attached to.**
Quoted verbatim:

> scaffold omits the schema-required title+testable_claim, and the kid was told
> to leave frontmatter alone, so scaffolded hypotheses ship malformed until a
> parent backfills

Confirmed in two commands. `.agi/context/schemas/[hypothesis].md` declares:

```
required: [id, type, mint_id, title, testable_claim]
```

and `node_writer.py` seeds neither `title` nor `testable_claim`. Every
hypothesis this loop has ever scaffolded is therefore **born violating its own
schema**. Iteration 102's two nodes carry `id`, `mint_id`, `type`, `parents`,
`scaffold_hash`, `verdict`, `confidence` — and no `title`.

## The vice, and it is a vice rather than a bug

Two rules that are individually correct compose into a contradiction:

1. **The scaffold owns frontmatter.** `node_writer.write_node` is the one gated
   write routine, and it stamps `scaffold_hash` so `completion.is_complete` can
   tell a filled node from an untouched one.
2. **The kid is told to leave frontmatter alone** — correctly, because a kid
   editing `scaffold_hash` would break the completion check that decides
   whether it finished.

So the field is required, the writer does not supply it, and the one agent
holding the content is forbidden from adding it. **The node cannot become valid
by anyone doing their job as briefed.** It becomes valid only when a parent
notices and backfills — which is unbriefed, unenforced, and happened once,
because one parent was attentive enough to check the schema.

## Why it matters beyond tidiness

**`title` is what every human-facing renderer reads.** `snapshot-goals.py`,
`dashboard.py` and the injected map all key on it. A corpus where most
hypotheses have no title is a corpus that renders as a wall of opaque ids —
which is `goal:g9`'s complaint, arriving from a direction G9 never looked.
`goal:g9.7` makes it sharper: the view a human tunes is the view an agent is
handed, so a missing title degrades *both* readers at once.

**And it is silent.** Nothing validates a node against its schema at write
time. `spawn_gate` enforces `parent_shapes` at creation; no equivalent
enforces `required`. The corpus has been accumulating invalid nodes with no
signal, which is the `goal:g7` failure mode (nothing silently lost) wearing a
different hat: nothing is lost, something is silently *never valid*.

## What the fix has to respect

**Do not solve it by telling kids to write frontmatter.** That re-opens the
`scaffold_hash` hazard rule 2 exists to prevent, and swaps a silent invalid
node for a silently broken completion check — a strictly worse trade.

The candidate shapes, undecided and deliberately left so:

- **Seed the required fields at scaffold time** from what dispatch already
  knows (target, tier, goal), leaving a placeholder the kid's body content
  displaces. Cheapest, and it puts the field where the schema says it belongs.
- **Let the write path derive `title` from the body's first heading** on
  completion, so the kid supplies it without touching frontmatter.
- **Validate `required` at write time and fail loudly**, which fixes nothing by
  itself but converts a silent defect into a visible one.

The first two are `goal:g13`'s territory — one write path that knows what a
node type requires — and this goal should be settled *inside* that work rather
than patched ahead of it, because a patch here is one more caller agreeing by
convention with a schema it does not read.

## Falsifier

Scaffold a hypothesis through the normal dispatch path and validate the
resulting file against `[hypothesis].md`'s `required` list with no parent
intervention. It passes. Then confirm `completion.is_complete` still
distinguishes the untouched scaffold from a filled one — the fix must not buy
validity with the completion check.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 by the director from a parent's `struggles:` line, in the
same session and by the same route as `goal:s27` and `goal:s28`. That route is
now the most productive defect-finding channel this project has, and it keeps
working for the same reason: the agent that hit the problem describes it in one
line, and the review that follows is looking at the artefact rather than at the
experience of producing it.

Filed `active` rather than `horizon` because it is a live corpus defect, not a
future concern — nodes are being written invalid right now, on every iteration.
But deliberately **not** scheduled ahead of `goal:g13`. The honest fix is one
write path that reads the schema's `required` list, which is precisely what
g13's `write.py` is for; patching `node_writer` first would add a tenth caller
that agrees with the schema by convention, in the exact session convened to
delete the other nine.

The "do not solve it by telling kids to write frontmatter" paragraph is the
load-bearing one. It is the obvious fix, it is wrong, and the reason it is
wrong (`scaffold_hash` is how completion is detected) is not visible from where
someone would be standing when they proposed it.
<!-- THOUGHT:END -->