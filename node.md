---
id: hypothesis:l2w1-ladder-node
mint_id: 706527cd0fb4426daec68dd7832f2dc5
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: c8973756e831b84a
season: 1
testable_claim: A [ladder].md schema and a .agi/nodes/.geometry/ladder.md node exist, validate against each other, and declare tiers 0 to 3, current_season 1, caps, budget, spawn profiles, read order by role, and director_rotate_at 0.35
thought_session: season
title: "L2 wave 1: l2w1-ladder-node"
---
# hypothesis:l2w1-ladder-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: .agi/context/schemas/[ladder].md (new) and .agi/nodes/.geometry/ladder.md (new). Model both on the existing pair [cron].md and .agi/nodes/.geometry/crons.md: same layout, same parenting move; check git log -- .agi/nodes/.geometry/crons.md for how that node was minted and mint ladder.md the same way, parented on goal:g12.3. Node fields: tiers, a list of four dicts with keys tier (int), plan_types (list), report_type (str, none for tier 3), judged_against (str), lens (str), cadence (str), exactly the four rows of the table in section 1; current_season: 1; caps: {moral: 5, vision: 3}; caps_apply_from_season: 2; budget_usd_week: 30; spawn_profiles: [fast, cheap, good, balanced]; read_order with keys kid, parent, director, prime_director from section 4.5; director_rotate_at: 0.35 (fraction of context used at which a director writes its handoff and rotates, section 6 Director rotation); zoom: numeric. Schema: validation.required covers id, type, mint_id, tiers, current_season, caps, director_rotate_at; types for each; spawn allowed_parents [goal], min_parents 1, max_parents 1. Node body: one line per tier and the invariants list from section 1 (measured at season close, never enforced as floors). VERIFY: links.py schema no new violations; links.py links 0 broken; the registry loads [ladder].md as an active type; commands.py run tests green; one new test that loads the ladder node through the engine's node reader and asserts current_season == 1 and director_rotate_at == 0.35. Sections 1, 4.5, 6. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md