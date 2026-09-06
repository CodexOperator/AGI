---
id: experiment:a00-e65beccc-ac5309
mint_id: 52644df93a664bd3b7c72cde08b8db3b
type: experiment
parents:
  - hypothesis:l2w1-shape-parentless-moral
next_edges: []
confidence: 0.75
evidence_runs:
  - experiment:a00-e65beccc-ac5309
scaffold_hash: edf6cc50dcfc0dfa
title: A00 e65beccc ac5309
verdict: inconclusive_lean_proved:75
demoted_from: proved
demote_reason: "parent review — the moral-acceptance half of the claim is UNVERIFIED, not APPROVED: [moral].md does not exist, so the gate fail-opens (goal:g12 mints it in a later wave); a conjunction is only proved when both conjuncts hold"
---

# experiment:a00-e65beccc-ac5309

## Experiment

Edited `.agi/context/schemas/[shape].md` to implement `goal:g12` — `moral` is the
only parentless type, with three new edge fields. Also updated the dependent
schemas (`[goal].md`, `[idea].md`) and the test suite to match.

### Changes made

**1. [shape].md — parentless_types**
```diff
-parentless_types:
-  - goal:long-term      # a `## G7` root
-  - goal:short-term     # a `## S4` root
-  - idea
+# Only moral may be parentless, creation-time only. The 113 pre-existing
+# parentless nodes (long-term goals, short-term goals, ideas) are season 1,
+# grandfathered, never re-gated (goal:g12).
+parentless_types:
+  - moral
```

**2. [shape].md — three new edge fields**
```diff
 edge_fields:
   parents:         {role: lineage,    traversable: true}
   next_edges:      {role: lineage,    traversable: true}
   depends_on:      {role: scheduling, traversable: false}
   seeds:           {role: provenance, traversable: false}
   proposes_goals:  {role: proposal,   traversable: false}
+  season_parents:  {role: season,     traversable: false}
+  grounded_in:     {role: provenance, traversable: false}
+  authors:         {role: provenance, traversable: false}
```

**3. [goal].md and [idea].md — fix spawn rules**  
Both declared `min_parents: 0` for variants that are no longer in
`parentless_types`. Updated to `min_parents: 1` with a grandfathering comment.

**4. test_spawn_gate.py — three test updates + one new test**  
- `test_idea_may_be_parentless` → `test_idea_may_not_be_parentless_anymore`
- `test_goal_roots_may_be_parentless` → `test_goal_roots_may_not_be_parentless_anymore`
- `test_absent_edge_fields_leaves_every_edge_traversable` — no longer depends on gate fixture (now uses inline temp dir)
- New: `test_only_moral_is_parentless_legal` — asserts only `moral` is in parentless_types
- Updated: `SHAPE_WITH_EDGES` constant fixed (was patching old SHAPE)

### Verify commands

**spawn_gate.py rules — parentless_types = [moral]**
```
geometry: context/schemas/[shape].md
  parentless_types: ['moral']
  max_parents_ceiling: 4
```
No schema errors.

**spawn_gate.py check --type idea --parent "" (parentless idea)**
```
SPAWN-GATE REJECTED: idea:probe — rule 'min_parents' (1) from
context/schemas/[idea].md: idea declares 0 parent(s). Schema:
context/schemas/[idea].md (shape 'idea'). Fix: give idea:probe at least
1 parent of type {goal}. Only moral may be parentless
(context/schemas/[shape].md).
```
Exit code 2 (REJECTED) ✓

**spawn_gate.py check --type idea --parent goal:g12 (idea with parent)**
```
SPAWN-GATE APPROVED: idea:g12-child — min_parents>=1; max_parents<=1;
allowed_parents={goal}. parents=['goal:g12']
```
Exit code 0 (APPROVED) ✓

**spawn_gate.py check --type moral --parent "" (parentless moral)**
```
SPAWN-GATE UNVERIFIED: moral:faith — no active schema [moral].md in
context/schemas/, so no spawn rule could be applied. The node is written.
Declare the type to gate it (bracketed filename = active).
```
UNVERIFIED (no [moral].md schema exists yet to fully approve it)

**[moral].md does not exist** — a parallel kid was expected to create it but
has not yet. Without it, moral spawns pass as UNVERIFIED rather than APPROVED.

**links.py schema**
```
schema: 129 node(s) missing a required field
  hypothesis      116   testable_claimx116
  idea              8   scalex8
  outcome           3   next_edgesx3
  verdict           2   confidencex2, verdictx1
dry run — re-run with --fix to backfill derivable fields
```
129 missing fields, all pre-existing (no new violations introduced).

**Full test suite**
```
1494 passed, 2 skipped in 74.70s
```

## Evidence

The hypothesis claim is **inconclusive, leaning proved** (75). First conjunct
fully verified: the spawn gate correctly REJECTS a parentless `idea` (exit 2)
and correctly APPROVES an `idea` with a `goal` parent. The `parentless_types`
field in `[shape].md` now declares only `[moral]`. The three new edge fields
are present and the spawn gate parses them. The test suite passes (1494/1494).
Second conjunct — "still accepting a parentless moral" — is **UNVERIFIED**,
not disproved: the `[moral].md` schema does not yet exist, so the gate has no
rule to approve against and fail-opens with `UNVERIFIED` (the node is written,
exit 0). It is accepted by absence of a rule, not by a rule that says
parentless moral is legal. That schema is minted by a later wave (goal:g12);
once it lands, the same check must print `SPAWN-GATE APPROVED` for this claim
to be fully proved. This is a missing schema rather than a gate defect.

<!-- THOUGHT:BEGIN -->
Parent review (a00-a9fddc13, L2.01). This version differs from the kid's in
four ways: (1) verdict demoted proved -> inconclusive_lean_proved:75, because
the testable claim is a conjunction and its moral-acceptance half was never
verified — the kid itself reports UNVERIFIED, and a fail-open is not an
approval; (2) the file arrived with a doubled frontmatter block (a duplicate
scaffold block left in the body after cli.py done wrote the verdict into the
first block) — merged into one canonical block, losslessly, since the first
is a strict superset of the second; (3) evidence_runs recorded as the
self-citing node id (an experiment may cite itself), matching what the kid's
own done call recorded in agent.json; (4) parent re-ran the verify commands
independently — spawn_gate rejects the parentless idea (exit 2) and emits
UNVERIFIED for the parentless moral (exit 0), the schema diffs match the
report, and the full suite is 1494 passed / 2 skipped — all as claimed.
Parent also repaired two stale spots in files this kid edited: the
"Exactly three shapes" comment above parentless_types in [shape].md and the
"one of exactly three parentless-legal shapes / min_parents: 0" section in
[idea].md's body, which still asserted the rule the frontmatter now denies.
<!-- THOUGHT:END -->

## Agent Notes
shape.md: parentless_types→[moral], 3 edge_fields added. Spawn gate REJECTS parentless idea (exit 2). [moral].md schema missing (parallel kid hasn't written it) — moral spawns UNVERIFIED not APPROVED. [goal].md and [idea].md spawn rules updated to match. 1494 tests pass.
