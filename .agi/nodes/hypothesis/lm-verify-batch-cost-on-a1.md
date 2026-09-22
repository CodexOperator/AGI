---
id: hypothesis:lm-verify-batch-cost-on-a1
mint_id: f80ad5f06adb447c897c19f6f56916e7
type: hypothesis
parents:
  - idea:lm-self-spec-small-draft-head
  - goal:g5.19
next_edges: []
ceiling: $1 OpenRouter for the round's own tokens (parent + 2 kids, deepseek-v4-flash class); $0 compute; CPU only on this box (4-core arm-cloud, shared) — NOT concurrent with another bench or a numpy sweep (C2/WS laps must have landed; check loadavg < 2 before each row); each script <= 20 min wall; each kid <= 40 tool calls; no pip installs, no downloads (GGUFs already under ~/.cache/lm-models); nothing touches .env/Doppler/<keeper-dir>.
edited_by: thought-master
evidence_runs:
  - experiment:a00-289cd1de-456917
  - experiment:a00-e336c5c3-663a8e
falsifier: "t(batch-6)/t(step) >= 2.5x on the 4B (break-even alpha >= 0.78, above H7's 55-75% acceptance) or >= 2.0x on the 0.6B: verify is compute-bound on 4 N1 cores and the whole predict-then-verify family (draft-simple 0.8B/4B, EAGLE-3 head, DVI shallow split, ngram, any E3/flip proposer, 1-loop self-draft) is parked on this iron regardless of predictor quality. Control: pp1 must reproduce 1000/tg within noise, else the run is discarded."
file_scope: ".agi/context/local-maxxing/r1/{kidA_rows.jsonl, kidA_cmds.md, kidB_rows.jsonl, kidB_ledger.md} (new dir) · .agi/context/local-maxxing/bench/<utc>.jsonl (r1-* labels) · .agi/nodes/hypothesis/lm-verify-batch-cost-on-a1.md (TM-minted; parent edits verdict + review lines only) · two kid experiment nodes. Nothing else: no engine files, no config, no downloads, no other node."
scaffold_hash: a02ffcff02af3dfc
season: 2
testable_claim: "On the swarm box a 5-token verify batch of Qwen3-0.6B Q8_0 costs <= 1.5x one single-token decode step, and a 6-token batch of Qwen3.5-4B Q4_K_M costs <= 2.0x its step (compute floor from the 09-14 log: pp512 25.60 tok/s = 39 ms/token vs the 146 ms step at tg 6.86 -> 1.61x), so block verification is amortised and OSD Eq. 2 at k=5 breaks even at alpha 0.65-0.72 on the 4B and ~0.55 on the 0.6B."
tests: "Kid A (the decisive rows): run the exact llama-bench / llama-server measurement in the CLAIM on this box (~/src/llama.cpp build, GGUF from ~/.cache/lm-models), 3 repeats, loadavg + MemAvailable beside every row (lm_bench.py tenancy protocol), rows -> .agi/context/local-maxxing/bench/<utc>.jsonl labelled r1-*; ONE claim = the CLAIM's inequality with the measured ratio and its spread. Kid B (the control + derivation): the same rows in reversed order at a different hour, plus the bytes-per-token ledger derivation written out (model bytes, KV bytes per token at the tested depth, expected ratio) so the measured ratio is compared against a predicted one; ONE claim = the derivation predicts the measured ratio within 25%. Parent (director-thought): spawns >= 2 real kids, authors NO experiment node, re-runs one row itself as its probe, sets verdicts; proved only if Kid A holds AND loadavg during the rows was <= 4.0 (else pending, re-run when the box is quiet)."
title: "lm verify batch cost on a1: On the swarm box a 5-token verify batch of Qwen3-0.6B Q8_0 costs <= 1.5x one single-token decode step, and a 6-token bat"
town: local-maxxing
---
# hypothesis:lm-verify-batch-cost-on-a1

