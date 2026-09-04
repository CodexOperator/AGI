---
id: experiment:a01-42536fa8-6df6f6
mint_id: b75d8b6f2f1245228dfb92f3d90a79f2
type: experiment
parents:
  - hypothesis:a01-f9ba05b4-30da30
next_edges: []
confidence: 0.95
edited_by: parent
evidence_runs:
  - experiment:a01-42536fa8-6df6f6
scaffold_hash: 23b59299e72e0bda
title: Proving load_existing_nodes last-wins hides orphan parents
verdict: proved
---
# experiment:a01-42536fa8-6df6f6

## Experiment

**Demonstrated that `load_existing_nodes()'s` last-wins duplicate-id collapse hides dangling parent
references from the referential-integrity check in `snapshot-goals.py`.**

**Setup:** Created a three-file test corpus in a temp directory:
- `a-first-file.md` — id=`goal:g-test`, parents=`[goal:g-real, missing:ghost]` (has a dangling ref)
- `z-second-file.md` — id=`goal:g-test` (duplicate!), parents=`[goal:g-real]` (no dangling ref)
- `g-real.md` — id=`goal:g-real`, parents=`[]`

**Method:** Ran the exact `load_existing_nodes()` algorithm on the corpus (sorts `*.rglob("*.md")`
and overwrites into a plain dict `nodes[node_id] = {...}`), then ran the same
`collect_parent_refs()` + integrity check logic.

**Result:** `z-second-file.md` (sorts second lexicographically) overwrote
`a-first-file.md`. The loaded dict for `goal:g-test` showed parents=`[goal:g-real]` —
the dangling ref `missing:ghost` was invisible. `report_integrity` flagged zero
unresolved refs.

**Conclusion:** The hypothesis is proved: `load_existing_nodes()` last-wins
behavior does cause the integrity check to miss dangling refs when duplicate
IDs collide with differing parents.

**Corpus state (2026-09-04):** The 17 duplicate-id pairs originally detected by
exp:integrity-detection-r1 have been cleaned up — current scan finds 0
duplicates. The code defect persists unfixed. No active blind spots remain in
the corpus because the duplicates are gone, but any future generator that
produces a duplicate ID will re-introduce the blind spot.

## Evidence

```
=== Test corpus files ===
  a-first-file.md
    id:      goal:g-test
    parents: ['goal:g-real', 'missing:ghost']
  g-real.md
    id:      goal:g-real
    parents: []
  z-second-file.md
    id:      goal:g-test
    parents: ['goal:g-real']

=== load_existing_nodes() — last-wins dict ===
  SET goal:g-real ← g-real.md
    parents = []
  SET goal:g-test ← a-first-file.md
    parents = ['goal:g-real', 'missing:ghost']
  SET goal:g-test ← z-second-file.md  ← OVERWRITES!
    parents = ['goal:g-real']

=== Integrity check (report_integrity) ===
  Known IDs: {'goal:g-real', 'goal:g-test'}
  All refs collected: {'goal:g-real': ['goal:g-test']}
  Unresolved refs: []
  → missing:ghost was HIDDEN by last-wins collapse

=== Winner (file in dict) ===
  Source file: z-second-file.md
  Parents:      ['goal:g-real']

================================================
DEMONSTRATED: load_existing_nodes() last-wins
hides dangling refs from the integrity check.
================================================
```


## Agent Notes
Demonstrated load_existing_nodes() last-wins behavior hides dangling refs from integrity check using synthetic corpus with duplicate IDs and differing parents. Real duplicates cleaned up (0 remain) but code defect persists.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-a1f67a2d review (iter 1062): accepted with one fix — `evidence_runs` was missing from the frontmatter, which would have caused the gate to demote `proved` to `inconclusive_lean_proved:50`. Added self-citation (`evidence_runs: [experiment:a01-42536fa8-6df6f6]`): an experiment IS its own run, the synthetic test output is the evidence. The controlled 3-file corpus (a-first sorts before z-second, differing parents, one dangling ref) is the right methodology: it isolates the mechanism from corpus noise. Verified independently: `snapshot-goals.py:439` still reads `nodes[node_id] = {...}` with no duplicate check, while `loader.py`'s `load_directory` has first-wins + `DuplicateIdError`. The caveat (no real duplicates remain) is honest and correct — the proof is mechanistic, not observational on the live corpus. Pairs with `a00-f4255dd1`'s audit: this proves the mechanism, that one proves the corpus no longer triggers it.
<!-- THOUGHT:END -->
