---
id: experiment:a01-de655bfd-635cd0
mint_id: 1ae0d0e7e8d54d9fa1dfc27ffe8e77f5
type: experiment
parents:
  - hypothesis:a00-edae0fba-940d3a
next_edges: []
scaffold_hash: cf6c6014c5eb5e09
title: A01 de655bfd 635cd0
verdict: disproved
confidence: 0.85
evidence_runs:
  - experiment:a01-de655bfd-635cd0
---
# experiment:a01-de655bfd-635cd0

## Experiment

**Test:** Can `title` AND `testable_claim` both be seeded at scaffold time from dispatch context, making hypothesis nodes schema-valid at birth without breaking completion detection?

**Method:** Used `node_writer.write_node` to scaffold a hypothesis against a schema that requires `[id, type, mint_id, title, testable_claim]`, then checked:

1. Is `title` seeded from the slug?
2. Is `testable_claim` seeded at all? (dispatch context has neither the claim text nor any field it could derive from)
3. Is `completion.is_complete` returning False on untouched scaffold?
4. Does `derive_required_from_body` lift `testable_claim` from the body after the kid writes it?
5. Does frontmatter seeding affect `scaffold_hash`?

**Result:** The hypothesis is disproved for `testable_claim`. `title` IS seeded at scaffold time (from the slug), but `testable_claim` CANNOT be derived from dispatch context — the goal id and agent tag carry no claim content. The existing code correctly handles this:
  - `seed_required` seeds only `title` at scaffold time (a real human-readable value from the slug, never a placeholder)
  - `testable_claim` is reported as `missing_required` with a `SCHEMA-WARNING` on stderr
  - `derive_required_from_body` lifts `testable_claim` from the body after the kid writes it under `### Testable claim` heading
  - `scaffold_hash` hashes the BODY only, so frontmatter seeding does not affect completion detection

**The counterfactual the kid did not run, stated so a reader does not have to infer it:** if `node_writer` were changed to seed a fabricated `testable_claim` (the only value available at scaffold time), the required-field check would pass at birth — the schema checks presence, not truth. That is exactly the `TODO(model)` failure `goal:g2.10`'s 8,034 fields are the standing proof of, and the disproof clause of `hypothesis:born-valid-without-touching-frontmatter` ("any field filled with a placeholder"). The hypothesis is therefore dead as a buildable design: its antecedent has no real content source, and the only way to satisfy it invents the value, which converts a silent invalid node into a silent lie. That is the disproof; the mechanical fact behind it (dispatch context carries no claim text) is what this experiment verified.

## Evidence

Reconstruction of the check, with elided setup (`graph = ...  # temp .agi`,
helper scaffolds) — the values below were observed, the listing is not a
verbatim transcript:

```
$ python3 -c '
import tempfile, os, sys
sys.path.insert(0, "extensions/agi/bin")
sys.path.insert(0, "extensions/agi/src")

graph = ...  # temp .agi with [hypothesis].md requiring [id,type,mint_id,title,testable_claim]

res = node_writer.write_node(graph, "hypothesis", "my-testable-claim", parents=["goal:g1"], announce=False)
print(f"missing_required: {res.missing_required}")
print(f"title in file: {"title: My testable claim" in res.path.read_text()}")
print(f"testable_claim in file: {"testable_claim" in res.path.read_text()}")
print(f"is_complete(untouched): {completion.is_complete(graph, "hypothesis:my-testable-claim")}")

# Then kid writes body with testable claim
body = res.path.read_text().replace(
    "# hypothesis:my-testable-claim",
    "# hypothesis:my-testable-claim\n\n### Testable claim\n\nThe claim is seedable at scaffold time.\n")
res.path.write_text(body)
filled = node_writer.derive_required_from_body(graph, "hypothesis:my-testable-claim")
print(f"after derive: testable_claim lifted: {"testable_claim: The claim is seedable at scaffold time." in res.path.read_text()}")

# scaffold_hash unaffected by frontmatter
same_slug_bare = scaffold_without_title(graph_bare)
same_slug_full = scaffold_with_title(graph_full)
print(f"hashes match: {hash_of(bare) == hash_of(full)}")  # same slug -> same body -> same hash
'

Output:
missing_required: ['testable_claim']
title in file: True
testable_claim in file: False
is_complete(untouched): False
after derive: testable_claim lifted: True
hashes match: True
```


## Agent Notes
Hypothesis claims title+testable_claim both seedable at scaffold time from dispatch context. DISPROVED for testable_claim: dispatch context (goal id, agent tag) carries no claim text. title IS seeded from slug; testable_claim correctly deferred to derive_required_from_body after kid writes body; scaffold_hash unaffected (hashes body only).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the kid's first version. The disproof stands; the version
changed the confidence and added the two things the kid could not see from
inside its own run.

**Confidence 1.0 → 0.85.** The kid's evidence block is a reconstruction —
`graph = ...  # temp .agi` and undefined helpers — not a verbatim transcript,
and the one clause of the hypothesis it did NOT run (seed a fabricated claim
and watch the presence check pass) was left as a footnote. 1.0 is for a
mechanism that was observed to fail, and this one was observed not to be
buildable. The distinguishing fact — dispatch context carries no claim text —
was verified in code by the reviewer as well as by the kid: the dispatch
arguments are project, iteration, tier, target, and `BODY_PROMPTS['hypothesis']`
is three lines of prompt, none of it claim content. That is solid. What is
NOT solid is the counterfactual half, which the kid never executed, so the
confidence caps below it.

**The counterfactual paragraph is added to the body, not left to inference.**
A reader who took the hypothesis literally — "if the writer seeded both, the
required check passes at birth" — would find that the check DOES pass, because
it checks presence, not truth. The kid's disproved verdict and that tautology
only coexist if the reader understands the hypothesis as a buildable design
rather than a claim about the schema's grammar. The added paragraph states
the coexistence explicitly: dead as a design because the antecedent has no
content source, and the only satisfying implementation is a placeholder —
which is the failure the goal's own scar tissue exists to forbid.

**`evidence_runs` added to the frontmatter.** The gate ran correctly at
`cli.py done` time (the flag value resolved to this node, itself, which is
the one self-citation a run may make) and recorded the decision in the
manifest — but for an existing node the done path persists only `verdict` to
the file, so the evidence link was invisible to anyone zooming in on the
node. The original falsifier node carries its `evidence_runs` in the
frontmatter by the kid's own hand; this version matches that, because a
disproved verdict whose evidence no reader can find is a disproved verdict a
later parent has to re-litigate.

This closes the last open hypothesis under `goal:s31`: the three candidate
shapes are now all examined — seed (title only, by this node and the falsifier),
lift (the falsifier), report (the falsifier's stderr clause). Shape 1 for
non-derivable fields is dead, and the graph says so with a reason.
<!-- THOUGHT:END -->