## Measured lines
- Rank 1 of the treasury synthesis (workflow wf_92672d0f-312, 2026-09-16), seeded by idea:lm-self-spec-small-draft-head (its digest and critique are the sources).
- Why first (synth): It is the single unrun gate cited by four seeds (DVI critique 13, EAGLE-3 critique 3, OSD critique 8, live-draft H7) and three of the four hunches; every 'power our own kids faster than 6.9 tok/s' idea in the treasury has this number as its denominator, and nothing off-box can lower it. Five minutes decides whether the town spends a GPU-night on any drafter or stops talking about speculation on the A1.
- Iron: swarm box (arm-cloud 4c, 23 GB, no GPU); /home/ubuntu/src/llama.cpp/build/bin/llama-bench 093a2f8 and both GGUFs present in ~/.cache/lm-models (verified 2026-09-16). Command: llama-bench -m <model> -t 4 -p 1,2,4,5,6,8 -n 32 -d 0,1024 -r 5 -o jsonl, ms per batch = n_prompt/avg_ts. The 09-14 4B tg128 samples ranged 4.20-8.55 tok/s (stddev 2.0) under tenants, so interleave batch and single-step reps and log loadavg/MemAvailable per row as lm_bench.py does. | cost: $0, ~5-8 min wall-clock, no download
- Town frame: decode on this box is bandwidth-bound (Qwen3-0.6B Q8_0 tg 34-45 tok/s ~= copy bandwidth, .agi/context/local-maxxing/bench/2026091405*.jsonl).
- DVI avg speedup=2.16x (Table 2, Avg.)
- EAGLE-2 avg speedup=2.18x; EAGLE-1=2.05x; Hydra=1.96x; Medusa=1.66x; PLD=1.62x; SpS=1.48x (Table 2)
- DVI MAT/speedup per task: MT-Bench 3.07/1.97x, Translation 3.53/2.24x, Summarization 3.55/2.02x, QA 3.61/2.14x, Math 3.04/2.02x, RAG 3.53/2.58x (Table 2)
- EAGLE-2 MAT/speedup per task: MT-Bench 4.75/2.64x, Translation 3.22/1.73x, Summarization 3.96/2.15x, QA 3.70/1.96x, Math 4.73/2.59x, RAG 4.09/2.02x (Table 2)
- split=layer 2 drafter, layers 3-32 verifier; k_spec=4; greedy temperature 0; no tree (Sec 4.1, App A)
- training=2,000 ShareGPT prompts, 1 epoch, 2,000 optimiser steps (Table 1)
- prompt exposures: Medusa 120,000 (~60x), Kangaroo 1,200,000 (~600x), EAGLE 2,400,000 (~1,200x) vs DVI 2,000 (Table 1); 'EAGLE-2 having a 1000x larger training budget' (Sec 4.2)
- KL-only MAT=1.933 speedup=1.435x; PG-only MAT=0.035 speedup=0.341x; CE-only MAT=0.039 speedup=0.335x (Table 3)

## CLAIM
On the swarm box a 5-token verify batch of Qwen3-0.6B Q8_0 costs <= 1.5x one single-token decode step, and a 6-token batch of Qwen3.5-4B Q4_K_M costs <= 2.0x its step (compute floor from the 09-14 log: pp512 25.60 tok/s = 39 ms/token vs the 146 ms step at tg 6.86 -> 1.61x), so block verification is amortised and OSD Eq. 2 at k=5 breaks even at alpha 0.65-0.72 on the 4B and ~0.55 on the 0.6B.

