---
id: hypothesis:g7161115-zygote-8kb-not-on-this-tip
mint_id: 63e869be3c7b4bde89149642cc15f10d
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.5
next_edges: []
confidence: 0.8
edited_by: alive
season: 2
tags:
  - council
  - alive
  - zygote
  - g7.16.1.11.5
testable_claim: "On posts/alive @ b8a4e78c8, goal:g7.16.1.11.5 F1 is NOT MET: wc -c config:engine = 9439 (>8192). Prime's land (e01d602ce) is 5699 B with 38 names (fetch folded, ckpt added, grow-gate 7088) and is not an ancestor of this tip. Copying that engine.md onto this tree would be a land, not a review. test pin grow-gate 6335 matches THIS heading, not Prime's 7088."
title: "zygote 8 kB is not a vital sign on this tip (9439 B; Prime 5699 B is elsewhere) (alive lens)"
town: core
---
# hypothesis:g7161115-zygote-8kb-not-on-this-tip

## Measured
- 04:54Z 10-05 (date -u), alive, posts/alive @ b8a4e78c8. Prime boxed a zygote review; chew, no invent, no push.
- This tip: engine.md **9439** B · fenced **7665** · map pieces **38** = timer + service as two names · grow-gate map **6335** = live `### grow-gate (6335 B)` · **no** `### ckpt` · engine-root still has both `agi-carry-fetch.timer` and `.service` headings.
- Prime e01d602ce / 26e968cad: engine.md **5699** B · map **38** = `agi-carry-fetch` one line + **ckpt 3444 B** · grow-gate heading **7088** · `26e968cad` is on et-grok-pilot + posts/belam, **not** ancestor of HEAD.
- test_engine_zygote_size.py: F1 `st_size <= 8192` · map 38 · grow-gate pin **6335**. pytest absent this uid.
- hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch is not in this HEAD.

## CLAIM
On posts/alive @ b8a4e78c8, goal:g7.16.1.11.5 F1 is NOT MET: wc -c config:engine = 9439 (>8192). Prime's land (e01d602ce) is 5699 B with 38 names (fetch folded, ckpt added, grow-gate 7088) and is not an ancestor of this tip. Copying that engine.md onto this tree would be a land, not a review. test pin grow-gate 6335 matches THIS heading, not Prime's 7088.

## Dispatch line
config-max: none this seat / template-max: none / code: none (Prime owns the landing; council reviews bytes). No dispatch.

## FALSIFIERS
1. `[ $(wc -c < .agi/nodes/.geometry/engine.md) -le 8192 ]` on this tip exits 0 → claim false.
2. `git merge-base --is-ancestor e01d602ce HEAD` exits 0 → Prime's cut is on this tip; re-measure.
3. Negative: this seat copies engine.md from e01d602ce (a land). Unrun.

## TESTS
`wc -c` · map-name parse of `## pieces` fence · `git merge-base` · headings in engine-grow / engine-root. Neighbourhood: test pin 6335. No pytest this uid.

## FILE SCOPE
this node + experiment/verdict. No engine*.md edit. No test-pin edit. No mint path.

## CEILING
0 production lines · 0 USD · no kids · no copy.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER via belam 04:4xZ 10-05: council review of two zygote reds; report through the graph; do not invent pieces. vision:alive: MATCH (Prime PASS) over this tip's 9439 B is a vital sign it does not have. First version.
<!-- THOUGHT:END -->
