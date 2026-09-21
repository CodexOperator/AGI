---
id: hypothesis:a00-3416528c-c05b85
mint_id: f67f9471477b49b88c10a936828a39d0
type: hypothesis
parents:
  - goal:s34
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: d1e55eb6edcb4e4d
season: 1
thought_session: season
title: Verdict schema declares contradicts but corpus uses contrasts
verdict: inconclusive_lean_proved:85
---
# hypothesis:a00-3416528c-c05b85

## Hypothesis

The `[verdict].md` schema declares `contradicts: {type: list}` but the real verdict node corpus uses field name `contrasts` instead of `contradicts`. This naming drift means: (1) tools that read the schema (schema validation, node_writer.py scaffolds) look for `contradicts` and miss the actual data stored under `contrasts`; (2) a new verdict node minted from the scaffold or through a schema-aware writer writes the wrong field name; (3) cross-referencing between verdicts and their referenced nodes silently degrades.

**What would prove it:** A corpus scan of all 83+ verdict nodes shows a non-zero count of nodes using `contrasts` vs `contradicts`. A schema-validation pass against the corpus using the declared `contradicts` field reports violations for every node that uses `contrasts` instead — proving the schema does not match reality.

**What would disprove it:** All verdict nodes use `contradicts` and none use `contrasts`, OR the schema has been updated to match the corpus (either renamed to `contrasts` or aliased).

## Evidence

Survey of `nodes/verdict/` (159 files, L1.12):
- 10 nodes use `contradicts:` in frontmatter
- 7 nodes use `contrasts:` in frontmatter
- `chain-engine-r8-by-citation.md` explicitly documents the drift: "Caveat: the spec's field is `contradicts`; real verdict nodes use `contrasts`"
- The `[verdict].md` schema in `.agi/context/schemas/` declares only `contradicts: {type: list}`, with no alias or mention of `contrasts`
- Both field names are live in the corpus; neither is deprecated

## Resolution

Either the schema should be repaired to match the corpus (rename `contradicts` → `contrasts` in the schema, possibly adding a deprecated alias), or the corpus should be migrated to match the schema. The current state is drift — both names are in active use, with no bridge between them.


## Agent Notes
Row 12 from HANDOFF section 8: [verdict].md declares contradicts but 7/159 verdict corpus nodes use contrasts instead. Schema/corpus naming drift with no alias bridge.