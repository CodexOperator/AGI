---
id: experiment:a00-a111bc47-done-body-shape
mint_id: 3fd04ed18e0a4ea4b8b1cc34d2c74a5b
type: experiment
parents:
  - hypothesis:a00-a111bc47-ff00ea
next_edges: []
title: Filling a hypothesis body under ## Hypothesis does not lift testable_claim at done
---
# experiment:a00-a111bc47-done-body-shape

## Experiment

Tested whether `node_writer.derive_required_from_body` — the step `cli.py
cmd_done` runs on every hypothesis to close `goal:s31`'s residual — lifts
`testable_claim` from the body shape the scaffold's own brief produces.

Set up a scratch project root mirroring the engine layout (`<root>/nodes/`,
`<root>/context/schemas` = a copy of the real `[hypothesis].md`), so
`required_fields` resolved `['id','type','mint_id','title','testable_claim']`
exactly as in production.

Command / inputs (scratch root `/tmp/tmp.kZVJ1mykwz`, real schemas):

```
required_fields(root, "hypothesis")            -> ['id','type','mint_id','title','testable_claim']
write_node(root, hypothesis, slug="scratch-kid", parents=["goal:s31"])  -> written
missing_required at birth                       -> ['testable_claim']      # goal:s31 residual, expected
# kid fills body exactly as BODY_PROMPTS["hypothesis"] asks = prose under ## Hypothesis
missing_required after body fill                -> ['testable_claim']
derive_required_from_body                       -> UNCHANGED "nothing derivable from the body"
missing_required after done path                -> ['testable_claim']
```

Actual output:

```
required: ['id', 'type', 'mint_id', 'title', 'testable_claim']
scaffold: written
at birth testable_claim present: False
missing at birth: ['testable_claim']
missing after body fill (before done): ['testable_claim']
derive status: unchanged nothing derivable from the body
after done  testable_claim present: False | value: None
still missing at done: ['testable_claim']
```

### Root cause

`_BODY_SECTIONS["testable_claim"] = ("testable claim", "claim")` and
`_section_text` matches only a Markdown heading whose stripped title equals one
of those literals. The scaffold's own prompt is `"## Hypothesis\n\nWhat is the
testable claim? ..."` — no instruction to open a `### Testable claim`
subheading — so a standard brief-following kid leaves its claim as a paragraph
under `## Hypothesis`, which `_section_text` does not match (returns `None`).
Direct unit check across shapes:

```
under ## Hypothesis        -> None
under ### Testable claim   -> 'The actual claim.'
Claim: line under ## Hyp.   -> None
```

### What this does NOT show

- Not a live dispatch through `cli.py` itself; it calls the identical
  `derive_required_from_body` step, which is the code under test.
- Not a claim that the lift is never useful — a body that opens a literal
  `### Testable claim` subheading IS lifted; the gap is the prose-under-
  `## Hypothesis` shape that the brief's own wording produces.

## Evidence

The console transcript above, reproduced from the scratch run; and the
`_section_text` matrix.