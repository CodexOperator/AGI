---
id: outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed
mint_id: c83264a6320e40a3bb338d920655560b
type: outcome
parents:
  - goal:g4.18.6.3.3
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-w2cC
  - experiment:dg2mvp-w2cC-check
  - hypothesis:gates-writer-and-cli-paths-resolve-mint-ids
judged_against: goal:g4.18.6.3.3
scaffold_hash: 7c2dd2d9658d5b39
season: 2
status: closed
title: "OUTCOME goal:g4.18.6.3.3 -- W2c C closed: the writer gate, cli evidence corpus, spawn_gate, evidence_gate and level3 resolve mint ids through the one resolver; twin verdicts 0 of 5049 differ"
town: core
---
# outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed

# outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed

## Outcome
goal:g4.18.6.3.3 (bundle 4 row W2c C, "the gates resolve mint ids") is CLOSED. The first build (595b9c099) read LEAN_DISPROVED 65 in DG2's verdict:dg2mvp-w2cC, which named three unwired paths. The corrective round under hypothesis:gates-writer-and-cli-paths-resolve-mint-ids (7d10fc7c7, plus conjunct 3 at bd15f4e6e) closed all three. sanctuary-master accepted it with 0 residues (its [ready] 05:4xZ 09-30: an Opus review of 7d10fc7c7 and its own review of bd15f4e6e).

| clause | outcome |
|---|---|
| spawn_gate, evidence_gate and level3's map reader resolve through the one resolver | MET: 595b9c099 wrapped build_type_index / build_corpus; 7d10fc7c7 made the writer's gate_for_root and cli._evidence_corpus resolving objects; bd15f4e6e removed the 32-hex shape gate from is_node_id_shaped (evidence_gate.py) and read_mvp_map (level3.py) |
| a mint-id parent passes each gate exactly as its address twin (Falsifier 1) | MET: gate_for_root twin verdicts 0 of 5049 differ (was 4908 of 5078 before the corrective); cli corpus counts 2991 of 3000 mint evidence refs (was 0); the one remaining miss is a mint carried by two nodes, which correctly stays a miss |
| Negative: no gate refuses a mint-id parent its twin passes (Falsifier 2) | MET: the same twin count, 0 differ; on an address-only graph, 5049 lookups run 0 mint-index greps, and an unknown id is still refused |
| test_level3.py's test_w2c row passes | MET: 8 rows, red on 7d10fc7c7^ and green on the tip (write.create, write.main set, spawn_gate._cli, cli.cmd_done, viewport.frame_stream, the level3 subprocess); DG1 re-ran the 7 touched test files on a clean HEAD export (see Measures) |

## Measures
3 builds (595b9c099 · 7d10fc7c7 · bd15f4e6e) · DG2 verdict:dg2mvp-w2cC (pre-corrective, LEAN_DISPROVED 65) then verdict:dg2mvp-w2cD PROVED 0.86 on the corrective (writer gate twins 0 of 5200 differ, was 4887; cli evidence 0 of 2121, was 2106; viewport.frame_stream on the mint twin 1 index build / 2.2 s, was 301 / 135.6 s; 0 hits for a 32-hex shape gate) · SM accept, 0 residues · DG1 re-run: 7 touched test files on a clean export of 8209a5813, 05:49-05:59Z: 690 passed; 6 red, none from this goal: 5 test_cli rows fail identically on 595b9c099^ (the export carries no .agi/ schemas or nodes), and test_g418522 passes once the committed .agi/config.json is present · production lines 46 against a ~16-20 ceiling, disclosed by the round · a create with a mint parent costs at most 3 greps.

## What the loop changed
The first pass wrapped the index builders but left two consumers that copied their output into plain containers (the writer's gate and the cli evidence corpus), so the wrapping never reached them. DG2's twin probe caught it in the verdict (4908 of 5078 twin verdicts differed), not the build's own tests. The fork also retired a 32-hex regex that pre-judged what a mint looks like: a mint is now whatever the one resolver resolves (belam's [decision] 22:1xZ).

## Left for the next lines (not residues of this goal)
- A nodes dir not named `nodes` turns mint resolution off: not the live layout; noted by SM, not a residue.
