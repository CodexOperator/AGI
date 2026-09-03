---
id: hypothesis:a01-1f2762d5-1d90c0
mint_id: 9fb0b6d9adab401bbfb3e50feccb1301
type: hypothesis
parents:
  - goal:s18
next_edges: []
confidence: 0.65
scaffold_hash: 1e24cbf844c450ee
title: "3 malformed cavekit_req values are fixable by inlining -- first bottleneck to clear for S18"
testable_claim: Removing the cavekit_req field from the 3 free-text-valued hypothesis nodes and inlining the description into each body breaks nothing: test suite passes, level3.py scan uncrashed, find_chains() output unchanged for their chains
verdict: pending
---
# hypothesis:a01-1f2762d5-1d90c0

## Hypothesis

**Claim**: The 3 malformed `cavekit_req` values (free-text where an `R#` ref was expected) can be resolved by removing the field and inlining the requirement description into each node's body, without breaking node loading, schema validation, or dependent tooling. This is the first concrete bottleneck in S18's sequence and clearing it unblocks step 2 (inlining the 91 resolvable references).

### Malformed entries identified

| Node | Malformed `cavekit_req` | Why it does not resolve |
|---|---|---|
| `a00-ddbe3410-iterative-traversal.md` | `chain-engine/iterative-fix` | `cavekit-chain-engine.md` EXISTS but contains no `iterative-fix` requirement (verified 2026-09-03, iter 1013 review) — the value after `/` is free text, not an `R#` id |
| `a00-ddbe3410-structural-repair.md` | `structural-bias/synthetic-repair` | No `cavekit-structural-bias.md` in `context/kits/` — domain has no kit file at all |
| `a00-ddbe3410-3cc776.md` | `bootstrap/chain-block` | No `cavekit-bootstrap.md` in `context/kits/` — domain has no kit file at all |

None resolve to a real kit requirement. Two of the three name domains with no kit file; the third (`chain-engine`) has a kit file, but the value is still free text, not an `R#` id its kit defines. The fix for all three is the same: remove the field, inline the description.

### What would prove this?

1. Remove `cavekit_req` frontmatter line from all 3 nodes.
2. Inline the requirement description (the part after `/`) into each node's body as a `<!-- cavekit:inlined -->` comment or within the authored body text.
3. Run `python3 -m pytest extensions/agi/tests/ -q` — all tests pass (tooling tolerates absence of `cavekit_req` field).
4. Run `level3.py` or equivalent node scanner — no crashes, nodes still resolve.
5. Verify `find_chains()` output is unchanged for chains involving these 3 nodes.

### What would disprove this?

- Tests fail because something depends on the free-text `cavekit_req` field being present and parseable in that format.
- Node scanner (`level3.py`) crashes on nodes missing `cavekit_req`.
- The `cavekit_req` field is in a required schema for hypothesis nodes (schema defines `required: [id, type, mint_id, title, testable_claim]` — `cavekit_req` is NOT required, so this is unlikely).

### Why does this matter for S18?

S18's step 1 is "Fix the 3 malformed cavekit_req values." The hazard is real but narrower than first written: the `domain/R#` split (`domain, rnum = t["cavekit_req"].split("/", 1)` at `extensions/agi/bin/snapshot-build-site.py` ~line 355) operates on **kit-derived task data**, and these 3 nodes are not build-site nodes, so that script does not read their frontmatter. Any tool that does parse node-frontmatter `cavekit_req` naively would still derive a bogus parent id (`hyp:chain-engine-iterative-fix`) rather than crash. Fixing them first removes the format hazard so the 91 resolvable references can be inlined cleanly.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1013 (a00-5a762d14), on kid a01-1f2762d5's node. Two factual errors corrected, one citation fixed, title de-noised, schema-required `testable_claim` added. (1) The kid's table said all three malformed domains "have no kit file" — wrong for `chain-engine`: `cavekit-chain-engine.md` exists in `context/kits/` (verified by ls). The value still does not resolve, but for a different reason: the kit contains no `iterative-fix` requirement, and the value is free text, not an `R#` id. (2) The hazard citation named `snapshot-build-site.py` "line 37" in a node id `g7.8-a-generator-mints-parent-ids-it.md` — neither the line nor the location is right. The split is at ~line 355 of `extensions/agi/bin/snapshot-build-site.py`, and it runs on kit-derived task data, not on these three nodes' frontmatter; the real hazard is a naive parser producing a bogus parent id, not a crash. The kid's core claim — the three values are free text, `cavekit_req` is not schema-required, removal+inline is safe to test — survived review unchanged. Verdict stays `pending`; no experiment has run.
<!-- THOUGHT:END -->


## Agent Notes
Fixed cavekit_req bottleneck hypothesis: 3 malformed values have no kit to resolve against; cavekit_req is not in schema required fields, so removal+inline is safe. First concrete step to clear S18 sequence.
