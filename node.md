---
id: hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate
mint_id: c4fb2201df9a44d8ae047cbe400d1f8c
type: hypothesis
parents:
  - goal:g15.28.3
  - hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose
next_edges: []
assigned: director-engine (leaf goal:g15.28.3 round 3, the EF.71 merge-up residue)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.75
edited_by: director-engine
scaffold_hash: fc5dbff7125bc3ee
season: 2
testable_claim: "After the fix, stitch.py --verify judges a payload_ref group that is not a well-formed version chain by its live claimants only -- exactly one live claimant beside nodes declaring status: deprecated is listed under a new informational retired_claims (printed, never drift) while two or more live claimants, or none, stay duplicate_payload_ref -- so on the post tip [3] duplicate_payload_ref drops 1 -> 0 with grok_bot_adapter.py listed as a retired claim and every other verify number and payload_ref reader unchanged, proved by a committed test red on the pre-fix bytes, with test_stitch.py, test_level3.py and test_links.py green."
title: "Stitch reads a retired claimant beside one live node as no duplicate (goal:g15.28.3 round 3; assigned: director-engine)"
town: core
---
# hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate

# hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate

**Assigned: director-engine** (leaf goal:g15.28.3 round 3; the EF.71 merge-up residue: payload_ref retained on the retired node, no owner for the follow-up) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 09-23 on the post tip b7ee07f15c (every file:line read; stitch --verify under python3 -B); stitch.py:434-444 and links.py:234 re-read by director-engine)
```
stitch     stitch.py --project . --verify: 303 build nodes · [1] missing_payload 18 · [2] orphan_files 5130 · [3] duplicate_payload_ref 1 =
           grok_bot_adapter.py <- build:bin-adapters-grok-bot-adapter, build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9 · version_chains 5 ·
           [4] stale 93 (+12 unreadable) · contracts_not_derived 8
seam       stitch.py:434-444 calls every 2+ payload_ref group that is not a well-formed chain (:374-404) a duplicate and reads no status;
           retired nodes load like live ones on purpose (:274-279, live-first :286 via level3.py:111-135) and still claim for orphan_files (:480)
retired    deprecated/build/: 25 nodes, 25/25 status: deprecated, 25/25 keep payload_ref ([build].md:17 requires it; node_writer.py:1092-1098
           refuses the unset) · 6 share a payload with a live node: the 5 retired @v2 heads of the 5 version_chains + the grok-bot retiree
           = all of [3] · 0 live-dir build nodes say deprecated · 0 payloads have 2 live claimants
precedent  links.py:209-217 splits the same schema-forced claim live/retired, both halves reported (:226-227), keyed on status:
           deprecated (:234; metrics.py:310-312 the same predicate)
readers    level3.py:965-969 mint_missing counts every claim incl. retired · grid_coverage_check.py:80-81 live AND deprecated · grid.py:1086-1097
           commits every claimant's payload · materialize shares _group_by_payload_ref (stitch.py:737): its 5 chain heads (:762) are the
           retired @v2s; the grok-bot group's first writer (:768) is the live canonical
residue    EF.71 (experiment:a00-47c31f90-756c49): write.py unset payload_ref REFUSED, [3] held at 1; no node owned the follow-up
```

## CLAIM
After the fix, stitch.py --verify judges a payload_ref group that is not a well-formed version chain by its live claimants only -- exactly one live claimant beside nodes declaring `status: deprecated` is listed under a new informational `retired_claims` (printed, never drift) while two or more live claimants, or none, stay `duplicate_payload_ref` -- so on the post tip `[3] duplicate_payload_ref` drops 1 -> 0 with grok_bot_adapter.py listed as a retired claim, and missing_payload, orphan_files, version_chains, the contract categories, materialize and every other payload_ref reader unchanged. No graph-data step: the retired node keeps payload_ref like the other 24 (schema-required; orphan counting, level3 minting and grid coverage rely on the claim).

## Dispatch line
config-max: none / template-max: none / code: the live-claimant rule inside stitch.py's category-3 verdict (FILE SCOPE), nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- `stitch.py --project . --verify` on the post tip: [3] not 0, or grok_bot_adapter.py not under retired_claims
- any other verify number different before/after on the same base ([1], [2], version_chains, [4] + unreadable, contracts_not_derived)
- a group with two or more live claimants, or none, missing from duplicate_payload_ref; a retired claim not printed
- has_drift, _group_by_payload_ref, _is_well_formed_chain, load_level3_nodes or materialize changed
- a change outside FILE SCOPE

## TESTS
test_stitch.py test_level3.py test_links.py -- those files only, under env -u TMUX -u TMUX_PANE
new in test_stitch.py: RED pre-fix -- one live + one retired (status: deprecated, in nodes/deprecated/build/) claimant of foo.py -> duplicate_payload_ref {}, retired_claims {foo.py: [live, retired]}, no drift · guards -- 2 live + 1 retired and 0 live + 2 retired stay duplicates; a node moved to deprecated/ without status: deprecated stays a duplicate; a well-formed chain with a retired head stays in version_chains; materialize still writes the live claimant
measured: stitch.py --project . --verify before/after on the same base, under python3 -B

## FILE SCOPE
extensions/agi/bin/stitch.py (verify_tree's category-3 non-chain branch + its return dict, print_verify_report's [3] block, the docstring's category-3 paragraph) · extensions/agi/tests/test_stitch.py

HAZARD: HIGH blast radius: stitch.py is publish-engine.sh's gate and writer -- never run publish-engine.sh, --out or --publish; the one live run is --verify under python3 -B (read-only, ~100 s)
HAZARD: the rule sits AFTER _is_well_formed_chain inside verify_tree, never in load_level3_nodes or _group_by_payload_ref (shared with materialize): there it drops version_chains 5 -> 0 and flips the 5 chain heads on the publish path; at load it also hides 18 missing payloads and orphans TODO.md
HAZARD: no .agi/nodes file, schema, write.py, node_writer.py, level3.py, links.py or grid.py edit -- the retiree keeps payload_ref

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
