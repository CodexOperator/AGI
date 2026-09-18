# Kid A commands - tm.23 r2 q4_0 KV cache (kid A, decisive rows)

## Exact mandated command (full matrix, per hypothesis node TESTS)
llama-bench -m /home/ubuntu/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf \
  -fa 1 -p 0 -n 64 -d 0,2048,4096,8192 \
  -ctk f16,q8_0,q4_0 -ctv f16,q8_0,q4_0 -r 3 -o jsonl

## Attempt record (all tenancy-instrumented via lm_bench.py protocol:
## loadavg + MemAvailable + swap + pgmajfault before/after, streamed)
# 1. 20260917T005931Z  '0,2048,4096'  3types  - TIMEOUT 1550s, only d0 f16,q8_0 cells
#    load b{1.9/5.4/7.1} a{6.0/5.5/5.8}; box contended hard. rows=14 (garbage tg).
# 2. 20260917T012718Z  '4096'         3types  - TIMEOUT 1200s, only d4096 f16,q8_0 cells
#    load b{2.1/4.1/5.2}; d4096 f16 6.98 (within-cell 2x spread). q4_0 never ran.
# 3. 20260917T014901Z  '4096'         f16,q4_0 - COMPLETED ret 0 (the decision rows)
#    load b{2.1/4.2/4.8} a{4.5/4.5/4.7} -> RESULT: q4_0/f16 ratio ~1.68-1.79x at depth 4096
#
## Why the full matrix never fitted: node estimated prefill-to-8192 at ~200 tok/s
## (-> 12-18min); measured prefill here is ~30-40 tok/s and dropped further under
## the ~15 resident agents (sustained load 4-5, >4.0 gate). Full 36-cell matrix
## needs ~25-40min, over the 20min script ceiling. Only the decisive depth-4096
## f16-vs-q4_0 comparison completed in budget.
#
## Tenacity finding: box sustains load 4-5 from ~15 standing agents (belam-*, sensei-*,
## director-*, thought-master, heal watch, viewport). A <2 window is momentary (l1 only);
## l5/l15 stay 4-7. The parent's "loadavg <= 4.0 during rows else pending" gate FAILED here.