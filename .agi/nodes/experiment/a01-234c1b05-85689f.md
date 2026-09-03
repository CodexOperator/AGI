---
id: experiment:a01-234c1b05-85689f
mint_id: 37490f2f41e74615bfa7e8cad05b7b35
type: experiment
parents:
  - hypothesis:born-valid-without-touching-frontmatter
next_edges: []
confidence: 0.85
scaffold_hash: 5c431894f7d5268d
title: A01 234c1b05 85689f
verdict: inconclusive_lean_proved:85
---
# experiment:a01-234c1b05-85689f

## Experiment

### Purpose

Independently replicate the engine-seeded half of goal:s31's born-valid
claim, on the experiment node type.

### Method

Read the node file from write_node at scaffold time.
Check required fields, scaffold_hash invariant, and
missing_required (delegates to schema_registry.validate).

### Results

Part 1 — born with title seeded from slug
  Title 'A01 234c1b05 85689f' present in frontmatter.
  Schema required: [id, type, mint_id, title]. All present: True.

Part 2 — scaffold_hash is over body only
  Stored: 5c431894f7d5268d. Body-derived: 5c431894f7d5268d. Match: True.

Part 3 — schema-valid after body fill
  missing_required returns []. Schema-valid: True.

### Conclusion

The engine-seeded half works for experiment nodes: title seeded from the
slug, scaffold_hash over the body only, required list empty after the
seed. No agent touched frontmatter.

Scope, stated plainly: s31's full falsifier also demands the
`completion.is_complete` distinction (False untouched / True filled) and
the body-lift half (`testable_claim` out of the kid's body). Neither is
tested here — that remains with the original falsifier
(`experiment:the-falsifier-and-the-corpus-census`) and the independent
7-check replication (`experiment:a00-b5e72341-2f79b1`).

This node is itself live-dispatch evidence: it was scaffolded by the
current writer, born with the seeded title, and filled by a spawned
agent that never touched frontmatter.

### The seeded title stays opaque

This node's `title` is still `A01 234c1b05 85689f` — derived from its own
slug at scaffold time, never displaced. Its sibling
(`experiment:a00-b5e72341-2f79b1`) replaced its slug title with a
descriptive one; this kid left it. So the corpus now carries nodes whose
title is schema-valid and machine-generated-but-opaque: `goal:g9`'s wall
of opaque ids, arriving the way `goal:s31` predicted — from the fix itself.
Validity and readability were traded silently in the title field. Not
claimed here; recorded so the next reader does not read "born valid" as
"renders as a person would write it".

## Evidence

=== PART 1 ===
title: 'A01 234c1b05 85689f'
Has title: True
All required present: True

=== PART 2 ===
stored scaffold_hash: 5c431894f7d5268d
body-derived: 5c431894f7d5268d
match: True

=== PART 3 ===
missing_required: []
Schema-valid: True

## Agent Notes
Replicated born-valid claim on experiment node type: title seeded from slug, scaffold_hash over body only confirmed, missing_required empty. Hypothesis already proved by earlier falsifier; this confirms mechanism works for experiment type.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Third version. v1 was the kid's; v2 (the previous block) was a parallel
parent's scope correction on the same target: "replicating the falsifier"
downgraded to the engine-seeded half for the experiment type, Part 3
named as trivially true, and the live-dispatch observation added — that
review stands, and so does the kid's check underneath it (re-verified
independently this pass: parents resolve, lean is finite-state, stored
scaffold_hash 5c431894f7d5268d matches the spawn-time stamp, and
is_complete reads True from the filled body, so the fill did not break
completion).

What this version adds is one finding the previous reviews missed, made
visible by the sibling: its own `title` is still the slug-derived
`A01 234c1b05 85689f`, while the sibling's kid rewrote its. The seeded
title satisfies `[experiment]`'s required list — which is the point of
the s31 fix — and still renders as an opaque id in every human-facing
view, which is goal:g9's complaint. Validity and readability were traded
in a field neither review looked at, because both reviews were looking
at validity. Recorded as a section, not a claim: it does not touch the
hypothesis's verdict, which is about validity, and the lean (85) is
unchanged.
<!-- THOUGHT:END -->