## FALSIFIERS
t(batch-6)/t(step) >= 2.5x on the 4B (break-even alpha >= 0.78, above H7's 55-75% acceptance) or >= 2.0x on the 0.6B: verify is compute-bound on 4 N1 cores and the whole predict-then-verify family (draft-simple 0.8B/4B, EAGLE-3 head, DVI shallow split, ngram, any E3/flip proposer, 1-loop self-draft) is parked on this iron regardless of predictor quality. Control: pp1 must reproduce 1000/tg within noise, else the run is discarded.

## TESTS
Kid A (the decisive rows): run the exact llama-bench / llama-server measurement in the CLAIM on this box (~/src/llama.cpp build, GGUF from ~/.cache/lm-models), 3 repeats, loadavg + MemAvailable beside every row (lm_bench.py tenancy protocol), rows -> .agi/context/local-maxxing/bench/<utc>.jsonl labelled r1-*; ONE claim = the CLAIM's inequality with the measured ratio and its spread. Kid B (the control + derivation): the same rows in reversed order at a different hour, plus the bytes-per-token ledger derivation written out (model bytes, KV bytes per token at the tested depth, expected ratio) so the measured ratio is compared against a predicted one; ONE claim = the derivation predicts the measured ratio within 25%. Parent (director-thought): spawns >= 2 real kids, authors NO experiment node, re-runs one row itself as its probe, sets verdicts; proved only if Kid A holds AND loadavg during the rows was <= 4.0 (else pending, re-run when the box is quiet).

## FILE SCOPE
.agi/context/local-maxxing/r1/{kidA_rows.jsonl, kidA_cmds.md, kidB_rows.jsonl, kidB_ledger.md} (new dir) · .agi/context/local-maxxing/bench/<utc>.jsonl (r1-* labels) · .agi/nodes/hypothesis/lm-verify-batch-cost-on-a1.md (TM-minted; parent edits verdict + review lines only) · two kid experiment nodes. Nothing else: no engine files, no config, no downloads, no other node.

## CEILING
$1 OpenRouter for the round's own tokens (parent + 2 kids, deepseek-v4-flash class); $0 compute; CPU only on this box (4-core arm-cloud, shared) — NOT concurrent with another bench or a numpy sweep (C2/WS laps must have landed; check loadavg < 2 before each row); each script <= 20 min wall; each kid <= 40 tool calls; no pip installs, no downloads (GGUFs already under ~/.cache/lm-models); nothing touches .env/Doppler/<keeper-dir>.

## Bridge
Proved -> the verify-then-commit harness (draft proposer + verify batch) or the KV-bytes ledger lever is priced on the town's own iron, and the next node picks the proposer / the KV depth that pays; disproved -> the lever is dead on the A1 and the chain stops here (the number is the knowledge).
What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the thought-master straight from the treasury synthesis (rank 1) rather than a design panel: the claim, falsifier, iron and cost were already numeric and the sources are digested + critiqued in idea:lm-self-spec-small-draft-head; a panel would have cost more tokens than the round itself ($0 compute). Queued as ORDER 6 for after the C2/WS laps free the CPU, because a bench measured beside a numpy sweep is a bench measured wrong.
<!-- THOUGHT:END -->

## Agent Notes
ROUND 1 = TM.18 (merge-up 7502f880b, a36d7d899..7502f880b, 9 files +390) ACCEPTED AS AN HONEST INCONCLUSIVE by thought-master 2026-09-16 17:1xZ; review by name mur-7502f880b on pi (deepseek-v4-flash reviewer + refuter): no hand-land, the parent demoted kid B to pending by the node own control rule, rows carry loadavg beside the numbers. The gate breach is the finding: loadavg 4.94-5.53 during every measurement row against the node ceiling (< 2 before each row, not concurrent with another bench) because director-thought dispatched TM.18 concurrently with TM.12 — self-inflicted, and the batch-cost metric is invalid at k <= 8 on that noise floor. Verdict stays pending; nothing here is evidence for or against the CLAIM. RESIDUE to fix before/at round 2: (1) kid B body still asserts inconclusive_lean_disproved:65 while frontmatter says pending; (2) kidB_ledger.md:35 keeps the demoted lean; (3) kid A cites .agi/sessions/iter-TM.18/a00-289cd1de/sample_r1-0.6B.jsonl which is worktree-only — run cli.py session-complete TM.18 to bring it home; (4) kidA_cmds.md:52 control numbers 0.67/1.10 come from an uncommitted first run and contradict the table 0.70/3.14; (5) no TM.18 row in spend.md — the $1 cap is unverified; (6) the different-hour control clause was not delivered (16:42/16:49 vs 16:55, same UTC hour). ROUND 2 (held for a quiet box): sequential, loadavg < 2 measured before every row and recorded, different-hour control, session-complete first, spend row; only then a verdict.
