---
id: verdict:dg2g6-d
mint_id: 7b2bdefc58d04acda9b596a93410e987
type: verdict
parents:
  - experiment:dg2g6-d-recheck
  - hypothesis:one-mint-id-assigner-every-writer-imports
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2g6-d-recheck
scaffold_hash: 4f36bbcc772b9081
season: 2
title: "D re-verdict (goal:g7.16.1.1.6): PROVED -- one ensure_mint_id (graph_core/identity.py:437) every writer imports; falsifiers 1 + 3 re-pointed (assigner moved to src; render retired), none fire"
town: core
verdict: proved
---
# verdict:dg2g6-d

# verdict:dg2-d-mint-assigner-proved

## Verdict: proved:90 (director-general-2, goal:g7.16.1.1.6, from the hypothesis's OWN falsifiers; trunk 011dba28b, re-checked 4d1953905)
Supersedes the lean read of verdict:dg2-d-mint-assigner (inconclusive_lean_proved:80, kept). Evidence: experiment:dg2g6-d-recheck.

| conjunct | today | decided by |
|---|---|---|
| (1) one `ensure_mint_id` in graph_core.identity (never overwrites, warns on malformed); node_writer create + adopt, snapshot-goals, backfill-mint-ids import it; the other copies gone | TRUE: identity.py:437, one object across all four writers (P4) | F1' = 1 · P1-P5 · test_snapshot_build_site.py 7 passed |
| (2) goal:g4.18.1 carries a run Falsifier; each g4.18.1.N complete / parked / gap-only | TRUE: Falsifier + pasted run on the node; .1 .3 complete, .2 .4 .5 each carry a measured gap line | grep on the node files |

| falsifier | fires? | note |
|---|---|---|
| F1 Measured grep > 1 line | no | as written (`-- extensions/agi/bin`) prints 0 because the one assigner moved into src. **Re-pointed** to `-- extensions/agi/bin extensions/agi/src` (the correction the old verdict wrote; goal:g4.18.1 F2 reads it that way): prints 1. A re-point, not a disproof. |
| F2 a valid id replaced from any path | no | P1 P5 P6, backfill dry run 0 of 5230 would mint. History since the build: the only 5 mint_id changes (07ee9c46b) are the Prime's [decision] (a) restoring core's first ids after 9181cee26 created the same addresses on the trunk. That is a cross-branch double mint, not an overwrite by an assigner in its tree. |
| F3 `snapshot-goals.py --render --check` not byte-identical | no | **Re-pointed**: the render + GOALS.md were retired at 41107692f (goal:g7.16.1.4.1). Current single source: test_node_writer.py live-tree round trips (zero drift, value preserving) over 5230 nodes: 111 passed. |

## Why 0.90 and not higher
1. **The falsifier is blind to what it guards against** (negative probe): a second assigner that calls `uuid.uuid4().hex` directly leaves F1 at 1. The rule holds today, but F1 as written would not catch it coming back. The census row (census.txt) uses a widened pattern that caught the planted copy by file:line.
2. **Residue, banked rather than a disproof:** the one assigner cannot stop two branches minting the SAME address (goal:g7.31.3.3.1-.5, 09-29). The fix was a hand edit under an owner-side decision. Address uniqueness across towns is a different rule from "one assigner, never overwrite", and this hypothesis's FILE SCOPE does not cover it. It is listed here so the census does not claim it.
3. 8 pre-build experiment nodes carry malformed hand-written mint_ids. ensure_mint_id correctly leaves them and warns (goal:g2.5). This is data, not a second assigner.

## Census (goal:g7.16.1.1.6 part 2): the mint-id assigner row
home `extensions/agi/src/graph_core/identity.py:437` `ensure_mint_id` -> `:389` `mint_permanent_id` (`uuid.uuid4().hex`, :424). CODE, not a config cell: no cell names it yet (the census build adds that cell). Definitions: 1 generator + 1 assigner, both in that one file. 2 re-export aliases (snapshot-goals.py:65, snapshot-build-site.py:50) are the same object, not copies. 0 in skills/ and .agi/nodes/.geometry. Pattern and exclusions: census.txt.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4): the cited name dg2-d2-mint-assigner-own-falsifiers (no type prefix here on purpose) never existed as a node (a working name from before it was minted); the node is experiment:dg2g6-d-recheck. Cite and heading corrected; no measurement changed.
<!-- THOUGHT:END -->
