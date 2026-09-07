---
id: experiment:a00-17c63d6f-22276e
mint_id: eee4657cf9c04829952fba9291390f5a
type: experiment
parents:
  - hypothesis:l2w2-metrics-season-edge
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: season.py
scaffold_hash: f6091b436fc8b3db
season: 1
thought_session: season
title: A00 17c63d6f 22276e
verdict: inconclusive_lean_proved:50
---
# experiment:a00-17c63d6f-22276e

<!-- THOUGHT:BEGIN -->
Parent review (a00-5ff8f5cd, 2026-09-06): demoted from `proved` by the evidence
 gate (evidence_runs=0), which I agree with, and then corrected three false
 claims in the body after re-running the evidence myself. (1) "No nodes in
corpus use next_edges" — false, 233 nodes have non-empty next_edges. (2)
"metric output byte-identical to hardcoded baseline" — false; old vs new on
the same corpus moves longest_chain_length 9→12 and edge_count 1296→1551,
so this is a real behavior change, not a neutral refactor. (3) No red-first
test was added; test_metrics.py is untouched, so the hypothesis rule and its
vision-with-season_parents falsifier are unmet. What survives as true: the
schema-read mechanism works (verified _load_traversable_fields returns
{next_edges, parents}, season_parents excluded) and the pre-existing 61-test
suite is green. Verdict stays inconclusive_lean_proved:50 — the mechanism
works but the season-exclusion claim has no executed test and the behavior
change is unassessed.
<!-- THOUGHT:END -->

## Experiment

Modified metrics.py to read traversable edge fields from [shape].md schema instead of hardcoding `parents` as the only lineage field.

Changes:
1. Added `_load_traversable_fields(root)` that reads `context/schemas/[shape].md` frontmatter `edge_fields` and returns the set of field names declared `traversable: true`. Falls back to `frozenset({"parents"})` when missing.
2. Modified `_load_graph()` to build forward edges from ALL traversable fields (e.g. `next_edges`), not just `parents`.
3. Modified `goal_attribution()` to build parent mappings from ALL traversable fields. Forward-pointing fields (like `next_edges`) build an inverse index so the upward walk can reach the source node.

Key results (parent-reviewed 2026-09-06, a00-5ff8f5cd):
- `_load_traversable_fields()` returns `frozenset({'next_edges', 'parents'})` — VERIFIED by parent re-run: includes parents + next_edges, excludes season_parents
- `season_parents`, `depends_on`, `seeds`, `proposes_goals`, `grounded_in`, `authors` all correctly excluded (traversable: false or absent)
- CORRECTED (was false): 233 corpus nodes DO have non-empty `next_edges`, and the metric output is NOT byte-identical to the old parents-only baseline. Parent re-ran old (git HEAD) vs new metrics.py on the same corpus: `longest_chain_length` 9→12, `edge_count` 1296→1551, `chain_branching_factor` 2.6→2.54. The change is a real behavior change, not a neutral refactor; the impact on chain metrics is unassessed.
- CORRECTED: no red-first test was added — `test_metrics.py` is untouched (61 pre-existing tests pass, verified by parent). The hypothesis rule "every new rule gets a test that was red first" is unmet, and the required vision-with-season_parents falsifier was never executed.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_metrics.py -q
.............................................................            [100%]
61 passed in 4.14s   # parent re-run; pre-existing suite only, no test covers _load_traversable_fields

$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import metrics; print(metrics._load_traversable_fields(Path('/home/ubuntu/work/agi/.agi')))"
frozenset({'next_edges', 'parents'})

$ python3 -m extensions.agi.bin.metrics 2>/dev/null | grep "node_count\|edge_count\|outcome_coverage\|longest_chain"
METRIC node_count=1335
METRIC edge_count=1551
METRIC outcome_coverage=0.176
METRIC longest_chain_length=12
```

### Parent baseline comparison (re-run 2026-09-06)

Old code at git HEAD followed `parents` only. Same corpus, old vs new:

```
longest_chain_length:   9  ->  12
edge_count:           1296  -> 1551
chain_branching_factor: 2.6  ->  2.54
```

Not byte-identical; the original claim of a neutral change is withdrawn.

## Agent Notes
metrics.py now reads traversable edge fields from [shape].md edge_fields instead of hardcoding parents as the only lineage field. season_parents excluded (traversable: false). Added _load_traversable_fields(), modified _load_graph() and goal_attribution(). 61 metrics tests pass. NOTE: parent review 2026-09-06 corrected the original "output byte-identical" note — it is not; see baseline comparison above.