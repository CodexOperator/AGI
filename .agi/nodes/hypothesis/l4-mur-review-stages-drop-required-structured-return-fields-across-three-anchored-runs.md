---
id: hypothesis:l4-mur-review-stages-drop-required-structured-return-fields-across-three-anchored-runs
mint_id: 3f5c9eea58fa4ae49df348bdf677f1c5
type: hypothesis
parents:
  - goal:g6.20
next_edges: []
edited_by: belam
loop: hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 37c4c111079034de
season: 2
testable_claim: "\"The merge-up-review stages of three consecutive anchored mur runs (run key mur-core-season2-posts-sensei-director-main) each returned a structured result MISSING a different schema-required field, one per run and stage, with the wall/timeout NOT the cause: review:SM.107 returned no valid JSON at all, review:SM.108 was valid JSON missing `round`, review:SM.109 was valid JSON missing `verdict_recommendation`; verify:SM.107 and verify:SM.108 were valid JSON missing `verdicts`, and verify:SM.109 returned a fenced ```yaml block instead of JSON. Falsifier: any of those six stage results, re-read from the recorded run artifacts, is schema-valid or is explained by a wall/timeout rather than by model output drift.\""
thought_session: dissolve-legacy-2026-09-19
title: "Three anchored mur runs each dropped a different schema-required structured-return field: a model-output-reliability pattern, not a wall"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-mur-review-stages-drop-required-structured-return-fields-across-three-anchored-runs

## Hypothesis

The mur review/verify stages fail as MODEL OUTPUT RELIABILITY, not as walls:
across three consecutive anchored mur runs (`mur-core-season2-posts-sensei-
director-main`), every structured return was missing a DIFFERENT required
field, and no two runs missed the same one.

## Measured pattern (SM.114, parent brief, verbatim labels)

- `review:SM.107` — no valid JSON at all (no parseable object).
- `review:SM.108` — valid JSON missing `round`.
- `review:SM.109` — valid JSON missing `verdict_recommendation`.
- `verify:SM.107` — valid JSON missing `verdicts`.
- `verify:SM.108` — valid JSON missing `verdicts`.
- `verify:SM.109` — returned a ```yaml fenced block instead of JSON.

## Testable claim

Each of the six stage results above, re-read from the recorded run artifacts,
is (a) schema-invalid against the stage's declared `schema`, and (b) NOT
explained by a wall/timeout (the stage completed inside its resolved budget).
Prove by re-reading the six recorded results and running each through
`_resolve_lenient_return` / `links.py schema`-style validation with the stage's
own required list.

## Falsifier

Any one of the six results is schema-valid when re-read from the artifacts, or
is explained by the stage hitting its wall / a context-build failure rather than
by the model's own output shape — then the claim is not a model-reliability
pattern and this node is disproved.

## Why this is a separate node

Fixing output reliability (retry-on-schema-miss, prompt/schema simplification)
is a different defect from the SM.114 wall/timeout work and would conflate two
unrelated changes in one diff. This node preserves the finding; SM.114's
experiment deliberately does not fix it.
