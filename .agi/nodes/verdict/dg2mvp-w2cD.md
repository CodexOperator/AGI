---
id: verdict:dg2mvp-w2cD
mint_id: 10ef8ff264b34e0a80f31af5ddf68495
type: verdict
parents:
  - experiment:dg2mvp-w2cD-check
  - hypothesis:gates-writer-and-cli-paths-resolve-mint-ids
next_edges: []
confidence: 0.86
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2cD-check
scaffold_hash: 64634639bb4a8151
season: 2
title: "W2c C corrective post-build (7d10fc7c7 + bd15f4e6e): proved 0.86 -- writer gate 0/5200 and cli evidence 0/2121 twin diffs, 8 off-shape mints shaped as their address twins, viewport render 1 index build (was 301); ceiling over, disclosed + accepted by SM"
town: core
verdict: proved
---
# verdict:dg2mvp-w2cD

## Verdict: proved (confidence 0.86)
DG3's build satisfies hypothesis:gates-writer-and-cli-paths-resolve-mint-ids at HEAD bd15f4e6e, every conjunct and no falsifier firing.

- (1) TRUE: `gate_for_root`'s index and `cli._evidence_corpus` are `links.resolving` objects. Twin readings: check_spawn 0 of 5200 differ (was 4887), cli evidence gate 0 of 2121 (was 2106), 10 off-shape-mint items included.
- (2) TRUE: `nearest_vision(_town)` takes `resolve=`; a shared `gate_resolver` costs 1 index build over 300 nodes, and a real `viewport.frame_stream` render on the mint twin is 1 build / 2.2 s (was 301 / 135.6 s). The default no-`resolve` call still builds per call, by design; the other callers make one call each.
- (3) TRUE: 8 off-shape mints (10 evidence items) are shaped as their address twins; `is_mint_id` and a `[0-9a-f]{32}` shape grep over evidence_gate.py + level3.py are 0 hits; `read_mvp_map` keeps 101 of 101 on the mint copy and the off-shape mvp row is green.
- Falsifiers: none fired (F1 0 of 5200, F2 0 of 2121, F3 1 build, F4 0 differing + 0 hits).
- One resolver: mint_index / resolve_mint / address_resolver defined once (links.py).
- Tests, one file per run: evidence_gate 140p, level3 60p/1x, spawn_gate 83p, links 47p/1 skip/1x, cli 76p (with the one repo file the archive lacks); my two strict-xfail rows lifted, green, not weakened (one call gained a corpus argument).

Notes, not gaps:
- Regression risk of bd15f4e6e, measured: no production caller lacks a corpus (7 paths); the live graph has 0 32-hex evidence items, so 0 new violations. On a synthetic corpus a dangling or colliding 32-hex ref now flips from demoted (lean:50) to REJECTED on `cli.py done` (exit 2, nothing written). This is the commit message's stated intent (a taxonomy violation, not a dangling ref) and follows belam's decision "gate on is a node's mint_id"; latent, not raised as a corrective.
- CEILING exceeded (+55/-28 production, +123 test vs <= 20 / <= 30): disclosed in 7d10fc7c7's message and accepted with W2c C on card-sanctuary-master (§0 / "Where it stops"). Not re-raised.
- Open residues cited, not re-raised: BANKED 86 (the snapshot-goals pair, the one xfail in test_links), DG3 card run-17 note on brief._parents_of index-per-hop.
