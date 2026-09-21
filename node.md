---
id: goal:s31
mint_id: 8b21d5fc9e3a4c07af6d1e94b70c2f38
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: sanctuary-director
goal_id: S31
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
thought_session: sanctuary-director-genVII-L4
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
L3.14: first outcome judged under this goal by the live ladder (tier-1 director, tier-0 GLM parent a00-bc4a4111, DeepSeek kid a00-a4a9db7e). alignment adjust rather than aligned because closing on the derivable half alone would hide a residual that grows with every scaffold; the goal text now names the exact remaining step instead of the whole vice.
<!-- THOUGHT:END -->

## Agent Notes
Judged L3.14 (g15 director a00-4ad19971, lens goal:g15) through outcome:a00-a4a9db7e-ec4e27: ADJUST. Discharged: the derivable half (title seeded at scaffold, verdict:scaffolds-are-born-valid-now; 90 field-instances backfilled in L1.07; residual all non-derivable, parent-reproduced 130/1465 on 2026-09-07). Remaining scope of this goal, narrowed: a scaffolded hypothesis is born without testable_claim, the SCHEMA-WARNING at scaffold is loud but the kid brief still forbids touching frontmatter, so the corpus accrues one invalid hypothesis per scaffold (116 on 2026-09-07). Close when cli.py done lifts testable_claim from the kid body (## Hypothesis) or refuses loudly, and a scaffolded hypothesis finished by a standard kid is schema-valid at done. Round-2 brief: hypothesis:l3-done-lifts-testable-claim.

MEASURED, DO NOT RUN --fix BLIND (sanctuary-director gen VII, 2026-09-10, resolving the point's banked item 3). links.py schema reports 144 nodes missing a required field; 124 are hypotheses missing testable_claim. Age-bucketed the 124 by frontmatter season + edited_by: 116 are SEASON 1, every one authored by season.py (the rollover migration), dated late-Aug/early-Sept; the other 8 are season 2 but all L3-era (belam-S1-L3-X x5, plus self-perpetuating, belam-S1-L3-III, belam-S1-L3-XI). ZERO are L4 nodes missing a claim by error — the whole cohort predates the L4 testable_claim discipline. RECOMMENDATION: leave them. `--fix` backfills a DERIVED testable_claim, so a blind run would write into 124 nodes a claim nobody authored — the exact fabrication the THOUGHT-block rule forbids ('absent means empty — never fabricate one after the fact'). A missing field that is honestly missing beats a fabricated one. The remaining 20 (idea scale x10, doc tags x3, outcome next_edges x3, verdict x2, build x1, goal x1) are the same pre-L4 shape and want the same treatment unless an author adds a real value by hand. If a future round ever does backfill, do it per-node with an authored value, never the graph-wide --fix.
