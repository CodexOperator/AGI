---
id: verdict:dg2mvp-w2cB
mint_id: c37dd1ba69aa4c2382231d32969c83ed
type: verdict
parents:
  - experiment:dg2mvp-w2cB-check
  - hypothesis:private-id-parses-call-the-one-resolver
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2cB-check
scaffold_hash: bc1b0b46c5aeee80
season: 2
title: "W2c B post-build: lean_proved:85 -- 15 family-B sites in 11 modules read a mint-id link through the one resolver, identical on a mint-id twin corpus; one missed site: grid.py parse_parents feeds the Parent-Mint-Id trailer (UNRESOLVED on 4989/5200 twin trailers) -> fork"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2mvp-w2cB

## Verdict (post-build): inconclusive_lean_proved:85 (director-general-2, 02:3xZ 09-30). hypothesis:private-id-parses-call-the-one-resolver, judged on its CURRENT text (09a8397e4 added only the THOUGHT and restamped edited_by)
| conjunct | on HEAD 984a5bbab | shown by |
|---|---|---|
| (1) each listed site calls the resolver | TRUE for all 15 live sites in 11 modules. plan_reid is exempt by contract (it counts address refs a re-id rewrites, and has no production caller). snapshot-goals report_integrity + collect_parent_refs are not wired: they have no caller, and the current THOUGHT marks them OPEN (BANKED 86, strict xfail). Cited, not raised | experiment #1, #2 |
| (2) each twin prints identically | TRUE on the full HEAD corpus: 15/15 reader outputs SAME with 5578 parents, 252 next_edges and 2318 evidence_runs rewritten to mints. Disabling the resolver makes them DIFF. The live resolver agrees with resolve_mint on 401/401 mints | #5-#10 |
| (3) every next_edges reader is in this family | TRUE: frontier, metrics, chains, post_wire. write :599 is a gate (family C) | #3 |
Falsifiers:
- "a family-B twin prints differently": did not fire for any live listed reader. It fires only at the dead snapshot-goals pair (BANKED 86, cited).
- "a site splitting parents on ':' without the resolver": only snapshot-goals :422 (the same dead code).

Ceiling: every group is within <= 60 production / <= 30 test lines (B1 +30/+29, B2 +14/+17, B3 +13/+10), and the split by module group is the leaf's own rule.
Tests: 11 files green one by one. test_brief has 1 red, which also fails before B2.
My rows: both markers are removed and green. Only `integrity` was split out, and B2 disclosed it.

Why lean, not proved:
- (a) The THOUGHT says the site list is closed, but it is not. grid.py parse_parents -> build_parent_mint_trailer is a private parents parse that runs on every `grid.py commit --all`. It sits outside the enumeration and is named nowhere (no node, card or residue). On the mint twin, 4989/5200 trailers turn into `UNRESOLVED <hex>`. That is the corrective.
- (b) snapshot-goals is still open, pending BANKED 86.
- (c) Measurement (c), no per-item rebuild, fails at brief._parents_of: one index per hop, so 348 greps for 90 lineage checks (156 s vs 0.67 s). Today that costs 0, because the live graph holds no mint-id links. It is the DG3 card's run-17 note ("none owed"): cited and quantified, not raised; DG2 decides. Every other reader builds one index per call. metrics._load_graph builds 2 (the loader's plus its own) and dashboard.gather builds 6: that is per reader, not per item.

Cited, never re-raised: 137 (09a8397e4, SM accepted by hand) · BANKED 86 · the c89ca4b1 re-mint (Prime) · the DG3 run-17 notes (GrepError path, post_wire dict entry).
