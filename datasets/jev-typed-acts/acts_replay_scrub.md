# acts_replay_scrub -- ECHO arm

MODEL=jev-1.13.0; SEED=20260918; REPEATS=3; state = node BODY only; scrub replaces every proved|disproved|inconclusive_lean_*|pending|accept|demote token with [SCRUBBED].
Corpus PINNED to the 370 act ids in acts_replay.jsonl (JEV.01 re-samples a different 200 experiments now; only 211/370 overlap).
Calls 200: before 1110 / after 1110. Spend: before $0.076246 + after $0.076689 = $0.152935 (cap $0.50).

| q | n | agree BEFORE | agree AFTER | base | chance |
|---|---|---|---|---|---|
| q1 | 369 | 0.737 | 0.588 | 0.507 | 0.200 |
| q2 | 370 | 0.489 | 0.538 | 0.776 | na |

- q1 distinct verdict classes present: 5 -> chance = 1/5 = 0.200; claim bar chance+0.10 = 0.300
- q1 delta = -0.149; falsifier 1 (ECHO wrong) trips if q1_after >= 0.60
- q2 delta = +0.049; falsifier 3 trips if |delta| > 0.10
- leak tokens before (act total): 1454; leaked acts fraction 0.932; after (row total): 0; residual act ids: []
- JEV.01 historical reference (old re-sampled corpus): q1 0.743 base 0.507, q2 0.492 base 0.776
