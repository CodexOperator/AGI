---
id: hypothesis:lm-ouro-loops-beat-dense-on-kid-checklist
mint_id: 583209b50ebe4f2db09c58aa009af13e
type: hypothesis
parents:
  - goal:g14.3
next_edges: []
ceiling: 1 USD OpenRouter; 0 compute; ONE model file <= 1.6 GB on ARM4C under /tmp only with the owner yes, deleted at round end; runs <= 10 min each
edited_by: thought-master
falsifier: loops=4 <= loops=1 on accuracy (looping adds nothing at this size) OR loops=4 <= the dense Qwen3-1.7B baseline (depth recurrence is not the source of the gain) OR the patched llama.cpp does not build/run the arch on aarch64 within the round (then the CPU path is closed and the chain moves to the 2.6B / Huginn rows on the rig).
scaffold_hash: 2c85c1224047c0e8
season: 2
testable_claim: On ARM4C (4 cores, 23 GB, 19 GB disk free), with a patched llama.cpp carrying the ouro arch (no upstream support today, MEASURED), Ouro-1.4B Q8_0 (1.53 GB, BrandeisPatrick/Ouro-1.4B-GGUF) or Q4_K_M (0.896 GB) run at --override-kv ouro.num_loops=4 scores strictly higher exact-answer accuracy on the town 20-prompt kid checklist (<= 64 new tokens, greedy, 3 reps) than (a) the same file at num_loops=1 and (b) Qwen3-1.7B Q4_K_M (same unique-param class, non-looped); tok/s at 1 and 4 loops recorded beside every row (ESTIMATE 13 / 3.3 tok/s at 12 GB/s), and the bytes-touched-per-token ledger records weight_bytes x loops.
tests: "GATED ON THE OWNER: model bytes on ARM4C are forbidden by the 05:5xZ standing rule -- this round needs ONE file <= 1.6 GB under /tmp, deleted at round end; asked the owner 20:1xZ in the pane; dispatch only on a yes. Then ONE pi parent + ONE kid, ARM4C-light, 1 USD OpenRouter, 0 compute cost: (1) build the ouro-arch llama.cpp fork/PR named in the GGUF README in a user prefix (record commit + build wall); (2) fetch Ouro-1.4B Q8_0 (Q4_K_M if disk < 10 GB free), sha256 vs the HF lfs oid; (3) the town 20-prompt kid checklist (the file hypothesis:lm-bonsai2-27b-kid-tier conjunct 3 uses) at loops 1, 2, 4, greedy, <= 64 new tokens, 3 reps each -> exact-answer accuracy + tok/s + peak RSS per row; (4) the dense control Qwen3-1.7B Q4_K_M on the same prompts (its ~1.1 GB counts against the same permission); (5) rows to bench/<utc>.jsonl with the loadavg gate; the kid persists rows after every probe, the parent commits promptly; (6) delete the model files at the end, record df before/after. FILE SCOPE .agi/context/local-maxxing/ouro/{cmds.md, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node; anonymization; kid line_ceiling 120."
title: "Chain (d) first hop (from doc:recurrent-looped-transformer + the 2026-09-18-looped survey): on the town 20-prompt kid checklist, Ouro-1.4B (looped, 24 layers x 4 loops, Apache-2.0) at num_loops=4 beats BOTH the same file at num_loops=1 AND a same-unique-param dense model (Qwen3-1.7B-class, Q4) on exact-answer accuracy, on the 4-core aarch64 box, short outputs -- looping is the lever, not scale"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-ouro-loops-beat-dense-on-kid-checklist

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
