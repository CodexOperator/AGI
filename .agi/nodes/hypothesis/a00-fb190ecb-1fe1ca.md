---
id: hypothesis:a00-fb190ecb-1fe1ca
mint_id: e059155d2d4f4cd2a4119ee1a99afa0b
type: hypothesis
parents:
  - goal:g7.31.2.2
next_edges: []
confidence: 0.9
edited_by: a00-fb190ecb
evidence_runs:
  - experiment:a00-fb190ecb-dh155-mur-verify
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 74c4e0f6c3193aea
season: 2
testable_claim: The four MUR residues the DH.45 round left on `goal:g7.31.2.2` — a false "inert" claim in `experiment:a00-33653715-dh45-verify`, two overclaimed closure summaries (`hypothesis:a00-33653715-0d018f`, `hypothesis:a00-3c0140ac-0fa4dd`), and a wrong `production_lines` metric — are closeable by edit/text correction alone, with no production code and no schema change.
title: "DH.155 four-residue corrective: false inert claim corrected, overclaimed closure summaries narrowed, production_lines set to 0"
town: core
verdict: inconclusive_lean_disproved:50
---
<!-- BODY:BEGIN -->
# hypothesis:a00-fb190ecb-1fe1ca

## Hypothesis

The four MUR residues the DH.45 round left on `goal:g7.31.2.2` — a false "inert"
claim in `experiment:a00-33653715-dh45-verify`, two overclaimed closure
summaries (`hypothesis:a00-33653715-0d018f`, `hypothesis:a00-3c0140ac-0fa4dd`),
and a wrong `production_lines` metric — are closeable by edit/text correction
alone, with no production code and no schema change.

The load-bearing claim is the first: `probes: list` in `[hypothesis].md`'s
`validation.types` is NOT inert. Through `schema_registry` it adds exactly four
`types:probes` errors on the live corpus (`a00-8ee9bdff`, `a00-bfd0d94a`,
`a00-debf9c6e`, `lm-typesafe-replay-200`); the earlier "inert" reading came from
`links.py schema`, which reads `required_fields` only and never sees
`validation.types`.

Prove by: the registry probe reading BEFORE 127 / AFTER 131 = 127 + 4
`types:probes`; `grep` finding no "is inert", no "all three residues closed" and
no "and inert" on the four corrected nodes; `production_lines: 0` on
`hypothesis:a00-f4f7eb39-a27b6a`; and the schema file unchanged. Disprove by any
of those checks failing.

## Agent Notes
Closed four DH.155 MUR residues on goal:g7.31.2.2: false 'inert' probe corrected to refused (schema_registry BEFORE 127 / AFTER 131 = +4 types:probes), two closure summaries narrowed to partial, production_lines set 0; THOUGHT blocks and schema untouched.
