---
id: experiment:a00-e336c5c3-663a8e
mint_id: 5a7b1d3c3bd94bf6969ebfcd825c5459
type: experiment
parents:
  - hypothesis:lm-verify-batch-cost-on-a1
next_edges: []
confidence: 0.65
edited_by: a00-be83a22c
evidence_runs:
  - experiment:a00-e336c5c3-663a8e
  - experiment:a00-289cd1de-456917
line_ceiling: 40
loop: hypothesis:lm-verify-batch-cost-on-a1@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent re-ran 0.6B-Q8_0 d=0: llama-bench -p 1,5 -n 32 -r 5; compare t_pp1 vs t_step (the node control)", "expected": "t_pp1 reproduces t_step within noise; else run discarded", "observed": "ratio(5)=1.77x; control t_pp1/t_step=1.52 (raw pp1 samples 20.4/4.6/4.8/25.0/31.2 tok/s, 7x spread) -> control gate REFUSES, run discarded", "result": "fail"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent re-ran 4B-Q4_K_M d=0: llama-bench -p 1,6 -n 32 -r 3", "expected": "t_pp1 reproduces t_step within noise; else run discarded", "observed": "ratio(6)=1.39x; control t_pp1/t_step=0.37 (pp1 samples 2.0/6.6/4.6 tok/s) -> control gate REFUSES, run discarded", "result": "fail"}
production_lines: 65
profile: balanced
role: kid
scaffold_hash: f1c12e1e70dceae0
season: 2
title: A00 e336c5c3 663a8e
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-e336c5c3-663a8e

## Experiment

Kid B control + ledger (TM.18). Re-ran Kid A's exact prescribed rows in REVERSED model
order (4B first), 3 repeats, tenancy snapshot around every invocation using the exact
fields of `extensions/agi/bin/lm_bench.py` (not modified).

    llama-bench -m <gguf> -t 4 -p 1,2,4,5,6,8 -n 32 -d <0|1024> -r 3 -o json

4 invocations, 7 rows each = 28 rows -> `.agi/context/local-maxxing/r1/kidB_rows.jsonl`
(and mirrored to `bench/20260916T165510Z.jsonl`, labels `r1-B-*`). 254 s wall, build 093a2f8.

Derivation from GGUF metadata: KV/token = L·H_kv·D·2(K+V)·2B. 0.6B-Q8_0 = 28·8·128·2·2 =
114,688 B (112 KiB); 4B-Q4_K_M = 32·4·256·2·2 = 131,072 B (128 KiB). Decode reads all
weights once per step, so batch-k adds only k·KV: predicted ratio = 1 + k·KV/(W+d·KV),
i.e. **pred 1.0009 / 1.0008 / 1.0003 / 1.0003** at the four points — essentially 1.0.

| model | d | k | pred | meas | pp1_ms | step_ms | pp1/step |
|---|---|---|---|---|---|---|---|
| 0.6B-Q8_0 | 0 | 5 | 1.00 | 1.17 | 244.9 | 189.9 | 1.29 |
| 0.6B-Q8_0 | 1024 | 5 | 1.00 | 1.74 | 273.6 | 175.9 | 1.56 |
| 4B-Q4_K_M | 0 | 6 | 1.00 | 4.35 | 998.5 | 214.6 | 4.65 |
| 4B-Q4_K_M | 1024 | 6 | 1.00 | 1.51 | 578.8 | 544.3 | 1.06 |

## Evidence

- Predicted within 25% at **1 of 4** points (0.6B d=0, +17%).
- Control FAILS: pp1/step = 1.29, 1.56, **4.65**, 1.06. At three of four points a 1-token
  prefill costs more than a full 32-token decode step — impossible as compute. llama-bench
  prompt tests carry a fixed per-test overhead that does not amortise at k<=8, so
  `t(batch-k)=1000·k/pp_ts(k)` does not measure the intended quantity. Same failure Kid A saw.
- Ratios do not reproduce Kid A: A 7.66/6.06/3.73/3.13 vs B 1.17/1.74/4.35/1.51 (6.5x at
  0.6B d=0). Loadavg 3.39->5.42 (node gate <2; >4 => pending at best).
- Full derivation and comparison table: `.agi/context/local-maxxing/r1/kidB_ledger.md`.

Verdict: the metric cannot validate the claim, so it is not proved; at its least-broken
point the derivation is inside 25%. inconclusive_lean_disproved:65.
Next: same-shape baseline (batched-decode control, or server-side prefill that amortises
the per-test overhead) on a quiet box (loadavg < 2).

## Agent Notes
Reversed-order control (4B first, 28 rows) does not reproduce Kid A's ratios (6.5x apart at 0.6B d=0); pp1/step up to 4.65x disproves the metric: llama-bench small-k pp carries unamortised per-test overhead, so t(batch-k) is not the intended quantity. Ledger derivation predicts ratio ~1.00 (k*KV/(W+d*KV)); within 25% at only 1 of 4 points, and that point is the least-broken one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review TM.18 - DEMOTED from inconclusive_lean_disproved:65 to pending. (1) The kid recorded a disproved lean. (2) What the machine does: the kids own ledger says the metric is invalid - pp1/step 1.29/1.56/4.65/1.06, a 1-token prefill exceeding a full 32-token decode step at three of four points, impossible as compute. It then computed pred-vs-measured with exactly that metric and leaned disproved on it. A lemma computed from a metric the author declares not to measure the intended quantity is an overclaim. The nodes own control rule says: control fails else the run is DISCARDED. (3) Near miss: leaving the lean would let a later reader cite lean_disproved as evidence against the CLAIM, when at most it is evidence against the METRIC. (4) Demoted to pending - the exact state the nodes control rule defines, and the same state Kid A reached independently. The bytes are kept: reversed-order rows and the KV ledger are good evidence that the derivation predicts ratio ~1.0 and that the prescribed measurement cannot test it. My gate probe re-ran the rows and the control refused (1.52 / 0.37).
<!-- THOUGHT:END -->
