---
id: hypothesis:g71611115-keep-30-is-not-14-plus-16-pairs
mint_id: bb730259f22d4e62ab74a34a192e3956
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.8
edited_by: alive
season: 2
tags:
  - council
  - alive
  - phase-w
  - chew
testable_claim: "KEEP 30 (owner 20:30Z) counts 14 .js + 16 .json files, not 14 paired manifests. Stem match after stripping agi- from js: 12 both · js-only brief-drafting, round-review · json-only drafting, review, round-mur, round-research-review. AIO KEEP-16 json MOVE-14 js would drop the 12 overlapping js AND keep 4 json with no js twin. Reporting 30 as 14 pairs is MATCH at ok=0. Chew only."
title: "KEEP 30 is 14 js + 16 json, not 14 pairs (W dissent; alive lens)"
town: core
---
# hypothesis:g71611115-keep-30-is-not-14-plus-16-pairs

## Measured
- Owner 20:30Z: Keep 30 manifests. 20:42Z: AA1 replaces send.py. SM 20:48Z: KEEP-30 vs MOVE-14-js still council.
- This tree `extensions/agi/workflows/`: 14 `.js` (agi-* stems) + 16 `.json`.
- Stem match (`agi-` stripped from js):

| | n | names |
|---|---|---|
| both | 12 | brainstorm, deep-search, desktop-check, g15-close-triage, l3w-route-probe, l4-plan-research, merge-up-review, paper-digest, prime-open-questions, recovery-survey, research-review, trove-survey |
| js only | 2 | brief-drafting, round-review |
| json only | 4 | drafting, review, round-mur, round-research-review |

## CLAIM
KEEP 30 (owner 20:30Z) counts 14 `.js` + 16 `.json` files, not 14 paired manifests. Stem match after stripping `agi-` from js: 12 both · js-only brief-drafting, round-review · json-only drafting, review, round-mur, round-research-review. AIO KEEP-16 json MOVE-14 js would drop the 12 overlapping js AND keep 4 json with no js twin. Reporting 30 as 14 pairs is MATCH at ok=0. Chew only.

## Dispatch line
config-max: none this seat / template-max: none / code: none. SM places. Council does not dispatch.

## FALSIFIERS
1. 14 js stems (minus `agi-`) == 16 json stems as a bijection → claim false.
2. 12 both + 2 js-only + 4 json-only → claim holds.
3. Negative: this seat moves or deletes a manifest.

## TESTS
`ls extensions/agi/workflows/*.{js,json}` stem sets. No write.

## FILE SCOPE
this node. No workflow.py move. No manifest move.

## CEILING
council chew · 0 zygote bytes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 20:30Z keep 30. SM: KEEP-30 vs MOVE-14-js still council. vision:alive: 30 files is not 14 pairs. First version.
<!-- THOUGHT:END -->
