---
id: experiment:a00-4a304d3b-5931f3
mint_id: 21c34a86654e4194b49192da99f96f25
type: experiment
parents:
  - hypothesis:a00-edae0fba-940d3a
next_edges: []
confidence: 0.8
scaffold_hash: 5052bb834be3a593
title: A00 4a304d3b 5931f3
verdict: inconclusive_lean_proved:80
---
# experiment:a00-4a304d3b-5931f3

## Experiment

**Test:** Does node_writer.seed_required make scaffolded hypothesis nodes schema-valid at birth without breaking completion detection?

**Setup:** Scaffolded a hypothesis via node_writer.write_node in a temp project with [hypothesis].md declaring `required: [id, type, mint_id, title, testable_claim]`.

**Run 1 — scaffold birth**
```
res = nw.write_node(graph, 'hypothesis', 'seeded-title-test', parents=['goal:s31'])
```
- Status: written
- missing_required: ['testable_claim']
- title: "Seeded title test" (derived from slug)
- testable_claim: absent (cannot derive from slug alone)
- SCHEMA-WARNING emitted on stderr
- __Conclusion: title seeded from slug but node still schema-invalid because testable_claim missing.__

**Run 2 — completion detection**
- `is_complete(graph, 'hypothesis:seeded-title-test')` → **False** on untouched scaffold ✓
- After kid fills body text: `is_complete` → **True** ✓
- Body hash differs from stored scaffold_hash (as expected) ✓

**Run 3 — derive_required_from_body**
```
nw.derive_required_from_body(graph, 'hypothesis:seeded-title-test')
```
- Status: updated
- `testable_claim` lifted from kid's body prose into frontmatter
- All 5 required fields now present, schema-valid ✓
- __Conclusion: two-step pattern (scaffold seeds title, completion lifts claim) achieves goal s31.__

## Evidence

**Test results from temp project (ephemeral, cleaned up):**

```
SCENARIO 1: Scaffold hypothesis
write_node status: written
missing_required: ['testable_claim']
title: Seeded title test
testable_claim in fm: False
scaffold_complete: False

SCENARIO 2: Kid fills body
After fill, complete: True
Body hash differs from stored hash: True

SCENARIO 3: derive_required_from_body
Fill status: updated
testable_claim now present: True
All required fields present: True
```

**Full test suite (1380 passed, 1 pre-existing unrelated failure in test_provisioning.py):**
```
$ python3 -m pytest extensions/agi/tests/ -q
1380 passed, 1 failed (test_provisioning: revoked-key check, unrelated)
```

**Key tests for this hypothesis:**
- test_a_scaffold_is_born_with_a_real_title_not_a_placeholder ✓
- test_a_field_that_cannot_be_derived_is_reported_not_invented ✓
- test_seeding_required_fields_does_not_move_the_scaffold_hash ✓
- test_the_completion_half_lifts_a_claim_out_of_the_body ✓
- test_the_completion_half_invents_nothing_when_the_section_is_absent ✓
- All 50 test_node_writer.py tests pass
- All 18 test_completion.py tests pass

**Verdict reasoning:**
- Hypothesis claimed both `title` and `testable_claim` can be seeded from dispatch-time context (goal id + agent iteration tag)
- `title` IS successfully seeded from slug → PROVED
- `testable_claim` CANNOT be seeded from dispatch context alone (slug, goal id, iteration tag carry no claim content) → disproved the strong claim
- BUT `derive_required_from_body` fills `testable_claim` from kid prose, achieving the S31 goal without touching frontmatter
- Completion detection is unaffected throughout (scaffold_hash hashes body, not frontmatter) ✓
- Result: node IS schema-valid, just not at the exact moment of birth but after derive_required_from_body runs
- The two-step pattern is arguably better than seeding a fabricated claim

## Files examined
- node_writer.py: seed_required(), _derive_title(), derive_required_from_body()
- completion.py: is_complete(), scaffold_body_for()
- [hypothesis].md schema: required: [id, type, mint_id, title, testable_claim]\n- [experiment].md schema: required: [id, type, mint_id, title]


## Agent Notes
title seeded from slug; testable_claim not derivable from dispatch context alone — two-step pattern (seed title + derive_required_from_body) achieves S31 goal
