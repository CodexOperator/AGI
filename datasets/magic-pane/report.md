# magic-pane chunk 1 — confusion matrix + latency table

Segments: 237 (pi streams 176, comms 61). Majority class `bench_jsonl` = 0.3038.

| condition | N | top-1 acc | majority baseline | median s | p95 s | pi acc | comms acc |
|---|---|---|---|---|---|---|---|
| fixed | 40 | 0.1097 | 0.3038 | 0.190 | 0.270 | 0.1477 | 0.0000 |
| fixed | 80 | 0.1181 | 0.3038 | 0.314 | 0.382 | 0.1477 | 0.0328 |
| shuffled | 40 | 0.2700 | 0.3038 | 0.369 | 0.408 | 0.3523 | 0.0328 |
| shuffled | 80 | 0.2869 | 0.3038 | 0.415 | 0.485 | 0.3523 | 0.0984 |

### confusion — fixed, N=40

| gold \ pred | write_note | write_set | dm | merge_up | dispatch | bench_jsonl | node_write | UNPARSED |
|---|---|---|---|---|---|---|---|---|
| write_note | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| write_set | 2 | 4 | 0 | 0 | 1 | 0 | 1 | 0 |
| dm | 49 | 0 | 0 | 1 | 11 | 0 | 0 | 0 |
| merge_up | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dispatch | 26 | 0 | 0 | 1 | 15 | 0 | 0 | 0 |
| bench_jsonl | 65 | 0 | 0 | 2 | 1 | 4 | 0 | 0 |
| node_write | 37 | 2 | 1 | 1 | 7 | 3 | 2 | 0 |

### confusion — fixed, N=80

| gold \ pred | write_note | write_set | dm | merge_up | dispatch | bench_jsonl | node_write | UNPARSED |
|---|---|---|---|---|---|---|---|---|
| write_note | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| write_set | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| dm | 46 | 0 | 2 | 3 | 8 | 0 | 0 | 2 |
| merge_up | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dispatch | 24 | 0 | 0 | 0 | 18 | 0 | 0 | 0 |
| bench_jsonl | 68 | 0 | 0 | 1 | 2 | 1 | 0 | 0 |
| node_write | 40 | 4 | 0 | 0 | 6 | 1 | 2 | 0 |

### confusion — shuffled, N=40

| gold \ pred | write_note | write_set | dm | merge_up | dispatch | bench_jsonl | node_write | UNPARSED |
|---|---|---|---|---|---|---|---|---|
| write_note | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| write_set | 2 | 3 | 0 | 1 | 1 | 0 | 1 | 0 |
| dm | 13 | 4 | 2 | 10 | 14 | 4 | 12 | 2 |
| merge_up | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dispatch | 5 | 3 | 0 | 4 | 20 | 6 | 4 | 0 |
| bench_jsonl | 17 | 2 | 0 | 4 | 3 | 29 | 16 | 1 |
| node_write | 15 | 10 | 2 | 3 | 7 | 5 | 9 | 2 |

### confusion — shuffled, N=80

| gold \ pred | write_note | write_set | dm | merge_up | dispatch | bench_jsonl | node_write | UNPARSED |
|---|---|---|---|---|---|---|---|---|
| write_note | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| write_set | 1 | 5 | 0 | 0 | 1 | 1 | 0 | 0 |
| dm | 9 | 2 | 6 | 12 | 11 | 7 | 9 | 5 |
| merge_up | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dispatch | 5 | 1 | 0 | 4 | 20 | 4 | 6 | 2 |
| bench_jsonl | 19 | 5 | 0 | 9 | 5 | 25 | 9 | 0 |
| node_write | 13 | 12 | 0 | 2 | 9 | 5 | 12 | 0 |

